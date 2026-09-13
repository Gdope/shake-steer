# -*- coding: utf-8 -*-
"""
make-images.py — generates the SVG placeholder artwork in /assets/img/.

You do NOT need to run this to use the website. It is kept in the repo only
so the placeholder images can be regenerated or re-coloured later.

    python tools/make-images.py

Everything it writes is a placeholder: replace the files in /assets/img/ with
real photographs (keep the same file names and nothing else has to change).
"""

import os
import math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

# ---------------------------------------------------------------------------
# Brand palette (matches the CSS custom properties in assets/css/base.css)
# ---------------------------------------------------------------------------
PLUM_DEEP = "#150d1c"
GOLD = "#c9a35e"
GOLD_SOFT = "#f0e2c4"

# Per-drink colour pairs: (deep background tone, liquid tone)
DRINK_COLORS = [
    ("#3b1550", "#e0563c"),  # 01 amber / smoky
    ("#2a0f3d", "#f2c14e"),  # 02 gold
    ("#4a1030", "#e35a7a"),  # 03 rose
    ("#1c1240", "#6fd0c8"),  # 04 aqua
    ("#3d0f24", "#8e1c3f"),  # 05 burgundy
    ("#251142", "#b47ae8"),  # 06 violet
    ("#123324", "#7fd67f"),  # 07 herbal green
    ("#40200c", "#d98a3a"),  # 08 spiced orange
    ("#0f1a3a", "#5b8dee"),  # 09 midnight blue
    ("#2d1030", "#efe3c8"),  # 10 champagne
]

GALLERY_COLORS = [
    ("#2b1140", "#8e1c3f"),
    ("#3d1028", "#7c3fa3"),
    ("#1b1038", "#c9a35e"),
    ("#42142c", "#b47ae8"),
    ("#1d1430", "#e0563c"),
    ("#33103c", "#f2c14e"),
    ("#221038", "#6fd0c8"),
    ("#3a1124", "#e35a7a"),
    ("#141a3a", "#c9a35e"),
    ("#2e1236", "#8e1c3f"),
    ("#1a1030", "#d98a3a"),
    ("#3c1030", "#7c3fa3"),
]


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(svg)
    print("  wrote", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------------------
# Glassware silhouettes. Each entry returns the SVG for one glass, drawn in a
# 400 x 500 box: (outline path, liquid path, extra decoration).
# ---------------------------------------------------------------------------
def stem(top, base_y, rx=52):
    """Stem + foot shared by the stemmed glasses, as raw path data."""
    ry = 9
    return (
        ' M196,{t} L196,{b}'
        ' M204,{t} L204,{b}'
        ' M{x0},{b} a{rx},{ry} 0 1,0 {d},0 a{rx},{ry} 0 1,0 -{d},0 Z'
    ).format(t=top, b=base_y, rx=rx, ry=ry, x0=200 - rx, d=rx * 2)


GLASSES = {
    "coupe": {
        "glass": 'M118,196 L282,196 C280,250 246,288 200,288 C154,288 120,250 118,196 Z'
                 + stem(288, 396),
        "liquid": 'M129,210 L271,210 C266,250 238,274 200,274 C162,274 134,250 129,210 Z',
    },
    "martini": {
        "glass": 'M104,186 L296,186 L200,304 Z' + stem(304, 400),
        "liquid": 'M124,204 L276,204 L200,297 Z',
    },
    "highball": {
        "glass": 'M152,150 L248,150 L242,408 L158,408 Z',
        "liquid": 'M158,206 L242,206 L237,400 L163,400 Z',
    },
    "rocks": {
        "glass": 'M140,236 L260,236 L252,404 L148,404 Z',
        "liquid": 'M147,282 L253,282 L246,396 L154,396 Z',
    },
    "flute": {
        "glass": 'M176,130 C176,236 186,296 196,308 L204,308 C214,296 224,236 224,130 Z'
                 + stem(308, 402, 44),
        "liquid": 'M179,168 C180,240 188,292 197,302 L203,302 C212,292 220,240 221,168 Z',
    },
    "copa": {
        "glass": 'M134,184 C134,272 163,318 200,318 C237,318 266,272 266,184 '
                 'C266,170 134,170 134,184 Z' + stem(318, 402),
        "liquid": 'M144,216 C150,282 172,306 200,306 C228,306 250,282 256,216 Z',
    },
    "hurricane": {
        "glass": 'M158,146 C147,226 176,248 172,302 C170,336 184,352 200,352 '
                 'C216,352 230,336 228,302 C224,248 253,226 242,146 Z'
                 + stem(352, 404, 46),
        "liquid": 'M166,206 C162,248 178,254 174,300 C172,332 185,344 200,344 '
                  'C215,344 228,332 226,300 C222,254 238,248 234,206 Z',
    },
    "tiki": {
        "glass": 'M154,188 L246,188 L238,404 L162,404 Z'
                 'M246,224 C284,228 284,292 246,296',
        "liquid": 'M160,236 L240,236 L233,396 L167,396 Z',
    },
    "julep": {
        "glass": 'M156,200 L244,200 L234,406 L166,406 Z',
        "liquid": 'M161,240 L239,240 L230,398 L170,398 Z',
    },
    "goblet": {
        "glass": 'M148,172 C148,258 170,304 200,310 C230,304 252,258 252,172 Z'
                 + stem(310, 400),
        "liquid": 'M156,214 C160,268 178,296 200,300 C222,296 240,268 244,214 Z',
    },
}

GLASS_ORDER = [
    "coupe", "martini", "highball", "rocks", "flute",
    "copa", "hurricane", "tiki", "julep", "goblet",
]


# ---------------------------------------------------------------------------
# Garnishes
# ---------------------------------------------------------------------------
def citrus_wheel(cx, cy, r, color):
    """A citrus slice perched on the rim."""
    parts = ['<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".85"/>' % (cx, cy, r, color),
             '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2" opacity=".9"/>'
             % (cx, cy, r * 0.78, GOLD_SOFT)]
    for i in range(8):
        angle = i * math.pi / 4
        x = cx + math.cos(angle) * r * 0.74
        y = cy + math.sin(angle) * r * 0.74
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="1.4" opacity=".7"/>' % (cx, cy, x, y, GOLD_SOFT)
        )
    return "".join(parts)


