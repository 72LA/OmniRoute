# AI72 #16 – Mythos-Check #5 "10.000 Schritte" (Paluch et al. 2022) – kg infographic, no character, retention system (hook A, ending 2)
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import SCENE_CSS
from scenes_knacken import pill
from scenes_vitc import S, T
import motion as M

FX = True
KEYS = {"10.000", "schritte", "werbung", "60ern", "japanische", "schrittzähler", "keine", "50.000", "nutzen", "flacht", "60", "6.000", "8.000", "jünger", "zahl"}
TITLES = {"pedo": "DIE HERKUNFT", "zero": "WISSENSCHAFT?", "crowd": "DIE STUDIE", "curve": "DAS ERGEBNIS", "marks": "DEINE ZIELZAHL", "end": "MYTHOS-CHECK #5"}

def foot(x, y, rot, cls):
    return (f'<g class="{cls}" transform="rotate({rot} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="26" ry="40" fill="#f1eefc"/>'
            + "".join(f'<circle cx="{x - 18 + i*10}" cy="{y - 50 + abs(i-2)*3}" r="7" fill="#f1eefc"/>' for i in range(5)) + '</g>')

def device(cx, cy, disp_id, val="0"):
    return (f'<rect x="{cx-170}" y="{cy-230}" width="340" height="460" rx="80" fill="{K.INK}" transform="translate(12 16)"/>'
            + K.shaded(K.rrect(cx - 170, cy - 230, 340, 460, 80), "#ff8c42", f"M{cx} {cy-240} H{cx+180} V{cy+240} H{cx} Z", "#e06d24")
            + f'<rect x="{cx-120}" y="{cy-150}" width="240" height="130" rx="22" fill="#1b2a1b"/>'
            + f'<text id="{disp_id}" x="{cx}" y="{cy-62}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="58" fill="#9dff8a">{val}</text>'
            + f'<circle cx="{cx}" cy="{cy+100}" r="44" fill="#ffd23f"/>')

def hook(p, dur, lead):
    feet = "".join(foot(150 + k * 120, 1040 - (k % 2) * 40, 80, f"{p}-ft") for k, _ in enumerate(range(7)))
    inner = feet
    sv, cam = S(p, inner, dur)
    html = sv + f'<div id="{p}-n" class="big" style="top:520px;font-size:230px">10.000</div>' + \
           f'<div id="{p}-tag" class="pill" style="left:560px;top:800px;width:380px;height:96px;line-height:96px;font-size:52px;background:{K.MAG};color:#fff;transform-origin:20% 0%">WERBUNG</div>'
    js = (cam + f'tl.fromTo("#{p}-tag", {{rotation: -14}}, {{rotation: 6, duration: 0.5, repeat: {int(dur/0.5)}, yoyo: true, ease: "sine.inOut"}}, 0);'
          + f'tl.fromTo(".{p}-ft", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.15, stagger: 0.14}}, 0.9);'
          + f'tl.fromTo("#{p}-n", {{scale: 1}}, {{scale: 1.05, duration: 0.25, repeat: 1, yoyo: true, ease: "sine.inOut"}}, 1.6);')
    return html, js

def pedo(p, dur, lead):
    span = dur - lead
    inner = f'<g id="{p}-dv">{device(540, 820, p + "-dp")}</g>'
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 160, 470, 360, "1960ER", K.Y, 40, 80) + pill(f"{p}-b", 560, 470, 360, "JAPAN", "#f1eefc", 40, 80) + \
           pill(f"{p}-c", 140, 1080, 800, "„10.000-SCHRITTE-ZÄHLER“", "#2ad4c0", 34, 76)
    js = (cam + f'tl.fromTo("#{p}-dv", {{y: 120, rotation: -10, svgOrigin: "540 820", opacity: 0}}, {{y: 0, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.4)"}}, {lead});'
          + M.count(f"{p}-dp", 0, 10000, lead + 0.4, span * 0.8) + M.pop(f"#{p}-a", lead + span * 0.15) + M.pop(f"#{p}-b", lead + span * 0.3)
          + M.pop(f"#{p}-c", lead + span * 0.62))
    return html, js

def zero(p, dur, lead):
    paper = (f'<rect x="300" y="600" width="480" height="460" rx="24" fill="#fff6e6"/>'
             + "".join(f'<rect x="350" y="{660 + k*60}" width="{380 - (k%2)*90}" height="18" rx="9" fill="#e9dcc4"/>' for k in range(6)))
    lens = f'<g id="{p}-lz"><circle cx="460" cy="760" r="90" fill="none" stroke="{K.INK}" stroke-width="22"/><path d="M525 825 l80 80" stroke="{K.INK}" stroke-width="28" stroke-linecap="round"/></g>'
    inner = paper + lens
    sv, cam = S(p, inner, dur)
    html = sv + f'<div id="{p}-z" class="big" style="top:440px;font-size:150px">0 STUDIEN</div>'
    js = (cam + f'tl.fromTo("#{p}-lz", {{x: -60, y: 0}}, {{x: 160, y: 120, duration: {dur}, ease: "sine.inOut"}}, 0);'
          + f'tl.fromTo("#{p}-z", {{scale: 1.6, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.3, ease: "power4.out"}}, {lead + 0.1});')
    return html, js

