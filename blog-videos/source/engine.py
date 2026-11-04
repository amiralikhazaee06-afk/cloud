"""Motion-graphics renderer for the Silver Siding blog videos.

Style follows the reference reel: cream and near-black backgrounds, heavy
display type with one red highlighted phrase, cut-out cards with soft
shadows, words that pop in one at a time.

A video is a list of scene dicts (see scripts/*.py). Each scene carries the
narration as a list of sentences; elements reveal at the start of the
sentence index given by their `at` value, so picture and voice stay in sync.
"""
import json, math, os, re, subprocess, sys, random
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1920, 1080, 30
TR = 0.32                                   # scene cross-fade
CREAM = (244, 240, 232)
CREAM2 = (236, 231, 221)
PAPER = (255, 253, 249)
INK = (22, 22, 24)
SOFT = (96, 94, 90)
MUTE = (150, 146, 138)
RED = (222, 34, 40)
DARK = (14, 14, 16)
WHITE = (255, 255, 255)
GREEN = (38, 140, 86)
BLUE = (70, 140, 210)

HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/opentype/inter/"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eback(x, s=1.7):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x


# ------------------------------------------------------------------ fonts / text
@lru_cache(None)
def font(name, size):
    if name == "mono": return ImageFont.truetype(MONO, size)
    return ImageFont.truetype(FD + name + ".otf", size)

F_BIG = "InterDisplay-Black"
F_BOLD = "InterDisplay-ExtraBold"
F_SEMI = "InterDisplay-SemiBold"
F_MED = "InterDisplay-Medium"
F_REG = "InterDisplay-Regular"
F_LIGHT = "InterDisplay-Light"


@lru_cache(None)
def word_sprite(txt, fname, size, color):
    f = font(fname, size)
    asc, desc = f.getmetrics()
    w = max(1, int(math.ceil(f.getlength(txt))))
    pad = 6
    im = Image.new("RGBA", (w + 2 * pad, asc + desc + 2 * pad), color + (0,))
    ImageDraw.Draw(im).text((pad, pad + asc), txt, font=f, fill=color + (255,), anchor="ls")
    im.info["pad"] = pad; im.info["asc"] = asc
    return im


def parse_rich(text):
    """'Your siding is *not waterproof*' -> [(word, accent_bool), ...]"""
    out, acc = [], False
    for tok in re.split(r"(\*)", text):
        if tok == "*": acc = not acc; continue
        ws = tok.split()
        if ws and out and not tok[0].isspace() and re.match(r"^[,.;:!?’']", ws[0]):
            # punctuation glued to the end of the previous (highlighted) word
            pw, pa = out[-1]
            head = re.match(r"^[,.;:!?’']+", ws[0]).group(0)
            out[-1] = (pw + head, pa)
            rest = ws[0][len(head):]
            ws = ([rest] if rest else []) + ws[1:]
        for w in ws:
            out.append((w, acc))
    return out


def layout_rich(text, size, maxw, fname=F_BIG, afname=None, gap=0.26):
    """Wrap rich text. Returns lines -> [(word, accent, x, width)], line height."""
    afname = afname or fname
    words = parse_rich(text)
    sp = font(fname, size).getlength(" ") * (1 + gap)
    lines, cur, x = [], [], 0
    for w, a in words:
        wd = font(afname if a else fname, size).getlength(w)
        if cur and x + wd > maxw:
            lines.append(cur); cur, x = [], 0
        cur.append((w, a, x, wd)); x += wd + sp
    if cur: lines.append(cur)
    return lines, int(size * 1.08)


def line_width(line): return line[-1][2] + line[-1][3] if line else 0


def draw_rich(fr, text, x, y, size, maxw, t, t0, color=INK, accent=RED, fname=F_BIG,
              afname=None, align="left", stagger=0.055, lh=None, pop=True, alpha=1.0):
    """Animated rich text block. Words pop in from t0. Returns block height."""
    lines, lh0 = layout_rich(text, size, maxw, fname, afname)
    lh = lh or lh0
    k = 0
    for li, line in enumerate(lines):
        lw = line_width(line)
        ox = x if align == "left" else (x - lw / 2 if align == "center" else x - lw)
        for (w, a, wx, wd) in line:
            p = (t - t0 - k * stagger) / 0.42
            k += 1
            if p <= 0: continue
            spr = word_sprite(w, (afname or fname) if a else fname, size, accent if a else color)
            sc = lerp(0.72, 1.0, eback(p)) if pop else 1.0
            al = clamp(p * 2.2) * alpha
            dy = (1 - eo(p)) * size * 0.35
            cx = ox + wx + wd / 2
            cy = y + li * lh + size * 0.55 + dy
            put(fr, spr, cx, cy, a=al, sc=sc)
    return len(lines) * lh


def text_block_height(text, size, maxw, fname=F_BIG, lh=None):
    lines, lh0 = layout_rich(text, size, maxw, fname)
    return len(lines) * (lh or lh0)


# ------------------------------------------------------------------ compositing
LUTS = {}
def with_alpha(im, a):
    if a >= 0.995: return im
    q = int(a * 64)
    if q not in LUTS: LUTS[q] = [int(v * q / 64) for v in range(256)]
    out = im.copy(); out.putalpha(im.getchannel("A").point(LUTS[q])); return out


