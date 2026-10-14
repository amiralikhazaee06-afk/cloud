import json, math, os, re, sys, subprocess, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(HERE, "..", "images")
W, H, FPS = 1920, 1080, 30
TR = 0.45                       # crossfade between scenes
RED = (228, 30, 36)
CREAM = (246, 243, 237)
INK = (28, 28, 30)
FD = "/usr/share/fonts/opentype/inter/"

# ---------------------------------------------------------------- timeline
durs = json.load(open(os.path.join(HERE, "tts", "durs.json")))["durs"]
TL = []
t = 0.0
for i, s in enumerate(SCENES):
    lead = 0.7 if i == 0 else 0.35
    tail = 4.0 if i == len(SCENES) - 1 else 0.5
    d = lead + durs[i] + tail
    TL.append(dict(i=i, start=t, dur=d, vs=lead, vd=durs[i], s=s))
    t += d
TOTAL = t

# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eback(x, s=1.6):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

@lru_cache(None)
def font(name, size): return ImageFont.truetype(FD + name + ".otf", size)

@lru_cache(None)
def text_sprite(txt, fname, size, color, glow=None, spacing=0):
    f = font(fname, size)
    asc, desc = f.getmetrics()
    if spacing:
        w = sum(f.getlength(c) for c in txt) + spacing * (len(txt) - 1)
    else:
        w = f.getlength(txt)
    pad = 40 if glow else 12
    im = Image.new("RGBA", (int(w + 2 * pad), asc + desc + 2 * pad), color + (0,))
    d = ImageDraw.Draw(im)
    if spacing:
        x = pad
        for c in txt:
            d.text((x, pad + asc), c, font=f, fill=color + (255,), anchor="ls"); x += f.getlength(c) + spacing
    else:
        d.text((pad, pad + asc), txt, font=f, fill=color + (255,), anchor="ls")
    if glow:
        g = Image.new("RGBA", im.size, glow + (0,))
        g.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(13)).point(lambda v: int(v * 0.85)))
        g.alpha_composite(im); im = g
    im.info["base"] = pad + asc      # baseline y inside the sprite
    im.info["pad"] = pad
    return im

LUTS = {}
def with_alpha(im, a):
    if a >= 0.999: return im
    q = int(a * 64)
    if q not in LUTS: LUTS[q] = [int(v * q / 64) for v in range(256)]
    out = im.copy(); out.putalpha(im.getchannel("A").point(LUTS[q])); return out

def put(fr, im, x, y, a=1.0, sc=1.0, blur=0.0, anchor="c"):
    """Paste RGBA sprite onto RGB frame. (x,y) = centre, or top-left if anchor='tl'."""
    if a <= 0.01: return
    if abs(sc - 1) > 0.004:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    if blur > 0.6: im = im.filter(ImageFilter.GaussianBlur(blur))
    im = with_alpha(im, a)
    if anchor == "c": x, y = x - im.width / 2, y - im.height / 2
    fr.paste(im, (int(round(x)), int(round(y))), im)

def rounded(size, r, fill, ss=2):
    w, h = size
    im = Image.new("RGBA", (w * ss, h * ss), fill[:3] + (0,))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=fill)
    return im.resize((w, h), Image.LANCZOS)

# ---------------------------------------------------------------- images
@lru_cache(None)
def photo(n): return Image.open(os.path.join(IMGDIR, f"{n}.jpg")).convert("RGB")

def kenburns(img, p, tw, th, z0, z1, f0, f1):
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    z = lerp(z0, z1, eio(p) * 0.4 + p * 0.6)
    vw, vh = tw / (s * z), th / (s * z)
    fx, fy = lerp(f0[0], f1[0], p) * iw, lerp(f0[1], f1[1], p) * ih
    x0 = clamp(fx - vw / 2, 0, iw - vw); y0 = clamp(fy - vh / 2, 0, ih - vh)
    return img.resize((tw, th), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))

KB = {  # per-photo zoom / focal moves
    1: (1.05, 1.18, (0.45, 0.5), (0.6, 0.45)),
    2: (1.12, 1.02, (0.5, 0.45), (0.5, 0.5)),
    3: (1.04, 1.16, (0.4, 0.5), (0.55, 0.45)),
    4: (1.0, 1.12, (0.5, 0.55), (0.5, 0.45)),
    5: (1.05, 1.15, (0.55, 0.5), (0.45, 0.45)),
}

