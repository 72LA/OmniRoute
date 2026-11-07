# usage (in episode dir): python3 ../engine/render2.py <theme line|flat> <ep "03"> <scenes.py> [preview times...]
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
THEME, EP, SCENES = sys.argv[1], sys.argv[2], sys.argv[3]
# Kanal je Stil: line (Dark) = malangenommen72, flat (Wissen) = AI72
CHANNEL = os.environ.get("CHANNEL", "MAL ANGENOMMEN" if THEME == "line" else "AI72")
HANDLE = os.environ.get("HANDLE", "@malangenommen72" if THEME == "line" else "@ai72")  # AI72-Handle beim Betreiber bestätigen
PREVIEW = [float(v) for v in sys.argv[4:]]
LINES = json.load(open("script.json"))
SEGS = [(a, b, l) for (a, b), l in zip(json.load(open("segs_abs.json")), LINES)]
TOTAL = SEGS[-1][1] + 1.6
NFRAMES = int(math.ceil(TOTAL * FPS))

MS = "/tmp/fonts/Montserrat.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
_fc = {}
def font(size, weight="Bold"):
    k = (size, weight)
    if k not in _fc:
        if weight == "mono":
            _fc[k] = ImageFont.truetype(MONO, size)
        else:
            f = ImageFont.truetype(MS, size); f.set_variation_by_name(weight); _fc[k] = f
    return _fc[k]

# ---------------- palette ----------------
if THEME == "line":
    FG = (255, 255, 255); BGC = (0, 0, 0); ACC = (255, 255, 255); ACC2 = (255, 255, 255); OUT = (255, 255, 255)
    LW = 6
else:
    FG = (255, 255, 255); BGC = (14, 26, 61); ACC = (255, 212, 0); ACC2 = (255, 79, 139); CY = (62, 224, 255)
    OUT = (10, 15, 36); LW = 7
    CREAM = (255, 236, 214); NAVY2 = (28, 46, 100)

# ---------------- easing / helpers ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_out_back(x):
    x = clamp(x); c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def paste_center(canvas, sprite, cx, cy, scale=1.0):
    s = sprite
    if scale <= 0.01: return
    if abs(scale - 1) > 1e-3:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BILINEAR)
    canvas.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def text_c(d, xy, txt, f, fill, stroke=0, sfill=None):
    d.text(xy, txt, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sfill or OUT)

def poly_len(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def poly_progress(d, pts, p, fill=None, width=None, closed=False):
    """Draw polyline up to fraction p of its length (line-draw reveal)."""
    fill = fill or FG; width = width or LW
    if closed: pts = list(pts) + [pts[0]]
    p = clamp(p)
    if p <= 0: return
    total = poly_len(pts); target = total * p; acc = 0; out = [pts[0]]
    for i in range(len(pts) - 1):
        seg = math.dist(pts[i], pts[i + 1])
        if acc + seg >= target:
            r = (target - acc) / seg if seg else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)); break
        out.append(pts[i + 1]); acc += seg
    if len(out) > 1: d.line(out, fill=fill, width=width, joint="curve")

