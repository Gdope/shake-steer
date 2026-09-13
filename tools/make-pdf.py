# -*- coding: utf-8 -*-
"""
make-pdf.py — builds the two downloadable menu PDFs.

    python tools/make-pdf.py

Writes:
    downloads/shake-and-steer-menu-en.pdf   (English)
    downloads/shake-and-steer-menu-sr.pdf   (Serbian)

The cocktail list lives in tools/menu_data.py — edit that file, re-run this
script, and both PDFs are regenerated. No external libraries are needed; the
PDF writer is tools/pdfkit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import menu_data                      # noqa: E402
from pdfkit import PDF, A4            # noqa: E402


# ---------------------------------------------------------------------------
# Brand colours, tuned for paper rather than screen
# ---------------------------------------------------------------------------
PAPER = (0.984, 0.973, 0.957)   # warm ivory
INK = (0.165, 0.133, 0.169)
MUTED = (0.420, 0.376, 0.439)
BORDO = (0.420, 0.078, 0.188)
PLUM = (0.227, 0.106, 0.290)
GOLD = (0.600, 0.447, 0.196)    # darker gold so it stays legible in print
HAIRLINE = (0.855, 0.827, 0.800)

DARK = (0.082, 0.051, 0.110)    # cover background
GOLD_LIGHT = (0.788, 0.639, 0.369)
CHAMPAGNE = (0.941, 0.886, 0.769)

# ---------------------------------------------------------------------------
# Page geometry (A4)
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN_X = 56.0
MARGIN_TOP = 64.0
MARGIN_BOTTOM = 58.0
CONTENT_W = PAGE_W - 2 * MARGIN_X
BODY_TOP = PAGE_H - MARGIN_TOP - 24.0     # below the running header
BODY_BOTTOM = MARGIN_BOTTOM + 18.0        # above the page number

FRONT_MATTER_PAGES = 2                    # cover + "about this list"

# ---------------------------------------------------------------------------
# Fonts — Windows system fonts, with fallbacks
# ---------------------------------------------------------------------------
FONT_CANDIDATES = {
    "serif": ["pala.ttf", "georgia.ttf", "times.ttf", "constan.ttf"],
    "serif_bold": ["palab.ttf", "georgiab.ttf", "timesbd.ttf", "constanb.ttf"],
    "serif_italic": ["palai.ttf", "georgiai.ttf", "timesi.ttf", "constani.ttf"],
    "sans": ["trebuc.ttf", "verdana.ttf", "arial.ttf", "segoeui.ttf"],
    "sans_bold": ["trebucbd.ttf", "verdanab.ttf", "arialbd.ttf", "segoeuib.ttf"],
}

FONT_DIRS = [
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
    os.path.join(HERE, "fonts"),
    "/usr/share/fonts/truetype/msttcorefonts",
    "/Library/Fonts",
]


def find_font(filenames):
    for directory in FONT_DIRS:
        for name in filenames:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                return path
    raise SystemExit(
        "Could not find any of these fonts: %s\n"
        "Put a .ttf with one of those names in tools/fonts/ and run again."
        % ", ".join(filenames)
    )


# ---------------------------------------------------------------------------
# Small drawing helpers
# ---------------------------------------------------------------------------
def draw_glass(pdf, cx, base_y, scale=1.0, color=GOLD_LIGHT, width=1.1):
    """A minimal Art-Deco coupe/martini outline, drawn from straight lines."""
    bowl_w = 34 * scale
    bowl_h = 26 * scale
    stem_h = 26 * scale
    foot_w = 20 * scale

    top = base_y + stem_h + bowl_h
    pdf.line(cx - bowl_w, top, cx + bowl_w, top, color, width)
    pdf.line(cx - bowl_w, top, cx, base_y + stem_h, color, width)
    pdf.line(cx + bowl_w, top, cx, base_y + stem_h, color, width)
    pdf.line(cx, base_y + stem_h, cx, base_y, color, width)
    pdf.line(cx - foot_w, base_y, cx + foot_w, base_y, color, width)


def draw_frame(pdf, inset, color, width=0.8, double=True):
    """A thin rectangle just inside the page edge, optionally doubled."""
    x0, y0 = inset, inset
    x1, y1 = PAGE_W - inset, PAGE_H - inset
    for offset in ((0,) if not double else (0, 5)):
        a, b = x0 + offset, y0 + offset
        c, d = x1 - offset, y1 - offset
        pdf.line(a, b, c, b, color, width)
        pdf.line(c, b, c, d, color, width)
        pdf.line(c, d, a, d, color, width)
        pdf.line(a, d, a, b, color, width)
        width *= 0.5


# ---------------------------------------------------------------------------
# The document builder
# ---------------------------------------------------------------------------
class MenuDocument(object):
    def __init__(self, lang, category_pages=None):
        self.lang = lang
        self.copy = menu_data.FRONT[lang]
        self.category_pages = category_pages or {}
        self.measured = {}          # category index -> page it starts on
        self.page_no = 0
        self.current_category = ""

        self.pdf = PDF(
            page_size=A4,
            title="%s - %s" % (menu_data.BRAND, self.copy["doc_title"]),
            author=menu_data.BRAND,
            subject="Full cocktail menu",
        )
        for key, names in FONT_CANDIDATES.items():
            self.pdf.add_font(key, find_font(names))

    # -- page furniture -----------------------------------------------------
    def start_page(self, background=PAPER):
        self.pdf.new_page()
        self.page_no += 1
        self.pdf.rect(0, 0, PAGE_W, PAGE_H, background)
        self.y = BODY_TOP

    def running_header(self):
        pdf = self.pdf
        y = PAGE_H - MARGIN_TOP + 12
        pdf.text(MARGIN_X, y, menu_data.BRAND.upper(), "sans", 6.6, GOLD, spacing=2.2)
        if self.current_category:
            pdf.text_right(PAGE_W - MARGIN_X, y, self.current_category.upper(),
                           "sans", 6.6, MUTED, spacing=2.0)
        pdf.line(MARGIN_X, y - 8, PAGE_W - MARGIN_X, y - 8, HAIRLINE, 0.6)

    def page_footer(self):
        pdf = self.pdf
        y = MARGIN_BOTTOM - 16
        pdf.line(MARGIN_X, y + 14, PAGE_W - MARGIN_X, y + 14, HAIRLINE, 0.6)
        pdf.text_center(PAGE_W / 2.0, y, "%02d" % self.page_no, "serif", 8.2, MUTED,
                        spacing=1.2)

    def new_content_page(self):
        self.start_page()
        self.running_header()
        self.page_footer()

    def space_left(self):
        return self.y - BODY_BOTTOM

    def need(self, height):
        """Start a new page if `height` points will not fit."""
        if self.space_left() < height:
            self.new_content_page()

    # -- cover --------------------------------------------------------------
    def build_cover(self):
        pdf = self.pdf
        self.start_page(DARK)

        # A soft burgundy band behind the title block
        pdf.rect(0, PAGE_H * 0.40, PAGE_W, PAGE_H * 0.22, (0.145, 0.063, 0.125))
        draw_frame(pdf, 26, GOLD_LIGHT, 0.9)

        pdf.text_center(PAGE_W / 2.0, PAGE_H - 150,
                        "MOBILE COCKTAIL BAR", "sans", 7.6, GOLD_LIGHT, spacing=4.4)

        pdf.text_center(PAGE_W / 2.0, PAGE_H - 232, menu_data.BRAND,
                        "serif", 46, CHAMPAGNE, spacing=1.0)

        pdf.line(PAGE_W / 2.0 - 70, PAGE_H - 258, PAGE_W / 2.0 + 70,
                 PAGE_H - 258, GOLD_LIGHT, 0.7)

        pdf.text_center(PAGE_W / 2.0, PAGE_H - 288, self.copy["tagline"],
                        "serif_italic", 13, GOLD_LIGHT)

        pdf.text_center(PAGE_W / 2.0, PAGE_H - 372, self.copy["doc_title"],
                        "serif", 21, CHAMPAGNE, spacing=0.6)

        pdf.text_center(PAGE_W / 2.0, PAGE_H - 396,
                        "%d %s" % (menu_data.count(), self.copy["drinks"]),
                        "sans", 8.4, GOLD_LIGHT, spacing=3.0)

        draw_glass(pdf, PAGE_W / 2.0, 190, 1.25)

        pdf.line(PAGE_W / 2.0 - 40, 150, PAGE_W / 2.0 + 40, 150, GOLD_LIGHT, 0.6)
        pdf.text_center(PAGE_W / 2.0, 120, self.copy["edition"],
                        "sans", 7.4, (0.55, 0.50, 0.58), spacing=1.6)

    # -- "about this list" + contents ---------------------------------------
    def build_front_matter(self):
        pdf = self.pdf
        self.start_page()
        self.page_footer()

        y = PAGE_H - 120
        pdf.text(MARGIN_X, y, self.copy["intro_title"].upper(), "sans", 7.4, GOLD,
                 spacing=3.2)
        y -= 30

        for line in pdf.wrap(self.copy["intro"], "serif", 10.4, CONTENT_W - 40):
            pdf.text(MARGIN_X, y, line, "serif", 10.4, INK)
            y -= 16.5

        y -= 24
        pdf.line(MARGIN_X, y, PAGE_W - MARGIN_X, y, HAIRLINE, 0.7)
        y -= 34

        pdf.text(MARGIN_X, y, self.copy["contents"].upper(), "sans", 7.4, GOLD,
                 spacing=3.2)
        y -= 30

        for index, category in enumerate(menu_data.CATEGORIES):
            name = category[0] if self.lang == "en" else category[1]
            items = len(category[4])
            page = self.category_pages.get(index)

            pdf.text(MARGIN_X + 4, y, "%02d" % (index + 1), "serif_italic", 9.5, GOLD)
            pdf.text(MARGIN_X + 30, y, name, "serif", 12.5, INK)

            label = "%d %s" % (items, self.copy["drinks"])
            if page:
                label += "   ·   %s %d" % (self.copy["page"], page)
            pdf.text_right(PAGE_W - MARGIN_X, y, label, "sans", 8.2, MUTED)

            y -= 12
            pdf.line(MARGIN_X + 30, y, PAGE_W - MARGIN_X, y, HAIRLINE, 0.5)
            y -= 20

    # -- one cocktail --------------------------------------------------------
    def entry_height(self, entry):
        desc = entry[1] if self.lang == "en" else entry[3]
        ingredients = entry[2] if self.lang == "en" else entry[4]

        desc_lines = len(self.pdf.wrap(desc, "serif_italic", 9.4, CONTENT_W - 12))
        ing_lines = len(self.pdf.wrap(ingredients, "sans", 7.8, CONTENT_W - 74))
        return 16 + desc_lines * 12.6 + 6 + max(1, ing_lines) * 10.4 + 16

    def draw_entry(self, entry):
        pdf = self.pdf
        name = entry[0]
        desc = entry[1] if self.lang == "en" else entry[3]
        ingredients = entry[2] if self.lang == "en" else entry[4]

        pdf.text(MARGIN_X, self.y, name, "serif_bold", 11.8, BORDO, spacing=0.3)
        self.y -= 16

        for line in pdf.wrap(desc, "serif_italic", 9.4, CONTENT_W - 12):
            pdf.text(MARGIN_X, self.y, line, "serif_italic", 9.4, INK)
            self.y -= 12.6

        self.y -= 6
        label = self.copy["ingredients"].upper()
        pdf.text(MARGIN_X, self.y, label, "sans_bold", 6.6, GOLD, spacing=1.8)

        indent = 74
        lines = pdf.wrap(ingredients, "sans", 7.8, CONTENT_W - indent)
        for i, line in enumerate(lines):
            pdf.text(MARGIN_X + indent, self.y, line, "sans", 7.8, MUTED)
            if i < len(lines) - 1:
                self.y -= 10.4
        self.y -= 16

        pdf.line(MARGIN_X, self.y + 6, PAGE_W - MARGIN_X, self.y + 6, HAIRLINE, 0.4)

    # -- one category --------------------------------------------------------
    def draw_category(self, index, category):
        pdf = self.pdf
        name_en, name_sr, note_en, note_sr, entries = category
        name = name_en if self.lang == "en" else name_sr
        note = note_en if self.lang == "en" else note_sr

        # Start a chapter on a fresh page unless there is real room left
        if self.page_no <= FRONT_MATTER_PAGES or self.space_left() < 260:
            self.current_category = name
            self.new_content_page()
        else:
            self.current_category = name
            self.y -= 26

        self.measured[index] = self.page_no

        pdf.text(MARGIN_X, self.y, "%02d" % (index + 1), "serif_italic", 10, GOLD,
                 spacing=1.0)
        self.y -= 26

        pdf.text(MARGIN_X, self.y, name, "serif", 23, PLUM, spacing=0.4)
        self.y -= 20

        for line in pdf.wrap(note, "serif_italic", 9.6, CONTENT_W - 90):
            pdf.text(MARGIN_X, self.y, line, "serif_italic", 9.6, MUTED)
            self.y -= 13

        self.y -= 8
        pdf.line(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y, GOLD, 0.8)
        self.y -= 26

        for entry in entries:
            height = self.entry_height(entry)
            if self.space_left() < height:
                self.new_content_page()
            self.draw_entry(entry)

    # -- back page -----------------------------------------------------------
    def build_back(self):
        pdf = self.pdf
        self.start_page(DARK)
        draw_frame(pdf, 26, GOLD_LIGHT, 0.9)

        cx = PAGE_W / 2.0
        draw_glass(pdf, cx, PAGE_H - 220, 1.0)

        pdf.text_center(cx, PAGE_H - 300, menu_data.BRAND, "serif", 30, CHAMPAGNE,
                        spacing=0.8)
        pdf.line(cx - 60, PAGE_H - 324, cx + 60, PAGE_H - 324, GOLD_LIGHT, 0.7)

        pdf.text_center(cx, PAGE_H - 366, self.copy["back_title"], "serif_italic",
                        15, GOLD_LIGHT)

        y = PAGE_H - 404
        for line in pdf.wrap(self.copy["back_text"], "serif", 10.2, CONTENT_W - 120):
            pdf.text_center(cx, y, line, "serif", 10.2, (0.82, 0.79, 0.85))
            y -= 15.5

        # ---- contact block: PLACEHOLDERS -----------------------------------
        y -= 40
        pdf.text_center(cx, y, self.copy["placeholder_note"].upper(), "sans", 6.6,
                        (0.72, 0.55, 0.35), spacing=2.6)
        y -= 34

        contact = menu_data.CONTACT
        for value in (contact["email"], contact["phone"], contact["web"],
                      contact["social"], contact["city"]):
            pdf.text_center(cx, y, value, "serif", 11.5, CHAMPAGNE, spacing=0.6)
            y -= 20

        pdf.line(cx - 40, 128, cx + 40, 128, GOLD_LIGHT, 0.6)
        pdf.text_center(cx, 104, self.copy["back_note"], "sans", 7.2,
                        (0.55, 0.50, 0.58), spacing=2.0)

    # -- assemble ------------------------------------------------------------
    def build(self):
        self.build_cover()
        self.build_front_matter()
        for index, category in enumerate(menu_data.CATEGORIES):
            self.draw_category(index, category)
        self.build_back()
        return self.measured


def build(lang, out_path):
    """Two passes: the first works out page numbers for the contents page."""
    first = MenuDocument(lang)
    pages = first.build()

    final = MenuDocument(lang, category_pages=pages)
    final.build()
    size = final.pdf.save(out_path)
    return size, final.page_no


def main():
    out_dir = os.path.join(ROOT, "downloads")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    print("Building menu PDFs (%d cocktails)..." % menu_data.count())
    for lang, filename in (("en", "shake-and-steer-menu-en.pdf"),
                           ("sr", "shake-and-steer-menu-sr.pdf")):
        path = os.path.join(out_dir, filename)
        size, pages = build(lang, path)
        print("  %-34s %2d pages  %6.1f KB" % (filename, pages, size / 1024.0))
    print("Done.")


if __name__ == "__main__":
    main()
