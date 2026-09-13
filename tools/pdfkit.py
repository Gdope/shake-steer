# -*- coding: utf-8 -*-
"""
pdfkit.py — a very small, dependency-free PDF writer.

It exists so the two menu PDFs in /downloads/ can be regenerated without
installing anything (no reportlab, no npm, no LaTeX). It supports exactly what
the Shake&Steer menu needs and nothing more:

  * A4 pages, filled rectangles and hairline rules
  * Embedded TrueType fonts, subsetted, via Type0 / Identity-H
    (needed for Serbian characters like č ć š ž đ)
  * Text drawing with left / centre alignment and word wrapping
  * A /ToUnicode map so text can still be copied out of the PDF
  * Flate compression for page content and font files

Not a general-purpose library — just enough machinery, kept readable.
"""

import struct
import zlib


# ---------------------------------------------------------------------------
# TrueType parsing + subsetting
# ---------------------------------------------------------------------------
class TrueTypeFont(object):
    """Reads the handful of TrueType tables a PDF needs, and can subset them."""

    def __init__(self, path):
        with open(path, "rb") as handle:
            self.data = handle.read()

        if self.data[:4] not in (b"\x00\x01\x00\x00", b"true", b"ttcf"):
            raise ValueError("%s is not a plain TrueType font" % path)

        num_tables = struct.unpack(">H", self.data[4:6])[0]
        self.tables = {}
        for i in range(num_tables):
            base = 12 + i * 16
            tag = self.data[base:base + 4].decode("latin-1")
            offset, length = struct.unpack(">II", self.data[base + 8:base + 16])
            self.tables[tag] = (offset, length)

        self._read_head()
        self._read_metrics()
        self._read_cmap()
        self._read_loca()

    # -- table readers ------------------------------------------------------
    def _table(self, tag):
        if tag not in self.tables:
            return None
        offset, length = self.tables[tag]
        return self.data[offset:offset + length]

    def _read_head(self):
        head = self._table("head")
        self.units_per_em = struct.unpack(">H", head[18:20])[0]
        self.x_min, self.y_min, self.x_max, self.y_max = struct.unpack(
            ">hhhh", head[36:44]
        )
        self.index_to_loc_format = struct.unpack(">h", head[50:52])[0]

        maxp = self._table("maxp")
        self.num_glyphs = struct.unpack(">H", maxp[4:6])[0]

        hhea = self._table("hhea")
        self.ascender, self.descender = struct.unpack(">hh", hhea[4:8])
        self.num_h_metrics = struct.unpack(">H", hhea[34:36])[0]

        os2 = self._table("OS/2")
        self.cap_height = self.ascender
        if os2 and len(os2) >= 90 and struct.unpack(">H", os2[0:2])[0] >= 2:
            self.cap_height = struct.unpack(">h", os2[88:90])[0] or self.ascender

        post = self._table("post")
        self.italic_angle = 0.0
        if post and len(post) >= 8:
            whole, frac = struct.unpack(">hH", post[4:8])
            self.italic_angle = whole + frac / 65536.0

    def _read_metrics(self):
        hmtx = self._table("hmtx")
        self.advances = []
        last = 0
        for i in range(self.num_glyphs):
            if i < self.num_h_metrics:
                last = struct.unpack(">H", hmtx[i * 4:i * 4 + 2])[0]
            self.advances.append(last)

    def _read_cmap(self):
        """Build a unicode -> glyph id map from the best available subtable."""
        cmap = self._table("cmap")
        count = struct.unpack(">H", cmap[2:4])[0]
        best = None
        best_score = -1
        for i in range(count):
            platform, encoding, offset = struct.unpack(
                ">HHI", cmap[4 + i * 8:12 + i * 8]
            )
            # Prefer Windows full-repertoire (3,10), then Windows BMP (3,1)
            score = {(3, 10): 3, (3, 1): 2, (0, 4): 2, (0, 3): 1}.get(
                (platform, encoding), 0
            )
            if score > best_score:
                best_score, best = score, offset

        self.cmap = {}
        fmt = struct.unpack(">H", cmap[best:best + 2])[0]

        if fmt == 4:
            seg_x2 = struct.unpack(">H", cmap[best + 6:best + 8])[0]
            segs = seg_x2 // 2
            ends = best + 14
            starts = ends + seg_x2 + 2
            deltas = starts + seg_x2
            ranges = deltas + seg_x2
            for s in range(segs):
                end = struct.unpack(">H", cmap[ends + s * 2:ends + s * 2 + 2])[0]
                start = struct.unpack(">H", cmap[starts + s * 2:starts + s * 2 + 2])[0]
                delta = struct.unpack(">h", cmap[deltas + s * 2:deltas + s * 2 + 2])[0]
                range_off = struct.unpack(">H", cmap[ranges + s * 2:ranges + s * 2 + 2])[0]
                if start == 0xFFFF:
                    continue
                for code in range(start, end + 1):
                    if range_off == 0:
                        gid = (code + delta) & 0xFFFF
                    else:
                        pos = ranges + s * 2 + range_off + (code - start) * 2
                        if pos + 2 > len(cmap):
                            continue
                        gid = struct.unpack(">H", cmap[pos:pos + 2])[0]
                        if gid:
                            gid = (gid + delta) & 0xFFFF
                    if gid:
                        self.cmap[code] = gid

        elif fmt == 12:
            n_groups = struct.unpack(">I", cmap[best + 12:best + 16])[0]
            for g in range(n_groups):
                base = best + 16 + g * 12
                start, end, start_gid = struct.unpack(">III", cmap[base:base + 12])
                for code in range(start, min(end, start + 0x10000) + 1):
                    self.cmap[code] = start_gid + (code - start)

        else:
            raise ValueError("Unsupported cmap format %d" % fmt)

    def _read_loca(self):
        loca = self._table("loca")
        self.loca = []
        if self.index_to_loc_format == 0:
            for i in range(self.num_glyphs + 1):
                self.loca.append(
                    struct.unpack(">H", loca[i * 2:i * 2 + 2])[0] * 2
                )
        else:
            for i in range(self.num_glyphs + 1):
                self.loca.append(struct.unpack(">I", loca[i * 4:i * 4 + 4])[0])

    # -- public helpers -----------------------------------------------------
    def glyph_id(self, char):
        """Glyph for a character, falling back to a space then .notdef."""
        return self.cmap.get(ord(char)) or self.cmap.get(32) or 0

    def advance(self, gid):
        """Advance width in 1/1000 em, the unit PDF wants."""
        if gid >= len(self.advances):
            return 0
        return int(round(self.advances[gid] * 1000.0 / self.units_per_em))

    def text_width(self, text, size):
        """Width of `text` at `size` points."""
        total = 0
        for char in text:
            total += self.advance(self.glyph_id(char))
        return total * size / 1000.0

    # -- subsetting ---------------------------------------------------------
    def _glyph_data(self, gid):
        glyf_off = self.tables["glyf"][0]
        start, end = self.loca[gid], self.loca[gid + 1]
        if end <= start:
            return b""
        return self.data[glyf_off + start:glyf_off + end]

    def _components(self, gid):
        """Glyph ids referenced by a composite glyph."""
        raw = self._glyph_data(gid)
        if len(raw) < 10:
            return []
        if struct.unpack(">h", raw[0:2])[0] >= 0:
            return []  # simple glyph

        out = []
        pos = 10
        while pos + 4 <= len(raw):
            flags, index = struct.unpack(">HH", raw[pos:pos + 4])
            out.append(index)
            pos += 4
            pos += 4 if flags & 0x0001 else 2      # arguments
            if flags & 0x0008:
                pos += 2                            # single scale
            elif flags & 0x0040:
                pos += 4                            # x and y scale
            elif flags & 0x0080:
                pos += 8                            # 2x2 transform
            if not flags & 0x0020:                  # MORE_COMPONENTS
                break
        return out

    def subset(self, gids):
        """
        Build a slimmed-down TrueType file containing only `gids`.

        Glyph ids are preserved (unused glyphs simply become empty), which
        keeps /CIDToGIDMap /Identity valid and the code simple.
        """
        keep = set(gids) | {0}

        # Pull in the parts of composite glyphs
        pending = list(keep)
        while pending:
            gid = pending.pop()
            for component in self._components(gid):
                if component not in keep:
                    keep.add(component)
                    pending.append(component)

        # Rebuild glyf + loca
        glyf = bytearray()
        loca = []
        for gid in range(self.num_glyphs):
            loca.append(len(glyf))
            if gid in keep:
                raw = self._glyph_data(gid)
                glyf += raw
                while len(glyf) % 4:      # keep glyphs 4-byte aligned
                    glyf += b"\x00"
        loca.append(len(glyf))

        new_loca = b"".join(struct.pack(">I", value) for value in loca)

        # head with indexToLocFormat forced to "long"
        head = bytearray(self._table("head"))
        head[8:12] = b"\x00\x00\x00\x00"             # checkSumAdjustment
        head[50:52] = struct.pack(">h", 1)

        tables = {
            "head": bytes(head),
            "hhea": self._table("hhea"),
            "maxp": self._table("maxp"),
            "hmtx": self._table("hmtx"),
            "loca": new_loca,
            "glyf": bytes(glyf),
        }
        # 'cmap' is not needed by PDF (CIDToGIDMap is Identity) but keeping the
        # original makes the embedded font program valid on its own, which some
        # strict PDF validators are happier about. Glyph ids are unchanged, so
        # the table stays correct.
        for optional in ("cmap", "cvt ", "fpgm", "prep", "OS/2"):
            block = self._table(optional)
            if block:
                tables[optional] = block

        return _build_ttf(tables)


