# AI72 #12 – Mythos-Check #2: "Hilft Vitamin C gegen Erkältung?" (Hemilä & Chalker 2013; Prather et al. 2015) – kg house style.
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import SCENE_CSS
from scenes_knacken import pill, check

KEYS = {"vitamin", "c", "erkältung", "11.000", "kaum", "zählt", "nicht", "8", "%", "halber", "tag", "kratzt", "kein", "klarer",
        "effekt", "@ai72", "mythos-check", "schlaf", "erkältungsviren", "5", "6", "4-mal", "7", "ehrlich", "hände", "paprika",
        "kiwi", "speicher", "vitamin-c-tabletten"}
TITLES = {"hook": "MYTHOS-CHECK #2", "week": "DAS ERGEBNIS", "late": "UND BEI HALSKRATZEN?", "follow": "AI72",
          "sleep": "WAS MEHR ZÄHLT", "tips": "SO SCHÜTZT DU DICH", "share": "SPEICHERN & TEILEN"}

def S(p, inner, dur):
    svg = f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920"><g id="{p}-cam">{inner}</g></svg>'
    return svg, f'tl.fromTo("#{p}-cam", {{scale: 1}}, {{scale: 1.025, svgOrigin: "540 820", duration: {dur}, ease: "none"}}, 0);'

def T(x, y, text, fs=40, col="#fff", w=900, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="{w}" font-size="{fs}" fill="{col}">{text}</text>'

def orange(cx, cy, r):
    seg = "".join(f'<path d="M{cx} {cy} L{cx + r*0.78*math.cos(math.radians(a)):.0f} {cy + r*0.78*math.sin(math.radians(a)):.0f}" stroke="#ffd9a8" stroke-width="6"/>' for a in range(0, 360, 45))
    return (K.shaded(K.circ(cx, cy, r), K.ORA, f"M{cx} {cy - r - 5} H{cx + r + 5} V{cy + r + 5} H{cx} Z", "#e06d24")
            + f'<circle cx="{cx}" cy="{cy}" r="{r*0.8}" fill="#ffb25c"/>' + seg + f'<circle cx="{cx}" cy="{cy}" r="{r*0.12}" fill="#ffd9a8"/>')

def bottle(cx, cy, s=1.0):
    w, h = 170 * s, 240 * s
    return (f'<rect x="{cx - w/2 + 12}" y="{cy - h/2 + 14}" width="{w}" height="{h}" rx="{30*s}" fill="{K.INK}"/>'
            + K.shaded(K.rrect(cx - w/2, cy - h/2, w, h, 30 * s), "#f4f1ff", f"M{cx + 10} {cy - h} H{cx + w} V{cy + h} H{cx + 10} Z", "#cfc6f5")
            + K.shaded(K.rrect(cx - w/2 + 10*s, cy - h/2 - 50*s, w - 20*s, 60*s, 16*s), K.MAG, f"M{cx + 10} {cy - h} H{cx + w} V{cy} H{cx + 10} Z", "#d2357f")
            + f'<rect x="{cx - w/2}" y="{cy - 30*s}" width="{w}" height="{90*s}" fill="{K.Y}"/>'
            + T(cx, cy + 40 * s, "C", 80 * s, K.INK))

def virus(cls, cx, cy, r, col="#2ad4c0"):
    sp = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + (r+16)*math.cos(math.radians(a)):.0f}" y2="{cy + (r+16)*math.sin(math.radians(a)):.0f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
                 f'<circle cx="{cx + (r+18)*math.cos(math.radians(a)):.0f}" cy="{cy + (r+18)*math.sin(math.radians(a)):.0f}" r="8" fill="{col}"/>' for a in range(0, 360, 45))
    return f'<g class="{cls}">{sp}<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx - r*0.3}" cy="{cy - r*0.3}" r="{r*0.22}" fill="#7ff3e4"/></g>'

def bed(cx, cy, s=1.0):
    return (f'<rect x="{cx - 230*s}" y="{cy - 20*s}" width="{460*s}" height="{90*s}" rx="{20*s}" fill="#6b4bd6"/>'
            + f'<rect x="{cx - 250*s}" y="{cy - 120*s}" width="{40*s}" height="{230*s}" rx="{16*s}" fill="#4a35b0"/>'
            + K.shaded(K.rrect(cx - 205*s, cy - 70*s, 120*s, 60*s, 26*s), "#f4f1ff", f"M{cx - 140*s} {cy - 80*s} H{cx - 80*s} V{cy} H{cx - 140*s} Z", "#cfc6f5")
            + K.shaded(K.rrect(cx - 90*s, cy - 60*s, 330*s, 70*s, 30*s), K.HOOD, f"M{cx + 60*s} {cy - 70*s} H{cx + 250*s} V{cy + 20*s} H{cx + 60*s} Z", K.HOOD_D)
            + f'<circle cx="{cx - 145*s}" cy="{cy - 75*s}" r="{40*s}" fill="{K.SKIN}"/><path d="M{cx - 175*s} {cy - 95*s} Q{cx - 145*s} {cy - 135*s} {cx - 110*s} {cy - 95*s}" fill="{K.HAIR}"/>'
            + f'<path d="M{cx - 160*s} {cy - 72*s} q8 6 16 0 M{cx - 136*s} {cy - 72*s} q8 6 16 0" stroke="{K.INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')

