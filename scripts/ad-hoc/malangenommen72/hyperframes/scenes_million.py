# malangenommen72 #11 – "Macht eine Million glücklicher?" (Brickman et al. 1978, hedonische Anpassung) – Dark v2.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import S, IN, DRAW, ln, follow, SCENE_CSS

W = L.W
KEYS = {"million.", "million", "glücklicher?", "überrascht.", "wirkt.", "1978", "lottogewinner", "4,0.", "3,8.", "unterschied.",
        "@malangenommen72", "hedonische", "anpassung:", "normal.", "etwas,", "erlebnisse", "pausen,", "speicher"}
TITLES = {"hook": "MAL ANGENOMMEN …", "loop": "DIE ANTWORT", "bars": "DIE LOTTO-STUDIE", "treadmill": "GEWÖHNUNG",
          "tip": "SO NUTZT DU ES"}

def ticket(p, x, y, cls):
    d = f"M{x} {y} H{x+300} V{y+50} A28 28 0 0 0 {x+300} {y+106} V{y+156} H{x} V{y+106} A28 28 0 0 0 {x} {y+50} Z"
    return f'<g filter="url(#{p}-glow)">' + ln(d, cls) + ln(f"M{x+210} {y+12} V{y+144}", cls, 3, 'stroke-dasharray="6 10"') + '</g>'