# ---------------------------------------------------------------- backgrounds
def _ring(R, th, col):
    ss = 2; S = (R + th) * 2 * ss
    im = Image.new("RGBA", (S, S), col + (0,))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=col + (255,))
    d.ellipse((th * 2 * ss, th * 2 * ss, S - 1 - th * 2 * ss, S - 1 - th * 2 * ss), fill=col + (0,))
    return im.resize((S // ss, S // ss), Image.LANCZOS)

@lru_cache(None)
def bg_light_base():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 80): d.line((x, 0, x, H), fill=(238, 235, 228))
    for y in range(0, H, 80): d.line((0, y, W, y), fill=(238, 235, 228))
    return im

RING = None
def bg_light(u, seed=0):
    global RING
    if RING is None: RING = _ring(760, 70, (206, 203, 199))
    im = bg_light_base().copy()
    side = seed % 2
    cx = (W + 260 if side else -260) + 40 * math.sin(u * 0.35)
    cy = H * 0.5 + 60 * math.sin(u * 0.25 + seed)
    put(im, RING, cx, cy, a=0.55)
    return im

@lru_cache(None)
def bg_dark_base():
    im = Image.new("L", (W // 4, H // 4), 0)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            dx = (x - im.width / 2) / (im.width / 2); dy = (y - im.height / 2) / (im.height / 2)
            px[x, y] = int(26 * clamp(1 - math.sqrt(dx * dx * 0.6 + dy * dy)))
    im = im.resize((W, H), Image.BICUBIC)
    return Image.merge("RGB", (im, im, im.point(lambda v: int(v * 1.08))))

def bg_dark(u, seed=0): return bg_dark_base().copy()

@lru_cache(None)
def dark_overlay(strength):
    g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), int(255 * strength * (0.75 + 0.25 * abs(y / H - 0.5) * 2)))
    g = g.resize((W, H))
    ov = Image.new("RGBA", (W, H), (8, 8, 10, 0)); ov.putalpha(g); return ov

# ---------------------------------------------------------------- kinetic text
def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))

def word_times(sc, words, from_cue=None):
    """Estimate when each on-screen word is spoken (local seconds)."""
    sub = sc["s"]["sub"]; L = len(sub)
    toks = [(m.start(), norm(m.group())) for m in re.finditer(r"\S+", sub)]
    j = 0
    if from_cue:
        p = sub.lower().find(from_cue.lower())
        while j < len(toks) and toks[j][0] < p: j += 1
    out, last = [], sc["vs"]
    for w in words:
        nw, k = norm(w), j
        while k < len(toks) and toks[k][1] != nw: k += 1
        if k < len(toks):
            last = sc["vs"] + sc["vd"] * toks[k][0] / L - 0.08; j = k + 1
        else:
            last += 0.18
        out.append(max(0.05, last))
    # keep monotonic & spaced
    for i in range(1, len(out)): out[i] = max(out[i], out[i - 1] + 0.1)
    return out

def cue_time(sc, cue, frac=None):
    sub = sc["s"]["sub"].lower()
    if frac is not None: return sc["vs"] + sc["vd"] * frac
    p = sub.find(cue.lower())
    if p < 0: p = 0
    return sc["vs"] + sc["vd"] * p / len(sub) - 0.1

def layout_lines(lines, dark, cx, cy, small=72, big=132, align="c", maxw=1640):
    """Return tokens: dict(sprite, x(center), base_y, word)."""
    col = (255, 255, 255) if dark else INK
    rows = []
    for ln in lines:
        parts = re.split(r"(\*[^*]+\*)", ln)
        toks = []
        for p in parts:
            if not p.strip(): continue
            acc = p.startswith("*")
            for w in p.strip("*").split():
                toks.append((w, acc))
        rows.append(toks)
    scale = 1.0
    while True:
        built, widths = [], []
        for toks in rows:
            items, x = [], 0
            for w, acc in toks:
                sz = int((big if acc else small) * scale)
                sp = text_sprite(w, "InterDisplay-ExtraBold" if acc else "InterDisplay-Bold", sz,
                                 RED if acc else col, glow=(RED if (acc and dark) else None))
                gw = font("InterDisplay-ExtraBold" if acc else "InterDisplay-Bold", sz).getlength(w)
                items.append([sp, x, gw, w, sz]); x += gw + sz * 0.26
            widths.append(x - items[-1][4] * 0.26)
            built.append(items)
        if max(widths) <= maxw: break
        scale *= 0.92
    heights = [max(it[4] for it in r) * 1.08 for r in built]
    tot = sum(heights)
    y = cy - tot / 2
    out = []
    for r, wdt, hh in zip(built, widths, heights):
        base = y + hh * 0.82
        x0 = cx - wdt / 2 if align == "c" else cx
        for sp, x, gw, w, sz in r:
            out.append(dict(sp=sp, x=x0 + x + gw / 2, base=base, w=w))
        y += hh
    return out

def draw_tokens(fr, toks, times, u, ):
    for tk, t0 in zip(toks, times):
        p = (u - t0) / 0.38
        if p <= 0: continue
        e = eo(p)
        sp = tk["sp"]
        cy = tk["base"] - sp.info["base"] + sp.height / 2
        put(fr, sp, tk["x"], cy + (1 - e) * 26, a=clamp(p * 1.6), sc=lerp(1.22, 1.0, e), blur=(1 - e) * 9)

