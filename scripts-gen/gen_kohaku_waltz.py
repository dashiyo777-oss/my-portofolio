# -*- coding: utf-8 -*-
"""「ほどける夜のワルツ / 琥珀譲二」 — YouTube promo short (elegant jazz-lounge waltz).
Original take: a warm vintage lounge — a crystal chandelier, a grand-piano stage,
a glowing bar, a mirror-polished parquet floor, two glasses of red wine and a candle.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
On-screen words are verified from the cover (ほどける夜のワルツ / 琥珀譲二 / KOHAKU JOJI).
BGM: hodokeru-waltz-bgm.mp3 (33s segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#0f0803;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:#ecdcae;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:radial-gradient(120% 80% at 50% 30%, #3a2008 0%, #241206 40%, #160c04 74%, #0d0602 100%)}
  #curtain{position:absolute;left:0;top:280px;width:420px;height:420px;background:repeating-linear-gradient(90deg,#4a1214 0 26px,#3a0e10 26px 52px);opacity:.7}
  #stagefloor{position:absolute;left:0;top:640px;width:430px;height:120px;background:linear-gradient(#1a0f06,#0f0803);border-radius:0 20px 0 0}
  #spot{position:absolute;left:60px;top:340px;width:340px;height:420px;background:radial-gradient(ellipse at 40% 30%,rgba(255,196,110,.34),transparent 66%)}
  #pianobody{position:absolute;left:66px;top:556px;width:300px;height:96px;background:linear-gradient(#100b12,#07050a);
    border-radius:14px 120px 22px 22px;box-shadow:0 10px 26px rgba(0,0,0,.5),inset 0 3px 0 rgba(210,180,140,.14)}
  #pianolid{position:absolute;left:120px;top:470px;width:250px;height:96px;background:linear-gradient(#141019,#0a070d);
    clip-path:polygon(0 100%,60% 0,100% 30%,46% 100%);box-shadow:inset 0 2px 0 rgba(210,180,140,.16)}
  #pianoleg{position:absolute;left:120px;top:648px;width:10px;height:70px;background:#08060a}
  #pianoleg2{position:absolute;left:300px;top:648px;width:10px;height:60px;background:#08060a}
  /* bar right */
  #bar{position:absolute;right:0;top:560px;width:360px;height:220px;background:linear-gradient(#2a1608,#160c04);border-radius:16px 0 0 0}
  .bottle{position:absolute;width:12px;border-radius:3px;background:linear-gradient(#e8a24a,#7a4a1e);opacity:.8}
  .pend{position:absolute;width:44px;height:56px;border-radius:0 0 40% 40%;background:radial-gradient(circle at 50% 30%,#ffcf82,#b0691f);
    box-shadow:0 0 26px 8px rgba(255,180,90,.5)}
  /* chandelier */
  #chand{position:absolute;left:57%;top:150px;transform:translateX(-50%);width:300px;height:420px;z-index:3}
  #chGlow{position:absolute;left:57%;top:180px;transform:translate(-50%,-50%);width:620px;height:620px;border-radius:50%;
    background:radial-gradient(circle,rgba(255,214,140,.5),rgba(255,180,90,.14) 40%,transparent 66%)}
  #chChain{position:absolute;left:57%;top:-150px;transform:translateX(-50%);width:4px;height:180px;background:linear-gradient(#8a6a2a,#c9a24a)}
  #chCrown{position:absolute;left:50%;top:24px;transform:translateX(-50%);width:230px;height:40px;border-radius:50%;
    background:linear-gradient(#f4d488,#c9922e);box-shadow:0 0 20px rgba(240,200,110,.6)}
  #chCone{position:absolute;left:50%;top:40px;transform:translateX(-50%);width:250px;height:300px;
    clip-path:polygon(50% 100%,4% 8%,96% 8%);
    background:radial-gradient(ellipse at 50% 20%,rgba(255,238,190,.9),rgba(240,190,110,.5) 40%,rgba(180,120,50,.25) 72%);filter:blur(.5px)}
  .cbead{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff3d0,#e0b060);opacity:0}
  .flame{position:absolute;width:8px;height:18px;border-radius:50% 50% 50% 50%/62% 62% 38% 38%;
    background:linear-gradient(#fff2cc,#ffbf5e 60%,#e0902a);box-shadow:0 0 12px 3px rgba(255,190,90,.7)}
  /* floor + reflections */
  #floor{position:absolute;left:0;top:56%;width:100%;height:44%;
    background:linear-gradient(#2a1708 0%,#1c0f06 34%,#160c04 70%,#0f0803 100%)}
  #floortex{position:absolute;left:0;top:56%;width:100%;height:44%;opacity:.14;pointer-events:none;
    background-image:repeating-linear-gradient(38deg,#e8a24a 0 2px,transparent 2px 16px),repeating-linear-gradient(-38deg,#e8a24a 0 2px,transparent 2px 16px)}
  .fref{position:absolute;top:0;width:46px;height:100%;filter:blur(7px);opacity:.5;
    background:linear-gradient(rgba(255,196,110,.6),transparent 78%)}
  /* foreground table: wine + candle */
  #table{position:absolute;right:120px;bottom:150px;width:520px;height:150px;border-radius:50%;
    background:radial-gradient(ellipse at 50% 30%,rgba(120,80,40,.5),rgba(30,18,8,.6) 70%);box-shadow:0 20px 50px rgba(0,0,0,.5)}
  .wine{position:absolute;width:96px;height:150px}
  .wbowl{position:absolute;left:8px;top:0;width:80px;height:104px;border-radius:46% 46% 50% 50%/40% 40% 60% 60%;
    background:linear-gradient(160deg,rgba(255,240,220,.12),rgba(180,150,120,.05));border:2px solid rgba(255,230,190,.28)}
  .wliq{position:absolute;left:14px;top:44px;width:68px;height:56px;border-radius:44% 44% 50% 50%/30% 30% 70% 70%;
    background:linear-gradient(#8a1a2a,#4a0e18);box-shadow:0 0 20px rgba(150,20,40,.5)}
  .whl{position:absolute;left:20px;top:10px;width:10px;height:70px;background:rgba(255,255,255,.22);border-radius:8px;filter:blur(1px)}
  .wstem{position:absolute;left:46px;top:100px;width:5px;height:36px;background:rgba(255,240,220,.3)}
  .wbase{position:absolute;left:30px;top:134px;width:38px;height:12px;border-radius:50%;background:rgba(255,240,220,.18)}
  #candle{position:absolute;width:70px;height:96px}
  #cholder{position:absolute;left:0;bottom:0;width:70px;height:74px;border-radius:8px;
    background:linear-gradient(rgba(255,220,160,.22),rgba(255,190,110,.12));border:2px solid rgba(255,220,160,.25);
    box-shadow:0 0 30px rgba(255,180,90,.5)}
  #cwax{position:absolute;left:20px;bottom:8px;width:30px;height:40px;background:#f0e2c0;border-radius:4px}
  #cflame{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);width:14px;height:30px;
    border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:linear-gradient(#fff6d8,#ffcf6b 46%,#e08a2a);
    box-shadow:0 0 30px 10px rgba(255,180,90,.7)}
  .mote{position:absolute;width:6px;height:6px;border-radius:50%;background:radial-gradient(circle,#ffe6b8,#e0a24a 60%,transparent 70%);opacity:0}
  #grain{position:absolute;inset:0;opacity:.09;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 88% at 50% 44%, transparent 46%, rgba(6,3,1,.82) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    text-align:center;padding:110px 70px 0;opacity:0;z-index:8}
  .scene.mid{justify-content:center;padding-top:0}
  .kick{font-size:28px;letter-spacing:.5em;color:#d8bd84;font-weight:500;text-transform:uppercase;margin-bottom:20px}
  .title{font-size:120px;line-height:1.14;font-weight:600;color:#eedcac;letter-spacing:.06em;
    text-shadow:0 2px 30px rgba(0,0,0,.85),0 0 46px rgba(230,190,120,.28)}
  .orn{display:flex;align-items:center;justify-content:center;gap:22px;margin:30px 0 18px;color:#c9ac72}
  .orn i{display:block;width:130px;height:1px;background:linear-gradient(90deg,transparent,#c9ac72,transparent)}
  .orn b{font-size:28px;color:#e6c98a}
  .artist{font-size:52px;letter-spacing:.28em;color:#e6d2a0;font-weight:500;text-shadow:0 2px 16px rgba(0,0,0,.8)}
  .rome{font-size:26px;letter-spacing:.46em;color:#c9ac72;margin-top:12px}
  .tag{margin-top:32px;font-size:28px;letter-spacing:.44em;color:#d8bd84;text-transform:uppercase}
  #bar2{position:absolute;left:0;bottom:0;height:6px;width:0;background:linear-gradient(90deg,#c9822a,#f0c078);opacity:.85;z-index:9}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(15,8,3,.86);backdrop-filter:blur(4px);z-index:20;gap:26px;padding:0 70px;text-align:center}
  #ui .k{font-size:26px;letter-spacing:.4em;color:#e6c98a;text-transform:uppercase}
  #ui h1{font-size:98px;font-weight:600;color:#eedcac;line-height:1.12;letter-spacing:.06em}
  #ui p{font-size:38px;letter-spacing:.24em;color:#e6d2a0}
  #play{font-family:'Noto Serif JP',serif;font-size:38px;font-weight:600;color:#160c04;background:#e6c98a;border:none;
    border-radius:100px;padding:26px 74px;cursor:pointer;letter-spacing:.14em;box-shadow:0 10px 40px rgba(230,201,138,.35)}
  #play:hover{background:#f2dca8}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  // chandelier: crystal beads over the cone + candle flames on the crown
  const chand=document.getElementById('chand'), BEAD=[];
  for(let r=0;r<9;r++){const y=48+r*30; const w=236*(1-r/10)-r*4; const n=Math.max(2,Math.round(w/18));
    for(let c=0;c<n;c++){const b=document.createElement('div');b.className='cbead';const sz=5+((r+c)%3)*3;
      b.style.width=sz+'px';b.style.height=sz+'px';b.style.left=(150 - w/2 + c*(w/(n-1||1)))+'px';b.style.top=y+'px';
      b.dataset.ph=((r*7+c*13)%100)/100;chand.appendChild(b);BEAD.push(b);}}
  const FL=[]; const nf=11; for(let i=0;i<nf;i++){const f=document.createElement('div');f.className='flame';
    const ang=(i/(nf-1))*Math.PI; const x=150 - Math.cos(ang)*116; const y=30 - Math.sin(ang)*10;
    f.style.left=x+'px';f.style.top=y+'px';f.dataset.ph=i*0.5;chand.appendChild(f);FL.push(f);}
  // bar bottles + pendants
  const bar=document.getElementById('bar');
  for(let i=0;i<12;i++){const b=document.createElement('div');b.className='bottle';b.style.right=(20+i*28)+'px';
    b.style.top=(10+((i%3)*10))+'px';b.style.height=(60+((i%3)*16))+'px';bar.appendChild(b);}
  [[880,370],[1010,410]].forEach((p,i)=>{const e=document.createElement('div');e.className='pend';
    e.style.left=p[0]+'px';e.style.top=p[1]+'px';e.dataset.ph=i;stage.appendChild(e);});
  const PEND=[...document.querySelectorAll('.pend')];
  // floor reflections (of chandelier, centered)
  const FR=[]; for(let i=0;i<9;i++){const e=document.createElement('div');e.className='fref';
    e.style.left=(376+i*56)+'px';e.dataset.ph=i*0.4;stage.appendChild(e);FR.push(e);}
  const MO=[]; for(let i=0;i<16;i++){const e=document.createElement('div');e.className='mote';
    e.style.left=((i*61)%100)+'%';e.dataset.dur=8+((i*47)%40)/10;e.dataset.ph=((i*31)%100)/100;stage.appendChild(e);MO.push(e);}
  const chGlow=document.getElementById('chGlow'),cflame=document.getElementById('cflame'),bar2=document.getElementById('bar2');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/860,(en-t)/580),0,1);}
  function flick(ts){return 0.9+0.1*(0.6*Math.sin(ts*6.2)+0.4*Math.sin(ts*10.4+1));}
  window.renderAt=function(t){
    const ts=t/1000, fl=flick(ts), waltz=Math.sin(ts*1.05); // ~3/4 gentle sway
    chand.style.transform=`translateX(-50%) rotate(${waltz*1.3}deg)`;
    chGlow.style.opacity=(0.8+0.2*Math.sin(ts/1.6)).toFixed(3);
    for(const b of BEAD){const ph=+b.dataset.ph;b.style.opacity=(0.45+0.5*(0.5+0.5*Math.sin(ts*2.4+ph*6.28))).toFixed(2);}
    for(const f of FL){const ph=+f.dataset.ph;f.style.transform=`scaleY(${1+0.14*Math.sin(ts*9+ph)}) translateX(${Math.sin(ts*6+ph)*1.2}px)`;}
    for(const p of PEND){p.style.opacity=(0.7+0.3*flick(ts+ +p.dataset.ph)).toFixed(2);}
    for(const r of FR){const ph=+r.dataset.ph;r.style.transform=`translateX(${waltz*10+Math.sin(ts*1.6+ph)*8}px) scaleX(${1+0.35*Math.sin(ts*2+ph)})`;
      r.style.opacity=(0.35+0.25*Math.sin(ts*1.8+ph)).toFixed(2)*fl;}
    cflame.style.transform=`translateX(-50%) scaleY(${1+0.16*Math.sin(ts*11)}) rotate(${Math.sin(ts*7)*3}deg)`;
    cflame.style.opacity=fl;
    for(const e of MO){const p=frac(ts/(+e.dataset.dur)+ +e.dataset.ph);e.style.top=(1780-p*1500)+'px';
      e.style.opacity=(Math.sin(p*Math.PI)*0.5*fl).toFixed(2);}
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    if(bar2) bar2.style.width=(clamp(t/total,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search), ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar2.style.display='none'; }
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
    (5200, '<div class="scene"><div class="kick">New Single</div></div>'),
    (8600, '<div class="scene" style="text-align:left;align-items:flex-start;padding-left:78px"><div class="title" style="font-size:100px">ほどける<br>夜のワルツ</div>'
           '<div class="orn"><i></i><b>&#10086;</b><i></i></div>'
           '<div class="artist">琥珀譲二</div><div class="rome">KOHAKU JOJI</div></div>'),
    (5400, '<div class="scene mid"><div class="orn" style="margin:0"><i></i><b>&#10086;</b><i></i></div></div>'),
    (8800, '<div class="scene" style="text-align:left;align-items:flex-start;padding-left:78px"><div class="title" style="font-size:100px">ほどける<br>夜のワルツ</div>'
           '<div class="orn"><i></i><b>&#10086;</b><i></i></div>'
           '<div class="artist">琥珀譲二</div><div class="rome">KOHAKU JOJI</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="ほどける夜のワルツ / 琥珀譲二 (Promo Short)",
  desc="シャンデリアの灯りとワインと。琥珀譲二の新曲「ほどける夜のワルツ」。",
  k="琥珀譲二 / KOHAKU JOJI", ep="ほどける夜のワルツ", tagline="Waltz")

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
  <div id="curtain"></div>
  <div id="spot"></div>
  <div id="stagefloor"></div>
  <div id="pianolid"></div>
  <div id="pianobody"></div>
  <div id="pianoleg"></div>
  <div id="pianoleg2"></div>
  <div id="bar"></div>
  <div id="floor"></div>
  <div id="floortex"></div>
  <div id="chGlow"></div>
  <div id="chChain"></div>
  <div id="chand"><div id="chCone"></div><div id="chCrown"></div></div>
  <div id="table"></div>
  <div class="wine" style="right:360px;bottom:236px"><div class="wbowl"></div><div class="wliq"></div><div class="whl"></div><div class="wstem"></div><div class="wbase"></div></div>
  <div class="wine" style="right:250px;bottom:210px"><div class="wbowl"></div><div class="wliq"></div><div class="whl"></div><div class="wstem"></div><div class="wbase"></div></div>
  <div id="candle" style="right:440px;bottom:180px"><div id="cholder"></div><div id="cwax"></div><div id="cflame"></div></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="vig"></div>
  <div id="bar2"></div>
  <div id="ui">
    <div class="k">琥珀譲二 &middot; KOHAKU JOJI</div>
    <h1>ほどける夜のワルツ</h1>
    <p>Waltz</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="hodokeru-waltz-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "hodokeru-waltz-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote hodokeru-waltz-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
