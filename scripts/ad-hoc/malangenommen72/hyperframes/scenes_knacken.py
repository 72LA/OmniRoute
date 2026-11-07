# AI72 #11 – Mythos-Check: "Macht Fingerknacken Arthrose?" – kg house style, helpful question format (no riddle).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import S, SCENE_CSS

KEYS = {"fingerknacken", "arthrose", "60", "jahre", "linken", "rechte", "keiner", "ig-nobelpreis", "@ai72", "alltag", "215",
        "zusammenhang", "gas-hohlraum", "20", "minuten", "ehrlich", "geschwollene", "harmlos", "weh", "abklären", "speicher", "knackt"}
TITLES = {"hook": "MYTHOS-CHECK", "unger": "DER SELBSTTEST", "result": "DAS ERGEBNIS", "follow": "AI72",
          "joint": "WAS DA KNACKT", "honest": "EHRLICH GESAGT", "share": "SPEICHERN & TEILEN"}

def pill(id_, x, y, w, text, bg, fs=30, h=72, col="#1b0f3d", extra=""):
    return (f'<div id="{id_}" class="pill" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;line-height:{h}px;'
            f'font-size:{fs}px;background:{bg};color:{col};{extra}">{text}</div>')

def burst(cls, x, y, text="KNACK!", col=K.Y):
    pts = " ".join(f"{x + (70 if i % 2 == 0 else 40) * __import__('math').cos(i * 0.5236):.0f},{y + (70 if i % 2 == 0 else 40) * __import__('math').sin(i * 0.5236):.0f}" for i in range(12))
    return (f'<g class="{cls}" opacity="0"><polygon points="{pts}" fill="{col}"/>'
            f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="30" fill="{K.INK}">{text}</text></g>')

def check(cls, x, y):
    return (f'<g class="{cls}" opacity="0"><circle cx="{x}" cy="{y}" r="52" fill="#2ad4c0"/>'
            f'<path d="M{x-24} {y+2} L{x-6} {y+20} L{x+26} {y-18}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>')

def hook(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + f'<g id="{p}-hl">{K.hand(330, 960, 0.5, -12)}</g><g id="{p}-hr">{K.hand(750, 960, 0.5, 12)}</g>'
             + burst(f"{p}-k1", 250, 760) + burst(f"{p}-k2", 830, 760) + burst(f"{p}-k3", 540, 700)) + \
           '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;font-size:50px">Macht Fingerknacken<br/>Arthrose?</div>' + \
           pill(f"{p}-t", 260, 1080, 560, "60 JAHRE SELBSTTEST", K.Y)
    js = (f'tl.fromTo("#{p}-card", {{scale: 0.85}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, 0.1);'
          f'tl.fromTo(["#{p}-hl", "#{p}-hr"], {{y: 40}}, {{y: 0, duration: 0.5, ease: "expo.out", stagger: 0.12}}, 0.1);'
          + "".join(f'tl.fromTo(".{p}-k{k}", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.5)"}}, {0.8 + k * 0.55});'
                    f'tl.to(".{p}-k{k}", {{opacity: 0, duration: 0.2}}, {1.3 + k * 0.55});' for k in range(1, 4))
          + f'tl.fromTo("#{p}-t", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + (dur - lead) * 0.6});')
    return html, js

def unger(p, dur, lead):
    html = S(f'<g id="{p}-hl">{K.hand(300, 900, 0.55, -8)}</g><g id="{p}-hr">{K.hand(780, 900, 0.55, 8)}</g>'
             + "".join(burst(f"{p}-k", 300 + dx, 640 + dy) for dx, dy in [(-70, 0), (60, -40)])) + \
           f'<div id="{p}-n" class="big" style="top:440px;font-size:92px">60+ JAHRE</div>' + \
           pill(f"{p}-l", 90, 1060, 420, "LINKS: 2× TÄGLICH", K.Y) + pill(f"{p}-r", 570, 1060, 420, "RECHTS: NIE", "#f1eefc")
    span = dur - lead
    js = (f'tl.fromTo("#{p}-hl", {{x: -120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + span * 0.12});'
          f'tl.fromTo(".{p}-k", {{opacity: 0}}, {{opacity: 1, duration: 0.12, yoyo: true, repeat: 7, stagger: 0.3}}, {lead + span * 0.3});'
          f'tl.fromTo("#{p}-l", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.5});'
          f'tl.fromTo("#{p}-hr", {{x: 120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead + span * 0.74});'
          f'tl.fromTo("#{p}-r", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.8});')
    return html, js

def trophy(x, y):
    cup = f"M{x-80} {y-90} H{x+80} C {x+80} {y-10}, {x+40} {y+20}, {x} {y+20} C {x-40} {y+20}, {x-80} {y-10}, {x-80} {y-90} Z"
    return (K.shaded(cup, K.Y, f"M{x+10} {y-100} H{x+100} V{y+30} H{x+10} Z", K.Y_D)
            + f'<path d="M{x-80} {y-70} C {x-130} {y-70}, {x-130} {y-10}, {x-70} {y-20} M{x+80} {y-70} C {x+130} {y-70}, {x+130} {y-10}, {x+70} {y-20}" fill="none" stroke="{K.Y_D}" stroke-width="14"/>'
            + f'<rect x="{x-14}" y="{y+18}" width="28" height="40" fill="{K.Y_D}"/><rect x="{x-60}" y="{y+56}" width="120" height="30" rx="10" fill="{K.ORA}"/>')

def result(p, dur, lead):
    html = S(f'{K.hand(240, 900, 0.42, -8)}{K.hand(560, 900, 0.42, 8)}' + check(f"{p}-c", 240, 720) + check(f"{p}-c", 560, 720)
             + f'<g id="{p}-tr">{trophy(850, 860)}</g>') + \
           f'<div id="{p}-n" class="big" style="top:440px;font-size:76px">KEINE ARTHROSE</div>' + \
           pill(f"{p}-ig", 610, 1060, 420, "IG-NOBELPREIS 2009", "#f1eefc")
    span = dur - lead
    js = (f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + 0.3});'
          f'tl.fromTo(".{p}-c", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.25}}, {lead + 0.6});'
          f'tl.fromTo("#{p}-tr", {{scale: 0, svgOrigin: "850 900"}}, {{scale: 1, duration: 0.5, ease: "back.out(1.8)"}}, {lead + span * 0.55});'
          f'tl.fromTo("#{p}-ig", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.62});')
    return html, js