def put(fr, im, x, y, a=1.0, sc=1.0, anchor="c", rot=0.0):
    if a <= 0.01: return
    if abs(sc - 1) > 0.004:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    if abs(rot) > 0.05:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    im = with_alpha(im, a)
    if anchor == "c": x, y = x - im.width / 2, y - im.height / 2
    fr.paste(im, (int(round(x)), int(round(y))), im)


@lru_cache(None)
def rrect(w, h, r, fill, ss=2):
    im = Image.new("RGBA", (w * ss, h * ss), fill[:3] + (0,))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=fill if len(fill) == 4 else fill + (255,))
    return im.resize((w, h), Image.LANCZOS)


@lru_cache(None)
def shadow(w, h, r, blur=26, op=0.28, dark=False):
    pad = blur * 3
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + w, pad + h), r, fill=(0, 0, 0, int(255 * op)))
    return im.filter(ImageFilter.GaussianBlur(blur))


def card(fr, x, y, w, h, a=1.0, fill=PAPER, r=22, sh=True, sc=1.0, op=0.22):
    """Draw a rounded card with top-left (x,y)."""
    if a <= 0.01: return
    w2, h2 = int(w * sc), int(h * sc)
    cx, cy = x + w / 2, y + h / 2
    if sh: put(fr, shadow(w2, h2, r, op=op), cx, cy + 12 * sc, a=a)
    put(fr, rrect(w2, h2, r, fill), cx, cy, a=a)