def paprika(cx, cy):
    return (K.shaded(f"M{cx-60} {cy-40} C {cx-80} {cy+40}, {cx-40} {cy+90}, {cx} {cy+80} C {cx+40} {cy+90}, {cx+80} {cy+40}, {cx+60} {cy-40} C {cx+40} {cy-70}, {cx-40} {cy-70}, {cx-60} {cy-40} Z",
                     "#ff4a4a", f"M{cx+5} {cy-80} H{cx+90} V{cy+100} H{cx+5} Z", "#d93030")
            + f'<path d="M{cx} {cy-58} q4 -30 26 -34" stroke="#2ad4c0" stroke-width="12" fill="none" stroke-linecap="round"/>')

def kiwi(cx, cy, r=70):
    seeds = "".join(f'<ellipse cx="{cx + r*0.42*math.cos(math.radians(a)):.0f}" cy="{cy + r*0.42*math.sin(math.radians(a)):.0f}" rx="5" ry="9" fill="{K.INK}" transform="rotate({a+90} {cx + r*0.42*math.cos(math.radians(a)):.0f} {cy + r*0.42*math.sin(math.radians(a)):.0f})"/>' for a in range(0, 360, 30))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#8a5a2b"/><circle cx="{cx}" cy="{cy}" r="{r*0.86}" fill="#7bd64a"/>'
            + f'<circle cx="{cx}" cy="{cy}" r="{r*0.28}" fill="#e9f7c8"/>' + seeds)

def hook(p, dur, lead):
    span = dur - lead
    inner = (K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + f'<g id="{p}-or">{orange(330, 890, 130)}</g><g id="{p}-bt">{bottle(740, 900, 1.0)}</g>'
             + virus(f"{p}-v", 540, 720, 34, K.MAG))
    sv, cam = S(p, inner, dur)
    html = sv + '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;font-size:50px">Hilft Vitamin C gegen<br/>Erkältung?</div>' + \
           pill(f"{p}-n", 230, 1060, 620, "11.000+ MENSCHEN: KAUM", K.Y, 32, 76)
    js = (cam + f'tl.fromTo("#{p}-card", {{scale: 0.85}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, 0.1);'
          f'tl.fromTo("#{p}-or", {{y: 30}}, {{y: 0, duration: 0.6, ease: "back.out(1.6)"}}, 0.1);'
          f'tl.fromTo("#{p}-bt", {{rotation: -6, svgOrigin: "740 1020"}}, {{rotation: 6, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut"}}, 0.4);'
          f'tl.fromTo(".{p}-v", {{scale: 0, svgOrigin: "540 720"}}, {{scale: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + span * 0.2});'
          f'tl.to(".{p}-v", {{rotation: 90, svgOrigin: "540 720", duration: {span}, ease: "none"}}, {lead + span * 0.2});'
          f'tl.fromTo("#{p}-n", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.55});')
    return html, js

