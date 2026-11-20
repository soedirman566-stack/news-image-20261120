#!/usr/bin/env python3
"""Compose entry.png: a one-page newspaper front page summing up the world
news of Friday, 20 November 2026.

Deterministic by construction: fixed layout, fixed fonts, no randomness, no
clock. Running it twice produces a byte-identical entry.png.

Layout never aborts: every text block is fitted with an adaptive font-size
ladder (shrink until it fits its box), so the program always exits 0 and
always writes the image.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 245, 238)
INK = (17, 17, 17)
GRAY = (68, 68, 68)
ACCENT = (163, 22, 33)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns the list of lines for the given font."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, minimum, max_width, max_lines):
    """Adaptive ladder: shrink from `start` to `minimum` until the wrapped
    text fits max_width x max_lines. At the minimum size, truncate with an
    ellipsis rather than overflowing. Always returns (font, lines)."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, minimum)
    lines = wrap(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "...", font=fnt) > max_width:
            last = last[:-1]
        lines[-1] = last + "..."
    return fnt, lines


def draw_lines(draw, x, y, lines, fnt, fill, leading=1.18, align="left"):
    step = int(fnt.size * leading)
    for line in lines:
        if align == "center":
            lx = x + (CONTENT_W - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += step
    return y


def photo(name, width, height):
    """Load an asset and center-crop it to exactly width x height."""
    img = Image.open(ASSETS / name).convert("RGB")
    return ImageOps.fit(img, (width, height), Image.LANCZOS)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    fnt = font(SERIF_BOLD, 64)
    title = "THE DAILY GLOBE"
    tw = d.textlength(title, font=fnt)
    d.text(((W - tw) / 2, 22), title, font=fnt, fill=INK)
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=INK, width=3)
    d.line([(MARGIN, 114), (W - MARGIN, 114)], fill=INK, width=1)

    # ---- Date bar -------------------------------------------------------
    d.rectangle([MARGIN, 126, W - MARGIN, 182], fill=INK)
    fnt = font(SANS_BOLD, 38)
    date = "FRIDAY, 20 NOVEMBER 2026"
    tw = d.textlength(date, font=fnt)
    d.text(((W - tw) / 2, 136), date, font=fnt, fill=WHITE)

    # ---- Lead story -----------------------------------------------------
    y = 198
    d.text((MARGIN, y), "DIPLOMACY · SHENZHEN, CHINA",
           font=font(SANS_BOLD, 20), fill=ACCENT)
    y += 30
    fnt, lines = fit(
        d,
        "Trump, Xi and Putin Hold First Three-Way Summit and Sign Peace Declaration",
        SERIF_BOLD, 46, 30, CONTENT_W, 2)
    y = draw_lines(d, MARGIN, y, lines, fnt, INK, leading=1.12)
    y += 10
    page.paste(photo("summit.jpg", CONTENT_W, 238), (MARGIN, y))
    y += 238 + 8
    fnt, lines = fit(
        d,
        "Shenzhen, the summit's host city. The US, Chinese and Russian leaders "
        "pledged UN reform, lower nuclear risk and steady energy supplies. "
        "Hours later, Russian missiles hit Kyiv in one of the war's heaviest raids.",
        SANS, 18, 13, CONTENT_W, 3)
    draw_lines(d, MARGIN, y, lines, fnt, GRAY, leading=1.25)

    # ---- Divider --------------------------------------------------------
    d.line([(MARGIN, 664), (W - MARGIN, 664)], fill=INK, width=2)

    # ---- Three columns --------------------------------------------------
    stories = [
        ("JUSTICE · THE HAGUE", "icj.jpg",
         "World Court: Myanmar Committed Genocide Against Rohingya",
         "The ICJ ruled 9-6 that the 2017 crackdown on the Rohingya was "
         "genocide - a first verdict against a state."),
        ("ECONOMY · WORLD MARKETS", "markets.jpg",
         "AI Doubts Spark Global Stock Sell-Off",
         "Anthropic's record debut failed to calm nerves: the S&P 500 fell "
         "2%, the Nikkei 4.8%, gold 4.2%."),
        ("CLIMATE · ANTALYA, TURKEY", "cop31.jpg",
         "COP31 Draft Drops Fossil-Fuel Phase-Out",
         "Negotiators deleted every mention of ending fossil fuels from the "
         "draft deal on the talks' final day."),
    ]
    col_w = (CONTENT_W - 2 * 24) // 3
    top = 680
    for i, (kicker, img, headline, caption) in enumerate(stories):
        x = MARGIN + i * (col_w + 24)
        d.text((x, top), kicker, font=font(SANS_BOLD, 15), fill=ACCENT)
        page.paste(photo(img, col_w, 112), (x, top + 24))
        fnt, lines = fit(d, headline, SERIF_BOLD, 24, 17, col_w, 3)
        yy = draw_lines(d, x, top + 148, lines, fnt, INK, leading=1.15)
        fnt, lines = fit(d, caption, SANS, 15, 11, col_w, 3)
        draw_lines(d, x, yy + 4, lines, fnt, GRAY, leading=1.25)

    # ---- Footer ---------------------------------------------------------
    d.line([(MARGIN, 978), (W - MARGIN, 978)], fill=INK, width=1)
    credits = ("Photos: Dinkun Chen (CC BY-SA 4.0) · International Court of Justice "
               "(public domain) · Vlad Lazarenko (CC BY-SA 3.0) · IISD/ENB, Mike Muzurakis")
    fnt, lines = fit(d, credits, SANS, 14, 10, CONTENT_W, 1)
    draw_lines(d, MARGIN, 986, lines, fnt, GRAY, align="center")

    # ---- Save (keep under the 1 MiB gate limit) -------------------------
    page.save(OUT, format="PNG")
    if OUT.stat().st_size > 1_000_000:
        page.quantize(colors=256, method=Image.FASTOCTREE).save(OUT, format="PNG")


if __name__ == "__main__":
    main()
