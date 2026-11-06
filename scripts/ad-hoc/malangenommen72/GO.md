# GO-Ablauf – verbindlich, sobald der Betreiber „Go“ schreibt (Stand 2026-11-06)

Diese Datei ist die **eine Quelle** für jede Produktion. Sie vereint alte Regeln, die funktioniert haben
(Boosts „8 Gläser Wasser“ und „Fuß in der Tür“, Top-Videos „Warum du …?“), mit den neuen Regeln aus der
Studio-Auswertung (REICHWEITE.md §7–8). Details: README.md (Technik/Stil), AGENTUR.md (Abteilungen), IDEEN.md (Themen).

## 0. Ohne „Go“ nichts produzieren
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

## 8. Lieferung im Chat – KURZ
Nur: **Video 1 + Caption-Kopierblock, Video 2 + Caption-Kopierblock** (+ Anpinn-Kommentar im selben Block). Keine langen Texte.

## 9. Posting-Hinweise (stehen in AGENTUR.md, nur bei Änderungen erwähnen)
Titelbild = Frame 0 · „KI-generierter Inhalt“ an · Trend-Sound leise · Kommentar anpinnen · 1. Stunde antworten ·
3 beste Videos anpinnen · Bios: malangenommen72 „Psychologie-Tricks für deinen Alltag 🧠“, AI72 „Mythos-Check: Stimmt das wirklich? 🔍“.

## 10. Lernen
Nach 4–6 Videos im neuen Format: Studio-Screenshots (Ø Wiedergabe, % vollständig, Shares, Traffic, Suche) auswerten,
REICHWEITE.md ergänzen, diese Datei anpassen.
