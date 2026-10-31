# -*- coding: utf-8 -*-
"""
Colors at the Door / w-Band — Lv3「フル再現アニメ」（Claudeがジャケの世界をコードで描き起こす / デモ）
ジャケット準拠：彫刻の木の門が開き、黄金の朝日の街（寺院のドーム・椰子・川）へ。足元に色粉と花びらのランゴリ（曼荼羅）、
真鍮の色粉ボウル、マリーゴールドの花綱とジャスミン、右からブーゲンビリア。朝日のゴッドレイ、舞う花びらと色粉。
ブランド枠はLv1と共通：タイトル（多色）＋w-Band＋締めCTA＋Leo Musicロゴバグ。画面テキストはタイトル＋アーティストのみ。
ビート同期はごく控えめ（88.5BPM, beat 678ms, +5ms）。BGM: colors-bgm.mp3 (source 156s〜サビ)。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","colors-scene.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#140b06;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#140b06}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;font-family:"EB Garamond","Noto Serif JP",serif;background:#1c110a}
#world{position:absolute;inset:-20px;transform-origin:50% 56%}
/* sky / sunrise seen through the doorway */
#sky{position:absolute;left:0;right:0;top:0;height:1240px;background:
  radial-gradient(40% 30% at 56% 60%, rgba(255,236,170,.95), rgba(255,190,110,.4) 32%, transparent 64%),
  linear-gradient(180deg,#8ab0cf 0%,#b9c9cf 26%,# efd9b0 46%,#ffcf92 62%,#ffb878 78%,#e89a60 100%);
  background:
  radial-gradient(40% 30% at 56% 60%, rgba(255,236,170,.95), rgba(255,190,110,.4) 32%, transparent 64%),
  linear-gradient(180deg,#8ab0cf 0%,#bcc9cc 26%,#efd9b0 46%,#ffcf92 62%,#ffb878 78%,#e89a60 100%)}
#sun{position:absolute;left:600px;top:770px;width:150px;height:150px;transform:translate(-50%,-50%);border-radius:50%;z-index:2;
  background:radial-gradient(circle,#fffbe8,#ffe6a0 46%,#ffc46a 74%,rgba(255,180,100,0));box-shadow:0 0 90px 36px rgba(255,210,140,.6)}
#rays{position:absolute;left:600px;top:770px;width:1500px;height:1500px;transform:translate(-50%,-50%);z-index:2;pointer-events:none;mix-blend-mode:screen;opacity:.4;
  background:conic-gradient(from 0deg,rgba(255,232,180,0) 0deg,rgba(255,232,180,.18) 3deg,rgba(255,232,180,0) 8deg,rgba(255,232,180,0) 24deg,rgba(255,232,180,.14) 28deg,rgba(255,232,180,0) 33deg,rgba(255,232,180,0) 50deg,rgba(255,232,180,.16) 54deg,rgba(255,232,180,0) 60deg,rgba(255,232,180,0) 78deg,rgba(255,232,180,.13) 82deg,rgba(255,232,180,0) 88deg,rgba(255,232,180,0) 104deg,rgba(255,232,180,.16) 108deg,rgba(255,232,180,0) 114deg,rgba(255,232,180,0) 360deg)}
.cityb{position:absolute;bottom:0;background:linear-gradient(180deg,#b98a63,#8a6346);opacity:.55;border-radius:4px 4px 0 0}
.dome{position:absolute;border-radius:50% 50% 0 0;background:linear-gradient(180deg,#c49068,#8a6346);opacity:.55}
.palm{position:absolute;bottom:0;width:10px;background:#6a5038;opacity:.5}
#citywrap{position:absolute;left:360px;right:140px;top:980px;height:210px;z-index:2;overflow:hidden}
#river{position:absolute;left:360px;right:140px;top:1120px;height:70px;z-index:2;background:linear-gradient(180deg,rgba(255,210,150,.5),rgba(200,160,120,.2));filter:blur(2px)}
/* carved wooden door (left, foreground, opening) */
#door{position:absolute;left:-60px;top:40px;width:500px;height:1480px;z-index:5;transform:perspective(1600px) rotateY(20deg);transform-origin:left center}
#doorface{position:absolute;inset:0;background:
  repeating-linear-gradient(90deg,rgba(0,0,0,.14) 0 2px,transparent 2px 46px),
  linear-gradient(100deg,#2a1a0e,#4a2f18 55%,#6a4525);box-shadow:inset -30px 0 60px rgba(0,0,0,.5),30px 0 50px rgba(0,0,0,.4)}
.panel{position:absolute;border-radius:8px;background:linear-gradient(135deg,rgba(0,0,0,.3),rgba(120,80,40,.2));box-shadow:inset 0 0 0 4px rgba(90,60,30,.5),inset 0 0 20px rgba(0,0,0,.4)}
.stud{position:absolute;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 36% 30%,#d8b06a,#7a5222);box-shadow:0 2px 4px rgba(0,0,0,.5)}
#dooredge{position:absolute;right:-10px;top:0;bottom:0;width:20px;z-index:5;background:linear-gradient(90deg,#1a0f08,#3a2414)}
/* right stone pillar + bougainvillea */
#pillarR{position:absolute;right:-20px;top:0;width:150px;height:1300px;z-index:5;background:linear-gradient(90deg,#8a7a63,#b7a68a 60%,#6a5c48)}
#bougf{position:absolute;right:0;top:0;width:360px;height:720px;z-index:6}
.leaf{position:absolute;border-radius:0 70% 0 70%;background:linear-gradient(120deg,#3f6a3a,#2c5230)}
/* marigold garland (left door edge) */
#garland{position:absolute;left:30px;top:70px;width:90px;height:900px;z-index:6}
.mari{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 34%,#ffd24a,#ff8a1e 70%);box-shadow:0 1px 3px rgba(0,0,0,.3)}
/* floor (perspective stone) */
#floor{position:absolute;left:-60px;right:-60px;bottom:0;height:800px;z-index:7;
  background:linear-gradient(180deg,#b79274 0%,#9c7a5c 30%,#7c5e44 70%,#5a4230 100%)}
#floor::before{content:"";position:absolute;inset:0;opacity:.3;background:repeating-linear-gradient(92deg,rgba(0,0,0,.14) 0 2px,transparent 2px 120px),repeating-linear-gradient(2deg,rgba(0,0,0,.12) 0 2px,transparent 2px 120px)}
#floorwet{position:absolute;left:0;right:0;top:0;height:300px;z-index:7;pointer-events:none;mix-blend-mode:screen;opacity:.5;background:radial-gradient(60% 100% at 54% 0,rgba(255,210,150,.6),transparent 62%)}
/* rangoli mandala */
#rangoli{position:absolute;left:50%;bottom:150px;width:760px;height:360px;transform:translateX(-50%);z-index:8;border-radius:50%;
  background:repeating-radial-gradient(circle at 50% 50%,
    #ff2e86 0 18px,#fff2df 18px 26px,#ffd23d 26px 46px,#4bc86a 46px 58px,#ff8a3d 58px 78px,#8a6bff 78px 88px,#fff2df 88px 100px);
  box-shadow:0 10px 30px rgba(0,0,0,.35);opacity:.95}
#rangoli::after{content:"";position:absolute;inset:0;border-radius:50%;opacity:.6;
  background:repeating-radial-gradient(circle at 50% 50%,rgba(255,255,255,.7) 0 3px,transparent 3px 22px)}
#rangoli2{position:absolute;left:50%;bottom:196px;width:420px;height:200px;transform:translateX(-50%);z-index:8;border-radius:50%;opacity:.92;
  background:conic-gradient(from 0deg,#ff2e86 0 10%,transparent 10% 12.5%,#ffd23d 12.5% 22.5%,transparent 22.5% 25%,#4bc86a 25% 35%,transparent 35% 37.5%,#ff8a3d 37.5% 47.5%,transparent 47.5% 50%,#8a6bff 50% 60%,transparent 60% 62.5%,#ff2e86 62.5% 72.5%,transparent 72.5% 75%,#ffd23d 75% 85%,transparent 85% 87.5%,#4bc86a 87.5% 97.5%,transparent 97.5% 100%);
  -webkit-mask:radial-gradient(circle at 50% 50%,transparent 0 40px,#000 48px 96px,transparent 104px)}
#rangcore{position:absolute;left:50%;bottom:226px;width:140px;height:76px;transform:translateX(-50%);z-index:8;border-radius:50%;
  background:radial-gradient(circle,#fff6d0,#ffd23d 46%,#ff8a3d 78%);box-shadow:0 0 20px rgba(255,200,110,.6);opacity:.96}
/* brass bowls of powder (bottom-left) */
.bowl{position:absolute;z-index:9;border-radius:46% 46% 50% 50%/30% 30% 70% 70%;background:linear-gradient(180deg,#e7b86a,#8a5f28);box-shadow:0 8px 16px rgba(0,0,0,.4)}
.powderheap{position:absolute;z-index:9;border-radius:50% 50% 40% 40%}
/* scattered petals on floor */
.fpetal{position:absolute;z-index:8;border-radius:50% 50% 50% 50%/70% 70% 40% 40%}
/* particles */
#petals{position:absolute;inset:0;z-index:11;pointer-events:none}
#powder{position:absolute;inset:0;z-index:11;pointer-events:none}
.powd{position:absolute;border-radius:50%;filter:blur(1px)}
#dust{position:absolute;inset:0;z-index:11;pointer-events:none}
.dust{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,228,180,.9),transparent 70%)}
#bloom{position:absolute;inset:0;z-index:11;pointer-events:none;mix-blend-mode:screen;opacity:0;background:radial-gradient(44% 30% at 56% 42%,rgba(255,220,150,.6),transparent 70%)}
#vig{position:absolute;inset:0;z-index:13;pointer-events:none;background:radial-gradient(130% 80% at 50% 46%,transparent 54%,rgba(12,6,2,.6) 100%)}
#grain{position:absolute;inset:0;z-index:13;pointer-events:none;opacity:.045;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
/* text (brand frame, same as Lv1) */
#titlewrap{position:absolute;left:24px;right:24px;top:150px;text-align:center;z-index:16;opacity:0}
.tt{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:700;font-style:italic;font-size:118px;line-height:1.0;letter-spacing:1px;
  background:linear-gradient(92deg,#ff4d94,#ff8a3d 30%,#ffd23d 52%,#4bc86a 70%,#6fb7ff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 3px 10px rgba(10,6,2,.6)) drop-shadow(0 0 26px rgba(255,200,120,.4))}
.tart{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:500;font-size:52px;letter-spacing:12px;color:#f3ead6;text-shadow:0 2px 14px rgba(12,6,2,.7);margin-top:4px}
.tund{width:66%;height:3px;margin:12px auto 10px;background:linear-gradient(90deg,transparent,rgba(255,210,120,.9),transparent)}
#cta{position:absolute;left:30px;right:30px;top:560px;text-align:center;z-index:16;opacity:0}
.badge{display:inline-block;font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:7px;color:#3a1f08;background:linear-gradient(90deg,#ffd98a,#ff9a3c);padding:9px 28px;border-radius:30px;margin-bottom:22px;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.cta-a{font-family:"EB Garamond",serif;font-weight:500;font-size:50px;letter-spacing:12px;color:#f3ead6;margin-top:14px}
.cta-s{font-family:"EB Garamond","Noto Serif JP",serif;font-weight:600;font-size:40px;letter-spacing:3px;color:#ffd98a;margin-top:22px}
.cta-b{font-family:"EB Garamond",serif;font-weight:600;font-size:32px;letter-spacing:10px;color:#f3ead6;margin-top:12px;opacity:.92}
#logobug{position:absolute;left:40px;bottom:46px;width:124px;height:124px;border-radius:50%;overflow:hidden;z-index:14;box-shadow:0 0 0 3px rgba(255,220,150,.5),0 6px 16px rgba(0,0,0,.5);opacity:.92}
#logobug img{position:absolute;left:-14%;top:-10%;width:128%;height:128%;object-fit:cover}
#logotag{position:absolute;left:176px;bottom:70px;z-index:14;font-family:"EB Garamond",serif;font-weight:600;font-size:34px;letter-spacing:5px;color:#f7ecd6;opacity:.86;text-shadow:0 2px 8px rgba(0,0,0,.7)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#3a1f08;font-size:60px;background:linear-gradient(135deg,#ffd98a,#ff9a3c);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffd98a,#ff9a3c)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="sky"></div><div id="rays"></div><div id="sun"></div>
  <div id="citywrap"></div><div id="river"></div>
  <div id="floor"></div><div id="floorwet"></div>
  <div id="petalfloor"></div>
  <div id="rangoli"></div><div id="rangoli2"></div><div id="rangcore"></div>
  <div id="bowlf"></div>
  <div id="pillarR"></div><div id="bougf"></div>
  <div id="door"><div id="doorface"></div><div id="panelf"></div><div id="studf"></div></div><div id="dooredge"></div>
  <div id="garland"></div>
  <div id="bloom"></div>
  <div id="powder"></div><div id="petals"></div><div id="dust"></div>
  <div id="vig"></div><div id="grain"></div>
 </div>
 <div id="titlewrap"><div class="tt">Colors at the Door</div><div class="tund"></div><div class="tart">w-Band</div></div>
 <div id="cta"><span class="badge">NEW SONG</span><div class="tt" style="font-size:98px">Colors at the Door</div><div class="cta-a">w-Band</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
 <div id="logobug"><img src="leo-music-logo.png"></div><div id="logotag">LEO MUSIC</div>
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
let _s=77123;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');if(cls)d.className=cls;if(st)d.style.cssText+=st;p.appendChild(d);return d;}

// city silhouette (domes, buildings, palms)
const cw=document.getElementById('citywrap');let cx=0;
while(cx<600){const w=30+rnd()*54,h=40+rnd()*110;if(rnd()<0.3){mk(cw,'left:'+cx+'px;width:'+w+'px;height:'+(h*0.7)+'px','dome');mk(cw,'left:'+(cx+w*0.3)+'px;width:4px;height:'+(h+20)+'px;bottom:0;background:#8a6346;position:absolute;opacity:.5','');}else{mk(cw,'left:'+cx+'px;width:'+w+'px;height:'+h+'px','cityb');}cx+=w+6+rnd()*10;}
for(let i=0;i<5;i++){mk(cw,'left:'+(rnd()*580)+'px;height:'+(120+rnd()*70)+'px','palm');}
// door panels + studs
const pf=document.getElementById('panelf');const sf=document.getElementById('studf');
for(let r=0;r<4;r++){mk(pf,'left:60px;right:70px;top:'+(120+r*340)+'px;height:280px','panel');
  [[70,150],[70,120+300],[380,150],[380,120+300]].forEach(([x,y])=>{});}
for(let r=0;r<5;r++)for(let c=0;c<2;c++){mk(sf,'left:'+(70+c*300)+'px;top:'+(150+r*290)+'px','stud');}
// bougainvillea (right) leaves + magenta flowers
const bg=document.getElementById('bougf');
for(let i=0;i<26;i++){const w=22+rnd()*34;mk(bg,'position:absolute;right:'+(rnd()*300)+'px;top:'+(rnd()*680)+'px;width:'+w+'px;height:'+(w*0.6)+'px;transform:rotate('+(rnd()*360)+'deg);opacity:.9','leaf');}
for(let i=0;i<30;i++){const w=16+rnd()*18;mk(bg,'position:absolute;right:'+(rnd()*300)+'px;top:'+(rnd()*680)+'px;width:'+w+'px;height:'+w+'px;border-radius:50% 50% 50% 0;background:radial-gradient(circle at 50% 50%,#ffd24a 0 18%,#ff2e86 20%);transform:rotate('+(rnd()*360)+'deg)','');}
// marigold garland
const gl=document.getElementById('garland');
for(let i=0;i<24;i++){const w=30+rnd()*14;mk(gl,'left:'+(10+Math.sin(i*0.6)*18+rnd()*10)+'px;top:'+(i*38)+'px;width:'+w+'px;height:'+w+'px','mari');}
// scattered petals on floor
const pfl=document.getElementById('petalfloor');const FC=['#ff8a1e','#ffd24a','#ff3b5a','#ffffff','#ff2e86'];
for(let i=0;i<40;i++){const w=16+rnd()*22;const c=FC[(rnd()*FC.length)|0];mk(pfl,'position:absolute;left:'+(rnd()*1080)+'px;top:'+(1300+rnd()*560)+'px;width:'+w+'px;height:'+(w*0.7)+'px;background:'+c+';transform:rotate('+(rnd()*360)+'deg);opacity:.95','fpetal');}
// brass bowls of powder (bottom-left)
const bf=document.getElementById('bowlf');
const BW=[[20,1560,150,110,'#ff2e86'],[150,1640,140,100,'#ffd23d'],[40,1700,140,100,'#4bc86a']];
BW.forEach(([x,y,w,h,col])=>{mk(bf,'left:'+x+'px;top:'+y+'px;width:'+w+'px;height:'+h+'px','bowl');mk(bf,'left:'+(x+10)+'px;top:'+(y-14)+'px;width:'+(w-20)+'px;height:'+(h*0.6)+'px;background:radial-gradient(circle at 50% 30%,'+col+',rgba(0,0,0,.2));box-shadow:0 -4px 10px '+col,'powderheap');});
// particles
const pp=document.getElementById('petals');const petals=[];const PC=['#ff9a2e','#ffb64a','#ffd36a','#fff3df','#ff7a5a'];
for(let i=0;i<22;i++){const w=16+rnd()*24;const c=PC[(rnd()*PC.length)|0];const e=mk(pp,'position:absolute;width:'+w+'px;height:'+(w*0.72)+'px;border-radius:50% 50% 50% 50%/70% 70% 40% 40%;background:radial-gradient(circle at 50% 70%,'+c+','+c+'cc)','');petals.push({el:e,x:rnd()*1080,fall:40+rnd()*60,sway:40+rnd()*80,ph:rnd()*6.28,rot:(rnd()-0.5)*3,base:rnd()*1920,sp:0.4+rnd()*0.5});}
const pw=document.getElementById('powder');const powders=[];const HC=['rgba(255,70,150,.9)','rgba(255,210,70,.9)','rgba(90,210,120,.85)','rgba(255,130,60,.9)','rgba(170,110,255,.8)','rgba(255,255,255,.85)'];
for(let i=0;i<40;i++){const w=6+rnd()*18;const e=mk(pw,'width:'+w+'px;height:'+w+'px;background:radial-gradient(circle,'+HC[(rnd()*HC.length)|0]+',transparent 72%)','powd');powders.push({el:e,x:rnd()*1080,y:600+rnd()*1320,rise:5+rnd()*16,amp:16+rnd()*44,ph:rnd()*6.28,blinkR:1+rnd()*2,blinkP:rnd()*6.28,base:rnd()*1340});}
const df=document.getElementById('dust');const dusts=[];
for(let i=0;i<22;i++){const w=3+rnd()*8;const e=mk(df,'width:'+w+'px;height:'+w+'px','dust');dusts.push({el:e,x:rnd()*1080,sp:7+rnd()*16,amp:14+rnd()*40,ph:rnd()*6.28,base:rnd()*1920});}

const world=document.getElementById('world'),sun=document.getElementById('sun'),rays=document.getElementById('rays'),bloom=document.getElementById('bloom'),
  rangoli=document.getElementById('rangoli'),rangoli2=document.getElementById('rangoli2'),titlewrap=document.getElementById('titlewrap'),cta=document.getElementById('cta'),
  logobug=document.getElementById('logobug'),logotag=document.getElementById('logotag');

const BEAT=678.0, OFF=5;
const CL_IN=4000, CL_PK=19000, CL_OUT=27000;
const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const bp=(((t-OFF)%BEAT)+BEAT)%BEAT/BEAT;const swell=0.5+0.5*Math.cos(bp*6.2832);
  const climax=smooth(t,CL_IN,CL_PK)*(1-0.5*smooth(t,CL_OUT,30000));
  world.style.transform='scale('+(1.01+0.01*climax)+') translateY('+(Math.sin(ts*0.3)*2).toFixed(2)+'px)';
  sun.style.transform='translate(-50%,-50%) scale('+(1+0.03*Math.sin(ts*0.6)+0.06*climax)+')';
  rays.style.transform='translate(-50%,-50%) rotate('+(ts*2.4).toFixed(2)+'deg) scale('+(1+0.06*climax)+')';
  rays.style.opacity=(0.3+0.1*Math.sin(ts*0.5)+0.35*climax+0.05*swell).toFixed(3);
  bloom.style.opacity=(0.14+0.5*climax)*(0.85+0.15*swell);
  // rangoli: static mandala, gentle brightness pulse; petal ring turns very slowly
  rangoli2.style.transform='translateX(-50%) rotate('+(ts*4).toFixed(2)+'deg)';
  rangoli.style.filter='brightness('+(1+0.12*swell+0.16*climax)+') saturate(1.12)';
  rangoli.style.opacity=(0.9+0.08*swell).toFixed(3);
  // petals fall
  for(const pt of petals){let y=((pt.base+ts*pt.fall)%2040)-100;let x=pt.x+Math.sin(ts*pt.sp+pt.ph)*pt.sway;
    pt.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) rotate('+(ts*40*pt.rot).toFixed(1)+'deg)';
    pt.el.style.opacity=(0.85*smooth(y,-100,80)*(1-smooth(y,1820,1960))).toFixed(3);}
  for(const pd of powders){let y=pd.y-((ts*pd.rise)%1340);if(y<-30)y+=1340;let x=pd.x+Math.sin(ts*0.5+pd.ph)*pd.amp;
    const blink=0.4+0.6*Math.abs(Math.sin(ts*pd.blinkR+pd.blinkP));
    pd.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(0.8+0.3*blink)+')';
    pd.el.style.opacity=(blink*(0.35+0.4*climax+0.1)).toFixed(3);}
  for(const d of dusts){let y=1960-((ts*d.sp+d.base)%2100);let x=d.x+Math.sin(ts*0.4+d.ph)*d.amp;
    d.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';d.el.style.opacity=(0.3+0.4*climax).toFixed(3);}
  logobug.style.opacity=(0.9+0.06*Math.sin(ts*1.2)).toFixed(3);logotag.style.opacity=(0.82+0.06*Math.sin(ts*1.2)).toFixed(3);
  // title open 0.3-5s, re-flash ~13s, blaze 20-26s
  const tO=Math.min(smooth(t,300,1200),1-smooth(t,4600,5300));
  const tF=Math.min(smooth(t,12600,13000),1-smooth(t,14000,14400))*0.85;
  const tB=Math.min(smooth(t,20000,20900),1-smooth(t,26000,26700));
  const tv=Math.max(tO,tF,tB);titlewrap.style.opacity=tv.toFixed(3);titlewrap.style.transform='translateY('+((1-tv)*-8).toFixed(1)+'px) scale('+(1+0.02*swell*(tB>0?1:0.3))+')';
  const cvis=smooth(t,26500,27200);cta.style.opacity=cvis.toFixed(3);cta.style.transform='scale('+(0.98+0.02*cvis)+')';
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
<title>Colors at the Door / w-Band (Scene)</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
