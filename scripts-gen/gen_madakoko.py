# -*- coding: utf-8 -*-
"""「まだ ここに立っている / w-Band」 — promo short (vertical 9:16, ~29s).

A resilience anthem matching the cover: a hilltop overlook at golden hour over a city
skyline and a river catching the sun, and — in the foreground on a rocky ledge — small
wild daisies still blooming from a crack in the stone (the "Still Standing Here" motif),
backlit and glowing. A tree frames the upper-left. Warm light, god-rays, drifting embers,
a slow push-in, and a sun-flare bloom on the chorus.

On-screen text uses the rights-holder-supplied lyrics (selected lines), verified cover
text (title / artist / the cover tagline "Still Standing Here") and generic labels.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL for frame capture.
BGM: madakoko-bgm.mp3 (30s from ~2:25, into the chorus climax).
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
  /* sky */
  #sky{position:absolute;left:0;top:0;width:1080px;height:1060px;
    background:linear-gradient(180deg,#14356f 0%,#28578f 20%,#5a7196 38%,#9a7d78 54%,#d67f3c 70%,#ff9f42 82%,#ffd486 94%,#ffe9b6 100%)}
  #skywarm{position:absolute;left:660px;top:900px;width:1000px;height:820px;transform:translate(-50%,-50%);pointer-events:none;
    background:radial-gradient(ellipse at 50% 50%, rgba(255,224,150,.62), rgba(255,200,120,.18) 44%, transparent 70%)}
  .cloud{position:absolute;border-radius:50%;filter:blur(15px);
    background:radial-gradient(ellipse at 42% 40%, rgba(255,224,180,.8), rgba(255,180,120,.24) 54%, transparent 76%)}
  /* sun + rays + reflection */
  #sunglow{position:absolute;left:660px;top:992px;width:620px;height:620px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(255,250,228,.97) 0%, rgba(255,216,134,.7) 24%, rgba(255,182,92,.28) 48%, transparent 72%)}
  #rays{position:absolute;left:660px;top:992px;width:1180px;height:1180px;transform:translate(-50%,-50%);border-radius:50%;
    opacity:.5;mix-blend-mode:screen;pointer-events:none;filter:blur(2px);
    background:repeating-conic-gradient(from 0deg at 50% 50%, rgba(255,238,196,.55) 0deg 2.2deg, transparent 2.2deg 12deg);
    -webkit-mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 10%, #000 26%, transparent 48%);
    mask:radial-gradient(circle at 50% 50%, transparent 3%, #000 10%, #000 26%, transparent 48%)}
  #sun{position:absolute;left:660px;top:992px;width:128px;height:128px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle,#fffefb 0%,#fff4d2 42%,#ffdd8a 76%,#ffc264 100%);box-shadow:0 0 78px 34px rgba(255,218,138,.7)}
  #mtn{position:absolute;left:0;top:906px;width:1080px;height:180px;opacity:.5;filter:blur(1px);background:#5a6f96;
    clip-path:polygon(0 62%,14% 44%,26% 56%,40% 36%,54% 52%,66% 38%,80% 54%,92% 40%,100% 52%,100% 100%,0 100%)}
  /* city skyline + reflective river */
  #cityglow{position:absolute;left:0;top:980px;width:1080px;height:170px;pointer-events:none;
    background:linear-gradient(180deg,transparent,rgba(255,196,120,.4) 60%,rgba(255,214,150,.55) 82%,transparent);filter:blur(5px)}
  #city{position:absolute;left:0;top:0;width:1080px;height:1160px;z-index:3}
  #water{position:absolute;left:0;top:1112px;width:1080px;height:320px;z-index:2;
    background:linear-gradient(180deg, rgba(255,214,150,.9) 0%, rgba(216,158,96,.85) 16%, rgba(120,120,120,.5) 44%, rgba(40,52,74,.9) 100%)}
  #sunref{position:absolute;left:660px;top:1118px;width:150px;height:300px;transform:translateX(-50%);z-index:3;pointer-events:none;
    background:linear-gradient(180deg, rgba(255,232,160,.9), rgba(255,200,120,.34) 46%, transparent 100%);filter:blur(5px);mix-blend-mode:screen}
  /* foreground rock + tree */
  #fg{position:absolute;left:0;bottom:0;width:1080px;height:560px;background:#0d1420;z-index:6;
    clip-path:polygon(0 26%,16% 16%,36% 24%,56% 12%,74% 22%,90% 14%,100% 22%,100% 100%,0 100%)}
  #tree{position:absolute;left:-140px;top:-160px;width:640px;height:700px;z-index:7;pointer-events:none;filter:blur(3px);
    background:
     radial-gradient(ellipse 210px 150px at 32% 24%, rgba(9,14,24,.98), transparent 70%),
     radial-gradient(ellipse 165px 125px at 54% 13%, rgba(9,14,24,.96), transparent 72%),
     radial-gradient(ellipse 150px 135px at 15% 42%, rgba(9,14,24,.95), transparent 72%),
     radial-gradient(ellipse 150px 115px at 45% 42%, rgba(9,14,24,.9), transparent 74%),
     radial-gradient(ellipse 125px 105px at 28% 60%, rgba(9,14,24,.82), transparent 76%),
     radial-gradient(ellipse 95px 80px at 60% 34%, rgba(9,14,24,.8), transparent 78%)}
  /* particles */
  .mote{position:absolute;border-radius:50%;background:radial-gradient(circle,#fffdf2,#ffe4ac 52%,transparent 74%);opacity:0;z-index:8}
  /* bloom + grade */
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(122% 80% at 58% 50%, rgba(255,248,224,.96), rgba(255,214,140,.72) 38%, rgba(255,180,95,.34) 68%, rgba(255,150,70,.1) 100%)}
  #grain{position:absolute;inset:0;opacity:.05;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 56% 42%, transparent 48%, rgba(8,12,26,.72) 100%)}
  /* daisies (hero) */
  .daisy{position:absolute;z-index:9}
  .dstem{position:absolute;left:50%;transform:translateX(-50%);width:9px;background:linear-gradient(180deg,#3f5a34,#24401f);border-radius:6px}
  .dleaf{position:absolute;width:44px;height:22px;background:#2f4d26;border-radius:0 100% 0 100%}
  .dhead{position:absolute;left:50%;top:0;transform:translateX(-50%)}
  .dpetal{position:absolute;left:50%;top:50%;width:26px;height:66px;margin:-66px 0 0 -13px;transform-origin:50% 100%;
    background:radial-gradient(ellipse at 50% 30%, #ffffff 0%, #fff3d8 58%, #ffd98f 100%);border-radius:50% 50% 46% 46%;
    box-shadow:0 0 10px rgba(255,214,140,.55)}
  .dcore{position:absolute;left:50%;top:50%;width:40px;height:40px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle at 42% 40%, #ffe082, #f0a825 60%, #c97d12);box-shadow:0 0 14px rgba(255,190,90,.7)}
  /* text */
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:300px 84px 0}
  .scene.low{justify-content:flex-start;padding:232px 84px 0}
  .kick{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:.5em;color:#fff2d6;text-transform:uppercase;
    text-shadow:0 2px 20px rgba(8,14,34,.95)}
  .jp{font-size:66px;line-height:1.62;font-weight:600;color:#fff8ee;letter-spacing:.05em;
    text-shadow:0 2px 24px rgba(6,14,34,.98),0 0 44px rgba(20,20,40,.6)}
  .jp .em{color:#ffdf8a}
  .big{font-size:88px;line-height:1.3;font-weight:700;color:#fff;letter-spacing:.04em;display:inline-block;
    text-shadow:0 3px 26px rgba(8,14,34,1),0 0 56px rgba(255,214,140,.5)}
  .title{font-family:'Yuji Syuku','Shippori Mincho',serif;font-size:104px;line-height:1.14;color:#fff8ea;letter-spacing:.03em;
    text-shadow:0 4px 3px rgba(0,0,0,.35),0 6px 40px rgba(6,14,34,.9),0 0 60px rgba(255,214,140,.4)}
  .artist{font-family:'Anton',sans-serif;font-size:42px;letter-spacing:.3em;color:#ffe6b4;text-transform:uppercase;font-weight:400;
    text-shadow:0 2px 16px rgba(8,14,34,.9)}
  .hand{font-family:'Caveat',cursive;font-size:56px;color:#ffdf9a;letter-spacing:.01em;
    text-shadow:0 2px 18px rgba(8,14,34,.9)}
  .tag{margin-top:24px;font-family:'Anton',sans-serif;font-size:27px;letter-spacing:.42em;color:#ffe2aa;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(8,14,34,.9)}
  .orn{display:flex;align-items:center;justify-content:center;gap:22px;margin:24px 0 12px}
  .orn i{display:block;width:110px;height:1px;background:linear-gradient(90deg,transparent,#ffe2aa,transparent)}
  .orn b{font-size:28px;color:#ffdf8a}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#d67f3c,#ffdf8a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,14,30,.82);backdrop-filter:blur(4px);z-index:20;gap:26px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.4em;color:#ffdf9a;text-transform:uppercase}
  #ui h1{font-family:'Yuji Syuku','Shippori Mincho',serif;font-size:92px;color:#fff8ea;line-height:1.14}
  #ui p{font-family:'Caveat',cursive;font-size:50px;color:#ffe2aa}
  #play{font-family:'Anton',sans-serif;font-size:34px;color:#241505;background:#ffdf8a;border:none;
    border-radius:100px;padding:24px 72px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 40px rgba(255,200,110,.4)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  // clouds
  const CL=[]; const cd=[[90,300,420,150],[520,240,520,180],[300,430,360,140],[740,360,440,170],[150,540,300,120]];
  cd.forEach((d,i)=>{const e=document.createElement('div');e.className='cloud';e.style.left=d[0]+'px';e.style.top=d[1]+'px';
    e.style.width=d[2]+'px';e.style.height=d[3]+'px';e.style.opacity=(0.5-(i%3)*0.1).toFixed(2);
    e.dataset.ph=((i*27)%100)/100;e.dataset.sp=0.5+(i%3)*0.3;
    world.insertBefore(e,document.getElementById('sunglow'));CL.push(e);});
  // city skyline silhouette
  const city=document.getElementById('city'); const base=1112; let x=0; let bi=0;
  while(x<1080){const w=26+((bi*37)%54); const h=40+((bi*53)%150)+ (Math.abs(x-660)<220?40:0);
    const b=document.createElement('div'); b.style.position='absolute'; b.style.left=x+'px'; b.style.top=(base-h)+'px';
    b.style.width=(w-3)+'px'; b.style.height=h+'px';
    const near=Math.abs(x-660)<240; b.style.background=near?'#5b5566':'#33456a'; b.style.opacity=near?'0.82':'0.9';
    // a couple of lit windows
    if((bi%2)===0){b.style.boxShadow='inset 0 0 0 100px rgba(0,0,0,0)';}
    city.appendChild(b); x+=w+2+((bi*13)%6); bi++;}
  // daisies (hero) — still blooming from the rock
  function makeDaisy(px,py,scale,petals){const d=document.createElement('div');d.className='daisy';
    d.style.left=px+'px';d.style.top=py+'px';d.style.transform='scale('+scale+')';d.style.transformOrigin='50% 100%';
    const stemH=150; const stem=document.createElement('div');stem.className='dstem';stem.style.height=stemH+'px';stem.style.top='120px';d.appendChild(stem);
    const l1=document.createElement('div');l1.className='dleaf';l1.style.left='6px';l1.style.top='190px';l1.style.transform='rotate(20deg)';d.appendChild(l1);
    const l2=document.createElement('div');l2.className='dleaf';l2.style.left='-30px';l2.style.top='230px';l2.style.transform='scaleX(-1) rotate(20deg)';d.appendChild(l2);
    const head=document.createElement('div');head.className='dhead';head.style.width='150px';head.style.height='150px';head.style.top='40px';d.appendChild(head);
    for(let i=0;i<petals;i++){const p=document.createElement('div');p.className='dpetal';
      p.style.transform='rotate('+(i*(360/petals))+'deg)';head.appendChild(p);}
    const core=document.createElement('div');core.className='dcore';head.appendChild(core);
    world.appendChild(d);return d;}
  const DA=[makeDaisy(250,1300,1.0,12),makeDaisy(150,1360,1.32,13),makeDaisy(372,1372,0.9,12)];
  DA.forEach((d,i)=>{d.dataset.ph=(i*33%100)/100;});
  // embers
  const MO=[]; for(let i=0;i<30;i++){const e=document.createElement('div');e.className='mote';const sz=4+(i%4)*3;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=((i*37)%100)+'%';
    e.dataset.dur=7+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=40+((i*17)%86);
    stage.appendChild(e);MO.push(e);}
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
    world.style.transform=`scale(${1+0.08*prog}) translate(${Math.sin(ts/9)*5}px, ${-prog*12}px)`;
    const grow=1+0.03*Math.sin(ts/2.4);
    sunglow.style.transform=`translate(-50%,-50%) scale(${grow})`;
    sunglow.style.opacity=(0.9+0.1*Math.sin(ts/1.9)).toFixed(3);
    sun.style.opacity=(0.96+0.04*Math.sin(ts/1.5)).toFixed(3);
    rays.style.transform=`translate(-50%,-50%) rotate(${ts*1.1}deg)`;
    rays.style.opacity=(0.36+0.1*Math.sin(ts/2.2)).toFixed(3);
    sunref.style.opacity=(0.66+0.3*Math.sin(ts*1.5)).toFixed(3);
    sunref.style.transform=`translateX(-50%) scaleX(${1+0.12*Math.sin(ts*1.7)})`;
    for(const c of CL){const ph=+c.dataset.ph, sp=+c.dataset.sp;
      c.style.transform=`translateX(${Math.sin(ts*0.05*sp+ph*6.28)*26 + ts*3*sp}px)`;}
    for(const d of DA){const ph=+d.dataset.ph, base=+d.style.transform.match(/scale\(([^)]+)\)/)[1];
      const sway=Math.sin(ts*1.1+ph*6.28)*1.6;
      d.style.transform=`scale(${base}) rotate(${sway}deg)`;}
    for(const m of MO){const pr=frac(ts/(+m.dataset.dur)+ +m.dataset.ph);
      m.style.top=(1560-pr*1500)+'px';
      m.style.transform=`translateX(${Math.sin(pr*6.28+ +m.dataset.ph*8)*(+m.dataset.sway)}px)`;
      m.style.opacity=(Math.sin(pr*Math.PI)*0.62).toFixed(2);}
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
D = [2800, 4800, 4800, 4800, 6100, 6100]
S5 = D[0]+D[1]+D[2]+D[3]
BLOOM_FROM = S5 + 2400
BLOOM_PEAK = S5 + D[4] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="jp">何度も 膝をついた。<br>数えるのは、やめにした。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">折れた日の数だけ、<br>この背中は 広くなった。</div></div>'),
    (D[3], '<div class="scene mid"><div class="jp">誰も知らなくていい。<br><span class="em">この足跡は、消えない。</span></div></div>'),
    (D[4], '<div class="scene mid"><div class="jp">倒れた数だけ 強くなって、<br><span class="big">まだ ここに<br>立っている。</span></div></div>'),
    (D[5], '<div class="scene mid" style="padding-top:322px">'
           '<div class="title">まだ ここに<br>立っている</div>'
           '<div class="orn"><i></i><b>&#10039;</b><i></i></div>'
           '<div class="artist">w-Band</div>'
           '<div class="hand" style="margin-top:16px">Still Standing Here</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="まだ ここに立っている / w-Band (Promo Short)",
  desc="倒れた数だけ 強くなって、まだ ここに立っている。生き抜いた、それだけで胸を張っていい。w-Band の新曲「まだ ここに立っている」。")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@600&family=Yuji+Syuku&family=Shippori+Mincho:wght@600;700&family=Noto+Serif+JP:wght@500;600;700&display=swap">
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
    <div id="cityglow"></div>
    <div id="water"></div>
    <div id="sunref"></div>
    <div id="city"></div>
    <div id="fg"></div>
    <div id="tree"></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">w-Band</div>
    <h1>まだ ここに立っている</h1>
    <p>Still Standing Here</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="madakoko-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "madakoko-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote madakoko-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
