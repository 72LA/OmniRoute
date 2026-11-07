# Profilbilder AI72 – Stil A (line) und Stil B (flat). 1080x1080, Inhalt im Kreis (TikTok schneidet rund).
import math
from PIL import Image, ImageDraw, ImageFont
S = 1080; C = S / 2
def ms(size, w):
    f = ImageFont.truetype("/tmp/fonts/Montserrat.ttf", size); f.set_variation_by_name(w); return f
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 30)

def brain(d, cx, cy, r, line, fill=None, width=10, folds=True, mid_end=0.7):
    # two hemispheres made of lobes + centre split + folds
    lobes = [(-0.45, -0.35, 0.42), (-0.62, 0.05, 0.40), (-0.35, 0.35, 0.40), (0.45, -0.35, 0.42), (0.62, 0.05, 0.40), (0.35, 0.35, 0.40), (-0.12, -0.5, 0.36), (0.12, -0.5, 0.36)]
    if fill:
        for x, y, rr in lobes:
            d.ellipse((cx + (x - rr) * r, cy + (y - rr) * r, cx + (x + rr) * r, cy + (y + rr) * r), fill=fill)
    for x, y, rr in lobes:
        d.arc((cx + (x - rr) * r, cy + (y - rr) * r, cx + (x + rr) * r, cy + (y + rr) * r), 0, 360, fill=line, width=width)
    if fill:
        for x, y, rr in lobes:
            q = rr * 0.86
            d.ellipse((cx + (x - q) * r, cy + (y - q) * r, cx + (x + q) * r, cy + (y + q) * r), fill=fill)
    d.line((cx, cy - 0.8 * r, cx, cy + mid_end * r), fill=line, width=width)
    if not folds: return
    for x, y in [(-0.5, -0.2), (0.5, -0.2), (-0.4, 0.3), (0.4, 0.3)]:
        d.arc((cx + (x - 0.18) * r, cy + (y - 0.12) * r, cx + (x + 0.18) * r, cy + (y + 0.12) * r), 200, 340, fill=line, width=width - 2)

LOBES = [(-0.45, -0.35, 0.42), (-0.62, 0.05, 0.40), (-0.35, 0.35, 0.40), (0.45, -0.35, 0.42), (0.62, 0.05, 0.40), (0.35, 0.35, 0.40), (-0.12, -0.5, 0.36), (0.12, -0.5, 0.36), (0, 0.1, 0.45)]
def brain_flat(d, cx, cy, r, fill, out, ow=0.055):
    for x, y, rr in LOBES:
        q = rr + ow; d.ellipse((cx + (x - q) * r, cy + (y - q) * r, cx + (x + q) * r, cy + (y + q) * r), fill=out)
    for x, y, rr in LOBES:
        d.ellipse((cx + (x - rr) * r, cy + (y - rr) * r, cx + (x + rr) * r, cy + (y + rr) * r), fill=fill)

# ---------- Stil A: line ----------
im = Image.new("RGB", (S, S), (0, 0, 0)); d = ImageDraw.Draw(im)
for x in range(0, S, 54): d.line((x, 0, x, S), fill=(24, 24, 24))
for y in range(0, S, 54): d.line((0, y, S, y), fill=(24, 24, 24))
d.ellipse((90, 90, S - 90, S - 90), outline=(255, 255, 255), width=6)
d.ellipse((120, 120, S - 120, S - 120), outline=(90, 90, 90), width=2)
for k in range(72):  # tick ring
    a = math.radians(k * 5); r0 = 455 if k % 6 else 435
    d.line((C + r0 * math.cos(a), C + r0 * math.sin(a), C + 470 * math.cos(a), C + 470 * math.sin(a)), fill=(200, 200, 200), width=3)
