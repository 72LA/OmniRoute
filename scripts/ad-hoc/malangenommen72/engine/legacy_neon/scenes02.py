# Episode 02 scenes: Geschwister. Injected into render.py namespace.
FIG_BIG = figure(CYAN, "neutral")
FIG_BIG_SMILE = figure(CYAN, "smile")
FIG_SMALL = figure(PINK, "neutral")
FIG_SMALL_SMILE = figure(PINK, "smile")
FIG_SMALL_SHOCK = figure(PINK, "shock")
FIG_MOM = figure(LILAC, "smile")

def heart(d, cx, cy, r, col=(255, 70, 120)):
    d.ellipse((cx - r, cy - r, cx, cy), fill=col)
    d.ellipse((cx, cy - r, cx + r, cy), fill=col)
    d.polygon([(cx - r * 0.98, cy - r * 0.35), (cx + r * 0.98, cy - r * 0.35), (cx, cy + r * 1.05)], fill=col)

def bolt(d, cx, cy, s, col=YELLOW):
    pts = [(0, -1), (0.45, -1), (0.1, -0.15), (0.5, -0.15), (-0.25, 1.1), (0, 0.1), (-0.4, 0.1)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=col, outline=DARK)

def card(w, h, outline=CYAN):
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((20, 20, w + 20, h + 20), radius=40, fill=(40, 16, 80, 235), outline=outline + (255,), width=6)
    return glow(im, 12, 1)

CARD = card(440, 470)

