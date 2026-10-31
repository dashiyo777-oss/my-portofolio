# -*- coding: utf-8 -*-
"""
living-jacket — Lv1「リビング・ジャケット」量産テンプレ（ChatGPT等の静止ジャケをClaudeが動かす）
ジャケPNG＋BGMクリップを渡すだけで、Leo Music 統一フォーマットの縦9:16・30秒を生成する再利用ジェネレータ。

仕組み（高速版）：
  - 背景ブラーは *事前に1枚* ffmpegで作成（<slug>-bg.jpg）→ 毎フレームのCSSブラーを廃止して高速化
  - 9:16へは「ブラー背景で全面フィル＋中央にシャープな正方形」＋ゆっくりKen Burns（寄り）
  - 曲調に合う粒子（petals/powder/snow/sakura/fireflies/embers/bokeh）＋朝日/光のゴッドレイ＋サビで光のブルーム
  - タイトルはジャケ内蔵想定。締めCTA（Title / Artist / 配信中 Streaming Now / LEO MUSIC）＋ Leo Music ロゴバグ（既定：左下・丸・ゴールド枠）
ビート同期はごく控えめ。決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。

使い方:
  python3 scripts-gen/gen_living_jacket.py --slug colors --jacket colors-jacket.jpg --bgm colors-bgm.mp3 \
      --title "Colors at the Door" --artist "w-Band" --particles petals,powder,rays
  bash .claude/skills/promo-short-video/scripts/render_short.sh colors colors-bgm.mp3
"""
import os, argparse, subprocess

PARTICLES = {
 # name: dict(behavior, colors[], count, size_min, size_max)
 "petals":    dict(beh="fall", cols=["#ff9a2e","#ffb64a","#ffd36a","#fff3df","#ff7a5a"], n=22, smin=16, smax=40, shape="petal"),
 "sakura":    dict(beh="fall", cols=["#ffd0e0","#ffe0ec","#fff2f7","#ffc0d6"], n=24, smin=16, smax=34, shape="petal"),
 "snow":      dict(beh="fall", cols=["#ffffff","#eef4ff","#dfeaff"], n=40, smin=5, smax=16, shape="dot"),
 "powder":    dict(beh="rise", cols=["rgba(255,70,150,.9)","rgba(255,210,70,.9)","rgba(90,210,120,.85)","rgba(255,130,60,.9)","rgba(170,110,255,.8)","rgba(255,255,255,.85)"], n=40, smin=6, smax=24, shape="glow"),
 "embers":    dict(beh="rise", cols=["rgba(255,200,120,.95)","rgba(255,150,70,.9)","rgba(255,110,50,.85)"], n=34, smin=4, smax=14, shape="glow"),
 "fireflies": dict(beh="blink",cols=["rgba(228,255,150,1)","rgba(190,240,100,.9)"], n=40, smin=5, smax=16, shape="glow"),
 "bokeh":     dict(beh="float",cols=["rgba(255,224,170,.9)","rgba(255,200,130,.8)"], n=22, smin=6, smax=22, shape="glow"),
}

def build(slug, jacket, bgm, title, artist, particles, accent, accent2, logo, climax_pk):
    root = os.path.join(os.path.dirname(__file__), "..")
    # --- 1) pre-blur the background once (fast path) ---
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        bgpath = os.path.join(root, f"{slug}-bg.jpg")
        subprocess.run([ff, "-v", "error", "-y", "-i", os.path.join(root, jacket),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=38,eq=brightness=-0.16:saturation=1.12",
            "-q:v", "4", bgpath], check=True)
        print("wrote", bgpath)
    except Exception as e:
        print("WARN: could not pre-blur bg (", e, ") — html will fall back to CSS blur")
        bgpath = None
    bg_is_static = bgpath is not None
    logo_css = ("left:40px" if logo == "left" else "right:40px")
    tag_css  = ("left:176px" if logo == "left" else "right:176px;text-align:right")
    # particle JS config
    import json
    cfg = [PARTICLES[p] for p in particles if p in PARTICLES]
    use_rays = "rays" in particles
    cfg_json = json.dumps(cfg)

    BG_RULE = (f"#bgimg{{position:absolute;left:-4%;top:-3%;width:108%;height:106%;object-fit:cover;filter:brightness(1) saturate(1);will-change:transform}}"
               if bg_is_static else
               "#bgimg{position:absolute;left:-10%;top:-6%;width:120%;height:112%;object-fit:cover;filter:blur(42px) brightness(.62) saturate(1.1);will-change:transform}")
    bg_src = f"{slug}-bg.jpg" if bg_is_static else jacket

    CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#120a06;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#120a06}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;font-family:"EB Garamond","Noto Serif JP",serif;background:#1a0f08}
