# AI72 #05 – "Warum kannst du dich nicht selbst kitzeln?" – flat infographic style.
KEYS = {"selbst", "kitzeln", "nicht", "kleinhirn", "voraus", "gedämpft", "@ai72", "gehirn", "roboter", "verzögerung",
        "kitzliger", "vorhersage", "kitzlig"}

TITLES = {"hook": "SELBST KITZELN?", "try": "KLAPPT NICHT", "cerebellum": "DAS KLEINHIRN", "predict": "VORHERSAGE = LEISER",
          "robot": "DER ROBOTER-TEST", "mismatch": "PASST NICHT", "share": "SCHICK'S WEITER"}

SCENE_CSS = """
.title { -webkit-text-stroke: 12px #0a0f24; paint-order: stroke fill; }
svg { position: absolute; overflow: visible; }
.lbl { position: absolute; font-weight: 900; color: #fff; -webkit-text-stroke: 8px #0a0f24; paint-order: stroke fill; text-align: center; }
.pill { position: absolute; border: 6px solid #0a0f24; border-radius: 60px; box-shadow: 10px 12px 0 #0a0f24; font-weight: 900; text-align: center; }
"""
O = "#0a0f24"; Y = "#ffd400"; P = "#ff4f8b"; C = "#3ee0ff"; CR = "#ffecd6"; N2 = "#1c2e64"

def POP(sel, at, d=0.45, origin="50% 50%"):
    return f'tl.fromTo("{sel}", {{scale: 0, opacity: 0, transformOrigin: "{origin}"}}, {{scale: 1, opacity: 1, duration: {d}, ease: "back.out(1.6)"}}, {at});'

def face(id_, cx, cy, r, mood="neutral"):
    eyes = (f'<circle cx="{cx-r*0.35}" cy="{cy-r*0.12}" r="{r*0.09}" fill="{O}"/><circle cx="{cx+r*0.35}" cy="{cy-r*0.12}" r="{r*0.09}" fill="{O}"/>')
    if mood == "bored":
        eyes = (f'<path d="M{cx-r*0.48} {cy-r*0.12} h{r*0.26}" stroke="{O}" stroke-width="{r*0.08}" stroke-linecap="round"/>'
                f'<path d="M{cx+r*0.22} {cy-r*0.12} h{r*0.26}" stroke="{O}" stroke-width="{r*0.08}" stroke-linecap="round"/>')
    mouth = {"neutral": f'<path d="M{cx-r*0.22} {cy+r*0.38} h{r*0.44}" stroke="{O}" stroke-width="{r*0.08}" stroke-linecap="round"/>',
             "bored": f'<path d="M{cx-r*0.22} {cy+r*0.4} q{r*0.22} {-r*0.06} {r*0.44} 0" fill="none" stroke="{O}" stroke-width="{r*0.08}" stroke-linecap="round"/>',
             "laugh": f'<path d="M{cx-r*0.36} {cy+r*0.22} q{r*0.36} {r*0.55} {r*0.72} 0 z" fill="{O}"/>'}[mood]
    return (f'<g id="{id_}"><circle cx="{cx+14}" cy="{cy+16}" r="{r}" fill="{O}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CR}" stroke="{O}" stroke-width="10"/>'
            f'<ellipse cx="{cx-r*0.6}" cy="{cy+r*0.18}" rx="{r*0.15}" ry="{r*0.09}" fill="#ffa0aa"/>'
            f'<ellipse cx="{cx+r*0.6}" cy="{cy+r*0.18}" rx="{r*0.15}" ry="{r*0.09}" fill="#ffa0aa"/>{eyes}{mouth}</g>')

def hand(id_, x, y, s=1.0, col=P):
    # simple flat hand with 4 fingers pointing left
    fingers = "".join(f'<rect x="{x - 110*s}" y="{y - 60*s + k*32*s}" width="{120*s}" height="{26*s}" rx="{13*s}" fill="{col}" stroke="{O}" stroke-width="6"/>' for k in range(4))
    return (f'<g id="{id_}">{fingers}<rect x="{x-10*s}" y="{y-70*s}" width="{110*s}" height="{140*s}" rx="{36*s}" fill="{col}" stroke="{O}" stroke-width="7"/>'
            f'<rect x="{x+20*s}" y="{y+40*s}" width="{60*s}" height="{90*s}" rx="{20*s}" fill="{col}" stroke="{O}" stroke-width="7"/></g>')

