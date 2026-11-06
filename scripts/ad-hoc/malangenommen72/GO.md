# GO-Ablauf – verbindlich, sobald der Betreiber „Go“ schreibt (Stand 2026-11-06)

Diese Datei ist die **eine Quelle** für jede Produktion. Sie vereint alte Regeln, die funktioniert haben
(Boosts „8 Gläser Wasser“ und „Fuß in der Tür“, Top-Videos „Warum du …?“), mit den neuen Regeln aus der
Studio-Auswertung (REICHWEITE.md §7–8). Details: README.md (Technik/Stil), AGENTUR.md (Abteilungen), IDEEN.md (Themen).

## 0. Ohne „Go“ nichts produzieren
**Keine Rätsel mehr – auf keinem Kanal** (Betreiber 2026-11-06: kommen schlecht an). Kein Rätselkarten-, Countdown- oder Lösungs-Format.
„Go“ = **2 Videos**: 1× malangenommen72, 1× AI72 (außer Betreiber sagt anders). Thema: nächste Freigabe aus IDEEN.md.

## 1. Kanal-Profile (getrennt halten)
| | malangenommen72 | AI72 |
|---|---|---|
| Inhalt | Psychologie im Alltag: Menschen, Beziehungen, Denkfehler, Tricks | Mythos-Check & Neugier: Körper, Gesundheit, Alltagswissen |
| Stil | Dark v2 (schwarz, Glow, weiße Linienfigur, Punktraster) | kg-Hausstil (Indigo, flach, eigene Figur, keine Kurzgesagt-Figuren) |
| Serie | Stempel „MAL ANGENOMMEN #NN“ | „MYTHOS-CHECK #N“ |
| Follow-Text | Einblendung „@malangenommen72 folgen“ | Einblendung „@ai72 folgen“ |

## 2. Thema wählen – Pflicht-Filter (alle 5 erfüllen)
1. **„Warum du …?“** – Frage über eigenes Verhalten/Körper des Zuschauers (Top-Videos: zu spät kommen, schneller gehen,
   Echo, Lachen im Ernst, kitzeln). Mythos-Fragen („Hilft X wirklich?“) für AI72 ebenso erlaubt (Boost „8 Gläser“).
