# -*- coding: utf-8 -*-
"""「シグナル / Signal」 — YouTube promo short (rock / glitch broadcast).
Code-only cinematic: night city rooftop, broadcast tower + radio waves, giant
audio waveform, shattering fake-news / vanity-metric fragments, lone guitarist.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
On-screen words are verified from the cover (title, 嘘くさいニュース, 10,000 / 1,000,000 / 0).
BGM: signal-bgm.mp3 (32s chorus segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#05070f;overflow:hidden}
  body{font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN',system-ui,sans-serif;color:#eef3ff;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:#05070f;box-shadow:0 0 120px rgba(0,0,0,.6)}
  #sky{position:absolute;left:0;top:0;width:100%;height:60%;
    background:linear-gradient(to bottom,#070a1a 0%,#0c1430 34%,#233258 54%,#7c5a3e 72%,#d1772a 86%,#f2a63e 96%)}
  .star{position:absolute;width:3px;height:3px;border-radius:50%;background:#dfe8ff;opacity:0}
  #sunglow{position:absolute;left:50%;top:58%;transform:translate(-50%,-50%);width:900px;height:340px;
    background:radial-gradient(ellipse at center, rgba(255,170,70,.55), rgba(255,120,50,.12) 46%, transparent 70%)}
  .win{position:absolute;width:3px;height:4px;background:#ffd98a;opacity:0}
  #skyline{position:absolute;left:0;top:52%;width:100%;height:12%;background:#060912;
    clip-path:polygon(0 60%,4% 60%,4% 36%,8% 36%,8% 62%,12% 62%,12% 28%,15% 28%,15% 58%,20% 58%,20% 42%,25% 42%,25% 64%,30% 64%,30% 22%,33% 22%,33% 56%,38% 56%,38% 38%,42% 38%,42% 64%,46% 64%,46% 30%,50% 30%,50% 60%,54% 60%,54% 20%,57% 20%,57% 58%,62% 58%,62% 40%,66% 40%,66% 64%,70% 64%,70% 32%,74% 32%,74% 58%,79% 58%,79% 44%,83% 44%,83% 64%,88% 64%,88% 34%,92% 34%,92% 60%,96% 60%,96% 40%,100% 40%,100% 100%,0 100%)}
  #tower{position:absolute;left:50%;top:25%;transform:translateX(-50%);width:150px;height:37%;
    background:linear-gradient(#0a0e1c,#05070f);
    clip-path:polygon(41% 0,59% 0,74% 100%,26% 100%);opacity:.96}
  #towerX{position:absolute;left:50%;top:25%;transform:translateX(-50%);width:150px;height:37%;opacity:.5;
    background:repeating-linear-gradient(20deg, transparent 0 14px, #0d1424 14px 16px),
               repeating-linear-gradient(-20deg, transparent 0 14px, #0d1424 14px 16px);
    clip-path:polygon(41% 0,59% 0,74% 100%,26% 100%)}
  #beacon{position:absolute;left:50%;top:25%;transform:translate(-50%,-50%);width:26px;height:26px;border-radius:50%;
    background:radial-gradient(circle,#fff,#ff4a3a 55%,#c0140a);box-shadow:0 0 30px 10px rgba(255,60,40,.8)}
  #beam{position:absolute;left:50%;top:0;transform:translateX(-50%);width:8px;height:25%;
    background:linear-gradient(to top, rgba(255,70,50,.85), rgba(255,70,50,0));filter:blur(1px)}
  .ring{position:absolute;left:50%;top:25%;transform:translate(-50%,-50%);border:2px solid rgba(120,190,255,.6);
    border-radius:50%;width:0;height:0}
  #wave{position:absolute;left:0;top:59%;width:100%;height:150px;transform:translateY(-50%);
    display:flex;align-items:center;justify-content:center;gap:5px;z-index:3}
  #wave .b{width:6px;height:10px;background:#eaf3ff;border-radius:3px;box-shadow:0 0 8px rgba(150,200,255,.7)}
  #frags{position:absolute;inset:0;z-index:2}
  .frag{position:absolute;font-family:'Noto Sans JP',system-ui,sans-serif;opacity:0;will-change:transform}
  .frag.news{width:150px;height:120px;background:#c9c3b4;box-shadow:0 4px 14px rgba(0,0,0,.5);padding:10px;
    transform-origin:center;overflow:hidden}
  .frag.news .t{font-size:15px;font-weight:700;color:#a2231a;border-bottom:2px solid #2a2a2a;padding-bottom:4px}
  .frag.news .l{height:5px;background:#5a564c;margin-top:7px;border-radius:1px}
  .frag.chip{display:flex;align-items:center;gap:10px;background:rgba(12,20,40,.82);border:1px solid rgba(150,190,255,.35);
    border-radius:12px;padding:12px 20px;font-size:34px;font-weight:800;color:#eef3ff;box-shadow:0 0 18px rgba(80,140,255,.25)}
  .frag.chip .ic{font-size:34px}
  .frag.chip.like .ic{color:#4a9bff}  .frag.chip.play .ic{color:#ff5a5a}  .frag.chip.heart .ic{color:#ff4d7d}
  #floor{position:absolute;left:0;bottom:0;width:100%;height:22%;
    background:linear-gradient(to bottom, #0a0d18 0%, #05070f 100%)}
  #floorbeam{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:60px;height:22%;
    background:linear-gradient(to bottom, rgba(255,80,60,.28), transparent);filter:blur(4px)}
  #figure{position:absolute;left:50%;bottom:20%;transform:translateX(-50%);width:150px;height:360px;background:#04050b;
    clip-path:polygon(41% 0,46% 2%,54% 2%,59% 0,62% 9%,60% 15%,66% 22%,72% 42%,66% 44%,60% 30%,60% 56%,64% 99%,54% 100%,50% 66%,46% 100%,36% 99%,40% 56%,40% 30%,34% 44%,28% 42%,34% 22%,40% 15%,38% 9%)}
  #guitar{position:absolute;left:calc(50% + 60px);bottom:8%;width:70px;height:230px;background:#04050b;
    border-radius:50% 50% 46% 46%/62% 62% 38% 38%;transform:rotate(12deg)}
  #guitar::before{content:"";position:absolute;left:44%;top:-150px;width:9px;height:170px;background:#04050b;border-radius:4px}
  #grain{position:absolute;inset:0;opacity:.08;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(120% 92% at 50% 46%, transparent 52%, rgba(2,3,8,.72) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    text-align:center;padding:96px 90px 0;opacity:0;z-index:6}
  .scene.mid{justify-content:center;padding-top:0}
  .kick{font-size:30px;letter-spacing:.5em;color:#7fb2ff;font-weight:700;text-transform:uppercase;margin-bottom:26px}
  .title{font-size:210px;line-height:.92;font-weight:900;color:#f2f6ff;letter-spacing:.02em;
    text-shadow:3px 0 rgba(255,40,60,.6), -3px 0 rgba(60,180,255,.6), 0 0 40px rgba(120,180,255,.35)}
  .sig{display:flex;align-items:center;justify-content:center;gap:22px;margin-top:22px;color:#dfe9ff}
  .sig i{display:block;width:120px;height:2px;background:linear-gradient(90deg,transparent,#7fb2ff,transparent)}
  .sig b{font-family:Georgia,serif;font-size:56px;font-weight:400;letter-spacing:.34em;text-transform:uppercase}
  .noise{display:flex;flex-wrap:wrap;gap:26px;align-items:center;justify-content:center;max-width:900px}
  .card{background:rgba(10,16,34,.8);border:1px solid rgba(150,190,255,.3);border-radius:14px;padding:20px 30px;
    font-size:46px;font-weight:800;display:flex;align-items:center;gap:14px;box-shadow:0 0 20px rgba(80,140,255,.2)}
  .card .ic{font-size:46px}
  .newsbig{background:#c9c3b4;color:#20201c;border-radius:4px;padding:22px 30px;transform:rotate(-3deg);
    box-shadow:0 12px 30px rgba(0,0,0,.5);max-width:640px}
  .newsbig .t{color:#a2231a;font-weight:800;font-size:44px;border-bottom:3px solid #2a2a2a;padding-bottom:10px;letter-spacing:.02em}
  .newsbig .s{font-size:26px;color:#4a463c;margin-top:12px;letter-spacing:.3em}
  .tag{margin-top:34px;font-size:30px;letter-spacing:.46em;color:#7fb2ff;text-transform:uppercase}
  #bar{position:absolute;left:0;bottom:0;height:7px;width:0;background:linear-gradient(90deg,#ff3b46,#7fb2ff);opacity:.9;z-index:9}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(5,7,15,.85);backdrop-filter:blur(4px);z-index:20;gap:34px;padding:0 96px;text-align:center}
  #ui .k{font-size:30px;letter-spacing:.44em;color:#7fb2ff;text-transform:uppercase}
  #ui h1{font-size:150px;font-weight:900;color:#f2f6ff;line-height:.9;text-shadow:3px 0 rgba(255,40,60,.6),-3px 0 rgba(60,180,255,.6)}
  #ui p{font-family:Georgia,serif;font-size:44px;letter-spacing:.3em;color:#aab8d8;text-transform:uppercase}
  #play{font-size:40px;font-weight:800;color:#05070f;background:#7fb2ff;border:none;border-radius:100px;
    padding:28px 78px;cursor:pointer;letter-spacing:.12em;text-transform:uppercase;box-shadow:0 10px 40px rgba(127,178,255,.4)}
  #play:hover{background:#a7c8ff}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  // stars
  const STAR=[]; for(let i=0;i<60;i++){const x=((i*47)%100)/100*1080,y=((i*71)%100)/100*760;
    const e=document.createElement('div');e.className='star';e.style.left=x+'px';e.style.top=y+'px';
    e.dataset.ph=((i*13)%100)/100;stage.appendChild(e);STAR.push(e);}
  // window lights (on skyline band)
  const WIN=[]; for(let i=0;i<80;i++){const x=((i*53)%100)/100*1080,y=1010+((i*37)%150);
    const e=document.createElement('div');e.className='win';e.style.left=x+'px';e.style.top=y+'px';
    e.dataset.ph=((i*29)%100)/100;stage.appendChild(e);WIN.push(e);}
  // rings from beacon
  const RING=[]; const ringWrap=stage;
  for(let k=0;k<4;k++){const r=document.createElement('div');r.className='ring';ringWrap.appendChild(r);RING.push(r);}
  // waveform bars
  const wave=document.getElementById('wave'), BARS=[];
  for(let i=0;i<84;i++){const b=document.createElement('div');b.className='b';wave.appendChild(b);BARS.push(b);}
  // media fragments
  const fragsWrap=document.getElementById('frags'), FR=[];
  const fragDefs=[
    {cls:'chip like',html:'<span class="ic">&#128077;</span>10,000',x:150,y:720},
    {cls:'chip play',html:'<span class="ic">&#9654;</span>1,000,000',x:820,y:700},
    {cls:'chip heart',html:'<span class="ic">&#9829;</span>0',x:250,y:470},
    {cls:'news',html:'<div class="t">嘘くさいニュース</div><div class="l"></div><div class="l"></div><div class="l" style="width:70%"></div>',x:60,y:170},
    {cls:'news',html:'<div class="t">FAKE</div><div class="l"></div><div class="l" style="width:60%"></div>',x:880,y:250},
    {cls:'chip like',html:'<span class="ic">&#128077;</span>10,000',x:900,y:520},
    {cls:'news',html:'<div class="t">嘘くさいニュース</div><div class="l"></div><div class="l" style="width:80%"></div>',x:120,y:560},
  ];
  fragDefs.forEach((d,i)=>{const e=document.createElement('div');e.className='frag '+d.cls;e.innerHTML=d.html;
    e.style.left=d.x+'px';e.style.top=d.y+'px';fragsWrap.appendChild(e);
    FR.push({e,x0:d.x,y0:d.y,ph:i*0.7,dx:(d.x<540?-1:1),spd:12+i*3});});
  const beam=document.getElementById('beam');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'), bar=document.getElementById('bar');
  let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/700,(en-t)/520),0,1);}
  const beaconY=0.25*1920;
  window.renderAt=function(t){
    const ts=t/1000;
    for(const e of STAR){const ph=+e.dataset.ph; e.style.opacity=(0.3+0.6*(0.5+0.5*Math.sin(ts*1.6+ph*6.28))).toFixed(2);}
    for(const e of WIN){const ph=+e.dataset.ph; e.style.opacity=(0.4+0.5*(0.5+0.5*Math.sin(ts*1.2+ph*6.28))).toFixed(2);}
    beam.style.opacity=(0.55+0.45*Math.abs(Math.sin(ts*6))).toFixed(2);
    document.getElementById('beacon').style.transform=`translate(-50%,-50%) scale(${1+0.25*Math.abs(Math.sin(ts*3))})`;
    // rings expand
    const maxR=760;
    RING.forEach((r,k)=>{const rr=frac(ts*0.35+k*0.25)*maxR; r.style.width=rr+'px';r.style.height=rr+'px';
      r.style.top=beaconY+'px'; r.style.borderColor=`rgba(120,190,255,${(0.55*(1-rr/maxR)).toFixed(3)})`;});
    // waveform: lively, center-weighted envelope
    for(let i=0;i<BARS.length;i++){const c=(i-BARS.length/2)/(BARS.length/2);
      const env=0.35+0.65*Math.cos(c*1.3);
      let h=Math.abs(Math.sin(i*0.5+ts*7)*Math.sin(i*0.17+ts*3.3)+0.5*Math.sin(i*0.9-ts*5));
      h=(14+h*150*env);BARS[i].style.height=h.toFixed(1)+'px';}
    // fragments drift outward + glitchy flicker
    for(const f of FR){const dx=f.dx*(Math.sin(ts*0.5+f.ph)*18+ts*f.spd% 60);
      const dy=Math.sin(ts*0.7+f.ph)*16 - (ts*4)% 40;
      const fl=Math.sin(ts*12+f.ph*3)>0.6?0.25:1;
      f.e.style.transform=`translate(${dx}px,${dy}px) rotate(${Math.sin(ts*0.6+f.ph)*10}deg)`;
      f.e.style.opacity=(clamp(ts/1.5,0,1)*0.9*fl).toFixed(2);}
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
    (4600, '<div class="scene mid"><div class="noise">'
           '<div class="newsbig"><div class="t">嘘くさいニュース</div><div class="s">FAKE&nbsp;NEWS</div></div>'
           '<div class="card"><span class="ic" style="color:#4a9bff">&#128077;</span>10,000</div>'
           '<div class="card"><span class="ic" style="color:#ff5a5a">&#9654;</span>1,000,000</div>'
           '<div class="card"><span class="ic" style="color:#ff4d7d">&#9829;</span>0</div>'
           '</div></div>'),
    (7800, '<div class="scene"><div class="kick">New Single</div>'
           '<div class="title">シグナル</div>'
           '<div class="sig"><i></i><b>Signal</b><i></i></div></div>'),
    (6600, '<div class="scene mid">'
           '<div style="font-family:Georgia,serif;font-weight:400;font-size:176px;letter-spacing:.16em;color:#f2f6ff;'
           'text-shadow:3px 0 rgba(255,40,60,.55),-3px 0 rgba(60,180,255,.55)">SIGNAL</div>'
           '<div class="sig"><i></i><b>シグナル</b><i></i></div></div>'),
    (9200, '<div class="scene"><div class="title">シグナル</div>'
           '<div class="sig"><i></i><b>Signal</b><i></i></div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(
  title="シグナル / Signal (Promo Short)",
  desc="ノイズだらけの世界に、ひとつの信号を。ロック・シングル「シグナル / Signal」。",
  k="Signal", ep="シグナル", tagline="Signal")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@700;800;900&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sky"></div>
  <div id="sunglow"></div>
  <div id="skyline"></div>
  <div id="towerX"></div>
  <div id="tower"></div>
  <div id="beam"></div>
  <div id="beacon"></div>
  <div id="frags"></div>
  <div id="wave"></div>
  <div id="floor"></div>
  <div id="floorbeam"></div>
  <div id="figure"></div>
  <div id="guitar"></div>
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
<audio id="bgm" src="signal-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "signal-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote signal-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