def scene02(canvas, name, lt, gt):
    d = ImageDraw.Draw(canvas)
    if name == "bro":
        title(canvas, "WARUM LIEBST DU IHN?", lt, size=104)
        nudge = max(0, math.sin(gt * 7)) * 25 if lt < 2.2 else 0
        paste_center(canvas, FIG_BIG if lt < 2.2 else FIG_BIG_SMILE, 400 + nudge, 820, scale=0.9)
        paste_center(canvas, FIG_SMALL_SHOCK if lt < 2.2 else FIG_SMALL_SMILE, 690, 880, scale=0.65)
        if lt < 2.2:
            for i, (x, y) in enumerate([(560, 600), (620, 560)]):
                f = font_lg(80); text_center(d, (x + i * 50, y), "#!", f, (255, 90, 90), stroke=6)
        else:
            s = ease_out_back((lt - 2.2) / 0.4)
            heart(d, 545, 560 - 10 * math.sin(gt * 4), 90 * s)
    elif name == "fight":
        if lt < 3.0:
            title(canvas, "3x PRO STUNDE", lt, size=116)
            sh = math.sin(gt * 40) * 6
            paste_center(canvas, FIG_BIG, 330 + sh, 860, scale=0.7)
            paste_center(canvas, FIG_SMALL_SHOCK, 750 - sh, 900, scale=0.6)
            n = min(3, int(lt / 0.55) + 1)
            for i in range(n):
                bolt(d, 540, 640 + i * 150, 70)
            # clock
            cx, cy, r = 540, 560, 0
        else:
            title(canvas, "UND TROTZDEM...", lt - 3.0, size=110)
            paste_center(canvas, FIG_BIG_SMILE, 450, 840, scale=0.8)
            paste_center(canvas, FIG_SMALL_SMILE, 640, 880, scale=0.62)
            # rope / bond
            s = ease_out((lt - 3.0) / 0.5)
            d.line((450, 840, 450 + 190 * s, 860), fill=YELLOW, width=14)
            heart(d, 545, 640, 70 * ease_out_back((lt - 3.2) / 0.4))
    elif name == "brain2":
        title(canvas, "DEIN GEHIRN ENTSCHEIDET", lt, size=96)
        layer = Image.new("RGBA", (520, 420), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for (x, y, r) in [(170, 170, 120), (300, 150, 130), (380, 230, 110), (230, 260, 120), (140, 260, 90)]:
            ld.ellipse((x - r, y - r, x + r, y + r), fill=(255, 140, 200, 255), outline=(255, 210, 240, 255), width=6)
        for k in range(5):
            ld.arc((120 + k * 50, 120 + (k % 2) * 60, 220 + k * 50, 220 + (k % 2) * 60), 200, 340, fill=(200, 60, 150, 255), width=8)
        paste_center(canvas, glow(layer, 16, 1), W / 2, 760 + math.sin(gt * 3) * 6, scale=0.95)
        if lt > 1.4:
            for i, lab in enumerate(["HINWEIS 1", "HINWEIS 2"]):
                s = ease_out_back((lt - 1.4 - i * 0.35) / 0.35)
                if s > 0.02:
                    x = 300 + i * 480
                    d.rounded_rectangle((x - 170 * s, 1010 - 50 * s, x + 170 * s, 1010 + 50 * s), radius=40, fill=YELLOW)
                    text_center(d, (x, 1012), lab, font_lg(int(56 * s) + 1), DARK, stroke=0)
    elif name == "cues":
        title(canvas, "2 HINWEISE", lt, size=116)
        split = 2.6
        for i in range(2):
            s = ease_out_back((lt - (0 if i == 0 else split)) / 0.4)
            if s <= 0.02:
                continue
            cx = 290 + i * 500
            paste_center(canvas, CARD, cx, 800, scale=s)
            if s > 0.9:
                if i == 0:
                    paste_center(canvas, FIG_MOM, cx - 40, 790, scale=0.7)
                    # baby in arms
                    d.ellipse((cx + 20, 760, cx + 110, 830), fill=(255, 220, 240))
                    d.ellipse((cx + 70, 735, cx + 125, 790), fill=CREAM)
                    heart(d, cx + 90, 700 - 8 * math.sin(gt * 5), 26)
                    text_center(d, (cx, 990), "MAMA + BABY", font_lg(50), YELLOW, stroke=6)
                else:
                    # house
                    d.polygon([(cx - 150, 760), (cx, 640), (cx + 150, 760)], fill=YELLOW, outline=DARK)
                    d.rectangle((cx - 120, 760, cx + 120, 920), fill=(255, 240, 200), outline=DARK, width=4)
                    paste_center(canvas, FIG_BIG_SMILE, cx - 50, 860, scale=0.28)
                    paste_center(canvas, FIG_SMALL_SMILE, cx + 50, 875, scale=0.22)
                    yrs = min(18, int((lt - split) * 8) + 1)
                    text_center(d, (cx, 990), f"{yrs} JAHRE", font_lg(56), YELLOW, stroke=6)
    elif name == "help":
        title(canvas, "DU HILFST TROTZDEM", lt, size=104)
        up = ease_out((lt - 0.6) / 1.2)
        paste_center(canvas, FIG_BIG_SMILE, 400, 830, scale=0.85)
        ang_y = 990 - 140 * up
        paste_center(canvas, FIG_SMALL if up < 1 else FIG_SMALL_SMILE, 690, ang_y - 70 * (1 - up) + 30, scale=0.62)
        d.line((470, 820, 640, ang_y - 140), fill=CREAM, width=16)
        if lt > 2.2:
            heart(d, 545, 560 - 10 * math.sin(gt * 4), 75 * ease_out_back((lt - 2.2) / 0.4))
        if lt > 2.8:
            text_center(d, (760, 600), "nervt...", font_ms(46, "Black"), CREAM, stroke=5)
    elif name == "study":
        title(canvas, "LANGZEITSTUDIE", lt, size=116)
        y = 1000
        p = ease_out(lt / 2.2)
        d.line((180, y, 180 + 720 * p, y), fill=CREAM, width=10)
        for (x, lab, at) in [(180, "23", 0.0), (900, "41", 2.0)]:
            if lt >= at:
                d.ellipse((x - 28, y - 28, x + 28, y + 28), fill=YELLOW, outline=DARK, width=4)
                text_center(d, (x, y + 75), lab + " J.", font_lg(60), YELLOW, stroke=6)
        paste_center(canvas, FIG_BIG_SMILE, 260, 800, scale=0.55)
        paste_center(canvas, FIG_SMALL_SMILE, 380, 820, scale=0.45)
        heart(d, 320, 640, 40)
        if lt > 2.0:
            s = ease_out_back((lt - 2.0) / 0.4)
            paste_center(canvas, FIG_BIG_SMILE, 820, 800, scale=0.6 * s)
            if s > 0.9:
                d.rounded_rectangle((600, 590, 1000, 690), radius=40, fill=(60, 220, 140))
                text_center(d, (800, 640), "WENIGER ÄNGSTE", font_lg(48), DARK, stroke=0)
    elif name == "share":
        title(canvas, "OHNE KOMMENTAR", lt, size=112)
        s = ease_out_back(lt / 0.4)
        layer = Image.new("RGBA", (900, 420), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((40, 40, 860, 330), radius=70, fill=CREAM + (255,), outline=CYAN + (255,), width=8)
        ld.polygon([(170, 325), (290, 325), (150, 410)], fill=CREAM + (255,))
        text_center(ld, (450, 135), "SCHICK'S DEINEM", font_lg(78), (120, 30, 160), stroke=0)
        text_center(ld, (450, 235), "BRUDER / SCHWESTER", font_lg(70), (254, 44, 85), stroke=0)
        paste_center(canvas, glow(layer, 14, 1), W / 2, 640, scale=max(0.01, s))
        paste_center(canvas, FIG_BIG_SMILE, 460, 960, scale=0.5)
        paste_center(canvas, FIG_SMALL_SMILE, 620, 985, scale=0.4)
        heart(d, 540, 850 - 10 * abs(math.sin(gt * 4)), 40)
    else:
        return False
    return True
