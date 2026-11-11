"""malangenommen72 Dark v2 style frames – glowing white line-art on black, dot grid, solid glowing figure,
spaced-caps labels, metaphor diagrams + cozy scenes (after the operator's reference screenshots)."""
import os, subprocess
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;800;900&display=swap');"

DEFS = """<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="bloom" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="spot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="gridfade" cx=".5" cy=".5" r=".55"><stop offset=".6" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<pattern id="dots" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="16" cy="16" r="1.6" fill="#5a5a5a"/></pattern>
<mask id="gm"><rect x="0" y="420" width="1080" height="900" fill="url(#gridfade)"/></mask>
</defs>"""

def grid():
    return '<rect width="1080" height="1920" fill="#000"/><rect x="0" y="420" width="1080" height="900" fill="url(#dots)" mask="url(#gm)"/>'

def figure(x, y, s=1.0, pose="stand"):
    """solid white side-view figure, feet at (x,y)."""
    g = f'<g transform="translate({x} {y}) scale({s})" filter="url(#bloom)" fill="#fff">'
    g += '<circle cx="0" cy="-205" r="34"/>'                      # head
    g += '<rect x="-30" y="-165" width="60" height="95" rx="28"/>'  # torso
    if pose == "stand":
        g += '<rect x="-13" y="-85" width="26" height="85" rx="12"/><rect x="-4" y="-12" width="40" height="18" rx="9"/>'
        g += '<rect x="2" y="-205" width="22" height="120" rx="11" transform="rotate(14 13 -150)"/>'  # arm raised to head (thinking)
    else:  # sit
        g += '<rect x="-24" y="-85" width="80" height="26" rx="13"/><rect x="34" y="-85" width="26" height="80" rx="12"/><rect x="34" y="-12" width="40" height="18" rx="9"/>'
        g += '<rect x="0" y="-150" width="90" height="22" rx="11" transform="rotate(12 0 -140)"/>'
    return g + '</g>'

