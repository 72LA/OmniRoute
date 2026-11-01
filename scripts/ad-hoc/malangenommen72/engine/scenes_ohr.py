# Ohrwurm – flat infographic theme. Executed inside render2.py namespace.
KEYS.update({"lied", "kopf", "9", "10", "woche", "ohrwurm.", "ohrwurm", "3.000", "schnelles", "tempo", "überraschung",
             "@malangenommen72", "platz", "1", "romance", "bad", "kaugummi", "seltener", "song"})

def card_flat(d, cx, cy, w, h, col=None):
    d.rounded_rectangle((cx - w / 2 + 10, cy - h / 2 + 12, cx + w / 2 + 10, cy + h / 2 + 12), radius=34, fill=OUT)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=34, fill=col or NAVY2, outline=OUT, width=LW)

def big_head(d, cx, cy, r, face="annoyed", mouth=0.0):
    d.ellipse((cx - r + 14, cy - r + 16, cx + r + 14, cy + r + 16), fill=OUT)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREAM, outline=OUT, width=LW + 2)
    # ears
    for sx in (-1, 1):
        ex = cx + sx * r * 0.98
        d.ellipse((ex - 34, cy - 40, ex + 34, cy + 40), fill=CREAM, outline=OUT, width=LW)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=OUT, width=LW + 2)
    for ex in (-0.35, 0.35):
        x = cx + ex * r
        if face == "annoyed":
            d.line((x - 30, cy - 30, x + 30, cy - 22), fill=OUT, width=10)
            d.ellipse((x - 14, cy - 18, x + 14, cy + 10), fill=OUT)
        else:
            d.ellipse((x - 16, cy - 30, x + 16, cy + 2), fill=OUT)
    d.ellipse((cx - r * 0.7, cy + r * 0.12, cx - r * 0.4, cy + r * 0.3), fill=(255, 160, 170))
    d.ellipse((cx + r * 0.4, cy + r * 0.12, cx + r * 0.7, cy + r * 0.3), fill=(255, 160, 170))
    if face == "chew":
        h = 10 + 26 * mouth
        d.ellipse((cx - 40, cy + r * 0.38 - h / 2, cx + 40, cy + r * 0.38 + h / 2), fill=OUT)
    elif face == "smile":
        d.chord((cx - 60, cy + r * 0.2, cx + 60, cy + r * 0.6), 0, 180, fill=OUT)
    else:
        d.line((cx - 40, cy + r * 0.45, cx + 40, cy + r * 0.4), fill=OUT, width=10)

COLS = [ACC, ACC2, CY]

