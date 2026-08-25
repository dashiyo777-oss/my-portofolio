# -*- coding: utf-8 -*-
"""「愛が始まる場所 / 花明り」 v2 — YouTube promo short (warm cinematic version).
A different take from v1 (which was cool-blue): faithful to the cover's warm gold —
a gas lamp, a warm-lit train with an approaching headlight, a rain-glazed golden
platform, two profiles facing each other, holding hands. Blossom light and rain.
Unified engine (renderAt). On-screen words verified from the cover.
BGM: ai-hajimaru-v2-bgm.mp3 (33s segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#0a0a12;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:#ecdcae;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:linear-gradient(#10142a 0%,#181f3c 40%,#2a2a34 62%,#241a12 80%,#1a120a 100%)}
  .bok{position:absolute;border-radius:50%;opacity:0;filter:blur(3px)}
  .star{position:absolute;width:2px;height:2px;border-radius:50%;background:#cfe0ff;opacity:0}
  /* gas lamp left */
  #lampglow{position:absolute;left:40px;top:420px;width:360px;height:400px;
    background:radial-gradient(circle,rgba(255,190,90,.65),rgba(255,170,80,.16) 42%,transparent 66%)}
  #lamp{position:absolute;left:120px;top:470px;width:72px;height:100px;border-radius:12px 12px 6px 6px;
    background:linear-gradient(#ffe6b0,#ffbf5e 58%,#e0902a);box-shadow:0 0 44px 16px rgba(255,180,90,.6)}
  #lamptop{position:absolute;left:128px;top:450px;width:56px;height:24px;background:#0e0a08;border-radius:6px 6px 0 0}
  #lamppole{position:absolute;left:150px;top:568px;width:11px;height:760px;background:linear-gradient(#161009,#0e0a06)}
  /* train right + headlight */
  #train{position:absolute;right:0;top:700px;width:400px;height:560px;background:linear-gradient(100deg,#1a1206,#3a2a12 44%,#241708);
    border-radius:22px 0 0 22px;box-shadow:-8px 0 44px rgba(0,0,0,.5)}
  #trainroof{position:absolute;right:0;top:672px;width:420px;height:44px;background:#0c0f16;border-radius:12px 0 0 0}
  .twin{position:absolute;width:64px;height:98px;border-radius:6px;background:linear-gradient(#fff0c2,#f2b25a);box-shadow:0 0 24px rgba(242,178,90,.55)}
  #headlight{position:absolute;right:400px;top:1120px;width:80px;height:80px;border-radius:50%;
    background:radial-gradient(circle,#fff7e6,#ffcf7a 46%,rgba(255,180,80,0) 72%);box-shadow:0 0 90px 40px rgba(255,210,120,.6)}
  #platform{position:absolute;left:0;top:1150px;width:100%;height:770px;background:linear-gradient(#1c130a 0%,#150e07 40%,#0f0a05 100%)}
  #wet{position:absolute;left:0;top:1150px;width:100%;height:770px;pointer-events:none;overflow:hidden}
  .refl{position:absolute;top:0;width:60px;height:100%;filter:blur(7px);opacity:.5}
  /* couple: profiles facing each other */
  #couple{position:absolute;left:392px;top:980px;width:300px;height:470px;z-index:4}
  .fig{position:absolute;bottom:0;background:#05060c}
  #man{left:0;width:150px;height:470px;
    clip-path:polygon(38% 0,62% 0,66% 8%,60% 14%,71% 22%,73% 58%,64% 61%,60% 38%,60% 100%,52% 100%,50% 64%,48% 100%,40% 100%,40% 38%,36% 61%,27% 58%,29% 22%,40% 14%,34% 8%)}
  #woman{right:0;width:158px;height:430px;
    clip-path:polygon(40% 0,60% 0,64% 8%,58% 14%,68% 24%,70% 48%,62% 50%,60% 38%,62% 58%,80% 100%,20% 100%,38% 58%,40% 38%,38% 50%,30% 48%,32% 24%,42% 14%,36% 8%)}
  #hands{position:absolute;left:132px;bottom:210px;width:44px;height:15px;background:#05060c;border-radius:8px;z-index:5}
  #rim{position:absolute;left:392px;top:980px;width:300px;height:470px;z-index:3;pointer-events:none;filter:blur(1px)}
  #couplerefl{position:absolute;left:392px;top:1450px;width:300px;height:220px;z-index:2;opacity:.2;transform:scaleY(-1);pointer-events:none}
  #rain{position:absolute;inset:0;pointer-events:none;z-index:6}
  .drop{position:absolute;width:2px;background:linear-gradient(rgba(255,230,180,0),rgba(255,225,170,.4));opacity:.4}
  .petal{position:absolute;width:16px;height:11px;border-radius:60% 0 60% 0;background:#f5cfe0;opacity:0}
  #grain{position:absolute;inset:0;opacity:.08;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 88% at 46% 52%, transparent 46%, rgba(4,3,8,.8) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    text-align:center;padding:120px 70px 0;opacity:0;z-index:8}
  .scene.mid{justify-content:center;padding-top:0}
  .kick{font-size:28px;letter-spacing:.5em;color:#dcc188;font-weight:500;text-transform:uppercase;margin-bottom:20px}
  .title{font-size:116px;line-height:1.16;font-weight:600;color:#f0dfae;letter-spacing:.1em;
    text-shadow:0 2px 30px rgba(0,0,0,.8),0 0 44px rgba(240,200,120,.28)}
  .orn{display:flex;align-items:center;justify-content:center;gap:22px;margin:30px 0 20px;color:#cbb17a}
  .orn i{display:block;width:140px;height:1px;background:linear-gradient(90deg,transparent,#cbb17a,transparent)}
  .orn b{font-size:40px;color:#e8c98a}
  .artist{font-size:56px;letter-spacing:.36em;color:#ecd8a4;font-weight:500;text-shadow:0 2px 16px rgba(0,0,0,.7)}
  .tag{margin-top:34px;font-size:28px;letter-spacing:.44em;color:#dcc188;text-transform:uppercase}
  #bar{position:absolute;left:0;bottom:0;height:6px;width:0;background:linear-gradient(90deg,#e0902a,#f2c078);opacity:.85;z-index:9}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,8,6,.86);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 70px;text-align:center}
  #ui .k{font-size:28px;letter-spacing:.44em;color:#e8c98a;text-transform:uppercase}
  #ui h1{font-size:100px;font-weight:600;color:#f0dfae;line-height:1.12;letter-spacing:.08em}
  #ui p{font-size:44px;letter-spacing:.34em;color:#ecd8a4}
  #play{font-family:'Noto Serif JP',serif;font-size:38px;font-weight:600;color:#1a120a;background:#e8c98a;border:none;
    border-radius:100px;padding:26px 74px;cursor:pointer;letter-spacing:.14em;box-shadow:0 10px 40px rgba(232,201,138,.35)}
  #play:hover{background:#f2dca8}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  const STAR=[]; for(let i=0;i<26;i++){const e=document.createElement('div');e.className='star';
    e.style.left=((i*47)%100)+'%';e.style.top=((i*23)%30)+'%';e.dataset.ph=((i*13)%100)/100;stage.appendChild(e);STAR.push(e);}
  const BOK=[]; for(let i=0;i<34;i++){const e=document.createElement('div');e.className='bok';const cool=i%4===0;
    const sz=10+(i%6)*7;e.style.left=(6+(i*29)%56)+'%';e.style.top=(28+(i*23)%22)+'%';e.style.width=sz+'px';e.style.height=sz+'px';
    e.style.background=cool?'#6f9ac0':'#ffcf82';e.dataset.ph=((i*17)%100)/100;stage.appendChild(e);BOK.push(e);}
  const train=document.getElementById('train');
  for(let i=0;i<4;i++){const w=document.createElement('div');w.className='twin';w.style.right=(28+i*96)+'px';w.style.top='120px';train.appendChild(w);}
  const wet=document.getElementById('wet'),REFL=[];
  [['150px',80,'rgba(255,190,90,.6)'],['auto',260,'rgba(242,178,90,.5)'],['520px',110,'rgba(255,210,120,.7)'],['470px',60,'rgba(255,180,90,.5)']].forEach((r,i)=>{
    const e=document.createElement('div');e.className='refl';if(r[0]==='auto'){e.style.right='40px';}else{e.style.left=r[0];}
    e.style.width=r[1]+'px';e.style.background=`linear-gradient(${r[2]},transparent 74%)`;wet.appendChild(e);e.dataset.ph=i;REFL.push(e);});
  // couple rim + reflection clones
  const rim=document.getElementById('rim'),cr=document.getElementById('couplerefl');
  ['man','woman'].forEach(id=>{const src=document.getElementById(id);
    const a=src.cloneNode();a.id='';a.style.background='rgba(255,205,130,.45)';a.style.transform='translateX(-3px)';rim.appendChild(a);
    const b=src.cloneNode();b.id='';b.style.background='#05060c';cr.appendChild(b);});
  const rain=document.getElementById('rain'),DR=[];
  for(let i=0;i<64;i++){const e=document.createElement('div');e.className='drop';e.style.left=((i*37)%100)+'%';
    e.style.height=(28+(i%5)*18)+'px';e.style.transform='rotate(9deg)';e.dataset.ph=((i*29)%100)/100;e.dataset.sp=0.5+((i*13)%50)/60;rain.appendChild(e);DR.push(e);}
  const PET=[]; for(let i=0;i<12;i++){const e=document.createElement('div');e.className='petal';e.style.left=((i*53)%100)+'%';
    e.dataset.dur=8+((i*43)%40)/10;e.dataset.ph=((i*31)%100)/100;e.dataset.sway=30+((i*17)%40);stage.appendChild(e);PET.push(e);}
  const lamp=document.getElementById('lamp'),lampglow=document.getElementById('lampglow'),head=document.getElementById('headlight'),bar=document.getElementById('bar');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/860,(en-t)/580),0,1);}
  function flick(ts){return 0.9+0.1*(0.6*Math.sin(ts*6.2)+0.4*Math.sin(ts*10.6+1));}
  window.renderAt=function(t){
    const ts=t/1000,fl=flick(ts);
    lamp.style.opacity=fl;lampglow.style.opacity=(0.85*fl).toFixed(3);
    head.style.opacity=(0.7+0.3*Math.abs(Math.sin(ts*0.9))).toFixed(3);
    for(const e of STAR){const ph=+e.dataset.ph;e.style.opacity=(0.25+0.5*(0.5+0.5*Math.sin(ts*1.3+ph*6.28))).toFixed(2);}
    for(const e of BOK){const ph=+e.dataset.ph;e.style.opacity=(0.3+0.45*(0.5+0.5*Math.sin(ts*0.9+ph*6.28))).toFixed(2);}
    for(const r of REFL){const ph=+r.dataset.ph;r.style.transform=`scaleX(${1+0.35*Math.sin(ts*1.7+ph)}) translateX(${Math.sin(ts*1.2+ph)*8}px)`;
      r.style.opacity=(0.4+0.2*Math.sin(ts*2+ph)).toFixed(2)*fl;}
    for(const d of DR){const p=frac(ts*(+d.dataset.sp)+ +d.dataset.ph);d.style.top=(p*1920-120)+'px';d.style.opacity=(0.2+0.3*Math.sin(p*Math.PI)).toFixed(2);}
    for(const e of PET){const p=frac(ts/(+e.dataset.dur)+ +e.dataset.ph);e.style.top=(1780-p*1900)+'px';
      e.style.transform=`translateX(${Math.sin(p*6.28+ +e.dataset.ph*6)*(+e.dataset.sway)}px) rotate(${p*360}deg)`;e.style.opacity=(Math.sin(p*Math.PI)*0.5).toFixed(2);}
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    if(bar) bar.style.width=(clamp(t/total,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search), ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar.style.display='none'; }
  else {
    const bgm=document.getElementById('bgm');
    document.getElementById('play').addEventListener('click',()=>{
      ui.classList.add('hide');
      try{bgm.currentTime=0;bgm.volume=.85;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent='↻ Replay';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.85*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

scenes = [
    (5000, '<div class="scene"><div class="kick">New Single</div></div>'),
    (8600, '<div class="scene"><div class="title">愛が始まる<br>場所</div>'
           '<div class="orn"><i></i><b>&#10047;</b><i></i></div>'
           '<div class="artist">花明り</div></div>'),
    (5400, '<div class="scene mid"><div class="orn" style="margin:0"><i></i><b>&#10047;</b><i></i></div></div>'),
    (9000, '<div class="scene"><div class="title">愛が始まる<br>場所</div>'
           '<div class="orn"><i></i><b>&#10047;</b><i></i></div>'
           '<div class="artist">花明り</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="愛が始まる場所 / 花明り (Promo Short v2)",
  desc="雨あがりの駅、金色の灯りの中で手をつなぐ。花明りの新曲「愛が始まる場所」。",
  k="花明り", ep="愛が始まる場所", tagline="花明り")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = ENGINE.replace("SCENES", scenes_js)
html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="lampglow"></div>
  <div id="train"></div>
  <div id="trainroof"></div>
  <div id="headlight"></div>
  <div id="platform"></div>
  <div id="couplerefl"></div>
  <div id="rim"></div>
  <div id="couple"><div id="man" class="fig"></div><div id="woman" class="fig"></div><div id="hands"></div></div>
  <div id="lamptop"></div>
  <div id="lamp"></div>
  <div id="lamppole"></div>
  <div id="wet"></div>
  <div id="rain"></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="vig"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">花明り</div>
    <h1>愛が始まる場所</h1>
    <p>New Single</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="ai-hajimaru-v2-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "ai-hajimaru-v2-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote ai-hajimaru-v2-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
