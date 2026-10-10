# -*- coding: utf-8 -*-
"""
子猫のロック / Maron — 縦型9:16 宣伝ショート（キッズ・ロック / 2歳以上の日米向け）
ジャケット準拠：濃紺の壁の陽だまり部屋。左にまぶしい窓（観葉植物）、右に吊るしたギター＆アンプ、
猫ポスター、ストリングライト。虹色ニットのラグの上に子猫バンド——
前中央：トラ猫ボーカル＆赤ギター（前足あげて歌う・ウィンク）／左：茶トラのドラム（猫顔バスドラ）／
右：グレーのベース（サンバースト）／右端：ふわふわ子猫のキーボード。毛糸玉・ねずみのぬいぐるみ。
ビート同期：151BPM の弾む四つ打ち。ビートで全員ぴょこん、しっぽ揺れ、音符・肉球・ハートが舞う。
BGM: koneko-bgm.mp3 (source 3:36/216s の最終サビ 3:00〜：半音上げの大合唱＆締めの子守唄)。
英語の簡単な訳つき。画面テキストはジャケット表記＋提供歌詞のみ（創作なし）。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","koneko.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0d1430;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0d1430}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Noto Sans JP",system-ui,sans-serif;background:#13204d}
#world{position:absolute;inset:0;transform-origin:50% 72%}
/* ---- room ---- */
#wall{position:absolute;inset:0;background:
  radial-gradient(120% 80% at 18% 20%, rgba(255,214,140,.5), rgba(255,180,100,.14) 34%, transparent 58%),
  linear-gradient(180deg,#16255c 0%,#1b2c68 46%,#223170 68%,#1a2656 100%)}
#sun{position:absolute;left:-120px;top:-120px;width:780px;height:1180px;pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(52% 44% at 30% 26%, rgba(255,238,190,.92), rgba(255,210,140,.34) 46%, transparent 72%)}
/* window (left) */
#win{position:absolute;left:36px;top:70px;width:300px;height:470px;border-radius:14px;
  background:linear-gradient(180deg,#cfeiff 0%,#bfe6ff 30%,#eaf6ff 100%);
  background:linear-gradient(180deg,#bfe4ff 0%,#dff1ff 60%,#fff6e0 100%);
  box-shadow:0 0 70px 24px rgba(255,236,180,.5),inset 0 0 0 10px #2a3c86,inset 0 0 0 16px #1a2658}
#win::before{content:"";position:absolute;left:50%;top:14px;bottom:14px;width:8px;transform:translateX(-50%);background:#24347a}
#win::after{content:"";position:absolute;top:50%;left:14px;right:14px;height:8px;transform:translateY(-50%);background:#24347a}
.leaf{position:absolute;border-radius:60% 10% 60% 10%;background:radial-gradient(circle at 40% 30%,#8fd98a,#3f9e55);opacity:.95}
#sill{position:absolute;left:24px;top:540px;width:324px;height:26px;border-radius:8px;background:linear-gradient(180deg,#32468f,#1d2a63)}
/* shelf + guitar + amp (right) */
.poster{position:absolute;border-radius:6px;opacity:.9;box-shadow:0 6px 18px rgba(0,0,0,.3)}
#ghang{position:absolute;right:70px;top:150px;width:150px;height:560px;z-index:2;transform:rotate(9deg);transform-origin:top center}
#gbody{position:absolute;bottom:0;left:16px;width:118px;height:168px;border-radius:46% 46% 48% 48%/40% 40% 60% 60%;
  background:radial-gradient(circle at 36% 30%,#ff7a6a,#e23b3b 60%,#9e1f1f);box-shadow:0 8px 20px rgba(0,0,0,.35)}
#gneck{position:absolute;top:0;left:60px;width:26px;height:420px;border-radius:8px;background:linear-gradient(90deg,#6b4a2a,#8a6238,#5a3d22)}
#ghead{position:absolute;top:-6px;left:50px;width:46px;height:60px;border-radius:8px;background:#3a2817}
#amp{position:absolute;right:52px;top:560px;width:220px;height:210px;border-radius:14px;z-index:2;
  background:linear-gradient(180deg,#2a2630,#17141c);box-shadow:0 10px 26px rgba(0,0,0,.4),inset 0 0 0 7px #3b3540}
#amp::before{content:"";position:absolute;left:18px;top:18px;right:18px;height:120px;border-radius:8px;
  background:repeating-linear-gradient(45deg,#201d27 0 7px,#2b2733 7px 14px);box-shadow:inset 0 0 0 4px #4a4350}
.ampled{position:absolute;bottom:22px;width:16px;height:16px;border-radius:50%}
/* string lights */
#lights{position:absolute;left:0;right:0;top:40px;height:120px;z-index:3;pointer-events:none}
.bulb{position:absolute;width:20px;height:20px;border-radius:50%}
/* rug / floor */
#rug{position:absolute;left:-60px;right:-60px;bottom:0;height:720px;z-index:2;border-radius:52% 52% 0 0/120px 120px 0 0;
  background:
   repeating-linear-gradient(92deg,
    #ff8fb3 0 70px,#ffd36b 70px 140px,#7fe0d0 140px 210px,#8fb8ff 210px 280px,#ffb0d8 280px 350px);
  box-shadow:0 -10px 40px rgba(0,0,0,.25)}
#rug::after{content:"";position:absolute;inset:0;border-radius:52% 52% 0 0/120px 120px 0 0;
  background:radial-gradient(120% 90% at 50% 10%,rgba(255,240,210,.35),transparent 60%),
  linear-gradient(180deg,transparent 60%,rgba(0,0,0,.18))}
/* band */
#band{position:absolute;left:0;right:0;bottom:120px;height:1000px;z-index:5}
.kit{position:absolute;transform-origin:50% 100%;will-change:transform}
.kpart{position:absolute}
/* drum kit */
#drums{position:absolute;left:70px;bottom:150px;width:360px;height:360px;z-index:4}
.drum{position:absolute;border-radius:12px}
.bassdrum{width:230px;height:230px;border-radius:50%;left:60px;bottom:0;
  background:radial-gradient(circle at 42% 34%,#ff6a6a,#d0282e 62%,#8c1b1f);
  box-shadow:inset 0 0 0 12px #f2e7d2,0 10px 24px rgba(0,0,0,.35)}
.bdface{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:140px;height:140px;border-radius:50%;
  background:#f4ead6;box-shadow:inset 0 0 0 4px #d8c7a6}
.cym{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 35%,#ffe9a8,#e7b84e 60%,#b8862a);
  box-shadow:0 4px 10px rgba(0,0,0,.3)}
/* keyboard */
#keyb{position:absolute;right:28px;bottom:180px;width:250px;height:120px;z-index:4;transform:rotate(-6deg)}
#keyb .kb{position:absolute;bottom:34px;left:0;width:250px;height:60px;border-radius:10px;background:linear-gradient(180deg,#2b2a33,#141318);box-shadow:0 8px 18px rgba(0,0,0,.35)}
#keyb .keys{position:absolute;bottom:40px;left:12px;width:226px;height:30px;border-radius:4px;
  background:repeating-linear-gradient(90deg,#fff 0 16px,#222 16px 19px)}
.kleg{position:absolute;bottom:0;width:10px;height:40px;background:#1a1922;border-radius:4px}
/* instruments held */
.inst{position:absolute;z-index:6}
/* text */
#titlewrap{position:absolute;left:20px;right:20px;top:120px;text-align:center;z-index:12;opacity:0}
#ears-doodle{position:relative;height:70px;margin-bottom:-6px}
.edl,.edr{position:absolute;top:0;width:0;height:0;border-left:34px solid transparent;border-right:34px solid transparent;border-bottom:66px solid transparent}
.tt{font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:150px;line-height:.9;letter-spacing:2px;
  filter:drop-shadow(0 5px 0 rgba(0,0,0,.35)) drop-shadow(0 0 22px rgba(255,255,255,.25));display:inline-block}
.c1{color:#ffd93b}.c2{color:#ff5fa2}.c3{color:#ffffff}.c4{color:#4ad4ff}.c5{color:#ffffff}.c6{color:#ffd93b}
.tart{font-family:"Noto Serif JP",serif;font-weight:800;font-style:italic;font-size:56px;letter-spacing:6px;color:#fff;
  text-shadow:0 3px 0 rgba(0,0,0,.3);margin-top:4px}
.tund{width:300px;height:12px;margin:6px auto 0;border-radius:8px;background:linear-gradient(90deg,#ffd93b,#ff9b3b);transform:rotate(-2deg)}
#scenes{position:absolute;left:36px;right:36px;top:470px;height:470px;z-index:12}
.sc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;will-change:opacity,transform}
.hook{font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:118px;line-height:1.02;letter-spacing:1px;
  text-shadow:0 5px 0 rgba(0,0,0,.3),0 0 34px rgba(255,180,80,.5)}
.hook .n1{color:#ffd93b}.hook .n2{color:#ff5fa2}.hook .n3{color:#4ad4ff}
.hook .en{display:block;font-family:"Noto Sans JP",sans-serif;font-weight:800;font-size:92px;color:#fff;margin-top:6px;text-shadow:0 4px 0 rgba(0,0,0,.3)}
.lyr{font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:92px;line-height:1.08;letter-spacing:1px;color:#fff;
  text-shadow:0 5px 0 rgba(0,0,0,.32),0 0 30px rgba(255,150,200,.45)}
.lyr .hi{color:#ffd93b}.lyr .pk{color:#ff7ab0}.lyr .bl{color:#6fd6ff}
.lyr .en{display:block;font-family:"Noto Sans JP",sans-serif;font-weight:800;font-size:46px;letter-spacing:1px;color:#ffe59a;margin-top:18px;text-shadow:0 2px 10px rgba(0,0,0,.6)}
.badge{display:inline-block;font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:40px;letter-spacing:4px;color:#13204d;
  background:linear-gradient(90deg,#ffd93b,#ff9b3b);padding:10px 30px;border-radius:40px;margin-bottom:20px;box-shadow:0 6px 0 rgba(0,0,0,.25)}
.cta-t{font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:128px;line-height:.94;
  filter:drop-shadow(0 5px 0 rgba(0,0,0,.3))}
.cta-t .a{color:#ffd93b}.cta-t .b{color:#ff5fa2}.cta-t .c{color:#4ad4ff}
.cta-a{font-family:"Noto Serif JP",serif;font-style:italic;font-weight:800;font-size:52px;letter-spacing:6px;color:#fff;margin-top:12px}
.cta-s{font-family:"Noto Sans JP",sans-serif;font-weight:800;font-size:40px;color:#ffe59a;letter-spacing:2px;margin-top:20px}
.cta-b{font-family:"Noto Sans JP",sans-serif;font-weight:900;font-size:34px;color:#fff;letter-spacing:8px;margin-top:10px;opacity:.9}
#fx{position:absolute;inset:0;z-index:9;pointer-events:none}
#flash{position:absolute;inset:0;z-index:11;pointer-events:none;background:#fff;opacity:0;mix-blend-mode:screen}
#vig{position:absolute;inset:0;pointer-events:none;z-index:13;background:radial-gradient(135% 86% at 50% 44%,transparent 56%,rgba(5,8,24,.5) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:20}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#13204d;font-size:60px;background:linear-gradient(135deg,#ffd93b,#ff5fa2);box-shadow:0 10px 40px rgba(0,0,0,.5)}
#bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:20}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffd93b,#ff5fa2)}
body.capture #ui,body.capture #bar{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="wall"></div>
  <div id="sun"></div>
  <div id="win"></div><div id="leaves"></div><div id="sill"></div>
  <div id="posterf"></div>
  <div id="ghang"><div id="gneck"></div><div id="ghead"></div><div id="gbody"></div></div>
  <div id="amp"><div class="ampled" style="left:24px;background:radial-gradient(circle,#ffd36b,#b8781e)"></div><div class="ampled" style="left:52px;background:radial-gradient(circle,#ff6a9a,#aa2a55)"></div></div>
  <div id="lights"></div>
  <div id="rug"></div>
  <div id="drums"></div>
  <div id="keyb"><div class="kb"></div><div class="keys"></div><div class="kleg" style="left:26px"></div><div class="kleg" style="right:26px"></div></div>
  <div id="band"></div>
  <div id="fx"></div>
 </div>
 <div id="titlewrap">
  <div id="ears-doodle"><div class="edl"></div><div class="edr"></div></div>
  <div><span class="tt c1">子</span><span class="tt c2">猫</span><span class="tt c3">の</span><span class="tt c4">ロ</span><span class="tt c5">ッ</span><span class="tt c6">ク</span></div>
  <div class="tart">Maron</div><div class="tund"></div>
 </div>
 <div id="scenes"></div>
 <div id="flash"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="koneko-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=20251010;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');d.className=(cls||'kpart');if(st)d.style.cssText+=st;p.appendChild(d);return d;}

/* window plant leaves */
const lv=document.getElementById('leaves');
for(let i=0;i<10;i++){const e=document.createElement('div');e.className='leaf';const w=40+rnd()*60;
  e.style.cssText='position:absolute;width:'+w+'px;height:'+(w*0.7)+'px;left:'+(40+rnd()*280)+'px;top:'+(90+rnd()*360)+'px;transform:rotate('+((rnd()-0.5)*80)+'deg);opacity:.9;z-index:1';
  lv.appendChild(e);}
/* potted plant on sill */
(function(){const pot=document.createElement('div');pot.style.cssText='position:absolute;left:60px;top:470px;width:70px;height:66px;border-radius:8px 8px 14px 14px;background:linear-gradient(180deg,#e38b5a,#b85f34);z-index:3';document.getElementById('world').appendChild(pot);
  for(let i=0;i<6;i++){const e=document.createElement('div');e.className='leaf';const w=30+rnd()*26;
   e.style.cssText='position:absolute;width:'+w+'px;height:'+(w*0.8)+'px;left:'+(58+rnd()*74)+'px;top:'+(420+rnd()*60)+'px;transform:rotate('+((rnd()-0.5)*120)+'deg);z-index:3';document.getElementById('world').appendChild(e);} })();

/* cat posters on the wall */
const pf=document.getElementById('posterf');
const posterPos=[[770,120,120,150,'#2a3a86'],[930,120,110,150,'#30459a'],[792,300,150,120,'#26357e']];
posterPos.forEach(([x,y,w,h,bg])=>{const p=document.createElement('div');p.className='poster';
  p.style.cssText='left:'+x+'px;top:'+y+'px;width:'+w+'px;height:'+h+'px;background:'+bg+';z-index:1';
  // simple black cat silhouette head
  const c=document.createElement('div');c.style.cssText='position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);width:'+(w*0.5)+'px;height:'+(w*0.5)+'px;border-radius:50%;background:#0c1130';
  const e1=document.createElement('div');e1.style.cssText='position:absolute;left:14%;top:-30%;width:0;height:0;border-left:'+(w*0.1)+'px solid transparent;border-right:'+(w*0.1)+'px solid transparent;border-bottom:'+(w*0.22)+'px solid #0c1130';
  const e2=document.createElement('div');e2.style.cssText='position:absolute;right:14%;top:-30%;width:0;height:0;border-left:'+(w*0.1)+'px solid transparent;border-right:'+(w*0.1)+'px solid transparent;border-bottom:'+(w*0.22)+'px solid #0c1130';
  c.appendChild(e1);c.appendChild(e2);p.appendChild(c);pf.appendChild(p);});

/* string lights */
const LT=document.getElementById('lights');const bulbs=[];const bcol=['#ffd36b','#ff8fb3','#8fe0ff','#b6ff8f','#ffb0e0'];
for(let i=0;i<14;i++){const x=10+i*78;const y=50+Math.sin(i*0.9)*26+ (i%2)*8;
  const b=document.createElement('div');b.className='bulb';b.style.cssText='left:'+x+'px;top:'+y+'px;background:radial-gradient(circle at 40% 35%,#fff,'+bcol[i%bcol.length]+');box-shadow:0 0 16px 4px '+bcol[i%bcol.length];
  LT.appendChild(b);bulbs.push({el:b,ph:rnd()*6.28});}

/* ---- drum kit detail ---- */
const dk=document.getElementById('drums');
const bd=mk(dk,'width:230px;height:230px;border-radius:50%;left:64px;bottom:0;background:radial-gradient(circle at 42% 34%,#ff7a7a,#d0282e 62%,#8c1b1f);box-shadow:inset 0 0 0 12px #f2e7d2,0 10px 24px rgba(0,0,0,.35);z-index:2','drum');
const bdf=mk(dk,'left:118px;bottom:52px;width:128px;height:128px;border-radius:50%;background:#f4ead6;box-shadow:inset 0 0 0 4px #d8c7a6;z-index:3');
// cat face on bass drum
mk(bdf,'position:absolute;left:50%;top:54%;transform:translate(-50%,-50%);width:58px;height:50px;border-radius:50%;background:#1a1526');
mk(bdf,'position:absolute;left:24px;top:14px;width:0;height:0;border-left:16px solid transparent;border-right:16px solid transparent;border-bottom:30px solid #1a1526');
mk(bdf,'position:absolute;right:24px;top:14px;width:0;height:0;border-left:16px solid transparent;border-right:16px solid transparent;border-bottom:30px solid #1a1526');
mk(bdf,'position:absolute;left:40px;top:60px;width:8px;height:8px;border-radius:50%;background:#fff');
mk(bdf,'position:absolute;right:40px;top:60px;width:8px;height:8px;border-radius:50%;background:#fff');
// small tom + cymbals
mk(dk,'left:8px;bottom:150px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 40% 32%,#ff9a6a,#d85a2a);box-shadow:inset 0 0 0 9px #f2e7d2,0 8px 16px rgba(0,0,0,.3);z-index:2','drum');
const cymL=mk(dk,'left:-24px;bottom:232px;width:130px;height:26px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#ffe9a8,#e7b84e 60%,#b8862a);transform:rotate(-10deg);z-index:1','cym');
mk(dk,'left:30px;bottom:150px;width:10px;height:120px;background:#b9b2a2;z-index:0');

/* ---- kitten builder ---- */
const band=document.getElementById('band');
// cfg: {x, y, sc, fur, fur2, belly, ear, stripe, face, z}
function kitten(cfg){
  const z=cfg.z||5;
  const K=document.createElement('div');K.className='kit';
  K.style.cssText='left:'+cfg.x+'px;bottom:'+cfg.y+'px;transform:scale('+cfg.sc+');z-index:'+z;
  // local box 240 wide; parts positioned from left with center ~120
  const cx=120;
  // tail
  const tail=mk(K,'left:'+(cx+40)+'px;bottom:40px;width:120px;height:46px;border-top-left-radius:60px;border-top-right-radius:60px;border:22px solid '+cfg.fur+';border-bottom:none;border-right:none;transform-origin:left bottom;z-index:'+(z-1));
  // back feet
  mk(K,'left:'+(cx-70)+'px;bottom:0;width:72px;height:40px;border-radius:40px;background:'+cfg.fur);
  mk(K,'left:'+(cx+2)+'px;bottom:0;width:72px;height:40px;border-radius:40px;background:'+cfg.fur);
  // body
  const body=mk(K,'left:'+(cx-92)+'px;bottom:18px;width:184px;height:200px;border-radius:92px 92px 80px 80px;background:radial-gradient(circle at 42% 30%,'+cfg.fur2+','+cfg.fur+' 72%);box-shadow:0 10px 24px rgba(0,0,0,.28)');
  // belly patch
  mk(body,'position:absolute;left:50%;bottom:4px;transform:translateX(-50%);width:108px;height:130px;border-radius:60px 60px 54px 54px;background:'+cfg.belly);
  // head group (for bobbing)
  const hg=mk(K,'left:'+(cx-92)+'px;bottom:150px;width:184px;height:184px;z-index:'+(z+1));
  // ears
  const earL=mk(hg,'position:absolute;left:8px;top:-26px;width:0;height:0;border-left:34px solid transparent;border-right:20px solid transparent;border-bottom:70px solid '+cfg.fur+';transform:rotate(-16deg);transform-origin:bottom center');
  mk(earL,'position:absolute;left:-18px;top:30px;width:0;height:0;border-left:18px solid transparent;border-right:10px solid transparent;border-bottom:38px solid '+cfg.ear);
  const earR=mk(hg,'position:absolute;right:8px;top:-26px;width:0;height:0;border-left:20px solid transparent;border-right:34px solid transparent;border-bottom:70px solid '+cfg.fur+';transform:rotate(16deg);transform-origin:bottom center');
  mk(earR,'position:absolute;right:-18px;top:30px;width:0;height:0;border-left:10px solid transparent;border-right:18px solid transparent;border-bottom:38px solid '+cfg.ear);
  // head
  const head=mk(hg,'position:absolute;left:0;top:0;width:184px;height:172px;border-radius:50% 50% 48% 48%;background:radial-gradient(circle at 42% 34%,'+cfg.fur2+','+cfg.fur+' 76%);box-shadow:0 6px 16px rgba(0,0,0,.2)');
  // forehead stripes (tabby)
  if(cfg.stripe){
    mk(head,'position:absolute;left:50%;top:6px;transform:translateX(-50%);width:14px;height:40px;border-radius:8px;background:'+cfg.stripe);
    mk(head,'position:absolute;left:38%;top:10px;transform:translateX(-50%);width:11px;height:32px;border-radius:7px;background:'+cfg.stripe);
    mk(head,'position:absolute;left:62%;top:10px;transform:translateX(-50%);width:11px;height:32px;border-radius:7px;background:'+cfg.stripe);
  }
  // cheeks (white muzzle)
  mk(head,'position:absolute;left:50%;top:84px;transform:translateX(-50%);width:120px;height:78px;border-radius:60px;background:'+cfg.belly);
  // blush
  mk(head,'position:absolute;left:14px;top:96px;width:38px;height:24px;border-radius:50%;background:rgba(255,150,170,.55)');
  mk(head,'position:absolute;right:14px;top:96px;width:38px;height:24px;border-radius:50%;background:rgba(255,150,170,.55)');
  // eyes
  function openEye(x){const e=mk(head,'position:absolute;top:70px;'+x+'width:38px;height:44px;border-radius:50%;background:#1f1a2e');
    mk(e,'position:absolute;left:8px;top:8px;width:14px;height:14px;border-radius:50%;background:#fff');}
  function closeEye(x){mk(head,'position:absolute;top:88px;'+x+'width:40px;height:20px;border-bottom:7px solid #1f1a2e;border-radius:0 0 40px 40px');}
  if(cfg.face==='sing'){openEye('left:34px;');closeEye('right:34px;');}
  else if(cfg.face==='wink'){closeEye('left:34px;');openEye('right:34px;');}
  else if(cfg.face==='calm'){
    mk(head,'position:absolute;top:78px;left:40px;width:30px;height:34px;border-radius:50%;background:#1f1a2e');
    mk(head,'position:absolute;top:78px;right:40px;width:30px;height:34px;border-radius:50%;background:#1f1a2e');
  } else {closeEye('left:34px;');closeEye('right:34px;');}
  // nose
  mk(head,'position:absolute;left:50%;top:104px;transform:translateX(-50%);width:20px;height:15px;border-radius:50% 50% 60% 60%;background:#ff7a9a');
  // mouth
  if(cfg.face==='sing'){
    const m=mk(head,'position:absolute;left:50%;top:120px;transform:translateX(-50%);width:46px;height:46px;border-radius:40% 40% 50% 50%;background:#7a1f33');
    mk(m,'position:absolute;left:50%;bottom:4px;transform:translateX(-50%);width:30px;height:20px;border-radius:0 0 30px 30px;background:#ff8fa8');
  } else {
    mk(head,'position:absolute;left:46%;top:120px;width:22px;height:14px;border:5px solid #6a2838;border-top:none;border-right:none;border-radius:0 0 0 20px;transform:translateX(-100%)');
    mk(head,'position:absolute;left:54%;top:120px;width:22px;height:14px;border:5px solid #6a2838;border-top:none;border-left:none;border-radius:0 0 20px 0');
  }
  // whiskers
  for(const sgn of [-1,1]){for(let k=0;k<3;k++){
    mk(head,'position:absolute;top:'+(108+k*12)+'px;'+(sgn<0?'left:-6px':'right:-6px')+';width:46px;height:3px;border-radius:3px;background:rgba(255,255,255,.75);transform:rotate('+(sgn*(k-1)*10)+'deg)');
  }}
  band.appendChild(K);
  return {el:K,head:hg,tail:tail,earL:earL,earR:earR,cfg:cfg};
}

/* paw helper for arms holding instruments */
function paw(parent,st){return mk(parent,st+';border-radius:50%');}

/* --- place the band (match jacket layout) --- */
// Drummer (left, ginger) behind kit
const drummer=kitten({x:150,y:300,sc:0.92,fur:'#e8a25a',fur2:'#f6bf7d',belly:'#fff4e2',ear:'#ff9fb0',stripe:'#c67a34',face:'happy',z:4});
// drumsticks (animated)
const stickL=mk(band,'left:300px;bottom:560px;width:12px;height:150px;border-radius:6px;background:#caa06a;transform-origin:bottom center;z-index:7');
const stickR=mk(band,'left:360px;bottom:560px;width:12px;height:150px;border-radius:6px;background:#caa06a;transform-origin:bottom center;z-index:7');

// Bassist (right-center, grey tabby)
const bassist=kitten({x:720,y:300,sc:0.96,fur:'#9aa2ad',fur2:'#c3c9d2',belly:'#f3f5f8',ear:'#ffaebd',stripe:'#6e7681',face:'calm',z:5});
// bass guitar (sunburst) across body
const bass=mk(band,'left:690px;bottom:430px;width:300px;height:30px;border-radius:14px;background:linear-gradient(90deg,#3a2817,#8a6238 70%,#3a2817);transform:rotate(-16deg);transform-origin:left center;z-index:7');
mk(bass,'position:absolute;right:-18px;top:-34px;width:96px;height:96px;border-radius:46% 46% 50% 50%;background:radial-gradient(circle at 40% 34%,#ffd36b,#e08a2a 55%,#7a3d14)');

// Keyboardist (far right, fluffy grey-white)
const keyboardist=kitten({x:842,y:250,sc:0.82,fur:'#b7bcc6',fur2:'#e4e7ec',belly:'#fafbfc',ear:'#ffb6c4',stripe:'',face:'calm',z:5});

// Singer/guitarist (front center, tabby) — biggest, paw up
const singer=kitten({x:430,y:230,sc:1.3,fur:'#b5905c',fur2:'#d8b784',belly:'#fdf6e9',ear:'#ff9fb0',stripe:'#7c5c33',face:'sing',z:8});
// red guitar + strap across the LOWER body (kept clear of the face)
const guitar=mk(band,'left:470px;bottom:330px;width:360px;height:130px;z-index:9');
const gbody=mk(guitar,'position:absolute;right:0;bottom:0;width:150px;height:120px;border-radius:46% 46% 50% 50%/40% 40% 60% 60%;background:radial-gradient(circle at 36% 30%,#ff7a6a,#e23b3b 60%,#9e1f1f);box-shadow:0 8px 18px rgba(0,0,0,.3)');
mk(gbody,'position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;background:#2a0f0f');
mk(gbody,'position:absolute;left:12%;top:34%;width:60%;height:7px;border-radius:4px;background:#f0e6d0;transform:rotate(10deg);transform-origin:left');
mk(guitar,'position:absolute;left:0;top:34px;width:210px;height:20px;border-radius:8px;background:linear-gradient(90deg,#5a3d22,#8a6238);transform:rotate(12deg);transform-origin:right center');
const strap=mk(band,'left:548px;bottom:418px;width:26px;height:120px;background:#2a2740;transform:rotate(14deg);transform-origin:bottom center;z-index:8');
// star on the strap
mk(strap,'position:absolute;left:1px;top:30px;width:20px;height:20px;background:#ffd93b;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)');
// raised left arm + paw of the singer (rooted at the shoulder, pumps on beat)
const pawUp=mk(band,'left:474px;bottom:505px;width:40px;height:175px;border-radius:24px;background:linear-gradient(180deg,#c9a877,#b5905c);transform-origin:bottom center;z-index:10');
mk(pawUp,'position:absolute;left:-10px;top:-14px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle at 42% 34%,#d8b784,#b5905c)');
mk(pawUp,'position:absolute;left:5px;top:6px;width:20px;height:16px;border-radius:50%;background:#ff9fb0');
mk(pawUp,'position:absolute;left:28px;top:6px;width:20px;height:16px;border-radius:50%;background:#ff9fb0');
mk(pawUp,'position:absolute;left:14px;top:22px;width:28px;height:22px;border-radius:50%;background:#ff9fb0');

/* --- floating FX: paws / notes / stars / hearts --- */
const fx=document.getElementById('fx');const floaters=[];
const GLY=['note','note','paw','star','note','paw','star','heart','note','star','paw','note','heart','star','note'];
function floatEl(kind){
  const e=document.createElement('div');e.style.position='absolute';e.style.pointerEvents='none';
  const col=['#ffd93b','#ff5fa2','#4ad4ff','#8fe88f','#ff9b3b'][(rnd()*5)|0];
  if(kind==='note'){e.style.cssText+=';font-family:sans-serif;font-weight:900;color:'+col+';text-shadow:0 2px 6px rgba(0,0,0,.35)';e.textContent=(rnd()<0.5?'♪':'♫');e.style.fontSize=(44+rnd()*46)+'px';}
  else if(kind==='paw'){e.style.cssText+=';width:'+(30+rnd()*26)+'px;height:'+(30+rnd()*26)+'px';
    const pad=document.createElement('div');pad.style.cssText='position:absolute;left:20%;top:34%;width:60%;height:50%;border-radius:50%;background:'+col;e.appendChild(pad);
    for(let i=0;i<4;i++){const t=document.createElement('div');t.style.cssText='position:absolute;top:0;left:'+(8+i*22)+'%;width:16%;height:30%;border-radius:50%;background:'+col;e.appendChild(t);} }
  else if(kind==='star'){e.style.cssText+=';width:'+(34+rnd()*30)+'px;height:'+(34+rnd()*30)+'px;background:'+col+';clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)';}
  else {e.style.cssText+=';width:'+(30+rnd()*28)+'px;height:'+(30+rnd()*28)+'px;background:'+col+';clip-path:path("M12 21s-9-5.7-9-12a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 6.3-9 12-9 12z")';
    e.style.cssText+=';background:'+col+';border-radius:50% 50% 0 0;transform:rotate(45deg)';
    e.innerHTML='<div style="position:absolute;left:-50%;top:0;width:100%;height:100%;border-radius:50%;background:'+col+'"></div><div style="position:absolute;left:0;top:-50%;width:100%;height:100%;border-radius:50%;background:'+col+'"></div>';}
  fx.appendChild(e);
  return {el:e,kind,x:rnd()*1080,base:rnd()*2000,sp:60+rnd()*90,amp:20+rnd()*40,ph:rnd()*6.28,rot:(rnd()-0.5)*2,sz:0.7+rnd()*0.7};
}
for(let i=0;i<22;i++){floaters.push(floatEl(GLY[i%GLY.length]));}

/* confetti for climax */
const confetti=[];
for(let i=0;i<60;i++){const c=document.createElement('div');const col=['#ffd93b','#ff5fa2','#4ad4ff','#8fe88f','#ff9b3b','#fff'][(rnd()*6)|0];
  c.style.cssText='position:absolute;width:'+(10+rnd()*12)+'px;height:'+(14+rnd()*16)+'px;background:'+col+';border-radius:3px;opacity:0;z-index:10';
  fx.appendChild(c);confetti.push({el:c,x:rnd()*1080,vy:160+rnd()*220,sway:20+rnd()*40,ph:rnd()*6.28,rot:(rnd()-0.5)*4,delay:rnd()*600});}

const world=document.getElementById('world'),sun=document.getElementById('sun'),flash=document.getElementById('flash'),titlewrap=document.getElementById('titlewrap');
const edl=document.querySelector('.edl'),edr=document.querySelector('.edr');

const BEAT=397.4; // ms (151bpm felt)
const KEY=8900;   // key-change climax lands here (chorus BGM 180s->video; source ~199s)
const scenes=[
 {s:2500, e:6200,  html:'<div class="sc"><div class="hook"><span class="n1">ニャ</span> <span class="n2">ニャ</span> <span class="n3">ニャ</span><br>Rock ’n’ Roll<span class="en">Nya nya nya — rock ’n’ roll!</span></div></div>'},
 {s:6200, e:9600,  html:'<div class="sc"><div class="lyr">ちいさな こねこの<br><span class="hi">Rock ’n’ Roll</span><span class="en">We little kittens rock ’n’ roll!</span></div></div>'},
 {s:9600, e:13400, html:'<div class="sc"><div class="lyr"><span class="pk">ジャンプ ジャンプ</span><br>ソファーをこえて<span class="en">Jump, jump — over the sofa!</span></div></div>'},
 {s:13400,e:17200, html:'<div class="sc"><div class="lyr">ゴロゴロ <span class="pk">ハート</span>が<br>さけぶんだ<span class="en">Purr-purr — our hearts are singing!</span></div></div>'},
 {s:17200,e:21400, html:'<div class="sc"><div class="lyr">せかいで いちばん<br><span class="hi">じゆうなの</span><span class="en">The freest in the whole wide world!</span></div></div>'},
 {s:21400,e:25200, html:'<div class="sc"><div class="lyr">みんなで いっしょに<br><span class="bl">(ニャー！)</span><span class="en">All together now — meow!</span></div></div>'},
 {s:25200,e:30000, html:'<div class="sc"><span class="badge">♪ NEW SONG</span><div class="cta-t"><span class="a">子</span><span class="b">猫</span><span class="c">の</span><span class="a">ロ</span><span class="b">ッ</span><span class="c">ク</span></div><div class="cta-a">Maron</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>'},
];
const scEls=[];const marks=[];const scenesEl=document.getElementById('scenes');
scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
  scenesEl.appendChild(el);scEls.push(el);marks.push({start:sc.s,end:sc.e});});
const TOTAL=30000;window.TOTAL=TOTAL;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const bp=(t%BEAT)/BEAT;
  const kick=Math.pow(Math.max(0,1-bp*1.6),2);          // bounce impulse
  const beatN=Math.floor(t/BEAT);
  const up=(beatN%2===0);                                 // alternate big hop
  const climax=smooth(t,KEY,KEY+600)*(1-smooth(t,29000,30000)); // energy lift after key change
  const energy=0.6+0.4*climax;
  // whole room gentle breathe + beat thump
  world.style.transform='scale('+(1+0.012*kick*energy)+') translateY('+(-3*kick).toFixed(1)+'px)';
  // sunbeam pulse + twinkle lights
  sun.style.opacity=(0.8+0.2*Math.sin(ts*1.2)+0.12*kick).toFixed(3);
  for(const b of bulbs){b.el.style.opacity=(0.6+0.4*Math.abs(Math.sin(ts*2+b.ph))).toFixed(3);}
  // kittens bob on beat (head bobs harder), tails sway, ears flick
  const hop=kick*(0.8+0.6*climax);
  function bob(k,amp,phase){const y=-amp*hop;
    k.el.style.transform='scale('+k.cfg.sc+') translateY('+y.toFixed(1)+'px)';
    k.head.style.transform='translateY('+(-amp*0.5*hop).toFixed(1)+'px) rotate('+(Math.sin(ts*2+phase)*4).toFixed(1)+'deg)';
    const tw=Math.sin(ts*3+phase)*8;k.tail.style.transform='rotate('+(tw-18).toFixed(1)+'deg)';
    k.earL.style.transform='rotate('+(-16+Math.sin(ts*4+phase)*6).toFixed(1)+'deg)';
    k.earR.style.transform='rotate('+(16-Math.sin(ts*4+phase)*6).toFixed(1)+'deg)';}
  bob(singer,26,0);bob(bassist,18,1.4);bob(keyboardist,16,2.6);bob(drummer,16,3.6);
  // singer raised paw pumps on beat
  pawUp.style.transform='rotate('+(-4-20*hop).toFixed(1)+'deg) translateY('+(-8*hop).toFixed(1)+'px)';
  // drumsticks hit on beat
  const hit=(1-kick);stickL.style.transform='translateY('+(10*kick).toFixed(1)+'px) rotate('+(-24-30*hit).toFixed(1)+'deg)';
  stickR.style.transform='translateY('+(10*kick).toFixed(1)+'px) rotate('+(24+30*hit).toFixed(1)+'deg)';
  // floaters rise & loop
  for(const f of floaters){const yy=1980 - ((ts*f.sp + f.base) % 2100);
    const xx=f.x + Math.sin(ts*0.8+f.ph)*f.amp;
    const op=yy>1700?smooth(yy,1980,1760):(yy<160?smooth(yy,-40,160):1);
    f.el.style.left=xx.toFixed(1)+'px';f.el.style.top=yy.toFixed(1)+'px';
    f.el.style.opacity=(op*(0.65+0.35*climax)).toFixed(3);
    f.el.style.transform='scale('+(f.sz*(1+0.12*kick))+') rotate('+(ts*40*f.rot).toFixed(1)+'deg)';}
  // confetti burst at climax
  const ct=t-KEY;
  for(const c of confetti){ if(ct>c.delay){const e=(ct-c.delay)/1000;const yy=-40+c.vy*e;
     c.el.style.opacity=(yy>1980?0:0.95*(1-smooth(t,28600,30000))).toFixed(3);
     c.el.style.left=(c.x+Math.sin(e*2+c.ph)*c.sway)+'px';c.el.style.top=yy+'px';
     c.el.style.transform='rotate('+(e*c.rot*200).toFixed(0)+'deg)';}
   else c.el.style.opacity='0';}
  // title in/out with beat pop
  const tvis=Math.max(0,Math.min(smooth(t,250,1050),1-smooth(t,2050,2450)));
  titlewrap.style.opacity=tvis.toFixed(3);
  titlewrap.style.transform='scale('+(1+0.028*kick)+') rotate('+(Math.sin(ts*2)*1).toFixed(2)+'deg)';
  const ec='#fff';edl.style.borderBottomColor='rgba(255,255,255,'+(0.85).toFixed(2)+')';edr.style.borderBottomColor=edl.style.borderBottomColor;
  edl.style.transform='translateX(185px) rotate('+(-10+Math.sin(ts*4)*4).toFixed(1)+'deg)';
  edr.style.transform='translateX(265px) rotate('+(10-Math.sin(ts*4)*4).toFixed(1)+'deg)';
  // scenes
  const FADE=240;
  for(let i=0;i<scEls.length;i++){const m=marks[i];const o=smooth(t,m.start,m.start+FADE)*(1-smooth(t,m.end-FADE,m.end));
    scEls[i].style.opacity=o.toFixed(3);
    scEls[i].style.transform='translateY('+((1-o)*24).toFixed(1)+'px) scale('+(o*(1+0.045*kick*energy)).toFixed(3)+')';}
  // tiny beat flash at the key change only
  flash.style.opacity=(climax*0.1*kick).toFixed(3);
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
<title>子猫のロック / Maron</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
