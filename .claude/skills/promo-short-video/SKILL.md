---
name: promo-short-video
description: >-
  Create a vertical 9:16 promotional short video (for YouTube Shorts / Instagram
  Reels / TikTok) entirely from code — an animated HTML "engine" rendered
  frame-by-frame and encoded to a ready-to-post MP4 with background music. Use
  this whenever the user wants a promo/ad short, a "宣伝ショート", a quote/wisdom
  reel, a teaser or trailer clip, a continuation of an existing short-video
  series, or an English/other-language version of one — for a product, game,
  site, or campaign. Triggers on requests like "宣伝動画/ショート作って", "続きのshort動画",
  "英語版の宣伝動画", "make a promo reel", "turn these quotes into a short". Produces
  a real .mp4 (1080×1920, H.264+AAC), plus the editable HTML source. Prefer this
  over ad-hoc screen recording — it renders deterministically with no white
  pre-roll and exact timing.
---

# Promo Short Video (vertical 9:16, code-only)

Build a promotional short as a single self-contained HTML page whose entire look
is a pure function of time, then render it deterministically to an MP4 with music.
No video editor, no live screen recording.

Read the companion knowledge doc for the philosophy and the ethics rules:
`knowledge/promo-short-video-blueprint.md` (in this repo). The short version:
**only use verified, sourced quotes; show the source on screen; promise only the
truth.** This matters — putting invented words in a real person's mouth destroys
the trust the video is meant to build.

## The pipeline (4 steps)

1. **Write the scenes** — decide the arc (hook → series badge → [worry → answer]×3
   → summary → CTA), ~30–40s total. One theme per video. Pull quotes from a
   verified source (e.g. a game's own dataset), keeping the on-screen citation.
2. **Generate the HTML** — use `assets/short_template.html` as the engine and fill
   in the scene array + brand tokens. The engine exposes `window.renderAt(t)` and
   `window.TOTAL`, and supports two modes:
   - normal load → real-time playback with BGM (a **▶ Play** button); the user can
     watch or screen-record it directly.
   - `?capture=1` → no autoplay; you drive it via `renderAt(ms)` for frame export.
3. **Capture frames** — `scripts/capture_frames.js` opens `?capture=1` in headless
   Chromium and screenshots one JPEG per frame at 30fps by calling `renderAt`.
4. **Encode** — `scripts/render_short.sh` muxes the JPEG sequence with the BGM into
   H.264(yuv420p)+AAC, `+faststart`, audio faded in/out. Output is post-ready.

Steps 3–4 are automated: `bash scripts/render_short.sh <page-slug> <bgm-path>`.

## Quick start

```bash
# 0) one-time tooling (full ffmpeg with H.264/AAC + headless driver)
pip install imageio-ffmpeg >/dev/null
npm install playwright-core --no-save >/dev/null   # Chromium at /opt/pw-browsers/chromium-*/chrome-linux/chrome

# 1) author page.html from assets/short_template.html (fill SCENES + brand)
# 2) render (serves cwd, captures 30fps, encodes with BGM):
bash .claude/skills/promo-short-video/scripts/render_short.sh page path/to/bgm.mp3
# -> writes page.mp4 (1080x1920, ~40s, music, ready to upload)
```

## Authoring the scenes

The template's `<script>` has a `const scenes = [ {d, html}, ... ]` array. Each entry
is one beat: `d` is its duration in ms, `html` is the scene markup using the
provided classes. Helper classes available: `.lead` (hook), `.kicker`+`.ep-title`
(series badge), `.q-tag`+`.worry` (the problem), `.sage-name`+`.sage-era`+`.quote`
(+`.quote.sm` for long ones)+`.src` (the answer + citation), `.names`+`.names .big`
(roster), and the CTA block (`.cta-title`/`.cta-jp`/`.cta-sub`/`.cta-url`/`.cta-free`).

For a multi-video campaign, don't hand-write each file — write a small generator
like `scripts-gen/gen_en_shorts.py` (in this repo) that holds a shared engine and
one scene-list per episode, and emits all the HTML files. This keeps a series
visually consistent and trivial to re-render after copy edits.

## Brand tokens

Change these near the top of the template's CSS to re-skin: `--bg-dark` (background),
`--gold`/`--amber` (accents), `--white` (text); the display font (serif) and label
font (sans); and the central flame element. Defaults are the warm "lamp of wisdom"
palette. Match the destination site so the video feels like part of it.

## Why deterministic rendering (don't skip this)

Live headless screen-recording in this environment produces ~13s of white pre-roll
and stretches a 39s timeline to ~53s — unusable. Driving `renderAt(t)` one frame at
a time gives exact timing and zero pre-roll. For the same reason, the flame and
embers are animated inside `renderAt` (math on `t`), **not** CSS keyframes — inline
styles set each frame would otherwise fight a running CSS animation.

## Gotchas (environment)

- The ffmpeg bundled with Playwright is VP8-only with no audio/H.264 encoder. Always
  use the `imageio-ffmpeg` binary (`python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"`).
- Google Fonts are blocked by the proxy, but the browser's serif/CJK fallback renders
  cleanly — the output looks right without them. Don't block on font loading.
- Launch Chromium with `--no-sandbox`. Path: `/opt/pw-browsers/chromium-*/chrome-linux/chrome`.
- Deliver the finished `.mp4` to the user (e.g. `SendUserFile`), and commit both the
  `.mp4` and the `.html` source so the video is reproducible and editable later.

## Files

- `assets/short_template.html` — the unified engine (CSS + `renderAt` + playback).
  Copy it, fill the `scenes` array and brand tokens, save as `<slug>.html`.
- `scripts/capture_frames.js` — Playwright frame exporter (`node capture_frames.js <url> <outdir> [fps]`).
- `scripts/render_short.sh` — end-to-end: capture + encode with BGM. `render_short.sh <slug> <bgm> [port]`.
