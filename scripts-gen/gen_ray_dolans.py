# -*- coding: utf-8 -*-
"""Ray Dolan's Street "Rolling all stars" — YouTube promo short (heartland rock).
Code-only cinematic: dusk city street concert, crowd, neon, protest placards.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
All on-screen words are verified from the album cover (title, subtitle, the placard slogans).
BGM: ray-dolans-street-bgm.mp3 (34s chorus segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#08070c;overflow:hidden}
  body{font-family:'Roboto Slab','Rockwell',Georgia,'Times New Roman',serif;color:#f3e9d2;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:#08070c;box-shadow:0 0 120px rgba(0,0,0,.6)}
  #sky{position:absolute;left:0;top:0;width:100%;height:62%;
    background:linear-gradient(to bottom,#141428 0%,#241f39 30%,#5b3350 52%,#a4482f 74%,#d9772f 88%,#f0a martn 100%)}
  #sky{background:linear-gradient(to bottom,#141428 0%,#241f39 30%,#5b3350 52%,#a4482f 74%,#d9772f 88%,#f2b25a 100%)}
  #sunset{position:absolute;left:0;top:40%;width:100%;height:26%;
    background:radial-gradient(60% 100% at 50% 100%, rgba(255,170,70,.6), rgba(255,120,50,.2) 45%, transparent 70%)}
  #sun{position:absolute;left:50%;top:60%;transform:translate(-50%,-50%);width:120px;height:120px;border-radius:50%;
    background:radial-gradient(circle,#ffe6a6 0%,#ffb44e 45%,#e5731f 68%,rgba(229,115,31,0) 74%)}
  #skyline{position:absolute;left:0;top:46%;width:100%;height:16%;background:#0b0a14;
    clip-path:polygon(0 40%,4% 40%,4% 22%,8% 22%,8% 46%,13% 46%,13% 30%,16% 30%,16% 14%,20% 14%,20% 48%,26% 48%,26% 26%,30% 26%,30% 44%,34% 44%,34% 18%,37% 18%,37% 40%,42% 40%,42% 8%,45% 8%,45% 40%,50% 40%,50% 24%,54% 24%,54% 46%,59% 46%,59% 16%,62% 16%,62% 42%,67% 42%,67% 28%,71% 28%,71% 12%,74% 12%,74% 44%,79% 44%,79% 22%,83% 22%,83% 46%,88% 46%,88% 30%,92% 30%,92% 18%,96% 18%,96% 42%,100% 42%,100% 100%,0 100%)}
  .win{position:absolute;width:4px;height:5px;background:#ffd98a;opacity:.0;border-radius:1px}
  .neon{position:absolute;top:50%;width:150px;height:56px;border-radius:8px;filter:blur(1px);
    box-shadow:0 0 26px 6px rgba(214,52,40,.6);background:linear-gradient(#e0473a,#a52016);opacity:.0}
  #neonL{left:70px}  #neonR{right:70px;background:linear-gradient(#ff5a48,#c11d15)}
  #stagelt{position:absolute;left:50%;top:60%;transform:translate(-50%,-50%);width:640px;height:300px;
    background:radial-gradient(ellipse at center, rgba(255,196,120,.35), transparent 68%)}
  #crowd{position:absolute;left:0;bottom:0;width:100%;height:31%;background:linear-gradient(to bottom,#07060b 0%,#050409 100%);
    clip-path:polygon(0 22%,3% 12%,6% 20%,9% 9%,12% 19%,15% 7%,18% 18%,21% 10%,24% 20%,27% 8%,30% 17%,33% 6%,36% 18%,39% 11%,42% 20%,45% 7%,48% 16%,51% 9%,54% 19%,57% 8%,60% 17%,63% 10%,66% 20%,69% 7%,72% 18%,75% 9%,78% 19%,81% 8%,84% 17%,87% 11%,90% 20%,93% 8%,96% 18%,100% 12%,100% 100%,0 100%)}
  .arm{position:absolute;bottom:24%;width:8px;background:#040308;border-radius:4px;transform-origin:bottom center}
  .arm::after{content:"";position:absolute;top:-16px;left:50%;transform:translateX(-50%);width:20px;height:20px;
    border-radius:50%;background:#040308}
  .sign{position:absolute;bottom:26%;width:74px;height:56px;background:#d9cfb4;transform:rotate(-6deg);
    box-shadow:0 4px 10px rgba(0,0,0,.5);border:2px solid #b7ac8e}
  .sign i{position:absolute;left:10px;right:10px;top:12px;height:5px;background:#b23127;box-shadow:0 12px 0 #4a4a52,0 24px 0 #4a4a52}
  #embers{position:absolute;inset:0;pointer-events:none}
  .ember{position:absolute;width:6px;height:6px;border-radius:50%;
    background:radial-gradient(circle,#ffddا0,#e0902a 60%,transparent 70%);
    background:radial-gradient(circle,#ffdda0,#e0902a 60%,transparent 70%);opacity:0}
  #grain{position:absolute;inset:0;opacity:.09;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(120% 92% at 50% 44%, transparent 52%, rgba(6,5,10,.66) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:0 100px;opacity:0}
  .scene.top{justify-content:flex-start;padding-top:150px}
  /* held protest placard */
  .placard{background:#e7ddc4;color:#20222b;border:3px solid #c3b896;border-radius:4px;padding:44px 52px;
    box-shadow:0 18px 40px rgba(0,0,0,.55);transform:rotate(-2.5deg);max-width:820px;
    font-family:'Oswald','Arial Narrow','Helvetica Neue',system-ui,sans-serif;font-weight:700;text-transform:uppercase}
  .placard.r2{transform:rotate(2deg)}
  .placard .big{font-size:96px;line-height:1.02;letter-spacing:.01em;display:block}
  .placard .md{font-size:64px;line-height:1.12;letter-spacing:.01em;display:block}
  .placard .sm{font-size:52px;line-height:1.16;display:block}
  .placard em{color:#bd2f22;font-style:normal}
  .placard .tape{position:absolute;left:50%;top:-16px;transform:translateX(-50%) rotate(3deg);
    width:120px;height:34px;background:rgba(220,210,180,.55);box-shadow:0 2px 6px rgba(0,0,0,.3)}
  /* title */
  .title{font-family:'Roboto Slab','Rockwell',Georgia,serif;font-weight:800;font-size:138px;line-height:.92;
    letter-spacing:.005em;color:#f4ecd6;text-transform:uppercase;text-shadow:0 4px 26px rgba(0,0,0,.6)}
  .rule{display:flex;align-items:center;justify-content:center;gap:20px;margin:26px 0 6px;color:#c23327}
  .rule i{display:block;width:150px;height:3px;background:currentColor;opacity:.85}
  .rule b{font-size:34px}
  .script{font-family:'Brush Script MT','Segoe Script',Georgia,serif;font-style:italic;font-size:88px;color:#cf3a2e;
    text-shadow:0 3px 18px rgba(0,0,0,.55);letter-spacing:.01em}
  .tag{margin-top:40px;font-family:'Oswald','Arial Narrow',system-ui,sans-serif;font-size:30px;letter-spacing:.42em;
    color:#e7d9b8;text-transform:uppercase}
  #bar{position:absolute;left:0;bottom:0;height:7px;width:0;background:linear-gradient(90deg,#c23327,#f2b25a);opacity:.9;z-index:8}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(8,7,12,.85);backdrop-filter:blur(4px);z-index:20;gap:34px;padding:0 100px;text-align:center}
  #ui .k{font-family:'Oswald',system-ui,sans-serif;font-size:30px;letter-spacing:.4em;color:#cf3a2e;text-transform:uppercase}
  #ui h1{font-family:'Roboto Slab',Georgia,serif;font-size:104px;font-weight:800;color:#f4ecd6;line-height:.95;text-transform:uppercase}
  #ui p{font-family:'Brush Script MT',Georgia,serif;font-style:italic;font-size:44px;color:#cf3a2e}
  #play{font-family:'Oswald',system-ui,sans-serif;font-size:40px;font-weight:700;color:#1a0f0c;background:#f2b25a;border:none;
    border-radius:100px;padding:28px 78px;cursor:pointer;letter-spacing:.12em;text-transform:uppercase;box-shadow:0 10px 40px rgba(242,178,90,.4)}
  #play:hover{background:#ffca7a}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage');
  // window lights on skyline
  const WIN=[]; for(let i=0;i<70;i++){const x=((i*53)%100)/100*1080, y=890+((i*37)%110);
    const w=document.createElement('div');w.className='win';w.style.left=x+'px';w.style.top=y+'px';
    w.dataset.ph=((i*17)%100)/100;stage.appendChild(w);WIN.push(w);}
  // raised arms + a couple of held signs in the crowd
  const ARMS=[]; const ax=[90,180,300,430,560,690,820,930,1000,250,760];
  ax.forEach((x,i)=>{const a=document.createElement('div');a.className='arm';
    a.style.left=x+'px';a.style.height=(90+ (i%4)*30)+'px';a.dataset.ph=(i*0.6);a.dataset.amp=(3+i%3);
    stage.appendChild(a);ARMS.push(a);});
  [[360,'-6deg'],[720,'5deg']].forEach((s,i)=>{const g=document.createElement('div');g.className='sign';
    g.style.left=s[0]+'px';g.style.transform='rotate('+s[1]+')';g.innerHTML='<i></i>';
    g.dataset.ph=(i*1.3);stage.appendChild(g);ARMS.push({el:g,sign:true,ph:i*1.3});});
  // embers
  const emC=document.getElementById('embers'), EM=[];
  for(let i=0;i<22;i++){const x=((i*137.5)%100)/100*1080,dur=6+((i*53)%50)/10,phase=((i*29)%100)/100;
    const e=document.createElement('div');e.className='ember';e.style.left=x+'px';emC.appendChild(e);EM.push({e,dur,phase});}
  const sun=document.getElementById('sun'),sunset=document.getElementById('sunset'),
        neonL=document.getElementById('neonL'),neonR=document.getElementById('neonR'),
        stagelt=document.getElementById('stagelt'),bar=document.getElementById('bar');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/780,(en-t)/560),0,1);}
  window.renderAt=function(t){
    const ts=t/1000;
    sun.style.opacity=clamp(ts/1.2,0,1);
    sunset.style.opacity=(0.85+0.15*Math.sin(ts/2.4)).toFixed(3);
    stagelt.style.opacity=(0.7+0.3*Math.abs(Math.sin(ts/0.7))).toFixed(3);   // stage lights flicker to beat
    const np=0.55+0.45*Math.abs(Math.sin(ts/0.9+0.4));
    neonL.style.opacity=(0.5+0.5*Math.abs(Math.sin(ts/1.1))).toFixed(3);
    neonR.style.opacity=np.toFixed(3);
    for(const w of WIN){const ph=+w.dataset.ph; w.style.opacity=(0.35+0.5*(0.5+0.5*Math.sin(ts*1.3+ph*6.28))).toFixed(2);}
    for(const a of ARMS){ if(a.sign){a.el.style.transform=`rotate(${(a.ph<1?-6:5)+2*Math.sin(ts*2+a.ph)}deg) translateY(${Math.sin(ts*2+a.ph)*4}px)`;continue;}
      const ph=+a.dataset.ph, amp=+a.dataset.amp;
      a.style.transform=`translateY(${Math.sin(ts*2.4+ph)*amp - Math.max(0,Math.sin(ts*1.1+ph))*10}px) rotate(${Math.sin(ts*1.6+ph)*3}deg)`;}
    for(const m of EM){const prog=frac((ts)/m.dur+m.phase);
      m.e.style.top=(1560-prog*1500)+'px';m.e.style.transform=`scale(${0.6+prog*0.7})`;
      m.e.style.opacity=(Math.sin(prog*Math.PI)*0.7).toFixed(2);}
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
    (4200, '<div class="scene"><div class="placard"><span class="tape"></span>'
           '<span class="md">The whole town&rsquo;s</span><span class="big">coming out</span><span class="md">tonight</span></div></div>'),
    (7200, '<div class="scene top"><div class="title">Ray Dolan&rsquo;s<br>Street</div>'
           '<div class="rule"><i></i><b>&#9733;</b><i></i></div>'
           '<div class="script">Rolling all stars</div></div>'),
    (5200, '<div class="scene"><div class="placard r2"><span class="tape"></span>'
           '<span class="md">There&rsquo;s more</span><span class="big">of us</span><span class="md">than them</span></div></div>'),
    (6400, '<div class="scene"><div class="placard"><span class="tape"></span>'
           '<span class="sm"><em>Not</em> for me, not for you</span>'
           '<span class="sm"><em>for the kids</em></span>'
           '<span class="sm">who ain&rsquo;t been born yet</span></div></div>'),
    (6600, '<div class="scene top"><div class="title">Ray Dolan&rsquo;s<br>Street</div>'
           '<div class="rule"><i></i><b>&#9733;</b><i></i></div>'
           '<div class="script">Rolling all stars</div>'
           '<div class="tag">New Album</div></div>'),
]

meta = dict(
  title="Ray Dolan's Street — Rolling all stars (Promo Short)",
  desc="The whole town's coming out tonight. Ray Dolan's Street — 'Rolling all stars'. Heartland rock for the kids who ain't been born yet.",
  k="Ray Dolan's Street", ep="Rolling all stars", tagline="the whole town's coming out tonight.")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700;800&family=Oswald:wght@600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sky"></div>
  <div id="sunset"></div>
  <div id="sun"></div>
  <div id="skyline"></div>
  <div id="neonL" class="neon"></div>
  <div id="neonR" class="neon"></div>
  <div id="stagelt"></div>
  <div id="crowd"></div>
  <div id="embers"></div>
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
<audio id="bgm" src="ray-dolans-street-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "ray-dolans-street-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote ray-dolans-street-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
