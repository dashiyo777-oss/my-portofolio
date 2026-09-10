# -*- coding: utf-8 -*-
"""「Put It Back / Rolloing all stars」 — promo short (vertical 9:16, ~26s).

A hopeful golden-hour Americana piece matching the cover: a dusk sky over layered
mountain ridges and a lake, the sun setting on the horizon with god-rays and a
shimmering reflection, pine silhouettes and a rocky overlook in the foreground,
warm embers drifting up, and a sun-flare bloom on the emotional payoff. A small
Earth emblem (from the cover's sticker) appears on the title card.

On-screen text is limited to verified cover text (title / artist / the cover's own
tagline "Music for a Brighter Tomorrow") plus generic labels and evocative promo
copy — no invented lyrics.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL for frame capture.
BGM: putitback-bgm.mp3 (30s from 2:30, the final-chorus climax).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CSS = r"""
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:100%;height:100%;background:#0a1020;overflow:hidden}
  #wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0a1020}
  #stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform:scale(var(--s,1));transform-origin:center center;
    font-family:'Noto Serif JP',serif;background:#0a1020}
  #world{position:absolute;inset:0;transform-origin:52% 46%}
  /* sky + lake */
  #sky{position:absolute;left:0;top:0;width:1080px;height:1012px;
    background:linear-gradient(180deg,#122a55 0%,#22436e 22%,#48597a 42%,#8a5c46 60%,#d5762f 76%,#ff9f42 88%,#ffd987 100%)}
  #lake{position:absolute;left:0;top:1000px;width:1080px;height:600px;
    background:linear-gradient(180deg,#ffd383 0%,#e79746 7%,#9a7350 22%,#3f4f68 55%,#1d2b45 100%)}
  #haze{position:absolute;left:0;top:860px;width:1080px;height:220px;pointer-events:none;
    background:linear-gradient(180deg,transparent,rgba(255,200,120,.5) 60%,rgba(255,220,150,.75) 78%,transparent);filter:blur(6px)}
  /* clouds */
  .cloud{position:absolute;border-radius:50%;opacity:.5;filter:blur(18px);
    background:radial-gradient(ellipse at 42% 40%, rgba(255,220,170,.7), rgba(255,180,120,.18) 60%, transparent 76%)}
  /* sun */
  #sunglow{position:absolute;left:596px;top:948px;width:760px;height:760px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(255,244,214,.95) 0%, rgba(255,206,120,.7) 22%, rgba(255,168,80,.3) 46%, transparent 70%)}
  #rays{position:absolute;left:596px;top:948px;width:1300px;height:1300px;transform:translate(-50%,-50%);border-radius:50%;
    opacity:.5;mix-blend-mode:screen;pointer-events:none;filter:blur(2px);
    background:repeating-conic-gradient(from 0deg at 50% 50%, rgba(255,236,190,.55) 0deg 2.4deg, transparent 2.4deg 12deg);
    -webkit-mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 11%, #000 26%, transparent 46%);
    mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 11%, #000 26%, transparent 46%)}
  #sun{position:absolute;left:596px;top:948px;width:150px;height:150px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle,#fffefb 0%,#fff2cf 40%,#ffd987 74%,#ffbf63 100%);
    box-shadow:0 0 90px 40px rgba(255,214,130,.7)}
  #sunref{position:absolute;left:596px;top:1006px;width:150px;height:470px;transform:translateX(-50%);pointer-events:none;
    background:linear-gradient(180deg, rgba(255,226,150,.85), rgba(255,196,110,.3) 40%, rgba(255,180,90,.08) 100%);
    filter:blur(5px);mix-blend-mode:screen}
  /* mountain ridges */
  .ridge{position:absolute;left:0;width:1080px}
  #rg1{top:812px;height:210px;background:#3a4d6b;opacity:.72;
    clip-path:polygon(0 62%,10% 46%,20% 56%,30% 34%,42% 52%,54% 30%,66% 50%,78% 36%,88% 54%,100% 42%,100% 100%,0 100%)}
  #rg2{top:846px;height:190px;background:#2b3c58;opacity:.86;
    clip-path:polygon(0 54%,14% 66%,26% 40%,38% 60%,50% 42%,60% 62%,72% 44%,84% 64%,94% 48%,100% 60%,100% 100%,0 100%)}
  #rg3{top:900px;height:150px;background:#1e2c44;
    clip-path:polygon(0 70%,12% 54%,24% 72%,36% 56%,48% 74%,58% 58%,70% 76%,82% 60%,92% 74%,100% 62%,100% 100%,0 100%)}
  /* foreground: rocky overlook + pines */
  #fg{position:absolute;left:0;bottom:0;width:1080px;height:280px;background:#0c1019;z-index:6;
    clip-path:polygon(0 46%,14% 30%,30% 40%,48% 24%,66% 38%,82% 26%,100% 40%,100% 100%,0 100%)}
  .pine{position:absolute;bottom:150px;background:#0c1019;z-index:6;
    clip-path:polygon(50% 0,60% 20%,54% 20%,66% 42%,58% 42%,72% 66%,56% 66%,56% 100%,44% 100%,44% 66%,28% 66%,42% 42%,34% 42%,46% 20%,40% 20%)}
  /* particles */
  .ember{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffe6ac,#f6a52c 55%,transparent 74%);opacity:0;z-index:7}
  .glim{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff6de,#ffd27a 50%,transparent 72%);opacity:0;z-index:5}
  /* bloom + grade */
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(120% 78% at 55% 50%, rgba(255,244,214,.96), rgba(255,214,140,.72) 38%, rgba(255,180,95,.34) 68%, rgba(255,150,70,.1) 100%)}
  #grain{position:absolute;inset:0;opacity:.05;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 52% 44%, transparent 48%, rgba(8,10,22,.72) 100%)}
  /* text */
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
    text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:452px 84px 0}
  .scene.low{justify-content:flex-end;padding:0 84px 316px}
  .kick{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:.5em;color:#fff0d2;text-transform:uppercase;
    text-shadow:0 2px 20px rgba(10,14,30,.95)}
  .jp{font-size:70px;line-height:1.62;font-weight:600;color:#fff6e6;letter-spacing:.06em;
    text-shadow:0 2px 24px rgba(8,12,26,.98),0 0 44px rgba(20,20,40,.6)}
  .jp .em{color:#ffd77e}
  .big{font-size:96px;line-height:1.28;font-weight:600;color:#fff;letter-spacing:.05em;display:inline-block;
    text-shadow:0 3px 26px rgba(10,12,28,1),0 0 56px rgba(255,206,120,.5)}
  .title{font-family:'Anton',sans-serif;font-size:134px;line-height:.96;color:#fff5e4;letter-spacing:.03em;text-transform:uppercase;
    text-shadow:0 4px 2px rgba(0,0,0,.35),0 6px 40px rgba(8,10,24,.9),0 0 60px rgba(255,206,120,.4)}
  .artist{font-family:'Anton',sans-serif;font-size:40px;letter-spacing:.34em;color:#ffe6b4;text-transform:uppercase;font-weight:400;
    text-shadow:0 2px 16px rgba(10,12,28,.9)}
  .hand{font-family:'Caveat',cursive;font-size:60px;color:#ffdf9a;letter-spacing:.01em;
    text-shadow:0 2px 18px rgba(10,12,28,.9)}
  .tag{margin-top:26px;font-family:'Anton',sans-serif;font-size:28px;letter-spacing:.44em;color:#ffe0a4;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(10,12,28,.9)}
  .orn{display:flex;align-items:center;justify-content:center;gap:24px;margin:26px 0 14px}
  .orn i{display:block;width:120px;height:1px;background:linear-gradient(90deg,transparent,#ffdf9a,transparent)}
  /* small Earth emblem */
  .earth{position:relative;width:60px;height:60px;border-radius:50%;overflow:hidden;flex:0 0 auto;
    background:radial-gradient(circle at 36% 32%, #7cc0ee 0%, #2f7fc4 40%, #14538f 78%, #0c3866 100%);
    box-shadow:0 0 22px rgba(120,190,255,.6),inset -6px -6px 14px rgba(0,0,0,.4)}
  .earth b{position:absolute;background:#3c9a4e;border-radius:46% 54% 50% 50%}
  .e1{left:8px;top:12px;width:22px;height:16px;transform:rotate(-12deg)}
  .e2{left:30px;top:26px;width:20px;height:20px;border-radius:52% 48% 44% 56%}
  .e3{left:14px;top:34px;width:14px;height:12px}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#d5762f,#ffdf8a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,14,30,.82);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.4em;color:#ffdf9a;text-transform:uppercase}
  #ui h1{font-family:'Anton',sans-serif;font-size:132px;color:#fff5e4;line-height:1;letter-spacing:.02em;text-transform:uppercase}
  #ui p{font-family:'Caveat',cursive;font-size:52px;color:#ffe0a4}
  #play{font-family:'Anton',sans-serif;font-size:34px;color:#241505;background:#ffd98a;border:none;
    border-radius:100px;padding:24px 72px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 40px rgba(255,200,110,.4)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  // drifting clouds
  const CL=[]; const cd=[[120,250,420,180],[560,180,520,210],[300,410,360,150],[760,330,440,190],[40,150,300,130]];
  cd.forEach((d,i)=>{const e=document.createElement('div');e.className='cloud';e.style.left=d[0]+'px';e.style.top=d[1]+'px';
    e.style.width=d[2]+'px';e.style.height=d[3]+'px';e.dataset.ph=((i*27)%100)/100;e.dataset.sp=0.5+(i%3)*0.28;
    world.insertBefore(e,document.getElementById('sunglow'));CL.push(e);});
  // pines rising from the overlook
  const PN=[[70,150,320],[150,190,260],[905,160,300],[982,200,240],[360,120,190],[720,130,200]];
  PN.forEach(d=>{const e=document.createElement('div');e.className='pine';e.style.left=d[0]+'px';
    e.style.width=d[1]+'px';e.style.height=d[2]+'px';e.style.bottom=(120)+'px';world.appendChild(e);});
  // glimmers on the lake (sun reflection sparkle)
  const GL=[]; for(let i=0;i<26;i++){const e=document.createElement('div');e.className='glim';const sz=5+(i%4)*4;
    e.style.width=sz+'px';e.style.height=(sz*0.5)+'px';
    e.style.left=(430+((i*67)%230))+'px';e.style.top=(1020+((i*83)%470))+'px';
    e.dataset.ph=((i*37)%100)/100;e.dataset.sp=0.8+(i%5)*0.3;world.appendChild(e);GL.push(e);}
  // warm embers drifting up
  const EM=[]; for(let i=0;i<40;i++){const e=document.createElement('div');e.className='ember';const sz=4+(i%4)*3;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=((i*37)%100)+'%';
    e.dataset.dur=7+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=40+((i*17)%90);
    stage.appendChild(e);EM.push(e);}
  const sun=document.getElementById('sun'),sunglow=document.getElementById('sunglow'),rays=document.getElementById('rays'),
        sunref=document.getElementById('sunref'),bloom=document.getElementById('bloom'),bar=document.getElementById('bar');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/900,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    // slow cinematic push-in + gentle drift
    world.style.transform=`scale(${1+0.09*prog}) translate(${Math.sin(ts/9)*5}px, ${-prog*12}px)`;
    const grow=1+0.03*Math.sin(ts/2.4);
    sunglow.style.transform=`translate(-50%,-50%) scale(${grow})`;
    sunglow.style.opacity=(0.9+0.1*Math.sin(ts/1.9)).toFixed(3);
    sun.style.opacity=(0.96+0.04*Math.sin(ts/1.5)).toFixed(3);
    rays.style.transform=`translate(-50%,-50%) rotate(${ts*1.2}deg)`;
    rays.style.opacity=(0.34+0.1*Math.sin(ts/2.2)).toFixed(3);
    sunref.style.opacity=(0.7+0.28*Math.sin(ts*1.4)).toFixed(3);
    sunref.style.transform=`translateX(-50%) scaleX(${1+0.12*Math.sin(ts*1.7)})`;
    for(const c of CL){const ph=+c.dataset.ph, sp=+c.dataset.sp;
      c.style.transform=`translateX(${Math.sin(ts*0.06*sp+ph*6.28)*40 + ts*3*sp}px)`;}
    for(const g of GL){const ph=+g.dataset.ph, sp=+g.dataset.sp;
      g.style.opacity=(0.3+0.6*(0.5+0.5*Math.sin(ts*sp*2.4+ph*6.28))).toFixed(3);}
    for(const e of EM){const pr=frac(ts/(+e.dataset.dur)+ +e.dataset.ph);
      e.style.top=(1560-pr*1560)+'px';
      e.style.transform=`translateX(${Math.sin(pr*6.28+ +e.dataset.ph*8)*(+e.dataset.sway)}px)`;
      e.style.opacity=(Math.sin(pr*Math.PI)*0.7).toFixed(2);}
    // sun-flare bloom on the emotional payoff
    let bl=0;
    if(t>BLOOM_FROM){ const up=clamp((t-BLOOM_FROM)/(BLOOM_PEAK-BLOOM_FROM),0,1);
      bl=sm(up)*0.62; if(t>BLOOM_PEAK) bl=0.62-clamp((t-BLOOM_PEAK)/1500,0,1)*0.3; }
    bloom.style.opacity=bl.toFixed(3);
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    if(bar) bar.style.width=(clamp(prog,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search), ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar.style.display='none'; }
  else {
    const bgm=document.getElementById('bgm');
    document.getElementById('play').addEventListener('click',()=>{
      ui.classList.add('hide');
      try{bgm.currentTime=0;bgm.volume=.9;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent='↻ Replay';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.9*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

# scene timeline
D = [3200, 5200, 5400, 6200, 6400]
S1,S2,S3,S4,S5 = 0, D[0], D[0]+D[1], D[0]+D[1]+D[2], D[0]+D[1]+D[2]+D[3]
BLOOM_FROM = S4 + 2500
BLOOM_PEAK = S4 + D[3] - 200

EARTH = '<span class="earth"><b class="e1"></b><b class="e2"></b><b class="e3"></b></span>'

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="jp">沈む夕陽は、<br>終わりじゃない。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">季節はめぐり、<br><span class="em">いのちは還る。</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="jp">だからもう一度、<br><span class="big">あるべき場所へ。</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:318px">'
           '<div class="title">Put It<br>Back</div>'
           '<div class="orn"><i></i>' + EARTH + '<i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="hand" style="margin-top:20px">Music for a Brighter Tomorrow</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Put It Back / Rolloing all stars (Promo Short)",
  desc="沈む夕陽は終わりじゃない。この星に、もう一度光を。Rolloing all stars の新曲「Put It Back」— Music for a Brighter Tomorrow.")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js)
          .replace("BLOOMFROM", str(BLOOM_FROM)).replace("BLOOMPEAK", str(BLOOM_PEAK)))

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@600&family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="world">
    <div id="sky"></div>
    <div id="rg1" class="ridge"></div>
    <div id="rg2" class="ridge"></div>
    <div id="rg3" class="ridge"></div>
    <div id="sunglow"></div>
    <div id="rays"></div>
    <div id="sun"></div>
    <div id="haze"></div>
    <div id="lake"></div>
    <div id="sunref"></div>
    <div id="fg"></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">Rolloing all stars</div>
    <h1>Put It Back</h1>
    <p>Music for a Brighter Tomorrow</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="putitback-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "putitback-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote putitback-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