@lru_cache(None)
def icon(kind, d, col=None):
    ss = 3; D = d * ss
    im = Image.new("RGBA", (D, D), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    c = {"check": INK, "x": RED, "warn": RED, "dot": RED, "num": INK, "plus": INK, "minus": RED}.get(kind, INK)
    c = col or c
    if kind == "warn":
        g.polygon([(D / 2, D * 0.06), (D * 0.97, D * 0.92), (D * 0.03, D * 0.92)], fill=c + (255,))
        g.rectangle((D * 0.46, D * 0.36, D * 0.54, D * 0.66), fill=WHITE + (255,))
        g.ellipse((D * 0.455, D * 0.73, D * 0.545, D * 0.82), fill=WHITE + (255,))
    else:
        g.ellipse((0, 0, D - 1, D - 1), fill=c + (255,))
        lw = int(D * 0.11)
        if kind == "check":
            g.line([(D * 0.27, D * 0.53), (D * 0.44, D * 0.70), (D * 0.74, D * 0.33)], fill=WHITE + (255,), width=lw, joint="curve")
        elif kind == "x":
            g.line([(D * 0.32, D * 0.32), (D * 0.68, D * 0.68)], fill=WHITE + (255,), width=lw)
            g.line([(D * 0.68, D * 0.32), (D * 0.32, D * 0.68)], fill=WHITE + (255,), width=lw)
        elif kind == "plus":
            g.line([(D * 0.28, D / 2), (D * 0.72, D / 2)], fill=WHITE + (255,), width=lw)
            g.line([(D / 2, D * 0.28), (D / 2, D * 0.72)], fill=WHITE + (255,), width=lw)
        elif kind == "minus":
            g.line([(D * 0.28, D / 2), (D * 0.72, D / 2)], fill=WHITE + (255,), width=lw)
    return im.resize((d, d), Image.LANCZOS)


@lru_cache(None)
def num_icon(n, d, col=INK):
    im = icon("num", d, col).copy()
    f = font(F_BOLD, int(d * 0.52))
    ImageDraw.Draw(im).text((d / 2, d / 2 + 1), str(n), font=f, fill=WHITE, anchor="mm")
    return im


# ------------------------------------------------------------------ backgrounds
@lru_cache(None)
def bg_cream():
    im = Image.new("RGB", (W, H), CREAM)
    g = ImageDraw.Draw(im)
    for x in range(0, W + 1, 96): g.line((x, 0, x, H), fill=(237, 232, 223))
    for y in range(0, H + 1, 96): g.line((0, y, W, y), fill=(237, 232, 223))
    # paper grain
    rng = np.random.default_rng(1)
    n = (rng.normal(0, 3.2, (H, W, 1))).astype(np.int16)
    arr = np.clip(np.asarray(im).astype(np.int16) + n, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


@lru_cache(None)
def ring(R, th, col):
    ss = 2; S = (R + th) * 2 * ss
    im = Image.new("RGBA", (S, S), col + (0,)); g = ImageDraw.Draw(im)
    g.ellipse((0, 0, S - 1, S - 1), fill=col + (255,))
    g.ellipse((th * 2 * ss, th * 2 * ss, S - 1 - th * 2 * ss, S - 1 - th * 2 * ss), fill=col + (0,))
    return im.resize((S // ss, S // ss), Image.LANCZOS)


@lru_cache(None)
def bg_dark():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W * 0.5) / W) ** 2 + ((y - H * 0.42) / H) ** 2)
    v = np.clip(34 - d * 40, 8, 34)
    rng = np.random.default_rng(2)
    v = v + rng.normal(0, 2.0, v.shape)
    arr = np.clip(np.stack([v, v, v * 1.04], -1), 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def background(kind, t, seed=0):
    if kind == "dark":
        return bg_dark().copy()
    fr = bg_cream().copy()
    # slow drifting grey arc, like the reference
    r = ring(560, 70, (226, 221, 211))
    ang = seed * 1.7 + t * 0.06
    put(fr, r, W * (0.82 if seed % 2 == 0 else 0.18) + math.cos(ang) * 40, H * 0.5 + math.sin(ang) * 30, a=0.9)
    return fr


# ------------------------------------------------------------------ photos
IMG_ROOT = os.environ.get("IMG_ROOT", os.path.join(HERE, "..", "media"))

@lru_cache(None)
def photo(name):
    im = Image.open(os.path.join(IMG_ROOT, name)).convert("RGB")
    return im


def kenburns(img, p, tw, th, z0=1.04, z1=1.14, f0=(0.5, 0.5), f1=(0.5, 0.5)):
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    z = lerp(z0, z1, p)
    vw, vh = tw / (s * z), th / (s * z)
    fx, fy = lerp(f0[0], f1[0], p) * iw, lerp(f0[1], f1[1], p) * ih
    x0 = clamp(fx - vw / 2, 0, iw - vw); y0 = clamp(fy - vh / 2, 0, ih - vh)
    return img.resize((tw, th), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))


@lru_cache(None)
def rmask(w, h, r):
    return rrect(w, h, r, (255, 255, 255)).getchannel("A")


def photo_card(fr, name, x, y, w, h, p, a=1.0, sc=1.0, r=20, kb=None, crop=None, border=0):
    """Photo in a rounded card; (x,y) is the centre."""
    if a <= 0.01: return
    img = photo(name)
    if crop:   # fractional crop (l,t,r,b) to hide baked-in banners
        iw, ih = img.size
        img = img.crop((int(crop[0] * iw), int(crop[1] * ih), int(crop[2] * iw), int(crop[3] * ih)))
    kb = kb or {}
    w2, h2 = int(w * sc), int(h * sc)
    im = kenburns(img, p, w2, h2, **kb).convert("RGBA")
    im.putalpha(rmask(w2, h2, r))
    put(fr, shadow(w2, h2, r, blur=30, op=0.30), x, y + 16, a=a)
    if border:
        put(fr, rrect(w2 + 2 * border, h2 + 2 * border, r + border, PAPER), x, y, a=a)
    put(fr, im, x, y, a=a)


# ------------------------------------------------------------------ chrome
def chapter_tag(fr, label, a, dark=False):
    if not label or a <= 0.01: return
    f = font("mono", 22)
    txt = label.upper()
    w = int(f.getlength(txt)) + 44
    col = (255, 255, 255, 30) if dark else (22, 22, 24, 255)
    pill = rrect(w, 44, 22, (40, 40, 44) if dark else INK)
    im = pill.copy()
    ImageDraw.Draw(im).ellipse((16, 17, 26, 27), fill=RED)
    ImageDraw.Draw(im).text((34, 22), txt, font=f, fill=WHITE, anchor="lm")
    put(fr, im, 70, 62, a=a, anchor="tl")


def progress(fr, frac, dark=False):
    g = ImageDraw.Draw(fr)
    g.rectangle((0, H - 8, W, H), fill=(40, 40, 44) if dark else (226, 220, 210))
    g.rectangle((0, H - 8, int(W * frac), H), fill=RED)


# ------------------------------------------------------------------ scene renderers
def at_t(s, k):
    """local start time of sentence k in scene s (k may be fractional)"""
    cues = s["_cues"]
    if k is None: return 0.0
    i = int(k)
    if i >= len(cues): return s["_dur"]
    base = cues[i][0]
    frac = k - i
    return base + frac * (cues[i][1] - cues[i][0])


def r_kinetic(fr, s, t):
    dark = s.get("bg") == "dark"
    col = WHITE if dark else INK
    lines = s["lines"]
    sizes = s.get("sizes") or [s.get("size", 120)] * len(lines)
    maxw = s.get("maxw", 1500)
    hs = [text_block_height(l, sz, maxw) for l, sz in zip(lines, sizes)]
    gap = 26
    total = sum(hs) + gap * (len(lines) - 1)
    y = H / 2 - total / 2 - (40 if s.get("sub") else 0)
    for i, (l, sz) in enumerate(zip(lines, sizes)):
        ats = s.get("at", [0] * len(lines))
        t0 = at_t(s, ats[i]) + s.get("delay", [0] * len(lines))[i] if isinstance(s.get("delay"), list) else at_t(s, ats[i])
        fn = s.get("fonts", [F_BIG] * len(lines))[i]
        draw_rich(fr, l, W / 2, y, sz, maxw, t, t0, color=col, fname=fn, align="center")
        y += hs[i] + gap
    if s.get("sub"):
        t0 = at_t(s, s.get("sub_at", 0)) + 0.5
        p = eo((t - t0) / 0.5)
        f = font(F_MED, 38)
        spr = word_sprite(s["sub"], F_MED, 38, (180, 176, 168) if dark else SOFT)
        put(fr, spr, W / 2, y + 40 + (1 - p) * 20, a=p)
    if s.get("icons"):
        for ic in s["icons"]:
            t0 = at_t(s, ic.get("at", 0))
            p = (t - t0) / 0.5
            if p > 0:
                put(fr, icon(ic["k"], ic.get("d", 120)), ic["x"], ic["y"], a=clamp(p * 2), sc=eback(p))


def r_question(fr, s, t):
    # giant faded question mark
    q = word_sprite("?", F_BIG, 900, (34, 34, 38))
    put(fr, q, W - 300 + math.sin(t * 0.6) * 10, H / 2 + 20, a=eo(t / 0.6))
    f = font("mono", 30)
    lab = s.get("label", "QUESTION %02d" % s.get("n", 1))
    p = eo(t / 0.4)
    spr = word_sprite(lab, "mono", 30, RED) if False else None
    im = Image.new("RGBA", (int(f.getlength(lab)) + 20, 50), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 25), lab, font=f, fill=RED, anchor="lm")
    put(fr, im, 160, 300, a=p, anchor="tl")
    g = ImageDraw.Draw(fr)
    bw = int(140 * eo((t - 0.1) / 0.5))
    if bw > 0: g.rectangle((170, 360, 170 + bw, 368), fill=RED)
    hgt = draw_rich(fr, s["text"], 165, 400, s.get("size", 104), s.get("maxw", 1150), t, 0.15, color=WHITE, fname=F_BIG)
    if s.get("sub"):
        t0 = at_t(s, s.get("sub_at", 0.5))
        pp = eo((t - t0) / 0.5)
        spr = word_sprite(s["sub"], F_MED, 40, (175, 172, 165))
        put(fr, spr, 165, 400 + hgt + 40 + (1 - pp) * 16, a=pp, anchor="tl")