def _build_ttf(tables):
    """Assemble a TrueType file from a {tag: bytes} mapping."""
    tags = sorted(tables)
    count = len(tags)

    # searchRange / entrySelector / rangeShift, per the spec
    entry_selector = 0
    while (1 << (entry_selector + 1)) <= count:
        entry_selector += 1
    search_range = (1 << entry_selector) * 16
    range_shift = count * 16 - search_range

    header = struct.pack(
        ">IHHHH", 0x00010000, count, search_range, entry_selector, range_shift
    )

    offset = 12 + count * 16
    directory = b""
    body = b""
    for tag in tags:
        block = tables[tag]
        padded = block + b"\x00" * ((4 - len(block) % 4) % 4)
        checksum = 0
        for i in range(0, len(padded), 4):
            checksum = (checksum + struct.unpack(">I", padded[i:i + 4])[0]) & 0xFFFFFFFF
        directory += tag.encode("latin-1") + struct.pack(
            ">III", checksum, offset, len(block)
        )
        body += padded
        offset += len(padded)

    return header + directory + body


# ---------------------------------------------------------------------------
# The PDF document
# ---------------------------------------------------------------------------
A4 = (595.28, 841.89)


class Font(object):
    """One embedded font inside a document."""

    def __init__(self, name, path):
        self.name = name           # the /F1 style resource name
        self.ttf = TrueTypeFont(path)
        self.used = {}             # gid -> unicode code point (for /ToUnicode)

    def encode(self, text):
        """Text -> Identity-H hex string, recording which glyphs were used."""
        out = []
        for char in text:
            gid = self.ttf.glyph_id(char)
            self.used[gid] = ord(char)
            out.append("%04X" % gid)
        return "".join(out)

    def width(self, text, size):
        return self.ttf.text_width(text, size)


