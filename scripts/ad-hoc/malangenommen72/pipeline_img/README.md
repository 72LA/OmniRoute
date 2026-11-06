# Bild-Pipeline (ab #14 / AI72 #13) – I-Mind-Niveau mit kostenlosen Werkzeugen

1. **Bilder**: `horde_batch.py prompts.json outdir 6` – Stable Horde (kostenlos, anonymer Key `0000000000`),
   Modell „Juggernaut XL“ (SDXL), 576×1024 + `RealESRGAN_x2plus` → 1152×2048. Dauer ~9 min/Bild, 6 parallel.
   Getestet und verworfen: Pollinations anonym (geringe Auflösung, Wasserzeichen).
   Stil-Präfixe in `prompts_1314.json`: **A = dunkel** (Schwarz/Mitternachtsblau, rot-weißes Randlicht, gesichtslose Silhouetten)
   für malangenommen72, **B = vivid** (Indigo/Lila, Türkis/Magenta/Gelb, eigene Figur mit lila Haaren + türkisem Hoodie) für AI72.
   Keine Texte im Bild (Negativ-Prompt), keine fremden Figuren/Marken.
2. **Stimme**: wie bisher (`tts_groups.py`, `assemble.py`).
3. **Build**: `python3 build_img.py <ep> <proj> dark|vivid "<STEMPEL>" beats_x.py <bilder>` – Beats an Wörter gekoppelt (`at: (satz, wort)`),
   Kamerafahrten (push/pull/pan/up/down), Lichtblitz-Schnitte + Whoosh, Partikel, Vignette, Hook-Textbox (Titelbild),
   Follow-Pille, Loop-Box am Ende, **ein großes Wort pro Moment** (Anton, Schlüsselwörter hervorgehoben), Zahlen-Overlays.
   Schrift `fonts/Anton-Regular.ttf` (OFL, Google Fonts) liegt im Arbeitsordner `hf/fonts/`.
4. lint → snapshot → render → loudnorm wie gehabt.

## Erfahrungen (2026-11-06)
- Dunkler Stil (A) mit Juggernaut XL: 11/11 Bilder gut. Vivid (B): Gruppen-/Objekt-Motive liefen oft als **Musterflächen** aus
  (bestimmte Rechner, z. B. „dumbstupid_SDXL*“, „gn100-oxygen-janken“, „Neon_Nexus*“). `horde_batch.py` prüft jetzt jedes Bild
  (Anteil glatter Fläche < 0,6 = Müll → löschen, Rechner sperren, neu). Gute Illustrationen liegen bei 0,72–0,95.
- „Nova Flat XL“ wurde komplett zensiert (unbrauchbar). AlbedoBase XL 3.1 ebenfalls Müll-anfällig.
- Vivid-Prompts immer mit der AI72-Figur beschreiben (Einzelfigur funktioniert, Gruppen/Gehirn/Wissenschaftler nicht) → Motive so planen.
- Plan B: gute Bilder mehrfach nutzen (andere Kamerafahrt + Zahlen-Overlay), wie in AI72 #13.
