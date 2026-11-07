# AI72 (ehem. malangenommen72) – Video-Studio (TikTok)

> **Antwortstil: immer Caveman (`/anthropic-skills:caveman`) – kurz, ohne Füllwörter, alle Fakten bleiben. Dauerhaft, bis Betreiber „normal mode“ sagt.**

> **Bei „Go“: zuerst `GO.md` lesen – verbindlicher Ablauf (Mix aus alten + neuen Regeln). Bei Widerspruch gilt GO.md.**

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

## malangenommen72 – Dark v2 (ab #08, beim nächsten Go anwenden)

Vom Betreiber per Referenz-Screenshots vorgegeben (2026-11-03). Entwurf: `branding/stylelab_dark/malangenommen72_Dark_v2.png`
(`make_dark2.py`). Ersetzt den bisherigen Dark-Stil (Linienraster) für malangenommen72:
- Reines Schwarz, **Punktraster** nur im Mittelband, zum Rand ausgeblendet.
- **Glow/Bloom** auf allen weißen Elementen; weicher Lichtfleck hinter der Hauptfigur.
- **Massive, leuchtende weiße Figur** (Seitenansicht, runde Formen: Kopf, Pill-Torso, Beine; Posen stehen/sitzen).
- **Metapher-Diagramme**: z. B. „ERWARTUNGEN“ (gestrichelter Balken) über „UMSTÄNDE“ (durchgezogen),
  Maßlinie „GLEICHE LÜCKE“, Skala mit Werten und gestrichelten Hilfslinien.
- **Gemütliche Alltagsszenen** in Linien: Schreibtisch, Laptop, Tasse mit Dampf, Fenster mit Mond, Kalender mit Jahr.
- Beschriftung: kleine Großbuchstaben mit weitem Abstand (Letter-Spacing ~0.38 em); Titel weiß mit Glow.
- Erste Themenidee dazu: „Mal angenommen, du verdienst ab morgen das Doppelte – wärst du glücklicher?“
  (hedonische Anpassung; Fakten vor Produktion prüfen).

## AI72-Hausstil (ab #07) – vom Betreiber freigegeben am 2026-11-03

AI72 nutzt ab #07 den **kg-Stil** (Theme `kg` in `hyperframes/build_hf.py`, Bausteine in `hyperframes/kg_lib.py`,
Vorlage/Test `hyperframes/scenes_kg_demo.py`, Entwürfe `branding/stylelab_ai72/AI72_Stil_v3.png`):
- Flache Formen **ohne Konturen**, Schatten mit **harter Kante** (2–3 Töne je Form, `kg_lib.shaded`).
- Tiefes Indigo, dunkler Rand (Vignette), konzentrische Lichtringe hinter dem Hauptmotiv, Punkt-Sterne, gelbe Funkel.
- Satte Farben: Türkis, Magenta, Orange, Gelb, Blau; Blätter-Äste vom Bildrand, Pilze/Steine/Pflanzen unten.
- **Eigene Figur** (`kg_lib.person`, Posen `wave`/`point`): runder Kopf, rosa Haut, große lila Haare, kleine Punktaugen,
  Wangenröte, türkiser Hoodie. Hand = Fäustling-Form (`kg_lib.hand`).
- Titel kursiv 900 + Unterzeile „— AI72 ERKLÄRT —“; Untertitel weiß mit dunklem Schatten, Schlüsselwort gelb.
- **Keine Vögel, keine Ente, keine Kurzgesagt-Figuren/Logos** – nur der Stil ist Vorbild.
- Profilbild AI72: `branding/AI72_Profil_KG.png` (ersetzt die alten AI72-Profilbilder).
- malangenommen72 bleibt unverändert im Dark-Stil.

## Render-Werkzeug

Ab #05: **HyperFrames-Pipeline** – siehe `hyperframes/README.md`. Die Pillow-Engine (`engine/`) bleibt als Fallback.

## Referenzbilder

Die Original-Screenshots (Stilvorbilder, PsychoLogisch, TikTok-Tipps, Rätsel-Video) liegen bewusst **nicht** im Repo
(fremdes Material). Der Betreiber hat sie als `Referenzen.zip`. Inhalt (Stand 2026-11-06): 01–09 Stilvorbilder/Tipps, 10–13 Referenzanalyse (AGENTUR.md), 14–16 Profile + Boosts, 17–21 TikTok-Studio-Daten 29.10.–04.11. (Auswertung REICHWEITE.md §8), 22 Paar-Quiz (ausgeschlossen), 23 eigenes Wasser-Video. Für eine neue Sitzung bei Bedarf erneut hochladen.

