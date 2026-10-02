# -*- coding: utf-8 -*-
"""
十月桜 / 琥珀譲二 — 縦型9:16 宣伝ショート
ジャケット準拠：雪化粧した十月桜（うす紅）／ピンクの夕焼け空と沈む夕陽／街と橋・川／レトロなガス灯の並ぶ雪道／舞う花びら。
歌詞の核：季節外れと笑われても、泣きながらでも咲く。冬を越えて春にもう一度。
BGM: jugatsu-zakura-bgm.mp3 (source 3:19/199s のブリッジ→最終サビ belt)。歌い出しに同期。
日米向け＝日本語歌詞＋要所に英訳。画面テキストはジャケット表記＋提供歌詞のみ（創作なし）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","jugatsu-zakura.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#13132b;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#13132b}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Noto Sans JP",system-ui,sans-serif;background:#13132b}
#world{position:absolute;inset:0;transform-origin:50% 44%}
/* sunset sky */
#sky{position:absolute;inset:0;background:
  linear-gradient(180deg,#1b1c3e 0%,#352a56 30%,#6d3a68 52%,#b5487e 68%,#e8744f 84%,#ffb062 100%)}
#bloomwarm{position:absolute;inset:0;opacity:0;background:
  radial-gradient(60% 40% at 86% 80%, rgba(255,170,110,.5), transparent 66%),
  linear-gradient(180deg,transparent 40%, rgba(255,150,120,.14) 74%, rgba(255,170,120,.26) 100%)}
#sun{position:absolute;right:120px;bottom:470px;width:170px;height:170px;border-radius:50%;
  background:radial-gradient(circle,#fff0cf,#ffc072 52%,#ff8a4e 100%);
  box-shadow:0 0 80px 26px rgba(255,160,90,.55),0 0 180px 70px rgba(255,130,90,.3)}
.cloud{position:absolute;border-radius:50%;filter:blur(20px)}
/* city + river + bridge */
#city{position:absolute;left:0;right:0;bottom:360px;height:300px}
.bld{position:absolute;bottom:0;background:#2a2446}
.spire{position:absolute;bottom:0;width:30px;background:#271f40;clip-path:polygon(50% 0,100% 100%,0 100%)}
.clit{position:absolute;width:5px;height:6px;border-radius:1px;background:rgba(255,196,120,.95);box-shadow:0 0 7px 1px rgba(255,180,90,.7)}
#river{position:absolute;left:0;right:0;bottom:210px;height:150px;overflow:hidden;background:linear-gradient(180deg,#3a2c4e,#241a33)}
.rref{position:absolute;top:0;width:8px;height:100%;border-radius:4px;filter:blur(3px);opacity:.55}
#bridge{position:absolute;right:120px;bottom:300px;width:360px;height:40px;background:#211a36}
#bridge::before,#bridge::after{content:"";position:absolute;bottom:0;width:42%;height:30px;border:7px solid #211a36;border-bottom:none;border-radius:60px 60px 0 0}
#bridge::before{left:4%} #bridge::after{right:4%}
/* snowy path + lamps */
#path{position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(180deg,#5a5f7e 0%,#3c4060 40%,#2a2c45 100%)}
#snowground{position:absolute;left:0;right:0;bottom:0;height:200px;
  background:linear-gradient(180deg,rgba(235,240,255,.55),rgba(210,218,245,.15) 60%,transparent)}
.lamp{position:absolute;bottom:0}
.lamp .post{position:absolute;bottom:0;width:7px;background:#20212f;left:50%;transform:translateX(-50%)}
.lamp .bulb{position:absolute;left:50%;transform:translateX(-50%);width:20px;height:26px;border-radius:50% 50% 40% 40%;
  background:radial-gradient(circle at 50% 40%,#fff2c6,#ffb24d);box-shadow:0 0 22px 6px rgba(255,180,90,.75)}
/* cherry branch + blossoms */
#branch{position:absolute;left:-40px;top:-30px;width:720px;height:620px;z-index:4}
.twig{position:absolute;background:#2a1d18;border-radius:8px;transform-origin:left center;box-shadow:0 1px 0 rgba(255,255,255,.12)}
.snowcap{position:absolute;background:rgba(238,243,255,.8);border-radius:40px;filter:blur(1px)}
.blossom{position:absolute;width:52px;height:52px}
.blossom .pet{position:absolute;left:50%;top:50%;width:21px;height:28px;margin:-25px 0 0 -10px;transform-origin:50% 86%;
  background:radial-gradient(circle at 50% 30%,#fff2f7,#f7c8db 60%,#e89ab8 100%);border-radius:50% 50% 50% 50%/60% 60% 40% 40%;
  box-shadow:0 0 6px rgba(247,200,219,.5)}
.blossom .bc{position:absolute;left:50%;top:50%;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;
  background:radial-gradient(circle,#ffe6a0,#e8a24a);box-shadow:0 0 6px rgba(255,210,120,.6)}
/* petals + snow */
.petal{position:absolute;width:20px;height:16px;background:radial-gradient(circle at 60% 35%,#ffeef4,#f3b9d0);
  border-radius:75% 25% 75% 25%/70% 30% 70% 30%;opacity:.9;box-shadow:0 0 5px rgba(247,185,208,.4)}
.snow{position:absolute;border-radius:50%;background:rgba(240,245,255,.9)}
/* text */
#brand{position:absolute;left:0;right:0;top:140px;text-align:center;z-index:7;opacity:0}
#brand .bt{display:block;font-family:"Noto Serif JP",serif;font-size:66px;font-weight:600;letter-spacing:10px;
  background:linear-gradient(92deg,#ffe3ee,#f7b9d2 55%,#f59ac0);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 2px 14px rgba(0,0,0,.5))}
#brand .ba{display:block;font-family:"Noto Serif JP",serif;font-size:30px;letter-spacing:8px;color:#f0cfe0;margin-top:8px}
#scenes{position:absolute;left:70px;right:70px;top:360px;height:560px;z-index:8}
.sc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;will-change:opacity,transform}
.title-jp{font-family:"Noto Serif JP",serif;font-size:140px;font-weight:600;letter-spacing:12px;line-height:1.05;
  background:linear-gradient(92deg,#ffe3ee,#f7b9d2 50%,#f59ac0);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 4px 20px rgba(0,0,0,.5)) drop-shadow(0 0 30px rgba(247,160,200,.35))}
.tfl{width:300px;height:2px;margin:18px auto 14px;background:linear-gradient(90deg,transparent,rgba(247,190,214,.9),transparent)}
.artist{font-family:"Noto Serif JP",serif;font-size:46px;letter-spacing:10px;color:#f1d3e2}
.artist small{display:block;font-style:italic;font-size:24px;letter-spacing:6px;color:#d7aec6;margin-top:6px}
.lyr{font-family:"Noto Serif JP",serif;font-size:60px;font-weight:600;line-height:1.4;letter-spacing:1px;color:#fdf3f8;
  text-shadow:0 3px 22px rgba(0,0,0,.7),0 0 22px rgba(230,120,150,.3)}
.lyr .hl{color:#ffd0e2}
.lyr .en{display:block;font-family:"Noto Sans JP";font-size:34px;font-weight:600;color:#f3c7da;letter-spacing:1px;margin-top:14px;text-shadow:0 2px 12px rgba(0,0,0,.7)}
.badge{display:inline-block;font-family:"Noto Sans JP";font-size:28px;font-weight:800;letter-spacing:6px;color:#3a1226;
  background:linear-gradient(90deg,#ffe3ee,#f7a9c8);padding:9px 26px;border-radius:40px;margin-bottom:22px}
.cta-t{font-family:"Noto Serif JP",serif;font-size:110px;font-weight:600;letter-spacing:10px;
  background:linear-gradient(92deg,#ffe3ee,#f59ac0);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 3px 16px rgba(0,0,0,.5))}
.cta-a{font-family:"Noto Serif JP",serif;font-size:44px;letter-spacing:8px;color:#f1d3e2;margin-top:12px}
.cta-s{font-size:32px;color:#e7c6d8;letter-spacing:2px;margin-top:20px}
#vig{position:absolute;inset:0;pointer-events:none;z-index:9;background:radial-gradient(120% 82% at 48% 46%,transparent 54%,rgba(0,0,0,.52) 100%)}
#grain{position:absolute;inset:0;pointer-events:none;opacity:.05;z-index:9;mix-blend-mode:overlay;background-image:repeating-linear-gradient(0deg,rgba(255,255,255,.5) 0 1px,transparent 1px 3px)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:20}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#3a1226;font-size:60px;background:linear-gradient(135deg,#ffe3ee,#f7a9c8);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.12);z-index:20}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffe3ee,#f59ac0)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="sky"></div>
  <div id="clouds"></div>
  <div id="sun"></div>
  <div id="bloomwarm"></div>
  <div id="city"></div>
  <div id="river"></div>
  <div id="bridge"></div>
  <div id="path"></div><div id="snowground"></div>
  <div id="lamps"></div>
  <div id="branch"></div>
  <div id="petals"></div>
  <div id="snowf"></div>
 </div>
 <div id="brand"><span class="bt">十月桜</span><span class="ba">琥珀 譲二</span></div>
 <div id="scenes"></div>
 <div id="grain"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="jugatsu-zakura-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=10102026;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}

// clouds (warm dusk)
const cl=document.getElementById('clouds');const clouds=[];
const ccol=['rgba(180,72,126,.5)','rgba(232,116,79,.45)','rgba(60,46,86,.6)'];
for(let i=0;i<6;i++){const c=document.createElement('div');c.className='cloud';
  const w=280+rnd()*360,h=70+rnd()*70;c.style.width=w+'px';c.style.height=h+'px';
  c.style.left=(rnd()*900-80)+'px';c.style.top=(260+rnd()*420)+'px';
  c.style.background='radial-gradient(circle,'+ccol[(rnd()*3)|0]+',transparent 70%)';cl.appendChild(c);clouds.push({el:c,ph:rnd()*6.28});}

// city
const city=document.getElementById('city');const clits=[];
let x=-20;while(x<1120){const w=46+rnd()*80,h=70+rnd()*180;const b=document.createElement('div');b.className='bld';
  b.style.left=x+'px';b.style.width=w+'px';b.style.height=h+'px';city.appendChild(b);
  const cols=Math.max(1,Math.floor(w/20)),rows=Math.floor(h/28);
  for(let c=0;c<cols;c++)for(let r=0;r<rows;r++){if(rnd()<0.62)continue;const d=document.createElement('div');d.className='clit';
    d.style.left=(x+5+c*18)+'px';d.style.bottom=(8+r*26)+'px';city.appendChild(d);clits.push({el:d,ph:rnd()*6.28,sp:0.4+rnd()*1.6});}
  x+=w+rnd()*8;}
[200,470,760].forEach(sx=>{const s=document.createElement('div');s.className='spire';s.style.left=sx+'px';s.style.height=(200+rnd()*60)+'px';city.appendChild(s);});

// river reflections (sun + lights)
const river=document.getElementById('river');const rrefs=[];
for(let i=0;i<16;i++){const r=document.createElement('div');r.className='rref';r.style.left=(rnd()*1040)+'px';
  const warm=rnd()<0.6;r.style.background='linear-gradient(180deg,'+(warm?'rgba(255,170,100,.8)':'rgba(247,180,210,.7)')+',transparent)';
  river.appendChild(r);rrefs.push({el:r,ph:rnd()*6.28});}

// lamps receding bottom-left
const lamps=document.getElementById('lamps');
const lampData=[[70,250,1.0],[250,210,0.8],[400,185,0.62],[520,168,0.5],[615,156,0.4]];
for(const [lx,h,sc] of lampData){const L=document.createElement('div');L.className='lamp';L.style.left=lx+'px';L.style.width=(40*sc)+'px';L.style.height=h+'px';
  const post=document.createElement('div');post.className='post';post.style.height=h+'px';post.style.width=(7*sc)+'px';L.appendChild(post);
  const bulb=document.createElement('div');bulb.className='bulb';bulb.style.top='0';bulb.style.width=(20*sc)+'px';bulb.style.height=(26*sc)+'px';L.appendChild(bulb);
  lamps.appendChild(L);}

// cherry branch (twigs + snowcaps + blossoms)
const branch=document.getElementById('branch');
function twig(x,y,w,len,rot){const t=document.createElement('div');t.className='twig';t.style.left=x+'px';t.style.top=y+'px';
  t.style.width=len+'px';t.style.height=w+'px';t.style.transform='rotate('+rot+'deg)';branch.appendChild(t);
  const s=document.createElement('div');s.className='snowcap';s.style.left=x+'px';s.style.top=(y-2)+'px';s.style.width=len*0.7+'px';s.style.height=Math.max(3,w-2)+'px';
  s.style.transform='rotate('+rot+'deg)';s.style.transformOrigin='left center';branch.appendChild(s);}
twig(0,60,16,420,20);twig(150,112,10,200,-16);twig(300,165,8,170,8);twig(60,95,9,150,46);twig(360,150,7,130,-34);
const blossoms=[];
const bpos=[[120,150],[220,120],[300,180],[180,210],[360,200],[90,160],[260,90],[420,170],[150,80],[330,120]];
for(const [bx,by] of bpos){const bl=document.createElement('div');bl.className='blossom';bl.style.left=bx+'px';bl.style.top=by+'px';
  const scb=0.7+rnd()*0.8;bl.style.transform='scale('+scb+')';
  for(let i=0;i<5;i++){const p=document.createElement('div');p.className='pet';p.style.transform='rotate('+(i*72)+'deg)';bl.appendChild(p);}
  const c=document.createElement('div');c.className='bc';bl.appendChild(c);branch.appendChild(bl);blossoms.push({el:bl,ph:rnd()*6.28,sc:scb});}

// falling petals + snow
const petalsEl=document.getElementById('petals');const petals=[];
for(let i=0;i<16;i++){const p=document.createElement('div');p.className='petal';petalsEl.appendChild(p);
  petals.push({el:p,x:rnd()*1080,y:rnd()*1500,sp:28+rnd()*44,drift:24+rnd()*44,ph:rnd()*6.28,rot:rnd()*360,rs:(rnd()-0.5)*90,sc:0.7+rnd()*0.8});}
const snowEl=document.getElementById('snowf');const snows=[];
for(let i=0;i<50;i++){const s=document.createElement('div');s.className='snow';const sz=2+rnd()*4;s.style.width=sz+'px';s.style.height=sz+'px';snowEl.appendChild(s);
  snows.push({el:s,x:rnd()*1080,y:rnd()*1600,sp:16+rnd()*26,drift:10+rnd()*24,ph:rnd()*6.28});}

const sun=document.getElementById('sun'),bloomwarm=document.getElementById('bloomwarm');
const brandEl=document.getElementById('brand');

// scenes (BGM 3:19 start; bridge build -> final chorus belt ~ t=11s). sync to vocal swells.
const scenes=[
 {s:300,  e:2800,  html:'<div class="sc"><div class="title-jp">十月桜</div><div class="tfl"></div><div class="artist">琥珀 譲二<small>KOHAKU JOJI</small></div></div>'},
 {s:2800, e:6600,  html:'<div class="sc"><div class="lyr">散るためじゃない<br>咲くために</div></div>'},
 {s:6600, e:10600, html:'<div class="sc"><div class="lyr"><span class="hl">いのちは<br>季節を選ばない</span><span class="en">Life does not choose its season.</span></div></div>'},
 {s:10600,e:15200, html:'<div class="sc"><div class="lyr"><span class="hl">十月桜 わたしは咲く</span><span class="en">October cherry — I will bloom.</span></div></div>'},
 {s:15200,e:19400, html:'<div class="sc"><div class="lyr">冬を越えて<br>春にもう一度</div></div>'},
 {s:19400,e:23600, html:'<div class="sc"><div class="lyr">あの日 咲けなかった<br>春に</div></div>'},
 {s:23600,e:28200, html:'<div class="sc"><div class="lyr"><span class="hl">もう一度<br>咲いてみせるから</span><span class="en">I will bloom again, I promise.</span></div></div>'},
 {s:28200,e:31000, html:'<div class="sc"><span class="badge">NEW SINGLE</span><div class="cta-t">十月桜</div><div class="cta-a">琥珀譲二</div><div class="cta-s">配信中 &nbsp;/&nbsp; Streaming Now</div></div>'},
];
const scEls=[];const marks=[];const scenesEl=document.getElementById('scenes');
scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
  scenesEl.appendChild(el);scEls.push(el);marks.push({start:sc.s,end:sc.e});});
const TOTAL=31000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000,prog=t/TOTAL;
  // warmth/bloom rises into the final chorus (t>=10s)
  const warmf=smooth(t,9000,24000);
  bloomwarm.style.opacity=(0.85*warmf).toFixed(3);
  sun.style.boxShadow='0 0 '+(80+40*warmf)+'px '+(26+16*warmf)+'px rgba(255,160,90,'+(0.55+0.2*warmf)+'),0 0 '+(180+80*warmf)+'px 70px rgba(255,130,90,'+(0.3+0.15*warmf)+')';
  // clouds drift
  for(const c of clouds)c.el.style.transform='translateX('+(Math.sin(ts*0.12+c.ph)*18).toFixed(1)+'px)';
  // city twinkle
  for(const c of clits)c.el.style.opacity=(0.5+0.5*Math.sin(ts*c.sp+c.ph)).toFixed(3);
  // river shimmer
  for(const r of rrefs){r.el.style.transform='translateX('+(Math.sin(ts*0.8+r.ph)*4).toFixed(1)+'px) scaleY('+(1+0.12*Math.sin(ts*1.3+r.ph)).toFixed(3)+')';r.el.style.opacity=(0.35+0.2*Math.sin(ts*1.1+r.ph)).toFixed(3);}
  // blossoms gentle breathe
  for(const b of blossoms)b.el.style.transform='scale('+(b.sc*(1+0.03*Math.sin(ts*1.1+b.ph))).toFixed(3)+') rotate('+(Math.sin(ts*0.5+b.ph)*3).toFixed(1)+'deg)';
  // petals fall (swirl up a touch during chorus)
  for(const p of petals){let y=(p.y+ts*p.sp*(1+0.3*warmf))%1560;const xx=p.x+Math.sin(ts*0.7+p.ph)*p.drift+prog*40;
    p.el.style.transform='translate('+xx.toFixed(1)+'px,'+y.toFixed(1)+'px) rotate('+(p.rot+ts*p.rs*0.4).toFixed(0)+'deg) scale('+p.sc+')';
    p.el.style.opacity=(0.55+0.4*Math.sin(ts*1.1+p.ph)).toFixed(3);}
  // snow
  for(const s of snows){let y=(s.y+ts*s.sp)%1620;const xx=s.x+Math.sin(ts*0.5+s.ph)*s.drift;
    s.el.style.transform='translate('+xx.toFixed(1)+'px,'+y.toFixed(1)+'px)';s.el.style.opacity=(0.4+0.4*Math.sin(ts*0.9+s.ph)).toFixed(3);}
  // world push-in
  document.getElementById('world').style.transform='scale('+(1+0.04*prog).toFixed(4)+') translateY('+(-6*prog).toFixed(1)+'px)';
  // brand
  brandEl.style.opacity=Math.max(0,Math.min(smooth(t,2800,3500),1-smooth(t,27400,28200))).toFixed(3);
  // scenes
  const FADE=300;
  for(let i=0;i<scEls.length;i++){const m=marks[i];let o=0,dy=14;
    if(t>=m.start-FADE&&t<=m.end+FADE){if(t<m.start)o=(t-(m.start-FADE))/FADE;else if(t>m.end)o=1-(t-m.end)/FADE;else o=1;o=Math.max(0,Math.min(1,o));dy=14*(1-o);}
    scEls[i].style.opacity=o.toFixed(3);scEls[i].style.transform='translateY('+dy.toFixed(1)+'px)';}
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;
function play(){document.getElementById('ui').style.display='none';
  try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);
    barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const st=performance.now();(function fo(){const k=(performance.now()-st)/1600;
    bgm.volume=Math.max(0,0.92*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1600);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>十月桜 / 琥珀譲二</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
