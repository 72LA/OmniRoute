import json, math, os, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
EP = sys.argv[1] if len(sys.argv) > 1 else "01"
LINES = json.load(open(f"v{EP}.json"))
DURS = json.load(open("durs.json"))
OUT = "frames"
os.makedirs(OUT, exist_ok=True)

YELLOW = (255, 214, 26)
PINK = (255, 92, 190)
CYAN = (60, 230, 255)
CREAM = (248, 238, 255)
LILAC = (190, 150, 255)
DARK = (20, 6, 40)

def font_lg(size):
    return ImageFont.truetype("/tmp/fonts/LuckiestGuy.ttf", size)

def font_ms(size, weight="ExtraBold"):
    f = ImageFont.truetype("/tmp/fonts/Montserrat.ttf", size)
    f.set_variation_by_name(weight)
    return f

# ---------- timeline ----------
START = 0.15
segs, t = [], START
for line, d in zip(LINES, DURS):
    segs.append((t, t + d, line))
    t += d + line["gap"]
TOTAL = t
if os.path.exists('segs_abs.json'):
    _abs = json.load(open('segs_abs.json'))
    segs = [(a, b, l) for (a, b), l in zip(_abs, LINES)]
    TOTAL = _abs[-1][1] + 1.6
NFRAMES = int(math.ceil(TOTAL * FPS))

# ---------- background ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([24, 8, 58]); mid = np.array([58, 18, 110]); bot = np.array([120, 26, 140])
    col = np.where(y < 0.55, top + (mid - top) * (y / 0.55), mid + (bot - mid) * ((y - 0.55) / 0.45))
    arr = np.repeat(col[:, None, :], W, axis=1).reshape(H, W, 3)
    # soft vignette
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    arr = arr * (1 - 0.45 * np.clip(d - 0.2, 0, 1))[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGB")

BG = make_bg()
random.seed(7)
STARS = [(random.randint(0, W), random.randint(0, H), random.uniform(1.5, 4), random.uniform(0, 6.28)) for _ in range(90)]

def glow(layer, radius=18, strength=2):
    blur = layer.filter(ImageFilter.GaussianBlur(radius))
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    for _ in range(strength):
        out = Image.alpha_composite(out, blur)
    return Image.alpha_composite(out, layer)

# ---------- sprites ----------
def figure(body=PINK, face="neutral", shirt_face=False, phone=False, scale=1.0):
    w, h = 300, 520
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # body
    d.rounded_rectangle((70, 200, 230, 470), radius=70, fill=body + (255,))
    # legs
    d.rounded_rectangle((95, 430, 140, 515), radius=20, fill=body + (255,))
    d.rounded_rectangle((160, 430, 205, 515), radius=20, fill=body + (255,))
    # head
    d.ellipse((75, 30, 225, 180), fill=CREAM + (255,))
    ex = [(122, 98), (178, 98)]
    if face == "shock":
        for x, y in ex:
            d.ellipse((x - 12, y - 14, x + 12, y + 14), fill=DARK + (255,))
        d.ellipse((136, 132, 164, 162), fill=DARK + (255,))
    else:
        for x, y in ex:
            d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=DARK + (255,))
        if face == "smile":
            d.arc((120, 105, 180, 155), 20, 160, fill=DARK + (255,), width=7)
        elif face == "down":
            for x, y in ex:
                d.ellipse((x - 9, y + 4, x + 9, y + 18), fill=DARK + (255,))
        else:
            d.line((130, 140, 170, 140), fill=DARK + (255,), width=7)
    if shirt_face:
        cx, cy = 150, 320
        d.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=YELLOW + (255,))
        d.ellipse((cx - 30, cy - 22, cx - 12, cy - 4), fill=DARK + (255,))
        d.ellipse((cx + 12, cy - 22, cx + 30, cy - 4), fill=DARK + (255,))
        d.chord((cx - 36, cy - 10, cx + 36, cy + 44), 0, 180, fill=DARK + (255,))
        d.chord((cx - 20, cy + 14, cx + 20, cy + 40), 0, 180, fill=PINK + (255,))
    if phone:
        d.rounded_rectangle((150, 230, 205, 320), radius=10, fill=CYAN + (255,))
        d.rounded_rectangle((158, 240, 197, 305), radius=6, fill=(20, 40, 80, 255))
    im = glow(im, 14, 1)
    if scale != 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return im