def week(p, dur, lead):
    span = dur - lead
    days = ["MO", "DI", "MI", "DO", "FR", "SA", "SO"]
    cells = ""
    for k, d in enumerate(days):
        x = 110 + k * 124
        cells += (f'<g class="{p}-d"><rect x="{x}" y="700" width="108" height="150" rx="20" fill="{K.MAG if k < 6 else "#ff8cc4"}"/>'
                  + T(x + 54, 790, d, 34, "#fff", 900) + '</g>')
    inner = (cells + f'<rect id="{p}-cut" x="{110 + 6*124 + 54}" y="690" width="64" height="170" rx="14" fill="{K.Y}" opacity="0"/>'
             + f'<path id="{p}-sc" d="M{110 + 6*124 + 54} 670 V880" stroke="#fff" stroke-width="6" stroke-dasharray="12 10" opacity="0"/>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 190, 470, 700, "SCHÜTZT NICHT VOR ERKÄLTUNG", "#f1eefc", 30, 76) + \
           pill(f"{p}-b", 330, 900, 420, "NUR −8 % DAUER", K.Y, 34, 76) + \
           pill(f"{p}-c", 290, 1000, 500, "≈ ½ TAG PRO WOCHE", "#2ad4c0", 32, 72) + \
           pill(f"{p}-x", 170, 590, 740, "AUSNAHME: EXTREMSPORTLER (−50 %)", "#3b2ca0", 28, 56, "#fff")
    js = (cam + f'tl.fromTo("#{p}-a", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead});'
          f'tl.fromTo(".{p}-d", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.08}}, {lead + span * 0.3});'
          f'tl.fromTo("#{p}-b", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.5});'
          f'tl.to(["#{p}-cut", "#{p}-sc"], {{opacity: 0.6, duration: 0.25}}, {lead + span * 0.72});'
          f'tl.fromTo("#{p}-c", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.74});'
          f'tl.fromTo("#{p}-x", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {lead + span * 0.2});')
    return html, js

def late(p, dur, lead):
    span = dur - lead
    inner = (f'<g id="{p}-bt">{bottle(360, 840, 0.9)}</g>'
             + f'<g id="{p}-th"><circle cx="760" cy="800" r="120" fill="{K.INK}" transform="translate(10 14)"/>'
             + K.shaded(K.circ(760, 800, 120), "#f1eefc", "M760 670 H890 V930 H760 Z", "#cfc6f5")
             + T(760, 830, "?", 110, K.MAG) + '</g>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-n", 190, 1020, 700, "KEIN KLARER EFFEKT", K.MAG, 36, 80, "#fff")
    js = (cam + f'tl.fromTo("#{p}-bt", {{x: -80, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.4, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-th", {{scale: 0, svgOrigin: "760 800"}}, {{scale: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + 0.4});'
          f'tl.fromTo("#{p}-n", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.5});')
    return html, js

def follow(p, dur, lead):
    sv, cam = S(p, f'<g id="{p}-guy">{K.person(540, 935, 0.6, "wave")}</g>', dur)
    html = sv + f'<div class="big" style="top:955px;font-size:60px;color:#fff;text-shadow:0 5px 0 #1b0f3d">@ai72</div>' + \
           pill(f"{p}-btn", 360, 1045, 360, "+ FOLGEN", K.MAG, 46, 84, "#fff") + \
           pill(f"{p}-tag", 240, 372, 600, "NÄCHSTER MYTHOS-CHECK", K.Y, 32, 70)
    js = (cam + f'tl.fromTo("#{p}-guy", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-btn", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.4});'
          f'tl.fromTo("#{p}-tag", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.7});')
    return html, js

def sleep(p, dur, lead):
    span = dur - lead
    base = 1000
    h1, h2 = 340, 340 / 4.2
    viruses = "".join(virus(f"{p}-vi", x, y, 20, K.MAG) for x, y in [(700, 560), (820, 620), (930, 540)])
    inner = (f'<g id="{p}-bed">{bed(330, 640, 0.85)}</g>'
             + f'<g id="{p}-z">{T(470, 470, "Z", 60, K.Y)}{T(520, 420, "z", 44, K.Y)}{T(560, 385, "z", 34, K.Y)}</g>'
             + f'<g id="{p}-vg">{viruses}</g>'
             + f'<g id="{p}-ch"><rect x="120" y="740" width="840" height="300" rx="40" fill="#2a1f86"/>'
             + f'<rect id="{p}-b1" x="250" y="{base - h1*0.62}" width="200" height="{h1*0.62}" rx="22" fill="{K.MAG}" style="transform-origin:350px {base}px"/>'
             + f'<rect id="{p}-b2" x="630" y="{base - h2*0.62}" width="200" height="{h2*0.62}" rx="22" fill="#2ad4c0" style="transform-origin:730px {base}px"/>'
             + T(350, base - h1*0.62 - 16, "≈ 4×", 46) + T(730, base - h2*0.62 - 16, "1×", 46)
             + T(350, base + 30, "5–6 STD", 28, "#fff", 800) + T(730, base + 30, "7+ STD", 28, "#fff", 800) + '</g>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-r", 600, 660, 380, "VIREN IN DIE NASE", "#f1eefc", 28, 64) + \
           pill(f"{p}-k", 250, 1060, 580, "ERKÄLTUNGS-RISIKO", K.Y, 32, 72)
    tc = lead + span * 0.5
    js = (cam + f'tl.fromTo("#{p}-bed", {{y: 40, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-z", {{y: 20, opacity: 0}}, {{y: -10, opacity: 1, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 3}}, {lead + 0.3});'
          f'tl.fromTo(".{p}-vi", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.15}}, {lead + span * 0.18});'
          f'tl.fromTo("#{p}-r", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.22});'
          f'tl.fromTo("#{p}-ch", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {tc - 0.3});'
          f'tl.fromTo("#{p}-b1", {{scaleY: 0}}, {{scaleY: 1, duration: 0.7, ease: "power3.out"}}, {tc});'
          f'tl.fromTo("#{p}-b2", {{scaleY: 0}}, {{scaleY: 1, duration: 0.6, ease: "power3.out"}}, {lead + span * 0.8});'
          f'tl.fromTo("#{p}-k", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {tc + 0.4});')
    return html, js

def tips(p, dur, lead):
    span = dur - lead
    hand = f'<g transform="translate(540 790)">{K.hand(0, 0, 0.34, 0)}</g>' + K.drop(500, 690, 18) + K.drop(590, 670, 14)
    inner = (f'<g id="{p}-i1">{bed(250, 800, 0.42)}</g><g id="{p}-i2">{hand}</g>'
             + f'<g id="{p}-i3">{paprika(800, 780)}{kiwi(910, 840, 56)}</g>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-e", 190, 450, 700, "EHRLICH: KLEINE STUDIE (164)", "#f1eefc", 28, 68) + \
           pill(f"{p}-t1", 80, 930, 300, "7 STD SCHLAF", K.Y, 28, 64) + \
           pill(f"{p}-t2", 390, 930, 300, "HÄNDE WASCHEN", "#2ad4c0", 28, 64) + \
           pill(f"{p}-t3", 700, 930, 300, "C AUS ESSEN", K.ORA, 28, 64)
    f = (0.25, 0.5, 0.72)
    js = cam + f'tl.fromTo("#{p}-e", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead});'
    for k in range(3):
        t = lead + span * f[k]
        js += (f'tl.fromTo("#{p}-i{k+1}", {{y: 50, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)"}}, {t});'
               f'tl.fromTo("#{p}-t{k+1}", {{scale: 0}}, {{scale: 1, duration: 0.3, ease: "back.out(1.8)"}}, {t + 0.15});')
    return html, js

def share(p, dur, lead):
    bub = (f'<g id="{p}-b"><rect x="430" y="520" width="580" height="300" rx="70" fill="{K.INK}" transform="translate(10 14)"/>'
           + K.shaded(K.rrect(430, 520, 580, 300, 70), "#f1eefc", "M720 500 H1030 V840 H720 Z", "#cfc6f5")
           + '<path d="M520 810 L 470 900 L 600 815 Z" fill="#f1eefc"/></g>')
    sv, cam = S(p, K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0) + f'<g id="{p}-guy">{K.person(240, 1150, 0.78, "point")}</g>' + bub, dur)
    html = sv + f'<div id="{p}-t" class="big" style="left:430px;right:auto;width:580px;top:585px;font-size:44px;color:#1b0f3d;text-shadow:none;line-height:1.15">SCHICK\'S DEM<br/><span style="color:{K.MAG}">VITAMIN-C-FAN!</span></div>' + \
           pill(f"{p}-sv", 560, 860, 420, "↓ SPEICHERN", K.Y, 34, 76) + \
           pill(f"{p}-q", 560, 960, 420, "HILFT VITAMIN C?", "#f1eefc", 28, 64)
    js = (cam + f'tl.fromTo("#{p}-b", {{scale: 0, transformOrigin: "720px 670px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-t", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-sv", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.2});'
          f'tl.fromTo("#{p}-q", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + (dur - lead) * 0.55});'
          f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, 0);')
    return html, js

SCENES = {"hook": hook, "week": week, "late": late, "follow": follow, "sleep": sleep, "tips": tips, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.1, 0.45), ("pop", 0, 1.4, 0.4), ("pop", 0, 3.9, 0.45), ("pop", 1, 0.0, 0.4),
       ("click-soft", 1, 2.2, 0.4), ("pop", 1, 3.6, 0.45), ("whoosh-short", 1, 5.2, 0.35), ("pop", 2, 0.4, 0.4), ("pop", 2, 1.6, 0.5),
       ("pop", 3, 0.4, 0.5), ("sparkle", 4, 0.3, 0.4), ("pop", 4, 2.0, 0.4), ("whoosh-short", 4, 5.2, 0.35), ("pop", 4, 8.3, 0.4),
       ("pop", 5, 0.0, 0.4), ("pop", 5, 1.5, 0.4), ("pop", 5, 2.9, 0.4), ("pop", 5, 4.0, 0.4), ("pop", 6, 0.2, 0.5), ("sparkle", 6, 4.8, 0.35)]