def follow(p, dur, lead):
    html = S(f'<g id="{p}-guy">{K.person(540, 935, 0.6, "wave")}</g>') + \
           f'<div class="big" style="top:955px;font-size:60px;color:#fff;text-shadow:0 5px 0 #1b0f3d">@ai72</div>' + \
           pill(f"{p}-btn", 360, 1045, 360, "+ FOLGEN", K.MAG, 46, 84, "#fff") + \
           pill(f"{p}-tag", 270, 420, 540, "WISSEN, DAS DIR HILFT", K.Y, 32, 70)
    js = (f'tl.fromTo("#{p}-guy", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-btn", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + 0.6});'
          f'tl.fromTo("#{p}-tag", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + 1.1});')
    return html, js

def joint(p, dur, lead):
    span = dur - lead
    base = 860
    h1, h2 = 300 * 0.181 / 0.25, 300 * 0.215 / 0.25
    bars = (f'<g id="{p}-st"><rect x="120" y="560" width="840" height="360" rx="40" fill="#2a1f86"/>'
            f'<rect id="{p}-b1" x="300" y="{base - h1}" width="160" height="{h1}" rx="20" fill="{K.Y}" style="transform-origin:380px {base}px"/>'
            f'<rect id="{p}-b2" x="620" y="{base - h2}" width="160" height="{h2}" rx="20" fill="#f1eefc" style="transform-origin:700px {base}px"/>'
            f'<text x="380" y="{base - h1 - 20}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#fff">18 %</text>'
            f'<text x="700" y="{base - h2 - 20}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#fff">22 %</text>'
            f'<text x="380" y="900" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">KNACKER</text>'
            f'<text x="700" y="900" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">NICHT-KNACKER</text></g>')
    bone = lambda y0, flip: K.shaded(K.rrect(410, y0, 260, 170, 80), "#fff6e6", f"M540 {y0 - 10} H690 V{y0 + 190} H540 Z", "#e9dcc4")
    jnt = (f'<g id="{p}-jt" opacity="0"><rect x="380" y="560" width="320" height="400" rx="60" fill="#3b2ca0" opacity=".7"/>'
           f'<g id="{p}-top">{bone(560, 0)}</g><g id="{p}-bot">{bone(790, 1)}</g>'
           f'<g id="{p}-gas"><circle cx="540" cy="760" r="38" fill="#7ff3e4"/><circle cx="526" cy="748" r="10" fill="#fff"/></g></g>')
    html = S(bars + jnt) + pill(f"{p}-s", 190, 440, 700, "215 MENSCHEN: KEIN ZUSAMMENHANG", "#f1eefc", 28, 70) + \
           pill(f"{p}-g", 700, 725, 320, "GAS-HOHLRAUM", "#2ad4c0", 30, 70, extra="opacity:0") + \
           pill(f"{p}-m", 290, 1040, 500, "⏱ CA. 20 MIN PAUSE", K.Y, 32, 76)
    tj = lead + span * 0.3; tm = lead + span * 0.7
    js = (f'tl.fromTo("#{p}-s", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead});'
          f'tl.fromTo(["#{p}-b1", "#{p}-b2"], {{scaleY: 0}}, {{scaleY: 1, duration: 0.6, ease: "power3.out", stagger: 0.25}}, {lead + 0.4});'
          f'tl.to("#{p}-st", {{opacity: 0, duration: 0.3}}, {tj - 0.3});tl.to("#{p}-s", {{opacity: 0, duration: 0.3}}, {tj - 0.3});'
          f'tl.to("#{p}-jt", {{opacity: 1, duration: 0.3}}, {tj});'
          f'tl.fromTo("#{p}-top", {{y: 30}}, {{y: -20, duration: 0.5, ease: "power2.out"}}, {tj + 1.0});'
          f'tl.fromTo("#{p}-bot", {{y: -30}}, {{y: 20, duration: 0.5, ease: "power2.out"}}, {tj + 1.0});'
          f'tl.fromTo("#{p}-gas", {{scale: 0, svgOrigin: "540 760"}}, {{scale: 1.4, duration: 0.15, ease: "back.out(3)"}}, {tj + 1.3});'
          f'tl.to("#{p}-g", {{opacity: 1, duration: 0.25}}, {tj + 1.5});'
          f'tl.fromTo("#{p}-m", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {tm});')
    return html, js

