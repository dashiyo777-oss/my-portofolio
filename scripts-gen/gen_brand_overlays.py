#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_brand_overlays.py
Sora2 等の実写・外部動画に「重ねるだけ」で Leo Music ブランドを統一するための
透過PNGオーバーレイ素材を生成する再利用ツール。

出力（いずれも 1080x1920・背景透過PNG）:
  <slug>-ov-title.png   手描き風マルチカラーのタイトルロックアップ（上部）＋アーティスト
  <slug>-ov-logobug.png Leo Music 丸ロゴバグ＋「LEO MUSIC」（左下・全編に重ねる想定）
  <slug>-ov-cta.png     締めのCTAエンドカード（やわらかいスクリム＋NEW SONG/タイトル/配信中・Streaming Now/LEO MUSIC＋ロゴバグ）

使い方:
  python3 scripts-gen/gen_brand_overlays.py \
      --slug colors --title "Colors at the Door" --artist "w-Band" \
      --accent "#ffd23d" --accent2 "#ff9a3c" --logo left --port 8170

重ね方（CapCut等）: 下記 README を参照。
"""
import argparse, os, subprocess, sys, time, socket, signal

def free_port(start):
    s = socket.socket();
    try:
        s.bind(("127.0.0.1", start)); s.close(); return start
    except OSError:
        s.close();
        for p in range(start+1, start+60):
            t = socket.socket()
            try:
                t.bind(("127.0.0.1", p)); t.close(); return p
            except OSError:
                t.close()
        raise SystemExit("no free port")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--artist", required=True)
    ap.add_argument("--accent", default="#ffd23d")
    ap.add_argument("--accent2", default="#ff9a3c")
    ap.add_argument("--logo", default="left", choices=["left", "right"])
    ap.add_argument("--port", type=int, default=8170)
    a = ap.parse_args()

    root = os.getcwd()
    html_name = f"{a.slug}-overlay.html"
    html_path = os.path.join(root, html_name)

    if a.logo == "left":
        logo_css = "left:46px"; tag_css = "left:188px"
    else:
        logo_css = "right:46px"; tag_css = "right:188px"

    ACC, ACC2 = a.accent, a.accent2

    HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<title>__SLUG__ brand overlay</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,600&family=Kaushan+Script&family=Noto+Serif+JP:wght@500;600&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent}
#stage{position:fixed;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:"EB Garamond","Noto Serif JP",serif}
.layer{display:none}
.layer.on{display:block}

/* ---------- TITLE ---------- */
#title{position:absolute;left:60px;right:60px;top:196px}
.brush{font-family:"Kaushan Script",cursive;font-size:150px;line-height:1.02;
  background:linear-gradient(95deg,#ff5fa2 0%,#ff8a3c 26%,#ffd23d 46%,#8fd0ff 68%,#ffffff 90%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 3px 2px rgba(0,0,0,.45)) drop-shadow(0 8px 26px rgba(0,0,0,.55))}
.brush .s{ -webkit-text-stroke:0}
.t-artist{margin-top:10px;font-family:"EB Garamond",serif;font-weight:600;font-size:54px;
  letter-spacing:14px;color:#fff;text-shadow:0 2px 4px rgba(0,0,0,.5),0 6px 22px rgba(0,0,0,.6)}

/* ---------- LOGO BUG ---------- */
#logobug{position:absolute;__LOGO__;bottom:46px;width:124px;height:124px;border-radius:50%;
  overflow:hidden;box-shadow:0 0 0 3px rgba(255,220,150,.5),0 6px 16px rgba(0,0,0,.5);opacity:.95}
#logobug img{position:absolute;left:-14%;top:-10%;width:128%;height:128%;object-fit:cover}
#logotag{position:absolute;__TAG__;bottom:70px;font-family:"EB Garamond",serif;font-weight:600;
  font-size:34px;letter-spacing:5px;color:#f7ecd6;opacity:.9;text-shadow:0 2px 8px rgba(0,0,0,.7)}

/* ---------- CTA ---------- */
#scrim{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(10,6,2,0) 30%,rgba(10,6,2,.42) 58%,rgba(10,6,2,.72) 100%)}
#cta{position:absolute;left:30px;right:30px;top:560px;text-align:center}
.badge{display:inline-block;font-family:"EB Garamond",serif;font-weight:600;font-size:32px;
  letter-spacing:7px;color:#2a1704;background:linear-gradient(90deg,__ACC__,__ACC2__);
  padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-t{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-style:italic;
  font-size:104px;line-height:1.02;color:#fff;
  text-shadow:0 0 28px rgba(255,200,120,.6),0 5px 20px rgba(10,6,2,.7)}
.cta-a{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:500;font-size:50px;
  letter-spacing:12px;color:#f3ead6;margin-top:14px;text-shadow:0 2px 12px rgba(10,6,2,.8)}
.cta-s{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-size:40px;
  letter-spacing:3px;color:__ACC__;margin-top:22px}
.cta-b{font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:10px;
  color:#f3ead6;margin-top:12px;opacity:.92}
</style></head>
<body>
<div id="stage">
  <div class="layer" id="L-title">
    <div id="title"><div class="brush">__TITLE__</div><div class="t-artist">__ARTIST__</div></div>
  </div>
  <div class="layer" id="L-logobug">
    <div id="logobug"><img src="leo-music-logo.png"></div><div id="logotag">LEO MUSIC</div>
  </div>
  <div class="layer" id="L-cta">
    <div id="scrim"></div>
    <div id="cta"><span class="badge">NEW SONG</span>
      <div class="cta-t">__TITLE__</div><div class="cta-a">__ARTIST__</div>
      <div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
    <div id="logobug"><img src="leo-music-logo.png"></div><div id="logotag">LEO MUSIC</div>
  </div>
</div>
<script>
  var q=new URLSearchParams(location.search), layer=q.get('layer')||'L-title';
  var el=document.getElementById(layer); if(el) el.classList.add('on');
</script>
</body></html>"""

    HTML = (HTML.replace("__SLUG__", a.slug).replace("__LOGO__", logo_css)
            .replace("__TAG__", tag_css).replace("__ACC__", ACC).replace("__ACC2__", ACC2)
            .replace("__TITLE__", a.title).replace("__ARTIST__", a.artist))

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print("wrote", html_path)

    port = free_port(a.port)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port)],
                           cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    try:
        base = f"http://localhost:{port}/{html_name}"
        cap = os.path.join(root, "scripts-gen", "capture_png.js")
        subprocess.run(["node", cap, base, root, "L-title,L-logobug,L-cta"], check=True)
        # rename outputs to <slug>-ov-*.png
        for lay, nm in [("L-title","title"),("L-logobug","logobug"),("L-cta","cta")]:
            src = os.path.join(root, lay + ".png")
            dst = os.path.join(root, f"{a.slug}-ov-{nm}.png")
            if os.path.exists(src):
                os.replace(src, dst); print("->", dst)
    finally:
        srv.send_signal(signal.SIGTERM)

if __name__ == "__main__":
    main()