**NEUES FORMAT ab 2026-11-06 (Betreiber: „mach es so, wie es am meisten Reichweite bringt“): beide Kanäle 20–28 s**
(ersetzt 35–45 s, Grund: Diagnose REICHWEITE.md §7). Skript 55–75 Wörter: Satz 1 = Behauptung < 1 s, Bewegung ab Frame 0,
kein „MAL ANGENOMMEN“-Vorlauf-Titel, 1 Zahl + 1 Aha + 1 Tipp, Follow-Aufruf nur als Text-Einblendung (kein eigener Satz),
Schluss = Loop zur Anfangsfrage + 1 leichte Kommentarfrage. Nach 4–6 Videos mit Studio-Daten auswerten.
Profile: malangenommen72 = Psychologie im Alltag; AI72 = Mythos-Check Körper & Gesundheit.

**Lieferung im Chat (Betreiber-Regel 2026-11-06): nur noch kurz** – Video 1 + Caption-Kopierblock, Video 2 + Caption-Kopierblock.
Keine langen Erklärungen, Quellen nur in der Textdatei.

## Reichweiten-Regeln (seit 2026-11-03, aus Betreiber-Referenzen)

**AI72 ab #11 (Betreiber-Regel 2026-11-04): keine Rätsel mehr.** Reguläres Wissens-Format mit **Frage als Hook**
(„Warum …?“ / „Was passiert, wenn …?“), nach dem TikTok-Hinweis „hilfreicher Beitrag“: echte Details/Quelle,
ehrliche Einordnung, **umsetzbarer Tipp am Ende** („So nutzt du das“), Speicher-Aufruf, Follow-Aufruf in der Mitte
(„Folge AI72 für Wissen, das dir hilft“). Kein Countdown, keine Rätselkarte, kein „Schreib die Lösung“.

**Captions (Betreiber-Regel 2026-11-04):** passend zum Video, **kein Kanalname** (weder Text noch Hashtag),
**genau 5 Hashtags**, im Chat **je Video in einem eigenen Codeblock** (Caption + Hashtags zusammen), damit der
Betreiber mit einem Klick auf „Kopieren“ alles übernimmt. Zusätzlich in der Textdatei.

**Vollständiges Playbook + Pflicht-Checkliste pro Video: `REICHWEITE.md` – vor jeder Produktion lesen und abhaken.**
**Agentur-Ablauf (11 Abteilungen mit Gates, Posting-Checkliste, Referenzanalyse): `AGENTUR.md` – ab 2026-11-05 verbindlich.**
**AI72 ab #11: Serie „MYTHOS-CHECK“** (Alltagsmythos als Frage → Studie → ehrliche Grenzen → Alltagstipp), Vorlage `hyperframes/scenes_knacken.py`.

Quellen: TikTok-Hinweis „So erstellt man einen hilfreichen Beitrag“, Kanal PsychoLogisch, Rätsel-Video von EndzeitAkten.
- **Hilfreich = mehr Reichweite:** jedes Video endet mit einem **konkreten, umsetzbaren Tipp** („Probier es heute aus …“);
  echte Studien/Details nennen; ehrliche Einordnung; Caption **> 50 Zeichen** mit Kern-Erkenntnis (nicht nur Emojis).
- **malangenommen72** (Dark v2 bleibt): PsychoLogisch-Formel übernehmen, eigener Inhalt: ein konkreter Trick / ein Wort,
  **Vorher→Nachher-Zahl** (z. B. „60 % → 93 %“), dann „So nutzt du es“-Checkliste. Format bleibt „Mal angenommen …“.
