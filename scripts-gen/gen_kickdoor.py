# -*- coding: utf-8 -*-
"""
Kick the Door Down / Rolling All Stars — 縦型9:16 宣伝ショート（ダンス・ロック / 5歳以上の日米向け）
ジャケット準拠：蹴り開けた傷だらけのメタルドア→ライブハウス。ステージのバンド・カラフルなスポット・
ミラーボール・手を上げる観客・濡れた反射床・ポスター/グラフィティの壁。
ビート同期：130BPM 四つ打ち。キックに合わせて光がストロボ、観客がジャンプ、画面がドクンと脈打つ。
BGM: kickdoor-bgm.mp3 (source 3:58/238s の最終サビ：半音上げ→ゴスペル大合唱)。
英語フック＋要所に日本語訳。画面テキストはジャケット表記＋提供歌詞のみ（創作なし）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","kickdoor.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#07060c;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#07060c}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Noto Sans JP",system-ui,sans-serif;background:#07060c}
#world{position:absolute;inset:0;transform-origin:50% 54%}
/* club back wall (posters/graffiti) */
#wall{position:absolute;left:0;right:0;top:0;height:1300px;background:
  linear-gradient(180deg,#140f22 0%,#1b1430 44%,#241536 70%,#120b1e 100%)}
.poster{position:absolute;border-radius:2px;opacity:.22;filter:saturate(1.1)}
/* bright stage backdrop so band & crowd read as backlit silhouettes */
#stageglow{position:absolute;left:360px;right:60px;top:640px;height:470px;z-index:2;border-radius:18px;
  background:radial-gradient(72% 95% at 50% 24%, rgba(255,130,210,.62), rgba(150,90,230,.42) 46%, rgba(40,30,80,.08) 82%);
  box-shadow:0 0 90px 36px rgba(180,90,230,.3)}
#crowdglow{position:absolute;left:320px;right:30px;bottom:120px;height:560px;z-index:5;pointer-events:none;
  background:radial-gradient(72% 86% at 50% 24%, rgba(255,160,90,.62), rgba(255,90,170,.36) 48%, transparent 82%)}
#hazel{position:absolute;left:0;right:0;top:400px;height:800px;pointer-events:none;mix-blend-mode:screen;opacity:.45;
  background:radial-gradient(60% 50% at 50% 30%, rgba(255,150,220,.28), transparent 70%)}
/* spotlight beams */
.beam{position:absolute;top:-60px;transform-origin:50% 0;mix-blend-mode:screen;filter:blur(8px);
  clip-path:polygon(44% 0,56% 0,100% 100%,0 100%)}
/* mirror ball */
#ball{position:absolute;left:50%;top:230px;transform:translateX(-50%);width:120px;height:120px;border-radius:50%;z-index:3;
  background:conic-gradient(from 0deg,#cfe0ff,#8fa0c0,#eef4ff,#90a0c0,#cfe0ff,#9aa8c8,#eef4ff,#8fa0c0,#cfe0ff);
  box-shadow:0 0 40px 10px rgba(200,220,255,.5)}
#ball::after{content:"";position:absolute;inset:0;border-radius:50%;background:
  repeating-conic-gradient(from 0deg,rgba(0,0,0,.25) 0 8deg,transparent 8deg 16deg),
  repeating-radial-gradient(circle,rgba(0,0,0,.2) 0 8px,transparent 8px 16px)}
#balltop{position:absolute;left:50%;top:150px;transform:translateX(-50%);width:4px;height:84px;background:#2a2438;z-index:3}
.bdot{position:absolute;width:8px;height:8px;background:radial-gradient(circle,rgba(220,235,255,.95),transparent 70%);border-radius:50%;z-index:3;filter:blur(.5px)}
/* stage + band */
#stagep{position:absolute;left:380px;right:70px;top:930px;height:130px;z-index:4;background:linear-gradient(180deg,#1a1326,#0c0814);border-top:2px solid rgba(255,120,200,.35)}
.musician{position:absolute;bottom:0;background:#060409;z-index:4}
.rimc{position:absolute;bottom:0;z-index:4;mix-blend-mode:screen}
.mic{position:absolute;bottom:0;width:5px;background:#0a0710;z-index:4}
.mic::after{content:"";position:absolute;left:-7px;top:-14px;width:18px;height:18px;border-radius:50%;background:#0a0710}
/* crowd */
#crowd{position:absolute;left:0;right:0;bottom:120px;height:620px;z-index:6}
.person{position:absolute;bottom:0;width:100px;height:470px}
.phead{position:absolute;left:50%;transform:translateX(-50%);border-radius:50% 50% 46% 46%;background:#050409;box-shadow:-4px -3px 0 0 rgba(255,150,90,.4)}
.pbody{position:absolute;left:50%;transform:translateX(-50%);border-radius:52px 52px 0 0;background:#050409}
.parm{position:absolute;width:17px;background:#050409;border-radius:10px;transform-origin:bottom center}
/* door (foreground, kicked open on the left) */
#door{position:absolute;left:-40px;top:-40px;width:560px;height:2000px;z-index:8;transform-origin:left center;
  transform:perspective(1400px) rotateY(34deg);transform-style:preserve-3d}
#doorface{position:absolute;inset:0;background:linear-gradient(100deg,#3a3330 0%,#555049 40%,#6a655c 70%,#4a4640 100%);
  box-shadow:inset -30px 0 60px rgba(0,0,0,.5),20px 0 50px rgba(0,0,0,.6)}
#doorface::after{content:"";position:absolute;inset:0;mix-blend-mode:overlay;opacity:.5;
  background:repeating-linear-gradient(88deg,rgba(0,0,0,.2) 0 3px,transparent 3px 60px),radial-gradient(circle at 30% 40%,rgba(255,255,255,.1),transparent 40%)}
.sticker{position:absolute;border-radius:3px;transform:rotate(-6deg);box-shadow:0 2px 6px rgba(0,0,0,.4)}
#handle{position:absolute;right:46px;top:46%;width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#d9d2c4,#6a645a);box-shadow:0 0 14px rgba(0,0,0,.5)}
#frameR{position:absolute;right:0;top:0;bottom:0;width:70px;z-index:8;background:linear-gradient(90deg,transparent,#15110f 60%,#0a0807)}
/* floor */
#floor{position:absolute;left:0;right:0;bottom:0;height:380px;z-index:5;background:linear-gradient(180deg,#12101c 0%,#0a0812 60%,#07060c 100%)}
.fref{position:absolute;top:0;width:10px;height:100%;border-radius:6px;filter:blur(5px);opacity:.5}
/* text */
#titlewrap{position:absolute;left:30px;right:30px;top:120px;text-align:center;z-index:10;opacity:0}
.t1{font-family:"Anton","Arial Black",sans-serif;font-size:132px;line-height:.92;letter-spacing:1px;color:#fff;
  text-shadow:0 4px 0 #000,0 0 30px rgba(255,255,255,.4);transform:skewX(-6deg)}
.t2{font-family:"Anton","Arial Black",sans-serif;font-size:132px;line-height:.92;letter-spacing:1px;color:#ff2e2e;
  text-shadow:0 4px 0 #000,0 0 30px rgba(255,60,60,.6);transform:skewX(-6deg)}
.tund{width:70%;height:10px;margin:8px auto 10px;background:linear-gradient(90deg,#ff2e2e,#ff8a2e);border-radius:4px;transform:skewX(-14deg)}
.t-art{font-family:"Noto Serif JP",serif;font-style:italic;font-size:46px;letter-spacing:8px;color:#f0e6d0}
#scenes{position:absolute;left:40px;right:40px;top:520px;height:440px;z-index:10}
.sc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;will-change:opacity,transform}
.hook{font-family:"Anton","Arial Black",sans-serif;font-size:140px;line-height:.92;letter-spacing:1px;color:#ffe23d;transform:skewX(-6deg);
  text-shadow:0 5px 0 #000,0 0 40px rgba(255,210,60,.6)}
.lyr{font-family:"Anton","Arial Black",sans-serif;font-size:96px;line-height:.98;letter-spacing:1px;color:#fff;transform:skewX(-5deg);
  text-shadow:0 5px 0 #000,0 0 34px rgba(255,80,160,.5)}
.lyr .r{color:#ff3b6b} .lyr .c{color:#35e0ff}
.lyr .jp{display:block;font-family:"Noto Sans JP";font-weight:800;font-size:40px;letter-spacing:2px;color:#ffd23d;margin-top:14px;transform:skewX(0);text-shadow:0 2px 10px rgba(0,0,0,.8)}
.badge{display:inline-block;font-family:"Anton",sans-serif;font-size:34px;letter-spacing:6px;color:#07060c;background:linear-gradient(90deg,#ffe23d,#ff8a3d);padding:8px 26px;border-radius:8px;margin-bottom:18px;transform:skewX(-6deg)}
.cta-t{font-family:"Anton","Arial Black",sans-serif;font-size:110px;line-height:.92;color:#fff;transform:skewX(-6deg);text-shadow:0 5px 0 #000,0 0 34px rgba(255,80,160,.5)}
.cta-t .r{color:#ff2e2e}
.cta-a{font-family:"Noto Serif JP",serif;font-style:italic;font-size:44px;letter-spacing:8px;color:#f0e6d0;margin-top:12px}
.cta-s{font-family:"Noto Sans JP";font-weight:800;font-size:34px;color:#ffd23d;letter-spacing:2px;margin-top:18px}
#flash{position:absolute;inset:0;z-index:11;pointer-events:none;background:#fff;opacity:0;mix-blend-mode:screen}
#vig{position:absolute;inset:0;pointer-events:none;z-index:12;background:radial-gradient(130% 80% at 50% 46%,transparent 54%,rgba(0,0,0,.6) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:20}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#07060c;font-size:60px;background:linear-gradient(135deg,#ffe23d,#ff3b6b);box-shadow:0 10px 40px rgba(0,0,0,.6)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.12);z-index:20}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffe23d,#ff3b6b)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="wall"></div>
  <div id="posterf"></div>
  <div id="stageglow"></div>
  <div id="beamf"></div>
  <div id="hazel"></div>
  <div id="balltop"></div><div id="ball"></div><div id="balldots"></div>
  <div id="stagep"></div>
  <div id="band"></div>
  <div id="crowdglow"></div>
  <div id="crowd"></div>
  <div id="floor"></div><div id="floorref"></div>
  <div id="frameR"></div>
  <div id="door"><div id="doorface"></div><div id="stickerf"></div><div id="handle"></div></div>
 </div>
 <div id="titlewrap"><div class="t1">KICK THE</div><div class="t2">DOOR DOWN</div><div class="tund"></div><div class="t-art">Rolling All Stars</div></div>
 <div id="scenes"></div>
 <div id="flash"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="kickdoor-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=99887766;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
const COLORS=['#ff2d7e','#22d3ee','#ff8a3d','#a855f7','#ffd23d','#35e0ff'];

// posters confined to the upper back wall (small, faint)
const pf=document.getElementById('posterf');
for(let i=0;i<16;i++){const p=document.createElement('div');p.className='poster';const w=46+rnd()*70,h=60+rnd()*90;
  p.style.width=w+'px';p.style.height=h+'px';p.style.left=(rnd()*1080)+'px';p.style.top=(rnd()*470)+'px';
  p.style.background='linear-gradient(135deg,'+COLORS[(rnd()*COLORS.length)|0]+','+COLORS[(rnd()*COLORS.length)|0]+')';
  p.style.transform='rotate('+((rnd()-0.5)*14)+'deg)';pf.appendChild(p);}

// spotlight beams
const bf=document.getElementById('beamf');const beams=[];
const bx=[180,360,560,760,920];
for(let i=0;i<bx.length;i++){const b=document.createElement('div');b.className='beam';
  b.style.left=(bx[i]-220)+'px';b.style.width='440px';b.style.height='1200px';
  const c=COLORS[i%COLORS.length];b.style.background='linear-gradient(180deg,'+c+'cc,'+c+'00 78%)';
  bf.appendChild(b);beams.push({el:b,base:(i-2)*7,sp:0.5+rnd()*0.8,ph:rnd()*6.28,c:c});}

// mirror ball light dots
const bd=document.getElementById('balldots');const bdots=[];
for(let i=0;i<46;i++){const d=document.createElement('div');d.className='bdot';
  d.style.left=(rnd()*1080)+'px';d.style.top=(140+rnd()*1200)+'px';bd.appendChild(d);bdots.push({el:d,ph:rnd()*6.28,sp:1.5+rnd()*3});}

// band silhouettes (dark) standing on the stage, backlit by #stageglow
const band=document.getElementById('band');
function add(cls,l,b,w,h,extra){const d=document.createElement('div');d.className=cls;d.style.left=l+'px';d.style.bottom=b+'px';d.style.width=w+'px';d.style.height=h+'px';if(extra)d.style.cssText+=extra;band.appendChild(d);return d;}
function figure(cx,base,sc,rim){
  add('musician',cx-38*sc,base,76*sc,156*sc,'border-radius:'+(38*sc)+'px '+(38*sc)+'px 0 0');
  add('musician',cx-24*sc,base+146*sc,48*sc,54*sc,'border-radius:50%');
  if(rim)add('rimc',cx-40*sc,base,80*sc,210*sc,'border-radius:40px 40px 0 0;opacity:.7;background:linear-gradient(180deg,'+rim+',transparent)');
}
// positioned inside the doorway opening (x ~ 420..1000)
// drummer center-back + kit
figure(640,855,0.82,'rgba(53,224,255,.45)');
add('musician',598,865,84,34,'border-radius:16px');                       // kick drum
add('musician',552,905,16,64,'transform:rotate(-26deg)');add('musician',712,905,16,64,'transform:rotate(26deg)'); // cymbal stands
add('musician',540,962,46,10,'border-radius:6px;transform:rotate(-14deg)');add('musician',698,962,46,10,'border-radius:6px;transform:rotate(14deg)'); // cymbals
// guitarist left
figure(470,880,1.0,'rgba(53,224,255,.6)');
add('musician',400,934,140,20,'transform:rotate(-16deg);border-radius:12px');
// singer center + mic
figure(660,890,1.08,'rgba(255,210,60,.5)');
add('mic',695,1055,5,120,'');
// bassist right
figure(860,880,1.0,'rgba(255,45,126,.6)');
add('musician',790,934,140,18,'transform:rotate(14deg);border-radius:12px');

// crowd (foreground silhouettes with raised arms, backlit by #crowdglow)
const crowd=document.getElementById('crowd');const people=[];
const rows=[[0,1.0,0.98,70],[150,0.8,0.82,100]];  // [bottomY, scale, opacity, step]
for(let r=0;r<rows.length;r++){const [by,sc,op,step]=rows[r];let x=-10+r*36;
  while(x<1070){const P=document.createElement('div');P.className='person';P.style.left=x+'px';P.style.bottom=by+'px';P.style.opacity=op;P.style.transform='scale('+sc+')';
    const bo=document.createElement('div');bo.className='pbody';bo.style.width='100px';bo.style.height='200px';bo.style.bottom='0';P.appendChild(bo);
    const hd=document.createElement('div');hd.className='phead';hd.style.width='56px';hd.style.height='62px';hd.style.bottom='188px';P.appendChild(hd);
    const aL=document.createElement('div');aL.className='parm';aL.style.height='230px';aL.style.left='10px';aL.style.bottom='200px';P.appendChild(aL);
    const aR=document.createElement('div');aR.className='parm';aR.style.height='230px';aR.style.right='10px';aR.style.bottom='200px';P.appendChild(aR);
    crowd.appendChild(P);
    people.push({el:P,aL,aR,ph:rnd()*6.28,x:x,by:by});
    x+=step+rnd()*34;}
}

// door stickers
const sf=document.getElementById('stickerf');
for(let i=0;i<10;i++){const s=document.createElement('div');s.className='sticker';const w=70+rnd()*90,h=50+rnd()*80;
  s.style.width=w+'px';s.style.height=h+'px';s.style.left=(30+rnd()*380)+'px';s.style.top=(120+rnd()*1500)+'px';
  s.style.background='linear-gradient(135deg,'+COLORS[(rnd()*COLORS.length)|0]+','+COLORS[(rnd()*COLORS.length)|0]+')';
  s.style.transform='rotate('+((rnd()-0.5)*20)+'deg)';sf.appendChild(s);}
// floor reflections
const fr=document.getElementById('floorref');fr.style.cssText='position:absolute;left:0;right:0;bottom:0;height:380px;z-index:5;overflow:hidden';
const frefs=[];for(let i=0;i<12;i++){const r=document.createElement('div');r.className='fref';r.style.left=(rnd()*1080)+'px';
  const c=COLORS[(rnd()*COLORS.length)|0];r.style.background='linear-gradient(180deg,'+c+'cc,transparent)';fr.appendChild(r);frefs.push({el:r,ph:rnd()*6.28,c:c});}

const flash=document.getElementById('flash'),titlewrap=document.getElementById('titlewrap'),world=document.getElementById('world'),ball=document.getElementById('ball'),balldots=document.getElementById('balldots');

const BEAT=461.5; // ms (130bpm)
const scenes=[
 {s:2900, e:4700,  html:'<div class="sc"><div class="hook">HEY! HEY!</div></div>'},
 {s:4700, e:8200,  html:'<div class="sc"><div class="lyr"><span class="r">KICK THE<br>DOOR DOWN</span><span class="jp">ドアを蹴り開けろ</span></div></div>'},
 {s:8200, e:11800, html:'<div class="sc"><div class="lyr">DANCE UNTIL<br>IT\'S MORNING<span class="jp">朝まで踊ろう</span></div></div>'},
 {s:11800,e:15800, html:'<div class="sc"><div class="lyr">NOBODY\'S TURNING<br><span class="c">OUT THE LIGHT</span></div></div>'},
 {s:15800,e:17600, html:'<div class="sc"><div class="hook">HEY! HEY!</div></div>'},
 {s:17600,e:21200, html:'<div class="sc"><div class="lyr"><span class="r">KICK THE<br>DOOR DOWN</span></div></div>'},
 {s:21200,e:26000, html:'<div class="sc"><div class="lyr">THEY CAN\'T<br>HAVE TONIGHT<span class="jp">今夜だけは 渡さない</span></div></div>'},
 {s:26000,e:31000, html:'<div class="sc"><span class="badge">NEW SINGLE</span><div class="cta-t">KICK THE<br><span class="r">DOOR DOWN</span></div><div class="cta-a">Rolling All Stars</div><div class="cta-s">配信中 / Streaming Now</div></div>'},
];
const scEls=[];const marks=[];const scenesEl=document.getElementById('scenes');
scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
  scenesEl.appendChild(el);scEls.push(el);marks.push({start:sc.s,end:sc.e});});
const TOTAL=31000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const bp=(t%BEAT)/BEAT;                 // 0..1 within beat
  const kick=Math.pow(Math.max(0,1-bp*1.7),2);   // sharp thump, decays
  const beatN=Math.floor(t/BEAT);
  // world thump + tiny shake
  world.style.transform='scale('+(1+0.018*kick)+') translate('+((rnd()-0.5)*2*kick).toFixed(1)+'px,'+(-2*kick).toFixed(1)+'px)';
  // beams sweep + strobe with kick
  for(const b of beams){const ang=b.base+Math.sin(ts*b.sp+b.ph)*10;
    b.el.style.transform='rotate('+ang.toFixed(2)+'deg)';b.el.style.opacity=(0.28+0.6*kick).toFixed(3);}
  // mirror ball spin + dots
  ball.style.transform='translateX(-50%) rotate('+(ts*60).toFixed(1)+'deg)';
  for(const d of bdots){d.el.style.opacity=((0.2+0.7*Math.abs(Math.sin(ts*d.sp+d.ph)))*(0.5+0.5*kick)).toFixed(3);
    d.el.style.transform='translate('+(Math.sin(ts*0.3+d.ph)*10).toFixed(1)+'px,0)';}
  // crowd jump + arms on beat (keep each person's scale transform untouched)
  const jump=kick;
  for(const p of people){const yy=-18*jump*(0.7+0.5*Math.sin(p.ph));
    p.el.style.bottom=(p.by+yy)+'px';
    const a=16+36*jump;p.aL.style.transform='rotate('+(-a).toFixed(1)+'deg)';p.aR.style.transform='rotate('+a.toFixed(1)+'deg)';}
  // floor reflections shimmer
  for(const r of frefs){r.el.style.opacity=((0.3+0.3*Math.sin(ts*2+r.ph))*(0.6+0.4*kick)).toFixed(3);r.el.style.transform='scaleY('+(1+0.2*kick)+')';}
  // beat flash (subtle, stronger on downbeats every 4)
  const down=(beatN%4===0)?1:0.5;
  flash.style.opacity=(0.14*kick*down).toFixed(3);
  // title / scenes with beat-pop scale
  titlewrap.style.opacity=Math.max(0,Math.min(smooth(t,300,1200),1-smooth(t,2500,2900))).toFixed(3);
  titlewrap.style.transform='scale('+(1+0.03*kick)+')';
  const FADE=200;
  for(let i=0;i<scEls.length;i++){const m=marks[i];const o=smooth(t,m.start,m.start+FADE)*(1-smooth(t,m.end-FADE,m.end));
    scEls[i].style.opacity=o.toFixed(3);scEls[i].style.transform='scale('+(o*(1+0.05*kick)).toFixed(3)+')';}
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;
function play(){document.getElementById('ui').style.display='none';
  try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);
    barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const st=performance.now();(function fo(){const k=(performance.now()-st)/1200;
    bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1200);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kick the Door Down / Rolling All Stars</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
