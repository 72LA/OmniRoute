# AI72 #14 – Mythos-Check: "Frieren Frauen wirklich schneller?" (Kingma & van Marken Lichtenbelt 2015) – kg, upgraded
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import SCENE_CSS
from scenes_knacken import pill
from scenes_vitc import S, T

FX = True
KEYS = {"frieren", "frauen", "schneller", "ja", "büro", "formel", "60ern", "40-jährigen", "mann", "70", "kilo", "weniger", "körperwärme",
        "3", "grad", "wärmer", "zwiebellook", "füße", "heizung", "schick", "fenster"}
TITLES = {"hook": "MYTHOS-CHECK #3", "formula": "DIE BÜRO-FORMEL", "therm": "DER UNTERSCHIED", "tip": "SO HILFT'S", "share": "TEILEN"}

def flakes(cls, n=14, seed=2):
    import random; r = random.Random(seed)
    return "".join(f'<g class="{cls}"><path d="M{x} {y-14} V{y+14} M{x-12} {y-7} L{x+12} {y+7} M{x-12} {y+7} L{x+12} {y-7}" stroke="#bfeaff" stroke-width="4" stroke-linecap="round"/></g>'
                   for x, y in [(r.randint(80, 1000), r.randint(500, 1000)) for _ in range(n)])

def ac_unit(x, y):
    return (K.shaded(K.rrect(x, y, 300, 110, 24), "#f1eefc", f"M{x+150} {y-10} H{x+310} V{y+120} H{x+150} Z", "#cfc6f5")
            + "".join(f'<rect x="{x+30}" y="{y+60+k*14}" width="240" height="6" rx="3" fill="#8f86c9"/>' for k in range(3)))

def hook(p, dur, lead):
    span = dur - lead
    inner = (K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2) + flakes(f"{p}-fl")
             + f'<g id="{p}-ac">{ac_unit(640, 640)}' + "".join(f'<path class="{p}-air" d="M{680 + k*60} 770 q-20 60 10 120" stroke="#7fd8ff" stroke-width="8" fill="none" stroke-linecap="round" opacity="0"/>' for k in range(4)) + '</g>'
             + f'<g id="{p}-guy"><g id="{p}-sh">{K.person(330, 1150, 0.6, "belly")}</g></g>')
    sv, cam = S(p, inner, dur)
    html = sv + '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;font-size:50px">Frieren Frauen<br/>wirklich schneller?</div>' + \
           pill(f"{p}-ja", 600, 900, 300, "JA.", K.Y, 54, 96)
    tj = lead + span * 0.42; tb = lead + span * 0.6
    js = (cam + f'tl.fromTo("#{p}-card", {{scale: 0.85}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, 0.1);'
          f'tl.fromTo("#{p}-sh", {{x: -4}}, {{x: 4, duration: 0.06, repeat: {int(dur/0.06)}, yoyo: true, ease: "none"}}, 0);'
          f'tl.fromTo(".{p}-fl", {{y: -120, opacity: 0}}, {{y: 160, opacity: 1, duration: 2.6, ease: "none", stagger: 0.12}}, 0);'
          f'tl.fromTo("#{p}-ja", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2.2)"}}, {tj});'
          f'tl.to("#{p}-ja", {{opacity: 0, duration: 0.2}}, {tb - 0.1});'
          f'tl.fromTo("#{p}-ac", {{opacity: 0, y: -40}}, {{opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)"}}, {tb});'
          f'tl.to(".{p}-air", {{opacity: 1, duration: 0.3, stagger: 0.1}}, {tb + 0.3});')
    return html, js

