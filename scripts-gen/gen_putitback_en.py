# -*- coding: utf-8 -*-
"""「Put It Back / Rolloing all stars」 — English-caption promo short (vertical 9:16, ~26s).

Same golden-hour scene as gen_putitback (imported: CSS + ENGINE), with the on-screen
copy in English set in an elegant serif. On-screen text is limited to verified cover
text (title / artist / the cover tagline "Music for a Brighter Tomorrow") plus generic
labels and evocative promo copy — no invented lyrics.

BGM: putitback-bgm.mp3 (same 30s climax segment).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_putitback as g          # exposes CSS + ENGINE + EARTH (also regenerates the JP short; harmless)
OUT = os.path.dirname(HERE)

# English serif lyric type on top of the shared scene CSS
CSS = g.CSS + r"""
  .en{font-family:'Playfair Display',serif;font-size:66px;line-height:1.5;font-weight:600;color:#fff6e6;letter-spacing:.01em;
    text-shadow:0 2px 24px rgba(8,12,26,.98),0 0 44px rgba(20,20,40,.6)}
  .en .em{color:#ffd77e}
  .enbig{font-family:'Playfair Display',serif;font-weight:700;font-size:104px;line-height:1.16;color:#fff;letter-spacing:.01em;
    display:inline-block;text-shadow:0 3px 26px rgba(10,12,28,1),0 0 56px rgba(255,206,120,.5)}
"""

# scene timeline (mirror the JP cut)
D = [3200, 5200, 5400, 6200, 6400]
S4 = D[0]+D[1]+D[2]
BLOOM_FROM = S4 + 2500
BLOOM_PEAK = S4 + D[3] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="en">The sun sets low —<br>but it&rsquo;s not the end.</div></div>'),
    (D[2], '<div class="scene mid"><div class="en">Seasons turn,<br><span class="em">and life comes back.</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="en">So, once more —<br><span class="enbig">put it back.</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:318px">'
           '<div class="title">Put It<br>Back</div>'
           '<div class="orn"><i></i>' + g.EARTH + '<i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="hand" style="margin-top:20px">Music for a Brighter Tomorrow</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Put It Back / Rolloing all stars (Promo Short — EN)",
  desc="The sun sets low, but it's not the end. Seasons turn, and life comes back. Rolloing all stars — new single \"Put It Back\". Music for a Brighter Tomorrow.")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (g.ENGINE.replace("SCENES", scenes_js)
          .replace("BLOOMFROM", str(BLOOM_FROM)).replace("BLOOMPEAK", str(BLOOM_PEAK)))

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@600&family=Playfair+Display:wght@600;700&family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="world">
    <div id="sky"></div>
    <div id="rg1" class="ridge"></div>
    <div id="rg2" class="ridge"></div>
    <div id="rg3" class="ridge"></div>
    <div id="sunglow"></div>
    <div id="rays"></div>
    <div id="sun"></div>
    <div id="haze"></div>
    <div id="lake"></div>
    <div id="sunref"></div>
    <div id="fg"></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">Rolloing all stars</div>
    <h1>Put It Back</h1>
    <p>Music for a Brighter Tomorrow</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="putitback-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "putitback-en-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote putitback-en-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