# ---------------------------------------------------------------- icons & cards
@lru_cache(None)
def icon(kind, s=46):
    ss = 4; S = s * ss
    im = Image.new("RGBA", (S, S), (255, 255, 255, 0)); d = ImageDraw.Draw(im)
    if kind == "ok":
        d.ellipse((0, 0, S - 1, S - 1), fill=(255, 255, 255, 255))
        d.line([(S * .27, S * .52), (S * .44, S * .68), (S * .74, S * .34)], fill=(40, 150, 90, 255), width=int(S * .1), joint="curve")
    elif kind == "no":
        d.ellipse((0, 0, S - 1, S - 1), fill=RED + (255,))
        w = int(S * .1)
        d.line([(S * .33, S * .33), (S * .67, S * .67)], fill=(255, 255, 255, 255), width=w)
        d.line([(S * .67, S * .33), (S * .33, S * .67)], fill=(255, 255, 255, 255), width=w)
    elif kind == "warn":
        d.polygon([(S * .5, S * .04), (S * .98, S * .92), (S * .02, S * .92)], fill=RED + (255,))
        d.line([(S * .5, S * .34), (S * .5, S * .62)], fill=(255, 255, 255, 255), width=int(S * .09))
        d.ellipse((S * .45, S * .72, S * .55, S * .82), fill=(255, 255, 255, 255))
    else:
        d.ellipse((S * .3, S * .3, S * .7, S * .7), fill=RED + (255,))
    return im.resize((s, s), Image.LANCZOS)

@lru_cache(None)
def pin_sprite():
    ss = 4; S = 60 * ss
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((S * .18, S * .26, S * .86, S * .94), fill=(0, 0, 0, 70))
    d.ellipse((S * .1, S * .1, S * .8, S * .8), fill=(200, 18, 26, 255))
    d.ellipse((S * .22, S * .18, S * .48, S * .42), fill=(255, 140, 140, 200))
    return im.resize((60, 60), Image.LANCZOS)

