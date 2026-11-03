# AI72 #09 – Rätsel: "Warum schwimmt Eis?" – kg house style, riddle format.
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import S, SCENE_CSS, think, follow, share

KEYS = {"rätsel:", "schwimmt", "eis", "fest", "schwerer", "wachs", "kommentare,", "@ai72,", "lösung:", "gitter", "lücken.",
        "9", "%", "leichter", "leben:", "oben", "fische", "speicher", "schick"}
TITLES = {"hook": "RÄTSEL", "wax": "SELTSAM, ODER?", "think": "DEINE ANTWORT?", "follow": "AI72", "lattice": "DIE LÖSUNG",
          "lake": "DAS RETTET LEBEN", "share": "SPEICHERN & TEILEN"}

def glass(cx, cy, w, h, fill="#46a6ff", level=0.7):
    d = f"M{cx - w/2} {cy - h/2} L{cx - w/2 + 20} {cy + h/2} H{cx + w/2 - 20} L{cx + w/2} {cy - h/2}"
    top = cy + h/2 - h * level
    liquid = f"M{cx - w/2 + 20*(1-level) + 4} {top} H{cx + w/2 - 20*(1-level) - 4} L{cx + w/2 - 24} {cy + h/2 - 6} H{cx - w/2 + 24} Z"
    return (f'<path d="{liquid}" fill="{fill}" opacity=".85"/>'
            f'<path d="{d}" fill="none" stroke="#e8f6ff" stroke-width="10" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>')

def cube(cx, cy, s, cls="", col=("#dff6ff", "#a9dcf2")):
    d = K.rrect(cx - s/2, cy - s/2, s, s, s * 0.18)
    return f'<g class="{cls}">' + K.shaded(d, col[0], f"M{cx} {cy - s} H{cx + s} V{cy + s} H{cx} Z", col[1]) + \
           f'<rect x="{cx - s*0.32}" y="{cy - s*0.32}" width="{s*0.18}" height="{s*0.18}" rx="4" fill="#fff"/></g>'

def hook(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + f'<g id="{p}-gl">{glass(760, 930, 260, 300, level=0.75)}{cube(760, 830, 90, p+"-ice")}</g>'
             + f'<g id="{p}-guy">{K.person(230, 1150, 0.7, "point")}</g>') + \
           '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;left:400px;right:70px;font-size:46px">Warum schwimmt<br/>Eis oben?</div>'
    js = (f'tl.fromTo("#{p}-card", {{scale: 0.7, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)"}}, 0.2);'
          f'tl.fromTo("#{p}-gl", {{scale: 0, transformOrigin: "760px 930px"}}, {{scale: 1, duration: 0.5, ease: "back.out(1.6)"}}, 0.5);'
          f'tl.fromTo(".{p}-ice", {{y: -260}}, {{y: 0, duration: 0.7, ease: "bounce.out"}}, 1.0);')
    return html, js

def wax(p, dur, lead):
    html = S(f'<g id="{p}-a">{glass(300, 860, 260, 300, "#ffcf7a", 0.78)}{cube(300, 960, 80, p+"-wx", ("#ffe9b8", "#f0c070"))}</g>'
             + f'<g id="{p}-b">{glass(780, 860, 260, 300, "#46a6ff", 0.78)}{cube(780, 760, 80, p+"-ic")}</g>') + \
           f'<div class="pill" style="left:140px;top:1040px;width:320px;height:76px;line-height:76px;font-size:30px;background:#f1eefc">WACHS: SINKT</div>' + \
           f'<div class="pill" style="left:610px;top:1040px;width:340px;height:76px;line-height:76px;font-size:30px;background:{K.Y}">EIS: SCHWIMMT</div>'
    t2 = lead + (dur - lead) * 0.55
    js = (f'tl.fromTo("#{p}-a", {{x: -100, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo(".{p}-wx", {{y: -200}}, {{y: 0, duration: 0.9, ease: "power2.in"}}, {lead + 1.4});'
          f'tl.fromTo("#{p}-b", {{x: 100, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {t2 - 0.4});'
          f'tl.fromTo(".{p}-ic", {{y: -200}}, {{y: 0, duration: 0.8, ease: "bounce.out"}}, {t2});')
    return html, js

