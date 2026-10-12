# -*- coding: utf-8 -*-
"""
ジャスミンティーが冷めるまで / 水野灯 — 縦型9:16 宣伝ショート（しっとり系バラード / 2歳以上の日米向け）
ジャケット準拠：雨の夜の窓辺。あたたかな室内（ランプの金色）× 窓の外は雨にじむ夜景・川の反射・大きな満月。
テーブルに白いジャスミン柄のティーカップ（湯気）、ガラスの小瓶のジャスミン、重ねた古い本、散ったジャスミンの花。
左手前にクリームのニットで頬杖をつき窓の外を見つめる女性（あたたかな光）。
演出：ビート同期ではなく、しっとりしたゆらぎ——湯気が立ちほどけ、雨粒が窓を伝い、街の灯がにじみ、満月が静か。
「冷めるまで」を映像化：湯気は30秒かけて少しずつ薄くなり（＝お茶が冷める）、終盤は空のカップに月が映る。
最終サビで室内の光がやわらかくブルーム。BGM: jasmine-bgm.mp3 (source 4:38/278s の2番サビ 155.5s〜：タイトルのフック)。
英語の簡単な訳つき。画面テキストはジャケット表記＋提供歌詞のみ（創作なし）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","jasmine.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0d1224;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0d1224}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Noto Serif JP",serif;background:#111a33}
#world{position:absolute;inset:-30px;transform-origin:50% 56%}
/* ---- window view (upper) ---- */
#sky2{position:absolute;left:0;right:0;top:0;height:1240px;background:
  radial-gradient(60% 50% at 84% 14%, rgba(80,106,160,.55), rgba(30,44,80,.18) 40%, transparent 66%),
  linear-gradient(180deg,#121d3c,#16244a 44%,#1b2e56 72%,#243a66 100%)}
#moonglow{position:absolute;left:830px;top:110px;width:520px;height:520px;transform:translate(-50%,-50%);pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(circle,rgba(230,238,255,.8),rgba(180,200,245,.3) 34%,transparent 66%)}
#moon{position:absolute;left:830px;top:110px;width:150px;height:150px;transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(circle at 42% 40%,#f4f7ff,#dfe6fb 54%,#b9c6ea);box-shadow:0 0 60px 14px rgba(210,224,255,.5)}
#moon::after{content:"";position:absolute;inset:0;border-radius:50%;opacity:.14;
  background:radial-gradient(circle at 60% 36%,#8fa0c8 0 14px,transparent 15px),radial-gradient(circle at 38% 58%,#8fa0c8 0 10px,transparent 11px),radial-gradient(circle at 66% 66%,#8fa0c8 0 8px,transparent 9px)}
.star{position:absolute;width:3px;height:3px;border-radius:50%;background:#dfe6fb}
/* city skyline + bokeh */
#city{position:absolute;left:0;right:0;top:820px;height:300px}
.bldg{position:absolute;bottom:0;background:linear-gradient(180deg,#1c2a4c,#14213f);border-radius:3px 3px 0 0}
.wlit{position:absolute;width:5px;height:6px;border-radius:1px;background:rgba(255,206,130,.8)}
.bokeh{position:absolute;border-radius:50%;filter:blur(3px)}
#river{position:absolute;left:0;right:0;top:1055px;height:150px;background:linear-gradient(180deg,#1a3056,#152748 60%,#12203e);overflow:hidden}
.rref{position:absolute;top:0;width:8px;height:100%;filter:blur(3px);opacity:.55}
/* rain on glass */
#glass{position:absolute;left:0;right:0;top:0;height:1200px;pointer-events:none;
  background:linear-gradient(180deg,rgba(20,32,60,.18),rgba(16,26,50,.05) 40%,transparent 70%)}
.streak{position:absolute;width:2px;background:linear-gradient(180deg,rgba(200,220,255,.0),rgba(200,220,255,.28),rgba(200,220,255,0));filter:blur(.5px)}
.drop{position:absolute;width:7px;height:11px;border-radius:50% 50% 60% 60%;background:radial-gradient(circle at 40% 30%,rgba(230,240,255,.9),rgba(170,195,240,.3));filter:blur(.4px)}
/* window frame */
#frame{position:absolute;left:0;right:0;top:0;height:1210px;pointer-events:none}
#frame .mull{position:absolute;background:linear-gradient(180deg,#6a4c2e,#4a3420);box-shadow:0 2px 8px rgba(0,0,0,.4)}
#sill{position:absolute;left:-30px;right:-30px;top:1150px;height:90px;background:linear-gradient(180deg,#75522f,#4e371f);box-shadow:0 10px 30px rgba(0,0,0,.45);z-index:3}
/* interior warm light */
#lampglow{position:absolute;left:-120px;top:120px;width:900px;height:1500px;pointer-events:none;mix-blend-mode:screen;z-index:3;
  background:radial-gradient(44% 40% at 18% 40%, rgba(255,196,120,.6), rgba(255,170,90,.18) 44%, transparent 72%)}
#shelf{position:absolute;left:0;top:60px;width:230px;height:520px;z-index:2;background:linear-gradient(90deg,#2a1d12,#3a2a1a);opacity:.9}
.slit{position:absolute;border-radius:50%;filter:blur(4px)}
/* ---- woman (warm-lit, 3/4 back view, hand resting at cheek, gazing out) ---- */
#woman{position:absolute;left:30px;bottom:0;width:560px;height:1360px;z-index:5;transform-origin:42% 100%}
#sweater{position:absolute;left:-40px;bottom:0;width:660px;height:820px;z-index:6;
  background:radial-gradient(62% 56% at 46% 18%, #f4ecdd, #e3d5be 56%, #c8b599);
  clip-path:polygon(0 100%,0 48%,16% 26%,40% 11%,60% 11%,78% 26%,100% 46%,100% 100%)}
#sweater::after{content:"";position:absolute;inset:0;opacity:.5;mix-blend-mode:multiply;
  background:repeating-linear-gradient(28deg,rgba(150,130,100,.13) 0 7px,transparent 7px 15px),repeating-linear-gradient(-28deg,rgba(150,130,100,.1) 0 7px,transparent 7px 15px);
  clip-path:polygon(0 100%,0 48%,16% 26%,40% 11%,60% 11%,78% 26%,100% 46%,100% 100%)}
#hairback{position:absolute;left:150px;bottom:470px;width:300px;height:430px;z-index:6;
  background:radial-gradient(58% 54% at 42% 36%,#885733,#5a3620 60%,#3d2413);
  border-radius:50% 50% 44% 56% / 62% 60% 40% 40%}
#bun{position:absolute;left:166px;bottom:772px;width:152px;height:140px;z-index:6;border-radius:54% 46% 50% 50%;
  background:radial-gradient(circle at 42% 38%,#8f5e38,#5a3620 70%);transform:rotate(-10deg)}
/* cream sweater-sleeved arm, elbow on the table, hand up toward the head (cozy, blends with sweater) */
#sleeve{position:absolute;left:250px;bottom:400px;width:116px;height:300px;z-index:8;transform-origin:50% 100%;transform:rotate(12deg);
  background:linear-gradient(90deg,#f1e9d9,#dccdb4 70%,#cbbb9e);border-radius:58px 58px 40px 40px}
#sleeve::after{content:"";position:absolute;inset:0;border-radius:58px 58px 40px 40px;opacity:.5;mix-blend-mode:multiply;
  background:repeating-linear-gradient(20deg,rgba(150,130,100,.13) 0 7px,transparent 7px 15px)}
#wrim{position:absolute;left:30px;bottom:0;width:560px;height:1360px;z-index:10;pointer-events:none;mix-blend-mode:screen;opacity:.0;
  background:linear-gradient(300deg,rgba(255,202,124,.55),transparent 34%)}
/* ---- table + objects (foreground) ---- */
#table{position:absolute;left:-40px;right:-40px;bottom:0;height:520px;z-index:10;
  background:linear-gradient(180deg,#6a4522 0%,#4e3318 40%,#3a2612 100%);box-shadow:0 -10px 40px rgba(0,0,0,.4)}
#table::before{content:"";position:absolute;left:0;right:0;top:0;height:14px;background:linear-gradient(180deg,rgba(255,200,130,.5),transparent)}
#tableref{position:absolute;left:0;right:0;top:0;height:260px;opacity:.16;pointer-events:none;
  background:radial-gradient(60% 80% at 52% 0,rgba(255,210,150,.6),transparent 60%)}
#books{position:absolute;right:20px;bottom:300px;width:300px;height:150px;z-index:11}
.book{position:absolute;border-radius:4px;box-shadow:0 6px 14px rgba(0,0,0,.4)}
#vase{position:absolute;right:70px;bottom:430px;width:140px;height:180px;z-index:11}
#vaseglass{position:absolute;left:30px;bottom:0;width:84px;height:110px;border-radius:12px 12px 20px 20px;
  background:linear-gradient(90deg,rgba(220,235,255,.28),rgba(200,220,250,.14));border:2px solid rgba(220,235,255,.3);box-shadow:inset 0 0 14px rgba(255,220,160,.3)}
/* teacup */
#cup{position:absolute;left:360px;bottom:300px;width:360px;height:300px;z-index:13}
#saucer{position:absolute;left:10px;bottom:30px;width:340px;height:70px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 34%,#fdfaf4,#e9e0d0 70%,#cdbfa6);box-shadow:0 12px 24px rgba(0,0,0,.4)}
#cupbody{position:absolute;left:70px;bottom:52px;width:220px;height:170px;border-radius:14px 14px 48% 48%/10px 10px 70% 70%;
  background:linear-gradient(90deg,#f6f0e6,#fffdf8 40%,#e8ddca);box-shadow:inset 0 -14px 24px rgba(180,160,130,.3),0 8px 16px rgba(0,0,0,.3)}
#cupbody::before{content:"";position:absolute;left:8px;right:8px;top:6px;height:34px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#7a4a2a,#5a3418 70%,#432610)}
#cuprim{position:absolute;left:74px;bottom:214px;width:212px;height:30px;border-radius:50%;z-index:14;
  background:linear-gradient(180deg,#fffef9,#d9cbb2);box-shadow:0 0 0 2px rgba(210,180,120,.5)}
#handle{position:absolute;right:48px;bottom:96px;width:70px;height:84px;border:16px solid #f1e8d8;border-left:none;border-radius:0 46px 46px 0;z-index:13;box-shadow:4px 4px 10px rgba(0,0,0,.25)}
.cupflower{position:absolute;z-index:14}
#steam{position:absolute;left:360px;bottom:520px;width:360px;height:720px;z-index:15;pointer-events:none}
.swisp{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,252,245,.5),rgba(255,250,240,0) 70%);filter:blur(3px)}
/* jasmine flowers */
.jflower{position:absolute;z-index:16}
.jpetal{position:absolute;left:50%;top:50%;border-radius:50% 50% 50% 50%/70% 70% 40% 40%;transform-origin:50% 100%}
.jcenter{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,#ffe07a,#f3b53a)}
#motes{position:absolute;inset:0;z-index:17;pointer-events:none}
.mote{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,224,170,.9),rgba(255,210,150,0) 70%)}
#petals{position:absolute;inset:0;z-index:17;pointer-events:none}
#bloom{position:absolute;inset:0;z-index:18;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(54% 40% at 36% 46%,rgba(255,214,150,.55),transparent 66%)}
/* ---- text ---- */
#titlewrap{position:absolute;left:40px;right:40px;top:150px;text-align:center;z-index:20;opacity:0}
.tt{font-family:"Noto Serif JP",serif;font-weight:800;font-size:104px;line-height:1.18;letter-spacing:4px;color:#fff;
  text-shadow:0 0 26px rgba(255,214,150,.6),0 4px 18px rgba(10,20,45,.7)}
.tbrush{width:360px;height:3px;margin:16px auto 12px;background:linear-gradient(90deg,transparent,rgba(255,224,180,.9),transparent)}
.tart{font-family:"Noto Serif JP",serif;font-weight:600;font-size:52px;letter-spacing:16px;color:#f3ead9;text-shadow:0 2px 14px rgba(10,20,45,.7)}
#scenes{position:absolute;left:54px;right:54px;top:560px;height:470px;z-index:20}
.sc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;will-change:opacity,transform}
.lyr{font-family:"Noto Serif JP",serif;font-weight:700;font-size:70px;line-height:1.34;letter-spacing:3px;color:#fff;
  text-shadow:0 3px 18px rgba(8,16,40,.85),0 0 30px rgba(255,210,150,.3)}
.lyr .hl{color:#ffe0a2}
.lyr .en{display:block;font-family:"Noto Serif JP",serif;font-weight:500;font-style:italic;font-size:37px;letter-spacing:1px;color:#ece3f2;margin-top:20px;text-shadow:0 2px 12px rgba(8,16,40,.9)}
.badge{display:inline-block;font-family:"Noto Serif JP",serif;font-weight:700;font-size:32px;letter-spacing:7px;color:#3a2a14;
  background:linear-gradient(90deg,#ffe6b0,#ffcf86);padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-t{font-family:"Noto Serif JP",serif;font-weight:800;font-size:82px;line-height:1.2;letter-spacing:3px;color:#fff;text-shadow:0 0 26px rgba(255,214,150,.6),0 4px 18px rgba(10,20,45,.7)}
.cta-a{font-family:"Noto Serif JP",serif;font-weight:600;font-size:48px;letter-spacing:14px;color:#f3ead9;margin-top:14px}
.cta-s{font-family:"Noto Serif JP",serif;font-weight:600;font-size:38px;letter-spacing:3px;color:#ffe0a2;margin-top:22px}
.cta-b{font-family:"Noto Serif JP",serif;font-weight:700;font-size:30px;letter-spacing:9px;color:#ece3f2;margin-top:12px;opacity:.9}
#grain{position:absolute;inset:0;z-index:21;pointer-events:none;opacity:.05;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
#vig{position:absolute;inset:0;pointer-events:none;z-index:22;background:radial-gradient(130% 82% at 48% 44%,transparent 52%,rgba(6,10,26,.66) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#3a2a14;font-size:60px;background:linear-gradient(135deg,#ffe6b0,#ffcf86);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffe0a2,#fff)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="sky2"></div>
  <div id="moonglow"></div><div id="moon"></div>
  <div id="starf"></div>
  <div id="city"></div><div id="citylit"></div>
  <div id="river"></div><div id="riverref"></div>
  <div id="glass"></div><div id="streakf"></div><div id="dropf"></div>
  <div id="frame"></div><div id="sill"></div>
  <div id="shelf"></div><div id="shelflit"></div>
  <div id="lampglow"></div>
  <div id="woman">
    <div id="hairback"></div><div id="bun"></div>
    <div id="sweater"></div><div id="sleeve"></div><div id="wrim"></div>
  </div>
  <div id="table"></div><div id="tableref"></div>
  <div id="books"></div>
  <div id="vase"><div id="vaseglass"></div></div>
  <div id="cup"><div id="saucer"></div><div id="cupbody"></div><div id="cuprim"></div><div id="handle"></div><div id="cupflowerf"></div></div>
  <div id="steam"></div>
  <div id="jflowerf"></div>
  <div id="motes"></div>
  <div id="petals"></div>
  <div id="bloom"></div>
 </div>
 <div id="titlewrap"><div class="tt">ジャスミンティーが<br>冷めるまで</div><div class="tbrush"></div><div class="tart">水野 灯</div></div>
 <div id="scenes"></div>
 <div id="grain"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="jasmine-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=5551234;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');if(cls)d.className=cls;if(st)d.style.cssText+=st;p.appendChild(d);return d;}

// stars
const sf=document.getElementById('starf');
for(let i=0;i<40;i++){const s=mk(sf,'left:'+(rnd()*1080)+'px;top:'+(rnd()*760)+'px;opacity:'+(0.3+rnd()*0.6),'star');}
// city buildings + lit windows
const city=document.getElementById('city'),clit=document.getElementById('citylit');
let x=0;const BOK=['rgba(255,206,130,.9)','rgba(150,190,240,.8)','rgba(255,170,190,.8)','rgba(255,230,170,.9)'];
while(x<1080){const w=40+rnd()*70,h=90+rnd()*200;const b=mk(city,'left:'+x+'px;width:'+w+'px;height:'+h+'px','bldg');
  // windows
  for(let r=0;r<Math.floor(h/26);r++)for(let c=0;c<Math.floor(w/18);c++){ if(rnd()<0.5){mk(city,'left:'+(x+6+c*18)+'px;bottom:'+(8+r*26)+'px','wlit');}}
  x+=w+6+rnd()*14;}
// bokeh lights (blurred) over the city/river
for(let i=0;i<34;i++){const r=8+rnd()*26;mk(clit,'left:'+(rnd()*1080)+'px;top:'+(850+rnd()*280)+'px;width:'+r+'px;height:'+r+'px;background:'+BOK[(rnd()*BOK.length)|0]+';opacity:'+(0.4+rnd()*0.5),'bokeh');}
// river reflections
const rr=document.getElementById('riverref');const rref=[];
for(let i=0;i<22;i++){const e=mk(rr,'left:'+(rnd()*1080)+'px;background:linear-gradient(180deg,'+BOK[(rnd()*BOK.length)|0]+',transparent)','rref');rref.push({el:e,ph:rnd()*6.28,x:parseFloat(e.style.left)});}
// window frame mullions
const fr=document.getElementById('frame');
mk(fr,'left:50%;top:0;width:18px;height:1180px;transform:translateX(-50%)','mull');
mk(fr,'left:0;right:0;top:560px;height:18px','mull');
mk(fr,'left:-30px;top:0;width:34px;height:1180px','mull');mk(fr,'right:-30px;top:0;width:34px;height:1180px','mull');
// rain streaks
const stf=document.getElementById('streakf');
for(let i=0;i<60;i++){const h=40+rnd()*160;mk(stf,'left:'+(rnd()*1080)+'px;top:'+(rnd()*1120)+'px;height:'+h+'px;transform:rotate('+(4+rnd()*4)+'deg);opacity:'+(0.3+rnd()*0.6),'streak');}
// sliding droplets
const df=document.getElementById('dropf');const drops=[];
for(let i=0;i<22;i++){const e=mk(df,'left:'+(rnd()*1080)+'px','drop');drops.push({el:e,x:parseFloat(e.style.left),y:rnd()*1160,sp:40+rnd()*120,sz:0.7+rnd()*1.1,ph:rnd()*6.28});}
// bookshelf bokeh
const shl=document.getElementById('shelflit');
for(let i=0;i<10;i++){const r=14+rnd()*30;mk(shl,'position:absolute;left:'+(rnd()*210)+'px;top:'+(80+rnd()*460)+'px;width:'+r+'px;height:'+r+'px;background:rgba(255,200,120,.7);z-index:2','slit');}
// books (stacked, right)
const bk=document.getElementById('books');
const BC=['#3a5a3a','#6a4028','#4a4a6a','#7a5a2a'];
[[0,0,300,34],[16,34,270,30],[40,64,236,28]].forEach((b,i)=>{mk(bk,'left:'+b[0]+'px;bottom:'+b[1]+'px;width:'+b[2]+'px;height:'+b[3]+'px;background:linear-gradient(180deg,'+BC[i]+',rgba(0,0,0,.3))','book');});
// jasmine flower builder
function jasmine(parent,cx,cy,sc,z){const f=mk(parent,'left:'+cx+'px;top:'+cy+'px;width:'+(90*sc)+'px;height:'+(90*sc)+'px;z-index:'+z,'jflower');
  for(let p=0;p<5;p++){const pt=mk(f,'width:'+(30*sc)+'px;height:'+(46*sc)+'px;background:radial-gradient(circle at 50% 70%,#fffefb,#f3eee6 70%,#e6dccb);box-shadow:0 1px 4px rgba(0,0,0,.15)','jpetal');
    pt.style.transform='translate(-50%,-100%) rotate('+(p*72)+'deg)';}
  mk(f,'width:'+(22*sc)+'px;height:'+(22*sc)+'px','jcenter');return f;}
// cup pattern flowers (small, green leaves + jasmine)
const cf=document.getElementById('cupflowerf');
jasmine(cf,150,150,0.5,14);jasmine(cf,205,170,0.42,14);
mk(cf,'position:absolute;left:120px;top:176px;width:40px;height:16px;border-radius:0 60% 0 60%;background:#6a9a52;transform:rotate(20deg);z-index:14');
mk(cf,'position:absolute;left:210px;top:150px;width:36px;height:14px;border-radius:0 60% 0 60%;background:#6a9a52;transform:rotate(-30deg);z-index:14');
// foreground jasmine clusters (bottom-left + by vase)
const jf=document.getElementById('jflowerf');
function leaf(p,x,y,a,sc){mk(p,'position:absolute;left:'+x+'px;top:'+y+'px;width:'+(70*sc)+'px;height:'+(28*sc)+'px;border-radius:0 70% 0 70%;background:linear-gradient(120deg,#4f8544,#356a34);transform:rotate('+a+'deg);z-index:16');}
leaf(jf,40,1560,-18,1.4);leaf(jf,150,1660,26,1.2);leaf(jf,0,1700,8,1.3);
jasmine(jf,20,1560,1.5,16);jasmine(jf,150,1600,1.25,16);jasmine(jf,70,1690,1.35,16);jasmine(jf,230,1680,0.9,16);
// by the vase (right)
leaf(jf,830,1360,-30,0.9);leaf(jf,910,1340,18,0.8);
jasmine(jf,840,1320,0.9,16);jasmine(jf,900,1300,0.78,16);jasmine(jf,880,1380,0.7,16);
// steam wisps
const steam=document.getElementById('steam');const wisps=[];
for(let i=0;i<20;i++){const w=28+rnd()*44;const e=mk(steam,'width:'+w+'px;height:'+w+'px','swisp');
  wisps.push({el:e,col:120+(rnd()-0.5)*90,base:rnd()*720,sp:40+rnd()*46,amp:8+rnd()*16,ph:rnd()*6.28,sz:0.7+rnd()*0.8});}
// warm motes
const mf=document.getElementById('motes');const motes=[];
for(let i=0;i<22;i++){const w=4+rnd()*12;const e=mk(mf,'width:'+w+'px;height:'+w+'px','mote');
  motes.push({el:e,x:rnd()*1080,y:rnd()*1920,sp:7+rnd()*18,amp:18+rnd()*44,ph:rnd()*6.28,base:rnd()*1920});}
// drifting petals
const pf=document.getElementById('petals');const petals=[];
for(let i=0;i<7;i++){const e=mk(pf,'position:absolute;width:26px;height:34px;border-radius:50% 50% 50% 50%/70% 70% 40% 40%;background:radial-gradient(circle at 50% 70%,#fffefb,#ece3d4)','');
  petals.push({el:e,x:rnd()*1080,y:rnd()*1920,sp:18+rnd()*26,sway:40+rnd()*60,ph:rnd()*6.28,rot:(rnd()-0.5)*2,base:rnd()*1920});}
// moon reflection in the empty cup (appears as steam fades)
const cupmoon=mk(document.getElementById('cup'),'position:absolute;left:150px;bottom:150px;width:60px;height:36px;border-radius:50%;z-index:14;opacity:0;background:radial-gradient(ellipse at 50% 40%,rgba(235,242,255,.9),rgba(190,206,240,.2) 70%,transparent);filter:blur(1px)','');

const world=document.getElementById('world'),moon=document.getElementById('moon'),moonglow=document.getElementById('moonglow'),
  lampglow=document.getElementById('lampglow'),bloom=document.getElementById('bloom'),titlewrap=document.getElementById('titlewrap'),
  wrim=document.getElementById("wrim"),sleeve=document.getElementById("sleeve"),woman=document.getElementById('woman');

// BGM = source 155.5s.. (2nd chorus, title hook). climax light-bloom in the back half.
const CL_IN=9000, CL_PK=21000, CL_OUT=28500;
const scenes=[
 {s:2400, e:6600,  html:'<div class="sc"><div class="lyr">あなたが好きだった<br><span class="hl">白いカップ</span><span class="en">The white cup you always loved.</span></div></div>'},
 {s:6600, e:11000, html:'<div class="sc"><div class="lyr">泣くためじゃない<br>忘れるため<span class="en">Not to cry — but to let you go.</span></div></div>'},
 {s:11000,e:15600, html:'<div class="sc"><div class="lyr"><span class="hl">ジャスミンティーが<br>冷めるまでは</span><span class="en">Until the jasmine tea goes cold …</span></div></div>'},
 {s:15600,e:20000, html:'<div class="sc"><div class="lyr">あなたを想って<br>いてもいいでしょう<span class="en">… let me keep thinking of you, won’t you.</span></div></div>'},
 {s:20000,e:24200, html:'<div class="sc"><div class="lyr">空のカップに<br><span class="hl">映った月</span><span class="en">A moon, reflected in the empty cup.</span></div></div>'},
 {s:24200,e:27200, html:'<div class="sc"><div class="lyr">明日の私は<br><span class="hl">きっと笑ってる</span><span class="en">Tomorrow, I’ll surely be smiling.</span></div></div>'},
 {s:27200,e:30000, html:'<div class="sc"><span class="badge">NEW SONG</span><div class="cta-t">ジャスミンティーが<br>冷めるまで</div><div class="cta-a">水野 灯</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>'},
];
const scEls=[];const marks=[];const scenesEl=document.getElementById('scenes');
scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
  scenesEl.appendChild(el);scEls.push(el);marks.push({start:sc.s,end:sc.e});});
const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const climax=smooth(t,CL_IN,CL_PK)*(1-0.4*smooth(t,CL_OUT,30000));
  // tea cooling: steam amount fades from 1 -> ~0.18 over the clip
  const cool=1-0.82*smooth(t,1500,27000);
  // very slow intimate drift of the room
  world.style.transform='translateY('+(Math.sin(ts*0.3)*3).toFixed(2)+'px) scale('+(1.01+0.012*climax)+')';
  // moon + glow breathe, brighter at climax
  moonglow.style.opacity=(0.7+0.12*Math.sin(ts*0.5)+0.3*climax).toFixed(3);
  moon.style.transform='translate(-50%,-50%) scale('+(1+0.02*Math.sin(ts*0.6)+0.04*climax)+')';
  // warm lamp breathe (candle-like)
  lampglow.style.opacity=(0.78+0.08*Math.sin(ts*1.3)+0.06*Math.sin(ts*3.7)+0.22*climax).toFixed(3);
  // river reflections shimmer
  for(const r of rref){r.el.style.opacity=(0.35+0.3*Math.abs(Math.sin(ts*0.9+r.ph))).toFixed(3);
    r.el.style.transform='translateX('+(Math.sin(ts*0.7+r.ph)*8).toFixed(1)+'px) scaleY('+(1+0.3*Math.sin(ts*1.1+r.ph))+')';}
  // rain droplets slide down, reset to top
  for(const d of drops){let y=((d.y+ts*d.sp)%1240);const op=y<40?smooth(y,0,40):(y>1120?1-smooth(y,1120,1200):1);
    d.el.style.transform='translate('+(Math.sin(ts*0.6+d.ph)*3).toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+d.sz+')';d.el.style.opacity=(op*0.8).toFixed(3);}
  // steam wisps rise, wobble, fade, scaled by cooling
  for(const w of wisps){let y=720-((ts*w.sp+w.base)%820);
    const prog=1-(y/720);                    // 0 at bottom(cup) .. 1 at top
    const op=(prog<0.12?smooth(prog,0,0.12):1-smooth(prog,0.55,1))* (0.82) * cool;
    const xx=180+Math.sin(ts*0.9+w.ph+prog*3)*w.amp*(0.3+prog*0.7);
    w.el.style.transform='translate('+xx.toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(w.sz*(0.7+prog*1.4))+')';
    w.el.style.opacity=Math.max(0,op).toFixed(3);}
  // moon reflected in cup appears as the tea cools (late)
  cupmoon.style.opacity=(smooth(t,19000,27000)*(0.5+0.4*Math.sin(ts*0.8))).toFixed(3);
  // warm motes float up
  for(const m of motes){let y=1960-((ts*m.sp+m.base)%2100);let xx=m.x+Math.sin(ts*0.4+m.ph)*m.amp;
    const op=(y>1760?smooth(y,1960,1740):(y<140?smooth(y,-60,140):1));
    m.el.style.transform='translate('+xx.toFixed(1)+'px,'+y.toFixed(1)+'px)';m.el.style.opacity=(op*(0.3+0.5*climax+0.2)).toFixed(3);}
  // drifting petals
  for(const p of petals){let y=((p.base+ts*p.sp)%2100)-120;let xx=p.x+Math.sin(ts*0.5+p.ph)*p.sway;
    p.el.style.transform='translate('+xx.toFixed(1)+'px,'+y.toFixed(1)+'px) rotate('+(ts*30*p.rot).toFixed(1)+'deg)';
    p.el.style.opacity=(0.5*smooth(y,-120,120)*(1-smooth(y,1700,1980))).toFixed(3);}
  // woman: gentle breathing + warm rim grows with light; tiny chin-hand sway
  woman.style.transform='translateY('+(Math.sin(ts*0.5)*2.5).toFixed(2)+'px) rotate('+(Math.sin(ts*0.33)*0.3).toFixed(2)+'deg)';
  sleeve.style.transform='rotate('+(12+Math.sin(ts*0.5)*0.5).toFixed(2)+'deg)';
  wrim.style.opacity=(0.3+0.5*climax).toFixed(3);
  // title / scenes
  const tvis=Math.max(0,Math.min(smooth(t,350,1300),1-smooth(t,2000,2400)));
  titlewrap.style.opacity=tvis.toFixed(3);
  titlewrap.style.transform='translateY('+((1-tvis)*-8).toFixed(1)+'px)';
  bloom.style.opacity=(0.42*climax).toFixed(3);
  const FADE=360;
  for(let i=0;i<scEls.length;i++){const m=marks[i];const o=smooth(t,m.start,m.start+FADE)*(1-smooth(t,m.end-FADE,m.end));
    scEls[i].style.opacity=o.toFixed(3);scEls[i].style.transform='translateY('+((1-o)*16).toFixed(1)+'px)';}
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;
function play(){document.getElementById('ui').style.display='none';
  try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);
    barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const st=performance.now();(function fo(){const k=(performance.now()-st)/1500;
    bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1500);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ジャスミンティーが冷めるまで / 水野灯</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