def crowd(p, dur, lead):
    span = dur - lead
    dots = "".join(f'<circle class="{p}-d" cx="{120 + (k % 24) * 36}" cy="{560 + (k // 24) * 36}" r="11" fill="{[K.MAG, "#2ad4c0", K.Y, "#7f6ff0"][k % 4]}"/>' for k in range(24 * 13))
    inner = dots + f'<text id="{p}-c" x="540" y="1110" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="80" fill="#fff">0</text>'
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-fol", 290, 372, 500, "+ FOLGEN @ai72", K.MAG, 32, 66, "#fff")
    js = (cam + f'tl.fromTo(".{p}-d", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.2, ease: "back.out(2)", stagger: {{each: 0.006, from: "center"}}}}, {lead});'
          + M.count(f"{p}-c", 0, 47471, lead + 0.2, span * 0.85)
          + f'tl.fromTo("#{p}-fol", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(2)"}}, {lead});tl.to("#{p}-fol", {{opacity: 0, duration: 0.25}}, {lead + 2.0});')
    return html, js

CURVE = "M150 1000 C 300 760, 420 640, 560 600 C 680 570, 820 560, 960 556"
def axes():
    return (f'<path d="M150 1000 H970 M150 1000 V520" stroke="#f1eefc" stroke-width="6" stroke-linecap="round"/>'
            + T(560, 1060, "SCHRITTE PRO TAG →", 28, "#f1eefc", 800) + T(150, 500, "NUTZEN", 28, "#f1eefc", 800, "start"))

def curve(p, dur, lead):
    span = dur - lead
    inner = axes() + f'<path id="{p}-cv" d="{CURVE}" fill="none" stroke="{K.Y}" stroke-width="14" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1;stroke-dashoffset:1"/>'
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-f", 600, 640, 340, "FLACHT AB", "#2ad4c0", 34, 72)
    js = cam + f'tl.to("#{p}-cv", {{strokeDashoffset: 0, duration: {span * 0.8}, ease: "power1.inOut"}}, {lead});' + M.pop(f"#{p}-f", lead + span * 0.7)
    return html, js

def marks(p, dur, lead):
    span = dur - lead
    inner = (axes() + f'<path d="{CURVE}" fill="none" stroke="{K.Y}" stroke-width="14" stroke-linecap="round"/>'
             + f'<rect id="{p}-b1" x="480" y="520" width="140" height="480" fill="{K.MAG}" opacity="0"/>'
             + f'<rect id="{p}-b2" x="620" y="520" width="140" height="480" fill="#2ad4c0" opacity="0"/>'
             + f'<circle id="{p}-m1" cx="550" cy="604" r="22" fill="{K.MAG}"/><circle id="{p}-m2" cx="690" cy="575" r="22" fill="#2ad4c0"/>')
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-a", 90, 1090, 440, "60+: 6–8 TSD.", K.MAG, 36, 80, "#fff") + pill(f"{p}-b", 550, 1090, 440, "JÜNGER: 8–10 TSD.", "#2ad4c0", 34, 80)
    js = (cam + f'tl.to("#{p}-b1", {{opacity: 0.3, duration: 0.4}}, {lead + 0.2});' + M.pop(f"#{p}-m1", lead + 0.2, "550 604") + M.pop(f"#{p}-a", lead + 0.4)
          + f'tl.to("#{p}-b2", {{opacity: 0.3, duration: 0.4}}, {lead + span * 0.55});' + M.pop(f"#{p}-m2", lead + span * 0.55, "690 575") + M.pop(f"#{p}-b", lead + span * 0.6)
          + M.pulse(f"#{p}-m1", "550 604", lead + 0.8, dur - lead - 0.8, 0.25) + M.pulse(f"#{p}-m2", "690 575", lead + span * 0.7, dur - lead - span * 0.7, 0.25))
    return html, js

def end(p, dur, lead):
    inner = f'<g id="{p}-dv">{device(540, 800, p + "-dp", "????")}</g>'
    sv, cam = S(p, inner, dur)
    html = sv + pill(f"{p}-q", 190, 1090, 700, "DEINE ZAHL HEUTE?", K.Y, 40, 84)
    js = (cam + f'tl.fromTo("#{p}-dp", {{opacity: 1}}, {{opacity: 0.25, duration: 0.35, repeat: {int(dur/0.35)}, yoyo: true, ease: "steps(1)"}}, 0);'
          + M.floaty(f"#{p}-dv", 0, dur, 10) + M.pop(f"#{p}-q", lead + 0.3))
    return html, js

SCENES = {"hook": hook, "pedo": pedo, "zero": zero, "crowd": crowd, "curve": curve, "marks": marks, "end": end}
SFX = [("click-soft", -1, 0.0, 0.14), ("pop", 1, 0.0, 0.12), ("pop", 1, 1.0, 0.12), ("pop", 1, 3.8, 0.12), ("pop", 2, 0.1, 0.13),
       ("sparkle", 3, 0.2, 0.11), ("whoosh-short", 4, 0.1, 0.11), ("pop", 4, 2.3, 0.12), ("pop", 5, 0.4, 0.12), ("pop", 5, 3.0, 0.12),
       ("chime", 6, 0.3, 0.1)]
