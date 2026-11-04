# malangenommen72 #10 – "Innen sind wir uns ähnlicher" (gegen Rassismus, hoffnungsvoll) – Dark v2.
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import S, IN, DRAW, ln, follow, SCENE_CSS

W = L.W
KEYS = {"innen", "99,9", "%", "gleich.", "vorurteile", "innerhalb", "@malangenommen72", "verändert.", "verlernen.", "500",
        "kennenlernt,", "weniger", "zu.", "kennen,", "ähnlicher,"}
TITLES = {"hook": "MAL ANGENOMMEN …", "dna": "FAST GLEICH", "within": "WO DIE UNTERSCHIEDE SIND", "learn": "GELERNT = VERLERNBAR",
          "contact": "WAS WIRKLICH HILFT", "tip": "SO FÄNGST DU AN"}

def row(p, n, y, s, cls, x0=140, x1=940):
    step = (x1 - x0) / (n - 1)
    return "".join(f'<g class="{cls}">' + L.figure(p, x0 + i * step, y, s, "stand") + '</g>' for i in range(n))

def hook(p, dur, lead):
    inner = (L.spot(p, 540, 900, 460, 300) + L.big(540, 520, "ALLE MENSCHEN.", 80) + L.big(540, 615, "VON INNEN.", 80)
             + row(p, 5, 1100, 0.85, p + "-f") + f'<path d="M60 1102 H1020" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = f'tl.fromTo(".{p}-f", {{opacity: 0.25}}, {{opacity: 1, duration: 0.4, stagger: 0.15}}, 0.2);'
    return S(p, inner), js

def dna(p, dur, lead):
    pts1, pts2, rungs = [], [], ""
    for k in range(41):
        y = 560 + k * 13; x = 540 + 120 * math.sin(k / 3.2)
        pts1.append(f"{'M' if k == 0 else 'L'}{x:.0f} {y}"); pts2.append(f"{'M' if k == 0 else 'L'}{1080 - x:.0f} {y}")
        if k % 3 == 0: rungs += f'<path d="M{x:.0f} {y} H{1080 - x:.0f}" stroke="#fff" stroke-opacity=".45" stroke-width="3"/>'
    inner = (L.spot(p, 540, 800, 300, 320) + f'<g filter="url(#{p}-glow)">' + ln(" ".join(pts1), p + "-h1") + ln(" ".join(pts2), p + "-h2") + '</g>'
             + f'<g class="{p}-r" opacity="0">{rungs}</g>' + L.big(540, 500, "99,9 % GLEICH", 84, p + "-v"))
    js = (DRAW(f".{p}-h1", lead, 1.0) + DRAW(f".{p}-h2", lead + 0.1, 1.0) + f'tl.to(".{p}-r", {{opacity: 1, duration: 0.4}}, {lead + 0.9});'
          + IN(f".{p}-v", lead + 1.6))
    return S(p, inner), js

def within(p, dur, lead):
    r = random.Random(3)
    dots = ""
    for g, cx in enumerate((330, 750)):
        for _ in range(26):
            a = r.uniform(0, 6.28); d = r.uniform(0, 150)
            dots += f'<circle class="{p}-d" cx="{cx + d*math.cos(a):.0f}" cy="{800 + d*math.sin(a):.0f}" r="{r.choice([8, 11, 14])}" fill="#fff" opacity="{r.uniform(.5, 1):.2f}"/>'
    inner = (L.spot(p, 540, 800, 420, 280)
             + f'<g filter="url(#{p}-glow)">{ln("M330 800 m-190 0 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0", p+"-c1", 4)}{ln("M750 800 m-190 0 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0", p+"-c2", 4)}</g>'
             + dots + L.label(330, 1050, "GRUPPE A", 28) + L.label(750, 1050, "GRUPPE B", 28)
             + L.label(540, 1110, "~85 % DER VIELFALT: INNERHALB", 28, cls=p+"-t"))
    js = (DRAW(f".{p}-c1", lead, 0.5) + DRAW(f".{p}-c2", lead + 0.2, 0.5)
          + f'tl.fromTo(".{p}-d", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.25, stagger: 0.02, ease: "back.out(1.6)"}}, {lead + 0.4});'
          + IN(f".{p}-t", lead + (dur - lead) * 0.55))
    return S(p, inner), js

def learn(p, dur, lead):
    inner = (L.spot(p, 540, 840, 400, 300)
             + f'<g filter="url(#{p}-glow)">{ln("M150 650 H460 V1000 H150 Z M150 720 H460", p+"-b1")}{ln("M620 650 H930 V1000 H620 Z M620 720 H930", p+"-b2")}'
             + ln("M480 825 H600 M570 795 L600 825 L570 855", p+"-ar") + '</g>'
             + L.label(305, 700, "GELERNT", 30) + L.label(775, 700, "VERLERNT", 30)
             + L.big(305, 880, "SEHEN", 50) + L.big(305, 950, "HÖREN", 50)
             + f'<g class="{p}-x" opacity="0">{L.big(775, 900, "OFFEN", 60)}</g>')
    t2 = lead + (dur - lead) * 0.55
    js = DRAW(f".{p}-b1", lead, 0.6) + DRAW(f".{p}-ar", t2 - 0.4, 0.4) + DRAW(f".{p}-b2", t2, 0.6) + f'tl.to(".{p}-x", {{opacity: 1, duration: 0.3}}, {t2 + 0.5});'
    return S(p, inner), js

def contact(p, dur, lead):
    inner = (L.spot(p, 540, 880, 380, 300)
             + f'<g class="{p}-a">' + L.figure(p, 300, 1100, 1.05, "point") + '</g>'
             + f'<g class="{p}-b"><g transform="translate(1080 0) scale(-1 1)">' + L.figure(p, 300, 1100, 1.05, "point") + '</g></g>'
             + f'<path d="M60 1102 H1020" {W} stroke-width="3" stroke-opacity=".7"/>'
             + f'<g class="{p}-h" opacity="0">{L.big(540, 760, "♥", 90)}</g>'
             + L.label(540, 600, "515 STUDIEN · 38 LÄNDER", 30, cls=p+"-src")
             + L.label(540, 1160, "VORURTEILE MEIST ↓", 30, cls=p+"-t"))
    js = (IN(f".{p}-src", lead + 0.3)
          + f'tl.fromTo(".{p}-a", {{x: -180}}, {{x: 0, duration: 1.4, ease: "power2.out"}}, {lead + 1.2});'
          + f'tl.fromTo(".{p}-b", {{x: 180}}, {{x: 0, duration: 1.4, ease: "power2.out"}}, {lead + 1.2});'
          + f'tl.to(".{p}-h", {{opacity: 1, duration: 0.3}}, {lead + 2.8});' + IN(f".{p}-t", lead + (dur - lead) * 0.65))
    return S(p, inner), js

def tip(p, dur, lead):
    steps = ["1 · KENNENLERNEN", "2 · ZUHÖREN", "3 · WIDERSPRECHEN"]
    inner = L.spot(p, 540, 820, 380, 300) + f'<g filter="url(#{p}-glow)">{ln("M180 540 H900 V1040 H180 Z", p+"-card")}</g>'
    for k, s_ in enumerate(steps):
        y = 660 + k * 120
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M240 {y-28} H296 V{y+28} H240 Z", p+f"-box{k}", 4)}{ln(f"M250 {y} L265 {y+16} L290 {y-18}", p+f"-tick{k}", 6)}</g>'
        inner += L.label(330, y + 10, s_, 30, "start", cls=p + f"-t{k}")
    inner += L.label(540, 1110, "INNEN SIND WIR UNS ÄHNLICH", 30, cls=p+"-c")
    marks = [0.12, 0.3, 0.45]
    js = DRAW(f".{p}-card", lead, 0.5)
    for k in range(3):
        t = lead + (dur - lead) * marks[k]
        js += DRAW(f".{p}-box{k}", t, 0.25) + IN(f".{p}-t{k}", t + 0.1) + DRAW(f".{p}-tick{k}", t + 0.35, 0.25)
    js += IN(f".{p}-c", lead + (dur - lead) * 0.72)
    return S(p, inner), js

SCENES = {"hook": hook, "dna": dna, "within": within, "follow": follow, "learn": learn, "contact": contact, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.45), ("sparkle", 1, 1.6, 0.35), ("click-soft", 2, 0.4, 0.3), ("pop", 3, 1.1, 0.45),
       ("click-soft", 4, 3.4, 0.35), ("sparkle", 5, 2.8, 0.35), ("pop", 6, 1.3, 0.35), ("pop", 6, 3.0, 0.35), ("pop", 6, 4.4, 0.35)]
