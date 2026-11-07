"""AI72 style lab: two Kurzgesagt-inspired directions (own designs, no copied characters), 2 frames each."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap');"

def page(bg_svg, body_svg, title, caption, key, stamp_bg, stamp_fg, title_col="#fff"):
    cap = caption.replace(key, f'<b style="color:{stamp_bg}">{key}</b>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT}
    html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:Montserrat,sans-serif}}
    svg{{position:absolute;left:0;top:0}}
    .stamp{{position:absolute;top:190px;left:0;right:0;text-align:center}}
    .stamp span{{background:{stamp_bg};color:{stamp_fg};font-weight:900;font-size:30px;padding:8px 24px;border-radius:30px}}
    .title{{position:absolute;top:262px;left:0;right:0;text-align:center;color:{title_col};font-weight:900;font-size:88px;letter-spacing:-.01em;text-shadow:0 6px 30px rgba(0,0,0,.35)}}
    .cap{{position:absolute;top:1160px;left:0;right:0;text-align:center;color:#fff;font-weight:900;font-size:76px;padding:0 80px;text-shadow:0 4px 0 rgba(0,0,0,.25),0 8px 28px rgba(0,0,0,.45)}}
    </style></head><body>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920">{bg_svg}{body_svg}</svg>
    <div class="stamp"><span>AI72 #07</span></div><div class="title">{title}</div><div class="cap">{cap}</div>
    </body></html>"""

# ---------- shared defs ----------
def stars(seed, n=90, col="#fff"):
    import random
    r = random.Random(seed); s = ""
    for _ in range(n):
        x, y, rad, o = r.randint(0, 1080), r.randint(0, 1920), r.choice([1.2, 1.8, 2.5, 3.2]), r.uniform(.3, .9)
        s += f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{col}" opacity="{o:.2f}"/>'
    return s

GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>' \
       '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>' \
       '<filter id="haze" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'

# ================= IDEA 1: "KOSMOS-GLOW" =================
# deep navy->violet space, glowing subjects, rim light from top-left, no outlines.
I1_BG = f"""<defs>{GLOW}
  <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b2a"/><stop offset=".55" stop-color="#1a1452"/><stop offset="1" stop-color="#3a1a6b"/></linearGradient>
  <radialGradient id="neb1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff5c8a" stop-opacity=".55"/><stop offset="1" stop-color="#ff5c8a" stop-opacity="0"/></radialGradient>
  <radialGradient id="neb2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#4fd8ff" stop-opacity=".45"/><stop offset="1" stop-color="#4fd8ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="skin1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe3cf"/><stop offset=".55" stop-color="#f6b394"/><stop offset="1" stop-color="#c9746a"/></linearGradient>
  <linearGradient id="rim1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".25" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="drop1" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#e9fbff"/><stop offset=".4" stop-color="#6fe2ff"/><stop offset="1" stop-color="#1f7fd6"/></radialGradient>
  <linearGradient id="planet1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd86b"/><stop offset="1" stop-color="#ff8a3d"/></linearGradient>
</defs>
<rect width="1080" height="1920" fill="url(#sky1)"/>
<circle cx="200" cy="1500" r="420" fill="url(#neb1)" filter="url(#haze)"/>
<circle cx="920" cy="520" r="380" fill="url(#neb2)" filter="url(#haze)"/>
{stars(1)}
<circle cx="900" cy="1560" r="150" fill="url(#planet1)"/><path d="M780 1520 a150 150 0 0 0 250 120 a170 170 0 0 1 -250 -120z" fill="#000" opacity=".22"/>
<ellipse cx="900" cy="1560" rx="230" ry="38" fill="none" stroke="#ffd86b" stroke-opacity=".5" stroke-width="10" transform="rotate(-18 900 1560)"/>
"""

