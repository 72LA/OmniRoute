# malangenommen72 #16 – "Warum denkst du nach Gesprächen, dass sie dich nicht mochten?" (Boothby et al. 2018, Liking Gap) – Dark v2, clean motion
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import IN, DRAW, ln, SCENE_CSS
from scenes_motivation import tbox
from scenes_peakend import S
import motion as M

W = L.W; FX = True
KEYS = {"gesprächen", "mochten", "falsch", "5", "mehr", "glaubten", "mitbewohner", "monatelang", "sympathie-lücke", "grübeln", "schick", "zerdenkt"}
TITLES = {"hook": "MAL ANGENOMMEN …", "twist": "DEIN KOPF LÜGT", "gap": "5 STUDIEN", "name": "SYMPATHIE-LÜCKE", "tip": "SO GEHT'S BESSER"}

def hook(p, dur, lead):
    cloud = "M300 700 q-60 0 -60 -55 q0 -55 60 -55 q15 -45 70 -40 q45 -40 95 0 q60 -5 60 55 q50 10 40 60 q-5 40 -55 40 Z"
    inner = (L.spot(p, 540, 940, 420, 300, p + "-sp") + tbox(110, 455, 860, ["NACH DEM GESPRÄCH:", "„SIE MOCHTEN MICH NICHT?“"], 54)
             + f'<g class="{p}-me">{L.figure(p, 330, 1110, 1.05, "think")}</g>'
             + f'<g class="{p}-you"><g transform="translate(1080 0) scale(-1 1)">{L.figure(p, 300, 1110, 1.05, "stand")}</g></g>'
             + f'<g class="{p}-cl"><g transform="translate(0 110)"><g filter="url(#{p}-glow)">{ln(cloud, p + "-c", 5)}</g>{L.big(345, 690, "?", 90, p + "-q")}</g></g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>')
    sv, cam = S(p, inner, dur)
    js = (cam + DRAW(f".{p}-c", 0.15, 0.6) + IN(f".{p}-q", 0.5) + M.floaty(f".{p}-cl", 0.8, dur, 7)
          + f'tl.to(".{p}-you", {{x: 160, opacity: 0.35, duration: {dur - 0.4}, ease: "power1.inOut"}}, 0.4);'
          + M.pulse(f".{p}-sp", "540 940", 0, dur, 0.05))
    return sv, js

def twist(p, dur, lead):
    head = "M540 560 a200 200 0 1 0 0.1 0"
    inner = (L.spot(p, 540, 760, 360, 320) + f'<g filter="url(#{p}-glow)">{ln(head, p + "-hd", 6)}'
             + ln("M450 700 q20 -20 40 0 M590 700 q20 -20 40 0 M460 830 q80 -50 160 0", p + "-fc", 6) + '</g>'
             + f'<g class="{p}-st" opacity="0"><rect x="330" y="700" width="420" height="120" rx="14" fill="none" stroke="#fff" stroke-width="8"/>'
             + L.big(540, 790, "FALSCH", 86) + '</g>')
    sv, cam = S(p, inner, dur)
    t = lead + (dur - lead) * 0.45
    js = (cam + DRAW(f".{p}-hd", lead, 0.6) + DRAW(f".{p}-fc", lead + 0.4, 0.5)
          + f'tl.fromTo(".{p}-st", {{opacity: 0, scale: 1.8, rotation: -14, svgOrigin: "540 760"}}, {{opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power4.out"}}, {t});')
    return sv, js