__BG_RULE__
#bgtint{position:absolute;inset:0;background:radial-gradient(60% 50% at 54% 44%,rgba(255,180,90,.1),transparent 70%),linear-gradient(180deg,rgba(20,10,6,.22),rgba(20,10,6,.08) 30%,rgba(20,10,6,.28))}
#photo{position:absolute;left:0;top:420px;width:1080px;height:1080px;overflow:hidden;will-change:transform;box-shadow:0 0 80px rgba(0,0,0,.5)}
#photoimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
#rays{position:absolute;left:560px;top:860px;width:1500px;height:1500px;transform:translate(-50%,-50%);z-index:3;pointer-events:none;mix-blend-mode:screen;opacity:.3;
  background:conic-gradient(from 0deg,rgba(255,228,170,0) 0deg,rgba(255,228,170,.16) 3deg,rgba(255,228,170,0) 7deg,rgba(255,228,170,0) 22deg,rgba(255,228,170,.13) 25deg,rgba(255,228,170,0) 30deg,rgba(255,228,170,0) 46deg,rgba(255,228,170,.15) 50deg,rgba(255,228,170,0) 55deg,rgba(255,228,170,0) 72deg,rgba(255,228,170,.12) 75deg,rgba(255,228,170,0) 80deg,rgba(255,228,170,0) 98deg,rgba(255,228,170,.15) 102deg,rgba(255,228,170,0) 107deg,rgba(255,228,170,0) 360deg)}
