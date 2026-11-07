# HyperFrames-Pipeline (ab #05)

Seit #05 werden die Videos mit **HyperFrames** (HeyGen, Apache-2.0) gerendert: HTML + GSAP → MP4.
Plugin: `/plugin marketplace add heygen-com/hyperframes` und `/plugin install hyperframes@hyperframes`.
CLI über den Plugin-Launcher: `HF="node <PLUGIN_ROOT>/skills/hyperframes/scripts/plugin-cli.mjs"`
(`<PLUGIN_ROOT>` = `~/.claude/plugins/marketplaces/hyperframes`).

Ablauf pro Video (Episoden-Ordner mit `script.json`):

```bash
# 1) Stimme (Gemini "Puck") + Zeitmarken – Skripte aus ../engine
python3 ../engine/tts_groups.py gemini-3.8-flash-lite-tts Puck '[[0,1,2,3],[4,5,6]]'
python3 ../engine/assemble.py 1.05            # -> full_voice.wav, segs_abs.json
# 2) Projekt anlegen (einmal) und bauen
$HF init proj --resolution portrait --non-interactive --skip-skills --skill hyperframes
python3 build_hf.py <episode_dir> proj line 05 scenes_luegen.py     # Dark  = malangenommen72
python3 build_hf.py <episode_dir> proj flat 05 scenes_kitzeln.py    # Wissen = AI72
# 3) Prüfen, ansehen, rendern
cd proj && $HF lint && $HF check --json && $HF snapshot --at 1,8,15
$HF render --quality delivery -o out.mp4
# 4) Lautheit für TikTok
ffmpeg -i out.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k final.mp4
```

Szenen-Modul: `SCENES = {name: fn(prefix, dur, lead) -> (html, js)}`, `TITLES`, `KEYS`, `SFX`.
Dark-Stil: SVG-Pfade mit `pathLength="1"`, Strich-Animation über `strokeDashoffset 1 → 0`.
Wissens-Stil: flache SVG-Formen mit dunkler Kontur + Schlagschatten, `back.out`-Pops.
Sicherer Bereich (TikTok): Text nur zwischen y 168 und 1330 px; Untertitel bei y ≈ 1150.
Soundeffekte: mitgelieferte HyperFrames-Dateien (`media-use/audio/assets/sfx`), keine Musik (kommt in der App dazu).
