# AI72 #15 – Mythos-Check #4 "Macht Kälte krank?" (Johnson & Eccles 2005) – kg infographic, NO character, clean motion
import math, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import SCENE_CSS
from scenes_knacken import pill
from scenes_vitc import S, T, virus
import motion as M

FX = True
KEYS = {"kälte", "krank", "nicht", "direkt", "viren", "90", "20", "minuten", "füßen", "kaltem", "13", "5", "adern", "nase", "leichteres",
        "füße", "warm", "schick", "barfuß"}
TITLES = {"hook": "MYTHOS-CHECK #4", "feet": "DAS EXPERIMENT", "result": "DAS ERGEBNIS", "nose": "WAS PASSIERT", "tip": "SO SCHÜTZT DU DICH"}

def flakes(cls, n, seed, y0=420, y1=1100):
    r = random.Random(seed)
    return "".join(f'<g class="{cls}"><path d="M{x} {y-14} V{y+14} M{x-12} {y-7} L{x+12} {y+7} M{x-12} {y+7} L{x+12} {y-7}" stroke="#bfeaff" stroke-width="4" stroke-linecap="round" opacity=".8"/></g>'
                   for x, y in [(r.randint(70, 1010), r.randint(y0, y1)) for _ in range(n)])

def grid(cls, x0, y0, n_hi, col_hi, cols=10, rows=9, step=34, r=11):
    s = ""
    for k in range(cols * rows):
        cx, cy = x0 + (k % cols) * step, y0 + (k // cols) * step
        hi = k < n_hi
        s += f'<circle class="{cls}{" " + cls + "-hi" if hi else ""}" cx="{cx}" cy="{cy}" r="{r}" fill="{"#5b4fb5" if not hi else "#5b4fb5"}" data-hi="{1 if hi else 0}"/>'
    return s

def hook(p, dur, lead):
    span = dur - lead
    vs = "".join(f'<g class="{p}-v{k}">{virus(f"{p}-vv", x, y, rr, col)}</g>' for k, (x, y, rr, col) in enumerate([(250, 820, 46, K.MAG), (820, 760, 34, "#2ad4c0"), (640, 960, 26, K.MAG)]))
    therm = (f'<g id="{p}-th"><rect x="470" y="640" width="70" height="300" rx="35" fill="#f1eefc"/><circle cx="505" cy="950" r="55" fill="{K.BLU}"/>'
             f'<rect x="490" y="760" width="30" height="190" rx="15" fill="{K.BLU}"/></g>')
    inner = flakes(f"{p}-fl", 16, 3) + therm + vs
    sv, cam = S(p, inner, dur)
    html = sv + '<div class="rule">— AI72 ERKLÄRT —</div>' + f'<div id="{p}-card" class="card" style="top:450px;font-size:54px">Macht Kälte krank?</div>' + \
           pill(f"{p}-n", 240, 1060, 600, "NICHT DIREKT …", "#f1eefc", 34, 76)
    t1 = lead + span * 0.35; t2 = lead + span * 0.62
    js = (cam + f'tl.fromTo("#{p}-card", {{scale: 0.9, opacity: 1}}, {{scale: 1, duration: 0.5, ease: "expo.out"}}, 0.05);'
          + f'tl.fromTo(".{p}-fl", {{y: -80}}, {{y: 220, duration: {dur}, ease: "none", stagger: 0.05}}, 0);'
          + "".join(M.spin(f".{p}-v{k}", o, dur, 50 if k % 2 == 0 else -50) for k, o in enumerate(["250 820", "820 760", "640 960"]))
          + f'tl.fromTo(".{p}-vv", {{scale: 0.55, transformOrigin: "50% 50%", opacity: 0.5}}, {{scale: 0.7, opacity: 0.7, duration: 0.6}}, 0);'
          + M.pop(f"#{p}-th", 0.3, "505 800") + M.pop(f"#{p}-n", t1)
          + f'tl.to(".{p}-vv", {{scale: 1.25, opacity: 1, duration: 0.6, ease: "back.out(2)", stagger: 0.08}}, {t2});'
          + f'tl.to("#{p}-th", {{opacity: 0.25, duration: 0.4}}, {t2});')
    return html, js

def feet(p, dur, lead):
    span = dur - lead
    tub = (f'<path d="M260 900 H820 L780 1060 Q770 1090 740 1090 H340 Q310 1090 300 1060 Z" fill="{K.INK}" transform="translate(10 12)"/>'
           f'<path d="M260 900 H820 L780 1060 Q770 1090 740 1090 H340 Q310 1090 300 1060 Z" fill="#46a6ff"/>'
           f'<path id="{p}-wave" d="M280 930 q35 -18 70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0" stroke="#bfeaff" stroke-width="8" fill="none" stroke-linecap="round"/>')
    foot = lambda x: (f'<g class="{p}-ft"><rect x="{x}" y="700" width="90" height="230" rx="44" fill="#ffb3c2"/>'
                      f'<rect x="{x+48}" y="700" width="42" height="230" rx="21" fill="#ec8aa0"/></g>')
    clock = (f'<g id="{p}-ck"><circle cx="880" cy="640" r="80" fill="#f1eefc"/><circle cx="880" cy="640" r="80" fill="none" stroke="#cfc6f5" stroke-width="10"/>'
             f'<path id="{p}-arc" d="M880 568 A72 72 0 1 1 879.9 568" fill="none" stroke="{K.MAG}" stroke-width="14" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1;stroke-dashoffset:1"/>'
             + T(880, 655, "20′", 44, K.INK) + '</g>')
    inner = grid(f"{p}-d", 120, 480, 0, K.MAG, cols=15, rows=6, step=24, r=8) + tub + foot(420) + foot(560) + clock
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-n", 120, 640, 300, "90 MENSCHEN", K.Y, 32, 70)
    tf = lead + span * 0.35
    js = (cam + f'tl.fromTo(".{p}-d", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.25, ease: "back.out(2)", stagger: 0.008}}, {lead});'
          + M.pop(f"#{p}-n", lead + 0.5)
          + f'tl.fromTo(".{p}-ft", {{y: -200, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.7, ease: "power3.out", stagger: 0.12}}, {tf});'
          + f'tl.fromTo("#{p}-wave", {{x: -20}}, {{x: 20, duration: 0.8, repeat: {int(dur/0.8)}, yoyo: true, ease: "sine.inOut"}}, 0);'
          + M.pop(f"#{p}-ck", lead + span * 0.6, "880 640")
          + f'tl.to("#{p}-arc", {{strokeDashoffset: 0, duration: 1.2, ease: "power1.inOut"}}, {lead + span * 0.65});')
    return html, js

def result(p, dur, lead):
    span = dur - lead
    gl = grid(f"{p}-l", 150, 560, 13, K.MAG); gr = grid(f"{p}-r", 620, 560, 5, "#2ad4c0")
    inner = (f'<rect x="120" y="520" width="370" height="360" rx="30" fill="#2a1f86"/><rect x="590" y="520" width="370" height="360" rx="30" fill="#2a1f86"/>' + gl + gr
             + T(305, 940, "KALTE FÜSSE", 28, "#fff", 800) + T(775, 940, "OHNE", 28, "#fff", 800)
             + f'<text id="{p}-cl" x="305" y="510" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="{K.MAG}">0</text>'
             + f'<text id="{p}-cr" x="775" y="510" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="#2ad4c0">0</text>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-s", 290, 990, 500, "SELBST GEMELDET", "#f1eefc", 28, 62) + pill(f"{p}-fol", 290, 372, 500, "+ FOLGEN @ai72", K.MAG, 32, 66, "#fff")
    t1 = lead + 0.3; t2 = lead + span * 0.55
    js = (cam + f'tl.fromTo(".{p}-l, .{p}-r", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.2, ease: "back.out(2)", stagger: 0.004}}, {lead});'
          + f'tl.to(".{p}-l-hi", {{fill: "{K.MAG}", scale: 1.25, transformOrigin: "50% 50%", duration: 0.25, stagger: 0.06}}, {t1 + 0.6});'
          + M.count(f"{p}-cl", 0, 13, t1 + 0.6, 0.9)
          + f'tl.to(".{p}-r-hi", {{fill: "#2ad4c0", scale: 1.25, transformOrigin: "50% 50%", duration: 0.25, stagger: 0.08}}, {t2});'
          + M.count(f"{p}-cr", 0, 5, t2, 0.5) + M.pop(f"#{p}-s", lead + span * 0.8)
          + f'tl.fromTo("#{p}-fol", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(2)"}}, {lead});tl.to("#{p}-fol", {{opacity: 0, duration: 0.25}}, {lead + 2.0});')
    return html, js

def nose(p, dur, lead):
    span = dur - lead
    nose_d = "M420 560 C 420 700, 360 820, 330 900 C 320 930, 350 960, 400 960 L 560 960 C 600 960, 620 930, 600 900"
    vessels = "".join(f'<path class="{p}-ves" d="M{380 + k*40} 900 C {400 + k*40} 820, {430 + k*30} 720, {450 + k*20} 640" stroke="#ff4a4a" stroke-width="16" fill="none" stroke-linecap="round"/>' for k in range(4))
    vs = "".join(virus(f"{p}-vi", x, y, 18, K.MAG) for x, y in [(640, 780), (700, 880), (600, 680)])
    cold = "".join(f'<path class="{p}-cd" d="M{980} {640 + k*90} h-160" stroke="#7fd8ff" stroke-width="12" stroke-linecap="round" opacity="0"/>' for k in range(4))
    inner = (f'<rect x="250" y="520" width="580" height="500" rx="60" fill="#2a1f86"/>'
             + f'<path d="{nose_d}" fill="none" stroke="#ffb3c2" stroke-width="18" stroke-linecap="round"/>' + vessels + vs + cold
             + T(540, 580, "IN DER NASE", 30, "#fff", 900))
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 150, 450, 340, "VERMUTUNG", "#f1eefc", 30, 62) + pill(f"{p}-b", 560, 1060, 380, "ADERN ENG", "#7fd8ff", 32, 70) + \
           pill(f"{p}-c", 140, 1060, 380, "VIREN AKTIV", K.MAG, 32, 70, "#fff")
    tc = lead + span * 0.22; tv = lead + span * 0.55
    js = (cam + M.pop(f"#{p}-a", lead)
          + f'tl.to(".{p}-cd", {{opacity: 1, x: -60, duration: 0.6, ease: "power2.out", stagger: 0.1}}, {tc});'
          + f'tl.to(".{p}-ves", {{attr: {{"stroke-width": 6}}, duration: 0.9, ease: "power2.inOut", stagger: 0.08}}, {tc + 0.4});'
          + M.pop(f"#{p}-b", tc + 0.6)
          + f'tl.fromTo(".{p}-vi", {{scale: 0.6, transformOrigin: "50% 50%"}}, {{scale: 1.3, duration: 0.5, ease: "back.out(2.2)", stagger: 0.1}}, {tv});'
          + M.pop(f"#{p}-c", tv + 0.3))
    return html, js

def tip(p, dur, lead):
    span = dur - lead
    sock = lambda x, c: (f'<g class="{p}-sk"><path d="M{x} 640 h110 v230 q0 60 -60 60 h-90 q-40 0 -40 -40 q0 -40 40 -40 h40 Z" fill="{c}"/>'
                         f'<rect x="{x}" y="640" width="110" height="40" fill="#fff" opacity=".5"/></g>')
    glow = f'<circle id="{p}-gw" cx="540" cy="800" r="230" fill="#ff8c42" opacity="0"/>'
    inner = glow + sock(380, K.ORA) + sock(560, K.Y)
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 290, 470, 500, "FÜSSE WARM", K.Y, 38, 80) + pill(f"{p}-b", 120, 1010, 840, "SCHICK'S DEM BARFUSS-LÄUFER", "#f1eefc", 32, 72) + \
           pill(f"{p}-q", 290, 1100, 500, "MACHT KÄLTE KRANK?", "#2ad4c0", 28, 60)
    js = (cam + M.pop(f"#{p}-a", lead)
          + f'tl.fromTo(".{p}-sk", {{y: -160, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.7, ease: "back.out(1.4)", stagger: 0.15}}, {lead + 0.2});'
          + f'tl.to("#{p}-gw", {{opacity: 0.35, duration: 0.8}}, {lead + 0.8});' + M.pulse(f"#{p}-gw", "540 800", lead + 1.0, dur - lead - 1.0, 0.08)
          + M.pop(f"#{p}-b", lead + span * 0.45) + M.pop(f"#{p}-q", lead + span * 0.82))
    return html, js

SCENES = {"hook": hook, "feet": feet, "result": result, "nose": nose, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.16), ("click-soft", 0, 1.4, 0.12), ("pop", 0, 2.5, 0.13), ("click-soft", 1, 0.0, 0.11),
       ("pop", 1, 1.6, 0.12), ("click-soft", 2, 0.9, 0.12), ("pop", 2, 2.4, 0.12), ("whoosh-short", 3, 1.3, 0.11), ("pop", 3, 3.4, 0.12),
       ("pop", 4, 0.1, 0.12), ("chime", 4, 3.4, 0.11)]
