"""AI72 style lab v2: Idee 2 'Mikro-Welt' + standing character + new lineless mitten hand."""
import math, os, random, subprocess
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap');"

def page(svg, title, caption, key):
    cap = caption.replace(key, f'<b style="color:#ffb347">{key}</b>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT}
    html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:Montserrat,sans-serif}}
    svg{{position:absolute;left:0;top:0}}
    .stamp{{position:absolute;top:190px;left:0;right:0;text-align:center}}
    .stamp span{{background:#ffb347;color:#062a3a;font-weight:900;font-size:30px;padding:8px 24px;border-radius:30px}}
    .title{{position:absolute;top:262px;left:0;right:0;text-align:center;color:#fff;font-weight:900;font-size:88px;text-shadow:0 6px 30px rgba(0,0,0,.35)}}
    .cap{{position:absolute;top:1170px;left:0;right:0;text-align:center;color:#fff;font-weight:900;font-size:76px;padding:0 80px;text-shadow:0 4px 0 rgba(0,0,0,.25),0 8px 28px rgba(0,0,0,.45)}}
    </style></head><body><svg width="1080" height="1920" viewBox="0 0 1080 1920">{svg}</svg>
    <div class="stamp"><span>AI72 #07</span></div><div class="title">{title}</div><div class="cap">{cap}</div></body></html>"""

def stars(seed, n=60):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.randint(0,1080)}" cy="{r.randint(0,1400)}" r="{r.choice([1.5,2,2.8])}" fill="#bff8ff" opacity="{r.uniform(.25,.8):.2f}"/>' for _ in range(n))

DEFS = """<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="haze" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#062a3a"/><stop offset=".6" stop-color="#0b4b5e"/><stop offset="1" stop-color="#0f6b72"/></linearGradient>
<radialGradient id="light" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".35"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
<radialGradient id="cellA" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#ffd1a6"/><stop offset=".55" stop-color="#ff8a5c"/><stop offset="1" stop-color="#d4495e"/></radialGradient>
<radialGradient id="cellB" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#b9fff4"/><stop offset=".6" stop-color="#3fd6c5"/><stop offset="1" stop-color="#14857f"/></radialGradient>
<!-- character materials: light from top-left -->
<radialGradient id="skinH" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe9d8"/><stop offset=".6" stop-color="#ffc2a0"/><stop offset="1" stop-color="#e88f78"/></radialGradient>
<linearGradient id="skinL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe2cc"/><stop offset=".55" stop-color="#ffb994"/><stop offset="1" stop-color="#df8370"/></linearGradient>
<linearGradient id="skinD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6ad8d"/><stop offset="1" stop-color="#cf7262"/></linearGradient>
<linearGradient id="hood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb07a"/><stop offset=".5" stop-color="#ff7a55"/><stop offset="1" stop-color="#c9445a"/></linearGradient>
<linearGradient id="hoodD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ef6b52"/><stop offset="1" stop-color="#b23a55"/></linearGradient>
<linearGradient id="pants" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f8f9a"/><stop offset="1" stop-color="#16525e"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a3a6e"/><stop offset="1" stop-color="#2a1a3e"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d6a78"/><stop offset="1" stop-color="#0f4652"/></linearGradient>
<linearGradient id="derm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd7bf"/><stop offset="1" stop-color="#f29c86"/></linearGradient>
<linearGradient id="vein" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8fa3"/><stop offset="1" stop-color="#d8435f"/></linearGradient>
<radialGradient id="lens" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#1e7f8c"/><stop offset="1" stop-color="#0d4552"/></radialGradient>
<clipPath id="lensclip"><circle cx="790" cy="760" r="210"/></clipPath>
</defs>"""

BG = f"""<rect width="1080" height="1920" fill="url(#sea)"/><rect width="1080" height="900" fill="url(#light)"/>
<g opacity=".35" filter="url(#soft)"><circle cx="110" cy="430" r="90" fill="url(#cellB)"/><circle cx="1000" cy="1080" r="110" fill="url(#cellA)"/></g>
<g opacity=".18" filter="url(#haze)"><circle cx="540" cy="1650" r="420" fill="#3fd6c5"/></g>{stars(7)}
<path d="M0 1110 C 200 1050, 360 1170, 560 1110 S 900 1050, 1080 1110 V1920 H0 Z" fill="#0a4152" opacity=".95"/>
<path d="M0 1460 C 200 1380, 360 1520, 560 1450 S 900 1380, 1080 1450 V1920 H0 Z" fill="#083646"/>
<path d="M0 1560 C 240 1500, 420 1620, 640 1560 S 940 1500, 1080 1560 V1920 H0 Z" fill="#05242f"/>"""

# ---------- lineless mitten hand ----------
def finger(bx, by, length, w_base, w_tip, ang, fill, wr=0, tipshade=True):
    """tapered capsule from base (bx,by) pointing up, rotated by ang degrees."""
    hb, ht = w_base / 2, w_tip / 2
    L = length
    d = (f"M{-hb} 0 C {-hb} {-L*0.55}, {-ht} {-L*0.8}, {-ht} {-L+ht} "
         f"A {ht} {ht} 0 0 1 {ht} {-L+ht} C {ht} {-L*0.8}, {hb} {-L*0.55}, {hb} 0 Z")
    g = f'<g transform="translate({bx} {by}) rotate({ang})"><path d="{d}" fill="{fill}"/>'
    g += f'<path d="M{-ht*0.55} {-L*0.25} C {-ht*0.6} {-L*0.6}, {-ht*0.5} {-L*0.8}, {-ht*0.2} {-L+ht*0.9}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{w_tip*0.16}" stroke-linecap="round"/>'
    for k in range(wr):  # soft prune lines near the tip, colour-only (no outlines)
        y = -L + ht * 1.4 + k * w_tip * 0.32
        g += f'<path d="M{-ht*0.62} {y} q{ht*0.31} {-w_tip*0.12} {ht*0.62} 0 t{ht*0.62} 0" fill="none" stroke="#c96a5a" stroke-opacity=".5" stroke-width="{w_tip*0.08}" stroke-linecap="round"/>'
    return g + "</g>"

def mitten_hand(cx, cy, s=1.0, rot=0, wr=0):
    """palm: flat wide top, narrow curved bottom; 4 fanned fingers, middle longest; thumb on the side."""
    fs = [(-0.42, 1.55, -11, "url(#skinD)"), (-0.14, 1.85, -3, "url(#skinL)"), (0.14, 1.78, 4, "url(#skinL)"), (0.4, 1.4, 12, "url(#skinD)")]
    g = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
    g += '<ellipse cx="10" cy="60" rx="150" ry="170" fill="#000" opacity=".18" filter="url(#soft)"/>'
    for x, l, a, f in fs:  # back fingers first (darker), then front
        g += finger(x * 230, -70, l * 100, 64, 50, a, f, wr)
    g += ('<path d="M-125 -95 C -60 -120, 60 -120, 125 -95 C 140 -10, 120 90, 60 140 C 20 170, -30 170, -70 140 '
          'C -120 100, -140 -10, -125 -95 Z" fill="url(#skinL)"/>')
    g += '<path d="M-105 -80 C -60 -100, 0 -102, 40 -95" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="10" stroke-linecap="round"/>'
    g += finger(-110, 40, 135, 72, 54, -52, "url(#skinD)", 0)  # thumb
    g += '<path d="M-50 150 C -20 175, 30 175, 60 150 L 70 230 C 30 250, -30 250, -60 230 Z" fill="url(#skinD)"/>'  # wrist
    return g + "</g>"

# ---------- standing character ----------
def person(cx, ground, s=1.0, arm="wave", face="smile"):
    """feet on `ground`; head ~ 1/3 of height (friendly explainer proportions)."""
    g = f'<g transform="translate({cx} {ground}) scale({s})">'
    g += '<ellipse cx="0" cy="6" rx="130" ry="22" fill="#000" opacity=".28" filter="url(#soft)"/>'
    # legs + shoes
    for x in (-42, 42):
        g += f'<rect x="{x-30}" y="-190" width="60" height="170" rx="28" fill="url(#pants)"/>'
        g += f'<path d="M{x-38} -24 C {x-38} -48, {x+44} -48, {x+50} -20 C {x+52} -4, {x-38} -2, {x-38} -24 Z" fill="#f4f0e8"/>'
    # back arm (behind body)
    g += '<path d="M-95 -430 C -150 -380, -160 -300, -150 -240" fill="none" stroke="url(#hoodD)" stroke-width="58" stroke-linecap="round"/>'
    g += '<circle cx="-150" cy="-228" r="34" fill="url(#skinD)"/>'
    # torso (hoodie)
    g += ('<path d="M-115 -440 C -120 -470, -60 -490, 0 -490 C 60 -490, 120 -470, 115 -440 L 125 -210 '
          'C 125 -180, -125 -180, -125 -210 Z" fill="url(#hood)"/>')
    g += '<path d="M-70 -300 H 70 V -250 C 70 -235, -70 -235, -70 -250 Z" fill="#000" opacity=".1"/>'  # pocket
    g += '<path d="M-100 -450 C -80 -470, -40 -482, 0 -484" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="12" stroke-linecap="round"/>'
    # front arm
    if arm == "wave":   # raised, hand up next to head
        g += '<path d="M95 -440 C 160 -470, 190 -540, 190 -620" fill="none" stroke="url(#hood)" stroke-width="60" stroke-linecap="round"/>'
        g += mitten_hand(192, -690, 0.42, 8, 3)
    elif arm == "point":
        g += '<path d="M95 -430 C 170 -430, 230 -460, 290 -500" fill="none" stroke="url(#hood)" stroke-width="58" stroke-linecap="round"/>'
        g += finger(300, -500, 70, 40, 30, 62, "url(#skinL)")
        g += '<circle cx="300" cy="-505" r="36" fill="url(#skinL)"/>'
    # neck + head
    g += '<rect x="-30" y="-520" width="60" height="50" rx="20" fill="url(#skinD)"/>'
    g += '<circle cx="0" cy="-640" r="150" fill="url(#skinH)"/>'
    g += ('<path d="M-156 -640 C -170 -760, -90 -812, 0 -812 C 95 -812, 170 -760, 156 -640 '
          'C 150 -690, 120 -715, 80 -722 C 60 -690, 10 -680, -30 -700 C -60 -712, -80 -735, -95 -720 C -125 -705, -145 -680, -156 -640 Z" fill="url(#hair)"/>')
    g += '<path d="M-150 -650 C -158 -610, -150 -580, -138 -560 C -140 -600, -138 -630, -128 -660 Z" fill="url(#hair)"/>'
    g += '<ellipse cx="-60" cy="-760" rx="40" ry="16" fill="#fff" opacity=".22" transform="rotate(-18 -60 -760)"/>'
    # face (mascot style: big eyes with highlight, blush, small smile)
    for ex in (-52, 52):
        g += f'<ellipse cx="{ex}" cy="-620" rx="20" ry="25" fill="#2a1030"/><circle cx="{ex+7}" cy="-630" r="7" fill="#fff"/>'
        g += f'<ellipse cx="{ex*1.55}" cy="-575" rx="24" ry="12" fill="#ff8a8a" opacity=".45"/>'
    if face == "smile": g += '<path d="M-30 -568 q30 30 60 0" fill="none" stroke="#2a1030" stroke-width="9" stroke-linecap="round"/>'
    else: g += '<ellipse cx="0" cy="-560" rx="16" ry="20" fill="#2a1030"/>'
    return g + "</g>"

def drops(pts):
    s = ""
    for x, y, r in pts:
        s += f'<path d="M{x} {y-r*1.4} C {x-r} {y-r*0.2}, {x-r} {y+r}, {x} {y+r} C {x+r} {y+r}, {x+r} {y-r*0.2}, {x} {y-r*1.4} Z" fill="#7fe7ff" opacity=".9"/>'
        s += f'<ellipse cx="{x-r*0.3}" cy="{y+r*0.1}" rx="{r*0.2}" ry="{r*0.35}" fill="#fff" opacity=".8"/>'
    return s

# ---------- Frame A: hook – person waving wrinkled hand + magnifier lens on fingertips ----------
lens = ('<circle cx="790" cy="760" r="222" fill="#000" opacity=".25" filter="url(#soft)" transform="translate(0 16)"/>'
        '<circle cx="790" cy="760" r="210" fill="url(#lens)"/>'
        f'<g clip-path="url(#lensclip)">{mitten_hand(780, 1010, 1.25, 0, 4)}</g>'
        '<circle cx="790" cy="760" r="210" fill="none" stroke="#bff8ff" stroke-opacity=".55" stroke-width="10"/>'
        '<path d="M650 640 A 180 180 0 0 1 760 575" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="12" stroke-linecap="round"/>'
        '<path d="M470 860 L 600 820" stroke="#bff8ff" stroke-opacity=".5" stroke-width="6" stroke-dasharray="14 12"/>')
fa = DEFS + BG + drops([(150, 640, 20), (230, 560, 14), (980, 1050, 18), (560, 520, 12)]) + person(320, 1125, 0.86, "wave") + lens
A = page(fa, "SCHRUMPELFINGER?", "Warum passiert das im Wasser?", "Wasser")

# ---------- Frame B: explain – person pointing at a lineless cross-section card ----------
card = ('<rect x="470" y="560" width="560" height="560" rx="56" fill="#000" opacity=".28" filter="url(#soft)" transform="translate(0 20)"/>'
        '<rect x="470" y="560" width="560" height="560" rx="56" fill="url(#card)"/>'
        '<clipPath id="cc"><rect x="500" y="640" width="500" height="420" rx="34"/></clipPath><g clip-path="url(#cc)">'
        '<rect x="500" y="640" width="500" height="420" fill="url(#derm)"/>'
        '<path d="M500 700 Q 530 670 560 700 T 620 700 T 680 700 T 740 700 T 800 700 T 860 700 T 920 700 T 980 700 T 1040 700 V 640 H500 Z" fill="#1d6a78"/>'
        '<path d="M500 712 Q 530 682 560 712 T 620 712 T 680 712 T 740 712 T 800 712 T 860 712 T 920 712 T 980 712" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="8"/>'
        '<rect x="520" y="860" width="460" height="56" rx="28" fill="url(#vein)"/><rect x="520" y="860" width="460" height="14" rx="7" fill="#fff" opacity=".35"/>'
        '<path d="M520 1000 C 640 960, 800 1030, 980 970" fill="none" stroke="#ffe36b" stroke-width="40" stroke-linecap="round" opacity=".3" filter="url(#soft)"/>'
        '<path d="M520 1000 C 640 960, 800 1030, 980 970" fill="none" stroke="#ffe36b" stroke-width="12" stroke-linecap="round"/>'
        '</g>'
        '<g font-family="Montserrat" font-weight="800" font-size="30" fill="#e8fbff"><text x="510" y="610">QUERSCHNITT HAUT</text>'
        '<text x="530" y="850" fill="#fff">BLUTGEFÄSS ↓ ENGER</text><text x="530" y="1045" fill="#ffe36b">NERV</text></g>')
fb = DEFS + BG + card + person(215, 1125, 0.78, "point")
B = page(fb, "NERVEN STEUERN ES", "Die Gefäße werden enger", "enger")

for name, html in [("v2_a", A), ("v2_b", B)]:
    open(f"{OUT}/{name}.html", "w").write(html)
subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}});
for (const n of ['v2_a','v2_b']) { await p.goto('file://' + process.cwd() + '/' + n + '.html'); await p.waitForTimeout(1200); await p.screenshot({path: n + '.png'}); }
await b.close(); })();"""], check=True, cwd=OUT)
from PIL import Image
a, b = Image.open(f"{OUT}/v2_a.png"), Image.open(f"{OUT}/v2_b.png")
sheet = Image.new("RGB", (2200, 1920), (30, 30, 30)); sheet.paste(a, (0, 0)); sheet.paste(b, (1120, 0))
sheet.resize((1100, 960)).save(f"{OUT}/AI72_Stil_Idee2_v2.png"); print("ok")