def hand_glow(cx, cy, s, wr=True):
    fx = [-0.9, -0.3, 0.3, 0.9]; lens = [1.6, 2.0, 1.9, 1.5]; out = ""
    out += f'<ellipse cx="{cx}" cy="{cy+20}" rx="{360*s}" ry="{420*s}" fill="#ffb28f" opacity=".35" filter="url(#glow)"/>'
    for x, l in zip(fx, lens):
        X = cx + (x*100 - 44)*s; Y = cy - l*175*s
        out += f'<rect x="{X}" y="{Y}" width="{88*s}" height="{l*200*s}" rx="{44*s}" fill="url(#skin1)"/>'
        out += f'<rect x="{X}" y="{Y}" width="{88*s}" height="{l*200*s}" rx="{44*s}" fill="url(#rim1)"/>'
        if wr:
            for k in range(4):
                yy = Y + (26 + k*22)*s
                out += f'<path d="M{X+16*s} {yy} q{14*s} -9 {28*s} 0 t{28*s} 0" fill="none" stroke="#b5604f" stroke-opacity=".55" stroke-width="{5*s}" stroke-linecap="round"/>'
    out += f'<rect x="{cx-170*s}" y="{cy-40*s}" width="{340*s}" height="{320*s}" rx="{110*s}" fill="url(#skin1)"/>'
    out += f'<rect x="{cx-170*s}" y="{cy-40*s}" width="{340*s}" height="{320*s}" rx="{110*s}" fill="url(#rim1)"/>'
    out += f'<rect x="{cx+120*s}" y="{cy}" width="{86*s}" height="{190*s}" rx="{43*s}" fill="url(#skin1)" transform="rotate(-28 {cx+163*s} {cy+95*s})"/>'
    return out

def drops(cx_list, ys, fid):
    s = ""
    for x, y in zip(cx_list, ys):
        s += f'<circle cx="{x}" cy="{y+10}" r="34" fill="#6fe2ff" opacity=".5" filter="url(#{fid})"/>'
        s += f'<path d="M{x} {y-46} C {x-30} {y-6}, {x-34} {y+30}, {x} {y+34} C {x+34} {y+30}, {x+30} {y-6}, {x} {y-46} Z" fill="url(#drop1)"/>'
        s += f'<ellipse cx="{x-10}" cy="{y+4}" rx="7" ry="12" fill="#fff" opacity=".8"/>'
    return s

i1a = page(I1_BG, hand_glow(540, 760, 0.95) + drops([210, 380, 720, 880, 300], [560, 470, 500, 640, 1040], "soft"),
           "SCHRUMPELFINGER?", "Warum passiert das im Wasser?", "Wasser", "#ffcf3f", "#1a1452")

i1b_body = """
<defs><clipPath id="cut"><rect x="120" y="560" width="840" height="520" rx="60"/></clipPath>
<linearGradient id="derm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc9ad"/><stop offset="1" stop-color="#e07f74"/></linearGradient>
<linearGradient id="vein" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff86a8"/><stop offset="1" stop-color="#c22d5d"/></linearGradient></defs>
<rect x="120" y="560" width="840" height="520" rx="60" fill="#000" opacity=".25" transform="translate(0 24)" filter="url(#soft)"/>
<g clip-path="url(#cut)">
 <rect x="120" y="560" width="840" height="520" fill="url(#derm)"/>
 <path d="M120 620 Q 175 580 230 620 T 340 620 T 450 620 T 560 620 T 670 620 T 780 620 T 890 620 T 1000 620 V 560 H120 Z" fill="#1a1452"/>
 <path d="M120 640 Q 175 600 230 640 T 340 640 T 450 640 T 560 640 T 670 640 T 780 640 T 890 640 T 1000 640" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="10"/>
 <rect x="160" y="880" width="760" height="70" rx="35" fill="url(#vein)"/>
 <rect x="160" y="880" width="760" height="18" rx="9" fill="#fff" opacity=".35"/>
 <path d="M200 1040 C 400 980, 600 1060, 900 990" fill="none" stroke="#ffe36b" stroke-width="14" stroke-linecap="round"/>
 <path d="M200 1040 C 400 980, 600 1060, 900 990" fill="none" stroke="#ffe36b" stroke-width="40" stroke-linecap="round" opacity=".35" filter="url(#soft)"/>
</g>
<circle cx="900" cy="990" r="40" fill="#ffe36b" opacity=".6" filter="url(#glow)"/>
<g font-family="Montserrat" font-weight="800" font-size="34" fill="#fff"><text x="180" y="720" opacity=".9">HAUT</text><text x="180" y="860">BLUTGEFÄSS</text><text x="620" y="1070" fill="#ffe36b">NERV</text></g>
"""
i1b = page(I1_BG, i1b_body, "NERVEN STEUERN ES", "Die Gefäße werden enger", "enger", "#ffcf3f", "#1a1452")