def rr_pts(x0, y0, x1, y1, r, n=8):
    pts = []
    for cx, cy, a0 in [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def circle_pts(cx, cy, r, n=48, start=-90):
    return [(cx + r * math.cos(math.radians(start + 360 * k / n)), cy + r * math.sin(math.radians(start + 360 * k / n))) for k in range(n + 1)]

def wave_pts(x0, y, w, amp, cycles, phase=0, n=120, env=True):
    pts = []
    for k in range(n + 1):
        u = k / n; e = math.sin(math.pi * u) if env else 1
        pts.append((x0 + w * u, y + amp * e * math.sin(2 * math.pi * cycles * u + phase)))
    return pts

def arrow(d, x0, y0, x1, y1, p=1.0, fill=None, width=None, head=26):
    fill = fill or FG; width = width or LW
    p = clamp(p)
    if p <= 0: return
    xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    d.line((x0, y0, xe, ye), fill=fill, width=width)
    if p > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        for s in (2.6, -2.6):
            d.line((xe, ye, xe + head * math.cos(a + s), ye + head * math.sin(a + s)), fill=fill, width=width)

def note(d, x, y, s, col, outline=None):
    """music note ♪"""
    outline = outline or OUT
    d.ellipse((x - 22 * s, y - 15 * s, x + 22 * s, y + 15 * s), fill=col, outline=outline, width=max(2, int(4 * s)))
    d.line((x + 19 * s, y, x + 19 * s, y - 80 * s), fill=outline, width=max(3, int(9 * s)))
    d.line((x + 19 * s, y, x + 19 * s, y - 80 * s), fill=col, width=max(2, int(5 * s)))
    d.polygon([(x + 19 * s, y - 80 * s), (x + 50 * s, y - 60 * s), (x + 50 * s, y - 45 * s), (x + 19 * s, y - 62 * s)], fill=col, outline=outline)

def heart(d, cx, cy, r, col):
    d.ellipse((cx - r, cy - r, cx, cy), fill=col); d.ellipse((cx, cy - r, cx + r, cy), fill=col)
    d.polygon([(cx - r * 0.98, cy - r * 0.35), (cx + r * 0.98, cy - r * 0.35), (cx, cy + r * 1.05)], fill=col)

# ---------------- figures ----------------
def figure_line(d, cx, cy, s=1.0, face="neutral", p=1.0):
    """outline stick figure, cy = body centre"""
    hr = 62 * s
    hx, hy = cx, cy - 170 * s
    body = rr_pts(cx - 70 * s, cy - 95 * s, cx + 70 * s, cy + 110 * s, 60 * s)
    d.polygon(body, fill=BGC); d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=BGC)
    poly_progress(d, circle_pts(hx, hy, hr), p)
    poly_progress(d, body, clamp(p * 1.2 - 0.1))
    if p > 0.6:
        d.line((cx - 30 * s, cy + 110 * s, cx - 30 * s, cy + 175 * s), fill=FG, width=LW)
        d.line((cx + 30 * s, cy + 110 * s, cx + 30 * s, cy + 175 * s), fill=FG, width=LW)
    if p > 0.8:
        for ex in (-22, 22):
            r = 7 * s if face != "shock" else 10 * s
            d.ellipse((hx + ex * s - r, hy - 10 * s - r, hx + ex * s + r, hy - 10 * s + r), fill=FG)
        if face == "smile": d.arc((hx - 24 * s, hy - 5 * s, hx + 24 * s, hy + 30 * s), 20, 160, fill=FG, width=LW - 1)
        elif face == "shock": d.ellipse((hx - 12 * s, hy + 12 * s, hx + 12 * s, hy + 38 * s), outline=FG, width=LW - 1)
        else: d.line((hx - 18 * s, hy + 20 * s, hx + 18 * s, hy + 20 * s), fill=FG, width=LW - 1)

def figure_flat(d, cx, cy, s=1.0, col=None, face="neutral"):
    col = col or ACC2
    hr = 66 * s; hx, hy = cx, cy - 175 * s
    d.rounded_rectangle((cx - 30 * s - 18 * s, cy + 90 * s, cx - 30 * s + 18 * s, cy + 180 * s), radius=16 * s, fill=col, outline=OUT, width=LW)
    d.rounded_rectangle((cx + 30 * s - 18 * s, cy + 90 * s, cx + 30 * s + 18 * s, cy + 180 * s), radius=16 * s, fill=col, outline=OUT, width=LW)
    d.rounded_rectangle((cx - 78 * s, cy - 100 * s, cx + 78 * s, cy + 120 * s), radius=62 * s, fill=col, outline=OUT, width=LW)
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=CREAM, outline=OUT, width=LW)
    for ex in (-24, 24):
        if face == "closed":
            d.arc((hx + ex * s - 12 * s, hy - 16 * s, hx + ex * s + 12 * s, hy + 4 * s), 200, 340, fill=OUT, width=LW - 2)
        else:
            r = 9 * s; d.ellipse((hx + ex * s - r, hy - 8 * s - r, hx + ex * s + r, hy - 8 * s + r), fill=OUT)
    d.ellipse((hx - 46 * s, hy + 6 * s, hx - 26 * s, hy + 20 * s), fill=(255, 160, 170))
    d.ellipse((hx + 26 * s, hy + 6 * s, hx + 46 * s, hy + 20 * s), fill=(255, 160, 170))
    if face == "smile": d.arc((hx - 22 * s, hy, hx + 22 * s, hy + 34 * s), 20, 160, fill=OUT, width=LW - 2)
    elif face == "annoyed": d.line((hx - 18 * s, hy + 26 * s, hx + 18 * s, hy + 20 * s), fill=OUT, width=LW - 2)
    elif face == "chew":
        pass
    else: d.line((hx - 16 * s, hy + 24 * s, hx + 16 * s, hy + 24 * s), fill=OUT, width=LW - 2)

