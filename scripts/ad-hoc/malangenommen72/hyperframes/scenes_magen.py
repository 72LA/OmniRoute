# AI72 #07 – "Warum knurrt dein Magen?" – kg house style.
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K

KEYS = {"knurrt", "magen,", "magen", "hunger", "darm.", "darm", "90", "120", "putzwelle.", "putzwelle", "@ai72", "körper.",
        "leer,", "leer", "laut.", "motilin.", "motilin", "hungersignal", "gehirn.", "peinlichsten?", "kommentare."}
TITLES = {"hook": "MAGENKNURREN?", "source": "WOHER KOMMT'S?", "wave": "DIE PUTZWELLE", "follow": "AI72",
          "empty": "LEER = LAUT", "motilin": "EIN HUNGERSIGNAL", "ask": "UND BEI DIR?"}
SCENE_CSS = """
.title { top: 258px; font-style: italic; font-size: 78px; letter-spacing: .01em; }
.rule { position: absolute; top: 372px; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 34px; letter-spacing: .18em; color: #fff; }
.pill { position: absolute; border-radius: 60px; font-weight: 900; text-align: center; color: #1b0f3d; }
.grr { position: absolute; font-weight: 900; font-style: italic; color: #ffd23f; text-shadow: 0 6px 0 #1b0f3d; }
svg { position: absolute; overflow: visible; }
"""

def S(inner):
    return f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{inner}</svg>'

def stomach(cx, cy, s=1.0, food=False):
    d = (f"M{cx-60*s} {cy-150*s} C {cx-40*s} {cy-200*s}, {cx+30*s} {cy-190*s}, {cx+30*s} {cy-130*s} C {cx+30*s} {cy-80*s}, {cx+170*s} {cy-90*s}, {cx+170*s} {cy+20*s} "
         f"C {cx+170*s} {cy+150*s}, {cx-20*s} {cy+190*s}, {cx-120*s} {cy+110*s} C {cx-190*s} {cy+60*s}, {cx-130*s} {cy-20*s}, {cx-90*s} {cy-40*s} "
         f"C {cx-60*s} {cy-60*s}, {cx-80*s} {cy-120*s}, {cx-60*s} {cy-150*s} Z")
    g = K.shaded(d, K.MAG, f"M{cx+20*s} {cy-220*s} C {cx+200*s} {cy-60*s}, {cx+180*s} {cy+160*s}, {cx-40*s} {cy+220*s} H{cx+260*s} V{cy-220*s} Z", "#d2357f")
    g += f'<path d="M{cx-40*s} {cy-10*s} C {cx} {cy-40*s}, {cx+70*s} {cy-30*s}, {cx+100*s} {cy+10*s}" fill="none" stroke="#ff8cc4" stroke-width="{14*s}" stroke-linecap="round"/>'
    if food:
        for k, (x, y, col) in enumerate([(-40, 40, K.Y), (30, 70, K.ORA), (80, 20, K.HOOD), (0, 100, K.BLU), (-80, 80, K.Y)]):
            g += f'<circle cx="{cx+x*s}" cy="{cy+y*s}" r="{26*s}" fill="{col}"/>'
    return g

def gut(cx, cy, s=1.0, cls=""):
    pts = []
    for k in range(5):
        y = cy - 120*s + k*60*s; x0, x1 = cx - 170*s, cx + 170*s
        pts.append(f"{'M' if k == 0 else 'L'}{x0 if k % 2 == 0 else x1} {y}")
        pts.append(f"C {x0 if k % 2 == 0 else x1} {y}, {(x1 + 60*s) if k % 2 == 0 else (x0 - 60*s)} {y + 30*s}, {x1 if k % 2 == 0 else x0} {y + 60*s}")
    d = " ".join(pts)
    return (f'<path d="{d}" fill="none" stroke="#c94f78" stroke-width="{58*s}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path class="{cls}" d="{d}" fill="none" stroke="{K.SKIN}" stroke-width="{44*s}" stroke-linecap="round" stroke-linejoin="round"/>')

def arcs(cx, cy, n, cls, col=K.Y):
    return "".join(f'<path class="{cls}" d="M{cx + 40 + k*42} {cy - 50 - k*22} Q {cx + 70 + k*48} {cy}, {cx + 40 + k*42} {cy + 50 + k*22}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round"/>' for k in range(n))

