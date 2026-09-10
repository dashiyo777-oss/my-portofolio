# -*- coding: utf-8 -*-
"""「Give Us Back the Sky / Rolloing all stars」 — promo short (vertical 9:16, ~26s).

A companion piece to "Put It Back" (same band) but a distinct, brighter take that
matches THIS cover: a wide blue morning sky over a lake-and-forest valley, a bald
eagle soaring across the frame toward the light, and — in the foreground on a rocky
overlook — a boy with his arm around his dog, watching the sky. A tall pine frames
the left edge. Warm low sun on the right, drifting clouds, floating light, and a
sky-opening bloom on the payoff.

On-screen text is limited to verified cover text (title / artist) plus generic labels
and evocative promo copy — no invented lyrics, and the "Music for a Brighter Tomorrow"
tagline is NOT shown here (it is not printed on this cover).

Deterministic render: exposes window.renderAt(ms) + window.TOTAL for frame capture.
BGM: sky-bgm.mp3 (30s from ~1:38, the first big chorus).
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
  #world{position:absolute;inset:0;transform-origin:54% 48%}
  /* sky */
  #sky{position:absolute;left:0;top:0;width:1080px;height:1020px;
    background:linear-gradient(180deg,#123f86 0%,#2864ac 20%,#4e8ccb 40%,#84b4de 58%,#c3dcec 73%,#efe0b6 87%,#ffe6ac 100%)}
  #skywarm{position:absolute;right:-160px;top:360px;width:900px;height:760px;pointer-events:none;
    background:radial-gradient(ellipse at 60% 50%, rgba(255,224,150,.6), rgba(255,206,120,.18) 46%, transparent 70%)}
  .cloud{position:absolute;border-radius:50%;filter:blur(16px);
    background:radial-gradient(ellipse at 42% 38%, rgba(255,255,255,.92), rgba(232,240,250,.5) 52%, transparent 74%)}
  /* sun low-right */
  #sunglow{position:absolute;left:902px;top:930px;width:640px;height:640px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(255,248,224,.96) 0%, rgba(255,214,132,.7) 24%, rgba(255,180,90,.28) 48%, transparent 72%)}
  #rays{position:absolute;left:902px;top:930px;width:1200px;height:1200px;transform:translate(-50%,-50%);border-radius:50%;
    opacity:.5;mix-blend-mode:screen;pointer-events:none;filter:blur(2px);
    background:repeating-conic-gradient(from 0deg at 50% 50%, rgba(255,240,200,.55) 0deg 2.2deg, transparent 2.2deg 12deg);
    -webkit-mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 10%, #000 26%, transparent 48%);
    mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 10%, #000 26%, transparent 48%)}
  #sun{position:absolute;left:902px;top:930px;width:132px;height:132px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle,#fffefb 0%,#fff4d4 42%,#ffdd8c 76%,#ffc366 100%);box-shadow:0 0 80px 34px rgba(255,220,140,.7)}
  /* distant mountains */
  #mtn{position:absolute;left:0;top:820px;width:1080px;height:230px;opacity:.5;filter:blur(1px);background:#4a6a92;
    clip-path:polygon(0 60%,12% 42%,22% 54%,34% 30%,46% 50%,56% 34%,68% 52%,80% 36%,90% 52%,100% 40%,100% 100%,0 100%)}
  /* valley: forested hills + winding water */
  #vfar{position:absolute;left:0;top:958px;width:1080px;height:220px;background:#5c7d6a;opacity:.85;
    clip-path:polygon(0 40%,16% 54%,30% 44%,44% 58%,58% 46%,72% 60%,86% 48%,100% 58%,100% 100%,0 100%)}
  #water{position:absolute;left:0;top:1000px;width:1080px;height:360px;
    background:linear-gradient(180deg, rgba(200,224,236,.95), rgba(150,190,214,.9) 30%, rgba(96,140,168,.85) 100%);
    clip-path:polygon(0 8%,26% 14%,44% 26%,52% 44%,60% 66%,58% 100%,40% 100%,44% 66%,38% 44%,26% 30%,0 20%)}
  #wshine{position:absolute;left:0;top:1004px;width:1080px;height:60px;pointer-events:none;
    background:linear-gradient(180deg, rgba(255,244,214,.85), transparent);mix-blend-mode:screen;filter:blur(3px)}
  #vmid{position:absolute;left:0;top:1120px;width:1080px;height:280px;background:#3f5f57;
    clip-path:polygon(0 30%,20% 46%,40% 32%,60% 48%,80% 34%,100% 46%,100% 100%,0 100%)}
  /* foreground rock ledge + pines */
  #fg{position:absolute;left:0;bottom:0;width:1080px;height:360px;background:#0d1420;z-index:6;
    clip-path:polygon(0 40%,16% 22%,34% 34%,52% 20%,70% 32%,86% 22%,100% 34%,100% 100%,0 100%)}
  .pine{position:absolute;background:#0d1420;z-index:6;
    clip-path:polygon(50% 0,60% 20%,54% 20%,66% 42%,58% 42%,72% 66%,56% 66%,56% 100%,44% 100%,44% 66%,28% 66%,42% 42%,34% 42%,46% 20%,40% 20%)}
  #bigpine{position:absolute;left:-78px;top:410px;width:420px;height:950px;background:#0d1420;z-index:7;
    clip-path:polygon(50% 0,58% 16%,53% 16%,63% 34%,55% 34%,67% 54%,55% 54%,70% 76%,54% 76%,54% 100%,46% 100%,46% 76%,30% 76%,45% 54%,33% 54%,45% 34%,37% 34%,47% 16%,42% 16%)}
  /* eagle */
  #eagle{position:absolute;left:0;top:0;width:214px;height:100px;z-index:8;will-change:transform}
  #eagle svg{overflow:visible;display:block}
  /* boy + dog on the ledge (from behind) */
  #bdrim{position:absolute;z-index:7;filter:blur(1px)}
  #bdrim>*{background:linear-gradient(240deg, rgba(255,224,150,.7), rgba(255,190,110,.08) 60%)!important}
  #bd{position:absolute;z-index:8}
  #perch{position:absolute;left:300px;top:1392px;width:520px;height:220px;background:#0e1522;z-index:6;
    border-radius:52% 48% 0 0/72% 66% 0 0}
  #bd,#bdrim{left:356px;top:1150px;width:392px;height:330px;transform:scale(1.14);transform-origin:50% 100%}
  .s{position:absolute;background:#0e1522}
  /* boy from behind */
  #b-head{left:60px;top:6px;width:70px;height:78px;border-radius:50% 50% 47% 47%}
  #b-body{left:8px;top:60px;width:186px;height:270px;
    clip-path:polygon(32% 0,68% 0,82% 22%,93% 58%,100% 100%,0 100%,7% 58%,18% 22%)}
  /* dog sitting beside him, from behind */
  #d-tail{left:338px;top:150px;width:34px;height:122px;border-radius:50%;transform:rotate(34deg);transform-origin:50% 100%}
  #d-body{left:214px;top:150px;width:150px;height:180px;
    clip-path:polygon(40% 0,60% 0,72% 26%,82% 56%,96% 100%,4% 100%,20% 56%,28% 26%)}
  #d-head{left:246px;top:118px;width:66px;height:64px;border-radius:52% 52% 46% 46%}
  #d-earL{left:236px;top:104px;width:36px;height:54px;transform:rotate(18deg);clip-path:polygon(56% 0,100% 100%,0 90%)}
  #d-earR{left:298px;top:104px;width:36px;height:54px;transform:rotate(-18deg);clip-path:polygon(44% 0,100% 90%,0 100%)}
  /* particles */
  .mote{position:absolute;border-radius:50%;background:radial-gradient(circle,#fffdf4,#ffe6b0 52%,transparent 74%);opacity:0;z-index:7}
  /* bloom + grade */
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(122% 82% at 74% 46%, rgba(255,250,230,.96), rgba(210,232,248,.7) 36%, rgba(150,196,232,.4) 66%, rgba(120,170,220,.12) 100%)}
  #grain{position:absolute;inset:0;opacity:.05;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 60% 42%, transparent 50%, rgba(8,12,26,.68) 100%)}
  /* text */
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:300px 84px 0}
  .scene.low{justify-content:flex-start;padding:250px 84px 0}
  .kick{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:.5em;color:#fff4de;text-transform:uppercase;
    text-shadow:0 2px 20px rgba(8,16,40,.95)}
  .jp{font-size:70px;line-height:1.6;font-weight:600;color:#fff8ee;letter-spacing:.06em;
    text-shadow:0 2px 24px rgba(6,14,34,.98),0 0 44px rgba(16,30,60,.7)}
  .jp .em{color:#ffe08a}
  .big{font-size:96px;line-height:1.26;font-weight:600;color:#fff;letter-spacing:.05em;display:inline-block;
    text-shadow:0 3px 26px rgba(8,14,34,1),0 0 56px rgba(255,224,150,.5)}
  .title{font-family:'Anton',sans-serif;font-size:118px;line-height:.98;color:#fff7ea;letter-spacing:.02em;text-transform:uppercase;
    text-shadow:0 4px 2px rgba(0,0,0,.32),0 6px 40px rgba(6,14,34,.9),0 0 60px rgba(255,224,150,.4)}
  .artist{font-family:'Anton',sans-serif;font-size:40px;letter-spacing:.34em;color:#ffe9bc;text-transform:uppercase;font-weight:400;
    text-shadow:0 2px 16px rgba(8,14,34,.9)}
  .tag{margin-top:26px;font-family:'Anton',sans-serif;font-size:28px;letter-spacing:.44em;color:#ffe4ae;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(8,14,34,.9)}
  .orn{display:flex;align-items:center;justify-content:center;gap:24px;margin:26px 0 14px}
  .orn i{display:block;width:120px;height:1px;background:linear-gradient(90deg,transparent,#ffe4ae,transparent)}
  .orn b{font-size:30px;color:#ffe08a}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#2864ac,#ffe08a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,16,34,.82);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.4em;color:#ffe08a;text-transform:uppercase}
  #ui h1{font-family:'Anton',sans-serif;font-size:104px;color:#fff7ea;line-height:1;letter-spacing:.02em;text-transform:uppercase}
  #ui p{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.3em;color:#ffe4ae;text-transform:uppercase}
  #play{font-family:'Anton',sans-serif;font-size:34px;color:#0f2140;background:#ffe08a;border:none;
    border-radius:100px;padding:24px 72px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 40px rgba(120,180,240,.4)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  // drifting clouds
  const CL=[]; const cd=[[80,210,440,190],[520,150,560,220],[300,360,380,160],[720,300,460,200],[120,470,320,140],[820,470,360,150]];
  cd.forEach((d,i)=>{const e=document.createElement('div');e.className='cloud';e.style.left=d[0]+'px';e.style.top=d[1]+'px';
    e.style.width=d[2]+'px';e.style.height=d[3]+'px';e.style.opacity=(0.6-(i%3)*0.12).toFixed(2);
    e.dataset.ph=((i*27)%100)/100;e.dataset.sp=0.5+(i%3)*0.3;
    world.insertBefore(e,document.getElementById('sunglow'));CL.push(e);});
  // pines on the ledge
  const PN=[[250,150,300],[760,150,260],[900,130,300],[470,110,200]];
  PN.forEach(d=>{const e=document.createElement('div');e.className='pine';e.style.left=d[0]+'px';
    e.style.width=d[1]+'px';e.style.height=d[2]+'px';e.style.bottom='210px';world.appendChild(e);});
  // eagle silhouette (bald eagle gliding, wings spread)
  const eg=document.getElementById('eagle');
  eg.innerHTML=`<svg width="214" height="100" viewBox="-85 -40 170 80"><g fill="#10161f">
    <path d="M0 -2 C -22 -20 -46 -22 -82 -34 C -50 -12 -22 -4 -8 0 L -6 9 L 0 13 L 6 9 L 8 0
             C 22 -4 50 -12 82 -34 C 46 -22 22 -20 0 -2 Z"/>
    <circle cx="0" cy="-10" r="7"/></g></svg>`;
  // boy+dog rim-light clone
  const bd=document.getElementById('bd'), bdrim=document.getElementById('bdrim');
  [...bd.children].forEach(c=>{const a=c.cloneNode();a.style.transform=(c.style.transform||'')+' translateX(5px)';bdrim.appendChild(a);});
  // floating light motes
  const MO=[]; for(let i=0;i<26;i++){const e=document.createElement('div');e.className='mote';const sz=4+(i%4)*3;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=((i*37)%100)+'%';
    e.dataset.dur=8+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=36+((i*17)%80);
    stage.appendChild(e);MO.push(e);}
  const sun=document.getElementById('sun'),sunglow=document.getElementById('sunglow'),rays=document.getElementById('rays'),
        wshine=document.getElementById('wshine'),dtail=document.getElementById('d-tail'),bloom=document.getElementById('bloom'),bar=document.getElementById('bar');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/900,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    world.style.transform=`scale(${1+0.08*prog}) translate(${Math.sin(ts/9)*5}px, ${-prog*12}px)`;
    const grow=1+0.03*Math.sin(ts/2.4);
    sunglow.style.transform=`translate(-50%,-50%) scale(${grow})`;
    sunglow.style.opacity=(0.9+0.1*Math.sin(ts/1.9)).toFixed(3);
    sun.style.opacity=(0.96+0.04*Math.sin(ts/1.5)).toFixed(3);
    rays.style.transform=`translate(-50%,-50%) rotate(${ts*1.1}deg)`;
    rays.style.opacity=(0.36+0.1*Math.sin(ts/2.2)).toFixed(3);
    wshine.style.opacity=(0.5+0.4*Math.sin(ts*1.5)).toFixed(3);
    // eagle glides across and soars up toward the light
    const ep=clamp(prog*1.05,0,1);
    const ex=-170+ep*1330, ey=560-Math.sin(ep*2.05)*300-ep*60;
    const bank=Math.cos(ep*2.05)*10, flap=1+0.14*Math.sin(ts*3.4);
    eg.style.transform=`translate(${ex}px, ${ey}px) rotate(${-bank}deg) scaleY(${flap})`;
    eg.style.opacity=clamp(Math.min(ep/0.05,(1.02-ep)/0.06),0,1).toFixed(3);
    dtail.style.transform=`rotate(${30+4*Math.sin(ts*2.2)}deg)`;   // gentle tail wag
    for(const c of CL){const ph=+c.dataset.ph, sp=+c.dataset.sp;
      c.style.transform=`translateX(${Math.sin(ts*0.05*sp+ph*6.28)*30 + ts*3.4*sp}px)`;}
    for(const m of MO){const pr=frac(ts/(+m.dataset.dur)+ +m.dataset.ph);
      m.style.top=(1560-pr*1500)+'px';
      m.style.transform=`translateX(${Math.sin(pr*6.28+ +m.dataset.ph*8)*(+m.dataset.sway)}px)`;
      m.style.opacity=(Math.sin(pr*Math.PI)*0.6).toFixed(2);}
    // sky-opening bloom on the payoff
    let bl=0;
    if(t>BLOOM_FROM){ const up=clamp((t-BLOOM_FROM)/(BLOOM_PEAK-BLOOM_FROM),0,1);
      bl=sm(up)*0.6; if(t>BLOOM_PEAK) bl=0.6-clamp((t-BLOOM_PEAK)/1500,0,1)*0.3; }
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
S4 = D[0]+D[1]+D[2]
BLOOM_FROM = S4 + 2500
BLOOM_PEAK = S4 + D[3] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="jp">少年と犬は、<br>ただ空を見ていた。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">翼はまだ、<br><span class="em">自由を憶えている。</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="jp">いつかきっと、<br><span class="big">空を、返して。</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:300px">'
           '<div class="title">Give Us Back<br>the Sky</div>'
           '<div class="orn"><i></i><b>&#10022;</b><i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Give Us Back the Sky / Rolloing all stars (Promo Short)",
  desc="少年と犬が見上げた、あの大きな空。翼はまだ自由を憶えている。Rolloing all stars の新曲「Give Us Back the Sky」。")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="world">
    <div id="sky"></div>
    <div id="skywarm"></div>
    <div id="mtn"></div>
    <div id="sunglow"></div>
    <div id="rays"></div>
    <div id="sun"></div>
    <div id="vfar"></div>
    <div id="water"></div>
    <div id="wshine"></div>
    <div id="vmid"></div>
    <div id="fg"></div>
    <div id="bigpine"></div>
    <div id="perch"></div>
    <div id="bdrim"></div>
    <div id="bd">
      <div id="b-body" class="s"></div><div id="b-head" class="s"></div>
      <div id="d-tail" class="s"></div><div id="d-body" class="s"></div>
      <div id="d-head" class="s"></div><div id="d-earL" class="s"></div><div id="d-earR" class="s"></div>
    </div>
    <div id="eagle"></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">Rolloing all stars</div>
    <h1>Give Us Back the Sky</h1>
    <p>New Single</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="sky-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "giveusbacksky-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote giveusbacksky-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
