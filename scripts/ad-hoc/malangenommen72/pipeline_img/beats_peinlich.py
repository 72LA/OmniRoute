# malangenommen72 #14 – "Warum denkst du nachts an peinliche Momente?" – image beats (dark)
def pills(items):
    def ov(p, dur):
        h, j = "", ""
        for k, (lab, val, top, bg, fg) in enumerate(items):
            h += (f'<div id="{p}-o{k}" class="ovl" style="left:0;width:1080px;top:{top}px;text-align:center">'
                  f'<span style="display:inline-block;background:{bg};color:{fg};border-radius:20px;padding:14px 34px;font-weight:900;font-size:46px;'
                  f'box-shadow:0 10px 40px rgba(0,0,0,.5)">{lab} <b style="font-size:84px">{val}</b></span></div>')
            j += f'tl.fromTo("#{p}-o{k}", {{opacity: 0, scale: 0.6}}, {{opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)"}}, {0.25 + k * 0.7});'
        return h, j
    return ov
BEATS = [
    {"img": "a01", "move": "push"},
    {"img": "a02", "at": (0, 5), "move": "pull"},
    {"img": "a03", "at": (1, 0), "move": "push", "flash": True},
    {"img": "a04", "at": (1, 5), "move": "up"},
    {"img": "a05", "at": (2, 0), "move": "push", "flash": True},
    {"img": "a06", "at": (2, 12), "move": "pan-l"},
    {"img": "a07", "at": (3, 0), "move": "push", "flash": True},
    {"img": "a08", "at": (3, 3), "move": "pan-r", "ov": pills([("GEGLAUBT", "~50 %", 470, "rgba(255,255,255,.92)", "#000"),
                                                              ("BEMERKT", "~25 %", 640, "#ff3b4e", "#fff")])},
    {"img": "a09", "at": (4, 0), "move": "push"},
    {"img": "a10", "at": (4, 6), "move": "pan-l"},
    {"img": "a11", "at": (4, 10), "move": "push", "flash": True},
    {"img": "a01", "at": (4, 15), "move": "pull"},
]
KEYS = {"nachts", "peinliche", "10", "still", "ungewollte", "nichts", "dunkeln", "fehler", "halb", "keiner", "schick", "grübelt"}
HOOK = ["WARUM DENKST DU NACHTS AN", "PEINLICHE MOMENTE?"]
FOLLOW = "@malangenommen72"; FOLLOW_AT = (2, 5)
SFX = [("whoosh-short", None, 0.5), ("pop", (3, 4), 0.45), ("pop", (3, 9), 0.5), ("click-soft", (4, 3), 0.35), ("sparkle", (4, 15), 0.35)]