def moon_logo(size=360):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size, size), fill=(36, 34, 110, 255), outline=CYAN + (255,), width=10)
    m = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(m)
    r = size * 0.32
    cx, cy = size * 0.42, size * 0.55
    md.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    md.ellipse((cx - r + size * 0.16, cy - r - size * 0.1, cx + r + size * 0.16, cy + r - size * 0.1), fill=0)
    moon = Image.new("RGBA", (size, size), YELLOW + (255,))
    im.paste(moon, (0, 0), m)
    f = font_lg(int(size * 0.42))
    d.text((size * 0.68, size * 0.42), "?", font=f, fill=CREAM, anchor="mm", stroke_width=6, stroke_fill=DARK)
    return glow(im, 20, 1)

FIG_PINK = figure(PINK, "neutral")
FIG_SHIRT = figure(PINK, "shock", shirt_face=True)
FIG_LILAC = figure(LILAC, "neutral")
FIG_CYAN = figure(CYAN, "neutral")
FIG_PHONE = figure(LILAC, "down", phone=True)
FIG_SMILE = figure(PINK, "smile")
MOON = moon_logo()

def paste_center(canvas, sprite, cx, cy, scale=1.0, alpha=1.0):
    s = sprite
    if scale != 1.0:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BILINEAR)
    if alpha < 1.0:
        a = s.split()[3].point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    canvas.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def ease_out_back(x):
    x = min(max(x, 0), 1)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def ease_out(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3

def text_center(d, xy, txt, f, fill, stroke=10, sfill=DARK):
    d.text(xy, txt, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sfill)

def title(canvas, txt, lt, size=112):
    s = 0.7 + 0.3 * ease_out_back(lt / 0.35)
    layer = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font_lg(size)
    while d.textlength(txt, font=f) > W - 140:
        size -= 6; f = font_lg(size)
    text_center(d, (W / 2, 150), txt, f, YELLOW, stroke=12)
    layer = glow(layer, 10, 1)
    paste_center(canvas, layer, W / 2, 360, scale=max(0.01, s))

def spotlight(canvas, cx, top_y, bot_y, half_w, alpha):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon([(cx - 30, top_y), (cx + 30, top_y), (cx + half_w, bot_y), (cx - half_w, bot_y)], fill=(255, 240, 150, int(80 * alpha)))
    d.ellipse((cx - half_w, bot_y - 45, cx + half_w, bot_y + 45), fill=(255, 240, 150, int(120 * alpha)))
    layer = layer.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(layer)

# ---------- scenes ----------
CROWD = [(220 + (i % 4) * 213, 590 + (i // 4) * 235) for i in range(8)]

def bars(canvas, d, p1, p2, crowd_hl):
    for i, (x, y) in enumerate(CROWD):
        if i < crowd_hl:
            d.ellipse((x - 85, y - 120, x + 85, y + 120), outline=YELLOW, width=8)
        paste_center(canvas, FIG_LILAC if i % 2 else FIG_CYAN, x, y, scale=0.42)
    fl = font_ms(40)
    fb = font_lg(70)
    base_x, bw, y1, y2, bh = 300, 640, 970, 1075, 75
    for (y, p, lab, col, val) in [(y1, p1, "GESCHÄTZT", PINK, "50 %"), (y2, p2, "ECHT", YELLOW, "~25 %")]:
        if p <= 0:
            continue
        d.text((base_x - 20, y + bh / 2), lab, font=fl, fill=CREAM, anchor="rm", stroke_width=4, stroke_fill=DARK)
        d.rounded_rectangle((base_x, y, base_x + bw, y + bh), radius=40, outline=(255, 255, 255, 90), width=4)
        frac = 0.5 if val == "50 %" else 0.25
        cur = max(bh, int(bw * frac * ease_out(p)))
        d.rounded_rectangle((base_x, y, base_x + cur, y + bh), radius=40, fill=col)
        if p > 0.6:
            d.text((base_x + cur + 20, y + bh / 2), val, font=fb, fill=col, anchor="lm", stroke_width=6, stroke_fill=DARK)

def scene(canvas, name, lt, gt):
    if EP == '02' and scene02(canvas, name, lt, gt):
        return
    d = ImageDraw.Draw(canvas)
    if name in ("shirt", "shirtq"):
        z = 0.95 + 0.25 * ease_out(lt / 2.5) if name == "shirt" else 1.2
        bob = math.sin(gt * 6) * 6
        paste_center(canvas, FIG_SHIRT, W / 2, 800 + bob, scale=z * 1.15)
        title(canvas, "PEINLICHES T-SHIRT", lt if name == "shirt" else 5)
        if name == "shirtq":
            for i, (x, y) in enumerate([(250, 620), (840, 600), (870, 900), (220, 920)]):
                s = ease_out_back((lt - i * 0.12) / 0.3)
                if s > 0.02:
                    f = font_lg(int(130 * s))
                    text_center(d, (x, y), "?", f, YELLOW, stroke=8)
    elif name in ("bars1", "bars2"):
        title(canvas, "WER HAT'S BEMERKT?", lt if name == "bars1" else 5, size=104)
        if name == "bars1":
            hl = min(4, int(lt / 0.35))
            bars(canvas, d, lt / 0.8, 0, hl)
        else:
            bars(canvas, d, 5, lt / 0.6, 4 if lt < 0.5 else 2)
    elif name == "follow":
        s = ease_out_back(lt / 0.45)
        paste_center(canvas, MOON, W / 2, 720, scale=max(0.01, s) * 1.15)
        if lt > 0.3:
            ps = ease_out_back((lt - 0.3) / 0.35)
            layer = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            text_center(ld, (W / 2, 70), "@malangenommen72", font_ms(70), CREAM, stroke=8)
            ld.rounded_rectangle((W / 2 - 230, 150, W / 2 + 230, 260), radius=55, fill=(254, 44, 85, 255))
            text_center(ld, (W / 2, 205), "+ FOLGEN", font_lg(76), (255, 255, 255), stroke=0)
            paste_center(canvas, glow(layer, 10, 1), W / 2, 1060, scale=max(0.01, ps))
    elif name in ("spot", "spotphones"):
        a = ease_out(lt / 0.4) if name == "spot" else 1
        if name == "spotphones":
            for i, x in enumerate([170, 330, 750, 910]):
                f = min(1, lt / 0.4 - i * 0.2)
                if f > 0:
                    paste_center(canvas, FIG_PHONE, x, 880 + (40 if i in (1, 2) else 0), scale=0.55, alpha=0.75 * f)
        spotlight(canvas, W / 2, 470, 1060, 230, a)
        paste_center(canvas, FIG_PINK, W / 2, 830 + math.sin(gt * 5) * 5, scale=0.95)
        title(canvas, "SPOTLIGHT-EFFEKT", lt if name == "spot" else 5)
    elif name == "manyspots":
        xs = [150, 345, 540, 735, 930]
        for i, x in enumerate(xs):
            f = ease_out((lt - i * 0.22) / 0.35)
            if f > 0:
                spotlight(canvas, x, 470, 1000, 95, f)
        for i, x in enumerate(xs):
            spr = [FIG_CYAN, FIG_LILAC, FIG_SMILE, FIG_LILAC, FIG_CYAN][i]
            paste_center(canvas, spr, x, 860 + math.sin(gt * 4 + i) * 5, scale=0.5)
        title(canvas, "JEDER HAT SEIN LICHT", lt, size=100)
    elif name == "comment":
        s = ease_out_back(lt / 0.4)
        layer = Image.new("RGBA", (900, 560), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((40, 40, 860, 400), radius=70, fill=CREAM + (255,), outline=CYAN + (255,), width=8)
        ld.polygon([(170, 395), (290, 395), (150, 500)], fill=CREAM + (255,))
        text_center(ld, (450, 170), "DEIN PEINLICHSTER", font_lg(76), (120, 30, 160), stroke=0)
        text_center(ld, (450, 270), "MOMENT?", font_lg(100), (254, 44, 85), stroke=0)
        paste_center(canvas, glow(layer, 14, 1), W / 2, 720, scale=max(0.01, s))
        if lt > 0.6:
            bounce = abs(math.sin(gt * 5)) * 30
            y = 1020 + bounce
            d.polygon([(W / 2 - 60, y), (W / 2 + 60, y), (W / 2, y + 70)], fill=YELLOW)
            text_center(d, (W / 2, 990), "Schreib's in die Kommentare", font_ms(46), CREAM, stroke=5)
        title(canvas, "UND DU?", lt)

if EP == '02':
    exec(open('scenes02.py').read())

# ---------- subtitles ----------
KEY = {"bruder", "liebst", "dreimal", "gehirn", "hinweisen.", "hinweisen", "mutter", "dach", "@malangenommen72", "hilfst", "23", "41", "ängste.", "schwester.", "kommentar.", "fest.", "peinliches", "t-shirt", "hälfte", "viertel", "@malangenommen72", "spotlight-effekt", "innen", "eigenen", "spotlight", "moment", "überrascht", "genau"}

def chunks(text):
    words = text.split()
    out, cur = [], []
    for w_ in words:
        cur.append(w_)
        if len(" ".join(cur)) >= 14 or w_.endswith((",", ".", "?")) or len(cur) == 3:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out

SUBS = []
for (s0, s1, line) in segs:
    cs = chunks(line["show"])
    total_chars = sum(len(" ".join(c)) + 4 for c in cs)
    t0 = s0
    for c in cs:
        dur = (s1 - s0) * (len(" ".join(c)) + 4) / total_chars
        SUBS.append((t0, t0 + dur, c))
        t0 += dur

SUBF = font_ms(84, "Black")

def subtitle(canvas, gt):
    for (a, b, words) in SUBS:
        if a <= gt < b + 0.05:
            lt = gt - a
            s = 0.85 + 0.15 * ease_out(lt / 0.12)
            layer = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            parts = [(w_, YELLOW if w_.lower().strip(",.?") in KEY else (255, 255, 255)) for w_ in words]
            sp = d.textlength(" ", font=SUBF)
            total = sum(d.textlength(w_, font=SUBF) for w_, _ in parts) + sp * (len(parts) - 1)
            f = SUBF
            if total > W - 160:
                sc = (W - 160) / total
                f = font_ms(int(84 * sc), "Black")
                sp = d.textlength(" ", font=f)
                total = sum(d.textlength(w_, font=f) for w_, _ in parts) + sp * (len(parts) - 1)
            x = (W - total) / 2
            for w_, col in parts:
                d.text((x, 110), w_, font=f, fill=col, anchor="lm", stroke_width=10, stroke_fill=(0, 0, 0))
                x += d.textlength(w_, font=f) + sp
            paste_center(canvas, layer, W / 2, 1250, scale=s)
            return

STAMP = Image.new("RGBA", (420, 70), (0, 0, 0, 0))
_sd = ImageDraw.Draw(STAMP)
_sd.rounded_rectangle((0, 0, 419, 69), radius=34, fill=(0, 0, 0, 110), outline=(255, 255, 255, 120), width=3)
_sd.text((210, 36), f"MAL ANGENOMMEN #{EP}", font=font_ms(32, "Black"), fill=YELLOW, anchor="mm")

# ---------- render ----------
def seg_at(gt):
    cur = segs[0]
    for sg in segs:
        if gt >= sg[0] - 0.05:
            cur = sg
    return cur

def render(gt):
    canvas = BG.copy().convert("RGBA")
    d = ImageDraw.Draw(canvas)
    for (x, y, r, ph) in STARS:
        a = int(120 + 120 * (0.5 + 0.5 * math.sin(gt * 2 + ph)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))
    s0, s1, line = seg_at(gt)
    scene(canvas, line["scene"], max(0, gt - s0), gt)
    subtitle(canvas, gt)
    canvas.alpha_composite(STAMP, ((W - STAMP.width) // 2, 1380))
    return canvas.convert("RGB")

if __name__ == "__main__":
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    if only:
        for tt in only:
            render(float(tt)).save(f"preview_{tt}.png")
    else:
        for i in range(NFRAMES):
            render(i / FPS).save(f"{OUT}/f{i:05d}.jpg", quality=92)
        json.dump({"segs": [(a, b, l["scene"]) for a, b, l in segs], "total": TOTAL}, open("timeline.json", "w"))
        print("frames", NFRAMES, "total", TOTAL)