CARD_COL = (92, 95, 100)
@lru_cache(None)
def card_parts(idx):
    s = SCENES[idx]
    items = s["items"]
    CW = 1000 if len(items) <= 4 else 980
    pad = 60
    row = 74
    kick_h, head_h = 40, 92
    top = 70
    items_y = top + kick_h + head_h + 40
    CH = items_y + row * len(items) + 40
    base = rounded((CW, CH), 26, CARD_COL + (255,))
    d = ImageDraw.Draw(base)
    if s.get("kicker"):
        sp = text_sprite(s["kicker"], "Inter-SemiBold", 24, (214, 216, 220), spacing=3)
        base.alpha_composite(sp, (pad - sp.info["pad"], top - sp.info["pad"]))
    if s.get("badge"):
        sp = text_sprite(s["badge"], "Inter-Bold", 26, (255, 255, 255))
        bw = int(font("Inter-Bold", 26).getlength(s["badge"])) + 44
        pill = rounded((bw, 48), 24, RED + (255,))
        base.alpha_composite(pill, (CW - pad - bw, top - 8))
        base.alpha_composite(sp, (int(CW - pad - bw + 22 - sp.info["pad"]), int(top - 8 + 24 - sp.height / 2 + 2)))
    hs = text_sprite(s["head"], "InterDisplay-Bold", 80, (255, 255, 255))
    base.alpha_composite(hs, (pad - hs.info["pad"], int(top + kick_h + 72 - hs.info["base"])))
    d.rectangle((pad, items_y - 18, CW - pad, items_y - 14), fill=(52, 54, 58, 255))
    sprites = []
    for kind, txt, cue in items:
        ic = icon(kind)
        ts = text_sprite(txt, "Inter-SemiBold", 42, (255, 255, 255))
        it = Image.new("RGBA", (CW - 2 * pad + 20, row), (255, 255, 255, 0))
        it.alpha_composite(ic, (0, (row - ic.height) // 2))
        it.alpha_composite(ts, (ic.width + 24 - ts.info["pad"], int(row / 2 - ts.height / 2 + 2)))
        sprites.append(it)
    P = 90
    canvas = (CW + 2 * P, CH + 2 * P)
    sh = Image.new("RGBA", canvas, (0, 0, 0, 0))
    sh.paste(Image.new("RGBA", (CW, CH), (0, 0, 0, 110)), (P, P + 28))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    return dict(base=base, items=sprites, CW=CW, CH=CH, pad=pad, row=row, items_y=items_y, P=P, shadow=sh)

def draw_card(fr, sc, u, cx, cy):
    idx = sc["i"]; cp = card_parts(idx); s = sc["s"]
    card = cp["base"].copy()
    times = [cue_time(sc, c) for _, _, c in s["items"]]
    for k, (it, t0) in enumerate(zip(cp["items"], times)):
        p = (u - t0) / 0.4
        if p <= 0: continue
        e = eo(p)
        card.alpha_composite(with_alpha(it, clamp(p * 1.5)), (int(cp["pad"] - 30 * (1 - e)), cp["items_y"] + k * cp["row"]))
    P = cp["P"]
    canv = Image.new("RGBA", (cp["CW"] + 2 * P, cp["CH"] + 2 * P), CARD_COL + (0,))
    canv.alpha_composite(card, (P, P))
    rest = -1.4 if idx % 2 else 1.2
    ang = rest + 10 * math.exp(-3.2 * u) * math.cos(7 * u) + 0.25 * math.sin(u * 1.3)
    pivot = (canv.width / 2, P)
    rc = canv.rotate(ang, resample=Image.BICUBIC, center=pivot)
    rs = cp["shadow"].rotate(ang, resample=Image.BILINEAR, center=pivot)
    e = eback(u / 0.7, 1.2)
    a = clamp(u / 0.35)
    top = cy - cp["CH"] / 2 - P - (1 - e) * 90
    left = cx - canv.width / 2
    put(fr, rs, left, top, a=a * 0.9, anchor="tl")
    put(fr, rc, left, top, a=a, anchor="tl")
    pp = (u - 0.45) / 0.3
    if pp > 0:
        put(fr, pin_sprite(), cx, top + P + 4, a=clamp(pp * 2), sc=lerp(1.8, 1.0, eo(pp)))

# ---------------------------------------------------------------- misc sprites
@lru_cache(None)
def mountains():
    ss = 2; h = 300
    im = Image.new("RGBA", (W * ss, h * ss), (196, 192, 186, 0)); d = ImageDraw.Draw(im)
    for layer, (col, amp, base, seed) in enumerate([((214, 210, 204), 150, 250, 3), ((190, 186, 180), 190, 290, 7)]):
        rnd = random.Random(seed); pts = []; x = 0
        while x <= W + 80:
            pts.append((x * ss, (base - rnd.uniform(0.25, 1) * amp) * ss)); x += rnd.uniform(90, 220)
            pts.append((x * ss, (base - rnd.uniform(0, 0.35) * amp) * ss)); x += rnd.uniform(60, 160)
        d.line(pts, fill=col + (255,), width=5 * ss, joint="curve")
    return im.resize((W, h), Image.LANCZOS)

@lru_cache(None)
def thumb(n, w=330, h=220, rot=0):
    im = photo(n); s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    b = 10
    fr = Image.new("RGBA", (w + 2 * b + 60, h + 2 * b + 60), (0, 0, 0, 0))
    sh = Image.new("RGBA", fr.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (30, 44, 30 + w + 2 * b, 44 + h + 2 * b))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    fr.paste((255, 255, 255, 255), (30, 30, 30 + w + 2 * b, 30 + h + 2 * b))
    fr.paste(im, (30 + b, 30 + b))
    return fr.rotate(rot, resample=Image.BICUBIC, expand=True)

@lru_cache(None)
def rounded_photo_mask(w, h, r):
    return rounded((w, h), r, (255, 255, 255, 255)).getchannel("A")

def pill(text, dark=False, size=34):
    return text_sprite(text, "Inter-SemiBold", size, (255, 255, 255) if dark else INK)

@lru_cache(None)
def tag_sprite(text):
    f = font("Inter-SemiBold", 34); w = int(f.getlength(text)) + 64
    p = rounded((w, 66), 33, (255, 255, 255, 255))
    d = ImageDraw.Draw(p)
    d.ellipse((24, 27, 36, 39), fill=RED + (255,))
    d.text((48, 33), text, font=f, fill=INK + (255,), anchor="lm")
    out = Image.new("RGBA", (w + 40, 106), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 50), (20, 28, 20 + w, 28 + 66))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9))); out.alpha_composite(p, (20, 18))
    return out

# ---------------------------------------------------------------- scene renderers
def r_kinetic(sc, u):
    s = sc["s"]; dark = s.get("bg") == "dark"
    fr = bg_dark(u) if dark else bg_light(u, sc["i"])
    toks = layout_lines(s["lines"], dark, W / 2, H / 2 - 30)
    draw_tokens(fr, toks, word_times(sc, [t["w"] for t in toks]), u)
    return fr

def r_photo_text(sc, u):
    s = sc["s"]; z0, z1, f0, f1 = KB[s["img"]]
    fr = kenburns(photo(s["img"]), clamp(u / sc["dur"], 0, 1.1), W, H, z0, z1, f0, f1)
    put(fr, dark_overlay(0.58), 0, 0, anchor="tl")
    toks = layout_lines(s["lines"], True, W / 2, H / 2 - 30, small=78, big=150)
    draw_tokens(fr, toks, word_times(sc, [t["w"] for t in toks]), u)
    return fr