2. **Suchphrase**: so formuliert, wie Leute tippen („immer zu spät“, „kitzeln“).
3. **Echte Studie mit Zahl** (vorher→nachher oder große Stichprobe) – als **Beweis in der Mitte**, nicht als Überschrift.
4. **Share-Persona aus dem Thema** („schick's dem, der immer …“).
5. **Umsetzbarer Tipp** (TikTok „hilfreicher Beitrag“: Details, ehrlich, Ratschlag). Nicht in Themenliste (README).

## 3. Fakten
Primärquelle oder ≥ 2 unabhängige Quellen per Websuche prüfen. Unsicherheit sprachlich nennen („in einer Studie“, „meist“,
„kleine Studie“). Gesundheit: „Tut es weh / hält es an → ärztlich abklären“. Quellen nur in die Textdatei.

## 4. Skript – 20–28 s, 55–75 Wörter, 5–6 Sätze
| Beat | Zeit | Inhalt |
|---|---|---|
| 1 Hook | 0–2 s | Die „Warum du …?“-Frage bzw. überraschende Behauptung, < 1,5 s gesprochen, Suchwort drin |
| 2 Offene Schleife | 2–4 s | „Die Antwort ist nicht, was du denkst.“ / „Am Ende: was du dagegen tun kannst.“ |
| 3 Erklärung + Zahl | 4–15 s | Studie als Beweis (1 Zahl, groß im Bild) |
| 4 Aha / ehrlich | 15–20 s | Kurz-Mechanismus + Grenze („meist“, „kleine Studie“) |
| 5 Tipp | 20–25 s | 1 konkreter Satz, was man tut |
| 6 Schluss | 25–28 s | Share-Persona + Loop zurück zur Anfangsfrage; Kommentarfrage leicht beantwortbar (Ja/Nein, Zahl) |
- **Kein** gesprochener Follow-Satz mehr – nur Einblendung in der Mitte (Text + Button, 1,5 s).
- Kein „Mal angenommen …“ als langsamer Einstieg; der Kanalname steckt im Stempel.
- Aussprache: Zahlen in `say` ausschreiben, in `show` Ziffern.

## 5. Bild
- **Frame 0 = Titelbild**: Frage in **nativer Textbox** (weiß, schwarze Schrift) bzw. kg-Karte + Hauptmotiv sichtbar, nie leer.
- Bewegung ab Frame 0; neuer Bildbeat alle 2–3 s; **Kamerafahrt** (Scale 1 → 1,025–1,035) je Szene.
- Text ≥ 28 px, nur y 168–1130; Untertitel eingebrannt, Schlüsselwörter hervorgehoben.
- Zahl groß im Bild (Balken/Vergleich). Letztes Bild = Anfangsfrage (Loop).
- Vorlagen: Dark v2 `hyperframes/scenes_peakend.py`, kg `hyperframes/scenes_vitc.py`, `scenes_knacken.py`.

## 6. Technik (Reihenfolge)
1. `script.json` in `hf/aNN` bzw. `hf/bNN` (Arbeitsordner `_artifacts/malangenommen72/hf/`).
2. Stimme: `python3 ../tts_groups.py gemini-3.8-flash-tts Puck '[[0,1,2],[3,4,5]]'` (2 Requests/Video, Free-Tier 10/Tag/Modell,
   Fallbacks `gemini-3.1-flash-tts-preview`, `gemini-3.8-flash-lite-tts`; nie proben). Satzschnitte prüfen (ch/s-Ausreißer → von Hand schneiden).
3. `python3 ../assemble.py <tempo>` – Ziel Gesamtlänge ≤ 28 s (Builder hängt ~1,6 s an).
4. `hyperframes init proj_xNN --resolution portrait --non-interactive --skip-skills`; `python3 build_hf.py <ep> <proj> dark2|kg <NN> scenes_x.py`.
5. `lint` → `check --json` → `snapshot` ansehen und Fehler beheben (GSAP-Skalierung in SVG immer mit `svgOrigin`).
6. `render --quality delivery`; ffmpeg `loudnorm=I=-14:TP=-1.5:LRA=11`; fertiges MP4 Stichprobe ansehen.
7. Skript, Szenen, Caption-Datei ins Repo (`episodes/`, `hyperframes/`), Themenliste ergänzen, commit + push.

## 7. Caption
Beginnt mit der Suchphrase; 150–250 Zeichen; Kernzahl + Nutzen + Share-Persona; **genau 5 Hashtags, kein Kanalname**.
Dazu Anpinn-Kommentar (leichte Frage). Alles in Textdatei `VideoNN_Captions.txt` inkl. Quellen.

## 8. Lieferung im Chat – KURZ (Betreiber-Regel 2026-11-06)
Pro Video: **erst das Video senden (eigene Datei-Karte), direkt darunter genau EIN Kopierblock = Caption + 5 Hashtags.**
Reihenfolge: Video malangenommen72 → dessen Caption, Video AI72 → dessen Caption. Keine weiteren Blöcke, keine Erklärtexte,
kein Anpinn-Kommentar im Chat (der steht nur in der Textdatei).

## 9. Posting-Hinweise (stehen in AGENTUR.md, nur bei Änderungen erwähnen)
Titelbild = Frame 0 · „KI-generierter Inhalt“ an · Trend-Sound leise · Kommentar anpinnen · 1. Stunde antworten ·
3 beste Videos anpinnen · Bios: malangenommen72 „Psychologie-Tricks für deinen Alltag 🧠“, AI72 „Mythos-Check: Stimmt das wirklich? 🔍“.

## 10. Lernen
Nach 4–6 Videos im neuen Format: Studio-Screenshots (Ø Wiedergabe, % vollständig, Shares, Traffic, Suche) auswerten,
REICHWEITE.md ergänzen, diese Datei anpassen.

## 11. Qualitätsziel „I-Mind-Niveau“ (Betreiber-Referenz 2026-11-06, Screen-Recording, nicht im Repo)
Referenz: I-Mind „Going to bed late isn't what's hurting you“ – 24.965 Likes, 1.171 Komm., 2.988 Saves, 1.795 Shares.
Was die Qualität ausmacht und wie wir es umsetzen:
1. **Schnitt alle 1–2 s**: 12–16 Bildwechsel pro Video statt 6–7 Szenen → Szenen in Unter-Beats teilen (Zoom-in, neues Motiv, Perspektive).
2. **Ein Wort pro Moment, groß in der Bildmitte** (schmale fette Schrift, farbig, leichte Kontur), Wort-genau zur Stimme.
   Untertitel-Modus „single word center“ statt Zeilen unten.
3. **Licht & Tiefe**: Verlaufshintergründe, Rim-Light (z. B. rot/blau Kante), Glow, Partikel/Sterne, Vorder-/Hintergrund-Ebenen
   mit Parallaxe. Flache Formen bleiben, aber mit Licht.
4. **Lebendige Figuren**: Gehen, Jubeln, Kopf drehen, Blinzeln; Gegenstände reagieren (Wecker wackelt, Uhrzeit tickt hoch).
5. **Übergänge**: Lichtblitz-/Wisch-Übergang, Kamera-Push, Zahl-Enthüllung mit Ringen.
6. **Zahlen als Spektakel**: große Zahl + Masse-Visualisierung (z. B. 22.000 Figuren-Raster, Scan-Linie, Markierungskreise).
7. **Hook = Widerspruch über dich** („Spät ins Bett ist nicht dein Problem.“) – deckt sich mit „Warum du …?“-Regel.
Format bleibt 9:16 (TikTok-Vollbild). Stile Dark v2 / kg bleiben erkennbar, werden aber nach Punkt 1–6 aufgewertet.
**BETREIBER-ENTSCHEIDUNG 2026-11-06: KI-Bild-Pipeline VERWORFEN** (gefällt nicht; AI72 #13 Gähnen verworfen).
Zurück zum **alten Stil** (selbst gezeichnete SVG-Szenen: Dark v2 für malangenommen72, kg-Stil für AI72), aber **maßvoll aufgewertet**:
- mehr Bildwechsel: jede Szene in 2–3 Unter-Beats (neues Objekt, Zoom, Perspektive) → Wechsel alle ~2 s
- Kamerafahrt je Szene bleibt; dazu kurze Licht-/Wisch-Übergänge zwischen Szenen
- mehr Licht/Tiefe im eigenen Stil: Glow, weiche Lichtkegel, Partikel, Vorder-/Hintergrund-Ebenen
- Zahlen größer inszenieren (Hochzählen, Ringe, Balken)
- Untertitel wie bisher (Zeilen unten), Schlüsselwort hervorgehoben
Keine KI-Bilder, kein OpenArt/Stable Horde. `pipeline_img/` nur noch als Archiv.


## 12. Sound sauber (Betreiber 2026-11-06)
- Stimme nach `assemble.py` immer durch `hyperframes/clean_voice.sh <ep>`: Hochpass 75 Hz, Tiefpass 13,5 kHz, De-Esser, −1,5 dB @250 Hz,
  +1,5 dB @3,2 kHz (Präsenz), Kompressor 2,5:1, Limiter. Danach Build, Render, loudnorm −14 LUFS wie gehabt.
- SFX sparsam und leise (0,12–0,18): nur `click-soft`, `pop`, `whoosh-short`, `sparkle`, `chime`; keine Bass-Impacts, Glitches, Riser.
  Max. ~1 SFX pro Bildbeat, nie über der Stimme dominant.
- Bild-Upgrade im alten Stil: `FX = True` im Szenenmodul → Partikel + weicher Licht-Sweep bei jedem Szenenwechsel (`build_hf.py`),
  Kamerafahrt via `S(p, inner, dur)` aus `scenes_peakend.py` (Dark) bzw. `scenes_vitc.py` (kg), Unter-Beats je Szene, Follow-Pille als Einblendung.