- ~~AI72: jedes Video enthält ein Rätsel~~ **AUFGEHOBEN 2026-11-04 (ab AI72 #11 keine Rätsel mehr)** – früher: (Format EndzeitAkten, eigene Rätsel): Rätselkarte oben → Frage →
  Countdown „Schreib deine Antwort in die Kommentare, bevor du weiterschaust“ → Follow-Aufruf („jedes Mal ein neues Rätsel“)
  → Lösung mit Wissens-Erklärung → Bonus-Fakt → „Schick's jemandem, der es nicht lösen kann“.
  Rätsel müssen eine **belegbare Wissens-Lösung** haben (kein Copy fremder Rätsel-Videos).

## Verbindliche Regeln (Master-Briefing)

- Jede Anfrage = **zwei Videos**: eins in **Stil A**, eins in **Stil B**.
- Aufbau jedes Videos: **Hook** (1–3 s, keine Begrüßung) → Hauptteil mit konkretem Beispiel →
  **genau ein** kurzer Follow-Aufruf in der Mitte („Folge @malangenommen72 …“) →
  Abschluss mit Frage / Teil-Aufruf.
- Länge **35–45 s** (seit 2026-11-02, verbindlich; Skript auf ~95–125 Wörter auslegen), 9:16 (1080×1920), Untertitel eingebrannt, keine Musik (die fügt der Betreiber in der
  TikTok-App hinzu, privates Konto).
- Pro Video: TikTok-Caption + **genau 5 Hashtags**, **ohne Kanalnamen** (kein `#malangenommen72`/`#ai72`, Kanalname auch nicht im Caption-Text) – Betreiber-Regel seit 2026-11-04. Quellen nur für den Betreiber.
- Ablauf: Captions + Hashtags für beide Videos immer mitliefern und zusätzlich direkt im Chat schicken. Videos nur nach „Go“.
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
| 05 | Mal angenommen, niemand könnte lügen (malangenommen72) | A Dark, HyperFrames |
| 05 | Warum kannst du dich nicht selbst kitzeln? (AI72) | B Wissen, HyperFrames |
| 06 | Mal angenommen, du könntest nie wieder vergessen (malangenommen72) | A Dark, HyperFrames |
| 06 | Warum werden Finger im Wasser schrumpelig? (AI72) | B Wissen, HyperFrames |
| 07 | Mal angenommen, du könntest Gedanken lesen (malangenommen72) | A Dark, HyperFrames |
| 07 | Warum knurrt der Magen? (AI72) | kg-Hausstil, HyperFrames |
| 08 | Ein Wort, das Ja macht – „weil“ (malangenommen72) | Dark v2, HyperFrames |
| 08 | Rätsel: Warum sind Gullydeckel rund? (AI72) | kg + Rätsel, HyperFrames |
| 09 | Fuß-in-der-Tür (malangenommen72) | Dark v2, HyperFrames |
| 09 | Rätsel: Warum schwimmt Eis? (AI72) | kg + Rätsel, HyperFrames |
| 10 | Innen sind wir uns ähnlicher – gegen Rassismus (malangenommen72) | Dark v2, HyperFrames |
| 11 | Macht eine Million glücklicher? Lotto-Studie / hedonische Anpassung (malangenommen72) | Dark v2, HyperFrames |
| 10 | Rätsel: Warum ist der Flug NY → London kürzer? Jetstream (AI72) | kg + Rätsel, HyperFrames |
| 12 | Motivation bringt fast nichts – Wenn-dann-Plan 38 → 91 % (malangenommen72) | Dark v2 + native Textbox |
| 11 | Mythos-Check: Macht Fingerknacken Arthrose? (AI72) | kg, Mythos-Check |
| – | 8 Gläser Wasser am Tag? (vom Betreiber gepostet, geboostet) | Neon |
| 13 | 60 oder 90 Sekunden Schmerz? Peak-End-Regel (malangenommen72) | Dark v2 + Textbox + Kamerafahrt |
| 12 | Mythos-Check #2: Hilft Vitamin C gegen Erkältung? (AI72) | kg, Mythos-Check + Kamerafahrt |
| – | Türschwellen-Effekt | vom Betreiber selbst schon gemacht |
| – | Warum zuckst du beim Einschlafen? | schon verwendet (Betreiber 2026-11-06) |
| 14 | Warum denkst du nachts an peinliche Momente? (malangenommen72) | Bild-Pipeline dunkel |
| – | Gähnen (AI72) | VERWORFEN + gesperrt (Betreiber 2026-11-06) |
| 15 | Warum machst du so selten Komplimente? (malangenommen72) | Dark v2 aufgewertet, sauberer Sound |
| 14 | Mythos-Check #3: Frieren Frauen wirklich schneller? (AI72) | kg aufgewertet, sauberer Sound |
| 16 | Warum denkst du nach Gesprächen, dass sie dich nicht mochten? (malangenommen72) | Dark v2, motion.py |
| 15 | Mythos-Check #4: Macht Kälte krank? (AI72) | kg-Infografik ohne Figur, motion.py |

## Kanal-Befund (Stand 2026-11-01)

~740–854 Aufrufe/Video, ~8–9 % Like-Rate, aber nur 2 Follower → Follow-Aufruf, Serien-Stempel,
einheitliche Cover („volle Frage, max. 5 Wörter“) sind die Hebel. Für echte Analyse Screenshots aus
TikTok Studio (Wiedergabezeit, Retention-Kurve, Traffic-Quellen) anfordern.
