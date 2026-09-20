# -*- coding: utf-8 -*-
"""「Long Way Down to Morning / Rolling all stars」 — promo short (9:16, ~26s).

Matches the jacket: a dark, warm late-night dive bar. A hanging lamp pools amber light
over the counter; a lone figure sits hunched with a whiskey glass and a bottle; a classic
jukebox glows on the right; red/amber neon (LIVE MUSIC, LAST CALL 2:00 AM) hums on the
wall; a rain-streaked window shows cold blue city lights. Smoke drifts, the jukebox
breathes, and on the payoff the room warms as the title lands. Slow, moody, bluesy
Americana.

On-screen text uses verified cover text (title / artist / LIVE MUSIC / LAST CALL 2:00 AM)
plus generic labels and evocative promo copy — no invented lyrics.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL. BGM: lwd-bgm.mp3.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CSS = r"""
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:100%;height:100%;background:#0a0705;overflow:hidden}
  #wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0a0705}
  #stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform:scale(var(--s,1));transform-origin:center center;
    font-family:'Roboto Slab',serif;background:#0d0906}
  #world{position:absolute;inset:0;transform-origin:50% 46%}
  #room{position:absolute;inset:0;background:
     radial-gradient(ellipse 760px 560px at 47% 30%, rgba(90,60,32,.9), rgba(40,26,14,.6) 44%, transparent 72%),
     linear-gradient(180deg,#160f08 0%,#1c130a 40%,#140d07 72%,#0b0704 100%)}
  .frame{position:absolute;background:#20160d;border:2px solid rgba(120,86,40,.3);box-shadow:inset 0 0 12px rgba(0,0,0,.6)}
  /* window with rain + cold city bokeh */
  #window{position:absolute;left:392px;top:470px;width:340px;height:420px;overflow:hidden;
    background:linear-gradient(180deg,#12233a,#0e1a2c);border:14px solid #17100a;box-shadow:0 0 40px rgba(0,0,0,.6)}
  .citylight{position:absolute;border-radius:50%;filter:blur(3px)}
  #blinds{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(10,12,18,.5) 0 12px, transparent 12px 26px);opacity:.5}
  #rain{position:absolute;inset:0;background:repeating-linear-gradient(74deg, rgba(150,190,220,.10) 0 1px, transparent 1px 9px)}
  /* hanging lamp */
  #lampcord{position:absolute;left:540px;top:0;width:4px;height:150px;background:#0a0805;transform:translateX(-50%)}
  #lamp{position:absolute;left:540px;top:120px;width:120px;height:70px;transform:translateX(-50%);border-radius:50% 50% 46% 46%;
    background:radial-gradient(ellipse at 50% 30%, #ffd891, #d78a34 60%, #6c3f12);box-shadow:0 0 60px 20px rgba(255,180,90,.45)}
  #lampcone{position:absolute;left:540px;top:150px;width:520px;height:900px;transform:translateX(-50%);pointer-events:none;
    background:linear-gradient(180deg, rgba(255,190,100,.28), rgba(255,170,80,.06) 50%, transparent 80%);
    clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);filter:blur(8px)}
  /* neon */
  .neon{position:absolute;font-family:'Montserrat',sans-serif;font-weight:800;text-transform:uppercase;line-height:1.05}
  #neonLive{left:56px;top:344px;font-size:44px;letter-spacing:.06em;color:#ff6a72;
    text-shadow:0 0 6px #ff2b39,0 0 16px #ff2b39,0 0 34px #ff2b39,0 0 60px rgba(255,43,57,.7)}
  #neonLiveBox{left:36px;top:326px;width:210px;height:150px;border:4px solid rgba(255,60,74,.5);border-radius:12px;
    box-shadow:0 0 18px rgba(255,43,57,.5),inset 0 0 18px rgba(255,43,57,.3)}
  #neonLast{right:44px;top:214px;font-size:30px;letter-spacing:.12em;color:#ffd27a;text-align:center;
    text-shadow:0 0 6px #ff9a2e,0 0 16px #ff9a2e,0 0 30px rgba(255,154,46,.7)}
  #neonBud{left:70px;top:150px;font-size:26px;letter-spacing:.1em;color:#8fd0ff;
    text-shadow:0 0 6px #3fb0e0,0 0 16px #3fb0e0,0 0 28px rgba(63,176,224,.6)}
  /* jukebox */
  #jukebox{position:absolute;left:812px;top:560px;width:250px;height:600px;z-index:4}
  #jbGlow{position:absolute;left:125px;top:280px;width:520px;height:520px;transform:translate(-50%,-50%);pointer-events:none;border-radius:50%;
    background:radial-gradient(circle, rgba(255,176,80,.5), rgba(255,120,60,.16) 44%, transparent 70%)}
  #jbBody{position:absolute;left:0;top:0;width:250px;height:600px;border-radius:120px 120px 18px 18px;
    background:linear-gradient(180deg,#4a2f14 0%,#6a4218 36%,#3c2510 100%);box-shadow:inset 0 0 30px rgba(0,0,0,.6),0 10px 40px rgba(0,0,0,.6)}
  #jbArch{position:absolute;left:34px;top:30px;width:182px;height:210px;border-radius:100px 100px 12px 12px;
    background:radial-gradient(ellipse at 50% 70%, #ffe7ac, #ff9a3a 52%, #b85e14 100%);box-shadow:0 0 30px rgba(255,170,80,.6)}
  .jbtube{position:absolute;top:34px;width:20px;height:230px;border-radius:12px;
    background:linear-gradient(180deg,#ff2b39,#ff9a2e 50%,#ffd27a);box-shadow:0 0 14px rgba(255,90,60,.7)}
  #jbTL{left:20px} #jbTR{right:20px}
  #jbDisplay{position:absolute;left:38px;top:262px;width:174px;height:70px;border-radius:8px;background:#120a06;
    box-shadow:inset 0 0 12px rgba(255,180,90,.4);border:2px solid rgba(120,80,36,.5)}
  #jbGrille{position:absolute;left:34px;top:348px;width:182px;height:210px;border-radius:10px;
    background:repeating-linear-gradient(90deg,#2a1a0d 0 8px,#3c2612 8px 16px);box-shadow:inset 0 0 16px rgba(0,0,0,.6)}
  /* bar counter + items */
  #bar{position:absolute;left:0;top:1190px;width:1080px;height:730px;z-index:6;
    background:linear-gradient(180deg,#3a2312 0%,#24160b 30%,#160d06 100%)}
  #baredge{position:absolute;left:0;top:1178px;width:1080px;height:26px;z-index:6;
    background:linear-gradient(180deg,#6b4520,#2c1a0c);box-shadow:0 -2px 10px rgba(255,170,90,.25)}
  #barref{position:absolute;left:0;top:1204px;width:1080px;height:300px;z-index:6;pointer-events:none;opacity:.5;
    background:linear-gradient(180deg, rgba(255,160,80,.28), transparent 70%);mix-blend-mode:screen;filter:blur(6px)}
  #bottle{position:absolute;left:706px;top:980px;width:60px;height:250px;z-index:7;border-radius:26px 26px 10px 10px;
    background:linear-gradient(180deg,#0e0a06 0%,#0e0a06 30%,#7a4a16 46%,#c67e28 70%,#5c3712 100%);box-shadow:0 0 18px rgba(255,160,70,.3)}
  #bottleneck{position:absolute;left:726px;top:940px;width:20px;height:56px;z-index:7;background:#0e0a06;border-radius:6px}
  #glass{position:absolute;left:512px;top:1120px;width:64px;height:74px;z-index:7;border-radius:8px 8px 12px 12px;
    background:linear-gradient(180deg, rgba(230,150,60,.35) 0 40%, #d9862b 40%, #a5611a 100%);box-shadow:0 0 20px rgba(255,160,70,.5);border:2px solid rgba(255,200,130,.25)}
  #ashtray{position:absolute;left:636px;top:1176px;width:96px;height:26px;z-index:7;border-radius:50%;background:#1a1108;box-shadow:inset 0 3px 6px rgba(0,0,0,.7)}
  /* the man (side, hunched over the bar) */
  #manrim{position:absolute;left:120px;top:612px;width:360px;height:600px;z-index:7;filter:blur(1px)}
  #manrim>*{background:linear-gradient(270deg, rgba(255,180,90,.6), rgba(255,150,80,.05) 55%)!important}
  #man{position:absolute;left:116px;top:610px;width:360px;height:600px;z-index:8}
  .mn{position:absolute;background:#0b0805}
  #m-back{left:0;top:150px;width:250px;height:450px;clip-path:polygon(0 100%,0 34%,22% 12%,54% 2%,74% 8%,86% 26%,84% 62%,70% 100%)}
  #m-head{left:150px;top:96px;width:120px;height:126px;border-radius:52% 54% 50% 50%;transform:rotate(20deg)}
  #m-hair{left:150px;top:80px;width:132px;height:96px;border-radius:60% 60% 40% 40%;transform:rotate(18deg);background:#0b0805}
  #m-arm{left:150px;top:300px;width:230px;height:70px;border-radius:36px;transform:rotate(9deg)}
  .smoke{position:absolute;border-radius:50%;background:radial-gradient(circle, rgba(220,200,180,.16), transparent 70%);filter:blur(10px);z-index:8;opacity:0}
  .mote{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffdca0,#ffб printed);opacity:0;z-index:8}
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(120% 80% at 76% 46%, rgba(255,206,130,.85), rgba(255,168,80,.5) 40%, rgba(255,130,60,.18) 70%, transparent 100%)}
  #grain{position:absolute;inset:0;opacity:.08;pointer-events:none;mix-blend-mode:overlay;z-index:10;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:10;
    background:radial-gradient(120% 100% at 50% 44%, transparent 42%, rgba(4,3,1,.9) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:250px 84px 0}
  .scene.low{justify-content:flex-start;padding:196px 84px 0}
  .kick{font-family:'Montserrat',sans-serif;font-size:32px;letter-spacing:.5em;color:#ffdca0;text-transform:uppercase;font-weight:700;
    text-shadow:0 2px 20px rgba(0,0,0,.95)}
  .en{font-family:'Roboto Slab',serif;font-size:66px;line-height:1.4;font-weight:700;color:#ffedd2;letter-spacing:.01em;
    text-shadow:0 2px 22px rgba(0,0,0,.98),0 0 44px rgba(60,30,6,.7)}
  .en .em{color:#ffb24a}
  .ensub{font-family:'Montserrat',sans-serif;font-size:30px;letter-spacing:.16em;color:#c9a877;font-weight:500;margin-top:18px;text-transform:uppercase}
  .big{font-family:'Roboto Slab',serif;font-size:150px;line-height:1.0;font-weight:900;color:#ffb24a;letter-spacing:.02em;display:inline-block;
    text-shadow:0 3px 26px rgba(0,0,0,1),0 0 56px rgba(255,150,60,.5)}
  .title{font-family:'Roboto Slab',serif;font-size:104px;line-height:1.02;font-weight:900;color:#ffedd2;letter-spacing:.01em;
    text-shadow:0 3px 26px rgba(0,0,0,1),0 0 56px rgba(255,160,70,.4)}
  .artist{font-family:'Montserrat',sans-serif;font-size:40px;letter-spacing:.3em;color:#ffcf92;text-transform:uppercase;font-weight:700;margin-top:18px;
    text-shadow:0 2px 16px rgba(0,0,0,.9)}
  .tag{margin-top:24px;font-family:'Montserrat',sans-serif;font-size:26px;letter-spacing:.44em;color:#e8b878;text-transform:uppercase;font-weight:700;
    text-shadow:0 2px 14px rgba(0,0,0,.9)}
  .orn{display:flex;align-items:center;justify-content:center;gap:20px;margin:22px 0 12px}
  .orn i{display:block;width:110px;height:1px;background:linear-gradient(90deg,transparent,#e8b878,transparent)}
  .orn b{font-size:26px;color:#ffb24a}
  #bar2{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#8a4a16,#ffcf8a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(10,7,4,.9);backdrop-filter:blur(4px);z-index:20;gap:26px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Montserrat',sans-serif;font-size:28px;letter-spacing:.4em;color:#ffcf92;text-transform:uppercase;font-weight:700}
  #ui h1{font-family:'Roboto Slab',serif;font-size:110px;font-weight:900;color:#ffedd2;line-height:1.0}
  #ui p{font-family:'Montserrat',sans-serif;font-size:34px;letter-spacing:.2em;color:#e8b878;text-transform:uppercase}
  #play{font-family:'Montserrat',sans-serif;font-weight:800;font-size:30px;color:#1a0f06;background:#ffb24a;border:none;
    border-radius:8px;padding:22px 66px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v),
        rnd=v=>frac(Math.sin(v*12.9898)*43758.5453);
  try{['104px "Roboto Slab"','150px "Roboto Slab"','44px "Montserrat"']
      .forEach(f=>document.fonts.load(f));}catch(e){}
  // wall frames (photos/posters)
  const wall=document.createElement('div');world.insertBefore(wall,document.getElementById('window'));
  const fr=[[60,470,120,90],[210,500,90,120],[760,360,110,150],[900,540,120,90],[300,300,90,70],[60,640,90,110],[930,700,110,140]];
  fr.forEach(d=>{const e=document.createElement('div');e.className='frame';e.style.left=d[0]+'px';e.style.top=d[1]+'px';e.style.width=d[2]+'px';e.style.height=d[3]+'px';wall.appendChild(e);});
  // city bokeh in the window
  const win=document.getElementById('window');const cl=[[40,60,26,'#ffd27a'],[120,40,18,'#8fd0ff'],[220,90,22,'#ffb060'],[80,160,16,'#8fd0ff'],[260,180,20,'#ffd27a'],[170,120,14,'#ffffff'],[300,60,16,'#8fd0ff']];
  cl.forEach(d=>{const e=document.createElement('div');e.className='citylight';e.style.left=d[0]+'px';e.style.top=d[1]+'px';e.style.width=d[2]+'px';e.style.height=d[2]+'px';e.style.background=d[3];e.style.opacity=.6;win.insertBefore(e,document.getElementById('blinds'));});
  // jukebox tubes already in DOM; add smoke + motes
  const SMK=[]; for(let i=0;i<5;i++){const e=document.createElement('div');e.className='smoke';const w=140+i*40;e.style.width=w+'px';e.style.height=w+'px';
    e.style.left=(420+i*40)+'px';e.dataset.dur=10+i*2;e.dataset.ph=(i*23%100)/100;stage.appendChild(e);SMK.push(e);}
  const MO=[]; for(let i=0;i<20;i++){const e=document.createElement('div');e.className='mote';const sz=3+(i%3)*2;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.background='radial-gradient(circle,#ffdca0,#ff9a3a 55%,transparent 74%)';e.style.left=((i*41)%100)+'%';
    e.dataset.dur=8+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=20+((i*17)%50);e.dataset.y0=760+((i*37)%520);stage.appendChild(e);MO.push(e);}
  // man rim clone
  const man=document.getElementById('man'),manrim=document.getElementById('manrim');
  [...man.children].forEach(c=>{const a=c.cloneNode();manrim.appendChild(a);});
  const jbGlow=document.getElementById('jbGlow'),jbArch=document.getElementById('jbArch'),lamp=document.getElementById('lamp'),
        neonLive=document.getElementById('neonLive'),neonLiveBox=document.getElementById('neonLiveBox'),
        bloom=document.getElementById('bloom'),bar2=document.getElementById('bar2'),glass=document.getElementById('glass');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/900,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    world.style.transform=`scale(${1+0.05*prog}) translateY(${-prog*8}px)`;
    const jb=0.8+0.2*Math.sin(ts*1.1);
    jbGlow.style.opacity=jb.toFixed(3); jbArch.style.filter=`brightness(${(0.9+0.2*Math.sin(ts*1.3)).toFixed(3)})`;
    lamp.style.filter=`brightness(${(0.95+0.05*Math.sin(ts*2.1)).toFixed(3)})`;
    // neon flicker (characterful buzz on the red sign)
    const fl=(rnd(Math.floor(ts*12))<0.06)?0.4:1; neonLive.style.opacity=fl; neonLiveBox.style.opacity=fl;
    glass.style.filter=`brightness(${(0.9+0.15*Math.sin(ts*1.6)).toFixed(3)})`;
    for(const s of SMK){const pr=frac(ts/(+s.dataset.dur)+ +s.dataset.ph);
      s.style.top=(1180-pr*900)+'px';s.style.transform=`translateX(${Math.sin(pr*6.28+ +s.dataset.ph*6)*40}px) scale(${0.6+pr*1.4})`;
      s.style.opacity=(Math.sin(pr*Math.PI)*0.5).toFixed(3);}
    for(const m of MO){const pr=frac(ts/(+m.dataset.dur)+ +m.dataset.ph);
      m.style.top=((+m.dataset.y0)-pr*360)+'px';m.style.transform=`translateX(${Math.sin(pr*6.28+ +m.dataset.ph*8)*(+m.dataset.sway)}px)`;
      m.style.opacity=(Math.sin(pr*Math.PI)*0.5).toFixed(3);}
    let bl=0;
    if(t>BLOOM_FROM){ const up=clamp((t-BLOOM_FROM)/(BLOOM_PEAK-BLOOM_FROM),0,1);
      bl=up*up*(3-2*up)*0.5; if(t>BLOOM_PEAK) bl=0.5-clamp((t-BLOOM_PEAK)/1500,0,1)*0.24; }
    bloom.style.opacity=bl.toFixed(3);
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    if(bar2) bar2.style.width=(clamp(prog,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search), ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar2.style.display='none'; }
  else {
    const bgm=document.getElementById('bgm');
    document.getElementById('play').addEventListener('click',()=>{
      ui.classList.add('hide');
      try{bgm.currentTime=0;bgm.volume=.92;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent='REPLAY';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.92*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

# scene timeline
D = [3000, 5200, 5400, 6000, 6600]
S3 = D[0]+D[1]+D[2]
BLOOM_FROM = S3 + 2400
BLOOM_PEAK = S3 + D[3] - 200

scenes = [
    (D[0], '<div class="scene low"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="en">Live music.<br>Last call.</div></div>'),
    (D[2], '<div class="scene mid"><div class="big" style="font-size:120px">2 A.M.</div>'
           '<div class="ensub">the loneliest hour of the night</div></div>'),
    (D[3], '<div class="scene mid"><div class="en">It&rsquo;s a long way down,<br><span class="em">to morning.</span></div></div>'),
    (D[4], '<div class="scene mid" style="padding-top:236px">'
           '<div class="title">Long Way Down<br>to Morning</div>'
           '<div class="orn"><i></i><b>&#9733;</b><i></i></div>'
           '<div class="artist">Rolling all stars</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="Long Way Down to Morning / Rolling all stars (Promo Short)",
  desc="Live music, last call, 2 A.M. It's a long way down to morning. Rolling all stars, new single \"Long Way Down to Morning\".")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js).replace("BLOOMFROM", str(BLOOM_FROM)).replace("BLOOMPEAK", str(BLOOM_PEAK)))

BODY = r"""
  <div id="world">
    <div id="room"></div>
    <div id="window"><div id="blinds"></div><div id="rain"></div></div>
    <div id="lampcord"></div><div id="lampcone"></div><div id="lamp"></div>
    <div id="neonBud" class="neon">Budweiser</div>
    <div id="neonLiveBox"></div><div id="neonLive" class="neon">Live<br>Music</div>
    <div id="neonLast" class="neon">Last Call<br>2:00 AM</div>
    <div id="jbGlow"></div>
    <div id="jukebox">
      <div id="jbBody"></div><div id="jbArch"></div>
      <div id="jbTL" class="jbtube"></div><div id="jbTR" class="jbtube"></div>
      <div id="jbDisplay"></div><div id="jbGrille"></div>
    </div>
    <div id="bottleneck"></div><div id="bottle"></div>
    <div id="baredge"></div><div id="bar"></div><div id="barref"></div>
    <div id="glass"></div><div id="ashtray"></div>
    <div id="manrim"></div>
    <div id="man"><div id="m-back" class="mn"></div><div id="m-hair" class="mn"></div><div id="m-head" class="mn"></div><div id="m-arm" class="mn"></div></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
  <div id="bar2"></div>
  <div id="ui">
    <div class="k">Rolling all stars</div>
    <h1>Long Way Down to Morning</h1>
    <p>New Single</p>
    <button id="play">&#9654; Play</button>
  </div>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700;900&family=Montserrat:wght@500;700;800&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
{BODY}
</div></div>
<audio id="bgm" src="lwd-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "longway-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote longway-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