def mint_sprig(cx, cy, color):
    leaves = []
    for dx, dy, rot in ((-14, -10, -35), (12, -14, 30), (0, -26, 0)):
        leaves.append(
            '<ellipse cx="%s" cy="%s" rx="13" ry="8" fill="%s" opacity=".8" '
            'transform="rotate(%s %s %s)"/>' % (cx + dx, cy + dy, color, rot, cx + dx, cy + dy)
        )
    leaves.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="2" opacity=".8"/>'
                  % (cx, cy + 12, cx, cy - 20, color))
    return "".join(leaves)


def cherry(cx, cy, color):
    return (
        '<path d="M%s,%s C%s,%s %s,%s %s,%s" fill="none" stroke="%s" stroke-width="2" opacity=".8"/>'
        '<circle cx="%s" cy="%s" r="11" fill="%s" opacity=".9"/>'
        % (cx, cy, cx + 14, cy - 26, cx + 26, cy - 34, cx + 30, cy - 44, GOLD,
           cx, cy, color)
    )


def twist(cx, cy, color):
    return ('<path d="M%s,%s c18,-6 26,8 14,20 c-12,12 -30,4 -26,-12" fill="none" '
            'stroke="%s" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
            % (cx, cy, color))


def star_anise(cx, cy, color):
    pts = []
    for i in range(8):
        angle = i * math.pi / 4
        pts.append('<ellipse cx="%.1f" cy="%.1f" rx="7" ry="3.4" fill="%s" opacity=".85" '
                   'transform="rotate(%.1f %.1f %.1f)"/>'
                   % (cx + math.cos(angle) * 9, cy + math.sin(angle) * 9, color,
                      math.degrees(angle), cx + math.cos(angle) * 9, cy + math.sin(angle) * 9))
    return "".join(pts)