def lattice(p, dur, lead):
    r = random.Random(5)
    liq = "".join(f'<circle cx="{180 + r.randint(0, 240)}" cy="{640 + r.randint(0, 300)}" r="16" fill="{K.BLU}"/>' for _ in range(34))
    hexes = ""
    for row in range(4):
        for col in range(3):
            cx = 650 + col * 110 + (55 if row % 2 else 0); cy = 660 + row * 95
            pts = [(cx + 50 * math.cos(math.radians(60 * i + 30)), cy + 50 * math.sin(math.radians(60 * i + 30))) for i in range(6)]
            hexes += "<path d=\"" + " ".join(f"{'M' if i == 0 else 'L'}{x:.0f} {y:.0f}" for i, (x, y) in enumerate(pts)) + f' Z" fill="none" stroke="#bfeaff" stroke-width="6"/>'
            hexes += "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="{K.BLU}"/>' for x, y in pts[::2])
    html = S(f'<g id="{p}-l"><rect x="150" y="610" width="300" height="360" rx="40" fill="#3b2ca0"/>{liq}</g>'
             + f'<g id="{p}-s"><rect x="590" y="590" width="400" height="400" rx="40" fill="#3b2ca0"/>{hexes}</g>') + \
           f'<div class="pill" style="left:150px;top:1010px;width:300px;height:70px;line-height:70px;font-size:30px;background:#f1eefc">WASSER: DICHT</div>' + \
           f'<div class="pill" style="left:610px;top:1010px;width:360px;height:70px;line-height:70px;font-size:30px;background:{K.Y}">EIS: GITTER + LÜCKEN</div>' + \
           f'<div id="{p}-n" class="big" style="top:470px;font-size:96px">+9 % PLATZ</div>'
    t2 = lead + (dur - lead) * 0.62
    js = (f'tl.fromTo("#{p}-l", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-s", {{opacity: 0, scale: 0.6, transformOrigin: "790px 790px"}}, {{opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.4)"}}, {lead + 1.6});'
          f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {t2});')
    return html, js

def lake(p, dur, lead):
    fish = ""
    for k, (x, y, col) in enumerate([(320, 930, K.ORA), (620, 990, K.Y), (800, 900, K.MAG)]):
        fish += (f'<g class="{p}-fish"><ellipse cx="{x}" cy="{y}" rx="46" ry="26" fill="{col}"/>'
                 f'<path d="M{x-40} {y} L{x-80} {y-26} L{x-80} {y+26} Z" fill="{col}"/><circle cx="{x+22}" cy="{y-6}" r="6" fill="{K.INK}"/></g>')
    html = S(f'<rect x="90" y="640" width="900" height="450" rx="50" fill="#1f5fae"/>'
             + f'<rect x="90" y="840" width="900" height="250" fill="#174a8c"/>'
             + f'<g id="{p}-ice">{K.shaded(K.rrect(90, 600, 900, 90, 30), "#e6f7ff", "M540 590 H1000 V700 H540 Z", "#b7def2")}</g>' + fish) + \
           f'<div class="pill" style="left:380px;top:540px;width:320px;height:64px;line-height:64px;font-size:30px;background:#f1eefc">EIS OBEN</div>' + \
           f'<div class="pill" style="left:350px;top:1105px;width:380px;height:64px;line-height:64px;font-size:30px;background:{K.Y}">UNTEN: CA. 4 °C</div>'
    js = (f'tl.fromTo("#{p}-ice", {{scaleY: 0, transformOrigin: "540px 600px"}}, {{scaleY: 1, duration: 0.6, ease: "power3.out"}}, {lead + 0.4});'
          f'tl.fromTo(".{p}-fish", {{x: -30}}, {{x: 30, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: 0.2}}, {lead + 0.8});')
    return html, js

SCENES = {"hook": hook, "wax": wax, "think": think, "follow": follow, "lattice": lattice, "lake": lake, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.2, 0.45), ("pop", 0, 1.0, 0.4), ("click-soft", 1, 1.4, 0.4), ("pop", 1, 4.0, 0.45),
       ("click-soft", 2, 1.3, 0.4), ("click-soft", 2, 2.6, 0.4), ("click-soft", 2, 3.9, 0.4), ("pop", 3, 0.6, 0.5),
       ("sparkle", 4, 1.6, 0.4), ("pop", 4, 6.6, 0.5), ("whoosh-short", 5, 0.3, 0.35), ("pop", 6, 0.0, 0.5)]