def formula(p, dur, lead):
    span = dur - lead
    doc = (f'<rect x="150" y="610" width="330" height="420" rx="26" fill="{K.INK}" transform="translate(10 14)"/>'
           + K.shaded(K.rrect(150, 610, 330, 420, 26), "#fff6e6", "M320 600 H490 V1040 H320 Z", "#efe2c8")
           + "".join(f'<rect x="190" y="{690 + k*60}" width="{250 - (k % 2)*70}" height="16" rx="8" fill="#c9bfa6"/>' for k in range(5))
           + T(315, 670, "ϑ = f(M)", 40, K.INK))
    man = (f'<circle cx="790" cy="700" r="60" fill="#8f86c9"/>' + K.shaded(K.rrect(720, 770, 140, 220, 50), "#6b5ad6", "M790 760 H870 V1000 H790 Z", "#5546b8")
           + f'<rect x="735" y="980" width="45" height="80" rx="20" fill="#4a3d9e"/><rect x="800" y="980" width="45" height="80" rx="20" fill="#4a3d9e"/>')
    inner = f'<g id="{p}-doc">{doc}</g><g id="{p}-man">{man}</g>'
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-yr", 170, 520, 290, "1960ER", K.Y, 40, 76) + pill(f"{p}-m", 600, 1090, 400, "MANN · 40 J.", "#f1eefc", 32, 70) + \
           pill(f"{p}-kg", 660, 520, 280, "70 KG", K.MAG, 40, 76, "#fff")
    js = (cam + f'tl.fromTo("#{p}-doc", {{y: 80, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.5)"}}, {lead});'
          f'tl.fromTo("#{p}-yr", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.22});'
          f'tl.fromTo("#{p}-man", {{x: 120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead + span * 0.5});'
          f'tl.fromTo("#{p}-m", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.6});'
          f'tl.fromTo("#{p}-kg", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.8});')
    return html, js

def therm(p, dur, lead):
    span = dur - lead; base = 1040
    tube = (f'<rect x="700" y="560" width="90" height="440" rx="45" fill="{K.INK}" transform="translate(8 12)"/>'
            f'<rect x="700" y="560" width="90" height="440" rx="45" fill="#f1eefc"/><circle cx="745" cy="1010" r="70" fill="#ff4a4a"/>'
            f'<rect id="{p}-hg" x="725" y="660" width="40" height="350" rx="20" fill="#ff4a4a"/>')
    bars = (f'<rect id="{p}-w" x="180" y="{base-200}" width="150" height="200" rx="18" fill="{K.MAG}"/>'
            f'<rect id="{p}-mn" x="380" y="{base-290}" width="150" height="290" rx="18" fill="#6b5ad6"/>'
            + T(255, base + 50, "FRAUEN", 28, "#fff", 800) + T(455, base + 50, "MÄNNER", 28, "#fff", 800)
            + T(355, 700, "KÖRPERWÄRME", 30, "#fff", 900))
    inner = f'<g id="{p}-tb">{tube}</g>{bars}'
    sv, cam = S(p, inner, dur)
    html = sv + f'<div id="{p}-n" class="big" style="top:440px;left:560px;right:auto;width:400px;font-size:110px">+3 °C</div>' + \
           pill(f"{p}-fol", 290, 372, 500, "+ FOLGEN @ai72", K.MAG, 32, 66, "#fff") + \
           pill(f"{p}-s", 190, 1110, 700, "KLEINE STUDIE · 16 FRAUEN", "#f1eefc", 28, 64)
    tt = lead + span * 0.55
    js = (cam + f'tl.fromTo("#{p}-w", {{scaleY: 0, svgOrigin: "255 {base}"}}, {{scaleY: 1, duration: 0.5, ease: "power3.out"}}, {lead + 0.2});'
          f'tl.fromTo("#{p}-mn", {{scaleY: 0, svgOrigin: "455 {base}"}}, {{scaleY: 1, duration: 0.5, ease: "power3.out"}}, {lead + 0.5});'
          f'tl.fromTo("#{p}-tb", {{opacity: 0, x: 80}}, {{opacity: 1, x: 0, duration: 0.4, ease: "expo.out"}}, {tt - 0.5});'
          f'tl.fromTo("#{p}-hg", {{scaleY: 0.35, svgOrigin: "745 1010"}}, {{scaleY: 1, duration: 1.0, ease: "power2.out"}}, {tt});'
          f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {tt + 0.6});'
          f'tl.fromTo("#{p}-s", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(1.8)"}}, {lead + span * 0.82});'
          f'tl.fromTo("#{p}-fol", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead});tl.to("#{p}-fol", {{opacity: 0, duration: 0.25}}, {lead + 2.2});')
    return html, js