def r_card(sc, u):
    fr = bg_light(u, sc["i"])
    draw_card(fr, sc, u, W / 2, H / 2 - 10)
    return fr

def r_chapter(sc, u):
    s = sc["s"]; fr = bg_light(u, sc["i"])
    num = text_sprite(s["num"], "InterDisplay-Black", 460, (234, 230, 223))
    put(fr, num, W / 2, H / 2 - 40, a=clamp(u / 0.5), sc=lerp(1.15, 1.0, eo(u / 1.2)))
    toks = layout_lines(s["lines"], False, W / 2, H / 2 - 40, small=80, big=140)
    tt = word_times(sc, [t["w"] for t in toks])
    tt = [min(x, 0.25 + 0.16 * k) if k < 99 else x for k, x in enumerate(tt)]   # chapter titles are not spoken
    draw_tokens(fr, toks, tt, u)
    if s.get("grid"):
        for k, n in enumerate([3, 4, 1, 5, 2]):
            p = (u - 0.5 - k * 0.12) / 0.6
            if p <= 0: continue
            th = thumb(n, rot=[-5, 3, -2, 4, -4][k])
            put(fr, th, 230 + k * 365, 880 + (1 - eback(p)) * 260, a=clamp(p * 2))
    else:
        if s["num"] == "01":   # North Shore rain
            d = ImageDraw.Draw(fr); rnd = random.Random(5)
            for k in range(70):
                x0 = rnd.uniform(-200, W); sp = rnd.uniform(700, 1000); ph = rnd.uniform(0, H + 200)
                y = (ph + u * sp) % (H + 200) - 100; x = x0 + y * 0.18
                d.line((x, y, x + 9, y + 50), fill=(214, 211, 205), width=2)
        m = mountains(); wv = int(W * eio(u / 1.8))
        if wv > 2: fr.paste(m.crop((0, 0, wv, m.height)), (0, H - m.height + 10), m.crop((0, 0, wv, m.height)))
    return fr

def r_trio(sc, u):
    s = sc["s"]; fr = bg_dark(u)
    sps = [text_sprite(w, "InterDisplay-Bold", 66, (255, 255, 255)) for w, _ in s["words"]]
    gws = [font("InterDisplay-Bold", 66).getlength(w) for w, _ in s["words"]]
    gap = 120; tot = sum(gws) + gap * (len(gws) - 1)
    x = W / 2 - tot / 2; y = H / 2 - 120
    dot = icon("dot", 40)
    for k, ((w, cue), sp, gw) in enumerate(zip(s["words"], sps, gws)):
        t0 = cue_time(sc, cue); p = (u - t0) / 0.38
        if p > 0:
            e = eo(p); put(fr, sp, x + gw / 2, y + (1 - e) * 24, a=clamp(p * 1.6), sc=lerp(1.2, 1, e), blur=(1 - e) * 8)
            if k: put(fr, dot, x - gap / 2, y + 6, a=clamp(p * 1.6))
        x += gw + gap
    tl, cue = s["tail"]
    toks = layout_lines([tl], True, W / 2, H / 2 + 90, small=84, big=140)
    draw_tokens(fr, toks, word_times(sc, [t["w"] for t in toks], from_cue=cue), u)
    return fr

