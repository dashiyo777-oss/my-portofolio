# -*- coding: utf-8 -*-
"""
Colors at the Door / w-Band — Lv1「リビング・ジャケット」（ChatGPTの静止ジャケをClaudeが動かす / デモ）
方式：ChatGPTのフォトリアル・ジャケ(colors-jacket.jpg)を背景に、
  - 9:16へは「ブラーで全面フィル＋中央にシャープな正方形」＋ゆっくりKen Burns（寄り）
  - 花びら（マリーゴールド/ジャスミン）＋ホーリーの色粉モート＋朝日のゴッドレイ＋サビで光のブルーム
  - 締めのCTAカード（Title / w-Band / 配信中 Streaming Now / LEO MUSIC）＋ Leo Music ロゴバグ（左下・円形）
  - 画面テキストはタイトル＋アーティスト（＝ジャケに内蔵）＋CTAのみ（歌詞テロップなし）
ビート同期はごく控えめ（88.5BPM, beat 678ms, +5ms）：レイ/ブルーム/色粉がふわっと脈打つ。
BGM: colors-bgm.mp3 (source 4:47/287s のサビ 156s〜：歌詞が明瞭)。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","colors-living.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#120a06;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#120a06}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;font-family:"EB Garamond","Noto Serif JP",serif;background:#1a0f08}
#bgimg{position:absolute;left:-10%;top:-6%;width:120%;height:112%;object-fit:cover;filter:blur(42px) brightness(.62) saturate(1.1);will-change:transform}
#bgtint{position:absolute;inset:0;background:radial-gradient(60% 50% at 54% 44%,rgba(255,180,90,.12),transparent 70%),linear-gradient(180deg,rgba(20,10,6,.25),rgba(20,10,6,.1) 30%,rgba(20,10,6,.3))}
#photo{position:absolute;left:0;top:420px;width:1080px;height:1080px;overflow:hidden;will-change:transform;box-shadow:0 0 80px rgba(0,0,0,.5)}
#photoimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
#rays{position:absolute;left:594px;top:874px;width:1500px;height:1500px;transform:translate(-50%,-50%);z-index:3;pointer-events:none;mix-blend-mode:screen;opacity:.3;
  background:conic-gradient(from 0deg,
   rgba(255,228,170,0) 0deg,rgba(255,228,170,.16) 3deg,rgba(255,228,170,0) 7deg,
   rgba(255,228,170,0) 22deg,rgba(255,228,170,.13) 25deg,rgba(255,228,170,0) 30deg,
   rgba(255,228,170,0) 46deg,rgba(255,228,170,.15) 50deg,rgba(255,228,170,0) 55deg,
   rgba(255,228,170,0) 72deg,rgba(255,228,170,.12) 75deg,rgba(255,228,170,0) 80deg,
   rgba(255,228,170,0) 98deg,rgba(255,228,170,.15) 102deg,rgba(255,228,170,0) 107deg,
   rgba(255,228,170,0) 360deg)}
#sunbloom{position:absolute;left:594px;top:860px;width:760px;height:760px;transform:translate(-50%,-50%);z-index:3;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(circle,rgba(255,224,150,.6),rgba(255,180,100,.2) 40%,transparent 72%)}
#petals{position:absolute;inset:0;z-index:4;pointer-events:none}
#powder{position:absolute;inset:0;z-index:4;pointer-events:none}
.powd{position:absolute;border-radius:50%;filter:blur(1px)}
#dust{position:absolute;inset:0;z-index:4;pointer-events:none}
.dust{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,228,180,.9),transparent 70%)}
#vig{position:absolute;inset:0;z-index:7;pointer-events:none;background:radial-gradient(130% 80% at 50% 46%,transparent 54%,rgba(10,5,2,.6) 100%)}
#grain{position:absolute;inset:0;z-index:7;pointer-events:none;opacity:.045;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
/* CTA */
#cta{position:absolute;left:30px;right:30px;top:560px;text-align:center;z-index:12;opacity:0}
.badge{display:inline-block;font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:7px;color:#3a1f08;background:linear-gradient(90deg,#ffd98a,#ff9a3c);padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-t{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-style:italic;font-size:104px;line-height:1.02;color:#fff;text-shadow:0 0 28px rgba(255,200,120,.6),0 5px 20px rgba(10,6,2,.7)}
.cta-a{font-family:"EB Garamond",serif;font-weight:500;font-size:50px;letter-spacing:12px;color:#f3ead6;margin-top:14px;text-shadow:0 2px 12px rgba(10,6,2,.8)}
.cta-s{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-size:40px;letter-spacing:3px;color:#ffd98a;margin-top:22px}
.cta-b{font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:10px;color:#f3ead6;margin-top:12px;opacity:.92}
#ctadim{position:absolute;inset:0;z-index:11;background:rgba(10,6,2,.0);pointer-events:none}
/* Leo Music logo bug (circular, cropped to the cat) */
#logobug{position:absolute;left:40px;bottom:46px;width:124px;height:124px;border-radius:50%;overflow:hidden;z-index:13;
  box-shadow:0 0 0 3px rgba(255,220,150,.5),0 6px 16px rgba(0,0,0,.5);opacity:.92}
#logobug img{position:absolute;left:-14%;top:-10%;width:128%;height:128%;object-fit:cover}
#logotag{position:absolute;left:176px;bottom:70px;z-index:13;font-family:"EB Garamond",serif;font-weight:600;font-size:34px;letter-spacing:5px;color:#f7ecd6;opacity:.86;text-shadow:0 2px 8px rgba(0,0,0,.7)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#3a1f08;font-size:60px;background:linear-gradient(135deg,#ffd98a,#ff9a3c);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffd98a,#ff9a3c)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
  <img id="bgimg" src="colors-jacket.jpg">
  <div id="bgtint"></div>
  <div id="photo"><img id="photoimg" src="colors-jacket.jpg"></div>
  <div id="rays"></div>
  <div id="sunbloom"></div>
  <div id="powder"></div>
  <div id="petals"></div>
  <div id="dust"></div>
  <div id="ctadim"></div>
  <div id="cta"><span class="badge">NEW SONG</span><div class="cta-t">Colors at the Door</div><div class="cta-a">w-Band</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
  <div id="vig"></div><div id="grain"></div>
  <div id="logobug"><img src="leo-music-logo.png"></div>
  <div id="logotag">LEO MUSIC</div>
  <div id="ui"><button id="play">&#9654;</button></div>
  <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="colors-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');if(capture)document.body.classList.add('capture');
let _s=31337;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');if(cls)d.className=cls;if(st)d.style.cssText+=st;p.appendChild(d);return d;}

// petals (marigold orange + white jasmine)
const pf=document.getElementById('petals');const petals=[];
const PC=['#ff9a2e','#ffb64a','#ffd36a','#fff3df','#ff7a5a'];
for(let i=0;i<22;i++){const w=16+rnd()*26;const c=PC[(rnd()*PC.length)|0];
  const e=mk(pf,'position:absolute;width:'+w+'px;height:'+(w*0.72)+'px;border-radius:50% 50% 50% 50%/70% 70% 40% 40%;background:radial-gradient(circle at 50% 70%,'+c+','+c+'cc);box-shadow:0 1px 4px rgba(0,0,0,.15)','');
  petals.push({el:e,x:rnd()*1080,y:rnd()*1920,fall:40+rnd()*60,sway:40+rnd()*80,ph:rnd()*6.28,rot:(rnd()-0.5)*3,base:rnd()*1920,sp:0.4+rnd()*0.5});}
// holi colored-powder motes (pink/yellow/green/orange)
const pw=document.getElementById('powder');const powders=[];
const HC=['rgba(255,70,150,.9)','rgba(255,210,70,.9)','rgba(90,210,120,.85)','rgba(255,130,60,.9)','rgba(170,110,255,.8)','rgba(255,255,255,.85)'];
for(let i=0;i<40;i++){const w=6+rnd()*18;const e=mk(pw,'width:'+w+'px;height:'+w+'px;background:radial-gradient(circle,'+HC[(rnd()*HC.length)|0]+',transparent 72%)','powd');
  powders.push({el:e,x:rnd()*1080,y:600+rnd()*1320,rise:5+rnd()*16,amp:16+rnd()*44,ph:rnd()*6.28,blinkR:1+rnd()*2,blinkP:rnd()*6.28,base:rnd()*1340});}
// warm dust motes
const df=document.getElementById('dust');const dusts=[];
for(let i=0;i<22;i++){const w=3+rnd()*8;const e=mk(df,'width:'+w+'px;height:'+w+'px','dust');dusts.push({el:e,x:rnd()*1080,sp:7+rnd()*16,amp:14+rnd()*40,ph:rnd()*6.28,base:rnd()*1920});}

const bgimg=document.getElementById('bgimg'),photo=document.getElementById('photo'),rays=document.getElementById('rays'),
  sunbloom=document.getElementById('sunbloom'),cta=document.getElementById('cta'),ctadim=document.getElementById('ctadim'),
  logobug=document.getElementById('logobug'),logotag=document.getElementById('logotag');

const BEAT=678.0, OFF=5;                 // 88.5bpm, +5ms (gentle)
const CL_IN=4000, CL_PK=19000, CL_OUT=27000;
const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;const p=t/TOTAL;
  const bp=(((t-OFF)%BEAT)+BEAT)%BEAT/BEAT;const swell=0.5+0.5*Math.cos(bp*6.2832);
  const climax=smooth(t,CL_IN,CL_PK)*(1-0.5*smooth(t,CL_OUT,30000));
  // Ken Burns: slow push-in on the sharp photo + the blurred bg
  const sc=1.0+0.11*p; const ty=-14*p;
  photo.style.transform='scale('+sc.toFixed(4)+') translateY('+ty.toFixed(1)+'px)';
  bgimg.style.transform='scale('+(1.0+0.09*p)+') translateY('+(-10*p)+'px)';
  // god-rays rotate slowly + swell with beat/chorus
  rays.style.transform='translate(-50%,-50%) rotate('+(ts*2.2).toFixed(2)+'deg) scale('+(1+0.06*climax)+')';
  rays.style.opacity=(0.24+0.08*Math.sin(ts*0.5)+0.34*climax+0.05*swell).toFixed(3);
  // sunrise bloom swells into the chorus
  sunbloom.style.opacity=(0.18+0.5*climax)*(0.85+0.15*swell);
  sunbloom.style.transform='translate(-50%,-50%) scale('+(1+0.12*climax+0.02*swell)+')';
  // petals fall + sway + spin
  for(const pt of petals){let y=((pt.base+ts*pt.fall)%2040)-100;let x=pt.x+Math.sin(ts*pt.sp+pt.ph)*pt.sway;
    pt.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) rotate('+(ts*40*pt.rot).toFixed(1)+'deg)';
    pt.el.style.opacity=(0.85*smooth(y,-100,80)*(1-smooth(y,1820,1960))).toFixed(3);}
  // powder motes rise, blink, brighter at chorus
  for(const pd of powders){let y=pd.y-((ts*pd.rise)%1340);if(y<-30)y+=1340;let x=pd.x+Math.sin(ts*0.5+pd.ph)*pd.amp;
    const blink=0.4+0.6*Math.abs(Math.sin(ts*pd.blinkR+pd.blinkP));
    pd.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(0.8+0.3*blink)+')';
    pd.el.style.opacity=(blink*(0.35+0.4*climax+0.1)).toFixed(3);}
  // dust
  for(const d of dusts){let y=1960-((ts*d.sp+d.base)%2100);let x=d.x+Math.sin(ts*0.4+d.ph)*d.amp;
    d.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';d.el.style.opacity=(0.3+0.4*climax).toFixed(3);}
  // logo bug gentle breathe
  logobug.style.opacity=(0.9+0.06*Math.sin(ts*1.2)).toFixed(3);
  logotag.style.opacity=(0.82+0.06*Math.sin(ts*1.2)).toFixed(3);
  // CTA near the end (dim the photo a touch)
  const cvis=smooth(t,26400,27200);
  cta.style.opacity=cvis.toFixed(3);cta.style.transform='scale('+(0.98+0.02*cvis)+')';
  ctadim.style.background='rgba(10,6,2,'+(0.74*cvis).toFixed(3)+')';
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;
function play(){document.getElementById('ui').style.display='none';try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const s0=performance.now();(function fo(){const k=(performance.now()-s0)/1500;bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1500);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Colors at the Door / w-Band (Living Jacket)</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
