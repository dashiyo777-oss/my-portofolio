# -*- coding: utf-8 -*-
"""「Give Us Back the Sky / Rolloing all stars」 — English-caption promo short (~26s).

Same open-cloudscape / soaring-eagle scene as gen_giveusbacksky (imported: CSS + ENGINE
+ BODY), with the on-screen copy in English set in an elegant serif. On-screen text is
limited to verified cover text (title / artist) plus generic labels and evocative promo
copy — no invented lyrics. BGM: sky-bgm.mp3.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_giveusbacksky as g       # exposes CSS + ENGINE + BODY (also regenerates the JP short; harmless)
OUT = os.path.dirname(HERE)

CSS = g.CSS + r"""
  .en{font-family:'Playfair Display',serif;font-size:64px;line-height:1.46;font-weight:600;color:#fff;letter-spacing:.01em;
    text-shadow:0 2px 22px rgba(20,44,80,.95),0 0 46px rgba(30,70,120,.7)}
  .en .em{color:#ffe08a}
  .enbig{font-family:'Playfair Display',serif;font-weight:700;font-size:100px;line-height:1.12;color:#fff;letter-spacing:.01em;
    display:inline-block;text-shadow:0 3px 24px rgba(20,44,80,1),0 0 56px rgba(255,224,150,.55)}
"""

D = [3200, 5200, 5400, 6200, 6400]
S4 = D[0]+D[1]+D[2]
BLOOM_FROM = S4 + 2500
BLOOM_PEAK = S4 + D[3] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="en">Those wings still<br>remember —</div></div>'),
    (D[2], '<div class="scene mid"><div class="en">how it felt<br><span class="em">to be free.</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="en">So someday, please —<br><span class="enbig">give us back<br>the sky.</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:300px">'
           '<div class="title">Give Us Back<br>the Sky</div>'
           '<div class="orn"><i></i><b>&#10022;</b><i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Give Us Back the Sky / Rolloing all stars (Promo Short — EN)",
  desc="Those wings still remember how it felt to be free. So someday, please — give us back the sky. Rolloing all stars — new single.")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Playfair+Display:wght@600;700&family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
{g.BODY}
</div></div>
<audio id="bgm" src="sky-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "giveusbacksky-en-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote giveusbacksky-en-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