def r_rainscreen(sc, u):
    fr = bg_light(u, 1)
    s = sc["s"]
    # left text block
    k = text_sprite("HOW A RAINSCREEN WORKS", "Inter-Bold", 26, RED, spacing=4)
    put(fr, k, 150 - k.info["pad"], 300, a=clamp(u / 0.4), anchor="tl")
    t1 = text_sprite("Rainscreen", "InterDisplay-ExtraBold", 120, INK)
    put(fr, t1, 150 - t1.info["pad"] - (1 - eo(u / 0.6)) * 40, 345, a=clamp(u / 0.5), anchor="tl")
    for j, ln in enumerate(["A drained air gap", "behind your siding"]):
        sp = text_sprite(ln, "Inter-Medium", 48, (90, 90, 92)); p = (u - 0.35 - j * 0.15) / 0.5
        put(fr, sp, 150 - sp.info["pad"] - (1 - eo(p)) * 40, 510 + j * 64, a=clamp(p), anchor="tl")
    # diagram
    X, Y0, Y1 = 900, 210, 860
    t_struct = 0.3
    t_wrb = cue_time(sc, "rainscreen") - 0.3
    t_gap = cue_time(sc, "small air gap")
    t_sid = cue_time(sc, "behind the siding")
    t_water = cue_time(sc, "lets water drain")
    d = ImageDraw.Draw(fr)
    def reveal(t0): return clamp((u - t0) / 0.5)
    layers = [  # x0, x1, color, t
        (X, X + 28, (232, 232, 232), t_struct),
        (X + 28, X + 210, (238, 205, 128), t_struct + 0.1),
        (X + 210, X + 242, (196, 160, 112), t_struct + 0.2),
        (X + 242, X + 252, (40, 105, 200), t_wrb),
    ]
    for x0, x1, col, t0 in layers:
        p = reveal(t0)
        if p <= 0: continue
        off = (1 - eo(p)) * 60
        c = tuple(int(lerp(CREAM[i], col[i], p)) for i in range(3))
        d.rectangle((x0 + off, Y0, x1 + off, Y1), fill=c)
        if col == (238, 205, 128):   # insulation squiggle
            pts = [(x0 + 20 + off + (x1 - x0 - 40) * (0.5 + 0.5 * math.sin(yy / 18)), yy) for yy in range(Y0, Y1, 4)]
            d.line(pts, fill=tuple(int(lerp(CREAM[i], (205, 165, 80)[i], p)) for i in range(3)), width=3)
    pg = reveal(t_gap)
    if pg > 0:
        c = tuple(int(lerp(CREAM[i], (250, 248, 244)[i], pg)) for i in range(3))
        d.rectangle((X + 252, Y0, X + 292, Y1), fill=c)
        for yy in range(Y0, Y1, 26):
            d.line((X + 292, yy, X + 292, yy + 12), fill=tuple(int(lerp(CREAM[i], 160, pg)) for i in range(3)), width=2)
        # air arrows rising
        for kk in range(5):
            yy = Y1 - ((u * 90 + kk * 130) % (Y1 - Y0))
            a = int(255 * pg * 0.6)
            d.line([(X + 264, yy + 10), (X + 272, yy), (X + 280, yy + 10)], fill=(150, 170, 190), width=3)
    ps = reveal(t_sid)
    if ps > 0:
        off = (1 - eo(ps)) * 80
        boards = Image.new("RGBA", (120, Y1 - Y0 + 40), (0, 0, 0, 0)); bd = ImageDraw.Draw(boards)
        for b in range(9):
            y = b * 78
            bd.polygon([(0, y), (12, y), (34, y + 84), (0, y + 84)], fill=(66, 70, 76, 255))
            bd.line([(12, y), (34, y + 84)], fill=(96, 100, 106, 255), width=2)
        boards = boards.crop((0, 0, 120, Y1 - Y0))
        put(fr, boards, X + 292 + off, Y0, a=ps, anchor="tl")
        # flashing
        d.line([(X + 242, Y1), (X + 240, Y1 + 18), (X + 345, Y1 + 30)], fill=tuple(int(lerp(CREAM[i], 70, ps)) for i in range(3)), width=5)
    pw = clamp((u - t_water) / 0.4)
    if pw > 0:
        drop = icon("dot", 34)
        for kk in range(4):
            q = ((u - t_water) * 0.55 + kk * 0.25) % 1.0
            yy = lerp(Y0, Y1 + 20, q)
            xx = X + 272 + (max(0, yy - Y1) * 4)
            dr = Image.new("RGBA", (22, 30), (40, 130, 230, 0)); ImageDraw.Draw(dr).ellipse((3, 8, 19, 26), fill=(40, 130, 230, 255))
            ImageDraw.Draw(dr).polygon([(11, 0), (4, 14), (18, 14)], fill=(40, 130, 230, 255))
            put(fr, dr, xx, yy, a=pw * clamp((1.0 - q) * 6))
    # labels
    labels = [("Lap siding", X + 316, 300, t_sid + 0.3), ("Drained air gap", X + 272, 420, t_gap + 0.2),
              ("Weather barrier", X + 247, 540, t_wrb + 0.2), ("Sheathing", X + 226, 660, t_struct + 0.9),
              ("Insulated wall", X + 120, 780, t_struct + 1.2)]
    LX = X + 470
    for txt, tx, ty, t0 in labels:
        p = clamp((u - t0) / 0.45)
        if p <= 0: continue
        lc = tuple(int(lerp(CREAM[i], INK[i], p)) for i in range(3))
        d.line((tx, ty, lerp(tx, LX - 16, eo(p)), ty), fill=lc, width=2)
        d.ellipse((tx - 6, ty - 6, tx + 6, ty + 6), fill=lc)
        sp = text_sprite(txt, "Inter-SemiBold", 38, INK)
        put(fr, sp, LX - sp.info["pad"] + (1 - eo(p)) * 20, ty - sp.height / 2 + 4, a=p, anchor="tl")
    return fr