def SCENE(canvas, name, lt, gt, dur):
    d = ImageDraw.Draw(canvas)
    u = lt / max(dur, 0.1)
    if name == "hook":
        title(canvas, "OHRWURM?!", lt + 1)
        big_head(d, 540, 820, 210, "annoyed")
        for k in range(5):
            a = gt * 1.6 + k * 2 * math.pi / 5
            x = 540 + 330 * math.cos(a); y = 800 + 170 * math.sin(a)
            if math.sin(a) < -0.2 and abs(x - 540) < 220: continue
            note(d, x, y, 1.1, COLS[k % 3])
    elif name == "stat":
        title(canvas, "FAST JEDER", lt)
        for i in range(10):
            x = 160 + (i % 5) * 190; y = 680 + (i // 5) * 260
            figure_flat(d, x, y, 0.55, COLS[i % 3] if i < 9 else (120, 130, 170), "smile" if i == 9 else "annoyed")
            if i < 9 and lt > 0.3 + i * 0.12:
                s = ease_out_back((lt - 0.3 - i * 0.12) / 0.3)
                note(d, x + 40, y - 170, 0.7 * s, ACC)
        if lt > 1.8:
            s = ease_out_back((lt - 1.8) / 0.35)
            layer = Image.new("RGBA", (700, 170), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            ld.rounded_rectangle((10, 14, 690, 160), radius=70, fill=OUT)
            ld.rounded_rectangle((0, 0, 680, 146), radius=70, fill=ACC2, outline=OUT, width=7)
            ld.text((340, 73), "9 VON 10 / WOCHE", font=font(54, "Black"), fill=FG, anchor="mm", stroke_width=6, stroke_fill=OUT)
            paste_center(canvas, layer, 540, 1105, scale=s * 0.9)
    elif name == "study":
        title(canvas, "DIE STUDIE", lt)
        s = ease_out_back(lt / 0.4)
        layer = Image.new("RGBA", (500, 600), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((24, 50, 494, 594), radius=30, fill=OUT)
        ld.rounded_rectangle((10, 36, 480, 580), radius=30, fill=(245, 245, 255), outline=OUT, width=7)
        ld.rounded_rectangle((165, 10, 325, 80), radius=18, fill=ACC, outline=OUT, width=7)
        for k in range(6):
            y = 140 + k * 70; w_ = 300 - (k * 37) % 120
            ld.ellipse((50, y - 14, 78, y + 14), fill=COLS[k % 3], outline=OUT, width=4)
            ld.rounded_rectangle((100, y - 12, 100 + w_, y + 12), radius=12, fill=(190, 200, 230))
        paste_center(canvas, layer, 360, 800, scale=s)
        n = int(3000 * ease_out(lt / max(dur * 0.8, 0.5)))
        txt = f"{n:,}".replace(",", ".")
        d.text((800, 760), txt, font=font(110, "Black"), fill=ACC, anchor="mm", stroke_width=9, stroke_fill=OUT)
        d.text((800, 870), "MENSCHEN", font=font(52, "Black"), fill=FG, anchor="mm", stroke_width=7, stroke_fill=OUT)
        note(d, 760, 1000, 0.9, ACC2); note(d, 860, 990, 0.8, CY)
    elif name == "recipe":
        title(canvas, "DAS REZEPT", lt)
        labels = ["SCHNELL", "EINPRÄGSAM", "ÜBERRASCHUNG"]
        for i in range(3):
            s = ease_out_back((u - i * 0.28) / 0.12)
            if s <= 0.02: continue
            cx = 190 + i * 350; cy = 800
            layer = Image.new("RGBA", (330, 470), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            ld.rounded_rectangle((16, 18, 326, 466), radius=34, fill=OUT)
            ld.rounded_rectangle((4, 4, 312, 452), radius=34, fill=NAVY2, outline=OUT, width=7)
            c = COLS[i]
            if i == 0:  # speedometer
                ld.pieslice((44, 80, 272, 308), 180, 360, fill=(40, 60, 120), outline=OUT, width=6)
                ld.arc((44, 80, 272, 308), 180, 360, fill=c, width=16)
                a = math.radians(180 + 150 + 15 * math.sin(gt * 6)); ld.line((158, 194, 158 + 100 * math.cos(a), 194 + 100 * math.sin(a)), fill=FG, width=10)
                ld.ellipse((143, 179, 173, 209), fill=OUT)
            elif i == 1:  # simple wave
                pts = [(40 + 236 * k / 60, 200 + 50 * math.sin(2 * math.pi * 2 * k / 60 + gt * 4)) for k in range(61)]
                ld.line(pts, fill=c, width=14, joint="curve")
            else:  # wave with spike
                pts = []
                for k in range(61):
                    v = 30 * math.sin(2 * math.pi * 2 * k / 60)
                    if 34 <= k <= 40: v = -110 * math.sin(math.pi * (k - 34) / 6)
                    pts.append((40 + 236 * k / 60, 220 + v))
                ld.line(pts, fill=c, width=14, joint="curve")
                ld.regular_polygon((190, 80, 26), 5, rotation=gt * 60, fill=ACC, outline=OUT)
            f = font(40 if i < 2 else 34, "Black")
            ld.text((158, 380), labels[i], font=f, fill=FG, anchor="mm", stroke_width=5, stroke_fill=OUT)
            paste_center(canvas, layer, cx, cy, scale=s)
    elif name == "follow":
        s = ease_out_back(lt / 0.45); r = 160
        layer = Image.new("RGBA", (400, 400), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.ellipse((30, 34, 370, 374), fill=OUT)
        ld.ellipse((20, 20, 360, 360), fill=(36, 52, 130), outline=OUT, width=8)
        m = Image.new("L", (400, 400), 0); md = ImageDraw.Draw(m)
        md.ellipse((70, 110, 250, 290), fill=255); md.ellipse((125, 75, 305, 255), fill=0)
        layer.paste(ACC + (255,), (0, 0), m)
        ld.text((265, 160), "?", font=font(130, "Black"), fill=FG, anchor="mm", stroke_width=7, stroke_fill=OUT)
        paste_center(canvas, layer, 540, 720, scale=s)
        if lt > 0.3:
            q = ease_out_back((lt - 0.3) / 0.35)
            l2 = Image.new("RGBA", (800, 260), (0, 0, 0, 0)); l2d = ImageDraw.Draw(l2)
            l2d.text((400, 60), "@malangenommen72", font=font(64, "Black"), fill=FG, anchor="mm", stroke_width=8, stroke_fill=OUT)
            l2d.rounded_rectangle((180, 140, 630, 250), radius=55, fill=OUT)
            l2d.rounded_rectangle((170, 128, 620, 238), radius=55, fill=ACC2, outline=OUT, width=7)
            l2d.text((395, 183), "+ FOLGEN", font=font(58, "Black"), fill=FG, anchor="mm", stroke_width=6, stroke_fill=OUT)
            paste_center(canvas, l2, 540, 1030, scale=q)
    elif name == "podium":
        title(canvas, "PLATZ 1", lt)
        for (x, h, lab, c, delay) in [(270, 170, "2", CY, 0.3), (540, 280, "1", ACC, 0.0), (810, 120, "3", ACC2, 0.5)]:
            g = ease_out((lt - delay) / 0.5); hh = h * g
            if hh < 4: continue
            d.rectangle((x - 125 + 12, 1080 - hh + 12, x + 125 + 12, 1080 + 12), fill=OUT)
            d.rectangle((x - 125, 1080 - hh, x + 125, 1080), fill=c, outline=OUT, width=LW)
            if g > 0.8: d.text((x, 1080 - hh / 2), lab, font=font(90, "Black"), fill=FG, anchor="mm", stroke_width=8, stroke_fill=OUT)
        if lt > 0.8:
            s = ease_out_back((lt - 0.8) / 0.4)
            # trophy
            tl = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); td = ImageDraw.Draw(tl)
            td.pieslice((60, 10, 240, 190), 0, 180, fill=ACC, outline=OUT, width=7)
            td.rectangle((60, 10, 240, 100), fill=ACC, outline=OUT, width=7)
            td.rectangle((63, 13, 237, 100), fill=ACC)
            td.arc((20, 30, 90, 120), 90, 270, fill=OUT, width=10); td.arc((210, 30, 280, 120), 270, 90, fill=OUT, width=10)
            td.rectangle((130, 185, 170, 240), fill=ACC, outline=OUT, width=6)
            td.rounded_rectangle((85, 235, 215, 280), radius=12, fill=ACC2, outline=OUT, width=6)
            note(td, 140, 110, 0.8, ACC2)
            paste_center(canvas, tl, 540, 655, scale=s)
        if lt > 1.4:
            q = ease_out_back((lt - 1.4) / 0.35)
            l2 = Image.new("RGBA", (880, 110), (0, 0, 0, 0)); ld = ImageDraw.Draw(l2)
            ld.rounded_rectangle((12, 12, 878, 108), radius=48, fill=OUT)
            ld.rounded_rectangle((0, 0, 866, 96), radius=48, fill=FG, outline=OUT, width=7)
            ld.text((433, 48), "„BAD ROMANCE“ · LADY GAGA", font=font(40, "Black"), fill=OUT, anchor="mm")
            paste_center(canvas, l2, 540, 478, scale=q)
    elif name == "gum":
        title(canvas, "DER TRICK: KAUGUMMI", lt)
        mouth = 0.5 + 0.5 * math.sin(gt * 9)
        big_head(d, 470, 840, 190, "chew", mouth)
        if lt > 0.8:
            r = 40 + 90 * ease_out((lt - 0.8) / 2.0) + 6 * math.sin(gt * 4)
            bx, by = 650, 880
            d.ellipse((bx - r + 10, by - r + 12, bx + r + 10, by + r + 12), fill=OUT)
            d.ellipse((bx - r, by - r, bx + r, by + r), fill=ACC2, outline=OUT, width=LW)
            d.ellipse((bx - r * 0.5, by - r * 0.6, bx - r * 0.15, by - r * 0.3), fill=(255, 190, 215))
        if u > 0.45:
            q = ease_out((u - 0.45) / 0.2)
            for k, (x, y) in enumerate([(830, 620), (900, 760), (240, 600)]):
                note(d, x, y, 0.9, COLS[k], OUT)
                d.line((x - 50, y - 90, x + 70, y + 30), fill=(255, 70, 70), width=int(14 * q) + 1)
    elif name == "comment":
        title(canvas, "UND BEI DIR?", lt)
        s = ease_out_back(lt / 0.4)
        layer = Image.new("RGBA", (900, 470), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((54, 54, 874, 344), radius=70, fill=OUT)
        ld.rounded_rectangle((40, 40, 860, 330), radius=70, fill=FG, outline=OUT, width=8)
        ld.polygon([(170, 325), (290, 325), (150, 430)], fill=FG, outline=OUT)
        ld.line((172, 328, 288, 328), fill=FG, width=10)
        ld.text((450, 140), "WELCHER SONG", font=font(80, "Black"), fill=OUT, anchor="mm")
        ld.text((450, 240), "HÄNGT BEI DIR?", font=font(70, "Black"), fill=ACC2, anchor="mm")
        paste_center(canvas, layer, 540, 700, scale=max(0.01, s))
        for k in range(3):
            note(d, 220 + k * 320, 1000 + 18 * math.sin(gt * 4 + k), 0.9, COLS[k])
        if lt > 0.8:
            y = 1080 + abs(math.sin(gt * 5)) * 24
            d.polygon([(480, y), (600, y), (540, y + 60)], fill=ACC, outline=OUT, width=5)