class PDF(object):
    def __init__(self, page_size=A4, title="", author="", subject=""):
        self.width, self.height = page_size
        self.fonts = {}
        self.pages = []            # list of content-stream strings
        self._buffer = []
        self.title = title
        self.author = author
        self.subject = subject

    # -- fonts --------------------------------------------------------------
    def add_font(self, key, path):
        font = Font("F%d" % (len(self.fonts) + 1), path)
        self.fonts[key] = font
        return font

    # -- pages --------------------------------------------------------------
    def new_page(self):
        if self._buffer:
            self.pages.append("".join(self._buffer))
        self._buffer = []

    def finish_page(self):
        if self._buffer:
            self.pages.append("".join(self._buffer))
            self._buffer = []

    def _emit(self, chunk):
        self._buffer.append(chunk)

    # -- drawing ------------------------------------------------------------
    def rect(self, x, y, w, h, color):
        r, g, b = color
        self._emit("q %.3f %.3f %.3f rg %.2f %.2f %.2f %.2f re f Q\n"
                   % (r, g, b, x, y, w, h))

    def line(self, x1, y1, x2, y2, color, width=0.5):
        r, g, b = color
        self._emit("q %.3f %.3f %.3f RG %.2f w %.2f %.2f m %.2f %.2f l S Q\n"
                   % (r, g, b, width, x1, y1, x2, y2))

    def text(self, x, y, string, font_key, size, color=(0, 0, 0), spacing=0.0):
        """Draw one line of text with its baseline at (x, y)."""
        if not string:
            return
        font = self.fonts[font_key]
        r, g, b = color
        self._emit(
            "BT %.3f %.3f %.3f rg /%s %.2f Tf %.2f Tc %.2f %.2f Td <%s> Tj ET\n"
            % (r, g, b, font.name, size, spacing, x, y, font.encode(string))
        )

    def text_center(self, cx, y, string, font_key, size, color=(0, 0, 0), spacing=0.0):
        font = self.fonts[font_key]
        width = font.width(string, size) + spacing * max(0, len(string) - 1)
        self.text(cx - width / 2.0, y, string, font_key, size, color, spacing)

    def text_right(self, rx, y, string, font_key, size, color=(0, 0, 0), spacing=0.0):
        font = self.fonts[font_key]
        width = font.width(string, size) + spacing * max(0, len(string) - 1)
        self.text(rx - width, y, string, font_key, size, color, spacing)

    def wrap(self, string, font_key, size, max_width):
        """Split a string into lines that fit inside `max_width` points."""
        font = self.fonts[font_key]
        words = string.split()
        lines = []
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if font.width(candidate, size) <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    # -- output -------------------------------------------------------------
    def save(self, path):
        self.finish_page()

        objects = []           # list of byte strings, 1-indexed on output

        def add(obj):
            objects.append(obj)
            return len(objects)

        # Reserve: 1 catalog, 2 pages tree
        catalog_id = add(b"")
        pages_id = add(b"")

        # -- fonts -----------------------------------------------------------
        font_refs = {}
        for key, font in self.fonts.items():
            ttf = font.ttf
            gids = sorted(font.used)
            program = ttf.subset(gids)
            compressed = zlib.compress(program, 9)

            file_id = add(
                b"<< /Length " + str(len(compressed)).encode() +
                b" /Length1 " + str(len(program)).encode() +
                b" /Filter /FlateDecode >>\nstream\n" + compressed + b"\nendstream"
            )

            scale = 1000.0 / ttf.units_per_em
            flags = 4 | (64 if abs(ttf.italic_angle) > 0.01 else 0)
            descriptor_id = add((
                "<< /Type /FontDescriptor /FontName /%s /Flags %d "
                "/FontBBox [%d %d %d %d] /ItalicAngle %.1f /Ascent %d "
                "/Descent %d /CapHeight %d /StemV 80 /FontFile2 %d 0 R >>"
                % (font.name, flags,
                   int(ttf.x_min * scale), int(ttf.y_min * scale),
                   int(ttf.x_max * scale), int(ttf.y_max * scale),
                   ttf.italic_angle, int(ttf.ascender * scale),
                   int(ttf.descender * scale), int(ttf.cap_height * scale),
                   file_id)
            ).encode("latin-1"))

            # /W: widths, grouped into runs of consecutive glyph ids
            runs = []
            run_start = None
            run = []
            for gid in gids:
                if run_start is not None and gid == run_start + len(run):
                    run.append(ttf.advance(gid))
                else:
                    if run:
                        runs.append((run_start, run))
                    run_start, run = gid, [ttf.advance(gid)]
            if run:
                runs.append((run_start, run))
            widths = " ".join(
                "%d [%s]" % (start, " ".join(str(w) for w in values))
                for start, values in runs
            )

            descendant_id = add((
                "<< /Type /Font /Subtype /CIDFontType2 /BaseFont /%s "
                "/CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) "
                "/Supplement 0 >> /FontDescriptor %d 0 R /DW 1000 /W [%s] "
                "/CIDToGIDMap /Identity >>"
                % (font.name, descriptor_id, widths)
            ).encode("latin-1"))

            # /ToUnicode so the text stays selectable and copyable
            mappings = "".join(
                "<%04X> <%04X>\n" % (gid, code) for gid, code in sorted(font.used.items())
            )
            cmap = (
                "/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
                "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
                "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n"
                "1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n"
                "%d beginbfchar\n%sendbfchar\nendcmap\n"
                "CMapName currentdict /CMap defineresource pop\nend\nend"
                % (len(font.used), mappings)
            ).encode("utf-8")
            cmap_compressed = zlib.compress(cmap, 9)
            tounicode_id = add(
                b"<< /Length " + str(len(cmap_compressed)).encode() +
                b" /Filter /FlateDecode >>\nstream\n" + cmap_compressed + b"\nendstream"
            )

            font_id = add((
                "<< /Type /Font /Subtype /Type0 /BaseFont /%s /Encoding /Identity-H "
                "/DescendantFonts [%d 0 R] /ToUnicode %d 0 R >>"
                % (font.name, descendant_id, tounicode_id)
            ).encode("latin-1"))

            font_refs[font.name] = font_id

        resources = "<< /Font << %s >> >>" % " ".join(
            "/%s %d 0 R" % (name, ref) for name, ref in sorted(font_refs.items())
        )

        # -- pages -----------------------------------------------------------
        page_ids = []
        for content in self.pages:
            raw = content.encode("latin-1")
            compressed = zlib.compress(raw, 9)
            content_id = add(
                b"<< /Length " + str(len(compressed)).encode() +
                b" /Filter /FlateDecode >>\nstream\n" + compressed + b"\nendstream"
            )
            page_id = add((
                "<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] "
                "/Resources %s /Contents %d 0 R >>"
                % (pages_id, self.width, self.height, resources, content_id)
            ).encode("latin-1"))
            page_ids.append(page_id)

        objects[pages_id - 1] = (
            "<< /Type /Pages /Count %d /Kids [%s] >>"
            % (len(page_ids), " ".join("%d 0 R" % pid for pid in page_ids))
        ).encode("latin-1")

        objects[catalog_id - 1] = (
            "<< /Type /Catalog /Pages %d 0 R >>" % pages_id
        ).encode("latin-1")

        info_id = add((
            "<< /Title (%s) /Author (%s) /Subject (%s) /Creator (Shake&Steer) >>"
            % (_escape(self.title), _escape(self.author), _escape(self.subject))
        ).encode("latin-1"))

        # -- serialise --------------------------------------------------------
        out = bytearray(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(out))
            out += str(index).encode() + b" 0 obj\n" + obj + b"\nendobj\n"

        xref_pos = len(out)
        out += b"xref\n0 " + str(len(objects) + 1).encode() + b"\n"
        out += b"0000000000 65535 f \n"
        for offset in offsets[1:]:
            out += ("%010d 00000 n \n" % offset).encode()

        out += (
            "trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objects) + 1, catalog_id, info_id, xref_pos)
        ).encode("latin-1")

        with open(path, "wb") as handle:
            handle.write(bytes(out))

        return len(out)


def _escape(text):
    """Escape a string for a PDF literal (…) — ASCII only, for metadata."""
    safe = text.encode("ascii", "replace").decode("ascii")
    return safe.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
