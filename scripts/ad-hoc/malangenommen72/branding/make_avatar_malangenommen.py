# Profilbild malangenommen72 – Neon-Lila-Kanallook (Mond + Fragezeichen), 1080x1080, kreis-sicher.
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = 1080; C = S / 2
Y, PINK, CY, DARK, CREAM = (255, 214, 26), (255, 92, 190), (60, 230, 255), (20, 6, 40), (248, 238, 255)
def ms(size, w):
    f = ImageFont.truetype("/tmp/fonts/Montserrat.ttf", size); f.set_variation_by_name(w); return f
LG = lambda size: ImageFont.truetype("/tmp/fonts/LuckiestGuy.ttf", size)
im = Image.new("RGBA", (S, S)); d = ImageDraw.Draw(im)
for i in range(S):
    t = i / S; d.line((0, i, S, i), fill=tuple(int(a + (b - a) * t) for a, b in zip((24, 8, 58), (120, 26, 140))) + (255,))
random.seed(5)
for _ in range(80):
    x, y, r = random.randint(0, S), random.randint(0, S), random.uniform(1.5, 4); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 200))
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
g.ellipse((150, 110, 930, 890), outline=CY + (255,), width=26)
im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)))
d = ImageDraw.Draw(im)
d.ellipse((150, 110, 930, 890), fill=(36, 34, 110, 255), outline=CY + (255,), width=14)
m = Image.new("L", (S, S), 0); md = ImageDraw.Draw(m)
md.ellipse((240, 260, 640, 660), fill=255); md.ellipse((350, 190, 750, 590), fill=0)
moon = Image.new("RGBA", (S, S), Y + (255,))
mg = Image.new("RGBA", (S, S), (0, 0, 0, 0)); mg.paste(moon, (0, 0), m)
im.alpha_composite(mg.filter(ImageFilter.GaussianBlur(18))); im.paste(moon, (0, 0), m)
d.text((690, 400), "?", font=LG(330), fill=CREAM, anchor="mm", stroke_width=12, stroke_fill=DARK)
d.rounded_rectangle((C - 330 + 12, 760 + 14, C + 330 + 12, 900 + 14), radius=70, fill=DARK)
d.rounded_rectangle((C - 330, 760, C + 330, 900), radius=70, fill=PINK, outline=DARK, width=10)
d.text((C, 832), "MAL ANGENOMMEN", font=LG(78), fill=(255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=DARK)
d.text((C, 960), "72", font=LG(90), fill=Y, anchor="mm", stroke_width=8, stroke_fill=DARK)
im.convert("RGB").save("malangenommen72_Profil_Neon.png")
pv = Image.new("RGB", (S, S), (40, 40, 40)); mk = Image.new("L", (S, S), 0); ImageDraw.Draw(mk).ellipse((0, 0, S, S), fill=255)
pv.paste(im.convert("RGB"), (0, 0), mk); pv.resize((360, 360)).save("/home/user/OmniRoute/_artifacts/malangenommen72/avatar_mal_preview.png")