def honest(p, dur, lead):
    span = dur - lead
    html = S(f'<g id="{p}-h">{K.hand(540, 860, 0.55, 0)}</g>'
             + f'<circle id="{p}-sw" cx="540" cy="760" r="120" fill="{K.MAG}" opacity="0"/>') + \
           pill(f"{p}-e", 190, 440, 700, "ÄLTERE STUDIE: ÖFTER GESCHWOLLEN", "#f1eefc", 28, 70) + \
           pill(f"{p}-ok", 120, 960, 840, "✓ OHNE SCHMERZ: MEIST HARMLOS", "#2ad4c0", 32, 76) + \
           pill(f"{p}-doc", 120, 1050, 840, "TUT'S WEH? ÄRZTLICH ABKLÄREN", K.MAG, 32, 76, "#fff")
    js = (f'tl.fromTo("#{p}-e", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-h", {{y: 120, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-sw", {{opacity: 0}}, {{opacity: 0.35, duration: 0.5, yoyo: true, repeat: 3}}, {lead + 0.8});'
          f'tl.fromTo("#{p}-ok", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.48});'
          f'tl.fromTo("#{p}-doc", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.74});')
    return html, js

def share(p, dur, lead):
    bub = (f'<g id="{p}-b"><rect x="430" y="520" width="580" height="300" rx="70" fill="{K.INK}" transform="translate(10 14)"/>'
           + K.shaded(K.rrect(430, 520, 580, 300, 70), "#f1eefc", "M720 500 H1030 V840 H720 Z", "#cfc6f5")
           + '<path d="M520 810 L 470 900 L 600 815 Z" fill="#f1eefc"/></g>')
    html = S(K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0) + f'<g id="{p}-guy">{K.person(240, 1150, 0.78, "point")}</g>' + bub) + \
           f'<div id="{p}-t" class="big" style="left:430px;right:auto;width:580px;top:585px;font-size:46px;color:#1b0f3d;text-shadow:none;line-height:1.15">SCHICK\'S DEM<br/><span style="color:{K.MAG}">FINGER-KNACKER!</span></div>' + \
           pill(f"{p}-sv", 560, 860, 420, "↓ SPEICHERN", K.Y, 34, 76)
    js = (f'tl.fromTo("#{p}-b", {{scale: 0, transformOrigin: "720px 670px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-t", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-sv", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.2});'
          f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, 0);')
    return html, js

SCENES = {"hook": hook, "unger": unger, "result": result, "follow": follow, "joint": joint, "honest": honest, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.1, 0.45), ("click-soft", 0, 0.8, 0.5), ("click-soft", 0, 1.35, 0.5), ("click-soft", 0, 1.9, 0.5),
       ("pop", 0, 3.3, 0.4), ("pop", 1, 1.0, 0.4), ("click-soft", 1, 2.3, 0.45), ("click-soft", 1, 2.9, 0.45), ("pop", 1, 3.7, 0.4),
       ("pop", 1, 5.6, 0.4), ("sparkle", 2, 0.4, 0.45), ("pop", 2, 2.6, 0.45), ("pop", 3, 0.6, 0.5), ("pop", 4, 0.1, 0.4),
       ("click-soft", 4, 4.5, 0.55), ("pop", 4, 7.5, 0.4), ("pop", 5, 3.8, 0.4), ("pop", 5, 5.7, 0.4), ("pop", 6, 0.2, 0.5)]