def hook(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + f'<g id="{p}-guy">{K.person(400, 1150, 0.9, "belly")}</g>' + arcs(470, 880, 3, p + "-arc")) + \
           '<div class="rule">— AI72 ERKLÄRT —</div>' + f'<div id="{p}-g" class="grr" style="left:640px;top:760px;font-size:120px">GRRR…</div>'
    js = (f'tl.fromTo(".{p}-arc", {{opacity: 0, x: -20}}, {{opacity: 1, x: 0, duration: 0.25, stagger: 0.12, ease: "power2.out", repeat: 3, yoyo: true}}, 0.2);'
          f'tl.fromTo("#{p}-g", {{scale: 0.3, opacity: 0, rotation: -12}}, {{scale: 1, opacity: 1, rotation: -6, duration: 0.45, ease: "back.out(2)"}}, 0.5);'
          f'tl.fromTo("#{p}-guy", {{x: 0}}, {{x: 8, duration: 0.06, repeat: 9, yoyo: true}}, 0.5);')
    return html, js

def source(p, dur, lead):
    html = S(f'<g id="{p}-st">{stomach(330, 760, 1.0)}</g><g id="{p}-gu">{gut(760, 790, 0.9, "")}</g>') + \
           f'<div id="{p}-l1" class="pill" style="left:200px;top:990px;width:260px;height:80px;line-height:80px;font-size:40px;background:{K.Y}">MAGEN</div>' + \
           f'<div id="{p}-l2" class="pill" style="left:630px;top:990px;width:260px;height:80px;line-height:80px;font-size:40px;background:{K.HOOD}">+ DARM</div>'
    t2 = lead + (dur - lead) * 0.6
    js = (f'tl.fromTo("#{p}-st", {{scale: 0, transformOrigin: "330px 760px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-l1", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.5});'
          f'tl.fromTo("#{p}-gu", {{scale: 0, transformOrigin: "760px 790px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {t2});'
          f'tl.fromTo("#{p}-l2", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {t2 + 0.4});')
    return html, js

def wave(p, dur, lead):
    tube = (f'<rect x="120" y="760" width="840" height="150" rx="75" fill="#c94f78"/><rect x="130" y="770" width="820" height="130" rx="65" fill="{K.SKIN}"/>'
            f'<rect x="130" y="840" width="820" height="60" rx="30" fill="{K.SKIN_D}"/>')
    ring = f'<g id="{p}-ring"><rect x="150" y="740" width="70" height="190" rx="35" fill="{K.MAG}"/><rect x="185" y="740" width="35" height="190" rx="17" fill="#d2357f"/></g>'
    bits = "".join(f'<circle class="{p}-bit" cx="{260 + k*20}" cy="{820 + (k%2)*30}" r="{14 + (k%3)*4}" fill="{[K.Y, K.BLU, "#fff"][k%3]}"/>' for k in range(5))
    clock = (f'<g id="{p}-clk"><circle cx="540" cy="560" r="96" fill="{K.INK}"/>' + K.shaded(K.circ(540, 552, 90), "#f1eefc", "M540 450 H650 V650 H540 Z", "#cfc6f5")
             + f'<path id="{p}-hd" d="M540 552 V485" stroke="{K.INK}" stroke-width="12" stroke-linecap="round"/><circle cx="540" cy="552" r="10" fill="{K.INK}"/></g>')
    html = S(tube + bits + ring + clock) + \
           f'<div id="{p}-t" class="pill" style="left:620px;top:520px;width:380px;height:80px;line-height:80px;font-size:38px;background:{K.Y}">ALLE 90–120 MIN</div>'
    span = max(2.0, dur - lead - 1.5)
    js = (f'tl.fromTo("#{p}-clk", {{scale: 0, transformOrigin: "540px 552px"}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-hd", {{rotation: 0, svgOrigin: "540 552"}}, {{rotation: 720, duration: {span}, ease: "none"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-t", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 2.0});'
          f'tl.fromTo("#{p}-ring", {{x: 0}}, {{x: 700, duration: {span*0.7}, ease: "power1.inOut"}}, {lead + 3.0});'
          f'tl.fromTo(".{p}-bit", {{x: 0}}, {{x: 660, duration: {span*0.7}, ease: "power1.inOut", stagger: 0.05}}, {lead + 3.1});')
    return html, js

def follow(p, dur, lead):
    html = S(f'<g id="{p}-guy">{K.person(540, 935, 0.6, "wave")}</g>') + \
           f'<div id="{p}-h" class="grr" style="left:0;right:0;text-align:center;top:955px;font-size:60px;color:#fff">@ai72</div>' + \
           f'<div id="{p}-btn" class="pill" style="left:360px;top:1045px;width:360px;height:84px;line-height:84px;font-size:46px;background:{K.MAG};color:#fff">+ FOLGEN</div>'
    js = (f'tl.fromTo("#{p}-guy", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-btn", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + 0.6});')
    return html, js