# ================= IDEA 2: "MIKRO-DIORAMA" =================
# teal-to-deep-ocean inner-body world, layered parallax blobs, warm coral/yellow, soft depth blur, cute cell mascot.
I2_BG = f"""<defs>{GLOW}
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#062a3a"/><stop offset=".6" stop-color="#0b4b5e"/><stop offset="1" stop-color="#0f6b72"/></linearGradient>
  <radialGradient id="cell" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#ffd1a6"/><stop offset=".55" stop-color="#ff8a5c"/><stop offset="1" stop-color="#d4495e"/></radialGradient>
  <radialGradient id="cellb" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#b9fff4"/><stop offset=".6" stop-color="#3fd6c5"/><stop offset="1" stop-color="#14857f"/></radialGradient>
  <radialGradient id="light" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".35"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
  <linearGradient id="skin2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe6d2"/><stop offset=".6" stop-color="#ffb08a"/><stop offset="1" stop-color="#e07a6a"/></linearGradient>
  <linearGradient id="rim2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6dc" stop-opacity=".95"/><stop offset=".22" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1080" height="1920" fill="url(#sea)"/>
<rect width="1080" height="900" fill="url(#light)"/>
<g opacity=".35" filter="url(#soft)"><circle cx="120" cy="420" r="90" fill="url(#cellb)"/><circle cx="980" cy="760" r="120" fill="url(#cell)"/><circle cx="160" cy="1500" r="140" fill="url(#cellb)"/></g>
<g opacity=".18" filter="url(#haze)"><circle cx="540" cy="1650" r="420" fill="#3fd6c5"/></g>
{stars(7, 60, "#bff8ff")}
<path d="M0 1460 C 200 1380, 360 1520, 560 1450 S 900 1380, 1080 1450 V1920 H0 Z" fill="#083646" opacity=".9"/>
<path d="M0 1560 C 240 1500, 420 1620, 640 1560 S 940 1500, 1080 1560 V1920 H0 Z" fill="#05242f"/>
"""

def mascot(cx, cy, r, grad="cell"):
    return (f'<ellipse cx="{cx}" cy="{cy+r*0.95}" rx="{r*0.8}" ry="{r*0.16}" fill="#000" opacity=".25" filter="url(#soft)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{grad})"/>'
            f'<ellipse cx="{cx-r*0.35}" cy="{cy-r*0.45}" rx="{r*0.28}" ry="{r*0.16}" fill="#fff" opacity=".55" transform="rotate(-25 {cx-r*0.35} {cy-r*0.45})"/>'
            f'<circle cx="{cx-r*0.3}" cy="{cy-r*0.02}" r="{r*0.11}" fill="#2a1030"/><circle cx="{cx+r*0.3}" cy="{cy-r*0.02}" r="{r*0.11}" fill="#2a1030"/>'
            f'<circle cx="{cx-r*0.27}" cy="{cy-r*0.06}" r="{r*0.035}" fill="#fff"/><circle cx="{cx+r*0.33}" cy="{cy-r*0.06}" r="{r*0.035}" fill="#fff"/>'
            f'<path d="M{cx-r*0.16} {cy+r*0.22} q{r*0.16} {r*0.16} {r*0.32} 0" fill="none" stroke="#2a1030" stroke-width="{r*0.06}" stroke-linecap="round"/>')

