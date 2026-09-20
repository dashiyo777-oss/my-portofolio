#!/usr/bin/env bash
# End-to-end render of a promo short: capture deterministic frames, then encode to
# a post-ready MP4 (H.264 + AAC) with the given BGM faded in/out.
#
# Usage: render_short.sh <slug> <bgm-path> [port] [fps]
#   <slug>  : basename of "<slug>.html" in the CURRENT directory (served over http)
#   <bgm>   : path to a background-music file (mp3/m4a/etc.)
#   [port]  : local http port (default 8099)
#   [fps]   : frames per second (default 30)
# Output: ./<slug>.mp4
#
# Requires: python3, node + playwright-core, and imageio-ffmpeg (pip).
set -euo pipefail

SLUG="${1:?usage: render_short.sh <slug> <bgm> [port] [fps]}"
BGM="${2:?need a bgm path}"
PORT="${3:-8099}"
FPS="${4:-30}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"; [ -n "${SRV:-}" ] && kill "$SRV" 2>/dev/null || true' EXIT

[ -f "${SLUG}.html" ] || { echo "no ${SLUG}.html in $(pwd)"; exit 1; }
[ -f "$BGM" ] || { echo "bgm not found: $BGM"; exit 1; }

# full-featured ffmpeg (the bundled Playwright ffmpeg lacks H.264/AAC)
FF="$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
[ -x "$FF" ] || { echo "install ffmpeg: pip install imageio-ffmpeg"; exit 1; }

# serve cwd so the page can load its assets/BGM by relative path
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SRV=$!
sleep 1

echo "capturing frames -> $WORK/frames"
META="$(node "$SKILL_DIR/scripts/capture_frames.js" \
        "http://localhost:${PORT}/${SLUG}.html?capture=1" "$WORK/frames" "$FPS")"
FRAMES="$(ls "$WORK/frames"/*.jpg | wc -l | tr -d ' ')"
DUR="$(python3 -c "print(round($FRAMES/$FPS,3))")"
FADE="$(python3 -c "print(round($DUR-1.5,2))")"
echo "  $FRAMES frames -> ${DUR}s"

echo "encoding -> ${SLUG}.mp4"
"$FF" -y -framerate "$FPS" -i "$WORK/frames/f%05d.jpg" -i "$BGM" -t "$DUR" \
  -filter_complex "[1:a]afade=t=in:st=0:d=1.2,afade=t=out:st=${FADE}:d=1.5,volume=0.8[a]" \
  -map 0:v -map "[a]" \
  -c:v libx264 -pix_fmt yuv420p -crf 19 -preset medium -movflags +faststart \
  -c:a aac -b:a 160k -ar 44100 \
  "${SLUG}.mp4" >/dev/null 2>&1

echo "done: ${SLUG}.mp4 (1080x1920, ${DUR}s, H.264+AAC)"