def side_text(fr, s, t, x, y, w, dark=False):
    """kicker + title + bullet items used by photo/bullets scenes"""
    col = WHITE if dark else INK
    sub = (190, 186, 178) if dark else SOFT
    if s.get("kicker"):
        p = eo(t / 0.4)
        f = font("mono", 26)
        im = Image.new("RGBA", (int(f.getlength(s["kicker"].upper())) + 20, 44), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 22), s["kicker"].upper(), font=f, fill=RED, anchor="lm")
        put(fr, im, x, y, a=p, anchor="tl"); y += 58
    if s.get("title"):
        tsz = s.get("tsize", 72)
        y += draw_rich(fr, s["title"], x, y, tsz, w, t, at_t(s, s.get("title_at", 0)) + 0.05, color=col, fname=F_BIG) + 26
    isz = s.get("isize", 40)
    for i, it in enumerate(s.get("items", [])):
        if isinstance(it, str): it = {"t": it}
        t0 = at_t(s, it.get("at", i))
        p = (t - t0) / 0.45
        lines, lh = layout_rich(it["t"], isz, w - 80, F_SEMI)
        h = len(lines) * int(isz * 1.18)
        if it.get("s"): h += int(isz * 0.78 * 1.25) * len(layout_rich(it["s"], int(isz * 0.78), w - 80, F_REG)[0]) + 6
        if p > 0:
            k = it.get("k", s.get("icon", "check"))
            ic = num_icon(it.get("n", i + 1), 50) if k == "num" else icon(k, 50)
            put(fr, ic, x + 25, y + isz * 0.62, a=clamp(p * 2), sc=eback(p))
            draw_rich(fr, it["t"], x + 76, y, isz, w - 80, t, t0 + 0.08, color=col, fname=F_SEMI,
                      afname=F_BOLD, stagger=0.02, lh=int(isz * 1.18), pop=False)
            if it.get("s"):
                draw_rich(fr, it["s"], x + 76, y + len(lines) * int(isz * 1.18) + 4, int(isz * 0.78), w - 80, t, t0 + 0.25,
                          color=sub, fname=F_REG, stagger=0.012, lh=int(isz * 0.78 * 1.25), pop=False)
        y += h + s.get("igap", 30)
    return y


def r_photo(fr, s, t):
    dark = s.get("bg") == "dark"
    side = s.get("side", "left")
    pw, ph = s.get("pw", 1000), s.get("ph", 680)
    p = clamp(t / max(s["_dur"], 1))
    a = eo(t / 0.55)
    sc = lerp(0.94, 1.0, eo(t / 0.7))
    px = 110 + pw / 2 if side == "left" else W - 110 - pw / 2
    py = H / 2 + 20 + math.sin(t * 0.8) * 4
    photo_card(fr, s["img"], px, py, pw, ph, p, a=a, sc=sc, kb=s.get("kb"), crop=s.get("crop"), border=10)
    if s.get("label"):
        lp = eo((t - 0.6) / 0.5)
        f = font(F_SEMI, 28)
        lw = int(f.getlength(s["label"])) + 40
        lab = rrect(lw, 52, 26, INK).copy()
        ImageDraw.Draw(lab).text((20, 26), s["label"], font=f, fill=WHITE, anchor="lm")
        put(fr, lab, px - pw / 2 + 30, py + ph / 2 - 80 + (1 - lp) * 20, a=lp, anchor="tl")
    tx = (110 + pw + 90) if side == "left" else 120
    tw = W - pw - 110 - 90 - 120
    if "_fit" not in s:
        sc = 1.0
        for _ in range(12):
            ss = dict(s, tsize=int(s.get("tsize", 72) * sc), isize=int(s.get("isize", 40) * sc), igap=int(s.get("igap", 30) * sc))
            dummy = Image.new("RGB", (8, 8))
            h = side_text(dummy, ss, 1e6, 0, 0, tw) - ss["igap"]
            if h <= H - 230: break
            sc *= 0.93
        s["_fit"] = (ss["tsize"], ss["isize"], ss["igap"], (H - h) / 2 + 10)
    ts_, is_, ig_, ty_ = s["_fit"]
    side_text(fr, dict(s, tsize=ts_, isize=is_, igap=ig_), t, tx, s.get("ty", ty_), tw, dark)