GARNISHES = [citrus_wheel, mint_sprig, cherry, twist, star_anise]


def garnish_for(index, color):
    """Rotate through the garnish styles so no two cards look alike."""
    kind = index % 5
    if kind == 0:
        return citrus_wheel(262, 190, 28, color)
    if kind == 1:
        return mint_sprig(238, 176, "#8fd694")
    if kind == 2:
        return cherry(252, 186, "#c0243f")
    if kind == 3:
        return twist(244, 178, GOLD_SOFT)
    return star_anise(258, 186, "#d9a05b")


def bubbles(seed, color, count=14):
    """Pseudo-random bubbles rising through the drink (deterministic)."""
    out = []
    value = seed * 7919
    for i in range(count):
        value = (value * 1103515245 + 12345) % 2147483648
        x = 170 + (value % 60)
        value = (value * 1103515245 + 12345) % 2147483648
        y = 240 + (value % 140)
        value = (value * 1103515245 + 12345) % 2147483648
        r = 2 + (value % 4)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".35"/>'
                   % (x, y, r, color))
    return "".join(out)


# ---------------------------------------------------------------------------
# Cocktail cards (4:5)
# ---------------------------------------------------------------------------
def cocktail_svg(index):
    deep, liquid = DRINK_COLORS[index]
    glass = GLASSES[GLASS_ORDER[index]]
    uid = "c%02d" % (index + 1)

    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500" role="img" aria-label="Cocktail placeholder">
  <defs>
    <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{deep}"/>
      <stop offset="1" stop-color="{plum}"/>
    </linearGradient>
    <radialGradient id="{uid}glow" cx="50%" cy="38%" r="62%">
      <stop offset="0" stop-color="{liquid}" stop-opacity=".45"/>
      <stop offset="1" stop-color="{liquid}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{uid}liq" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{liquid}" stop-opacity=".95"/>
      <stop offset="1" stop-color="{liquid}" stop-opacity=".55"/>
    </linearGradient>
    <!-- keeps the bubbles inside the drink instead of floating past the glass -->
    <clipPath id="{uid}clip"><path d="{liquid_path}"/></clipPath>
  </defs>

  <rect width="400" height="500" fill="url(#{uid}bg)"/>
  <ellipse cx="200" cy="210" rx="200" ry="190" fill="url(#{uid}glow)"/>

  <!-- soft bokeh -->
  <circle cx="62" cy="92" r="46" fill="{gold}" opacity=".07"/>
  <circle cx="338" cy="404" r="62" fill="{liquid}" opacity=".09"/>
  <circle cx="326" cy="86" r="18" fill="{gold}" opacity=".12"/>

  <!-- drink -->
  <g>
    <path d="{liquid_path}" fill="url(#{uid}liq)"/>
    <g clip-path="url(#{uid}clip)">{bubbles}</g>
    <g fill="none" stroke="{gold}" stroke-width="2.4" stroke-linejoin="round" opacity=".92">
      <path d="{glass_path}"/>
    </g>
    {garnish}
  </g>

  <!-- reflection on the table -->
  <ellipse cx="200" cy="428" rx="120" ry="12" fill="{gold}" opacity=".08"/>

  <!-- frame + placeholder note -->
  <rect x="14" y="14" width="372" height="472" fill="none" stroke="{gold}" stroke-width="1" opacity=".25"/>
  <text x="200" y="470" text-anchor="middle" font-family="Georgia, serif" font-size="11"
        letter-spacing="4" fill="{gold}" opacity=".55">PLACEHOLDER PHOTO</text>
