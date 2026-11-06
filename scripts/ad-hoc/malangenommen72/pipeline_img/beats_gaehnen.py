# AI72 #13 – "Warum musst du gähnen, wenn andere gähnen?" – image beats (vivid)
def big(lines):
    def ov(p, dur):
        h, j = "", ""
        for k, (txt, top, size, col) in enumerate(lines):
            h += (f'<div id="{p}-o{k}" class="ovl" style="left:0;width:1080px;top:{top}px;text-align:center;font-family:Anton,Montserrat;font-size:{size}px;'
                  f'color:{col};-webkit-text-stroke:12px #1b0f3d;paint-order:stroke fill;text-shadow:0 12px 30px rgba(0,0,0,.5)">{txt}</div>')
            j += f'tl.fromTo("#{p}-o{k}", {{opacity: 0, scale: 0.4}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)"}}, {0.15 + k * 0.5});'
        return h, j
    return ov
def bars(p, dur):
    h = ('<div class="ovl" style="left:150px;right:150px;top:440px;height:420px;background:rgba(27,15,61,.78);border-radius:36px"></div>'
         f'<div id="{p}-b1" class="ovl" style="left:250px;top:{820-330}px;width:220px;height:330px;background:#ff4fa3;border-radius:22px;transform-origin:50% 100%"></div>'
         f'<div id="{p}-b2" class="ovl" style="left:610px;top:{820-126}px;width:220px;height:126px;background:#2ad4c0;border-radius:22px;transform-origin:50% 100%"></div>'
         '<div class="ovl" style="left:250px;width:220px;top:440px;text-align:center;font:900 56px Montserrat;color:#fff">55 %</div>'
         '<div class="ovl" style="left:610px;width:220px;top:620px;text-align:center;font:900 56px Montserrat;color:#fff">21 %</div>'
         '<div class="ovl" style="left:250px;width:220px;top:830px;text-align:center;font:800 26px Montserrat;color:#fff">MIT VIDEO</div>'
         '<div class="ovl" style="left:610px;width:220px;top:830px;text-align:center;font:800 26px Montserrat;color:#fff">OHNE</div>')
    j = (f'tl.fromTo("#{p}-b1", {{scaleY: 0}}, {{scaleY: 1, duration: 0.5, ease: "power3.out"}}, 0.1);'
         f'tl.fromTo("#{p}-b2", {{scaleY: 0}}, {{scaleY: 1, duration: 0.5, ease: "power3.out"}}, 0.5);')
    return h, j
BEATS = [
    {"img": "b01", "move": "push"},
    {"img": "b02", "at": (0, 7), "move": "push", "flash": True},
    {"img": "b03", "at": (1, 0), "move": "pan-r", "flash": True},
    {"img": "b04", "at": (1, 3), "move": "push", "ov": big([("55 %", 470, 230, "#ffd23f"), ("GÄHNTEN MIT", 730, 70, "#fff")])},
    {"img": "b03", "at": (1, 12), "move": "pull", "ov": bars},
    {"img": "b05", "at": (2, 0), "move": "push", "flash": True},
    {"img": "b06", "at": (2, 4), "move": "push"},
    {"img": "b07", "at": (3, 0), "move": "push", "flash": True},
    {"img": "b08", "at": (3, 6), "move": "pan-l"},
    {"img": "b09", "at": (3, 11), "move": "push", "ov": big([("0", 450, 260, "#2ad4c0"), ("GÄHNTEN MIT", 740, 70, "#fff")])},
    {"img": "b10", "at": (4, 0), "move": "push", "flash": True},
    {"img": "b11", "at": (4, 7), "move": "pan-r"},
    {"img": "b01", "at": (4, 11), "move": "pull"},
]
KEYS = {"gähnen", "gähnen?", "gähnst", "hälfte", "fünfte", "lesen", "jetzt", "kühlt", "gehirn", "nase", "gegähnt", "kommentare", "testen"}
HOOK = ["WARUM MUSST DU GÄHNEN,", "WENN ANDERE GÄHNEN?"]
FOLLOW = "@ai72"; FOLLOW_AT = (2, 0)
SFX = [("whoosh-short", None, 0.5), ("pop", (1, 3), 0.5), ("pop", (1, 13), 0.4), ("click-soft", (2, 4), 0.4), ("pop", (3, 11), 0.5), ("sparkle", (4, 0), 0.4)]
