# Demo / template for the AI72 house style (kg): animated character + props. Maps every scene of an episode
# to two generic layouts, only to validate the theme inside HyperFrames.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K

KEYS = {"schrumpelig?", "wasser", "nerven", "glatt", "blutgefäße", "falten", "@ai72", "körper", "murmeln", "reifen", "badewanne"}
TITLES = {"hook": "SCHRUMPELFINGER?", "myth": "DER MYTHOS", "nerve": "DIE NERVEN-SPUR", "vessels": "NERVEN STEUERN ES",
          "follow": "AI72", "marbles": "DER MURMEL-TEST", "tire": "WIE EIN REIFENPROFIL", "share": "SCHICK'S WEITER"}
SCENE_CSS = """
.title { top: 258px; font-style: italic; font-size: 78px; letter-spacing: .01em; }
.rule { position: absolute; top: 372px; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 34px; letter-spacing: .18em; color: #fff; }
svg { position: absolute; overflow: visible; }
"""

def _svg(inner):
    return f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{inner}</svg>'

def hook(p, dur, lead):
    lens = (f'<g id="{p}-lens" transform="translate(790 700)"><clipPath id="{p}-lc"><circle r="200"/></clipPath>'
            f'<circle r="224" fill="{K.INK}"/><circle r="200" fill="#3a2b9c"/><circle r="150" fill="#4535b0"/>'
            f'<g clip-path="url(#{p}-lc)">{K.hand(-10, 250, 1.2, 0, 4)}</g>'
            f'<rect x="150" y="150" width="46" height="150" rx="20" fill="{K.ORA}" transform="rotate(-45 173 225)"/></g>')
    html = _svg(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1060, 2)
                + f'<g id="{p}-props">{K.drop(170, 600, 22)}{K.drop(560, 470, 16)}{K.bubble(640, 560, 26)}{K.soap(860, 1120, -12)}</g>'
                + f'<g id="{p}-guy">{K.person(330, 1150, 0.84, "wave")}</g>' + lens) + '<div class="rule">— AI72 ERKLÄRT —</div>'
    js = (f'tl.fromTo("#{p}-guy", {{y: 0}}, {{y: -14, duration: 0.35, ease: "power2.out", yoyo: true, repeat: 3}}, 0.2);'
          f'tl.fromTo("#{p}-lens", {{scale: 0, transformOrigin: "790px 700px"}}, {{scale: 1, duration: 0.5, ease: "back.out(1.5)"}}, 0.6);'
          f'tl.fromTo("#{p}-props", {{y: -30, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.6, ease: "expo.out"}}, 0.1);')
    return html, js

def explain(p, dur, lead):
    html = _svg(K.plant_corner("l", 1300, 3) + K.plant_corner("r", 1250, 0)
                + f'<g id="{p}-guy">{K.person(225, 1150, 0.78, "point")}</g>'
                + f'<g id="{p}-card"><rect x="480" y="580" width="540" height="520" rx="50" fill="{K.INK}"/>'
                + K.shaded(K.rrect(470, 560, 540, 520, 50), "#3b2ca0", "M740 550 H1020 V1090 H740 Z", "#33268e") + '</g>')
    js = (f'tl.fromTo("#{p}-card", {{scale: 0.6, opacity: 0, transformOrigin: "740px 820px"}}, {{scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.4)"}}, {lead});'
          f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, 0);')
    return html, js

SCENES = {n: (hook if n == "hook" else explain) for n in TITLES}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.6, 0.5)]
