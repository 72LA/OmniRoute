# AI72 (ehem. malangenommen72) – Video-Studio (TikTok)

Produktionspaket für den TikTok-Kanal **@malangenommen72** (Psychologie, Wissen, „Wusstest du?“).
Nicht Teil von OmniRoute – reines Ad-hoc-Werkzeug. Freigegeben vom Kanal-Betreiber: Videos #03 und #04
sind die **Referenz-Qualität** für alle künftigen Videos.

## Zwei Kanäle – feste Zuordnung (seit 2026-11-01)

| Kanal | Stil | Profilbild |
|---|---|---|
| **malangenommen72** | **Stil A – Dark** (weiße Line-Art auf Schwarz) | `branding/malangenommen72_Profil_Dark.png` |
| **AI72** | **Stil B – Wissen** (flache Infografik, dunkelblau/gelb/pink) | `branding/AI72_Profil_StilB_Flat.png` |

- Jede Anfrage = zwei Videos: eins für malangenommen72 (Stil A), eins für AI72 (Stil B).
- Follow-Aufruf, Stempel und Hashtag passen zum Kanal: „Folge malangenommen72 …“ / `#malangenommen72`
  bzw. „Folge AI72 …“ (Sprechtext „A I zweiundsiebzig“) / `#ai72`.
- Engine: `render2.py` setzt `CHANNEL`/`HANDLE` automatisch je Stil (`line` → malangenommen72, `flat` → AI72).
  Follow-Szenen sollen `HANDLE` verwenden statt festen Text. AI72-Handle (`@ai72`) beim Betreiber bestätigen.
- Nummerierung läuft je Kanal ab #05 weiter.
- Profilbild-Skripte: `branding/make_avatar_malangenommen.py`, `branding/make_avatars.py`
  (erzeugt zusätzlich eine AI72-Variante im Line-Stil, nur als Alternative).

## Verbindliche Regeln (Master-Briefing)

- Jede Anfrage = **zwei Videos**: eins in **Stil A**, eins in **Stil B**.
- Aufbau jedes Videos: **Hook** (1–3 s, keine Begrüßung) → Hauptteil mit konkretem Beispiel →
  **genau ein** kurzer Follow-Aufruf in der Mitte („Folge @malangenommen72 …“) →
  Abschluss mit Frage / Teil-Aufruf.
- Länge 30–42 s, 9:16 (1080×1920), Untertitel eingebrannt, keine Musik (die fügt der Betreiber in der
  TikTok-App hinzu, privates Konto).
- Pro Video: Caption + **max. 5 Hashtags** (immer der Kanal-Hashtag `#malangenommen72` bzw. `#ai72`), Quellen nur für den Betreiber.
- Nur echte, geprüfte Fakten; Unsicherheit sprachlich kennzeichnen („meistens“, „etwa“, „in einer Studie“).
- Themen nicht wiederholen, Formulierungen variieren. Bevorzugt: Wiedererkennung, Diskussion, Teilbarkeit.
- Stempel „MAL ANGENOMMEN #NN“ unter den Untertiteln, Nummer fortlaufend.
- Lieferung: MP4 + Textdatei (Caption, Hashtags, Titelbild-Hinweis, Quellen) per Datei-Download.

## Stil A – `line`

Minimalist black and white line art animation style, white vector lines on solid black background,
dark aesthetic, clean diagram infographics, technical drawing, 2D outline illustration.
Umsetzung: schwarzes Raster, Eck-Passermarken, „FIG. NN“-Label, Linien zeichnen sich auf
(`poly_progress`), Boxen/Pfeile/Wellen, Schlüsselwörter invertiert (weißer Kasten, schwarze Schrift).
Referenz: `episodes/03_echo_line`, Szenen `engine/scenes_echo.py`.

## Stil B – `flat`