_HCACHE = {}
def content_h(s, w):
    k = id(s)
    if k not in _HCACHE:
        dummy = Image.new("RGB", (8, 8))
        _HCACHE[k] = side_text(dummy, s, 1e6, 0, 0, w) - s.get("igap", 30)
    return _HCACHE[k]


def r_bullets(fr, s, t):
    dark = s.get("bg") == "dark"
    w = s.get("w", 1400)
    x = (W - w) / 2
    ch = content_h(s, w)
    top = (H - ch) / 2 + 10
    if s.get("panel", True) and not dark:
        a = eo(t / 0.5)
        card(fr, x - 80, top - 70, w + 160, ch + 140, a=a, fill=PAPER, r=30, sc=lerp(0.97, 1, a))
    side_text(fr, s, t, x, top, w, dark)


def r_cards(fr, s, t):
    dark = s.get("bg") == "dark"
    cols = s["cols"]
    n = len(cols)
    ch = s.get("ch", 640)
    top = max(250, (H - ch) / 2 + 70)
    if s.get("title"):
        draw_rich(fr, s["title"], W / 2, top - 120, s.get("tsize", 64), 1700, t, 0.0, color=WHITE if dark else INK, align="center")
    gap = 44
    cw = int((W - 220 - gap * (n - 1)) / n)
    for i, c in enumerate(cols):
        t0 = at_t(s, c.get("at", i))
        p = (t - t0) / 0.55
        if p <= 0: continue
        x = 110 + i * (cw + gap)
        y = top + (1 - eo(p)) * 60
        card(fr, x, y, cw, ch, a=clamp(p * 1.6), fill=PAPER, r=26)
        head = c.get("color", INK)
        hb = rrect(cw, 120, 26, head).copy()
        ImageDraw.Draw(hb).rectangle((0, 70, cw, 120), fill=head)
        put(fr, hb, x, y, a=clamp(p * 1.6), anchor="tl")
        f = font(F_BIG, c.get("hsize", 52))
        hsz = c.get("hsize", s.get("hsize", 52))
        while hsz > 26 and font(F_BIG, hsz).getlength(c["head"]) > cw - 64: hsz -= 2
        hs = word_sprite(c["head"], F_BIG, hsz, WHITE)
        put(fr, hs, x + 36, y + 60 - hs.height / 2, a=clamp(p * 1.6), anchor="tl")
        yy = y + 150
        if c.get("tag"):
            f = font(F_BOLD, 30)
            tw_ = int(f.getlength(c["tag"])) + 40
            tp = rrect(tw_, 50, 25, CREAM2).copy()
            ImageDraw.Draw(tp).text((tw_ / 2, 25), c["tag"], font=f, fill=head if head != INK else INK, anchor="mm")
            put(fr, tp, x + 36, yy, a=clamp(p * 1.6), anchor="tl")
            yy += 76
        rsz = c.get("rsize", s.get("rsize", 34))
        for j, row in enumerate(c.get("rows", [])):
            if isinstance(row, str): row = {"t": row}
            rt0 = at_t(s, row["at"]) if "at" in row else t0 + 0.25 + j * 0.12
            rp = (t - rt0) / 0.4
            if rp > 0:
                k = row.get("k", "dot")
                if k == "dot":
                    put(fr, rrect(14, 14, 7, head if head != INK else RED), x + 46, yy + rsz * 0.6, a=clamp(rp * 2))
                else:
                    put(fr, icon(k, 38), x + 50, yy + rsz * 0.6, a=clamp(rp * 2), sc=eback(rp))
                draw_rich(fr, row["t"], x + 84, yy, rsz, cw - 120, t, rt0, color=INK, fname=F_SEMI, afname=F_BOLD,
                          stagger=0.015, lh=int(rsz * 1.2), pop=False)
            lines, _ = layout_rich(row["t"], rsz, cw - 120, F_SEMI)
            yy += len(lines) * int(rsz * 1.2) + s.get("rgap", 22)
        if c.get("badge"):
            bt0 = at_t(s, c.get("badge_at", c.get("at", i)))
            bp = (t - bt0 - 0.3) / 0.5
            if bp > 0:
                f = font(F_BOLD, 30)
                bw = int(f.getlength(c["badge"])) + 50
                b = rrect(bw, 58, 29, RED).copy()
                ImageDraw.Draw(b).text((bw / 2, 29), c["badge"], font=f, fill=WHITE, anchor="mm")
                put(fr, b, x + cw / 2, y + ch - 60, a=clamp(bp * 2), sc=eback(bp), rot=-3)


