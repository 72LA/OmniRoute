# Agentur-Handbuch – Produktionsfirma für malangenommen72 + AI72 (Stand 2026-11-05)

Jede Produktion durchläuft **alle Abteilungen nacheinander**. Jede Abteilung hat ein Ergebnis und ein
**Gate**: Wer das Gate nicht besteht, geht zurück. Ergänzt `README.md` (Stil, Technik) und
`REICHWEITE.md` (Algorithmus, Checkliste). Videos werden **nur auf „Go“** produziert.

## Abteilungen

| # | Abteilung | Ergebnis | Gate (muss erfüllt sein) |
|---|---|---|---|
| 1 | **Strategie & Trends** | Thema + Format + Suchbegriff | Thema hat (a) Suchwort, das Leute tippen, (b) konkreten Nutzen, (c) Share-Grund mit Person („schick's dem …“). Nicht in der Themenliste. |
| 2 | **Recherche & Faktencheck** | Quellenliste (nur Betreiber) | Jede Zahl aus Primärquelle oder ≥ 2 unabhängigen Quellen. Grenzen benennen (kleine Stichprobe, selbst berichtet, Effekt meist kleiner). Gesundheit: „ärztlich abklären“-Satz. |
| 3 | **Skript & Hook** | `script.json` (110–125 Wörter) | Hook ≤ 1,5 s mit Suchwort; offene Schleife in 5 s; genau 1 Follow-Aufruf in der Mitte; Zahl vorher→nachher; umsetzbarer Schluss; Speicher-Aufruf; Share-Persona; Schluss führt zum Anfang. |
| 4 | **Art Direction** | Szenenplan | Kanalstil (Dark v2 / kg); **Frame 0 = Cover** mit Kernaussage in **nativer Textbox** (weiß, schwarze Schrift); neuer Bildbeat alle 2–4 s; Text nur in y 168–1130; nur eigene Figuren. |
| 5 | **Motion & Schnitt** | HyperFrames-Projekt | `lint` 0 Fehler, `check` ok, Snapshots angesehen; keine Pause > 0,4 s; Länge **35–45 s**; **langsame Kamerafahrt** (Scale 1 → 1,025–1,035) in jeder Szene, damit nie Standbild entsteht (ab #13/#12, Vorlage `scenes_peakend.py` / `scenes_vitc.py`). |
| 6 | **Voice & Sound** | Stimme + SFX | Gemini „Puck“, max. 2 Requests pro Video; −14 LUFS; keine Musik im MP4. |
| 7 | **SEO & Caption** | Caption-Block | Beginnt mit Suchphrase; 150–300 Zeichen; Kernzahl + Nutzen + Aufruf; **genau 5 Hashtags**; **kein Kanalname**; im Chat je Video **ein Kopier-Codeblock**. |
| 8 | **Community** | Anpinn-Kommentar + Antwortplan | Kommentar-Frage, die leicht zu beantworten ist; in der 1. Stunde auf Kommentare antworten; gute Fragen → „Mit Video antworten“ = nächstes Thema. |
| 9 | **Veröffentlichung** | Posting-Checkliste | siehe unten |
| 10 | **Analytics** | Auswertung nach 48 h | Screenshots aus TikTok Studio → Entscheidung pro Video (Hook/Szene/Thema). |
| 11 | **Recht & Compliance** | Freigabe | Eigene Grafiken/Figuren, keine fremden Marken; KI-Kennzeichnung; keine Heilversprechen; Kommentarfilter bei sensiblen Themen. |

## Posting-Checkliste (für den Betreiber)
1. Video hochladen, **Titelbild = Frame 0** wählen (Kernfrage/Textbox).
2. Caption-Block per „Kopieren“ einfügen.
3. Sound in der App: Trend-Sound **leise** (ca. 5–10 %) unter die Stimme legen – Stimme muss klar bleiben.
4. Unter „Weitere Optionen“ **„KI-generierter Inhalt“ einschalten** (die Stimme ist synthetisch; TikTok verlangt
   eine Kennzeichnung realistischer KI-Inhalte – schützt vor Reichweiten-Strafen).
5. Bei sensiblen Themen Kommentarfilter an.
6. Nach dem Posten: vorbereiteten Kommentar schreiben und **anpinnen**; in der ersten Stunde antworten.
7. Zeitpunkt: gleiche Uhrzeit, regelmäßig; die beste Stunde steht in TikTok Studio → Follower → Aktivität.
8. Serie: AI72-Mythos-Checks in eine Playlist „Mythos-Check“ (falls die Funktion im Konto verfügbar ist).

## Referenzanalyse 2026-11-05 (Betreiber-Screenshots/Videos, nicht im Repo)

| Referenz | Zahlen | Was funktioniert | Übernommen als |
|---|---|---|---|
| **Eigener Beitrag „8 Gläser Wasser?“** – von TikTok **geboostet** (+399 Aufrufe, „sehr hilfreich“) | – | Mythos als Frage, große Studie (5.000+ Menschen), Alltagsrat (Tee/Obst/Suppe zählen, Durst meldet sich) | **AI72-Serie „MYTHOS-CHECK“** (ab #11) |
| **Strix – „Jede psychische Störung erklärt“** | 14.441 Likes · 3.530 Saves (24 %) · 2.204 Shares | Liste/Serie, 1 Maskottchen pro Punkt, Suchwort im Titel, Nachschlage-Wert → Saves | Format „Jede/r X erklärt“ als Mehrteiler (Teil 1/3) einplanen |
| **cryothum – Sparschwein an Kette** | 60.947 Likes · 15.566 Saves (26 %) · 4.498 Shares | Dark-Line-Art (= unser Dark v2), Contrarian-Satz in nativer Textbox, Geld/Mindset, Caption 1 Satz + 5 Hashtags | **Native Textbox im Cover**, Contrarian-Hooks („Motivation bringt fast nichts“) |
| **EndzeitAkten – Aufzug-Rätsel** | 13.118 Likes · 2.097 Saves · 2.002 Shares | Frage-Karte oben, Kommentar-Antworten | AI72-Rätsel beendet (Betreiber); Frage-Karte oben bleibt |

Muster: **Saves** kommen von Nachschlage-Wissen (Listen, Zahlen, Anleitungen), **Shares** von einer konkreten
Person, an die man denkt (Share-Persona, Regel aus `REICHWEITE.md`).

**Ausgeschlossen (Betreiber 2026-11-05):** Das „Wer würde eher …?“-Paar-Quiz (LiebesQuiz) ist **keine** Referenz –
nicht analysieren, nicht übernehmen. Jedes Video braucht beides: einen Grund zum Speichern und einen Menschen zum Schicken.
