# -*- coding: utf-8 -*-
"""
We Are the Fireflies / w-Band — 縦型9:16 宣伝ショート（やさしく壮大なアンセム / 3歳以上の日米インド向け）
ジャケット準拠：黄昏の棚田の谷。天の川の夜空→山の端に夕焼け、霧の山並み、谷に灯る村の灯、水を張った棚田の反射、
古民家の縁側（暖かな窓・風鈴）に長い髪の白いワンピの女性と黒猫が座って眺める、前景の草、そして無数の蛍。
主役＝蛍。たくさんの黄緑の光がゆっくり舞い、点滅し、少しずつ昇っていく。サビで光が増え、昇って「光の川」に。
演出：ビート同期はごく控えめ（87BPM, beat 689.7ms, +25ms）。キックで蛍の明滅と村灯がふわっと脈打つ程度。
BGM: fireflies-bgm.mp3 (source 4:48/288s の最終サビ 218s〜：歌詞が明瞭、ささやきのイントロ/アウトロは回避)。
画面テキストは「タイトルとアーティスト」のみ（歌詞テロップなし・ユーザー指示）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","fireflies.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0a1026;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0a1026}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"EB Garamond","Noto Serif JP",serif;background:#111a38}
#world{position:absolute;inset:-20px;transform-origin:50% 56%}
/* sky: starry night -> sunset at the mountain horizon */
#sky{position:absolute;left:0;right:0;top:0;height:1300px;background:
  linear-gradient(180deg,#0b1430 0%,#14204a 22%,#243260 40%,#3d3a68 54%,#6a4a66 64%,#b0624e 73%,#e08a52 80%,#f0a862 86%,#caa0a0 100%)}
#milky{position:absolute;left:-10%;top:40px;width:130%;height:520px;pointer-events:none;mix-blend-mode:screen;opacity:.5;
  background:radial-gradient(60% 40% at 50% 40%,rgba(200,210,255,.3),transparent 70%);transform:rotate(-18deg)}
.star{position:absolute;border-radius:50%;background:#eef3ff}
/* misty mountains (layered) */
#mtns{position:absolute;left:0;right:0;top:720px;height:360px}
.mtn{position:absolute;left:-5%;width:110%;bottom:0;border-radius:50% 50% 0 0/100% 100% 0 0}
/* valley mist */
#mist{position:absolute;left:0;right:0;top:930px;height:260px;z-index:2;pointer-events:none}
.mband{position:absolute;left:-10%;width:120%;height:70px;border-radius:50%;background:rgba(190,205,230,.1);filter:blur(16px)}
/* village warm lights */
#village{position:absolute;left:0;right:0;top:940px;height:180px;z-index:2}
.vlight{position:absolute;border-radius:50%;filter:blur(1px)}
/* terraced rice paddies (reflective water) */
#paddies{position:absolute;left:0;right:0;top:1080px;bottom:0;z-index:2;
  background:linear-gradient(180deg,#24406a 0%,#1c3458 24%,#15284a 60%,#0e1c38 100%)}
#paddies::before{content:"";position:absolute;left:0;right:0;top:0;height:150px;mix-blend-mode:screen;opacity:.5;
  background:linear-gradient(180deg,rgba(230,140,90,.45),rgba(180,110,120,.15) 50%,transparent)}
#paddies::after{content:"";position:absolute;left:0;right:0;top:120px;height:560px;opacity:.5;
  background:repeating-linear-gradient(180deg,rgba(120,150,200,.12) 0 2px,transparent 2px 96px)}
.terrace{position:absolute;left:-6%;width:112%;border-radius:50%/40px;
  background:linear-gradient(180deg,rgba(120,150,200,.18),rgba(40,70,120,.05));box-shadow:0 2px 10px rgba(0,0,0,.2)}
.pref{position:absolute;border-radius:50%;filter:blur(2px);mix-blend-mode:screen}
/* old farmhouse (left) + porch + window + wind chime */
#house{position:absolute;left:-30px;top:60px;width:430px;height:1200px;z-index:4}
#hwall{position:absolute;left:0;top:120px;width:360px;height:1080px;background:linear-gradient(90deg,#1a140f,#2a1f16 70%,#241a12);
  box-shadow:14px 0 40px rgba(0,0,0,.4)}
#eave{position:absolute;left:-30px;top:60px;width:470px;height:90px;background:linear-gradient(180deg,#2a2018,#140e09);transform:skewX(6deg);border-radius:0 0 8px 8px}
#post{position:absolute;left:300px;top:120px;width:26px;height:1080px;background:linear-gradient(90deg,#2a2018,#17110b)}
#win{position:absolute;left:66px;top:330px;width:164px;height:210px;border-radius:4px;
  background:linear-gradient(180deg,#ffdd9a,#f0b265 60%,#d88a44);box-shadow:0 0 50px 14px rgba(255,200,120,.45),inset 0 0 0 9px #2a1c10}
#win::after{content:"";position:absolute;inset:10px;background:
  linear-gradient(90deg,transparent 48%,rgba(90,60,30,.6) 49% 51%,transparent 52%),linear-gradient(180deg,transparent 48%,rgba(90,60,30,.6) 49% 51%,transparent 52%)}
#winglow{position:absolute;left:-40px;top:230px;width:420px;height:460px;z-index:3;pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(44% 42% at 40% 44%,rgba(255,196,110,.5),transparent 70%)}
#porch{position:absolute;left:-30px;bottom:0;width:470px;height:300px;z-index:4;background:linear-gradient(180deg,#2a1d12,#140d08);transform:perspective(500px) rotateX(16deg);transform-origin:bottom}
#chimewire{position:absolute;left:150px;top:150px;width:2px;height:70px;background:rgba(220,220,220,.4);z-index:5}
#chime{position:absolute;left:132px;top:214px;width:40px;height:40px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;z-index:5;transform-origin:50% -140%;
  background:radial-gradient(circle at 38% 30%,rgba(210,235,255,.85),rgba(150,190,230,.4) 60%,rgba(120,160,210,.2));box-shadow:0 0 12px rgba(200,230,255,.5)}
#chime::after{content:"";position:absolute;left:16px;top:38px;width:6px;height:46px;background:linear-gradient(180deg,#e8e0c8,#c0b48a)}
/* woman + cat (left foreground, backlit silhouette, warm rim) */
#woman{position:absolute;left:180px;bottom:170px;width:360px;height:470px;z-index:6;transform-origin:44% 100%}
#whead{position:absolute;left:150px;top:30px;width:96px;height:112px;z-index:5;border-radius:48% 52% 48% 50%;background:#0c0a14;transform:rotate(6deg)}
#whair{position:absolute;left:128px;top:24px;width:150px;height:300px;z-index:6;transform-origin:50% 8%;
  background:linear-gradient(96deg,#0a0810,#17121f 62%,#2b2235);
  border-radius:52% 48% 42% 44% / 40% 40% 60% 60%;transform:rotate(5deg)}
#wbody{position:absolute;left:54px;bottom:0;width:280px;height:360px;z-index:6;
  background:linear-gradient(100deg,#0b0912,#1a1422 70%,#2a2234);
  clip-path:polygon(40% 2%,58% 0,66% 14%,62% 30%,78% 40%,96% 78%,100% 100%,0 100%,16% 70%,30% 46%,30% 22%)}
#wdressrim{position:absolute;left:54px;bottom:0;width:280px;height:360px;z-index:7;pointer-events:none;mix-blend-mode:screen;opacity:.5;
  background:linear-gradient(82deg,rgba(255,224,156,.55),transparent 34%);
  clip-path:polygon(40% 2%,58% 0,66% 14%,62% 30%,78% 40%,96% 78%,100% 100%,0 100%,16% 70%,30% 46%,30% 22%)}
#cat{position:absolute;left:300px;bottom:10px;width:150px;height:140px;z-index:7;background:#09070e;
  clip-path:polygon(16% 100%,10% 50%,2% 30%,16% 36%,22% 14%,34% 34%,52% 30%,70% 40%,96% 30%,88% 52%,92% 100%)}
#cattail{position:absolute;left:420px;bottom:14px;width:90px;height:40px;z-index:7;border-top-left-radius:60px;border:16px solid #09070e;border-right:none;border-bottom:none;transform-origin:left bottom}
#wrim{position:absolute;left:150px;bottom:150px;width:420px;height:720px;z-index:8;pointer-events:none;mix-blend-mode:screen;opacity:.0;
  background:linear-gradient(74deg,rgba(255,214,150,.5),transparent 32%)}
/* foreground grass */
#grass{position:absolute;left:0;right:0;bottom:0;height:320px;z-index:9;pointer-events:none}
.blade{position:absolute;bottom:0;width:8px;border-radius:50% 50% 0 0;background:linear-gradient(180deg,#1e3420,#0c1a0e);transform-origin:bottom center}
/* fireflies (the hero) */
#flies{position:absolute;inset:0;z-index:10;pointer-events:none}
.fly{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(228,255,150,1),rgba(180,240,90,.5) 36%,rgba(150,220,70,0) 72%)}
#bloom{position:absolute;inset:0;z-index:11;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(70% 50% at 50% 70%,rgba(200,240,120,.3),transparent 70%)}
/* text (title + artist only) */
#titlewrap{position:absolute;left:26px;right:26px;top:150px;text-align:center;z-index:16;opacity:0}
.tt{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-style:italic;font-size:124px;line-height:1.0;letter-spacing:1px;color:#f5eeca;
  text-shadow:0 0 24px rgba(210,240,130,.6),0 0 50px rgba(180,230,90,.4),0 4px 18px rgba(10,16,40,.7)}
.tund{width:70%;height:3px;margin:14px auto 12px;background:linear-gradient(90deg,transparent,rgba(228,255,150,.9),transparent);box-shadow:0 0 12px rgba(200,240,120,.8)}
.tart{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:500;font-size:54px;letter-spacing:12px;color:#eaf0e0;text-shadow:0 2px 14px rgba(10,16,40,.7),0 0 20px rgba(200,230,130,.4)}
#cta{position:absolute;left:26px;right:26px;top:580px;text-align:center;z-index:16;opacity:0}
.badge{display:inline-block;font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:7px;color:#18220e;
  background:linear-gradient(90deg,#e4ff96,#bfe86a);padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-s{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-size:38px;letter-spacing:3px;color:#dcf0a8;margin-top:22px}
.cta-b{font-family:"EB Garamond",serif;font-weight:600;font-size:30px;letter-spacing:10px;color:#eaf0e0;margin-top:12px;opacity:.9}
#grain{position:absolute;inset:0;z-index:17;pointer-events:none;opacity:.045;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
#vig{position:absolute;inset:0;pointer-events:none;z-index:18;background:radial-gradient(130% 82% at 50% 46%,transparent 50%,rgba(5,8,22,.66) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#18220e;font-size:60px;background:linear-gradient(135deg,#e4ff96,#bfe86a);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,#e4ff96,#bfe86a)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="sky"></div>
  <div id="milky"></div>
  <div id="starf"></div>
  <div id="mtns"></div>
  <div id="mist"></div>
  <div id="village"></div>
  <div id="paddies"></div><div id="terracef"></div><div id="preff"></div>
  <div id="house">
    <div id="winglow"></div><div id="hwall"></div><div id="eave"></div><div id="post"></div>
    <div id="win"></div><div id="porch"></div>
    <div id="chimewire"></div><div id="chime"></div>
  </div>
  <div id="woman">
    <div id="whair"></div><div id="whead"></div><div id="wbody"></div><div id="wdressrim"></div>
  </div>
  <div id="cat"></div><div id="cattail"></div><div id="wrim"></div>
  <div id="grass"></div>
  <div id="flies"></div>
  <div id="bloom"></div>
 </div>
 <div id="titlewrap"><div class="tt">We Are the Fireflies</div><div class="tund"></div><div class="tart">w-Band</div></div>
 <div id="cta"><span class="badge">NEW SONG</span><div class="tt" style="font-size:104px">We Are the Fireflies</div><div class="tart" style="margin-top:12px">w-Band</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
 <div id="grain"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="fireflies-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=424242;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');if(cls)d.className=cls;if(st)d.style.cssText+=st;p.appendChild(d);return d;}

// stars (denser along the milky way band)
const sf=document.getElementById('starf');const stars=[];
for(let i=0;i<150;i++){const w=1+rnd()*3;const yy=rnd()*820;const e=mk(sf,'left:'+(rnd()*1080)+'px;top:'+yy+'px;width:'+w+'px;height:'+w+'px;opacity:'+(0.3+rnd()*0.6),'star');stars.push({el:e,ph:rnd()*6.28,sp:1+rnd()*3});}
// mountains (layered jagged range, misty; back lighter). sunset glow behind the ridge.
const mt=document.getElementById('mtns');
mk(mt,'left:20%;right:16%;bottom:70px;height:190px;background:radial-gradient(60% 100% at 46% 100%,rgba(255,156,92,.55),rgba(255,120,80,.2) 46%,transparent 74%);mix-blend-mode:screen','');
const RIDGES=[
 ['#3b4670',150,'polygon(0 100%,0 56%,10% 44%,20% 52%,30% 36%,42% 50%,52% 34%,64% 48%,74% 30%,86% 46%,100% 34%,100% 100%)'],
 ['#313c60',200,'polygon(0 100%,0 62%,12% 46%,24% 58%,34% 40%,46% 56%,58% 38%,70% 54%,82% 36%,92% 52%,100% 42%,100% 100%)'],
 ['#28324e',260,'polygon(0 100%,0 70%,14% 54%,26% 66%,40% 48%,54% 64%,66% 46%,80% 62%,90% 50%,100% 60%,100% 100%)']];
RIDGES.forEach(([c,h,cp],i)=>{mk(mt,'left:-5%;width:110%;bottom:0;height:'+h+'px;background:linear-gradient(180deg,'+c+','+c+');clip-path:'+cp+';opacity:'+(0.86+i*0.05),'mtn');});
// valley mist bands
const mi=document.getElementById('mist');const mbands=[];
for(let i=0;i<5;i++){const yy=i*44+rnd()*20;const e=mk(mi,'top:'+yy+'px','mband');mbands.push({el:e,x:rnd()*200,sp:6+rnd()*8,ph:rnd()*6.28});}
// village warm lights (bokeh clusters in the valley)
const vg=document.getElementById('village');const vlights=[];const VC=['rgba(255,200,120,.95)','rgba(255,220,150,.9)','rgba(255,180,100,.9)'];
for(let i=0;i<40;i++){const r=4+rnd()*12;const e=mk(vg,'left:'+(rnd()*1080)+'px;top:'+(20+rnd()*150)+'px;width:'+r+'px;height:'+r+'px;background:'+VC[(rnd()*3)|0],'vlight');vlights.push({el:e,ph:rnd()*6.28,sp:0.8+rnd()*2});}
// terraced paddies + their reflections
const tf=document.getElementById('terracef');
for(let i=0;i<5;i++){const yy=1120+i*130;mk(tf,'top:'+yy+'px;height:'+(90+i*14)+'px','terrace');}
const prf=document.getElementById('preff');const prefs=[];
for(let i=0;i<70;i++){const r=5+rnd()*13;const yy=1120+rnd()*740;const e=mk(prf,'left:'+(rnd()*1080)+'px;top:'+yy+'px;width:'+r+'px;height:'+(r*0.5)+'px;background:radial-gradient(circle,rgba(255,210,140,.6),transparent 70%)','pref');prefs.push({el:e,ph:rnd()*6.28,sp:1+rnd()*2.5});}
// grass blades (foreground)
const gr=document.getElementById('grass');const blades=[];
for(let i=0;i<60;i++){const h=80+rnd()*200;const x=rnd()*1080;const e=mk(gr,'left:'+x+'px;height:'+h+'px;width:'+(6+rnd()*6)+'px','blade');blades.push({el:e,ph:rnd()*6.28,sp:0.5+rnd()*0.8,lean:(rnd()-0.5)*8});}
// FIREFLIES (hero): many, drifting + blinking + slowly rising
const ff=document.getElementById('flies');const flies=[];
for(let i=0;i<120;i++){const near=rnd();const sz=4+near*near*18;
  // bias vertical start lower (more fireflies near grass/paddies)
  const y0=560+Math.pow(rnd(),0.7)*1340;
  const e=mk(ff,'width:'+sz+'px;height:'+sz+'px','fly');
  flies.push({el:e,x:rnd()*1080,y:y0,sz:sz,rise:5+rnd()*16+near*12,driftA:14+rnd()*40,driftP:rnd()*6.28,driftS:0.2+rnd()*0.4,
    blinkR:1.3+rnd()*2.2,blinkP:rnd()*6.28,base:rnd()*1340,near:near});}

const world=document.getElementById('world'),milky=document.getElementById('milky'),winglow=document.getElementById('winglow'),
  chime=document.getElementById('chime'),bloom=document.getElementById('bloom'),titlewrap=document.getElementById('titlewrap'),cta=document.getElementById('cta'),
  wrim=document.getElementById('wrim'),whair=document.getElementById('whair'),woman=document.getElementById('woman'),cattail=document.getElementById('cattail');

const BEAT=689.7, OFF=25;                // 87bpm, +25ms (gentle)
// BGM = source 218s.. (final chorus "...bring the whole world home / We are the fireflies"). climax builds.
const CL_IN=4000, CL_PK=22000;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const bp=(((t-OFF)%BEAT)+BEAT)%BEAT/BEAT;
  const swell=0.5+0.5*Math.cos(bp*6.2832);     // gentle 0..1 peak on the beat
  const climax=smooth(t,CL_IN,CL_PK);
  // very slow breath of the whole scene
  world.style.transform='translateY('+(Math.sin(ts*0.25)*2.5).toFixed(2)+'px) scale('+(1.01+0.008*climax)+')';
  milky.style.opacity=(0.4+0.12*Math.sin(ts*0.4)+0.12*climax).toFixed(3);
  // stars twinkle
  for(const s of stars){s.el.style.opacity=(0.3+0.5*Math.abs(Math.sin(ts*s.sp+s.ph))).toFixed(3);}
  // village + paddy reflections twinkle (gentle beat swell)
  for(const v of vlights){v.el.style.opacity=((0.5+0.4*Math.abs(Math.sin(ts*v.sp+v.ph)))*(0.8+0.2*swell)).toFixed(3);}
  for(const p of prefs){p.el.style.opacity=((0.3+0.4*Math.abs(Math.sin(ts*p.sp+p.ph)))*(0.7+0.3*swell)).toFixed(3);
    p.el.style.transform='scaleX('+(1+0.3*Math.sin(ts*0.6+p.ph))+')';}
  // mist drifts
  for(const m of mbands){const x=m.x+((ts*m.sp)%260)-20;m.el.style.transform='translateX('+x.toFixed(1)+'px)';m.el.style.opacity=(0.5+0.3*Math.sin(ts*0.3+m.ph)).toFixed(3);}
  // house window glow breathe
  winglow.style.opacity=(0.5+0.12*Math.sin(ts*0.9)+0.1*swell).toFixed(3);
  // wind chime sway + glint
  chime.style.transform='rotate('+(Math.sin(ts*1.1)*7).toFixed(2)+'deg)';
  // grass sway
  for(const b of blades){b.el.style.transform='rotate('+(b.lean+Math.sin(ts*b.sp+b.ph)*5).toFixed(2)+'deg)';}
  // woman hair flutter + warm rim grows
  whair.style.transform='rotate('+(Math.sin(ts*0.8)*2.2).toFixed(2)+'deg)';
  woman.style.transform='translateY('+(Math.sin(ts*0.5)*1.5).toFixed(2)+'px)';
  cattail.style.transform='rotate('+(10+Math.sin(ts*1.3)*8).toFixed(1)+'deg)';
  wrim.style.opacity=(0.3+0.4*climax).toFixed(3);
  // FIREFLIES: drift, rise, blink; climax => brighter + rise faster (light rises)
  const riseBoost=1+1.6*climax;
  for(const f of flies){
    let y=f.y - ((ts*f.rise*riseBoost + f.base)% 1400);   // rise, wrap
    if(y<-40)y+=1400;
    const x=f.x + Math.sin(ts*f.driftS+f.driftP)*f.driftA;
    const blink=Math.pow(Math.max(0,Math.sin(ts*f.blinkR+f.blinkP)),3);
    const vis=(0.25+0.75*blink)*(0.5+0.5*climax+0.15)*(0.85+0.15*swell);
    f.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(0.8+0.5*blink).toFixed(3)+')';
    f.el.style.opacity=Math.min(1,vis).toFixed(3);
    f.el.style.boxShadow='0 0 '+(6+f.sz*0.9*blink)+'px '+(2+f.sz*0.3*blink)+'px rgba(190,240,100,'+(0.5*blink).toFixed(2)+')';}
  bloom.style.opacity=(0.4*climax*(0.7+0.3*swell)).toFixed(3);
  // title reveals (title + artist only): open 0.3-5s, re-flash ~13s, blaze 20-26s
  const tOpen=Math.min(smooth(t,300,1200),1-smooth(t,4600,5300));
  const tFlash=Math.min(smooth(t,12600,13000),1-smooth(t,14000,14400))*0.85;
  const tBlaze=Math.min(smooth(t,20000,20900),1-smooth(t,26000,26700));
  const tvis=Math.max(tOpen,tFlash,tBlaze);
  titlewrap.style.opacity=tvis.toFixed(3);
  titlewrap.style.transform='translateY('+((1-tvis)*-8).toFixed(1)+'px) scale('+(1+0.02*swell*(tBlaze>0?1:0.4)).toFixed(3)+')';
  const cvis=smooth(t,26500,27200);
  cta.style.opacity=cvis.toFixed(3);
  cta.style.transform='scale('+(0.98+0.02*cvis).toFixed(3)+')';
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;const TOTAL=30000;window.TOTAL=TOTAL;
function play(){document.getElementById('ui').style.display='none';
  try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);
    barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const s0=performance.now();(function fo(){const k=(performance.now()-s0)/1500;
    bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1500);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>We Are the Fireflies / w-Band</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
