# -*- coding: utf-8 -*-
"""Noah Vale "We Are Still Here" — YouTube promo short (folk / Americana sunrise).
Code-only cinematic: misty lake sunrise (echoing the cover), elegant type, song BGM.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
All on-screen text is verified from the album cover (title, artist, taglines, cat#).
BGM: we-are-still-here-bgm.mp3 (34s segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  :root{
    --cream:#f6efe1; --slate:#7c9cб0; --slate:#7c9cb0; --ink:#26343f; --gold:#f4c06a; --sky:#a9c0cf;
  }
  html,body{height:100%;background:#0c1418;overflow:hidden}
  body{font-family:'Oswald','Bebas Neue','Arial Narrow','Helvetica Neue',system-ui,sans-serif;
    color:var(--cream);display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:#0c1418;box-shadow:0 0 120px rgba(0,0,0,.6)}
  /* --- sky & water --- */
  #sky{position:absolute;left:0;top:0;width:100%;height:63%;
    background:linear-gradient(to bottom,#93b2c6 0%,#acc 22%,#c9d4d0 46%,#e6d3a8 74%,#f7d99f 90%,#fbe6b0 100%)}
  #water{position:absolute;left:0;top:63%;width:100%;height:37%;
    background:linear-gradient(to bottom,#f3d69a 0%,#d9b98a 8%,#7f9aa6 34%,#557485 62%,#3c586a 100%)}
  #sun{position:absolute;left:58%;top:63%;transform:translate(-50%,-50%);width:150px;height:150px;border-radius:50%;
    background:radial-gradient(circle,#fffefb 0%,#fff2cf 42%,#ffd982 66%,rgba(255,196,100,0) 74%)}
  #glow{position:absolute;left:58%;top:63%;transform:translate(-50%,-50%);width:900px;height:640px;border-radius:50%;
    background:radial-gradient(ellipse at center, rgba(255,221,150,.55), rgba(255,214,140,.18) 40%, transparent 66%)}
  #refl{position:absolute;left:58%;top:63%;transform:translateX(-50%);width:150px;height:520px;
    background:linear-gradient(to bottom, rgba(255,236,180,.75), rgba(255,220,150,.16) 60%, transparent);
    filter:blur(3px);mix-blend-mode:screen}
  .shore{position:absolute;top:47%;height:16.5%;width:44%;background:#243642;filter:blur(.4px)}
  #shoreL{left:0;clip-path:polygon(0 100%,0 62%,6% 55%,12% 66%,18% 44%,24% 60%,30% 40%,37% 58%,44% 34%,52% 62%,60% 48%,70% 70%,82% 60%,100% 78%,100% 100%)}
  #shoreR{right:0;clip-path:polygon(0 82%,14% 66%,26% 76%,38% 52%,50% 70%,60% 44%,68% 64%,76% 40%,83% 62%,89% 50%,94% 66%,100% 58%,100% 100%,0 100%)}
  .mist{position:absolute;height:70px;width:130%;left:-15%;border-radius:50%;
    background:radial-gradient(ellipse at center, rgba(244,248,248,.55), transparent 70%);filter:blur(9px)}
  .bird{position:absolute;width:30px;height:14px}
  .bird::before,.bird::after{content:"";position:absolute;top:4px;width:17px;height:3px;background:#2c3b45;border-radius:3px}
  .bird::before{left:0;transform:rotate(20deg);transform-origin:right center}
  .bird::after{right:0;transform:rotate(-20deg);transform-origin:left center}
  #grain{position:absolute;inset:0;opacity:.06;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(120% 90% at 50% 42%, transparent 55%, rgba(8,16,20,.5) 100%)}
  /* --- text scenes --- */
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:0 120px;opacity:0}
  .scene.low{justify-content:flex-end;padding-bottom:360px}
  .scene.top{justify-content:flex-start;padding-top:172px}
  .whisper{font-family:Georgia,'Times New Roman',serif;font-style:italic;font-size:62px;line-height:1.5;color:#fbf4e6;
    text-shadow:0 2px 24px rgba(20,30,38,.5);letter-spacing:.01em}
  .kick{font-size:34px;letter-spacing:.5em;font-weight:600;color:#5c7a8e;text-shadow:0 2px 14px rgba(255,255,255,.4);
    text-transform:uppercase;margin-bottom:34px}
  .artist{font-size:46px;letter-spacing:.42em;font-weight:600;color:#4f7189;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(255,255,255,.45);margin-bottom:24px}
  .title{font-size:132px;line-height:.96;font-weight:700;letter-spacing:.02em;color:#223440;text-transform:uppercase;
    transform:scaleX(.9);text-shadow:0 3px 22px rgba(255,255,255,.4)}
  .rule{display:flex;align-items:center;justify-content:center;gap:22px;margin-top:34px;color:#3a5568}
  .rule i{display:block;width:120px;height:2px;background:currentColor;opacity:.7}
  .rule b{font-size:30px;letter-spacing:.3em}
  .sub{font-family:Georgia,serif;font-style:italic;font-size:56px;line-height:1.5;color:#fbf4e6;
    text-shadow:0 2px 22px rgba(20,30,38,.55)}
  .reprise{font-family:Georgia,serif;font-style:italic;font-size:100px;line-height:1.1;color:#fdf7ea;
    text-shadow:0 3px 30px rgba(18,28,36,.6)}
  .cat{margin-top:38px;font-size:28px;letter-spacing:.4em;color:#3a5568;text-shadow:0 2px 12px rgba(255,255,255,.4)}
  #bar{position:absolute;left:0;bottom:0;height:7px;width:0;background:linear-gradient(90deg,#f4c06a,#fbe6b0);opacity:.85;z-index:6}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,18,22,.82);backdrop-filter:blur(4px);z-index:20;gap:36px;padding:0 120px;text-align:center}
  #ui .k{font-size:30px;letter-spacing:.42em;color:#f4c06a;text-transform:uppercase}
  #ui h1{font-size:96px;font-weight:700;color:#fbf4e6;line-height:1.05;text-transform:uppercase;transform:scaleX(.9)}
  #ui p{font-family:Georgia,serif;font-style:italic;font-size:38px;color:#cfd8d0}
  #play{font-size:40px;font-weight:600;color:#12202a;background:#f4c06a;border:none;border-radius:100px;
    padding:28px 78px;cursor:pointer;letter-spacing:.14em;text-transform:uppercase;box-shadow:0 10px 40px rgba(244,192,106,.4)}
  #play:hover{background:#fbe6b0}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), sun=document.getElementById('sun'),
        glow=document.getElementById('glow'), refl=document.getElementById('refl');
  // mist bands
  const MIST=[]; const mistY=[1120,1180,1250,1330];
  mistY.forEach((y,i)=>{const m=document.createElement('div');m.className='mist';m.style.top=y+'px';
    stage.appendChild(m);MIST.push({m,y,spd:8+i*5,ph:i*0.5});});
  // birds (upper-right flock, drifting left like the cover)
  const BIRDS=[]; const bp=[[760,300],[820,340],[700,360],[880,300],[790,400],[660,410]];
  bp.forEach((p,i)=>{const b=document.createElement('div');b.className='bird';stage.appendChild(b);
    BIRDS.push({b,x0:p[0],y0:p[1],spd:10+ (i%3)*4,amp:10+i*2,ph:i*0.7,sc:.7+ (i%3)*0.18});});
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'), bar=document.getElementById('bar');
  let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/800,(en-t)/600),0,1);}
  window.renderAt=function(t){
    const ts=t/1000;
    // sun slow rise + glow breathe
    const rise=clamp(ts/14,0,1)*26;
    sun.style.top=(63*19.2 - rise)+'px';
    glow.style.top=(63*19.2 - rise)+'px';
    refl.style.top=(63*19.2 - rise)+'px';
    const br=1+0.05*Math.sin(ts/2.2);
    sun.style.transform=`translate(-50%,-50%) scale(${br})`;
    glow.style.opacity=(0.8+0.2*Math.sin(ts/2.6)).toFixed(3);
    refl.style.transform=`translateX(-50%) scaleX(${1+0.14*Math.sin(ts/1.3)})`;
    refl.style.opacity=(0.7+0.3*Math.abs(Math.sin(ts/1.7))).toFixed(3);
    // mist drift (seamless wrap)
    for(const o of MIST){const dx=((ts*o.spd)% 300)-150; o.m.style.transform=`translateX(${dx}px)`;
      o.m.style.opacity=(0.5+0.3*Math.sin(ts/3+o.ph)).toFixed(3);}
    // birds
    for(const o of BIRDS){let x=o.x0 - ts*o.spd; x=((x+200)% 1500)-200;
      const y=o.y0 + Math.sin(ts/2+o.ph)*o.amp;
      o.b.style.transform=`translate(${x}px,${y}px) scale(${o.sc})`;
      o.b.style.opacity=(0.55+0.25*Math.sin(ts/2.5+o.ph)).toFixed(2);}
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
    (4800, '<div class="scene low"><div class="whisper">the morning belongs<br>to all of us.</div></div>'),
    (7200, '<div class="scene top"><div class="kick">New Single</div>'
           '<div class="artist">Noah Vale</div>'
           '<div class="title">We Are<br>Still Here</div>'
           '<div class="rule"><i></i><b>&#9733;</b><i></i></div></div>'),
    (6000, '<div class="scene low"><div class="sub">Songs for the morning<br>we build together.</div></div>'),
    (6000, '<div class="scene low"><div class="reprise">We are<br>still here.</div></div>'),
    (6000, '<div class="scene top"><div class="artist">Noah Vale</div>'
           '<div class="title">We Are<br>Still Here</div>'
           '<div class="cat">NEW SINGLE &nbsp;&#9733;&nbsp; NV&mdash;01</div></div>'),
]

meta = dict(
  title="Noah Vale — We Are Still Here (Promo Short)",
  desc="The morning belongs to all of us. New single 'We Are Still Here' by Noah Vale — songs for the morning we build together.",
  k="Noah Vale", ep="We Are Still Here", tagline="the morning belongs to all of us.")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = ENGINE.replace("SCENES", scenes_js)
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sky"></div>
  <div id="glow"></div>
  <div id="shoreL" class="shore"></div>
  <div id="shoreR" class="shore"></div>
  <div id="water"></div>
  <div id="refl"></div>
  <div id="sun"></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="vig"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">{meta['k']}</div>
    <h1>{meta['ep']}</h1>
    <p>{meta['tagline']}</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="we-are-still-here-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "we-are-still-here-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote we-are-still-here-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
