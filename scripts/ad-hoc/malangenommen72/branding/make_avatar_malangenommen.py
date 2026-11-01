# Profilbild malangenommen72 – DARK-Stil (Stil A: weiße Linien auf Schwarz), 1080x1080, kreis-sicher.
import math
from PIL import Image, ImageDraw, ImageFont
S = 1080; C = S / 2; W_ = (255, 255, 255)
def ms(size, w):
    f = ImageFont.truetype("/tmp/fonts/Montserrat.ttf", size); f.set_variation_by_name(w); return f
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 30)
im = Image.new("RGB", (S, S), (0, 0, 0)); d = ImageDraw.Draw(im)
for x in range(0, S, 54): d.line((x, 0, x, S), fill=(24, 24, 24))
for y in range(0, S, 54): d.line((0, y, S, y), fill=(24, 24, 24))
d.ellipse((90, 90, S - 90, S - 90), outline=W_, width=6)
d.ellipse((120, 120, S - 120, S - 120), outline=(90, 90, 90), width=2)
for k in range(72):
    a = math.radians(k * 5); r0 = 455 if k % 6 else 435
    d.line((C + r0 * math.cos(a), C + r0 * math.sin(a), C + 470 * math.cos(a), C + 470 * math.sin(a)), fill=(200, 200, 200), width=3)
# crescent moon as outline: outer arc + inner arc
R, mx, my = 210, C - 70, 420
off = (95, -70); r2 = 190
def inside2(px, py): return math.dist((px, py), (mx + off[0], my + off[1])) < r2
outer = [(mx + R * math.cos(math.radians(t)), my + R * math.sin(math.radians(t))) for t in range(0, 361, 2)]
inner = [(mx + off[0] + r2 * math.cos(math.radians(t)), my + off[1] + r2 * math.sin(math.radians(t))) for t in range(0, 361, 2)]
def draw_run(pts, keep):
    run = []
    for p in pts:
        if keep(p): run.append(p)
        else:
            if len(run) > 1: d.line(run, fill=W_, width=9, joint="curve")
            run = []
    if len(run) > 1: d.line(run, fill=W_, width=9, joint="curve")
draw_run(outer, lambda p: not inside2(*p))
draw_run(inner, lambda p: math.dist(p, (mx, my)) < R)
# construction lines (technical drawing)
d.line((mx, my - R - 40, mx, my + R + 40), fill=(110, 110, 110), width=2)
d.line((mx - R - 40, my, mx + R + 40, my), fill=(110, 110, 110), width=2)
d.text((mx - R - 30, my - R - 20), "R", font=MONO, fill=(150, 150, 150))
# question mark outline style
d.text((C + 190, 400), "?", font=ms(300, "Bold"), fill=(0, 0, 0), anchor="mm", stroke_width=8, stroke_fill=W_)
d.text((C, 745), "MAL ANGENOMMEN", font=ms(64, "Bold"), fill=W_, anchor="mm")
d.line((C - 250, 795, C + 250, 795), fill=W_, width=4)
d.text((C, 850), "72", font=ms(80, "Bold"), fill=W_, anchor="mm")
d.text((C, 920), "WAS WÄRE WENN", font=MONO, fill=(170, 170, 170), anchor="mm")
im.save("malangenommen72_Profil_Dark.png")
pv = Image.new("RGB", (S, S), (40, 40, 40)); mk = Image.new("L", (S, S), 0); ImageDraw.Draw(mk).ellipse((0, 0, S, S), fill=255)
pv.paste(im, (0, 0), mk); pv.resize((360, 360)).save("/home/user/OmniRoute/_artifacts/malangenommen72/avatar_mal_preview.png")