def label(x, y, text, size=26, anchor="middle", op=1.0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="600" font-size="{size}" letter-spacing="{size*0.38:.0f}" fill="#fff" opacity="{op}">{text}</text>'

W = 'stroke="#fff" fill="none" stroke-linecap="round" stroke-linejoin="round"'

def frame_a():
    s = DEFS + grid()
    s += '<ellipse cx="540" cy="880" rx="330" ry="330" fill="url(#spot)"/>'
    s += f'<g filter="url(#glow)"><path d="M300 520 V1160 M780 520 V1160" {W} stroke-width="5"/></g>'
    for y, v, op in [(640, "€4.000", .65), (860, "€3.000", .65), (1080, "€2.000", 1)]:
        s += f'<path d="M40 {y} H1040" stroke="#fff" stroke-opacity=".22" stroke-width="2" stroke-dasharray="8 10"/>'
        s += f'<path d="M262 {y} H300" stroke="#fff" stroke-width="4"/>'
        s += f'<text x="250" y="{y+10}" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="34" fill="#fff" opacity="{op}">{v}</text>'
    s += f'<g filter="url(#glow)"><rect x="318" y="700" width="444" height="34" rx="12" {W} stroke-width="5" stroke-dasharray="18 12"/>'
    s += f'<rect x="318" y="1046" width="444" height="34" rx="12" {W} stroke-width="5"/></g>'
    s += label(540, 680, "ERWARTUNGEN")
    s += f'<path d="M370 1090 V1110 H710 V1090" {W} stroke-width="2"/>' + label(540, 1145, "UMSTÄNDE", 24)
    s += f'<path d="M560 772 H830 M560 1046 H830" stroke="#fff" stroke-opacity=".6" stroke-width="2" stroke-dasharray="6 6"/><path d="M815 772 V1046 M800 772 H830 M800 1046 H830" {W} stroke-width="3"/>'
    s += label(845, 918, "GLEICHE", 20, "start") + label(845, 948, "LÜCKE", 20, "start")
    s += figure(540, 1044, 1.15, "stand")
    return s

def frame_b():
    s = DEFS + grid()
    s += '<ellipse cx="560" cy="930" rx="260" ry="200" fill="url(#spot)"/>'
    s += f'<g filter="url(#glow)">'
    s += f'<path d="M60 1080 H1020" {W} stroke-width="3" stroke-opacity=".8"/>'
    s += f'<rect x="80" y="560" width="220" height="250" rx="12" {W} stroke-width="5"/><path d="M190 560 V810 M80 690 H300" {W} stroke-width="4"/>'
    s += f'<path d="M95 760 L150 735 L200 755 L285 725" {W} stroke-width="3"/><path d="M70 822 H310" {W} stroke-width="4"/>'
    s += '<path d="M150 600 a18 18 0 1 0 14 30 a14 14 0 1 1 -14 -30z" fill="#fff"/>'
    s += f'<rect x="790" y="600" width="210" height="240" rx="18" fill="#fff"/><rect x="800" y="680" width="190" height="150" rx="8" fill="#000"/>'
    s += f'<circle cx="840" cy="598" r="9" {W} stroke-width="4"/><circle cx="950" cy="598" r="9" {W} stroke-width="4"/>'
    s += f'<path d="M390 920 H900 M410 920 V1080 M880 920 V1080 M410 975 H880" {W} stroke-width="5"/>'
    s += f'<path d="M600 915 L640 800 M600 915 H680" {W} stroke-width="5"/>'
    s += f'<rect x="760" y="870" width="36" height="46" rx="6" {W} stroke-width="4"/><path d="M796 882 q16 6 0 18" {W} stroke-width="3"/>'
    s += f'<path d="M770 855 q-8 -12 0 -24 M784 855 q-8 -12 0 -24" {W} stroke-width="2" stroke-opacity=".7"/>'
    s += f'<path d="M300 1080 V990 M300 990 H360 M330 1000 L310 1080" {W} stroke-width="4"/>'
    s += '</g>'
    s += '<text x="895" y="655" text-anchor="middle" font-family="Montserrat" font-weight="600" font-size="20" letter-spacing="8" fill="#000">JAHR</text><text x="895" y="782" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="62" fill="#fff">2026</text>'
    s += figure(430, 1078, 1.0, "sit")
    return s

def page(svg, title, cap):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT}
    html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Montserrat,sans-serif}}
    svg{{position:absolute;left:0;top:0}}
    .stamp{{position:absolute;top:190px;left:0;right:0;text-align:center}}
    .stamp span{{font-weight:600;font-size:26px;letter-spacing:.35em;color:#cfcfcf;border:2px solid #777;padding:8px 20px}}
    .title{{position:absolute;top:270px;left:0;right:0;text-align:center;color:#fff;font-weight:800;font-size:64px;letter-spacing:.06em;text-shadow:0 0 18px rgba(255,255,255,.55)}}
    .cap{{position:absolute;top:1200px;left:0;right:0;text-align:center;color:#fff;font-weight:800;font-size:70px;padding:0 80px;text-shadow:0 0 16px rgba(255,255,255,.45)}}
    .cap b{{background:#fff;color:#000;padding:0 12px;text-shadow:none}}
    </style></head><body><svg width="1080" height="1920" viewBox="0 0 1080 1920">{svg}</svg>
    <div class="stamp"><span>MAL ANGENOMMEN #08</span></div><div class="title">{title}</div><div class="cap">{cap}</div></body></html>"""

A = page(frame_a(), "DOPPELT SO VIEL GELD?", "Die Lücke bleibt <b>gleich</b>")
B = page(frame_b(), "MAL ANGENOMMEN …", "… du verdienst ab <b>morgen</b>")
for n, h in [("dark2_a", A), ("dark2_b", B)]:
    open(f"{OUT}/{n}.html", "w").write(h)
subprocess.run(["node", "-e", """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1920}});
for (const n of ['dark2_b','dark2_a']) { await p.goto('file://' + process.cwd() + '/' + n + '.html'); await p.waitForTimeout(1200); await p.screenshot({path: n + '.png'}); }
await b.close(); })();"""], check=True, cwd=OUT)
from PIL import Image
a, b = Image.open(f"{OUT}/dark2_b.png"), Image.open(f"{OUT}/dark2_a.png")
sh = Image.new("RGB", (2200, 1920), (25, 25, 25)); sh.paste(a, (0, 0)); sh.paste(b, (1120, 0))
sh.resize((1100, 960)).save(f"{OUT}/malangenommen72_Dark_v2.png"); print("ok")
