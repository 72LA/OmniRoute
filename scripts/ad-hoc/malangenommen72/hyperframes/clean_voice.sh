#!/bin/bash
# usage: clean_voice.sh <episode_dir>  – cleaner voice: rumble/hiss cut, de-ess, gentle compression, slight presence
set -e; cd "$1"; [ -f full_voice_raw.wav ] || cp full_voice.wav full_voice_raw.wav
ffmpeg -y -v error -i full_voice_raw.wav -af "highpass=f=75,lowpass=f=13500,deesser=i=0.35:m=0.5:f=0.5,equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1:g=1.5,acompressor=threshold=0.125:ratio=2.5:attack=8:release=140:makeup=1.6,alimiter=limit=0.9" -ar 24000 -ac 1 full_voice.wav
echo cleaned "$1"