def hook(p, dur, lead):
    inner = (L.spot(p, 540, 880, 420, 300) + L.big(540, 520, "1 MILLION.", 96) + L.big(540, 625, "GLÜCKLICHER?", 84)
             + L.figure(p, 300, 1110, 1.1, "think") + ticket(p, 560, 800, p + "-tk")
             + f'<g class="{p}-l" opacity="0">{L.label(660, 890, "LOTTO", 40)}</g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = DRAW(f".{p}-tk", 0.2, 0.6) + f'tl.to(".{p}-l", {{opacity: 1, duration: 0.25}}, 0.7);'
    return S(p, inner), js

def loop(p, dur, lead):
    inner = (L.spot(p, 420, 900, 320, 300) + L.figure(p, 380, 1110, 1.15, "stand")
             + f'<g filter="url(#{p}-glow)">{ln("M600 640 H960 V1100 H600 Z", p+"-box")}</g>'
             + L.big(780, 900, "?", 200, p+"-q") + L.label(780, 1160, "AM ENDE: WAS WIRKT", 28, cls=p+"-end")
             + f'<path d="M80 1112 H560" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = DRAW(f".{p}-box", lead, 0.6) + IN(f".{p}-q", lead + 0.5) + IN(f".{p}-end", lead + (dur - lead) * 0.45)
    return S(p, inner), js

def bars(p, dur, lead):
    base, top = 1000, 680
    h1, h2 = (base - top) * 4.0 / 5, (base - top) * 3.82 / 5
    grid = "".join(f'<path d="M120 {base - (base-top)*k/5} H960" stroke="#fff" stroke-opacity=".18" stroke-width="2" stroke-dasharray="8 10"/>' for k in range(1, 6))
    inner = (L.spot(p, 540, 860, 400, 320) + ticket(p, 390, 420, p + "-tk")
             + L.label(540, 630, "1978 · 22 LOTTOGEWINNER", 28, op=.85, cls=p+"-src")
             + f'<path d="M120 {base} H960" {W} stroke-width="3" stroke-opacity=".8"/>' + grid
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-b1" x="250" y="{base - h1}" width="200" height="{h1}" rx="14" fill="#fff" style="transform-origin:350px {base}px"/>'
             + f'<rect id="{p}-b2" x="630" y="{base - h2}" width="200" height="{h2}" rx="14" {W} stroke-width="5" style="transform-origin:730px {base}px"/></g>'
             + L.big(350, base - h1 - 26, "4,0", 64, p+"-v1") + L.big(730, base - h2 - 26, "3,8", 64, p+"-v2")
             + L.label(350, base + 50, "GEWINNER", 28) + L.label(730, base + 50, "ANDERE", 28)
             + L.label(540, base + 95, "SKALA 0–5 · KAUM UNTERSCHIED", 28, op=.85, cls=p+"-note"))
    t1 = lead + (dur - lead) * 0.5; t2 = lead + (dur - lead) * 0.7
    js = (DRAW(f".{p}-tk", lead, 0.6) + IN(f".{p}-src", lead + 0.5)
          + f'tl.fromTo("#{p}-b1", {{scaleY: 0}}, {{scaleY: 1, duration: 0.7, ease: "power3.out"}}, {t1});' + IN(f".{p}-v1", t1 + 0.5)
          + f'tl.fromTo("#{p}-b2", {{scaleY: 0}}, {{scaleY: 1, duration: 0.7, ease: "power3.out"}}, {t2});' + IN(f".{p}-v2", t2 + 0.5)
          + IN(f".{p}-note", lead + (dur - lead) * 0.8))
    return S(p, inner), js

def treadmill(p, dur, lead):
    # happiness over time: spike at the win, decays back to the baseline
    curve = "M140 820 H330 C 360 820, 370 540, 400 540 C 470 540, 520 790, 640 805 C 720 815, 820 820, 940 820"
    inner = (L.spot(p, 540, 760, 440, 300)
             + f'<path d="M140 870 H960 M140 870 V500" {W} stroke-width="3" stroke-opacity=".8"/>'
             + '<path d="M140 820 H960" stroke="#fff" stroke-opacity=".35" stroke-width="2" stroke-dasharray="8 10"/>'
             + f'<g filter="url(#{p}-glow)">{ln(curve, p+"-c", 7)}</g>'
             + L.label(400, 505, "GEWINN", 28, cls=p+"-a") + L.label(740, 770, "WIEDER NORMAL", 28, cls=p+"-b")
             + L.label(860, 910, "ZEIT →", 28, op=.7)
             + L.label(540, 960, "MEHR GELD HILFT ETWAS –", 28, cls=p+"-h") + L.label(540, 1000, "WENIGER ALS GEDACHT", 28, cls=p+"-h")
)
    js = (DRAW(f".{p}-c", lead + 0.3, 2.2) + IN(f".{p}-a", lead + 1.0) + IN(f".{p}-b", lead + 2.4)
          + IN(f".{p}-h", lead + (dur - lead) * 0.6))
    return S(p, inner), js

def tip(p, dur, lead):
    steps = ["1 · ERLEBNISSE > DINGE", "2 · SCHÖNES MIT PAUSEN", "3 · SPEICHER DIR DAS"]
    inner = L.spot(p, 540, 820, 380, 300) + f'<g filter="url(#{p}-glow)">{ln("M110 540 H970 V1040 H110 Z", p+"-card")}</g>'
    for k, s_ in enumerate(steps):
        y = 660 + k * 120
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M160 {y-28} H216 V{y+28} H160 Z", p+f"-box{k}", 4)}{ln(f"M170 {y} L185 {y+16} L210 {y-18}", p+f"-tick{k}", 6)}</g>'
        inner += L.label(245, y + 10, s_, 30, "start", cls=p + f"-t{k}")
    inner += L.label(540, 1110, "1 MILLION. GLÜCKLICHER?", 30, cls=p+"-c")
    marks = [0.1, 0.4, 0.62]
    js = DRAW(f".{p}-card", lead, 0.5)
    for k in range(3):
        t = lead + (dur - lead) * marks[k]
        js += DRAW(f".{p}-box{k}", t, 0.25) + IN(f".{p}-t{k}", t + 0.1) + DRAW(f".{p}-tick{k}", t + 0.35, 0.25)
    js += IN(f".{p}-c", lead + (dur - lead) * 0.76)
    return S(p, inner), js

SCENES = {"hook": hook, "loop": loop, "bars": bars, "follow": follow, "treadmill": treadmill, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.7, 0.4), ("click-soft", 1, 0.5, 0.35), ("click-soft", 2, 0.6, 0.35),
       ("pop", 2, 7.2, 0.5), ("pop", 2, 9.6, 0.45), ("pop", 3, 1.1, 0.5), ("sparkle", 4, 1.0, 0.35), ("whoosh-short", 4, 2.4, 0.3),
       ("pop", 5, 1.3, 0.4), ("pop", 5, 4.6, 0.4), ("pop", 5, 7.1, 0.4)]