</svg>
""".format(uid=uid, deep=deep, liquid=liquid, plum=PLUM_DEEP, gold=GOLD,
           glass_path=glass["glass"], liquid_path=glass["liquid"],
           bubbles=bubbles(index + 1, GOLD_SOFT),
           garnish=garnish_for(index, liquid))


# ---------------------------------------------------------------------------
# Event / venue scenes used on the gallery, home and about pages
# ---------------------------------------------------------------------------
def scene_svg(index, width=1200, height=900, label="PLACEHOLDER PHOTO"):
    deep, accent = GALLERY_COLORS[index % len(GALLERY_COLORS)]
    uid = "s%02d" % (index + 1)
    variant = index % 4

    # deterministic bokeh field
    lights = []
    value = (index + 3) * 7919
    for i in range(26):
        value = (value * 1103515245 + 12345) % 2147483648
        x = value % width
        value = (value * 1103515245 + 12345) % 2147483648
        y = int((value % height) * 0.72)
        value = (value * 1103515245 + 12345) % 2147483648
        r = 5 + (value % 34)
        value = (value * 1103515245 + 12345) % 2147483648
        op = 0.05 + (value % 16) / 100.0
        color = GOLD if i % 3 else accent
        lights.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%.2f"/>'
                      % (x, y, r, color, op))

    # a different foreground silhouette per variant
    if variant == 0:  # bar counter with glasses
        fg = ('<rect x="0" y="{by}" width="{w}" height="{bh}" fill="{deep}" opacity=".85"/>'
              '<rect x="0" y="{by}" width="{w}" height="6" fill="{gold}" opacity=".5"/>'
              .format(by=int(height * 0.72), bh=int(height * 0.28), w=width, deep=PLUM_DEEP, gold=GOLD))
        for i in range(7):
            x = int(width * 0.1) + i * int(width * 0.12)
            y = int(height * 0.72)
            fg += ('<path d="M{a},{t} L{b},{t} L{c},{m} L{c},{s} M{d},{s} L{e},{s}" '
                   'fill="none" stroke="{gold}" stroke-width="3" opacity=".55"/>'
                   .format(a=x - 26, b=x + 26, c=x, t=y - 120, m=y - 46, s=y - 6,
                           d=x - 20, e=x + 20, gold=GOLD))
    elif variant == 1:  # hanging festoon lights
        fg = ''
        for row in range(3):
            y0 = int(height * (0.12 + row * 0.1))
            fg += ('<path d="M0,{y0} Q{hw},{y1} {w},{y0}" fill="none" stroke="{gold}" '
                   'stroke-width="2" opacity=".35"/>'
                   .format(y0=y0, y1=y0 + 90, hw=width // 2, w=width, gold=GOLD))
            for i in range(11):
                t = i / 10.0
                x = t * width
                y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (y0 + 90) + t ** 2 * y0
                fg += '<circle cx="%.0f" cy="%.0f" r="7" fill="%s" opacity=".65"/>' % (x, y + 10, GOLD_SOFT)
        fg += ('<rect x="0" y="{by}" width="{w}" height="{bh}" fill="{deep}" opacity=".75"/>'
               .format(by=int(height * 0.78), bh=int(height * 0.22), w=width, deep=PLUM_DEEP))
    elif variant == 2:  # raised glasses / toast
        fg = ('<rect x="0" y="{by}" width="{w}" height="{bh}" fill="{deep}" opacity=".8"/>'
              .format(by=int(height * 0.76), bh=int(height * 0.24), w=width, deep=PLUM_DEEP))
        for i, (x, scale) in enumerate(((0.22, 1.0), (0.38, 0.82), (0.56, 1.12), (0.74, 0.9))):
            cx = int(width * x)
            top = int(height * (0.3 + (1 - scale) * 0.12))
            fg += ('<g opacity=".6" stroke="{gold}" stroke-width="3" fill="none">'
                   '<path d="M{a},{t} L{b},{t} C{b},{m} {c},{n} {c},{n}"/>'
                   '<path d="M{a},{t} C{a},{m} {c},{n} {c},{n}"/>'
                   '<path d="M{c},{n} L{c},{s}"/><path d="M{d},{s} L{e},{s}"/></g>'
                   .format(a=cx - 44, b=cx + 44, c=cx, t=top, m=top + 90,
                           n=top + 130, s=top + 230, d=cx - 34, e=cx + 34, gold=GOLD))
    else:  # shaker + tools flat lay
        fg = ('<rect x="0" y="{by}" width="{w}" height="{bh}" fill="{deep}" opacity=".82"/>'
              .format(by=int(height * 0.7), bh=int(height * 0.3), w=width, deep=PLUM_DEEP))
        cx, cy = width // 2, int(height * 0.7)
        fg += ('<g fill="none" stroke="{gold}" stroke-width="4" opacity=".6">'
               '<path d="M{a},{t} L{b},{t} L{b},{u} L{c},{v} L{c},{w2} L{a2},{w2} L{a2},{v} L{a},{u} Z"/>'
               '<path d="M{a},{u} L{b},{u}"/></g>'
               .format(a=cx - 70, a2=cx - 58, b=cx + 70, c=cx + 58,
                       t=cy - 300, u=cy - 250, v=cy - 210, w2=cy - 20, gold=GOLD))

    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Event placeholder">
  <defs>
    <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{deep}"/>
      <stop offset="0.55" stop-color="{plum}"/>
      <stop offset="1" stop-color="{accent}" stop-opacity=".55"/>
    </linearGradient>
    <radialGradient id="{uid}glow" cx="30%" cy="24%" r="70%">
      <stop offset="0" stop-color="{gold}" stop-opacity=".28"/>
      <stop offset="1" stop-color="{gold}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>
  <rect width="{w}" height="{h}" fill="url(#{uid}glow)"/>
  {lights}
  {fg}
  <rect width="{w}" height="{h}" fill="none" stroke="{gold}" stroke-width="2" opacity=".18"/>
  <text x="{tx}" y="{ty}" text-anchor="middle" font-family="Georgia, serif" font-size="{fs}"
        letter-spacing="6" fill="{goldsoft}" opacity=".5">{label}</text>
</svg>
""".format(uid=uid, w=width, h=height, deep=deep, accent=accent, plum=PLUM_DEEP,
           gold=GOLD, goldsoft=GOLD_SOFT, lights="".join(lights), fg=fg,
           tx=width // 2, ty=height - 34, fs=max(12, width // 60), label=label)


# ---------------------------------------------------------------------------
# Brand mark
# ---------------------------------------------------------------------------
LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Shake&amp;Steer">
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#c9a35e"/>
      <stop offset="0.5" stop-color="#f0e2c4"/>
      <stop offset="1" stop-color="#c9a35e"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="30" fill="none" stroke="url(#lg)" stroke-width="1.5" opacity=".65"/>
  <!-- cocktail shaker -->
  <path d="M25,13 h14 v5 l3,5 v26 a4,4 0 0 1 -4,4 h-12 a4,4 0 0 1 -4,-4 v-26 l3,-5 z"
        fill="none" stroke="url(#lg)" stroke-width="2" stroke-linejoin="round"/>
  <path d="M22,23 h20" stroke="url(#lg)" stroke-width="2"/>
  <path d="M27,31 h10" stroke="url(#lg)" stroke-width="1.4" opacity=".7"/>
  <circle cx="32" cy="9" r="2.2" fill="url(#lg)"/>
</svg>
"""


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    print("Generating placeholder artwork...")
    write("logo.svg", LOGO)

    for i in range(10):
        write("cocktail-%02d.svg" % (i + 1), cocktail_svg(i))

    for i in range(12):
        # A couple of tiles are wide/tall in the gallery grid, so vary the crop
        if i in (0, 7):
            w, h = 1400, 800
        elif i in (3, 9):
            w, h = 900, 1200
        else:
            w, h = 1200, 900
        write("gallery-%02d.svg" % (i + 1), scene_svg(i, w, h))

    # Editorial images used on the home / about / services pages
    write("scene-story.svg", scene_svg(5, 1100, 1300))
    write("scene-craft.svg", scene_svg(2, 1100, 1300))
    write("scene-bar.svg", scene_svg(8, 1400, 900))
    write("scene-team.svg", scene_svg(11, 1100, 1300))

    print("Done.")


if __name__ == "__main__":
    main()
