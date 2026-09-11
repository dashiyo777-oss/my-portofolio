# -*- coding: utf-8 -*-
"""「Put It Back / Rolloing all stars」 — English-caption promo short (~26s).

Same cosmic Earth scene as gen_putitback (imported: CSS + ENGINE + BODY), with the
on-screen copy in English set in an elegant serif. On-screen text is limited to verified
cover text (title / artist / the cover tagline "Music for a Brighter Tomorrow") plus
generic labels and evocative promo copy. BGM: putitback-bgm.mp3.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_putitback as g          # exposes CSS + ENGINE + BODY (also regenerates the JP short; harmless)
OUT = os.path.dirname(HERE)

CSS = g.CSS + r"""
  .en{font-family:'Playfair Display',serif;font-size:66px;line-height:1.5;font-weight:600;color:#f4f8ff;letter-spacing:.01em;
    text-shadow:0 2px 22px rgba(2,6,20,.98),0 0 46px rgba(40,80,160,.7)}
  .en .em{color:#8fd0ff}
  .enbig{font-family:'Playfair Display',serif;font-weight:700;font-size:104px;line-height:1.14;color:#fff;letter-spacing:.01em;
    display:inline-block;text-shadow:0 3px 24px rgba(2,6,20,1),0 0 56px rgba(150,205,255,.55)}
"""

D = [3200, 5200, 5400, 6200, 6400]
S4 = D[0]+D[1]+D[2]
BLOOM_FROM = S4 + 2500
BLOOM_PEAK = S4 + D[3] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="en">One small<br>blue planet.</div></div>'),
    (D[2], '<div class="scene mid"><div class="en">Wounded,<br><span class="em">still turning.</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="en">So, once more —<br><span class="enbig">put it back.</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:250px">'
           '<div class="title">Put It<br>Back</div>'
           '<div class="orn"><i></i><b>&#10022;</b><i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="hand" style="margin-top:18px">Music for a Brighter Tomorrow</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Put It Back / Rolloing all stars (Promo Short — EN)",
  desc="One small blue planet. Wounded, still turning. So, once more — put it back. Rolloing all stars — Music for a Brighter Tomorrow.")

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
{g.BODY}
</div></div>
<audio id="bgm" src="putitback-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "putitback-en-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote putitback-en-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