#sunbloom{position:absolute;left:560px;top:850px;width:760px;height:760px;transform:translate(-50%,-50%);z-index:3;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(circle,rgba(255,224,150,.6),rgba(255,180,100,.2) 40%,transparent 72%)}
#parts{position:absolute;inset:0;z-index:4;pointer-events:none}
#vig{position:absolute;inset:0;z-index:7;pointer-events:none;background:radial-gradient(130% 80% at 50% 46%,transparent 54%,rgba(10,5,2,.6) 100%)}
#grain{position:absolute;inset:0;z-index:7;pointer-events:none;opacity:.045;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
#ctadim{position:absolute;inset:0;z-index:11;background:rgba(10,6,2,0);pointer-events:none}
#cta{position:absolute;left:30px;right:30px;top:560px;text-align:center;z-index:12;opacity:0}
.badge{display:inline-block;font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:7px;color:#2a1704;background:linear-gradient(90deg,__ACC__,__ACC2__);padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-t{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-style:italic;font-size:104px;line-height:1.02;color:#fff;text-shadow:0 0 28px rgba(255,200,120,.6),0 5px 20px rgba(10,6,2,.7)}
.cta-a{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:500;font-size:50px;letter-spacing:12px;color:#f3ead6;margin-top:14px;text-shadow:0 2px 12px rgba(10,6,2,.8)}
.cta-s{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-size:40px;letter-spacing:3px;color:__ACC__;margin-top:22px}
.cta-b{font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:10px;color:#f3ead6;margin-top:12px;opacity:.92}
#logobug{position:absolute;__LOGO__;bottom:46px;width:124px;height:124px;border-radius:50%;overflow:hidden;z-index:13;box-shadow:0 0 0 3px __ACCDIM__,0 6px 16px rgba(0,0,0,.5);opacity:.92}
#logobug img{position:absolute;left:-14%;top:-10%;width:128%;height:128%;object-fit:cover}
#logotag{position:absolute;__TAG__;bottom:70px;z-index:13;font-family:"EB Garamond",serif;font-weight:600;font-size:34px;letter-spacing:5px;color:#f7ecd6;opacity:.86;text-shadow:0 2px 8px rgba(0,0,0,.7)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#2a1704;font-size:60px;background:linear-gradient(135deg,__ACC__,__ACC2__);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,__ACC__,__ACC2__)}
body.capture #ui,body.capture #bar{display:none}
""".replace("__BG_RULE__", BG_RULE).replace("__ACC__", accent).replace("__ACC2__", accent2).replace("__ACCDIM__", "rgba(255,220,150,.5)").replace("__LOGO__", logo_css).replace("__TAG__", tag_css)

    BODY = f"""
<div id="wrap"><div id="stage">
  <img id="bgimg" src="{bg_src}">
  <div id="bgtint"></div>
  <div id="photo"><img id="photoimg" src="{jacket}"></div>
  <div id="rays"></div><div id="sunbloom"></div>
  <div id="parts"></div>
  <div id="ctadim"></div>
  <div id="cta"><span class="badge">NEW SONG</span><div class="cta-t">{title}</div><div class="cta-a">{artist}</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
  <div id="vig"></div><div id="grain"></div>
  <div id="logobug"><img src="leo-music-logo.png"></div><div id="logotag">LEO MUSIC</div>
  <div id="ui"><button id="play">&#9654;</button></div>
  <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="{bgm}" preload="auto"></audio>
"""

    ENGINE = r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');if(capture)document.body.classList.add('capture');
let _s=31337;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st){const d=document.createElement('div');if(st)d.style.cssText+=st;p.appendChild(d);return d;}
const PCFG=__CFG__; const USE_RAYS=__RAYS__;
const parts=document.getElementById('parts');const items=[];
for(const g of PCFG){for(let i=0;i<g.n;i++){const sz=g.smin+rnd()*(g.smax-g.smin);const col=g.cols[(rnd()*g.cols.length)|0];let st;
  if(g.shape==='petal')st='position:absolute;width:'+sz+'px;height:'+(sz*0.72)+'px;border-radius:50% 50% 50% 50%/70% 70% 40% 40%;background:radial-gradient(circle at 50% 70%,'+col+','+col+'cc)';
  else if(g.shape==='glow')st='position:absolute;width:'+sz+'px;height:'+sz+'px;border-radius:50%;background:radial-gradient(circle,'+col+',transparent 72%)';
  else st='position:absolute;width:'+sz+'px;height:'+sz+'px;border-radius:50%;background:'+col;
  const e=mk(parts,st);
  items.push({el:e,beh:g.beh,x:rnd()*1080,y:rnd()*1920,sz:sz,fall:40+rnd()*60,rise:5+rnd()*16,sp:0.4+rnd()*0.5,sway:30+rnd()*70,ph:rnd()*6.28,rot:(rnd()-0.5)*3,base:rnd()*1920,blinkR:1+rnd()*2,blinkP:rnd()*6.28,drift:7+rnd()*16});}}
const bgimg=document.getElementById('bgimg'),photo=document.getElementById('photo'),rays=document.getElementById('rays'),sunbloom=document.getElementById('sunbloom'),
  cta=document.getElementById('cta'),ctadim=document.getElementById('ctadim'),logobug=document.getElementById('logobug'),logotag=document.getElementById('logotag');
if(!USE_RAYS){rays.style.display='none';}
const BEAT=678.0, OFF=5; const CL_IN=4000, CL_PK=__CLPK__, CL_OUT=27000; const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}
window.renderAt=function(t){
  const ts=t/1000;const p=t/TOTAL;
  const bp=(((t-OFF)%BEAT)+BEAT)%BEAT/BEAT;const swell=0.5+0.5*Math.cos(bp*6.2832);
  const climax=smooth(t,CL_IN,CL_PK)*(1-0.5*smooth(t,CL_OUT,30000));
  photo.style.transform='scale('+(1.0+0.11*p).toFixed(4)+') translateY('+(-14*p).toFixed(1)+'px)';
  bgimg.style.transform='scale('+(1.04+0.06*p)+') translateY('+(-8*p)+'px)';
  rays.style.transform='translate(-50%,-50%) rotate('+(ts*2.2).toFixed(2)+'deg) scale('+(1+0.06*climax)+')';
  rays.style.opacity=(0.24+0.08*Math.sin(ts*0.5)+0.34*climax+0.05*swell).toFixed(3);
  sunbloom.style.opacity=(0.16+0.5*climax)*(0.85+0.15*swell);
  sunbloom.style.transform='translate(-50%,-50%) scale('+(1+0.12*climax+0.02*swell)+')';
  for(const it of items){let x,y,op=1,extra='';
    if(it.beh==='fall'){y=((it.base+ts*it.fall)%2040)-100;x=it.x+Math.sin(ts*it.sp+it.ph)*it.sway;op=0.85*smooth(y,-100,80)*(1-smooth(y,1820,1960));extra=' rotate('+(ts*40*it.rot).toFixed(1)+'deg)';}
    else if(it.beh==='rise'){y=it.y-((ts*it.rise)%1340);if(y<-30)y+=1340;x=it.x+Math.sin(ts*0.5+it.ph)*it.sway;const bl=0.4+0.6*Math.abs(Math.sin(ts*it.blinkR+it.blinkP));op=bl*(0.35+0.4*climax+0.1);extra=' scale('+(0.8+0.3*bl)+')';}
    else if(it.beh==='blink'){y=it.y-((ts*it.rise)%1340);if(y<-30)y+=1340;x=it.x+Math.sin(ts*0.5+it.ph)*it.sway;const bl=Math.pow(Math.max(0,Math.sin(ts*it.blinkR+it.blinkP)),3);op=(0.2+0.8*bl)*(0.4+0.5*climax+0.2);extra=' scale('+(0.8+0.5*bl)+')';}
    else{y=1960-((ts*it.drift+it.base)%2100);x=it.x+Math.sin(ts*0.4+it.ph)*it.sway;op=(0.3+0.4*climax);}
    it.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)'+extra;it.el.style.opacity=Math.max(0,op).toFixed(3);}
  logobug.style.opacity=(0.9+0.06*Math.sin(ts*1.2)).toFixed(3);logotag.style.opacity=(0.82+0.06*Math.sin(ts*1.2)).toFixed(3);
  const cvis=smooth(t,26400,27200);cta.style.opacity=cvis.toFixed(3);cta.style.transform='scale('+(0.98+0.02*cvis)+')';
  ctadim.style.background='rgba(10,6,2,'+(0.74*cvis).toFixed(3)+')';
};
const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;
function play(){document.getElementById('ui').style.display='none';try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();(function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const s0=performance.now();(function fo(){const k=(performance.now()-s0)/1500;bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1500);}
document.getElementById('play').addEventListener('click',play);window.renderAt(0);
""".replace("__CFG__", cfg_json).replace("__RAYS__", "true" if use_rays else "false").replace("__CLPK__", str(climax_pk))

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} / {artist} (Living Jacket)</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
    out = os.path.join(root, f"{slug}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.abspath(out), len(html), "bytes")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--jacket", required=True, help="sharp jacket image file already in repo root")
    ap.add_argument("--bgm", required=True, help="bgm mp3 file in repo root (for <audio> src)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--artist", required=True)
    ap.add_argument("--particles", default="petals,bokeh,rays", help="comma list: petals,sakura,snow,powder,embers,fireflies,bokeh,rays")
    ap.add_argument("--accent", default="#ffd23d")
    ap.add_argument("--accent2", default="#ff9a3c")
    ap.add_argument("--logo", default="left", choices=["left", "right"])
    ap.add_argument("--climax", type=int, default=19000)
    a = ap.parse_args()
    build(a.slug, a.jacket, a.bgm, a.title, a.artist, [p.strip() for p in a.particles.split(",")], a.accent, a.accent2, a.logo, a.climax)