def r_photo_side(sc, u):
    s = sc["s"]; fr = bg_light(u, 0)
    cw, ch = 600, 800
    z0, z1, f0, f1 = KB[s["img"]]
    ph = kenburns(photo(s["img"]), clamp(u / sc["dur"]), cw, ch, z0, z1, f0, f1).convert("RGBA")
    ph.putalpha(rounded_photo_mask(cw, ch, 28))
    e = eo(u / 0.9)
    x = 1310 + (1 - e) * 300
    shd = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0)); shd.paste((0, 0, 0, 80), (60, 84, 60 + cw, 84 + ch))
    put(fr, shd.filter(ImageFilter.GaussianBlur(28)) if u < 1 else _shadow_cache(cw, ch), x, H / 2 + 6, a=clamp(u / 0.6))
    put(fr, ph, x, H / 2, a=clamp(u / 0.6))
    toks = layout_lines(s["lines"], False, 590, H / 2 - 110, small=78, big=130, maxw=900)
    draw_tokens(fr, toks, word_times(sc, [t["w"] for t in toks]), u)
    tags = s["tags"]
    for k, tg in enumerate(tags):
        t0 = sc["vs"] + sc["vd"] * (0.45 + 0.13 * k); p = (u - t0) / 0.45
        if p <= 0: continue
        sp = tag_sprite(tg)
        put(fr, sp, 590, H / 2 + 90 + k * 92 + (1 - eback(p)) * 30, a=clamp(p * 1.6))
    return fr

@lru_cache(None)
def _shadow_cache(cw, ch):
    shd = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0)); shd.paste((0, 0, 0, 80), (60, 84, 60 + cw, 84 + ch))
    return shd.filter(ImageFilter.GaussianBlur(28))

