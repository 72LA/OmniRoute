# malangenommen72 #09 – Fuß-in-der-Tür (Freedman & Fraser 1966) – Dark v2, playbook format.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import S, IN, DRAW, ln, follow, SCENE_CSS

W = L.W
KEYS = {"kleine", "bitte,", "bitte.", "4-mal", "ja", "großen.", "1966", "17", "%", "@malangenommen72", "sofort", "76",
        "fuß-in-der-tür-effekt.", "treu", "kleiner,", "speicher", "große."}
TITLES = {"hook": "1 KLEINE BITTE", "loop": "MAL ANGENOMMEN …", "sign": "DAS RIESEN-SCHILD", "bars": "DER UNTERSCHIED",
          "steps": "FUSS IN DER TÜR", "tip": "SO NUTZT DU ES"}

def house(p, x, y, s=1.0, cls=""):
    d = f"M{x} {y} V{y-220*s} L{x+150*s} {y-330*s} L{x+300*s} {y-220*s} V{y} Z M{x+110*s} {y} V{y-120*s} H{x+190*s} V{y}"
    return f'<g filter="url(#{p}-glow)">' + ln(d, cls) + '</g>'

def hook(p, dur, lead):
    inner = (L.spot(p, 540, 860, 380, 300)
             + L.big(540, 520, "1 KLEINE BITTE.", 82) + L.big(540, 625, "4× MEHR JA.", 96)
             + f'<g filter="url(#{p}-glow)">{ln("M180 900 H300 V980 H180 Z", p+"-small")}{ln("M560 760 H960 V1060 H560 Z", p+"-bigs")}</g>'
             + L.label(240, 1030, "KLEIN", 28) + L.label(760, 1110, "GROSS", 28)
             + f'<g class="{p}-arr" opacity="0">{L.big(430, 950, "→", 90)}</g>')
    js = DRAW(f".{p}-small", 0.15, 0.4) + f'tl.to(".{p}-arr", {{opacity: 1, duration: 0.2}}, 0.6);' + DRAW(f".{p}-bigs", 0.7, 0.6)
    return S(p, inner), js

