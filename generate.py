#!/usr/bin/env python3
"""Render the front page for 25 November 2026 as a 1024x1024 PNG.

Deterministic: fixed fonts, fixed layout, no network, no clock, no
randomness. Run `python3 generate.py` from this directory; it writes
entry.png next to this file. Re-running produces identical bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (18, 18, 18)
SEA = (23, 52, 84)
FLAME = (232, 116, 24)
SMOKE = (120, 118, 112)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (headline, one-line deck). Every figure in the numbers strip below
# also appears in one of these stories.

LEAD_HEAD = "TANKERS ABLAZE IN HORMUZ"
LEAD_DECK = (
    "Two oil tankers hit naval mines and caught fire in the Strait of "
    "Hormuz early on Wednesday, Iran's Revolutionary Guards Navy said, "
    "warning ships to coordinate passage."
)

# region -> list of (headline, deck)
REGIONS = [
    ("MIDDLE EAST", [
        ("Houthi missile hits Riyadh tower again",
         "11 hurt in second strike in a week"),
        ("Saudis down four drones over Ras Tanura",
         "Defences intercept drones in the east"),
        ("Gaza: Hamas security chief killed",
         "Abuelouf dies with wife, two daughters"),
        ("Gaza aid-worker toll reaches 600",
         "UNRWA staffer killed at Jabalia well"),
        ("Storm threatens 1.76m in Gaza tents",
         "Gaza warns of floods as storm nears"),
    ]),
    ("EUROPE & UKRAINE", [
        ("Putin vows retaliation over refinery raids",
         "Two Samara plants hit; refining down 45%"),
        ("Ukraine strikes Kinzhal airfield",
         "Savasleyka base hit by drones"),
        ("Russia fires 112 drones overnight",
         "88 downed; 3 dead, 15 hurt"),
        ("Polish airspace breached by Russian drone",
         "Warsaw protests; Moscow blames Estonia"),
        ("Merz: Ukraine talks may resume in Abu Dhabi",
         "Europe will show Russia its limits"),
        ("Zelenskyy: Ukraine needs EUR 115bn",
         "Kyiv seeks aid to fight through 2027"),
    ]),
    ("ASIA-PACIFIC", [
        ("China launches Shenzhou-24",
         "Pakistan's first astronaut rides along"),
        ("Australia signs Solomon Islands treaty",
         "Canberra shores up Pacific ties"),
        ("North Korea expels Swiss envoy",
         "Office ordered shut within 48 hours"),
        ("Asia markets slide as AI doubts return",
         "Kospi falls 5%, Nikkei 3%"),
        ("Japan prices firm case for BOJ hike",
         "Services prices rise 4.2% in October"),
        ("Taiwan votes on Saturday",
         "Voters pick 11,000 local officials"),
    ]),
    ("AMERICAS", [
        ("Trump set to unveil tariffs on 16 partners",
         "Overcapacity probe targets China most"),
        ("Trump awards Giuliani Medal of Freedom",
         "Top US civilian honour for ex-mayor"),
        ("Unclassified CIA system breached",
         "Latest US cybersecurity incident"),
        ("US soldier admits selling secrets to China",
         "Jian Zhao pleads guilty"),
        ("Colombia police free supermarket hostages",
         "All rescued in Cartagena siege"),
    ]),
    ("AFRICA", [
        ("Sudan drone strikes kill 19 civilians",
         "RSF drones hit Blue Nile homes"),
        ("Ethiopia offers to host Sudan talks",
         "Abiy proposes unity government"),
        ("Landmine toll hits five-year high",
         "Nearly 7,000 hurt in 2025"),
    ]),
    ("WORLD & CULTURE", [
        ("UK police still institutionally racist",
         "Met reform has stalled, report finds"),
        ("Japan leaks expose millions",
         "Keio hack may hit 11m people"),
        ("Huawei convicted in US sanctions case",
         "Jury finds trade-secret theft"),
        ("US stroke cases set to nearly double",
         "20m Americans by 2050, group warns"),
    ]),
]

NUMBERS = [
    ("2", "tankers ablaze"),
    ("11", "hurt in Riyadh"),
    ("112", "drones fired"),
    ("45%", "refining cut"),
    ("1.76m", "in Gaza tents"),
    ("7,000", "mine victims"),
]


# ---------------------------------------------------------------- drawing
def draw_masthead(draw):
    title = font(SERIF_B, 44)
    draw.text((W // 2, 18), "THE WORLD IN ONE PICTURE",
              font=title, fill=INK, anchor="mt")
    sub = font(SANS_B, 15)
    draw.text((W // 2, 74),
              "WEDNESDAY, 25 NOVEMBER 2026  -  30 STORIES  -  SIX REGIONS",
              font=sub, fill=RED, anchor="mt")
    draw.line([(36, 100), (W - 36, 100)], fill=RULE, width=3)
    draw.line([(36, 106), (W - 36, 106)], fill=RULE, width=1)


def draw_lead(draw):
    """Lead story: headline + deck left, drawn tankers right."""
    x0, y0 = 36, 118
    kicker = font(SANS_B, 14)
    draw.text((x0, y0), "THE LEAD  -  IRAN WAR WIDENS", font=kicker, fill=RED)
    head = font(SANS_B, 36)
    y = text_block(draw, x0, y0 + 26, LEAD_HEAD, head, INK, 600, 42)
    deck = font(SANS, 15)
    y = text_block(draw, x0, y + 8, LEAD_DECK, deck, INK, 600, 20)
    # illustration: sea, two tankers, flames, smoke
    ix, iy, iw, ih = 668, 118, 320, 168
    draw.rectangle([ix, iy, ix + iw, iy + ih], fill=SEA)
    draw.rectangle([ix, iy + 118, ix + iw, iy + ih], fill=(16, 38, 62))
    for sx in (ix + 18, ix + 168):
        draw.rectangle([sx, iy + 96, sx + 120, iy + 118], fill=(8, 8, 8))
        draw.rectangle([sx + 52, iy + 78, sx + 66, iy + 96], fill=(8, 8, 8))
        for fx, fh in ((sx + 10, 26), (sx + 34, 38), (sx + 66, 30), (sx + 92, 22)):
            draw.polygon([(fx, iy + 96), (fx + 12, iy + 96 - fh),
                          (fx + 24, iy + 96)], fill=FLAME)
        for cx, cy, r in ((sx + 30, iy + 52, 12), (sx + 52, iy + 40, 15),
                          (sx + 76, iy + 52, 11)):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    draw.text((ix, iy + ih + 8), "Tehran ties reopening to an end to the blockade.",
              font=font(SANS, 11), fill=GREY)
    draw.line([(36, 312), (W - 36, 312)], fill=RULE, width=2)
    return 324


def draw_columns(draw, y_top):
    """Three columns of region sections."""
    col_w = 296
    xs = [36, 36 + col_w + 18, 36 + 2 * (col_w + 18)]
    # column 0: Middle East + Africa ; 1: Europe & Ukraine + World ;
    # column 2: Asia-Pacific + Americas
    plan = [[REGIONS[0], REGIONS[4]],
            [REGIONS[1], REGIONS[5]],
            [REGIONS[2], REGIONS[3]]]
    head_f = font(SANS_B, 13)
    h_f = font(SANS_B, 14)
    d_f = font(SANS, 12)
    for ci, groups in enumerate(plan):
        x = xs[ci]
        y = y_top
        for name, stories in groups:
            draw.text((x, y), name, font=head_f, fill=RED)
            y += 20
            draw.line([(x, y), (x + col_w, y)], fill=GREY, width=1)
            y += 8
            for head, deck in stories:
                y = text_block(draw, x, y, head, h_f, INK, col_w, 17,
                               max_lines=2)
                y = text_block(draw, x, y + 1, deck, d_f, GREY, col_w, 14,
                               max_lines=1)
                y += 8
            y += 4
    return y


def draw_numbers(draw):
    y0 = 928
    draw.line([(36, y0), (W - 36, y0)], fill=RULE, width=2)
    draw.text((36, y0 + 10), "THE DAY IN NUMBERS",
              font=font(SANS_B, 14), fill=RED)
    cell = (W - 72) // len(NUMBERS)
    big = font(SANS_B, 26)
    small = font(SANS, 11)
    for i, (num, label) in enumerate(NUMBERS):
        cx = 36 + cell * i + cell // 2
        draw.text((cx, y0 + 34), num, font=big, fill=INK, anchor="mt")
        draw.text((cx, y0 + 68), label, font=small, fill=GREY, anchor="mt")
    draw.line([(36, 1012), (W - 36, 1012)], fill=RULE, width=1)
    draw.text((W // 2, 1016), "Sources: Reuters, AP, Al Jazeera, Ukrinform, "
              "SCMP, Japan Times, Kyodo, Dawn, UN OCHA  -  25 Nov 2026",
              font=font(SANS, 10), fill=GREY, anchor="mt")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_columns(draw, 324)
    draw_numbers(draw)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
