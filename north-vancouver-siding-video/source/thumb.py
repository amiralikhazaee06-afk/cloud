import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = 2; W, H = 1280 * S, 720 * S
FD = "/usr/share/fonts/opentype/inter/"; RED = (228, 30, 36)
F = lambda n, s: ImageFont.truetype(FD + n + ".otf", s * S)
def cover(path, w, h, fx=0.5, fy=0.5, z=1.0):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height) * z
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))
def grad_left(im, strength=235, stop=0.62):
    g = Image.new("L", (W, 1))
    for x in range(W): g.putpixel((x, 0), int(strength * max(0, 1 - x / (W * stop)) ** 1.1))
    ov = Image.new("RGB", (W, H), (6, 6, 8)); im.paste(ov, (0, 0), g.resize((W, H))); return im
def rain(im, n=260, seed=2, alpha=70):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = random.Random(seed)
    for _ in range(n):
        x, y, l = r.uniform(0, W), r.uniform(-50, H), r.uniform(30, 80) * S
        d.line((x, y, x + l * 0.16, y + l), fill=(220, 230, 255, r.randint(alpha // 2, alpha)), width=S)
    im.paste(lay, (0, 0), lay)
def text_shadow(im, xy, txt, font, fill, anchor="ls"):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 4 * S, xy[1] + 6 * S), txt, font=font, fill=(0, 0, 0, 200), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(8 * S)); im.paste(sh, (0, 0), sh)
    ImageDraw.Draw(im).text(xy, txt, font=font, fill=fill, anchor=anchor)
def pill(im, x, y, txt, size=30, bg=RED, fg=(255, 255, 255)):
    f = F("Inter-ExtraBold", size); w = f.getlength(txt) + 44 * S; h = size * S * 1.7
    d = ImageDraw.Draw(im); d.rounded_rectangle((x, y, x + w, y + h), h / 2, fill=bg)
    d.text((x + 22 * S, y + h / 2), txt, font=f, fill=fg, anchor="lm"); return w
def brand(im):
    f = F("Inter-Bold", 30); x, y = 56 * S, H - 52 * S
    d = ImageDraw.Draw(im)
    for part, col in (("silver", (205, 208, 214)), ("siding", (255, 255, 255)), (".ca", RED)):
        text_shadow(im, (x, y), part, f, col); x += f.getlength(part)
IMG = "../images/"
# ---- A: dusk townhomes + rain question
im = cover(IMG + "3.jpg", W, H, fx=0.75, fy=0.35, z=1.05)
im = grad_left(im); rain(im)
pill(im, 56 * S, 52 * S, "NORTH VANCOUVER", 30)
f1, f2 = F("InterDisplay-Black", 128), F("InterDisplay-Black", 150)
text_shadow(im, (52 * S, 300 * S), "WHICH SIDING", f1, (255, 255, 255))
text_shadow(im, (52 * S, 440 * S), "SURVIVES", f1, (255, 255, 255))
text_shadow(im, (52 * S, 600 * S), "THE RAIN?", f2, RED)
brand(im)
im.resize((1280, 720), Image.LANCZOS).save("thumb/thumbnail_A.jpg", quality=92)
# ---- B: brick & stone vs metal split
im = Image.new("RGB", (W, H))
L = cover(IMG + "1.jpg", W // 2 + 40 * S, H, fx=0.62, fy=0.4, z=1.25)
R = cover(IMG + "6.jpg", W // 2 + 40 * S, H, fx=0.5, fy=0.38, z=1.0)
im.paste(L, (0, 0)); m = Image.new("L", R.size, 0); ImageDraw.Draw(m).polygon([(60 * S, 0), (R.width, 0), (R.width, H), (0, H)], fill=255)
im.paste(R, (W // 2 - 40 * S, 0), m)
ov = Image.new("L", (1, H))
for y in range(H): ov.putpixel((0, y), int(225 * max(0, (y / H - 0.42) / 0.58) ** 1.2))
im.paste(Image.new("RGB", (W, H), (6, 6, 8)), (0, 0), ov.resize((W, H)))
top = Image.new("L", (1, H))
for y in range(H): top.putpixel((0, y), int(120 * max(0, 1 - y / (H * 0.25))))
im.paste(Image.new("RGB", (W, H), (6, 6, 8)), (0, 0), top.resize((W, H)))
d = ImageDraw.Draw(im); d.line([(W // 2 + 20 * S, 0), (W // 2 - 40 * S, H)], fill=(255, 255, 255), width=8 * S)
pill(im, 56 * S, 48 * S, "BRICK & STONE", 30, bg=(255, 255, 255), fg=(20, 20, 22))
f = F("Inter-ExtraBold", 30); w = f.getlength("METAL SIDING") + 44 * S
pill(im, W - 56 * S - w, 48 * S, "METAL SIDING", 30, bg=(255, 255, 255), fg=(20, 20, 22))
fv = F("InterDisplay-Black", 90); cx, cy = W // 2 - 10 * S, 300 * S; r = 78 * S
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED); d.text((cx, cy + 4 * S), "VS", font=fv, fill=(255, 255, 255), anchor="mm")
fb = F("InterDisplay-Black", 112)
text_shadow(im, (W // 2, 560 * S), "WHAT LASTS IN", fb, (255, 255, 255), anchor="ms")
text_shadow(im, (W // 2, 680 * S), "NORTH VAN?", fb, RED, anchor="ms")
im.resize((1280, 720), Image.LANCZOS).save("thumb/thumbnail_B.jpg", quality=92)
