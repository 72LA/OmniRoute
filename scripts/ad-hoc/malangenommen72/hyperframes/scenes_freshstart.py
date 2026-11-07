# malangenommen72 #17 – Fresh-Start-Effekt (Dai, Milkman & Riis 2014) – Dark v2, retention system (hook D, ending 3)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import IN, DRAW, ln, SCENE_CSS
from scenes_motivation import tbox
from scenes_peakend import S
import motion as M

W = L.W; FX = True
KEYS = {"montag", "6", "neu", "wieder", "selbstbetrug", "gym-besuche", "diät-suchen", "ziele", "neuanfang", "geburtstag", "neues", "ich", "tag", "irgendwann", "witz", "neujahr"}
TITLES = {"twist": "KEIN SELBSTBETRUG", "data": "DIE DATEN", "spikes": "JEDES MAL", "self": "WARUM?", "trick": "DER TRICK", "end": "UND DU?"}

def cal(p, x, y, txt, cls, s=1.0):
    w, h = 220 * s, 240 * s
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{18*s}" fill="#000" stroke="#fff" stroke-width="5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{60*s}" rx="{18*s}" fill="#fff"/>' + L.big(x + w / 2, y + h * 0.72, txt, int(86 * s)) + '</g>')

def hook(p, dur, lead):
    inner = (L.spot(p, 540, 880, 420, 300, p + "-sp")
             + cal(p, 600, 650, "MO", p + "-c3", 1.0) + cal(p, 620, 630, "MO", p + "-c2", 1.0) + cal(p, 640, 610, "MO", p + "-c1", 1.0)
             + L.big(330, 760, "06:00", 120, p + "-clk")
             + f'<g class="{p}-guy">{L.figure(p, 300, 1110, 1.0, "stand")}</g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>'
             + f'<g class="{p}-start" opacity="0"><path d="M380 1112 V1040" stroke="#fff" stroke-width="6"/>{L.label(380, 1020, "START", 22)}</g>')
    sv, cam = S(p, inner, dur)
    js = (cam + f'tl.fromTo(".{p}-clk", {{scale: 1}}, {{scale: 1.06, svgOrigin: "330 720", duration: 0.12, repeat: 7, yoyo: true, ease: "sine.inOut"}}, 0);'
          + f'tl.to(".{p}-start", {{opacity: 1, duration: 0.2}}, 1.0);'
          + f'tl.fromTo(".{p}-guy", {{x: 0}}, {{x: 120, duration: 0.6, ease: "power2.out"}}, 1.1);'
          + f'tl.fromTo(".{p}-c2", {{x: 0, y: 0}}, {{x: -40, y: 30, duration: 0.3, ease: "back.out(2)"}}, 2.0);'
          + f'tl.fromTo(".{p}-c3", {{x: 0, y: 0}}, {{x: -80, y: 60, duration: 0.3, ease: "back.out(2)"}}, 2.3);')
    return sv, js

def twist(p, dur, lead):
    inner = L.spot(p, 540, 820, 420, 300) + tbox(170, 690, 740, ["SELBSTBETRUG?"], 70) + ln("M200 760 L880 790", p + "-x", 12)
    sv, cam = S(p, inner, dur)
    return sv, cam + DRAW(f".{p}-x", lead + (dur - lead) * 0.45, 0.25)

def data(p, dur, lead):
    span = dur - lead
    icons = [("M170 840 h40 v-60 h30 v160 h-30 v-60 h-40 Z M240 820 h120 v40 h-120 Z M360 780 h30 v160 h-30 Z M390 840 h40 v40 h-40 Z", 300, "GYM"),
             ("M510 760 a70 70 0 1 0 0.1 0 M590 890 l60 60", 540, "DIÄT-SUCHE"),
             ("M780 960 V740 M780 750 h130 l-30 45 l30 45 h-130", 840, "ZIELE")]
    inner = L.spot(p, 540, 840, 440, 300)
    js = ""
    for k, (d, cx, lab) in enumerate(icons):
        inner += f'<g class="{p}-i{k}"><g filter="url(#{p}-glow)">{ln(d, p + f"-d{k}", 7)}</g>{L.label(cx, 1020, lab, 26)}</g>'
        t = lead + span * (0.1 + k * 0.25)
        js += M.rise(f".{p}-i{k}", t, 0.5) + DRAW(f".{p}-d{k}", t, 0.5)
    sv, cam = S(p, inner, dur)
    return sv, cam + js