# ---------------- background ----------------
random.seed(11)
if THEME == "line":
    _bg = Image.new("RGB", (W, H), BGC); _d = ImageDraw.Draw(_bg)
    for x in range(0, W, 60): _d.line((x, 0, x, H), fill=(22, 22, 22), width=1)
    for y in range(0, H, 60): _d.line((0, y, W, y), fill=(22, 22, 22), width=1)
    for (x, y, sx, sy) in [(40, 260, 1, 1), (W - 40, 260, -1, 1), (40, 1470, 1, -1), (W - 40, 1470, -1, -1)]:
        _d.line((x, y, x + 50 * sx, y), fill=(120, 120, 120), width=3); _d.line((x, y, x, y + 50 * sy), fill=(120, 120, 120), width=3)
    BG = _bg.convert("RGBA")
    DECOR = []
else:
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([12, 22, 54]); bot = np.array([22, 38, 92])
    arr = np.repeat((top + (bot - top) * y)[:, None, :], W, axis=1)
    BG = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
    _d = ImageDraw.Draw(BG)
    for _ in range(70):
        x, yy, r = random.randint(0, W), random.randint(0, H), random.choice([2, 2, 3, 4])
        _d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 170))
    DECOR = [(random.choice(["tri", "circ", "squig", "plus"]), random.choice([ACC, ACC2, CY]),
              random.choice([60, 980, 120, 940, 80, 1000]), random.randint(200, 1500), random.uniform(0, 6.28), random.uniform(0.6, 1.1)) for _ in range(9)]

def draw_decor(canvas, gt):
    if not DECOR: return
    d = ImageDraw.Draw(canvas)
    for kind, col, x, y, ph, s in DECOR:
        yy = y + math.sin(gt * 0.8 + ph) * 14; rot = gt * 20 + ph * 50
        if kind == "circ": d.ellipse((x - 16 * s, yy - 16 * s, x + 16 * s, yy + 16 * s), fill=col, outline=OUT, width=4)
        elif kind == "tri":
            pts = [(x + 24 * s * math.cos(math.radians(rot + a)), yy + 24 * s * math.sin(math.radians(rot + a))) for a in (0, 120, 240)]
            d.polygon(pts, fill=col, outline=OUT, width=4)
        elif kind == "plus":
            d.line((x - 18 * s, yy, x + 18 * s, yy), fill=col, width=9); d.line((x, yy - 18 * s, x, yy + 18 * s), fill=col, width=9)
        else:
            pts = [(x - 40 * s + k * 8 * s, yy + 10 * s * math.sin(k * 1.2 + gt * 2)) for k in range(11)]
            d.line(pts, fill=col, width=8, joint="curve")