def hand2(cx, cy, s):
    fx = [-0.9, -0.3, 0.3, 0.9]; lens = [1.6, 2.0, 1.9, 1.5]; out = ""
    for x, l in zip(fx, lens):
        X = cx + (x*100 - 44)*s; Y = cy - l*175*s
        out += f'<rect x="{X}" y="{Y}" width="{88*s}" height="{l*200*s}" rx="{44*s}" fill="url(#skin2)"/><rect x="{X}" y="{Y}" width="{88*s}" height="{l*200*s}" rx="{44*s}" fill="url(#rim2)"/>'
        for k in range(4):
            yy = Y + (26 + k*22)*s
            out += f'<path d="M{X+16*s} {yy} q{14*s} -9 {28*s} 0 t{28*s} 0" fill="none" stroke="#c0604f" stroke-opacity=".5" stroke-width="{5*s}" stroke-linecap="round"/>'
    out += f'<rect x="{cx-170*s}" y="{cy-40*s}" width="{340*s}" height="{340*s}" rx="{110*s}" fill="url(#skin2)"/><rect x="{cx-170*s}" y="{cy-40*s}" width="{340*s}" height="{340*s}" rx="{110*s}" fill="url(#rim2)"/>'
    out += f'<rect x="{cx+120*s}" y="{cy}" width="{86*s}" height="{190*s}" rx="{43*s}" fill="url(#skin2)" transform="rotate(-28 {cx+163*s} {cy+95*s})"/>'
    return out

bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#bff8ff" stroke-opacity=".7" stroke-width="4"/><circle cx="{x-r*0.35}" cy="{y-r*0.35}" r="{r*0.2}" fill="#fff" opacity=".7"/>'
                  for x, y, r in [(230, 600, 26), (290, 520, 14), (850, 560, 30), (900, 470, 16), (800, 980, 20)])
i2a = page(I2_BG, hand2(560, 790, 0.92) + bubbles + mascot(230, 960, 90), "SCHRUMPELFINGER?", "Warum passiert das im Wasser?", "Wasser", "#ffb347", "#062a3a")

i2b_body = f"""
<ellipse cx="540" cy="830" rx="420" ry="300" fill="#3fd6c5" opacity=".2" filter="url(#glow)"/>
<path d="M150 760 C 260 700, 360 820, 470 760 S 690 700, 800 760 S 930 820, 960 790" fill="none" stroke="#ffe0c8" stroke-width="40" stroke-linecap="round"/>
<path d="M150 900 H 930" stroke="#ff6f7f" stroke-width="56" stroke-linecap="round"/>
<path d="M150 890 H 930" stroke="#ffb0b8" stroke-width="12" stroke-linecap="round" opacity=".7"/>
<path d="M160 1040 C 380 980, 620 1080, 930 1000" fill="none" stroke="#ffe36b" stroke-width="16" stroke-linecap="round"/>
<path d="M160 1040 C 380 980, 620 1080, 930 1000" fill="none" stroke="#ffe36b" stroke-width="44" stroke-linecap="round" opacity=".3" filter="url(#soft)"/>
{mascot(880, 1000, 70, "cellb")}
<g font-family="Montserrat" font-weight="800" font-size="34" fill="#fff"><text x="160" y="700">HAUT</text><text x="160" y="975">BLUTGEFÄSS</text><text x="400" y="1095" fill="#ffe36b">NERV SENDET SIGNAL</text></g>
"""
i2b = page(I2_BG, i2b_body, "NERVEN STEUERN ES", "Die Gefäße werden enger", "enger", "#ffb347", "#062a3a")

for name, html in [("idee1_a", i1a), ("idee1_b", i1b), ("idee2_a", i2a), ("idee2_b", i2b)]:
    open(f"{OUT}/{name}.html", "w").write(html)
import subprocess
subprocess.run(["node", "-e", """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}});
for (const n of ['idee1_a','idee1_b','idee2_a','idee2_b']) { await p.goto('file://' + process.cwd() + '/' + n + '.html'); await p.waitForTimeout(1200); await p.screenshot({path: n + '.png'}); }
await b.close(); })();"""], check=True, cwd=OUT)
from PIL import Image
for idea in ("idee1", "idee2"):
    a, bb = Image.open(f"{OUT}/{idea}_a.png"), Image.open(f"{OUT}/{idea}_b.png")
    sheet = Image.new("RGB", (2160 + 40, 1920), (30, 30, 30)); sheet.paste(a, (0, 0)); sheet.paste(bb, (1120, 0))
    sheet.resize((1100, 960)).save(f"{OUT}/AI72_Stil_{idea.replace('idee', 'Idee')}.png")
print("ok")
