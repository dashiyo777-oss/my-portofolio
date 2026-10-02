# -*- coding: utf-8 -*-
"""「花束の重さ / 水野灯」 — Lyric video (vertical, ~65s).
Reuses the night-train scene from gen_mizuno3 (imported) with a darker scrim, and
flows more of the (rights-holder-supplied) lyrics as elegant typography: Verse 1 →
Pre-Chorus → Chorus → the closing line. Paced to the music (not karaoke-synced).
BGM: hanataba-lyric-bgm.mp3 (65s segment).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_mizuno3 as g            # exposes CSS + ENGINE (also regenerates the Short; harmless)
OUT = os.path.dirname(HERE)

# darker scrim for readability + a touch larger lyric type
CSS = g.CSS + r"""
  #scrim{position:absolute;inset:0;background:rgba(6,4,2,.52);pointer-events:none;z-index:9}
  .lyric{font-size:66px!important;line-height:1.78!important}
  .lyric.sm{font-size:56px!important}
"""

def L(html, cls=""):   # a centered lyric beat
    return f'<div class="scene mid"><div class="lyric {cls}">{html}</div></div>'

scenes = [
    (4800, '<div class="scene mid"><div class="title" style="text-align:center">花束の重さ</div>'
           '<div class="orn c" style="justify-content:center;margin-top:20px"><i></i><b>&#10070;</b><i></i></div>'
           '<div class="artist" style="text-align:center;margin-top:10px">水野灯</div></div>'),
    (5000, L('送別会の、<br>帰りの電車。')),
    (5200, L('膝の上の 花束が、<br>重い。')),
    (6000, L('窓に映る、<br>少し老けた顔。<br><span class="sm" style="color:#d8c9a2">四十年 こんな顔だったか。</span>', 'sm')),
    (6000, L('謝る機会は、<br>もう来ない。<br><span class="em">それでも 忘れずに 持っていく。</span>', 'sm')),
    (5600, L('ここまで来られたのは、<br>私の力じゃない。', 'sm')),
    (5400, L('黙って 尻ぬぐいを<br>してくれた人。', 'sm')),
    (5400, L('理不尽な私を、<br>見捨てなかった人。', 'sm')),
    (5400, L('その顔が ひとつずつ、<br>浮かんでくる。', 'sm')),
    (6000, L('花束の重さは、<br><span class="em">そういう重さだ。</span>')),
    (6200, L('<span class="em">ありがとう、</span>と声に出して。<br>明日から また、<br>何かを始めよう。', 'sm')),
    (4000, '<div class="scene mid"><div class="artist" style="text-align:center;font-size:44px">花束の重さ</div>'
           '<div class="rome" style="text-align:center;margin-top:14px">水野灯 &middot; AKARI MIZUNO</div>'
           '<div class="tag" style="margin-top:22px">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="花束の重さ / 水野灯 (Lyric Video)")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = g.ENGINE.replace("SCENES", scenes_js)

BODY = r"""
  <div id="win"><div id="redtower"></div><div id="wref"></div></div>
  <div id="winframe"></div>
  <div id="sill"></div>
  <div id="seat"></div>
  <div id="bag"></div>
  <div id="bqglow"></div>
  <div id="manrim"></div>
  <div id="man"><div id="m-hair" class="mp"></div><div id="m-head" class="mp"></div><div id="m-body" class="mp"></div></div>
  <div id="wrap-paper"></div>
  <div id="ribbon"></div>
  <div id="rain"></div>
  <div id="scrim"></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="vig"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">水野灯 &middot; AKARI MIZUNO</div>
    <h1>花束の重さ</h1>
    <p>Lyric Video</p>
    <button id="play">&#9654; Play</button>
  </div>
"""

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
{BODY}
</div></div>
<audio id="bgm" src="hanataba-lyric-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "hanataba-lyric.html"), "w", encoding="utf-8").write(html)
print(f"wrote hanataba-lyric.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
