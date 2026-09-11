# -*- coding: utf-8 -*-
"""「Give Us Back the Sky / Rolloing all stars」 — promo short (vertical 9:16, ~26s).

Redesigned for its own identity (no landscape / no sun-on-the-horizon): the frame IS
the sky. Layered clouds drift with parallax, warm sunlight breaks through from the
upper right, and a lone bald eagle soars up across the whole frame toward the light —
freedom, the sky itself. On the payoff the clouds open and the light floods in.

On-screen text uses verified cover text (title / artist) plus generic labels and
evocative promo copy — no invented lyrics.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL for frame capture.
BGM: sky-bgm.mp3.
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
  #world{position:absolute;inset:0;transform-origin:56% 42%}
  #sky{position:absolute;inset:0;
    background:linear-gradient(165deg,#1f5fa8 0%,#3f80c4 26%,#69a4d8 48%,#a6cbe6 68%,#e6d9b8 84%,#ffe6ac 100%)}
  #sunbreak{position:absolute;right:-160px;top:120px;width:1000px;height:1000px;pointer-events:none;
    background:radial-gradient(circle at 62% 44%, rgba(255,248,220,.98), rgba(255,222,150,.66) 22%, rgba(255,196,110,.28) 44%, transparent 68%)}
  #rays{position:absolute;right:60px;top:300px;width:1500px;height:1500px;transform:translate(-50%,-50%);border-radius:50%;
    opacity:.42;mix-blend-mode:screen;pointer-events:none;filter:blur(3px);
    background:repeating-conic-gradient(from 0deg at 50% 50%, rgba(255,244,210,.5) 0deg 2deg, transparent 2deg 13deg);
    -webkit-mask:radial-gradient(circle at 50% 50%, transparent 6%, #000 16%, #000 40%, transparent 64%);
    mask:radial-gradient(circle at 50% 50%, transparent 6%, #000 16%, #000 40%, transparent 64%)}
  .cloud{position:absolute;will-change:transform}
  .puff{position:absolute;border-radius:50%}
  #eagle{position:absolute;left:0;top:0;width:230px;height:108px;z-index:8;will-change:transform}
  #eagle svg{overflow:visible;display:block}
  .feather{position:absolute;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:rgba(255,255,255,.7);opacity:0;z-index:7}
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(120% 90% at 66% 34%, rgba(255,252,238,.97), rgba(255,232,170,.72) 34%, rgba(210,232,248,.4) 66%, transparent 100%)}
  #grain{position:absolute;inset:0;opacity:.04;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 60% 40%, transparent 54%, rgba(20,44,80,.5) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:300px 84px 0}
  .scene.low{justify-content:flex-start;padding:250px 84px 0}
  .kick{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:.5em;color:#fff6de;text-transform:uppercase;
    text-shadow:0 2px 20px rgba(20,44,80,.8)}
  .jp{font-size:70px;line-height:1.6;font-weight:600;color:#fff;letter-spacing:.06em;
    text-shadow:0 2px 22px rgba(20,44,80,.95),0 0 46px rgba(30,70,120,.7)}
  .jp .em{color:#ffe08a}
  .big{font-size:96px;line-height:1.26;font-weight:700;color:#fff;letter-spacing:.05em;display:inline-block;
    text-shadow:0 3px 24px rgba(20,44,80,1),0 0 56px rgba(255,224,150,.55)}
  .title{font-family:'Anton',sans-serif;font-size:118px;line-height:.98;color:#fff;letter-spacing:.02em;text-transform:uppercase;
    text-shadow:0 4px 3px rgba(20,40,70,.4),0 6px 40px rgba(20,44,80,.85),0 0 60px rgba(255,224,150,.4)}
  .artist{font-family:'Anton',sans-serif;font-size:40px;letter-spacing:.34em;color:#fff1cf;text-transform:uppercase;font-weight:400;
    text-shadow:0 2px 16px rgba(20,44,80,.8)}
  .tag{margin-top:26px;font-family:'Anton',sans-serif;font-size:28px;letter-spacing:.44em;color:#ffe9bc;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(20,44,80,.8)}
  .orn{display:flex;align-items:center;justify-content:center;gap:24px;margin:26px 0 14px}
  .orn i{display:block;width:120px;height:1px;background:linear-gradient(90deg,transparent,#ffe9bc,transparent)}
  .orn b{font-size:30px;color:#ffe08a}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#3f80c4,#ffe08a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(20,44,80,.8);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.4em;color:#ffe08a;text-transform:uppercase}
  #ui h1{font-family:'Anton',sans-serif;font-size:104px;color:#fff;line-height:1;letter-spacing:.02em;text-transform:uppercase}
  #ui p{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.3em;color:#ffe9bc;text-transform:uppercase}
  #play{font-family:'Anton',sans-serif;font-size:34px;color:#123;background:#ffe08a;border:none;
    border-radius:100px;padding:24px 72px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 40px rgba(150,200,240,.4)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  const sky=document.getElementById('sky');
  // layered clouds (parallax). depth 0=far(high,small,slow,dim) .. 2=near(low,big,fast,bright)
  const CLOUDS=[];
  function buildCloud(cx,cy,scale,bright,depth){const c=document.createElement('div');c.className='cloud';
    c.style.left=cx+'px';c.style.top=cy+'px';c.style.transform='translateX(0)';
    const w=340*scale, h=150*scale;
    const puffs=[[0.16,0.55,0.5],[0.36,0.28,0.72],[0.56,0.5,0.86],[0.74,0.3,0.66],[0.88,0.58,0.48],[0.46,0.66,0.6]];
    puffs.forEach(p=>{const e=document.createElement('div');e.className='puff';
      const pw=w*p[2];e.style.width=pw+'px';e.style.height=(pw*0.82)+'px';
      e.style.left=(w*p[0]-pw/2)+'px';e.style.top=(h*p[1]-pw*0.41)+'px';
      e.style.background='radial-gradient(ellipse at 44% 38%, rgba(255,255,255,'+bright+'), rgba(226,238,250,'+(bright*0.5)+') 54%, transparent 76%)';
      e.style.filter='blur('+(6+depth*5)+'px)';c.appendChild(e);});
    c.dataset.sp=(0.3+depth*0.9); c.dataset.w=w; c.dataset.x0=cx;
    world.insertBefore(c,document.getElementById('rays'));CLOUDS.push(c);return c;}
  // far band
  buildCloud(120,240,0.9,0.5,0); buildCloud(640,180,1.05,0.5,0); buildCloud(900,320,0.8,0.45,0);
  // mid band
  buildCloud(-40,560,1.3,0.8,1); buildCloud(520,640,1.5,0.82,1); buildCloud(1000,700,1.2,0.78,1);
  // near band (lower, big, bright)
  buildCloud(60,1180,1.9,0.96,2); buildCloud(640,1320,2.2,0.98,2); buildCloud(-120,1520,2.0,0.95,2);
  buildCloud(760,1620,2.1,0.96,2);
  // eagle silhouette
  const eg=document.getElementById('eagle');
  eg.innerHTML=`<svg width="230" height="108" viewBox="-85 -40 170 80"><g fill="#1a2c46">
    <path d="M0 -2 C -22 -20 -46 -22 -82 -34 C -50 -12 -22 -4 -8 0 L -6 9 L 0 13 L 6 9 L 8 0
             C 22 -4 50 -12 82 -34 C 46 -22 22 -20 0 -2 Z"/>
    <circle cx="0" cy="-10" r="7"/></g></svg>`;
  // drifting feathers / light flecks
  const FE=[]; for(let i=0;i<22;i++){const e=document.createElement('div');e.className='feather';
    const w=8+(i%4)*7;e.style.width=w+'px';e.style.height=(w*0.5)+'px';e.style.left=((i*41)%100)+'%';
    e.dataset.dur=8+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=40+((i*17)%90);
    stage.appendChild(e);FE.push(e);}
  const sunbreak=document.getElementById('sunbreak'),rays=document.getElementById('rays'),
        bloom=document.getElementById('bloom'),bar=document.getElementById('bar');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/900,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    // slow rise (we drift upward through the clouds)
    world.style.transform=`scale(${1+0.06*prog}) translateY(${-prog*26}px)`;
    sunbreak.style.opacity=(0.92+0.08*Math.sin(ts/1.8)).toFixed(3);
    rays.style.transform=`translate(-50%,-50%) rotate(${ts*0.9}deg)`;
    rays.style.opacity=(0.34+0.12*Math.sin(ts/2.2)).toFixed(3);
    for(const c of CLOUDS){const sp=+c.dataset.sp, w=+c.dataset.w, x0=+c.dataset.x0;
      let x=(x0 - ts*14*sp); const span=1080+w+240; x=((x+240)%span+span)%span-240;
      c.style.transform=`translate(${x-x0}px, ${Math.sin(ts*0.3+sp)*6}px)`;}
    // eagle soars from lower-left up toward the light
    const ep=clamp(prog*1.04,0,1);
    const ex=-180+ep*1240, ey=1360-Math.pow(ep,0.9)*1040 + Math.sin(ep*6.28)*18;
    const bank=14-ep*20, flap=1+0.16*Math.sin(ts*3.2);
    eg.style.transform=`translate(${ex}px,${ey}px) rotate(${bank}deg) scaleY(${flap})`;
    eg.style.opacity=clamp(Math.min(ep/0.04,(1.03-ep)/0.05),0,1).toFixed(3);
    for(const f of FE){const pr=frac(ts/(+f.dataset.dur)+ +f.dataset.ph);
      f.style.top=(-40+pr*2020)+'px';
      f.style.transform=`translateX(${Math.sin(pr*6.28+ +f.dataset.ph*8)*(+f.dataset.sway)}px) rotate(${pr*260}deg)`;
      f.style.opacity=(Math.sin(pr*Math.PI)*0.5).toFixed(2);}
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
    (D[1], '<div class="scene mid"><div class="jp">その翼は、<br>まだ 憶えている。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">どこまでも 高く、<br><span class="em">自由だったことを。</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="jp">だからいつか、<br><span class="big">空を、返して。</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:300px">'
           '<div class="title">Give Us Back<br>the Sky</div>'
           '<div class="orn"><i></i><b>&#10022;</b><i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Give Us Back the Sky / Rolloing all stars (Promo Short)",
  desc="その翼はまだ憶えている、どこまでも高く自由だったことを。空を、返して。Rolloing all stars の新曲「Give Us Back the Sky」。")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js)
          .replace("BLOOMFROM", str(BLOOM_FROM)).replace("BLOOMPEAK", str(BLOOM_PEAK)))

BODY = r"""
  <div id="world">
    <div id="sky"></div>
    <div id="sunbreak"></div>
    <div id="rays"></div>
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
"""

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
{BODY}
</div></div>
<audio id="bgm" src="sky-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "giveusbacksky-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote giveusbacksky-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
