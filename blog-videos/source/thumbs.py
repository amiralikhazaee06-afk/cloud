"""YouTube thumbnails, 1280x720. Big words (readable at phone size), one red accent, real photos."""
import os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

TW, TH = 1280, 720
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")


def base(dark=True):
    if dark:
        return E.bg_dark().resize((TW, TH)).convert("RGB")
    return E.bg_cream().resize((TW, TH)).convert("RGB")


def fit(img, w, h):
    return E.kenburns(img, 0, w, h, z0=1.0, z1=1.0)


def rounded_photo(fr, name, x, y, w, h, r=26, crop=None, rot=0, border=10):
    img = E.photo(name)
    if crop:
        iw, ih = img.size
        img = img.crop((int(crop[0] * iw), int(crop[1] * ih), int(crop[2] * iw), int(crop[3] * ih)))
    im = fit(img, w, h).convert("RGBA"); im.putalpha(E.rmask(w, h, r))
    fr_ = E.rrect(w + 2 * border, h + 2 * border, r + border, E.PAPER).copy()
    fr_.paste(im, (border, border), im)
    E.put(fr, E.shadow(w + 2 * border, h + 2 * border, r, blur=24, op=0.45), x, y + 14, rot=rot)
    E.put(fr, fr_, x, y, rot=rot)


def words(fr, lines, x, y, sizes, cols, font=E.F_BIG, gap=0):
    for (t, sz, c) in zip(lines, sizes, cols):
        spr = E.word_sprite(t, font, sz, c)
        # dark outline for legibility over anything
        E.put(fr, spr, x, y, anchor="tl")
        y += int(sz * 1.02) + gap
    return y


def pill(fr, txt, x, y, size=40, bg=E.RED, fg=E.WHITE, rot=0):
    f = E.font(E.F_BIG, size)
    w = int(f.getlength(txt)) + size * 1.2
    h = int(size * 1.6)
    im = E.rrect(int(w), h, h // 2, bg).copy()
    ImageDraw.Draw(im).text((w / 2, h / 2), txt, font=f, fill=fg, anchor="mm")
    E.put(fr, im, x, y, anchor="tl", rot=rot)


def rainscreen():
    fr = base(dark=False)
    # big drawn wall section on the right, cropped feel
    big = Image.new("RGB", (640, 720), E.CREAM)
    E.wall_section(big, 120, 40, 640, 1.3, "rain", scale=2.6)
    E.put(fr, E.shadow(440, 660, 30, op=0.25), 1050, 372)
    card = E.rrect(440, 660, 30, E.PAPER).copy()
    crop = big.crop((90, 20, 530, 680)).convert("RGBA"); crop.putalpha(E.rmask(440, 660, 30))
    card.paste(crop, (0, 0), crop)
    E.put(fr, card, 1050, 360)
    words(fr, ["DOES YOUR", "HOUSE NEED A", "RAINSCREEN?"], 60, 120, [84, 84, 104], [E.INK, E.INK, E.RED])
    pill(fr, "BC CODE: 9.5 mm GAP", 64, 520, 40, E.INK)
    return fr


def wetclimate():
    fr = base(dark=True)
    names = [("metal-siding-in-west-vancouver-by-silver-siding-exterior.webp", "METAL"),
             ("Vinyl-Siding-Surrey.jpg", "VINYL"),
             ("james-hardie-Siding5.jpg", "FIBRE CEMENT")]
    x0, w, h, gap = 40, 390, 300, 25
    for i, (n, lab) in enumerate(names):
        x = x0 + i * (w + gap) + w / 2
        rounded_photo(fr, n, x, 520, w, h, r=22, border=8)
        pill(fr, lab, x - (E.font(E.F_BIG, 34).getlength(lab) + 41) / 2, 640, 34, E.RED if i == 0 else E.INK)
    words(fr, ["WHICH SIDING", "SURVIVES THE RAIN?"], 50, 50, [100, 100], [E.WHITE, E.RED])
    return fr


def lux():
    fr = base(dark=True)
    rounded_photo(fr, "LUX-Panels-vs.-Other-Metal-Siding-1.webp", 1010, 400, 470, 560, crop=(0.05, 0.0, 0.95, 0.76), rot=-3)
    words(fr, ["LUX", "vs LONGBOARD", "vs AL13"], 56, 70, [170, 80, 80], [E.WHITE, E.WHITE, E.WHITE])
    pill(fr, "STEEL OR ALUMINUM?", 60, 470, 46, E.RED, rot=2)
    pill(fr, "The real difference", 64, 580, 34, (50, 50, 56))
    return fr


def trends():
    fr = base(dark=False)
    rounded_photo(fr, "DD6A9214-1.jpg", 1010, 250, 460, 330, rot=3, border=8)
    rounded_photo(fr, "metal-panel-siding-north-vancouver-6.webp", 1050, 540, 420, 290, rot=-4, border=8)
    rounded_photo(fr, "james-hardie-coquitlam.jpeg", 760, 560, 360, 250, rot=2, border=8)
    words(fr, ["10", "SIDING", "IDEAS"], 56, 40, [250, 120, 120], [E.RED, E.INK, E.INK])
    pill(fr, "2026", 60, 560, 70, E.INK, rot=-3)
    return fr


if __name__ == "__main__":
    for name, fn in [("rainscreen", rainscreen), ("wetclimate", wetclimate), ("lux", lux), ("trends", trends)]:
        os.makedirs(os.path.join(OUT, name), exist_ok=True)
        im = fn()
        im.save(os.path.join(OUT, name, "thumbnail.jpg"), quality=90)
        print("thumb", name, os.path.getsize(os.path.join(OUT, name, "thumbnail.jpg")) // 1024, "KB")