def gap(p, dur, lead):
    span = dur - lead; base = 1030
    dots = "".join(f'<circle class="{p}-d" cx="{340 + k*100}" cy="560" r="20" fill="#fff"/>' for k in range(5))
    inner = (L.spot(p, 540, 820, 440, 320) + dots
             + f'<path d="M150 {base} H930" {W} stroke-width="3" stroke-opacity=".8"/>'
             + "".join(f'<path d="M150 {base - k*90} H930" stroke="#fff" stroke-opacity=".12" stroke-width="2" stroke-dasharray="6 10"/>' for k in range(1, 5))
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-g" x="230" y="{base-140}" width="200" height="140" rx="14" {W} stroke-width="5"/>'
             + f'<rect id="{p}-r" x="650" y="{base-340}" width="200" height="340" rx="14" fill="#fff"/></g>'
             + L.label(330, base + 48, "DEIN TIPP", 26) + L.label(750, base + 48, "IN WAHRHEIT", 26)
             + f'<g class="{p}-mo" opacity="0"><g filter="url(#{p}-glow)">{ln("M900 590 h110 v95 h-110 Z M900 620 h110", p + "-cal", 4)}</g>{L.label(955, 725, "MONATE", 20)}</g>'
             + f'<g class="{p}-fol" opacity="0"><rect x="200" y="390" width="680" height="64" rx="32" fill="#fff"/>'
             + f'<text x="540" y="433" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="28" fill="#000">+ FOLGEN @malangenommen72</text></g>')
    sv, cam = S(p, inner, dur); tb = lead + span * 0.32
    js = (cam + f'tl.fromTo(".{p}-d", {{scale: 0, transformOrigin: "50% 50%"}}, {{scale: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.1}}, {lead});'
          + M.grow(f"#{p}-g", f"330 {base}", tb, 0.7) + M.grow(f"#{p}-r", f"750 {base}", tb + 0.5, 1.0)
          + f'tl.to(".{p}-mo", {{opacity: 1, duration: 0.3}}, {lead + span * 0.78});' + DRAW(f".{p}-cal", lead + span * 0.78, 0.4)
          + f'tl.to(".{p}-fol", {{opacity: 1, duration: 0.3}}, {lead + 0.2});tl.to(".{p}-fol", {{opacity: 0, duration: 0.3}}, {lead + 2.3});')
    return sv, js

def name(p, dur, lead):
    inner = (L.spot(p, 540, 820, 440, 300)
             + L.label(150, 700, "DU GLAUBST", 26, "start") + ln("M150 740 H520", p + "-a", 10)
             + L.label(150, 940, "IN WAHRHEIT", 26, "start") + ln("M150 980 H900", p + "-b", 10)
             + f'<g filter="url(#{p}-glow)">{ln("M560 760 V960 M540 760 H580 M540 960 H580", p + "-m", 4)}</g>'
             + L.label(720, 870, "DIE LÜCKE", 30, cls=p + "-l"))
    sv, cam = S(p, inner, dur)
    js = cam + DRAW(f".{p}-a", lead - 0.1, 0.5) + DRAW(f".{p}-b", lead + 0.2, 0.7) + DRAW(f".{p}-m", lead + 0.8, 0.4) + IN(f".{p}-l", lead + 1.1)
    return sv, js

def tip(p, dur, lead):
    span = dur - lead
    phone = "M470 820 H610 Q630 820 630 840 V980 Q630 1000 610 1000 H470 Q450 1000 450 980 V840 Q450 820 470 820 Z M520 975 H560"
    inner = (L.spot(p, 540, 820, 420, 300) + f'<g class="{p}-a">{L.big(540, 600, "NICHT", 70)}{L.big(540, 690, "GRÜBELN.", 92)}</g>'
             + f'<g filter="url(#{p}-glow)">{ln(phone, p + "-ph", 5)}{ln("M660 930 L770 895 L705 995 Z", p + "-snd", 5)}</g>'
             + L.label(540, 1070, "SCHICK'S DEM ZERDENKER", 28, cls=p + "-s") + L.label(540, 1120, "SIE MOCHTEN DICH.", 26, op=.85, cls=p + "-lp"))
    sv, cam = S(p, inner, dur)
    js = (cam + M.rise(f".{p}-a", lead + 0.1) + DRAW(f".{p}-ph", lead + span * 0.45, 0.5) + DRAW(f".{p}-snd", lead + span * 0.55, 0.4)
          + f'tl.fromTo(".{p}-snd", {{x: 0, y: 0}}, {{x: 60, y: -40, duration: 0.6, ease: "power2.in"}}, {lead + span * 0.7});'
          + IN(f".{p}-s", lead + span * 0.55) + IN(f".{p}-lp", lead + span * 0.88))
    return sv, js

SCENES = {"hook": hook, "twist": twist, "gap": gap, "name": name, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.16), ("click-soft", 1, 1.0, 0.13), ("click-soft", 2, 0.1, 0.12), ("pop", 2, 2.3, 0.14),
       ("sparkle", 2, 2.9, 0.12), ("click-soft", 3, 0.9, 0.12), ("whoosh-short", 4, 5.2, 0.12), ("chime", 4, 6.3, 0.11)]