def r_stat(fr, s, t):
    dark = s.get("bg") == "dark"
    col = WHITE if dark else INK
    p = eo((t - 0.1) / 1.1)
    v = s["value"]
    if s.get("count"):
        num = float(re.sub(r"[^\d.]", "", v))
        dec = len(v.split(".")[1]) if "." in v else 0
        cur = num * p
        txt = f"{cur:,.{dec}f}" if "," in v else f"{cur:.{dec}f}"
        txt = s.get("prefix", "") + txt
    else:
        txt = s.get("prefix", "") + v
    big = word_sprite(txt, F_BIG, s.get("size", 330), RED)
    unit = word_sprite(s.get("unit", ""), F_BIG, int(s.get("size", 330) * 0.42), col) if s.get("unit") else None
    tw = big.width + (unit.width + 10 if unit else 0)
    x0 = W / 2 - tw / 2
    y0 = H / 2 - 110
    put(fr, big, x0, y0 - big.height / 2, a=clamp(t / 0.3), anchor="tl", sc=1.0)
    if unit:
        put(fr, unit, x0 + big.width + 10, y0 - big.height / 2 + big.info["pad"] + big.info["asc"] - unit.info["asc"] - unit.info["pad"],
            a=clamp((t - 0.3) / 0.3), anchor="tl")
    draw_rich(fr, s["caption"], W / 2, y0 + big.height / 2 + 30, s.get("csize", 52), 1400, t, at_t(s, s.get("cap_at", 0)) + 0.4,
              color=col, fname=F_BOLD, align="center", stagger=0.03)
    if s.get("note"):
        t0 = at_t(s, s.get("note_at", 1))
        pp = eo((t - t0) / 0.5)
        spr = word_sprite(s["note"], F_MED, 34, (175, 172, 165) if dark else SOFT)
        put(fr, spr, W / 2, H - 150 + (1 - pp) * 16, a=pp)


def r_tiers(fr, s, t):
    title = s.get("title")
    if title: draw_rich(fr, title, W / 2, 130, 64, 1700, t, 0, align="center")
    items = s["items"]
    n = len(items)
    bw, gap = 360, 120
    x0 = W / 2 - (n * bw + (n - 1) * gap) / 2
    base = H - 190
    mx = max(i["h"] for i in items)
    for i, it in enumerate(items):
        t0 = at_t(s, it.get("at", i))
        p = eo((t - t0) / 0.8)
        if p <= 0: continue
        h = int(560 * it["h"] / mx * p)
        x = x0 + i * (bw + gap)
        col = it.get("color", INK)
        if h > 4:
            put(fr, shadow(bw, h, 20, op=0.2), x + bw / 2, base - h / 2 + 10)
            put(fr, rrect(bw, max(h, 41), 20, col), x, base - h, anchor="tl")
        lab = word_sprite(it["tag"], F_BIG, 86, WHITE)
        if h > 140: put(fr, lab, x + bw / 2, base - h + 80, a=clamp((t - t0 - 0.4) / 0.3))
        nm = word_sprite(it["name"], F_BOLD, 44, INK)
        put(fr, nm, x + bw / 2, base + 44, a=p)
        if it.get("note"):
            ns = word_sprite(it["note"], F_MED, 30, SOFT)
            put(fr, ns, x + bw / 2, base - h - 36, a=clamp((t - t0 - 0.6) / 0.4))
    if s.get("foot"):
        t0 = at_t(s, s.get("foot_at", n))
        pp = eo((t - t0) / 0.5)
        spr = word_sprite(s["foot"], F_MED, 34, SOFT)
        put(fr, spr, W / 2, H - 60 + (1 - pp) * 10, a=pp)


def r_palette(fr, s, t):
    draw_rich(fr, s["title"], W / 2, 150, 70, 1700, t, 0, align="center")
    sw = s["swatches"]; n = len(sw)
    w, gap = 300, 34
    x0 = W / 2 - (n * w + (n - 1) * gap) / 2
    for i, (name, hexc, tag) in enumerate(sw):
        t0 = at_t(s, s.get("at", [0] * n)[i]) + i * 0.12
        p = (t - t0) / 0.6
        if p <= 0: continue
        col = tuple(int(hexc[j:j + 2], 16) for j in (1, 3, 5))
        x = x0 + i * (w + gap)
        y = 320 + (1 - eo(p)) * 80
        card(fr, x, y, w, 560, a=clamp(p * 1.5), fill=PAPER, r=24)
        put(fr, rrect(w - 30, 380, 16, col), x + 15, y + 15, a=clamp(p * 1.5), anchor="tl")
        ns = word_sprite(name, F_BOLD, 38, INK)
        put(fr, ns, x + 28, y + 420, a=clamp(p * 1.5), anchor="tl")
        ts = word_sprite(tag, F_MED, 24, SOFT)
        put(fr, ts, x + 28, y + 476, a=clamp(p * 1.5), anchor="tl")
    if s.get("foot"):
        t0 = at_t(s, s.get("foot_at", 1))
        pp = eo((t - t0) / 0.5)
        draw_rich(fr, s["foot"], W / 2, H - 150, 44, 1600, t, t0, color=INK, fname=F_BOLD, align="center", stagger=0.03)


def r_end(fr, s, t):
    dark = s.get("bg", "dark") == "dark"
    col = WHITE if dark else INK
    y = 300
    y += draw_rich(fr, s["title"], W / 2, y, 96, 1600, t, 0.1, color=col, align="center") + 40
    p = eo((t - at_t(s, s.get("url_at", 1))) / 0.5)
    if p > 0:
        f = font(F_BOLD, 46)
        uw = int(f.getlength(s["url"])) + 90
        pill = rrect(uw, 100, 50, RED).copy()
        ImageDraw.Draw(pill).text((uw / 2, 50), s["url"], font=f, fill=WHITE, anchor="mm")
        put(fr, pill, W / 2, y + 60, a=p, sc=eback(p))
    if s.get("sub"):
        pp = eo((t - at_t(s, s.get("sub_at", 1)) - 0.3) / 0.5)
        spr = word_sprite(s["sub"], F_MED, 38, (175, 172, 165) if dark else SOFT)
        put(fr, spr, W / 2, y + 190, a=pp)