Kurzgesagt-inspirierte flache Infografik (eigene Figuren, keine Kopie), vector flat design,
vibrant corporate-memphis aesthetic, clean bold outlines, solid color shapes, playful science animation,
dark blue background with bright yellow (#FFD400) and pink (#FF4F8B) contrast, Cyan (#3EE0FF) als Drittfarbe.
Umsetzung: Navy-Verlauf, Sterne, schwebende Memphis-Formen, dicke dunkle Outlines + Schlagschatten,
Titel weiß mit gelbem Balken, Schlüsselwörter gelb.
Referenz: `episodes/04_ohrwurm_flat`, Szenen `engine/scenes_ohr.py`.

## Stimme

Google Gemini TTS, Stimme **„Puck“** (`GEMINI_API_KEY` als Umgebungsvariable, nie im Code).
- Free Tier: **10 Requests pro Tag und Modell** – auch fehlgeschlagene/Test-Requests zählen. Nicht proben!
- Modelle: `gemini-3.8-flash-tts`, `gemini-3.1-flash-tts-preview`, `gemini-3.8-flash-lite-tts`,
  `gemini-2.5-flash-preview-tts` (braucht Präfix `TTS_STYLE="Say in German, curious and lively: "`,
  neuere Modelle lesen Präfixe dagegen laut vor → dort KEIN Präfix).
- Sparsam: mehrere Sätze pro Request (`tts_groups.py`), Satzgrenzen per Pausen-Erkennung,
  bei Zweifel `align.py` (Gemini-Textmodell liefert Satz-Zeitstempel).
- Aussprache: „@malangenommen72“ im Sprechtext als „mal angenommen zweiundsiebzig“ schreiben,
  Zahlen ausschreiben (`say`), Ziffern in der Anzeige (`show`).
- vidIQ-Voiceover kostet 14 Credits/1000 Zeichen – nur mit Zustimmung.

## Ablauf (pro Video, im Episoden-Ordner)

```bash
# Voraussetzungen: ffmpeg, Python 3 + Pillow + numpy, Fonts:
#   /tmp/fonts/Montserrat.ttf  <- https://raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf
#   /tmp/fonts/LuckiestGuy.ttf <- https://raw.githubusercontent.com/google/fonts/main/apache/luckiestguy/LuckiestGuy-Regular.ttf
# 1) script.json schreiben: [{"say":..., "show":..., "scene":...}, ...]
# 2) Stimme (Gruppen = Liste von Satz-Indizes je Request)
python3 ../engine/tts_groups.py gemini-3.8-flash-lite-tts Puck '[[0],[1,2,3,4],[5,6,7,8]]'
# 3) Zusammensetzen (Tempo; optional "echo" = Echo-Effekt auf Satz 0)
python3 ../engine/assemble.py 1.05
# 4) Vorschau einzelner Zeitpunkte, dann alle Frames
python3 ../engine/render2.py line 05 ../engine/scenes_xyz.py 1.0 8.0 15.0
python3 ../engine/render2.py line 05 ../engine/scenes_xyz.py
# 5) Sounds (sfx.json: [["pop"|"ding"|"whoosh"|"blip", satzIndex, offsetSek], ...]) + Encode
python3 ../engine/mix.py
ffmpeg -y -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -shortest -movflags +faststart out.mp4
```

Neue Szenen: eine `engine/scenes_<thema>.py` anlegen, die `SCENE(canvas, name, lt, gt, dur)` definiert
und `KEYS` (hervorgehobene Wörter) ergänzt; Hilfsfunktionen stehen in `render2.py`.
Layout-Zonen: Titel y≈360, Inhalt y 470–1130, Untertitel y 1250, Stempel y 1380, unten 20 % frei (TikTok-UI).

## Bereits verwendete Themen (nicht wiederholen)

| # | Thema | Stil |
|---|---|---|
| 01 | Spotlight-Effekt (peinliches T-Shirt) | alter Neon-Lila-Stil |
| 02 | Warum liebst du deinen Bruder? (Geschwister, Kin-Detection) | alter Neon-Lila-Stil |
| 03 | Echo im Call / verzögerte Stimme | A line |
| 04 | Ohrwurm | B flat |
| – | Türschwellen-Effekt | vom Betreiber selbst schon gemacht |

## Kanal-Befund (Stand 2026-11-01)

~740–854 Aufrufe/Video, ~8–9 % Like-Rate, aber nur 2 Follower → Follow-Aufruf, Serien-Stempel,
einheitliche Cover („volle Frage, max. 5 Wörter“) sind die Hebel. Für echte Analyse Screenshots aus
TikTok Studio (Wiedergabezeit, Retention-Kurve, Traffic-Quellen) anfordern.