def tip(p, dur, lead):
    span = dur - lead
    scarf = (f'<path d="M-90 -460 Q0 -420 90 -460 L95 -420 Q0 -380 -95 -420 Z" fill="{K.MAG}"/>'
             f'<rect x="40" y="-430" width="40" height="140" rx="16" fill="{K.MAG}"/>')
    inner = (K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0)
             + f'<g id="{p}-guy">{K.person(540, 1150, 0.72, "wave")}<g id="{p}-sc" transform="translate(540 1150) scale(0.72)">{scarf}</g></g>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 120, 470, 400, "ZWIEBELLOOK", K.Y, 34, 76) + pill(f"{p}-b", 560, 470, 400, "WARME FÜSSE", "#2ad4c0", 34, 76) + \
           pill(f"{p}-c", 190, 570, 700, "STATT HEIZUNGS-STREIT", "#f1eefc", 32, 70)
    js = (cam + f'tl.fromTo("#{p}-guy", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-sc", {{scale: 0, opacity: 0}}, {{scale: 0.72, opacity: 1, duration: 0.35, ease: "back.out(2)"}}, {lead + span * 0.25});'
          f'tl.fromTo("#{p}-a", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.15});'
          f'tl.fromTo("#{p}-b", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.4});'
          f'tl.fromTo("#{p}-c", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(2)"}}, {lead + span * 0.65});')
    return html, js

def share(p, dur, lead):
    span = dur - lead
    win = (f'<rect x="600" y="640" width="320" height="380" rx="20" fill="{K.INK}" transform="translate(10 14)"/>'
           f'<rect x="600" y="640" width="320" height="380" rx="20" fill="#7fd8ff"/>'
           f'<g id="{p}-wd"><rect x="600" y="640" width="160" height="380" rx="20" fill="#c9eefc" stroke="#f1eefc" stroke-width="14"/></g>'
           f'<rect x="600" y="640" width="320" height="380" rx="20" fill="none" stroke="#f1eefc" stroke-width="14"/>')
    inner = (K.plant_corner("l", 1250, 3) + win + flakes(f"{p}-fl", 8, 5)
             + f'<g id="{p}-guy">{K.person(270, 1150, 0.75, "point")}</g>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-t", 120, 470, 840, "SCHICK'S DEM FENSTER-AUFREISSER!", K.Y, 34, 80) + \
           pill(f"{p}-q", 330, 1070, 560, "FRIEREN FRAUEN SCHNELLER?", "#f1eefc", 28, 64)
    js = (cam + f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.4, ease: "expo.out"}}, 0);'
          f'tl.fromTo("#{p}-t", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.1});'
          f'tl.fromTo("#{p}-wd", {{scaleX: 1, svgOrigin: "600 830"}}, {{scaleX: 0.25, duration: 0.5, ease: "power2.inOut"}}, {lead + span * 0.3});'
          f'tl.fromTo(".{p}-fl", {{x: 0, opacity: 0}}, {{x: -380, opacity: 1, duration: 1.4, ease: "power1.out", stagger: 0.08}}, {lead + span * 0.4});'
          f'tl.fromTo("#{p}-q", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(1.8)"}}, {lead + span * 0.75});')
    return html, js

SCENES = {"hook": hook, "formula": formula, "therm": therm, "tip": tip, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.18), ("pop", 0, 0.1, 0.15), ("pop", 0, 1.9, 0.18), ("whoosh-short", 0, 2.7, 0.12),
       ("click-soft", 1, 0.0, 0.14), ("pop", 1, 1.3, 0.14), ("pop", 1, 2.9, 0.14), ("pop", 1, 4.4, 0.14),
       ("click-soft", 2, 0.2, 0.13), ("sparkle", 2, 3.9, 0.13), ("pop", 3, 0.5, 0.13), ("pop", 3, 1.4, 0.13), ("pop", 3, 2.2, 0.13),
       ("whoosh-short", 4, 0.9, 0.12), ("chime", 4, 2.3, 0.12)]