# --- diagrams --------------------------------------------------------------
def _drops(seed, n):
    rng = random.Random(seed)
    return [(rng.random(), rng.random(), rng.uniform(0.7, 1.3)) for _ in range(n)]


def wall_section(fr, ox, oy, h, t, mode="rain", labels=None, la=None, scale=1.0, show_rain=True):
    """Vertical wall section. mode: 'rain' (drained cavity) or 'sealed'.
    Layers left->right: sheathing | WRB | cavity (+furring) | siding. Rain comes from the right."""
    g = ImageDraw.Draw(fr)
    S = scale
    sh_w, wrb_w, cav_w, sid_w = int(70 * S), int(10 * S), int(46 * S) if mode == "rain" else 0, int(40 * S)
    x = ox
    # sheathing (wood)
    g.rectangle((x, oy, x + sh_w, oy + h), fill=(214, 182, 132))
    for yy in range(oy + 20, oy + h, int(46 * S)):
        g.line((x + 6, yy, x + sh_w - 6, yy + 8), fill=(196, 160, 110), width=2)
    xs = {"sheathing": x + sh_w / 2}
    x += sh_w
    g.rectangle((x, oy, x + wrb_w, oy + h), fill=(236, 240, 246))
    g.line((x + wrb_w, oy, x + wrb_w, oy + h), fill=(170, 182, 200), width=2)
    xs["wrb"] = x + wrb_w / 2
    x += wrb_w
    if mode == "rain":
        g.rectangle((x, oy, x + cav_w, oy + h), fill=(250, 248, 244))
        # furring strip behind (drawn as hatched band, light)
        xs["cavity"] = x + cav_w / 2
        xs["furring"] = x + cav_w / 2
        cav_x0, cav_x1 = x, x + cav_w
        x += cav_w
    # siding: lapped boards (sloped)
    bh = int(78 * S)
    for yy in range(oy, oy + h, bh):
        y2 = min(yy + bh, oy + h); k = (y2 - yy) / bh
        poly = [(x, yy), (x + sid_w * 0.55, yy), (x + sid_w * (0.55 + 0.45 * k), y2), (x, y2)]
        g.polygon(poly, fill=(58, 62, 70))
        g.line((x + sid_w * 0.55, yy, x + sid_w * (0.55 + 0.45 * k), y2), fill=(40, 42, 48), width=2)
    xs["siding"] = x + sid_w / 2
    sid_x1 = x + sid_w
    # bottom vent + screen
    if mode == "rain":
        g.rectangle((cav_x0, oy + h, cav_x1, oy + h + int(16 * S)), fill=(120, 120, 120))
        for k in range(cav_x0 + 3, cav_x1, 6):
            g.line((k, oy + h, k, oy + h + int(16 * S)), fill=(200, 200, 200), width=1)
        xs["vent"] = (cav_x0 + cav_x1) / 2
    # rain
    if show_rain:
        for i, (a, b, sp) in enumerate(_drops(7, 26)):
            ph = (t * 0.9 * sp + a) % 1.0
            rx = sid_x1 + 34 * S + 14 + b * 190 * S - ph * 30 * S
            ry = oy - 20 + ph * (h + 10)
            g.line((rx, ry, rx - 6 * S, ry + 26 * S), fill=(120, 170, 225), width=max(2, int(3 * S)))
    # water behind siding
    if mode == "rain":
        for i, (a, b, sp) in enumerate(_drops(11, 7)):
            ph = (t * 0.45 * sp + a) % 1.0
            dy = oy + ph * (h + 40)
            dx = cav_x0 + 8 + b * (cav_w - 16)
            r = 5 * S
            al = 255 if dy < oy + h + 10 else 0
            if al: g.ellipse((dx - r, dy - r * 1.3, dx + r, dy + r), fill=(70, 140, 210))
        # air arrows rising
        for i in range(3):
            ph = (t * 0.35 + i / 3) % 1.0
            ay = oy + h - ph * h
            ax = (cav_x0 + cav_x1) / 2
            alpha = math.sin(ph * math.pi)
            if alpha > 0.1:
                c = tuple(int(lerp(250, v, alpha)) for v in (230, 120, 60))
                g.line((ax, ay + 30 * S, ax, ay), fill=c, width=max(2, int(4 * S)))
                g.polygon([(ax - 9 * S, ay + 8 * S), (ax + 9 * S, ay + 8 * S), (ax, ay - 8 * S)], fill=c)
    else:
        # trapped moisture: spreading stain in the sheathing
        k = clamp(t / 6.0)
        r = 14 + 40 * k
        cx, cy = ox + sh_w * 0.7, oy + h * 0.62
        stain = Image.new("RGBA", (int(r * 2.4), int(r * 3.2)), (0, 0, 0, 0))
        ImageDraw.Draw(stain).ellipse((0, 0, stain.width - 1, stain.height - 1), fill=(90, 70, 40, 150))
        stain = stain.filter(ImageFilter.GaussianBlur(8))
        put(fr, stain, cx, cy)
        for i, (a, b, sp) in enumerate(_drops(5, 6)):
            dx = ox + sh_w + wrb_w - 2
            dy = oy + h * (0.35 + 0.5 * a) + math.sin(t * 2 + i) * 2
            g.ellipse((dx - 5, dy - 7, dx + 5, dy + 5), fill=(70, 140, 210))
    return xs, sid_x1