def empty(p, dur, lead):
    html = S(f'<g id="{p}-a">{stomach(290, 760, 0.8, True)}</g><g id="{p}-b">{stomach(770, 760, 0.8, False)}{arcs(860, 760, 3, p + "-arc")}</g>'
             + f'<path d="M250 640 q10 -30 20 0" fill="none" stroke="{K.Y}" stroke-width="8" stroke-linecap="round"/>') + \
           f'<div class="pill" style="left:170px;top:990px;width:240px;height:76px;line-height:76px;font-size:38px;background:#f1eefc">VOLL</div>' + \
           f'<div class="pill" style="left:650px;top:990px;width:240px;height:76px;line-height:76px;font-size:38px;background:{K.Y}">LEER</div>'
    js = (f'tl.fromTo("#{p}-a", {{x: -80, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-b", {{x: 80, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead + 0.3});'
          f'tl.fromTo(".{p}-arc", {{opacity: 0}}, {{opacity: 1, duration: 0.2, stagger: 0.1, repeat: 5, yoyo: true}}, {lead + 1.2});')
    return html, js

def motilin(p, dur, lead):
    hexes = "".join(K.shaded(" ".join(f"{'M' if i == 0 else 'L'}{x + 34*math.cos(math.radians(60*i))} {y + 34*math.sin(math.radians(60*i))}" for i in range(6)) + " Z",
                             K.HOOD, f"M{x} {y-40} H{x+40} V{y+40} H{x} Z", K.HOOD_D) for x, y in [(0, 0), (58, 34), (0, 68)])
    brain = "".join(K.shaded(K.circ(820 + x, 560 + y, r), "#ff7fb6", f"M{820 + x} {560 + y - r - 5} H{820 + x + r + 5} V{560 + y + r + 5} H{820 + x} Z", "#e0569a")
                    for x, y, r in [(-60, 0, 70), (0, -40, 80), (60, 0, 70), (0, 30, 70)])
    html = S(f'<g id="{p}-gut">{gut(260, 900, 0.55)}</g><g id="{p}-br">{brain}</g>'
             + f'<path id="{p}-path" d="M330 820 C 450 700, 600 760, 740 620" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="6" stroke-dasharray="14 14"/>'
             + f'<g transform="translate(300 820)"><g id="{p}-mol">{hexes}</g></g>') + \
           f'<div id="{p}-l" class="pill" style="left:120px;top:1040px;width:300px;height:76px;line-height:76px;font-size:38px;background:{K.HOOD}">MOTILIN</div>' + \
           f'<div id="{p}-v" class="pill" style="left:620px;top:1040px;width:400px;height:76px;line-height:76px;font-size:32px;background:#f1eefc">FORSCHER VERMUTEN</div>'
    t2 = lead + (dur - lead) * 0.45
    js = (f'tl.fromTo("#{p}-gut", {{scale: 0, transformOrigin: "260px 900px"}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-l", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 1.5});'
          f'tl.fromTo("#{p}-br", {{scale: 0, transformOrigin: "820px 560px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {t2});'
          f'tl.fromTo("#{p}-mol", {{x: 0, y: 0}}, {{x: 450, y: -210, duration: 1.2, ease: "power2.inOut"}}, {t2 + 0.3});'
          f'tl.fromTo("#{p}-v", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {t2 + 0.6});')
    return html, js

def ask(p, dur, lead):
    bub = (f'<g id="{p}-b"><rect x="430" y="520" width="580" height="300" rx="70" fill="{K.INK}" transform="translate(10 14)"/>'
           + K.shaded(K.rrect(430, 520, 580, 300, 70), "#f1eefc", "M720 500 H1030 V840 H720 Z", "#cfc6f5")
           + f'<path d="M520 810 L 470 900 L 600 815 Z" fill="#f1eefc"/></g>')
    html = S(K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0) + f'<g id="{p}-guy">{K.person(240, 1150, 0.78, "point")}</g>' + bub) + \
           f'<div id="{p}-t" class="grr" style="left:430px;width:580px;text-align:center;top:590px;font-size:52px;color:#1b0f3d;text-shadow:none;line-height:1.15">WANN KNURRT\'S<br/><span style="color:{K.MAG}">BEI DIR?</span></div>'
    js = (f'tl.fromTo("#{p}-b", {{scale: 0, transformOrigin: "720px 670px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-t", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, 0);')
    return html, js

SCENES = {"hook": hook, "source": source, "wave": wave, "follow": follow, "empty": empty, "motilin": motilin, "ask": ask}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.5, 0.5), ("pop", 1, 0.0, 0.45), ("pop", 1, 2.7, 0.45),
       ("click-soft", 2, 0.0, 0.4), ("pop", 2, 2.0, 0.45), ("whoosh-short", 2, 3.0, 0.35), ("pop", 3, 0.6, 0.5),
       ("pop", 4, 0.0, 0.4), ("pop", 4, 0.3, 0.4), ("sparkle", 5, 2.5, 0.35), ("pop", 6, 0.0, 0.5)]