# ---------------- title / subtitle / stamp ----------------
def title(canvas, txt, lt, size=None):
    d = ImageDraw.Draw(canvas)
    if THEME == "line":
        size = size or 78; f = font(size, "Bold")
        while d.textlength(txt, font=f) > W - 160: size -= 4; f = font(size, "Bold")
        tw = d.textlength(txt, font=f)
        a = clamp(lt / 0.25)
        col = tuple(int(c * a) for c in FG)
        d.text((W / 2, 370), txt, font=f, fill=col, anchor="mm")
        poly_progress(d, [(W / 2 - tw / 2, 430), (W / 2 + tw / 2, 430)], ease_out(lt / 0.5), width=3)
        d.text((W / 2 - tw / 2, 312), f"FIG. {EP}", font=font(24, "mono"), fill=(150, 150, 150), anchor="lm")
    else:
        size = size or 92; f = font(size, "Black")
        while d.textlength(txt, font=f) > W - 150: size -= 4; f = font(size, "Black")
        layer = Image.new("RGBA", (W, 240), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        tw = ld.textlength(txt, font=f)
        ld.rounded_rectangle((W / 2 - tw / 2 - 10, 150, W / 2 + tw / 2 + 10, 172), radius=11, fill=ACC)
        ld.text((W / 2, 110), txt, font=f, fill=FG, anchor="mm", stroke_width=8, stroke_fill=OUT)
        paste_center(canvas, layer, W / 2, 360, scale=0.75 + 0.25 * ease_out_back(lt / 0.35))

def _chunks(text):
    words = text.split(); out, cur = [], []
    for w_ in words:
        cur.append(w_)
        if len(" ".join(cur)) >= 14 or w_.endswith((",", ".", "?", "!", ":")) or len(cur) == 3:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

SUBS = []
for (s0, s1, line) in SEGS:
    cs = _chunks(line["show"]); tot = sum(len(" ".join(c)) + 4 for c in cs); t0 = s0
    for c in cs:
        dur = (s1 - s0) * (len(" ".join(c)) + 4) / tot; SUBS.append((t0, t0 + dur, c)); t0 += dur
KEYS = set()

def subtitle(canvas, gt):
    for (a, b, words) in SUBS:
        if a <= gt < b + 0.05:
            lt = gt - a
            layer = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            size = 80; f = font(size, "Black" if THEME == "flat" else "ExtraBold")
            sp = d.textlength(" ", font=f)
            tot = sum(d.textlength(w_, font=f) for w_ in words) + sp * (len(words) - 1)
            if tot > W - 160:
                size = int(size * (W - 160) / tot); f = font(size, "Black" if THEME == "flat" else "ExtraBold")
                sp = d.textlength(" ", font=f); tot = sum(d.textlength(w_, font=f) for w_ in words) + sp * (len(words) - 1)
            x = (W - tot) / 2
            for w_ in words:
                key = w_.lower().strip(",.?!:„“\"") in KEYS
                tw = d.textlength(w_, font=f)
                if THEME == "line":
                    if key:
                        d.rectangle((x - 10, 100 - size * 0.62, x + tw + 10, 100 + size * 0.62), fill=FG)
                        d.text((x, 100), w_, font=f, fill=BGC, anchor="lm")
                    else:
                        d.text((x, 100), w_, font=f, fill=FG, anchor="lm", stroke_width=6, stroke_fill=BGC)
                else:
                    d.text((x, 100), w_, font=f, fill=ACC if key else FG, anchor="lm", stroke_width=9, stroke_fill=OUT)
                x += tw + sp
            paste_center(canvas, layer, W / 2, 1250, scale=0.88 + 0.12 * ease_out(lt / 0.12))
            return

STAMP = Image.new("RGBA", (440, 64), (0, 0, 0, 0)); _sd = ImageDraw.Draw(STAMP)
if THEME == "line":
    _sd.rectangle((1, 1, 438, 62), outline=(200, 200, 200), width=2)
    _sd.text((220, 33), f"{CHANNEL} #{EP}", font=font(28, "mono"), fill=(220, 220, 220), anchor="mm")
else:
    _sd.rounded_rectangle((0, 0, 439, 63), radius=31, fill=ACC, outline=OUT, width=4)
    _sd.text((220, 33), f"{CHANNEL} #{EP}", font=font(30, "Black"), fill=OUT, anchor="mm")

# ---------------- scenes ----------------
exec(open(SCENES).read())   # defines SCENE(canvas, name, lt, gt, dur) and KEYS

def seg_at(gt):
    cur = SEGS[0]
    for sg in SEGS:
        if gt >= sg[0] - 0.05: cur = sg
    return cur

def render(gt):
    canvas = BG.copy()
    draw_decor(canvas, gt)
    s0, s1, line = seg_at(gt)
    SCENE(canvas, line["scene"], max(0.0, gt - s0), gt, s1 - s0)
    subtitle(canvas, gt)
    canvas.alpha_composite(STAMP, ((W - STAMP.width) // 2, 1380))
    return canvas.convert("RGB")

if PREVIEW:
    for tt in PREVIEW: render(tt).save(f"pv_{tt}.png")
else:
    os.makedirs("frames", exist_ok=True)
    for i in range(NFRAMES): render(i / FPS).save(f"frames/f{i:05d}.jpg", quality=92)
    json.dump({"segs": [(a, b, l["scene"]) for a, b, l in SEGS], "total": TOTAL}, open("timeline.json", "w"))
    print("frames", NFRAMES, "total", round(TOTAL, 2))