def hook(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      {face(p+"-f", 470, 800, 210, "neutral")}
      {hand(p+"-h", 820, 800, 1.1)}
      <path id="{p}-feather" d="M760 560 q90 -120 200 -60 q-40 110 -200 60 z" fill="{Y}" stroke="{O}" stroke-width="7"/>
      <path d="M760 560 l160 -50" stroke="{O}" stroke-width="6"/>
    </svg>
    """
    js = (f'tl.fromTo("#{p}-h", {{x: 0}}, {{x: -30, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: 15}}, 0.2);'
          + f'tl.fromTo("#{p}-feather", {{rotation: 0, svgOrigin: "760 560"}}, {{rotation: 14, duration: 0.18, ease: "sine.inOut", yoyo: true, repeat: 11}}, 0.3);')
    return html, js

def try_(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      {face(p+"-f", 540, 780, 230, "bored")}
      <g id="{p}-x"><path d="M790 520 L960 690 M960 520 L790 690" stroke="{O}" stroke-width="58" stroke-linecap="round"/>
      <path d="M790 520 L960 690 M960 520 L790 690" stroke="{Y}" stroke-width="34" stroke-linecap="round"/></g>
    </svg>
    <div id="{p}-dots" class="lbl" style="left:0;right:0;top:1010px;font-size:70px">… nichts.</div>
    """
    js = POP(f"#{p}-x", lead + 0.9) + f'tl.fromTo("#{p}-dots", {{opacity: 0}}, {{opacity: 1, duration: 0.25}}, {lead + 1.4});'
    return html, js

def brain_side(cx, cy, s, pid):
    lobes = [(-0.55, -0.1, 0.42), (-0.2, -0.38, 0.46), (0.22, -0.36, 0.44), (0.5, -0.05, 0.4), (0.0, 0.05, 0.5), (-0.4, 0.2, 0.36)]
    out = "".join(f'<circle cx="{cx+x*s}" cy="{cy+y*s}" r="{r*s+9}" fill="{O}"/>' for x, y, r in lobes)
    fill = "".join(f'<circle cx="{cx+x*s}" cy="{cy+y*s}" r="{r*s}" fill="{P}"/>' for x, y, r in lobes)
    folds = "".join(f'<path d="M{cx+x*s-40} {cy+y*s} q40 -30 80 0" fill="none" stroke="{O}" stroke-width="8" stroke-linecap="round"/>' for x, y in [(-0.35, -0.2), (0.15, -0.3), (0.3, 0.05), (-0.15, 0.1)])
    cb = (f'<g id="{pid}-cb"><ellipse cx="{cx+0.62*s+12}" cy="{cy+0.42*s+14}" rx="{0.3*s}" ry="{0.2*s}" fill="{O}"/>'
          f'<ellipse cx="{cx+0.62*s}" cy="{cy+0.42*s}" rx="{0.3*s}" ry="{0.2*s}" fill="{Y}" stroke="{O}" stroke-width="8"/>'
          + "".join(f'<path d="M{cx+0.42*s} {cy+(0.34+k*0.06)*s} h{0.4*s}" stroke="{O}" stroke-width="6"/>' for k in range(3)) + '</g>')
    stem = f'<rect x="{cx+0.25*s}" y="{cy+0.35*s}" width="{0.16*s}" height="{0.45*s}" rx="20" fill="{CR}" stroke="{O}" stroke-width="8"/>'
    return stem + out + fill + folds + cb

def cerebellum(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-brain">{brain_side(500, 760, 300, p)}</g>
      <path id="{p}-arrow" d="M900 1000 Q 860 900 780 920" fill="none" stroke="{O}" stroke-width="22" stroke-linecap="round"/>
      <path id="{p}-arrow2" d="M900 1000 Q 860 900 780 920" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
    </svg>
    <div id="{p}-lab" class="pill" style="left:620px;top:1000px;width:360px;height:100px;line-height:88px;background:{Y};color:{O};font-size:48px">KLEINHIRN</div>
    """
    js = (POP(f"#{p}-brain", lead, 0.5) + f'tl.fromTo("#{p}-cb", {{scale: 1}}, {{scale: 1.18, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1, svgOrigin: "686 886"}}, {lead + 1.6});'
          + f'tl.fromTo(["#{p}-arrow", "#{p}-arrow2"], {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 1.5});' + POP(f"#{p}-lab", lead + 1.6))
    return html, js

def predict(p, dur, lead):
    third = (dur - lead) / 3
    meter = "".join(f'<rect class="{p}-bar" x="{690 + k*62}" y="{1000 - k*48}" width="44" height="{60 + k*48}" rx="10" fill="{C if k < 2 else (Y if k < 4 else P)}" stroke="{O}" stroke-width="6"/>' for k in range(6))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-c1">{hand(p+"-hd", 250, 620, 0.85, P)}</g>
      <g id="{p}-c2"><circle cx="270" cy="930" r="125" fill="{O}" transform="translate(12 14)"/><circle cx="270" cy="930" r="125" fill="{N2}" stroke="{O}" stroke-width="8"/>
        <path d="M180 930 q22 -50 45 0 t45 0 t45 0 t45 0" fill="none" stroke="{Y}" stroke-width="12" stroke-linecap="round"/></g>
      <g id="{p}-meter">{meter}</g>
    </svg>
    <div id="{p}-l1" class="lbl" style="left:110px;width:320px;top:1070px;font-size:40px">VORHERSAGE</div>
    <div id="{p}-l2" class="lbl" style="left:640px;width:380px;top:1070px;font-size:40px">GEFÜHL</div>
    <div id="{p}-l3" class="lbl" style="left:640px;width:380px;top:1070px;font-size:40px;color:{Y};opacity:0">GEDÄMPFT</div>
    """
    js = (POP(f"#{p}-c1", lead) + POP(f"#{p}-c2", lead + third * 0.8) + f'tl.fromTo("#{p}-l1", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + third * 0.8});'
          + POP(f"#{p}-meter", lead + third * 1.2) + f'tl.fromTo("#{p}-l2", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + third * 1.2});'
          + f'tl.to(".{p}-bar:nth-child(n+3)", {{opacity: 0.15, duration: 0.5, stagger: -0.08, ease: "power2.in"}}, {lead + third * 2.1});'
          + f'tl.to("#{p}-l2", {{opacity: 0, duration: 0.1}}, {lead + third * 2.1});'
          + f'tl.fromTo("#{p}-l3", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + third * 2.1 + 0.1});')
    return html, js

def follow(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920"><g id="{p}-logo">
      <circle cx="552" cy="672" r="200" fill="{O}"/><circle cx="540" cy="660" r="200" fill="#24347e" stroke="{O}" stroke-width="10"/>
      {"".join(f'<circle cx="{540+x*150}" cy="{640+y*150}" r="{r*150+8}" fill="{O}"/>' for x,y,r in [(-0.45,-0.3,0.42),(-0.6,0.08,0.4),(-0.33,0.38,0.4),(0.45,-0.3,0.42),(0.6,0.08,0.4),(0.33,0.38,0.4),(0,0.1,0.45),(-0.12,-0.48,0.36),(0.12,-0.48,0.36)])}
      {"".join(f'<circle cx="{540+x*150}" cy="{640+y*150}" r="{r*150}" fill="{P}"/>' for x,y,r in [(-0.45,-0.3,0.42),(-0.6,0.08,0.4),(-0.33,0.38,0.4),(0.45,-0.3,0.42),(0.6,0.08,0.4),(0.33,0.38,0.4),(0,0.1,0.45),(-0.12,-0.48,0.36),(0.12,-0.48,0.36)])}
      <circle cx="490" cy="640" r="14" fill="{O}"/><circle cx="590" cy="640" r="14" fill="{O}"/>
      <path d="M505 680 q35 40 70 0 z" fill="{O}"/>
    </g></svg>
    <div id="{p}-h" class="lbl" style="left:0;right:0;top:900px;font-size:66px">@ai72</div>
    <div id="{p}-btn" class="pill" style="left:330px;top:1000px;width:420px;height:100px;line-height:88px;background:{P};color:#fff;font-size:52px">+ FOLGEN</div>
    """
    js = POP(f"#{p}-logo", lead, 0.5) + f'tl.fromTo("#{p}-h", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 0.3});' + POP(f"#{p}-btn", lead + 0.7)
    return html, js

def robot(p, dur, lead):
    half = lead + (dur - lead) * 0.45
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-bot">
        <rect x="132" y="932" width="240" height="120" rx="20" fill="{O}"/><rect x="120" y="920" width="240" height="120" rx="20" fill="{C}" stroke="{O}" stroke-width="8"/>
        <circle cx="190" cy="980" r="18" fill="{O}"/><circle cx="290" cy="980" r="18" fill="{O}"/>
        <g id="{p}-arm"><rect x="230" y="700" width="40" height="230" rx="18" fill="{Y}" stroke="{O}" stroke-width="8"/>
          <rect x="250" y="680" width="300" height="40" rx="18" fill="{Y}" stroke="{O}" stroke-width="8"/>
          <path d="M540 700 q90 -110 200 -50 q-40 110 -200 50 z" fill="#fff" stroke="{O}" stroke-width="7"/></g>
      </g>
      {face(p+"-f", 830, 820, 130, "neutral")}
      <g id="{p}-clock"><circle cx="250" cy="540" r="70" fill="#fff" stroke="{O}" stroke-width="8"/><path id="{p}-hand" d="M250 540 V485" stroke="{O}" stroke-width="10" stroke-linecap="round"/></g>
    </svg>
    <div id="{p}-delay" class="pill" style="left:360px;top:500px;width:470px;height:84px;line-height:72px;background:{Y};color:{O};font-size:38px">+ VERZÖGERUNG</div>
    <div id="{p}-meterbg" style="position:absolute;left:180px;top:1100px;width:720px;height:40px;border:6px solid {O};border-radius:20px;background:{N2}"></div>
    <div id="{p}-meter" style="position:absolute;left:186px;top:1106px;width:708px;height:28px;border-radius:14px;background:{P};transform-origin:0 50%"></div>
    """
    js = (POP(f"#{p}-bot", lead, 0.45) + POP(f"#{p}-f", lead + 0.2, 0.45)
          + f'tl.fromTo("#{p}-meter", {{scaleX: 0.15}}, {{scaleX: 0.2, duration: 0.3}}, {lead + 0.5});'
          + f'tl.fromTo("#{p}-arm", {{x: 0}}, {{x: 22, duration: 0.15, ease: "sine.inOut", yoyo: true, repeat: 9}}, {lead + 0.6});'
          + POP(f"#{p}-clock", half - 0.3) + f'tl.fromTo("#{p}-hand", {{rotation: 0, svgOrigin: "250 540"}}, {{rotation: 120, duration: 0.8, ease: "power2.inOut"}}, {half});'
          + POP(f"#{p}-delay", half)
          + f'tl.to("#{p}-meter", {{scaleX: 0.95, duration: 0.9, ease: "power3.out"}}, {half + 0.9});'
          + f'tl.to("#{p}-f", {{scale: 1.12, svgOrigin: "830 820", duration: 0.2, yoyo: true, repeat: 3}}, {half + 1.0});')
    return html, js

def mismatch(p, dur, lead):
    def wave(y, off, col):
        d = "M140 " + str(y) + "".join(f" L{140 + k*8} {y + 60 * __import__('math').sin((k*8 - off)/50)}" for k in range(101))
        return f'<path d="{d}" fill="none" stroke="{O}" stroke-width="22" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round"/>'
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-w1">{wave(560, 0, Y)}</g>
      <g id="{p}-w2">{wave(850, 70, P)}</g>
      <g id="{p}-neq"><circle cx="540" cy="705" r="70" fill="#fff" stroke="{O}" stroke-width="8"/>
        <path d="M505 690 h70 M505 722 h70 M555 665 L525 748" stroke="{O}" stroke-width="12" stroke-linecap="round"/></g>
    </svg>
    <div class="lbl" style="left:140px;top:450px;font-size:36px">ERWARTET</div>
    <div class="lbl" style="left:140px;top:940px;font-size:36px">GESPÜRT</div>
    """
    js = (f'tl.fromTo("#{p}-w1", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: 0.4, ease: "expo.out"}}, {lead});'
          + f'tl.fromTo("#{p}-w2", {{opacity: 0, x: -60}}, {{opacity: 1, x: 0, duration: 0.4, ease: "expo.out"}}, {lead + 0.3});' + POP(f"#{p}-neq", lead + 0.8))
    return html, js

def share(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      {face(p+"-f", 380, 860, 170, "laugh")}
      <g id="{p}-arr"><circle cx="782" cy="872" r="120" fill="{O}"/><circle cx="770" cy="860" r="120" fill="{Y}" stroke="{O}" stroke-width="8"/>
        <path d="M710 900 q10 -90 110 -90 v-40 l70 70 l-70 70 v-40 q-70 0 -110 30 z" fill="{O}"/></g>
    </svg>
    <div id="{p}-b" class="pill" style="left:120px;top:470px;width:840px;height:150px;background:#fff;color:{O};font-size:48px;line-height:1.15;padding-top:18px">DER KITZLIGSTEN<br/><span style="color:{P}">PERSON, DIE DU KENNST</span></div>
    """
    js = (POP(f"#{p}-b", lead) + POP(f"#{p}-f", lead + 0.3) + POP(f"#{p}-arr", lead + 0.6)
          + f'tl.fromTo("#{p}-f", {{rotation: -4, svgOrigin: "380 860"}}, {{rotation: 4, duration: 0.15, ease: "sine.inOut", yoyo: true, repeat: 7}}, {lead + 0.9});')
    return html, js

SCENES = {"hook": hook, "try": try_, "cerebellum": cerebellum, "predict": predict, "follow": follow, "robot": robot, "mismatch": mismatch, "share": share}

SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 1, 0.9, 0.5), ("pop", 2, 1.6, 0.5), ("click-soft", 3, 0.0, 0.4), ("pop", 3, 2.0, 0.4),
       ("pop", 4, 0.7, 0.5), ("sparkle", 5, 3.4, 0.4), ("click-soft", 6, 0.8, 0.45), ("pop", 7, 0.0, 0.5)]