@lru_cache(None)
def lower_third(label, detail):
    f1, f2 = font("InterDisplay-Bold", 60), font("Inter-Medium", 34)
    w = int(max(f1.getlength(label), f2.getlength(detail))) + 90
    im = Image.new("RGBA", (w, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg = rounded((w, 170), 18, (14, 14, 16, 190)); im.alpha_composite(bg)
    d.rectangle((0, 22, 8, 148), fill=RED + (255,))
    d.text((40, 82), label, font=f1, fill=(255, 255, 255, 255), anchor="ls")
    d.text((40, 132), detail, font=f2, fill=(220, 220, 224, 255), anchor="ls")
    return im

def r_showcase(sc, u):
    s = sc["s"]; imgs = s["imgs"]; n = len(imgs); D = sc["dur"] + TR
    seg = D / n; k = min(n - 1, int(u / seg))
    def frame_for(j, uu):
        z0, z1, f0, f1 = KB[imgs[j]]
        return kenburns(photo(imgs[j]), clamp(uu / (seg + 0.8), 0, 1.2), W, H, z0, z1, f0, f1)
    fr = frame_for(k, u - k * seg)
    if k > 0 and u - k * seg < 0.7:
        prev = frame_for(k - 1, u - (k - 1) * seg)
        fr = Image.blend(prev, fr, eio((u - k * seg) / 0.7))
    put(fr, dark_overlay(0.12), 0, 0, anchor="tl")
    lt = lower_third(s["label"], s["detail"])
    p = (u - 0.4) / 0.6
    if p > 0:
        put(fr, lt, 90 - (1 - eo(p)) * 60, 120, a=clamp(p * 1.5), anchor="tl")
    return fr

def r_end(sc, u):
    s = sc["s"]; fr = bg_dark(u)
    thanks = s.get("thanks")
    uu = u + (99 if thanks else 0)
    parts = [("silver", (196, 200, 208)), ("siding", (255, 255, 255)), (".ca", RED)]
    f = font("InterDisplay-ExtraBold", 170)
    tot = sum(f.getlength(p) for p, _ in parts)
    x = W / 2 - tot / 2; y = H / 2 - 40
    for k, (p, col) in enumerate(parts):
        sp = text_sprite(p, "InterDisplay-ExtraBold", 170, col, glow=(RED if col == RED else None))
        gw = f.getlength(p); q = (uu - 0.3 - k * 0.22) / 0.45
        if q > 0:
            e = eo(q)
            put(fr, sp, x + gw / 2, y + (1 - e) * 30, a=clamp(q * 1.6), sc=lerp(1.2, 1, e), blur=(1 - e) * 10)
        x += gw
    kk = text_sprite("REQUEST A QUOTE", "Inter-Bold", 30, RED, spacing=6)
    put(fr, kk, W / 2, y - 150, a=clamp((uu - 0.1) / 0.5))
    sub = text_sprite("Siding installation & replacement  ·  North Vancouver", "Inter-Medium", 38, (190, 190, 196))
    put(fr, sub, W / 2, y + 140, a=clamp((uu - 1.0) / 0.6))
    if thanks:
        q = (u - 0.3) / 0.6
        th = text_sprite("Thanks for watching", "InterDisplay-SemiBold", 54, (255, 255, 255))
        put(fr, th, W / 2, y + 250 + (1 - eo(q)) * 20, a=clamp(q))
        fade = clamp((u - (sc["dur"] - 1.2)) / 1.2)
        if fade > 0: fr = Image.blend(fr, Image.new("RGB", (W, H), (0, 0, 0)), fade)
    return fr

R = dict(kinetic=r_kinetic, photo_text=r_photo_text, card=r_card, chapter=r_chapter, trio=r_trio,
         rainscreen=r_rainscreen, photo_side=r_photo_side, showcase=r_showcase, end=r_end)

# ---------------------------------------------------------------- subtitles
def chunks(text, maxc=58):
    words = text.split(); out, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
            if cur.endswith((".", "?", ":")) and len(cur) > 22: out.append(cur); cur = ""
    if cur: out.append(cur)
    # merge tiny tails
    res = []
    for c in out:
        if res and len(c) < 14 and len(res[-1]) + len(c) < maxc + 10: res[-1] += " " + c
        else: res.append(c)
    return res

SUBS = []
for sc in TL:
    cs = chunks(sc["s"]["sub"]); L = sum(len(c) + 1 for c in cs)
    t0 = sc["start"] + sc["vs"]
    for c in cs:
        d = sc["vd"] * (len(c) + 1) / L
        SUBS.append((t0, t0 + d, c)); t0 += d

@lru_cache(None)
def sub_sprite(txt):
    f = font("Inter-SemiBold", 44)
    w = int(f.getlength(txt)) + 56
    im = rounded((w, 72), 14, (10, 10, 12, 170))
    ImageDraw.Draw(im).text((28, 37), txt, font=f, fill=(255, 255, 255, 255), anchor="lm")
    return im

def draw_sub(fr, t):
    for a, b, txt in SUBS:
        if a - 0.05 <= t < b + 0.12:
            al = clamp((t - a + 0.05) / 0.12) * clamp((b + 0.12 - t) / 0.12)
            put(fr, sub_sprite(txt), W / 2, H - 92, a=al)
            return

@lru_cache(None)
def chap_sprite(txt, dark):
    f = font("Inter-SemiBold", 26)
    w = int(f.getlength(txt)) + 66
    im = rounded((w, 50), 25, (255, 255, 255, 40) if dark else (20, 20, 22, 18))
    d = ImageDraw.Draw(im)
    d.ellipse((22, 19, 34, 31), fill=RED + (255,))
    d.text((44, 26), txt, font=f, fill=((235, 235, 240) if dark else (60, 60, 64)) + (255,), anchor="lm")
    return im

@lru_cache(None)
def wm_sprite(dark):
    return text_sprite("silversiding.ca", "Inter-Bold", 30, (235, 235, 240) if dark else (60, 60, 64))

DARK_KINDS = {"kinetic_dark", "photo_text", "trio", "showcase", "end"}
def is_dark(s): return (s["kind"] + ("_dark" if s.get("bg") == "dark" else "")) in DARK_KINDS or s.get("bg") == "dark"

def render_frame(t):
    i = 0
    while i + 1 < len(TL) and TL[i + 1]["start"] <= t: i += 1
    sc = TL[i]; u = t - sc["start"]
    fr = R[sc["s"]["kind"]](sc, u)
    if i > 0 and u < TR:
        pv = TL[i - 1]
        fr = Image.blend(R[pv["s"]["kind"]](pv, t - pv["start"]), fr, eio(u / TR))
    dark = is_dark(sc["s"])
    if sc["s"]["chap"]:
        a = clamp(u / 0.5) if (i == 0 or TL[i - 1]["s"]["chap"] != sc["s"]["chap"]) else 1
        put(fr, chap_sprite(sc["s"]["chap"], dark), 60, 46, a=a, anchor="tl")
    if sc["s"]["kind"] != "end":
        sp = wm_sprite(dark); put(fr, sp, W - 60 - sp.width + sp.info["pad"], 46, a=0.85, anchor="tl")
    draw_sub(fr, t)
    return fr

def srt():
    def ts(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s_:02d},{ms:03d}"
    return "\n".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{c}\n" for k, (a, b, c) in enumerate(SUBS))

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "still":
        for x in sys.argv[2:]:
            render_frame(float(x)).save(os.path.join(HERE, "out", f"still_{float(x):06.2f}.jpg"), quality=88)
    elif mode == "chunk":
        a, b, path = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
        for n in range(a, b):
            p.stdin.write(render_frame(n / FPS).tobytes())
            if n % 300 == 0: print(path, n, flush=True)
        p.stdin.close(); p.wait()
    elif mode == "info":
        print("TOTAL", TOTAL, "frames", int(math.ceil(TOTAL * FPS)))
        for sc in TL: print(f"{sc['start']:7.2f} {sc['dur']:6.2f} {sc['s']['kind']}")
        open(os.path.join(HERE, "out", "subtitles.srt"), "w").write(srt())
        json.dump([(sc["start"] + sc["vs"]) for sc in TL], open(os.path.join(HERE, "out", "voice_starts.json"), "w"))