def loop(p, dur, lead):
    inner = (L.spot(p, 420, 900, 320, 300) + L.figure(p, 380, 1110, 1.15, "think")
             + f'<g filter="url(#{p}-glow)">{ln("M600 640 H960 V1100 H600 Z", p+"-box")}</g>'
             + L.big(780, 900, "?", 200, p+"-q") + L.label(780, 1160, "AM ENDE: DER TRICK", 28, cls=p+"-end")
             + f'<path d="M80 1112 H560" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = DRAW(f".{p}-box", lead, 0.6) + IN(f".{p}-q", lead + 0.5) + IN(f".{p}-end", lead + (dur - lead) * 0.5)
    return S(p, inner), js

def sign(p, dur, lead):
    inner = (L.spot(p, 540, 860, 400, 300) + house(p, 90, 1110, 1.1, p+"-h")
             + f'<g filter="url(#{p}-glow)">{ln("M520 640 H1000 V880 H520 Z M760 880 V1110", p+"-sg")}'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/></g>'
             + L.label(760, 745, "FAHR", 44, cls=p+"-st") + L.label(760, 810, "VORSICHTIG", 44, cls=p+"-st")
             + L.big(760, 590, "17 % JA", 72, p+"-v") + L.label(540, 1170, "1966 · FREEDMAN & FRASER", 28, op=.8, cls=p+"-src"))
    js = (DRAW(f".{p}-h", lead, 0.7) + DRAW(f".{p}-sg", lead + 0.8, 0.6) + IN(f".{p}-st", lead + 1.3) + IN(f".{p}-src", lead + 0.6)
          + IN(f".{p}-v", lead + (dur - lead) * 0.72))
    return S(p, inner), js

def bars(p, dur, lead):
    base, top = 1050, 520
    h1, h2 = (base - top) * 0.17, (base - top) * 0.76
    inner = (L.spot(p, 540, 860, 380, 320)
             + f'<path d="M120 {base} H960" {W} stroke-width="3" stroke-opacity=".8"/>'
             + "".join(f'<path d="M120 {base - (base-top)*k/4} H960" stroke="#fff" stroke-opacity=".18" stroke-width="2" stroke-dasharray="8 10"/>' for k in range(1, 5))
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-b1" x="250" y="{base - h1}" width="200" height="{h1}" rx="14" {W} stroke-width="5" style="transform-origin:350px {base}px"/>'
             + f'<rect id="{p}-b2" x="630" y="{base - h2}" width="200" height="{h2}" rx="14" fill="#fff" style="transform-origin:730px {base}px"/></g>'
             + L.big(350, base - h1 - 30, "17 %", 70, p+"-v1") + L.big(730, base - h2 - 30, "76 %", 70, p+"-v2")
             + L.label(350, base + 50, "DIREKT", 28) + L.label(730, base + 50, "ERST KLEIN", 28)
             + L.label(540, base + 100, "AUFKLEBER → SCHILD", 28, op=.8, cls=p+"-note"))
    t2 = lead + (dur - lead) * 0.62
    js = (f'tl.fromTo("#{p}-b1", {{scaleY: 0}}, {{scaleY: 1, duration: 0.6, ease: "power3.out"}}, {lead});' + IN(f".{p}-v1", lead + 0.5)
          + IN(f".{p}-note", lead + 1.2)
          + f'tl.fromTo("#{p}-b2", {{scaleY: 0}}, {{scaleY: 1, duration: 0.8, ease: "power3.out"}}, {t2});' + IN(f".{p}-v2", t2 + 0.6))
    return S(p, inner), js

def steps(p, dur, lead):
    st = "".join(ln(f"M{160 + k*190} {1100 - k*110} H{350 + k*190} V{1100 - (k+1)*110}", p + f"-s{k}", 6) for k in range(4))
    inner = (L.spot(p, 540, 840, 420, 300) + f'<g filter="url(#{p}-glow)">{st}</g>'
             + f'<g class="{p}-guy">' + L.figure(p, 260, 1100, 0.75, "stand") + '</g>'
             + L.label(540, 560, "EINMAL JA = ICH HELFE GERN", 28, cls=p+"-t")
             + L.label(540, 1170, "SPÄTERE STUDIEN: KLEINERER EFFEKT", 28, op=.8, cls=p+"-c"))
    js = "".join(DRAW(f".{p}-s{k}", lead + 0.2 + k * 0.35, 0.3) for k in range(4))
    js += IN(f".{p}-t", lead + 1.6)
    js += f'tl.fromTo(".{p}-guy", {{x: 0, y: 0}}, {{keyframes: [{{x: 190, y: -110, duration: 0.5}}, {{x: 380, y: -220, duration: 0.5}}, {{x: 570, y: -330, duration: 0.5}}]}}, {lead + 2.2});'
    js += IN(f".{p}-c", lead + (dur - lead) * 0.6)
    return S(p, inner), js

def tip(p, dur, lead):
    stepsl = ["1 · KLEINE BITTE", "2 · KURZ WARTEN", "3 · GROSSE BITTE"]
    inner = L.spot(p, 540, 820, 380, 300) + f'<g filter="url(#{p}-glow)">{ln("M180 540 H900 V1040 H180 Z", p+"-card")}</g>'
    for k, s_ in enumerate(stepsl):
        y = 660 + k * 120
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M240 {y-28} H296 V{y+28} H240 Z", p+f"-box{k}", 4)}{ln(f"M250 {y} L265 {y+16} L290 {y-18}", p+f"-tick{k}", 6)}</g>'
        inner += L.label(330, y + 10, s_, 30, "start", cls=p + f"-t{k}")
    inner += L.label(540, 1110, "↓ SPEICHER DIR DAS", 30, cls=p+"-c")
    per = max(0.8, (dur - lead) / 4.5)
    js = DRAW(f".{p}-card", lead, 0.5)
    for k in range(3):
        t = lead + 0.8 + k * per
        js += DRAW(f".{p}-box{k}", t, 0.25) + IN(f".{p}-t{k}", t + 0.1) + DRAW(f".{p}-tick{k}", t + 0.35, 0.25)
    js += IN(f".{p}-c", lead + (dur - lead) * 0.55)
    return S(p, inner), js

SCENES = {"hook": hook, "loop": loop, "sign": sign, "follow": follow, "bars": bars, "steps": steps, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.6, 0.4), ("click-soft", 1, 0.5, 0.35), ("pop", 2, 4.9, 0.45),
       ("pop", 3, 1.1, 0.5), ("pop", 4, 0.5, 0.4), ("pop", 4, 5.3, 0.5), ("click-soft", 5, 2.2, 0.35), ("click-soft", 5, 2.7, 0.35),
       ("click-soft", 5, 3.2, 0.35), ("pop", 6, 1.2, 0.4), ("pop", 6, 2.7, 0.4), ("pop", 6, 4.2, 0.4)]
