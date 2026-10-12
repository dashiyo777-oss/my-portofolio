# -*- coding: utf-8 -*-
"""
白い帆 / Seira Lumen — 縦型9:16 宣伝ショート（シネマティック・オーケストラ・バラード / 2歳以上の日米向け）
ジャケット準拠：黄金時間の海。白いドレスの女性が帆船の舳先で手すりに手をかけ、風に髪とドレスをなびかせ光を見上げる。
左上を占める大きな白い帆（はためき）、索具・ウインチ・手すり、右の岬に白い灯台、舞うカモメ、
水平線に沈む太陽ときらめく光の道、深い青の海としぶき。
演出：ビート同期ではなくシネマティックな緩やかなうねり（船の揺れ・帆のはためき・雲と光のドリフト・髪となびき）。
最終サビ（転調・フルオケ＆合唱）で光がブルームして暖色に満ちる。
BGM: shiroihan-bgm.mp3 (source 4:05/245s の最終サビ 205s〜：転調サビ→締めのハープ)。
英語の簡単な訳つき。画面テキストはジャケット表記＋提供歌詞のみ（創作なし）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","shiroihan.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0b2545;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0b2545}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Noto Serif JP",serif;background:#12427a}
#world{position:absolute;inset:-40px;transform-origin:50% 60%}
/* sky (bright golden-hour, like the jacket) */
#sky{position:absolute;inset:0;background:
  linear-gradient(180deg,#1f73ba 0%,#3a8fcf 20%,#6fb0dc 40%,#a6d0e8 54%,#d8ecf2 62%,#ffe8bf 71%,#ffd79e 82%,#ffc98e 92%,#f3bd84 100%)}
#clouds{position:absolute;left:0;right:0;top:120px;height:760px}
.cloud{position:absolute;border-radius:50%;filter:blur(14px);background:radial-gradient(circle,rgba(255,240,215,.9),rgba(255,225,190,.0) 70%)}
/* sun */
#sunglow{position:absolute;left:760px;top:720px;width:900px;height:900px;transform:translate(-50%,-50%);pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(circle,rgba(255,244,210,.95),rgba(255,210,130,.5) 26%,rgba(255,190,110,.18) 46%,transparent 68%)}
#rays{position:absolute;left:760px;top:720px;width:1600px;height:1600px;transform:translate(-50%,-50%);pointer-events:none;mix-blend-mode:screen;opacity:.5;
  background:conic-gradient(from 0deg,
   rgba(255,240,200,.0) 0deg,rgba(255,240,200,.22) 3deg,rgba(255,240,200,0) 8deg,
   rgba(255,240,200,0) 20deg,rgba(255,240,200,.18) 24deg,rgba(255,240,200,0) 30deg,
   rgba(255,240,200,0) 44deg,rgba(255,240,200,.2) 48deg,rgba(255,240,200,0) 54deg,
   rgba(255,240,200,0) 70deg,rgba(255,240,200,.16) 74deg,rgba(255,240,200,0) 80deg,
   rgba(255,240,200,0) 96deg,rgba(255,240,200,.2) 100deg,rgba(255,240,200,0) 106deg,
   rgba(255,240,200,0) 124deg,rgba(255,240,200,.16) 128deg,rgba(255,240,200,0) 134deg,
   rgba(255,240,200,0) 150deg,rgba(255,240,200,.2) 154deg,rgba(255,240,200,0) 160deg,
   rgba(255,240,200,0) 360deg)}
#sun{position:absolute;left:760px;top:740px;width:170px;height:170px;transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(circle at 50% 46%,#fffdf2,#fff0c4 40%,#ffd884 72%,rgba(255,200,110,0) 100%);
  box-shadow:0 0 90px 36px rgba(255,226,150,.65)}
/* headland + lighthouse (right) — warm-lit by the low sun */
#headland{position:absolute;right:-20px;top:706px;width:470px;height:210px}
#cliff{position:absolute;right:0;bottom:0;width:470px;height:120px;
  background:linear-gradient(180deg,#9a8a74,#6a5f55 60%,#4a4a52);border-radius:180px 70px 0 0/90px 44px 0 0;opacity:.92;
  box-shadow:inset 40px 14px 50px rgba(255,214,150,.4)}
#cliff::after{content:"";position:absolute;left:14px;right:40px;top:10px;height:40px;border-radius:60px;background:rgba(120,160,110,.4);filter:blur(4px)}
#light{position:absolute;right:120px;bottom:96px;width:38px;height:120px;border-radius:7px 7px 0 0;
  background:linear-gradient(90deg,#cfd0c8,#f6f4ec 42%,#e6cda6);box-shadow:0 2px 10px rgba(0,0,0,.2)}
#light::before{content:"";position:absolute;left:-8px;top:-24px;width:54px;height:28px;border-radius:8px 8px 4px 4px;background:#3a4656}
#light::after{content:"";position:absolute;left:5px;top:-16px;width:30px;height:14px;border-radius:4px;background:radial-gradient(circle,#fff6cf,#ffcf6e)}
#lightcap{position:absolute;right:111px;bottom:232px;width:54px;height:15px;border-radius:50%;background:#2a3645}
/* sea */
#sea{position:absolute;left:0;right:0;top:772px;bottom:0;background:
  linear-gradient(180deg,#3f86ac 0%,#2a6c98 10%,#1d5885 30%,#154a76 60%,#0e3a63 100%)}
#horizon{position:absolute;left:0;right:0;top:770px;height:8px;background:linear-gradient(90deg,rgba(255,224,170,.35),rgba(255,238,200,.95) 66%,rgba(255,220,170,.4));filter:blur(2px)}
#sunpath{position:absolute;left:760px;top:776px;width:420px;height:900px;transform:translateX(-50%);pointer-events:none;mix-blend-mode:screen;
  background:linear-gradient(180deg,rgba(255,236,186,.8),rgba(255,214,150,.22) 36%,transparent 80%);
  clip-path:polygon(43% 0,57% 0,100% 100%,0 100%);filter:blur(11px)}
.swell{position:absolute;left:-10%;width:120%;height:5px;border-radius:50%;background:rgba(255,255,255,.1);filter:blur(1.5px)}
#spray{position:absolute;left:0;right:0;bottom:0;height:420px;pointer-events:none}
.sparkle{position:absolute;width:6px;height:6px;border-radius:50%;background:radial-gradient(circle,#fff,rgba(255,240,200,0) 70%)}
/* gulls */
.gull{position:absolute;pointer-events:none}
.gull i{position:absolute;top:0;width:34px;height:10px;border-top:5px solid rgba(255,255,255,.92);border-radius:50%}
/* boat: big white sail upper-left + rigging + deck foreground */
#sail{position:absolute;left:-120px;top:-60px;width:720px;height:1180px;z-index:6;transform-origin:top left;
  background:linear-gradient(118deg,rgba(255,255,255,.97) 0%,rgba(244,250,255,.9) 42%,rgba(214,232,246,.82) 72%,rgba(190,214,236,.7) 100%);
  clip-path:polygon(0 0,62% 2%,46% 100%,0 100%);box-shadow:inset -40px 0 80px rgba(120,150,190,.35)}
#sail2{position:absolute;left:300px;top:-60px;width:380px;height:760px;z-index:5;transform-origin:top left;
  background:linear-gradient(130deg,rgba(255,255,255,.85),rgba(206,226,244,.6));clip-path:polygon(0 0,100% 6%,0 86%);opacity:.9}
#sailshade{position:absolute;left:-120px;top:-60px;width:720px;height:1180px;z-index:6;pointer-events:none;mix-blend-mode:multiply;
  clip-path:polygon(0 0,62% 2%,46% 100%,0 100%);opacity:.0;
  background:linear-gradient(118deg,rgba(90,120,160,0) 40%,rgba(80,110,150,.3) 100%)}
#mast{position:absolute;left:-116px;top:-60px;width:16px;height:1300px;z-index:7;background:linear-gradient(90deg,#caa877,#8a6a44);transform-origin:top center}
.rope{position:absolute;z-index:7;height:3px;background:rgba(240,235,220,.55);transform-origin:left center;filter:blur(.3px)}
#deck{position:absolute;left:-60px;bottom:-20px;width:720px;height:420px;z-index:8;transform:rotate(-7deg);transform-origin:left bottom;
  background:linear-gradient(180deg,#6a4a2c,#4a3420);border-radius:40px 180px 0 0;box-shadow:0 -6px 30px rgba(0,0,0,.3)}
#rail{position:absolute;left:120px;bottom:300px;width:620px;height:18px;z-index:9;transform:rotate(-7deg);transform-origin:left center;border-radius:10px;
  background:linear-gradient(180deg,#e7ddc8,#b7a988);box-shadow:0 3px 8px rgba(0,0,0,.3)}
.stanchion{position:absolute;bottom:300px;width:12px;height:70px;z-index:9;background:linear-gradient(180deg,#d8cdb4,#9c8e6e);border-radius:6px}
#winch{position:absolute;left:30px;bottom:150px;width:120px;height:120px;z-index:9;border-radius:50%;
  background:radial-gradient(circle at 40% 34%,#f0ead8,#b9ab86 60%,#7c7152);box-shadow:0 8px 20px rgba(0,0,0,.35)}
#winch::after{content:"";position:absolute;inset:26px;border-radius:50%;background:repeating-radial-gradient(circle,#8c7f5e 0 4px,#b9ab86 4px 9px)}
#coil{position:absolute;left:-10px;bottom:70px;width:200px;height:120px;z-index:9;border-radius:50%;
  background:repeating-radial-gradient(ellipse 100px 60px at 50% 50%,#c9b78c 0 10px,#9c8a62 10px 20px);clip-path:ellipse(100px 60px at 50% 50%);opacity:.95}
/* woman at the bow — elegant backlit silhouette, warm gold rim (looks to the sun, hair streaming leeward) */
#woman{position:absolute;left:316px;bottom:300px;width:250px;height:560px;z-index:10;transform-origin:50% 100%}
#halo{position:absolute;left:300px;bottom:320px;width:300px;height:360px;z-index:9;pointer-events:none;mix-blend-mode:screen;opacity:.0;
  background:radial-gradient(44% 42% at 56% 36%,rgba(255,234,172,.9),rgba(255,214,150,.3) 46%,transparent 72%);filter:blur(6px)}
#hair{position:absolute;left:58px;top:96px;width:160px;height:308px;z-index:10;
  background:linear-gradient(120deg,#160f0a,#241910 70%);
  clip-path:polygon(34% 0,70% 0,88% 22%,80% 48%,66% 74%,46% 96%,20% 86%,30% 58%,22% 34%,26% 12%);transform-origin:50% 8%;filter:blur(.5px)}
#dress{position:absolute;left:52px;bottom:0;width:170px;height:430px;z-index:11;
  background:linear-gradient(90deg,#191009,#271a10 56%,#372614);
  clip-path:polygon(40% 0,60% 0,64% 16%,58% 36%,72% 64%,94% 90%,98% 100%,6% 100%,22% 70%,30% 40%,34% 14%);
  box-shadow:inset -16px 0 34px rgba(255,210,150,.16)}
#torso{position:absolute;left:96px;bottom:236px;width:64px;height:182px;z-index:11;border-radius:34px 34px 24px 24px;
  background:linear-gradient(90deg,#1a110a,#2c1e13);transform:rotate(-4deg)}
#head{position:absolute;left:122px;bottom:394px;width:54px;height:66px;z-index:11;border-radius:50% 50% 48% 48%;
  background:linear-gradient(90deg,#1b130c,#30220f);transform-origin:50% 100%;transform:rotate(-8deg)}
#arm{position:absolute;left:150px;bottom:214px;width:22px;height:166px;z-index:11;border-radius:14px;
  background:linear-gradient(90deg,#190f09,#2a1c12);transform:rotate(6deg);transform-origin:top center}
#rim{position:absolute;left:52px;bottom:0;width:170px;height:430px;z-index:12;pointer-events:none;mix-blend-mode:screen;opacity:.0;
  background:linear-gradient(250deg,rgba(255,232,172,.95),transparent 24%);
  clip-path:polygon(40% 0,60% 0,64% 16%,58% 36%,72% 64%,94% 90%,98% 100%,6% 100%,22% 70%,30% 40%,34% 14%)}
/* light bloom overlay for the climax */
#bloom{position:absolute;inset:0;z-index:13;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:radial-gradient(60% 46% at 70% 40%,rgba(255,238,200,.85),rgba(255,214,150,.3) 40%,transparent 72%)}
#motes{position:absolute;inset:0;z-index:13;pointer-events:none}
.mote{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,246,220,.95),rgba(255,230,180,0) 70%)}
/* text */
#titlewrap{position:absolute;right:48px;top:150px;text-align:right;z-index:16;opacity:0}
.tt{font-family:"Noto Serif JP",serif;font-weight:900;font-size:188px;line-height:.98;letter-spacing:6px;color:#fff;
  text-shadow:0 6px 26px rgba(20,50,90,.55),0 0 40px rgba(255,255,255,.3)}
.tbrush{width:360px;height:14px;margin:6px 0 10px auto;border-radius:0 8px 8px 0;background:linear-gradient(90deg,transparent,#fff);
  -webkit-mask:linear-gradient(90deg,transparent,#000 20%,#000 80%,transparent);opacity:.92}
.tart{font-family:"Noto Serif JP",serif;font-weight:600;font-size:60px;letter-spacing:12px;color:#eaf2fb;text-shadow:0 3px 14px rgba(20,50,90,.5)}
#scenes{position:absolute;left:60px;right:60px;top:560px;height:520px;z-index:16}
.sc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;will-change:opacity,transform}
.lyr{font-family:"Noto Serif JP",serif;font-weight:800;font-size:82px;line-height:1.26;letter-spacing:3px;color:#fff;
  text-shadow:0 4px 22px rgba(15,40,80,.72),0 0 36px rgba(120,170,220,.4)}
.lyr .hl{color:#ffe6a6}
.lyr .en{display:block;font-family:"Noto Serif JP",serif;font-weight:500;font-style:italic;font-size:40px;letter-spacing:1px;color:#e6eefb;margin-top:22px;text-shadow:0 2px 14px rgba(10,30,60,.8)}
.badge{display:inline-block;font-family:"Noto Serif JP",serif;font-weight:700;font-size:34px;letter-spacing:8px;color:#13406f;
  background:linear-gradient(90deg,#fff,#e8f2ff);padding:9px 30px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(10,40,80,.4)}
.cta-t{font-family:"Noto Serif JP",serif;font-weight:900;font-size:150px;letter-spacing:6px;color:#fff;text-shadow:0 6px 26px rgba(15,40,80,.6)}
.cta-a{font-family:"Noto Serif JP",serif;font-weight:600;font-size:52px;letter-spacing:12px;color:#eaf2fb;margin-top:14px}
.cta-s{font-family:"Noto Serif JP",serif;font-weight:600;font-size:40px;letter-spacing:3px;color:#ffe6a6;margin-top:22px}
.cta-b{font-family:"Noto Serif JP",serif;font-weight:700;font-size:32px;letter-spacing:10px;color:#eaf2fb;margin-top:12px;opacity:.9}
#flash{position:absolute;inset:0;z-index:17;pointer-events:none;background:#fff;opacity:0;mix-blend-mode:screen}
#grain{position:absolute;inset:0;z-index:17;pointer-events:none;opacity:.05;background:
  repeating-radial-gradient(circle at 20% 30%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
#vig{position:absolute;inset:0;pointer-events:none;z-index:18;background:radial-gradient(130% 84% at 56% 42%,transparent 54%,rgba(8,22,46,.6) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:20}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#13406f;font-size:60px;background:linear-gradient(135deg,#fff,#cfe2f6);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.16);z-index:20}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffe6a6,#fff)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="sky"></div>
  <div id="clouds"></div>
  <div id="sunglow"></div>
  <div id="rays"></div>
  <div id="sun"></div>
  <div id="headland"><div id="cliff"></div><div id="light"></div></div><div id="lightcap"></div>
  <div id="sea"></div>
  <div id="horizon"></div>
  <div id="sunpath"></div>
  <div id="swellf"></div>
  <div id="spray"></div>
  <div id="gullf"></div>
  <div id="sail2"></div>
  <div id="sail"></div><div id="sailshade"></div>
  <div id="mast"></div>
  <div id="ropef"></div>
  <div id="halo"></div>
  <div id="woman">
    <div id="hair"></div><div id="dress"></div><div id="torso"></div><div id="head"></div><div id="arm"></div><div id="rim"></div>
  </div>
  <div id="deck"></div>
  <div id="coil"></div><div id="winch"></div>
  <div id="rail"></div><div id="stanf"></div>
  <div id="bloom"></div>
  <div id="motes"></div>
 </div>
 <div id="titlewrap"><div class="tt">白い帆</div><div class="tbrush"></div><div class="tart">Seira Lumen</div></div>
 <div id="scenes"></div>
 <div id="flash"></div><div id="grain"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="shiroihan-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=778899;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}

// clouds
const cf=document.getElementById('clouds');const clouds=[];
for(let i=0;i<9;i++){const c=document.createElement('div');c.className='cloud';const w=200+rnd()*320;
  c.style.cssText='width:'+w+'px;height:'+(w*0.42)+'px;left:'+(rnd()*1100-100)+'px;top:'+(rnd()*560)+'px;opacity:'+(0.4+rnd()*0.5);
  cf.appendChild(c);clouds.push({el:c,x:rnd()*1100-100,sp:6+rnd()*14,y:parseFloat(c.style.top)});}

// swell lines on the sea
const sw=document.getElementById('swellf');const swells=[];
for(let i=0;i<16;i++){const s=document.createElement('div');s.className='swell';const yy=800+i*62+rnd()*20;
  s.style.top=yy+'px';s.style.opacity=(0.05+rnd()*0.12);sw.appendChild(s);swells.push({el:s,y:yy,ph:rnd()*6.28,sp:0.4+rnd()*0.6});}

// water sparkles along the sun path
const sp=document.getElementById('spray');const sparks=[];
for(let i=0;i<70;i++){const s=document.createElement('div');s.className='sparkle';
  const cx=540+(rnd()-0.5)*(260+ (i*5));const yy=790+rnd()*560;
  s.style.left=(760+(rnd()-0.5)*(120+ (yy-790)*0.9))+'px';s.style.top=yy+'px';s.style.width=s.style.height=(4+rnd()*7)+'px';
  sp.appendChild(s);sparks.push({el:s,ph:rnd()*6.28,sp:2+rnd()*4});}

// gulls
const gf=document.getElementById('gullf');const gulls=[];
const gpos=[[720,300,1.6],[900,520,1.2],[1020,210,1.0]];
gpos.forEach(([x,y,sc])=>{const g=document.createElement('div');g.className='gull';g.style.cssText='left:'+x+'px;top:'+y+'px;transform:scale('+sc+')';
  const a=document.createElement('i'),b=document.createElement('i');a.style.left='-30px';a.style.transform='rotate(18deg)';b.style.left='4px';b.style.transform='rotate(-18deg)';
  g.appendChild(a);g.appendChild(b);gf.appendChild(g);gulls.push({el:g,a:a,b:b,x:x,y:y,sc:sc,ph:rnd()*6.28,sp:7+rnd()*5});});

// rigging ropes from mast top to deck points
const rf=document.getElementById('ropef');
const ropes=[[-108,-40,520,470],[-108,-40,240,560],[-108,120,560,360],[-108,80,120,300]];
ropes.forEach(([x1,y1,x2,y2])=>{const dx=x2-x1,dy=y2-y1;const len=Math.hypot(dx,dy);const ang=Math.atan2(dy,dx)*180/Math.PI;
  const r=document.createElement('div');r.className='rope';r.style.left=x1+'px';r.style.top=y1+'px';r.style.width=len+'px';r.style.transform='rotate('+ang+'deg)';rf.appendChild(r);});

// stanchions along the rail
const stf=document.getElementById('stanf');
for(let i=0;i<5;i++){const s=document.createElement('div');s.className='stanchion';s.style.left=(150+i*140)+'px';s.style.bottom=(300 - i*16)+'px';stf.appendChild(s);}

// light motes
const mf=document.getElementById('motes');const motes=[];
for(let i=0;i<26;i++){const m=document.createElement('div');m.className='mote';const w=4+rnd()*12;
  m.style.width=m.style.height=w+'px';mf.appendChild(m);
  motes.push({el:m,x:rnd()*1080,y:rnd()*1920,sp:8+rnd()*22,amp:20+rnd()*50,ph:rnd()*6.28,base:rnd()*1920});}

const world=document.getElementById('world'),sun=document.getElementById('sun'),sunglow=document.getElementById('sunglow'),rays=document.getElementById('rays'),
  sail=document.getElementById('sail'),sail2=document.getElementById('sail2'),sailshade=document.getElementById('sailshade'),mast=document.getElementById('mast'),
  hair=document.getElementById('hair'),dress=document.getElementById('dress'),head=document.getElementById('head'),arm=document.getElementById('arm'),
  rim=document.getElementById('rim'),bloom=document.getElementById('bloom'),woman=document.getElementById('woman'),
  flash=document.getElementById('flash'),titlewrap=document.getElementById('titlewrap'),sunpath=document.getElementById('sunpath'),halo=document.getElementById('halo');

// BGM window = source 205s..236s. Chorus enters ~video 11s, summit ~video 21s, outro tail ~28s.
const CL_IN=8500, CL_PK=20500, CL_OUT=28800;   // climax light-bloom envelope
const scenes=[
 {s:2600, e:6600,  html:'<div class="sc"><div class="lyr">夜明けの港に<br>風が目を覚ます<span class="en">At dawn, the wind awakens in the harbor.</span></div></div>'},
 {s:6600, e:10600, html:'<div class="sc"><div class="lyr">私は今<br><span class="hl">白い帆を上げる</span><span class="en">And now — I raise my white sail.</span></div></div>'},
 {s:10600,e:14600, html:'<div class="sc"><div class="lyr">怖くはない<br>空がこんなに広いから<span class="en">I’m not afraid — the sky is this wide.</span></div></div>'},
 {s:14600,e:19000, html:'<div class="sc"><div class="lyr"><span class="hl">歌え 白い帆よ</span><br>光の海を<span class="en">Sing, white sail — across this sea of light.</span></div></div>'},
 {s:19000,e:23400, html:'<div class="sc"><div class="lyr">失くしたものも<br>抱きしめたまま<span class="en">Holding even what I’ve lost, close to me.</span></div></div>'},
 {s:23400,e:27000, html:'<div class="sc"><div class="lyr">私は行く<br><span class="hl">光になって</span><span class="en">I sail on — becoming the light.</span></div></div>'},
 {s:27000,e:30000, html:'<div class="sc"><span class="badge">NEW SONG</span><div class="cta-t">白い帆</div><div class="cta-a">Seira Lumen</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>'},
];
const scEls=[];const marks=[];const scenesEl=document.getElementById('scenes');
scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
  scenesEl.appendChild(el);scEls.push(el);marks.push({start:sc.s,end:sc.e});});
const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  // climax light envelope (0..1): rise from CL_IN to CL_PK, gently ease after CL_OUT
  const climax=smooth(t,CL_IN,CL_PK)*(1-0.5*smooth(t,CL_OUT,30000));
  // slow cinematic boat sway
  const sway=Math.sin(ts*0.5)*0.7+Math.sin(ts*0.23+1)*0.4;
  world.style.transform='rotate('+sway.toFixed(3)+'deg) scale('+(1.02+0.02*climax)+')';
  // sun breathe + grow + rise slightly at climax
  const sPulse=1+0.03*Math.sin(ts*0.8)+0.1*climax;
  sun.style.transform='translate(-50%,-50%) scale('+sPulse.toFixed(3)+')';
  sunglow.style.opacity=(0.8+0.2*Math.sin(ts*0.6)+0.25*climax).toFixed(3);
  sunglow.style.transform='translate(-50%,-50%) scale('+(1+0.12*climax)+')';
  rays.style.opacity=(0.32+0.1*Math.sin(ts*0.4)+0.4*climax).toFixed(3);
  rays.style.transform='translate(-50%,-50%) rotate('+(ts*1.6).toFixed(2)+'deg)';
  sunpath.style.opacity=(0.7+0.3*Math.sin(ts*1.1)+0.2*climax).toFixed(3);
  // clouds drift right, slow
  for(const c of clouds){let x=((c.x+ts*c.sp)%1300)-150;c.el.style.transform='translateX('+x.toFixed(1)+'px)';}
  // swells shimmer
  for(const s of swells){s.el.style.transform='translateX('+(Math.sin(ts*s.sp+s.ph)*14).toFixed(1)+'px) scaleY('+(1+0.5*Math.sin(ts*s.sp+s.ph))+')';
    s.el.style.opacity=(0.05+0.1*Math.abs(Math.sin(ts*0.5+s.ph))+0.08*climax).toFixed(3);}
  // sparkles twinkle (brighter at climax)
  for(const k of sparks){k.el.style.opacity=((0.1+0.6*Math.pow(Math.abs(Math.sin(ts*k.sp+k.ph)),3))*(0.6+0.6*climax)).toFixed(3);}
  // gulls glide across + gentle wing flap
  for(const g of gulls){let x=g.x-((ts*g.sp)% (1400))*1;let gy=g.y+Math.sin(ts*0.6+g.ph)*18;
    if(x<-80)x+=1400;g.el.style.transform='translate('+(x-g.x).toFixed(1)+'px,'+(gy-g.y).toFixed(1)+'px) scale('+g.sc+')';
    const fl=Math.sin(ts*2.4+g.ph)*10;g.a.style.transform='rotate('+(18+fl)+'deg)';g.b.style.transform='rotate('+(-18-fl)+'deg)';}
  // sail billow (slow ripple via skew + shading), stronger with wind at climax
  const bil=Math.sin(ts*0.7)*1.2+Math.sin(ts*1.3+1)*0.6;
  sail.style.transform='skewY('+(bil*0.5).toFixed(3)+'deg) scaleX('+(1+0.015*Math.sin(ts*0.9))+')';
  sail2.style.transform='skewY('+(-bil*0.5).toFixed(3)+'deg)';
  sailshade.style.opacity=(0.3+0.3*Math.sin(ts*0.9)).toFixed(3);
  mast.style.transform='rotate('+(bil*0.12).toFixed(3)+'deg)';
  // hair & dress flow in the wind (slow), billowing more at climax
  const wind=Math.sin(ts*0.9)*1+Math.sin(ts*1.7+0.6)*0.5;
  hair.style.transform='rotate('+(2+wind*1.6).toFixed(2)+'deg) scaleX('+(1+0.05*Math.sin(ts*1.1))+')';
  dress.style.transform='rotate('+(wind*0.9).toFixed(2)+'deg)';
  head.style.transform='rotate('+(wind*0.5).toFixed(2)+'deg)';
  arm.style.transform='rotate('+(16+wind*0.4).toFixed(2)+'deg)';
  woman.style.transform='rotate('+(-sway*0.4).toFixed(3)+'deg)';
  // warm rim light + backlight halo on the figure grow with the light
  rim.style.opacity=(0.3+0.6*climax).toFixed(3);
  halo.style.opacity=(0.2+0.7*climax).toFixed(3);
  halo.style.transform='scale('+(1+0.08*Math.sin(ts*0.7)+0.1*climax)+')';
  // climax bloom wash
  bloom.style.opacity=(0.5*climax).toFixed(3);
  // motes rise, brighter at climax
  for(const m of motes){let y=1960-((ts*m.sp+m.base)%2100);let x=m.x+Math.sin(ts*0.5+m.ph)*m.amp;
    const op=(y>1760?smooth(y,1960,1740):(y<140?smooth(y,-60,140):1));
    m.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';
    m.el.style.opacity=(op*(0.3+0.6*climax)).toFixed(3);}
  // title in/out (upper-right, like the jacket)
  const tvis=Math.max(0,Math.min(smooth(t,350,1300),1-smooth(t,2150,2600)));
  titlewrap.style.opacity=tvis.toFixed(3);
  titlewrap.style.transform='translateY('+((1-tvis)*-10).toFixed(1)+'px)';
  // scenes fade (cross-free, gentle rise)
  const FADE=360;
  for(let i=0;i<scEls.length;i++){const m=marks[i];const o=smooth(t,m.start,m.start+FADE)*(1-smooth(t,m.end-FADE,m.end));
    scEls[i].style.opacity=o.toFixed(3);scEls[i].style.transform='translateY('+((1-o)*18).toFixed(1)+'px)';}
  // a soft swell of light right at the key-change summit
  flash.style.opacity=(0.14*smooth(t,CL_PK-900,CL_PK)*(1-smooth(t,CL_PK,CL_PK+1400))).toFixed(3);
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
<title>白い帆 / Seira Lumen</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
