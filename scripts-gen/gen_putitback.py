# -*- coding: utf-8 -*-
"""「Put It Back / Rolloing all stars」 — promo short (vertical 9:16, ~26s).

Redesigned for its own identity (no sunset landscape): a cosmic view — a small blue
Earth (from the cover's Earth sticker) glowing in a field of stars, lit from the right
by its star, its night side speckled with warm city lights. On the payoff, light floods
back across the dark side and the whole planet warms to gold: "put it back", music for
a brighter tomorrow.

On-screen text is limited to verified cover text (title / artist / the cover tagline
"Music for a Brighter Tomorrow") plus generic labels and evocative promo copy.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL for frame capture.
BGM: putitback-bgm.mp3.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CSS = r"""
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:100%;height:100%;background:#05060d;overflow:hidden}
  #wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#05060d}
  #stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform:scale(var(--s,1));transform-origin:center center;
    font-family:'Noto Serif JP',serif;background:#05060d}
  #world{position:absolute;inset:0;transform-origin:50% 68%}
  #space{position:absolute;inset:0;
    background:
      radial-gradient(ellipse 900px 700px at 74% 22%, rgba(60,52,96,.5), transparent 60%),
      radial-gradient(ellipse 800px 900px at 24% 78%, rgba(24,60,96,.42), transparent 62%),
      linear-gradient(180deg,#070912 0%,#0a0e1c 44%,#0b1020 72%,#070a14 100%)}
  .star{position:absolute;border-radius:50%;background:#fff}
  /* Earth */
  #earthglow{position:absolute;left:540px;top:1300px;width:900px;height:900px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(120,180,255,.5) 30%, rgba(90,150,235,.22) 42%, transparent 60%);filter:blur(6px)}
  #earth{position:absolute;left:540px;top:1300px;width:680px;height:680px;transform:translate(-50%,-50%);border-radius:50%;overflow:hidden;
    background:radial-gradient(circle at 74% 38%, #4aa0d8 0%, #2f78c0 32%, #1b4f92 62%, #123a72 100%)}
  .cont{position:absolute;background:#3f8a54;opacity:.88;filter:blur(2px)}
  #ct1{left:44%;top:16%;width:220px;height:180px;clip-path:polygon(30% 0,66% 12%,88% 40%,72% 66%,86% 90%,50% 100%,24% 78%,8% 44%,18% 18%)}
  #ct2{left:8%;top:44%;width:250px;height:210px;background:#3c8250;clip-path:polygon(24% 6%,60% 0,80% 26%,66% 52%,84% 82%,44% 100%,12% 72%,0 40%)}
  #ct3{left:56%;top:56%;width:200px;height:170px;background:#4e8a48;clip-path:polygon(20% 10%,58% 0,92% 30%,74% 60%,80% 92%,40% 88%,10% 60%)}
  #ct4{left:30%;top:2%;width:150px;height:120px;background:#4f8f52;clip-path:polygon(30% 0,74% 18%,88% 56%,54% 90%,18% 62%,6% 26%)}
  #clouds{position:absolute;inset:0;opacity:.32;filter:blur(2px);
    background:
      radial-gradient(ellipse 110px 66px at 32% 28%, rgba(255,255,255,.8), transparent 72%),
      radial-gradient(ellipse 120px 74px at 64% 22%, rgba(255,255,255,.65), transparent 74%),
      radial-gradient(ellipse 100px 64px at 52% 58%, rgba(255,255,255,.7), transparent 74%),
      radial-gradient(ellipse 96px 60px at 80% 62%, rgba(255,255,255,.55), transparent 76%),
      radial-gradient(ellipse 104px 62px at 22% 70%, rgba(255,255,255,.55), transparent 76%)}
  #night{position:absolute;inset:0;
    background:radial-gradient(circle at 80% 36%, transparent 26%, rgba(3,7,20,.45) 54%, rgba(2,5,16,.9) 82%)}
  #lights{position:absolute;inset:0;opacity:.9}
  .clight{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffd98a,#ff9a3c 60%,transparent 78%)}
  #warmwash{position:absolute;inset:0;opacity:0;mix-blend-mode:screen;
    background:radial-gradient(circle at 42% 60%, rgba(255,210,130,.9), rgba(255,180,90,.4) 44%, transparent 74%)}
  #rim{position:absolute;left:540px;top:1300px;width:684px;height:684px;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;
    background:radial-gradient(circle at 80% 37%, transparent 60%, rgba(190,225,255,.5) 71%, rgba(150,205,255,0) 80%)}
  /* the star (sun) */
  #starSun{position:absolute;left:1010px;top:520px;width:340px;height:340px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(255,252,236,1) 0%, rgba(255,232,170,.7) 26%, rgba(255,200,120,.28) 50%, transparent 72%)}
  #starCore{position:absolute;left:1010px;top:520px;width:70px;height:70px;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle,#fff,#fff2cf 60%,#ffdf9a);box-shadow:0 0 60px 26px rgba(255,224,150,.6)}
  .dust{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff,transparent 70%);opacity:0;z-index:6}
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(120% 80% at 50% 66%, rgba(255,246,220,.95), rgba(255,214,140,.66) 36%, rgba(255,180,95,.3) 66%, transparent 100%)}
  #grain{position:absolute;inset:0;opacity:.05;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 50% 62%, transparent 44%, rgba(2,3,8,.85) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:250px 84px 0}
  .scene.low{justify-content:flex-start;padding:196px 84px 0}
  .kick{font-family:'Anton',sans-serif;font-size:34px;letter-spacing:.5em;color:#eaf0ff;text-transform:uppercase;
    text-shadow:0 2px 20px rgba(2,6,20,.95)}
  .jp{font-size:70px;line-height:1.6;font-weight:600;color:#f4f8ff;letter-spacing:.06em;
    text-shadow:0 2px 22px rgba(2,6,20,.98),0 0 46px rgba(40,80,160,.7)}
  .jp .em{color:#8fd0ff}
  .big{font-size:104px;line-height:1.24;font-weight:600;color:#fff;letter-spacing:.03em;display:inline-block;
    text-shadow:0 3px 24px rgba(2,6,20,1),0 0 56px rgba(150,205,255,.55)}
  .title{font-family:'Anton',sans-serif;font-size:134px;line-height:.96;color:#fff;letter-spacing:.03em;text-transform:uppercase;
    text-shadow:0 4px 3px rgba(2,6,20,.5),0 6px 40px rgba(2,6,20,.9),0 0 64px rgba(150,205,255,.5)}
  .artist{font-family:'Anton',sans-serif;font-size:40px;letter-spacing:.34em;color:#cfe4ff;text-transform:uppercase;font-weight:400;
    text-shadow:0 2px 16px rgba(2,6,20,.9)}
  .hand{font-family:'Caveat',cursive;font-size:60px;color:#9fd0ff;letter-spacing:.01em;text-shadow:0 2px 18px rgba(2,6,20,.9)}
  .tag{margin-top:26px;font-family:'Anton',sans-serif;font-size:28px;letter-spacing:.44em;color:#cfe4ff;text-transform:uppercase;
    text-shadow:0 2px 14px rgba(2,6,20,.9)}
  .orn{display:flex;align-items:center;justify-content:center;gap:24px;margin:26px 0 14px}
  .orn i{display:block;width:120px;height:1px;background:linear-gradient(90deg,transparent,#9fd0ff,transparent)}
  .orn b{font-size:26px;color:#9fd0ff}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#2f78c0,#9fd0ff);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(4,7,16,.86);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Anton',sans-serif;font-size:30px;letter-spacing:.4em;color:#9fd0ff;text-transform:uppercase}
  #ui h1{font-family:'Anton',sans-serif;font-size:132px;color:#fff;line-height:1;letter-spacing:.02em;text-transform:uppercase}
  #ui p{font-family:'Caveat',cursive;font-size:52px;color:#cfe4ff}
  #play{font-family:'Anton',sans-serif;font-size:34px;color:#0a1630;background:#9fd0ff;border:none;
    border-radius:100px;padding:24px 72px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 40px rgba(120,180,240,.4)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  // starfield
  const ST=[]; for(let i=0;i<150;i++){const e=document.createElement('div');e.className='star';
    const sz=1+((i*7)%3); e.style.width=sz+'px';e.style.height=sz+'px';
    e.style.left=((i*53)%100)+'%'; e.style.top=((i*97)%78)+'%';
    e.style.opacity=(0.3+((i*13)%60)/100).toFixed(2);
    e.dataset.ph=((i*29)%100)/100; e.dataset.amp=0.2+((i*11)%50)/100;
    if(i%17===0){e.style.width='3px';e.style.height='3px';e.style.boxShadow='0 0 8px 2px rgba(200,220,255,.7)';}
    world.insertBefore(e,document.getElementById('earthglow'));ST.push(e);}
  // city lights on the night side
  const lights=document.getElementById('lights'); const CL=[];
  const lp=[[24,50],[18,60],[30,64],[14,44],[22,72],[34,54],[12,54],[26,40],[20,80],[38,68],[16,36],[28,76]];
  lp.forEach((p,i)=>{const e=document.createElement('div');e.className='clight';const sz=4+(i%3)*2;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=p[0]+'%';e.style.top=p[1]+'%';
    e.dataset.ph=((i*19)%100)/100;lights.appendChild(e);CL.push(e);});
  // stardust
  const DU=[]; for(let i=0;i<20;i++){const e=document.createElement('div');e.className='dust';const sz=2+(i%3)*2;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=((i*37)%100)+'%';
    e.dataset.dur=10+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=30+((i*17)%70);
    stage.appendChild(e);DU.push(e);}
  const clouds=document.getElementById('clouds'),warmwash=document.getElementById('warmwash'),
        night=document.getElementById('night'),starCore=document.getElementById('starCore'),
        bloom=document.getElementById('bloom'),bar=document.getElementById('bar');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/900,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    world.style.transform=`scale(${1+0.07*prog}) translateY(${-prog*10}px)`;
    for(const s of ST){const ph=+s.dataset.ph, amp=+s.dataset.amp;
      s.style.opacity=(0.3+amp*(0.5+0.5*Math.sin(ts*1.6+ph*6.28))).toFixed(3);}
    clouds.style.transform=`rotate(${ts*1.4}deg)`;   // slow weather drift
    starCore.style.opacity=(0.9+0.1*Math.sin(ts*2)).toFixed(3);
    // warmth returns to the planet on the payoff
    const warm=clamp((t-(BLOOM_FROM-1400))/3000,0,1);
    warmwash.style.opacity=(warm*0.5).toFixed(3);
    night.style.opacity=(1-warm*0.42).toFixed(3);      // night side lifts into light
    for(const c of CL){const ph=+c.dataset.ph;
      c.style.opacity=((0.5+0.5*Math.sin(ts*3+ph*6.28))*(1-warm*0.4)).toFixed(3);}
    for(const d of DU){const pr=frac(ts/(+d.dataset.dur)+ +d.dataset.ph);
      d.style.top=(1900-pr*1900)+'px';
      d.style.transform=`translateX(${Math.sin(pr*6.28+ +d.dataset.ph*8)*(+d.dataset.sway)}px)`;
      d.style.opacity=(Math.sin(pr*Math.PI)*0.5).toFixed(2);}
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
    (D[1], '<div class="scene mid"><div class="jp">ちいさな、<br>青い星。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">傷ついても、<br><span class="em">まだ 廻っている。</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="jp">だからもう一度、<br><span class="big">あるべき場所へ。</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:250px">'
           '<div class="title">Put It<br>Back</div>'
           '<div class="orn"><i></i><b>&#10022;</b><i></i></div>'
           '<div class="artist">Rolloing all stars</div>'
           '<div class="hand" style="margin-top:18px">Music for a Brighter Tomorrow</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Put It Back / Rolloing all stars (Promo Short)",
  desc="ちいさな青い星。傷ついても、まだ廻っている。だからもう一度、あるべき場所へ。Rolloing all stars「Put It Back」— Music for a Brighter Tomorrow.")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js)
          .replace("BLOOMFROM", str(BLOOM_FROM)).replace("BLOOMPEAK", str(BLOOM_PEAK)))

BODY = r"""
  <div id="world">
    <div id="space"></div>
    <div id="earthglow"></div>
    <div id="earth">
      <div id="ct1" class="cont"></div><div id="ct2" class="cont"></div>
      <div id="ct3" class="cont"></div><div id="ct4" class="cont"></div>
      <div id="clouds"></div>
      <div id="night"></div>
      <div id="lights"></div>
      <div id="warmwash"></div>
    </div>
    <div id="rim"></div>
    <div id="starSun"></div>
    <div id="starCore"></div>
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
"""

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
{BODY}
</div></div>
<audio id="bgm" src="putitback-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "putitback-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote putitback-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