def spikes(p, dur, lead):
    span = dur - lead; base = 980
    curve = ("M120 980 H260 C 290 980, 300 760, 330 760 C 360 760, 380 960, 430 970 H500 C 530 970, 545 700, 575 700 C 605 700, 625 950, 680 965 H750"
             " C 780 965, 795 620, 830 620 C 865 620, 885 950, 960 960")
    inner = (L.spot(p, 540, 820, 460, 320) + f'<path d="M120 {base} H960" {W} stroke-width="3" stroke-opacity=".8"/>'
             + f'<g filter="url(#{p}-glow)">{ln(curve, p + "-c", 7)}</g>'
             + L.label(330, 1040, "WOCHE", 24, cls=p + "-l0") + L.label(575, 1040, "MONAT", 24, cls=p + "-l1") + L.label(830, 1040, "GEBURTSTAG", 24, cls=p + "-l2")
             + f'<g class="{p}-fol" opacity="0"><rect x="200" y="390" width="680" height="64" rx="32" fill="#fff"/>'
             + f'<text x="540" y="433" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="28" fill="#000">+ FOLGEN @malangenommen72</text></g>')
    sv, cam = S(p, inner, dur)
    js = (cam + DRAW(f".{p}-c", lead + 0.2, span * 0.85)
          + "".join(IN(f".{p}-l{k}", lead + 0.2 + span * 0.85 * f) for k, f in enumerate((0.25, 0.55, 0.85)))
          + f'tl.to(".{p}-fol", {{opacity: 1, duration: 0.3}}, {lead});tl.to(".{p}-fol", {{opacity: 0, duration: 0.3}}, {lead + 2.2});')
    return sv, js

def self_(p, dur, lead):
    span = dur - lead
    inner = (L.spot(p, 640, 900, 360, 300) + f'<path d="M540 640 V1112" stroke="#fff" stroke-width="4" stroke-dasharray="14 12" opacity=".7"/>'
             + f'<g opacity=".28">{L.figure(p, 380, 1110, 1.1, "stand")}</g>'
             + f'<g class="{p}-new">{L.figure(p, 380, 1110, 1.1, "wave")}</g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>'
             + L.label(380, 600, "GESTERN", 26, op=.6) + L.label(760, 600, "NEUES ICH", 30, cls=p + "-l"))
    sv, cam = S(p, inner, dur)
    js = cam + f'tl.fromTo(".{p}-new", {{x: 0}}, {{x: 380, duration: 1.1, ease: "power3.inOut"}}, {lead + span * 0.35});' + IN(f".{p}-l", lead + span * 0.6)
    return sv, js

def trick(p, dur, lead):
    span = dur - lead
    letters = "IRGENDWANN"
    inner = L.spot(p, 540, 840, 420, 300)
    for k, ch in enumerate(letters):
        inner += f'<g class="{p}-ch{k}">{L.big(250 + k * 64, 700, ch, 70)}</g>'
    inner += cal(p, 430, 820, "MO", p + "-cal", 1.0) + f'<g filter="url(#{p}-glow)">{ln("M540 790 a150 150 0 1 0 0.1 0", p + "-ring", 6)}</g>'
    sv, cam = S(p, inner, dur); tf = lead + span * 0.45
    js = cam + "".join(f'tl.to(".{p}-ch{k}", {{y: 420, rotation: {(-1) ** k * 25}, svgOrigin: "{250 + k*64} 700", opacity: 0, duration: 0.8, ease: "power2.in"}}, {tf + k * 0.04});' for k in range(len(letters)))
    js += M.pop(f".{p}-cal", lead + 0.1, "540 940") + DRAW(f".{p}-ring", tf + 0.5, 0.5)
    return sv, js

def end(p, dur, lead):
    beam = f'<g class="{p}-beam"><path d="M240 800 H840" stroke="#fff" stroke-width="8"/>' + \
           f'<path d="M240 800 l-60 140 h120 Z M840 800 l-60 140 h120 Z" fill="none" stroke="#fff" stroke-width="5"/>' + \
           L.label(240, 990, "MONTAG", 28) + L.label(840, 990, "NEUJAHR", 28) + '</g>'
    inner = (L.spot(p, 540, 860, 420, 300) + f'<path d="M540 800 V1100 M440 1100 H640" stroke="#fff" stroke-width="8"/>' + beam
             + L.label(540, 640, "WORAUF WARTEST DU?", 30, cls=p + "-q"))
    sv, cam = S(p, inner, dur)
    js = (cam + f'tl.fromTo(".{p}-beam", {{rotation: -7, svgOrigin: "540 800"}}, {{rotation: 7, duration: 0.9, repeat: {int(dur / 0.9)}, yoyo: true, ease: "sine.inOut"}}, 0);'
          + IN(f".{p}-q", lead + 0.3))
    return sv, js

SCENES = {"hook": hook, "twist": twist, "data": data, "spikes": spikes, "self": self_, "trick": trick, "end": end}
SFX = [("click-soft", -1, 0.0, 0.14), ("click-soft", 0, 2.0, 0.12), ("click-soft", 0, 2.3, 0.12), ("whoosh-short", 1, 0.6, 0.12),
       ("pop", 2, 0.4, 0.12), ("pop", 2, 1.3, 0.12), ("pop", 2, 2.2, 0.12), ("sparkle", 3, 4.6, 0.11), ("whoosh-short", 4, 1.3, 0.11),
       ("whoosh-short", 5, 1.6, 0.11), ("chime", 6, 0.4, 0.1)]