brain(d, C, 400, 230, (255, 255, 255), fill=(0, 0, 0), width=9)
# circuit traces from brain
for sx in (-1, 1):
    for k, dy in enumerate((-60, 20, 100)):
        x0 = C + sx * 250; y0 = 400 + dy; x1 = C + sx * (330 + k * 18)
        d.line((x0, y0, x1, y0, x1, y0 + 40), fill=(255, 255, 255), width=5)
        d.ellipse((x1 - 10, y0 + 30, x1 + 10, y0 + 50), outline=(255, 255, 255), width=5)
d.text((C, 770), "AI72", font=ms(210, "Bold"), fill=(255, 255, 255), anchor="mm")
d.line((C - 200, 880, C + 200, 880), fill=(255, 255, 255), width=4)
d.text((C, 925), "FIG. 00 · WISSEN", font=MONO, fill=(170, 170, 170), anchor="mm")
im.save("AI72_Profil_StilA_Lineart.png")

# ---------- Stil B: flat ----------
NAVY, Y, P, CY, OUT = (14, 26, 61), (255, 212, 0), (255, 79, 139), (62, 224, 255), (10, 15, 36)
im = Image.new("RGB", (S, S), NAVY); d = ImageDraw.Draw(im)
for i in range(S):  # gradient
    t = i / S; d.line((0, i, S, i), fill=tuple(int(a + (b - a) * t) for a, b in zip((12, 22, 54), (24, 42, 100))))
import random; random.seed(3)
for _ in range(60):
    x, y, r = random.randint(0, S), random.randint(0, S), random.choice([2, 3, 4]); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
d.ellipse((110, 110, S - 110, S - 110), fill=(30, 50, 115), outline=OUT, width=12)
# memphis bits
d.polygon([(220, 260), (290, 230), (270, 300)], fill=Y, outline=OUT, width=6)
d.ellipse((800, 230, 860, 290), fill=P, outline=OUT, width=6)
d.line([(780 + k * 12, 820 + 14 * math.sin(k * 1.3)) for k in range(9)], fill=CY, width=12, joint="curve")
d.line((230, 780, 290, 780), fill=Y, width=14); d.line((260, 750, 260, 810), fill=Y, width=14)
# brain with shadow
brain_flat(d, C + 16, 418, 230, OUT, OUT)
brain_flat(d, C, 400, 230, P, OUT)
d.line((C, 400 - 0.85 * 230, C, 400 - 0.42 * 230), fill=OUT, width=11)
for x, y in [(-0.55, -0.3), (0.55, -0.3), (-0.62, 0.22), (0.62, 0.22)]:
    d.arc((C + (x - 0.15) * 230, 400 + (y - 0.1) * 230, C + (x + 0.15) * 230, 400 + (y + 0.1) * 230), 200, 340, fill=OUT, width=10)
for x in (-0.42, 0.42):
    d.ellipse((C + x * 230 - 34, 455, C + x * 230 + 34, 485), fill=(255, 170, 205))
# face
d.ellipse((C - 78, 395, C - 42, 435), fill=OUT); d.ellipse((C + 42, 395, C + 78, 435), fill=OUT)
d.chord((C - 48, 440, C + 48, 510), 0, 180, fill=OUT)
# AI72 label pill
d.rounded_rectangle((C - 250 + 14, 690 + 16, C + 250 + 14, 880 + 16), radius=90, fill=OUT)
d.rounded_rectangle((C - 250, 690, C + 250, 880), radius=90, fill=Y, outline=OUT, width=12)
d.text((C, 785), "AI72", font=ms(170, "Black"), fill=OUT, anchor="mm")
im.save("AI72_Profil_StilB_Flat.png")

# preview with circle crop
pv = Image.new("RGB", (S * 2 + 60, S), (40, 40, 40))
for i, f in enumerate(["AI72_Profil_StilA_Lineart.png", "AI72_Profil_StilB_Flat.png"]):
    a = Image.open(f); m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
    pv.paste(a, (i * (S + 60), 0), m)
pv.resize((pv.width // 3, pv.height // 3)).save("/home/user/OmniRoute/_artifacts/malangenommen72/avatar_preview.png")