def r_layers(fr, s, t):
    ox, oy, hh = 360, 250, 660
    xs, x1 = wall_section(fr, ox, oy, hh, t, "rain", scale=1.9)
    labels = s["labels"]   # list of (key, text, at, y)
    for i, (key, text, at, yy) in enumerate(labels):
        t0 = at_t(s, at)
        p = eo((t - t0) / 0.45)
        if p <= 0: continue
        g = ImageDraw.Draw(fr)
        lx = xs[key]
        ly = oy + yy if key != "vent" else oy + hh + 16
        tx = 1110
        g.line((lx, ly, lerp(lx, tx - 20, p), ly), fill=INK, width=3)
        g.ellipse((lx - 8, ly - 8, lx + 8, ly + 8), fill=RED)
        spr = word_sprite(text, F_BOLD, 44, INK)
        put(fr, spr, tx, ly - spr.height / 2, a=p, anchor="tl")
        if len(labels[i]) and s.get("subs") and s["subs"].get(key):
            sp = word_sprite(s["subs"][key], F_MED, 30, SOFT)
            put(fr, sp, tx, ly + 22, a=p, anchor="tl")
    if s.get("title"):
        draw_rich(fr, s["title"], 110, 125, 58, 1700, t, 0, fname=F_BIG)


def r_twowalls(fr, s, t):
    for i, (mode, name, verdict, k) in enumerate([("sealed", "Face-sealed wall", "Water is trapped", "x"),
                                                    ("rain", "Rainscreen wall", "Water drains, wall dries", "check")]):
        t0 = at_t(s, s.get("at", [0, 1])[i])
        p = eo((t - t0) / 0.5)
        if p <= 0: continue
        cx = 300 + i * 900
        card(fr, cx - 140, 150, 760, 820, a=p, fill=PAPER, r=30)
        wall_section(fr, cx, 300, 520, max(0, t - t0), mode, scale=1.6)
        put(fr, word_sprite(name, F_BIG, 54, INK), cx - 100, 200, a=p, anchor="tl")
        put(fr, icon(k, 56), cx - 72, 915, a=p, sc=eback((t - t0) / 0.5))
        vs = word_sprite(verdict, F_BOLD, 42, RED if k == "x" else INK)
        put(fr, vs, cx - 30, 915 - vs.height / 2, a=p, anchor="tl")


RENDERERS = dict(kinetic=r_kinetic, q=r_question, photo=r_photo, bullets=r_bullets, cards=r_cards,
                 stat=r_stat, tiers=r_tiers, palette=r_palette, end=r_end, layers=r_layers, twowalls=r_twowalls)


def render_scene(s, t, seed):
    bgk = s.get("bg", "dark" if s["kind"] in ("q", "end") else "cream")
    fr = background(bgk, t + s["_start"], seed)
    RENDERERS[s["kind"]](fr, s, t)
    return fr


# ------------------------------------------------------------------ timeline + video
def build_timeline(scenes, durs):
    """durs: per scene list of per-sentence durations (s). Adds _start,_dur,_cues, _aud (abs sentence starts)."""
    T = 0.0
    for i, s in enumerate(scenes):
        lead = 0.55 if i == 0 else s.get("lead", 0.35)
        cues, lt = [], lead
        for d in durs[i]:
            cues.append((lt, lt + d)); lt += d + s.get("gap", 0.30)
        lt -= s.get("gap", 0.30) if durs[i] else 0
        dur = max(lt + s.get("tail", 0.55), s.get("min", 2.2))
        s["_start"], s["_dur"], s["_cues"] = T, dur, cues
        T += dur
    return T


def frame_at(scenes, T, total, chapters):
    i = 0
    while i + 1 < len(scenes) and scenes[i + 1]["_start"] <= T: i += 1
    s = scenes[i]
    lt = T - s["_start"]
    fr = render_scene(s, lt, i)
    if i > 0 and lt < TR:
        prev = scenes[i - 1]
        a = render_scene(prev, T - prev["_start"], i - 1)
        e = eio(lt / TR)
        fr = Image.blend(a, fr, e)
    dark = s.get("bg", "dark" if s["kind"] in ("q", "end") else "cream") == "dark"
    if s["kind"] not in ("q", "end") and i > 0:
        lab = None
        for (st, name) in chapters:
            if st <= s["_start"] + 0.01: lab = name
        chapter_tag(fr, lab, eo(lt / 0.5), dark)
    progress(fr, T / total, dark)
    return fr


def render_video(scenes, total, chapters, out_path, start=0.0, end=None, fps=FPS):
    end = total if end is None else end
    n0, n1 = int(start * fps), int(end * fps)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", os.environ.get("CRF", "20"), "-pix_fmt", "yuv420p", out_path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(n0, n1):
        fr = frame_at(scenes, n / fps, total, chapters)
        pr.stdin.write(fr.tobytes())
        if n % 300 == 0: print(f"  frame {n}/{n1}", flush=True)
    pr.stdin.close(); pr.wait()
