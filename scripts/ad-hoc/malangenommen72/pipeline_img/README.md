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
