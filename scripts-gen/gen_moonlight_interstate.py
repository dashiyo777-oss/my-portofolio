# -*- coding: utf-8 -*-
"""「Moonlight on the Interstate -Signal-」 — YouTube promo short (night road-trip rock).
Signal series, original take: a moonlit interstate — wet highway rushing forward toward
a glowing city, full moon, a convertible of friends, a "NEXT EXIT ANYWHERE" sign.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
On-screen words are verified from the cover (title / Signal / NEXT EXIT ANYWHERE).
BGM: moonlight-interstate-bgm.mp3 (33s segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#060c1c;overflow:hidden}
  body{font-family:Georgia,'Times New Roman','Noto Serif JP',serif;color:#efe6cf;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:#0a1428}
  #sky{position:absolute;left:0;top:0;width:100%;height:46%;
    background:linear-gradient(#08122c 0%,#0d1c40 52%,#16305e 82%,#294b74 100%)}
  .star{position:absolute;width:3px;height:3px;border-radius:50%;background:#dfe8ff;opacity:0}
  .cloud{position:absolute;height:52px;border-radius:60px;background:#20365c;opacity:.5;filter:blur(7px)}
  #moon{position:absolute;left:800px;top:150px;width:180px;height:180px;border-radius:50%;
    background:radial-gradient(circle at 42% 40%, #fbf6e6 0%, #efe6cf 44%, #b9b49a 74%, rgba(150,146,120,0) 86%);
    box-shadow:0 0 70px 24px rgba(240,236,207,.4)}
  #moon::after{content:"";position:absolute;inset:0;border-radius:50%;
    background:radial-gradient(circle at 60% 36%, rgba(150,150,120,.4) 0 6%,transparent 8%),
              radial-gradient(circle at 40% 62%, rgba(150,150,120,.35) 0 5%,transparent 7%)}
  #city{position:absolute;left:0;top:38%;width:100%;height:10%;background:#0a1530;
    clip-path:polygon(0 60%,6% 60%,6% 34%,10% 34%,10% 58%,15% 58%,15% 22%,18% 22%,18% 54%,24% 54%,24% 40%,29% 40%,29% 64%,34% 64%,34% 30%,38% 30%,38% 56%,43% 56%,43% 42%,48% 42%,48% 100%,0 100%)}
  .clight{position:absolute;width:4px;height:4px;background:#ffcf82;opacity:0;border-radius:1px}
  /* road */
  #road{position:absolute;left:0;top:43%;width:100%;height:57%;background:#0b1428;overflow:hidden;
    clip-path:polygon(48% 0,52% 0,100% 100%,0 100%)}
  #road::before{content:"";position:absolute;inset:0;
    background:linear-gradient(#12203c 0%, #0e1830 40%, #0a1226 100%)}
  #roadsheen{position:absolute;left:0;top:43%;width:100%;height:57%;overflow:hidden;
    clip-path:polygon(48% 0,52% 0,100% 100%,0 100%);pointer-events:none}
  #moonrefl{position:absolute;left:50%;top:0;transform:translateX(-50%);width:70px;height:100%;
    background:linear-gradient(rgba(240,236,207,.0),rgba(200,210,230,.28) 40%,rgba(160,190,230,.12));filter:blur(6px)}
  .dash{position:absolute;left:50%;transform:translateX(-50%);background:#e8c34a;border-radius:3px;
    box-shadow:0 0 10px rgba(232,195,74,.5)}
  .head{position:absolute;border-radius:2px;background:#fff;opacity:0;filter:blur(1px)}
  /* highway sign */
  #sign{position:absolute;left:760px;top:560px;width:270px;height:170px;background:#1c6b3c;border:5px solid #eef3ea;
    border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.5);padding:22px 18px 0;color:#f2f7f0;text-align:center}
  #sign .a{font-family:'Arial Narrow',Helvetica,sans-serif;font-weight:700;font-size:38px;letter-spacing:.04em;line-height:1.1}
  #sign .b{font-family:'Arial Narrow',Helvetica,sans-serif;font-weight:700;font-size:44px;letter-spacing:.03em;margin-top:6px}
  #sign .arw{font-size:44px;line-height:1;margin-top:2px}
  #signpost{position:absolute;left:882px;top:730px;width:12px;height:150px;background:#20303f}
  /* car (rear view, foreground) */
  #car{position:absolute;left:50%;bottom:70px;transform:translateX(-50%);width:660px;height:470px;z-index:5}
  .cx{position:absolute;background:#05070e}
  #c-body{left:20px;bottom:0;width:620px;height:250px;border-radius:40px 40px 26px 26px;background:linear-gradient(#0a0f1c,#05070e);
    box-shadow:0 -2px 0 rgba(150,180,230,.18)}
  #c-deck{left:70px;bottom:210px;width:520px;height:120px;border-radius:30px 30px 0 0;background:#070a14}
  #c-wsL{left:150px;bottom:300px;width:150px;height:110px;background:#080c16;transform:skewX(8deg);border-radius:8px}
  #c-wsR{right:150px;bottom:300px;width:150px;height:110px;background:#080c16;transform:skewX(-8deg);border-radius:8px}
  .tl{position:absolute;bottom:56px;width:150px;height:34px;border-radius:8px;background:linear-gradient(#ff6a4a,#e11208);
    box-shadow:0 0 30px 8px rgba(240,40,20,.7)}
  #tlL{left:80px}  #tlR{right:80px}
  #plate{position:absolute;left:50%;bottom:64px;transform:translateX(-50%);width:110px;height:34px;border-radius:5px;
    background:#c9c3a8;opacity:.5}
  .pass{position:absolute;bottom:330px;border-radius:50% 50% 46% 46%;background:#04060c}
  .arm{position:absolute;width:12px;background:#04060c;border-radius:6px;transform-origin:bottom center}
  #grain{position:absolute;inset:0;opacity:.09;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(120% 92% at 50% 40%, transparent 52%, rgba(4,8,18,.72) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    text-align:center;padding:100px 80px 0;opacity:0;z-index:8}
  .scene.mid{justify-content:center;padding-top:0}
  .kick{font-family:'Arial Narrow',system-ui,sans-serif;font-size:30px;letter-spacing:.5em;color:#e8c341;font-weight:700;
    text-transform:uppercase;margin-bottom:24px}
  .title{font-style:italic;font-weight:700;font-size:118px;line-height:.98;color:#efe6cf;letter-spacing:.005em;
    text-shadow:0 3px 24px rgba(0,0,0,.7)}
  .sig{font-style:italic;font-weight:700;font-size:78px;color:#e8c341;margin-top:14px;
    text-shadow:0 2px 14px rgba(0,0,0,.6);border-bottom:4px solid #e8c341;display:inline-block;padding-bottom:6px}
  .bigsign{background:#1c6b3c;border:6px solid #eef3ea;border-radius:14px;padding:40px 60px;box-shadow:0 16px 40px rgba(0,0,0,.55);
    font-family:'Arial Narrow',Helvetica,sans-serif;color:#f2f7f0;transform:rotate(-2deg)}
  .bigsign .l1{font-weight:700;font-size:74px;letter-spacing:.04em}
  .bigsign .l2{font-weight:700;font-size:96px;letter-spacing:.03em;line-height:1}
  .bigsign .l3{font-size:80px;margin-top:6px}
  .tag{margin-top:28px;font-family:'Arial Narrow',system-ui,sans-serif;font-size:30px;letter-spacing:.44em;color:#e8c341;text-transform:uppercase;font-weight:700}
  #bar{position:absolute;left:0;bottom:0;height:7px;width:0;background:linear-gradient(90deg,#e8c341,#e11208);opacity:.9;z-index:9}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(6,12,28,.86);backdrop-filter:blur(4px);z-index:20;gap:30px;padding:0 80px;text-align:center}
  #ui .k{font-family:'Arial Narrow',system-ui,sans-serif;font-size:28px;letter-spacing:.44em;color:#e8c341;text-transform:uppercase}
  #ui h1{font-style:italic;font-size:96px;font-weight:700;color:#efe6cf;line-height:1.0}
  #ui p{font-style:italic;font-size:52px;color:#e8c341}
  #play{font-family:'Arial Narrow',system-ui,sans-serif;font-size:40px;font-weight:700;color:#0a1428;background:#e8c341;border:none;
    border-radius:100px;padding:26px 76px;cursor:pointer;letter-spacing:.12em;text-transform:uppercase;box-shadow:0 10px 40px rgba(232,195,65,.4)}
  #play:hover{background:#f2d564}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  const sky=document.getElementById('sky');
  const STAR=[]; for(let i=0;i<54;i++){const e=document.createElement('div');e.className='star';
    e.style.left=((i*47)%100)+'%';e.style.top=((i*29)%84)+'%';e.dataset.ph=((i*13)%100)/100;sky.appendChild(e);STAR.push(e);}
  const CL=[]; [['16%','12%',260],['62%','6%',300],['40%','28%',220],['80%','20%',200]].forEach((c,i)=>{const e=document.createElement('div');
    e.className='cloud';e.style.left=c[0];e.style.top=c[1];e.style.width=c[2]+'px';sky.appendChild(e);CL.push({e,i});});
  const city=document.getElementById('city'), CLI=[];
  for(let i=0;i<26;i++){const e=document.createElement('div');e.className='clight';
    e.style.left=(i*3.5)+'%';e.style.top=(20+(i*37)%60)+'%';e.dataset.ph=((i*23)%100)/100;city.appendChild(e);CLI.push(e);}
  // lane dashes (perspective forward motion)
  const road=document.getElementById('road'), DASH=[];
  for(let i=0;i<10;i++){const d=document.createElement('div');d.className='dash';road.appendChild(d);DASH.push(d);}
  // oncoming headlights
  const HL=[]; for(let i=0;i<2;i++){const h=document.createElement('div');h.className='head';road.appendChild(h);HL.push(h);}
  // passengers + arms on the car
  const car=document.getElementById('car');
  const pdefs=[[120,74,90],[250,80,96],[360,80,96],[490,74,90]]; // left,width,height (bottom fixed)
  pdefs.forEach((p,i)=>{const e=document.createElement('div');e.className='pass';e.style.left=p[0]+'px';
    e.style.width=p[1]+'px';e.style.height=p[2]+'px';car.appendChild(e);});
  const ARM=[]; [[150,-1],[560,1]].forEach((a,i)=>{const e=document.createElement('div');e.className='arm';
    e.style.left=a[0]+'px';e.style.bottom='400px';e.style.height='130px';car.appendChild(e);ARM.push({e,dir:a[1],ph:i});});
  const moon=document.getElementById('moon'),tlL=document.getElementById('tlL'),tlR=document.getElementById('tlR'),bar=document.getElementById('bar');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/820,(en-t)/560),0,1);}
  const RH=1920*0.57;  // road element height
  window.renderAt=function(t){
    const ts=t/1000;
    moon.style.boxShadow=`0 0 ${70+10*Math.sin(ts/2)}px 24px rgba(240,236,207,.4)`;
    for(const e of STAR){const ph=+e.dataset.ph;e.style.opacity=(0.3+0.6*(0.5+0.5*Math.sin(ts*1.5+ph*6.28))).toFixed(2);}
    for(const c of CL){c.e.style.transform=`translateX(${Math.sin(ts/12+c.i)*20+ts*2}px)`;}
    for(const e of CLI){const ph=+e.dataset.ph;e.style.opacity=(0.4+0.55*(0.5+0.5*Math.sin(ts*1.2+ph*6.28))).toFixed(2);}
    // dashes: p 0(horizon)->1(bottom)
    for(let i=0;i<DASH.length;i++){const p=frac(ts*0.6+i/DASH.length);const pe=Math.pow(p,1.8);
      const y=pe*RH; const sc=0.06+p*1.0;
      const d=DASH[i]; d.style.top=y+'px'; d.style.height=(70*sc)+'px'; d.style.width=(16*sc)+'px';
      d.style.opacity=(clamp(p*2.2,0,1)*0.95).toFixed(2);}
    // oncoming headlights (left lane), approach then reset
    for(let i=0;i<HL.length;i++){const p=frac(ts*0.14+i*0.02+0.3);const pe=Math.pow(p,2.0);
      const y=pe*RH*0.9; const sc=0.1+p*0.7; const cx=50-(p*14); // drift left as it nears
      const h=HL[i]; h.style.top=y+'px'; h.style.left=cx+'%'; h.style.width=(10+18*sc)+'px'; h.style.height=(6+8*sc)+'px';
      h.style.background='#fff'; h.style.boxShadow=`0 0 ${8+14*sc}px rgba(220,235,255,.9)`;
      h.style.opacity=(clamp(p*1.6,0,1)*(1-p*0.3)).toFixed(2);}
    const tp=0.7+0.3*Math.abs(Math.sin(ts*2.2));
    tlL.style.opacity=tp; tlR.style.opacity=tp;
    for(const a of ARM){a.e.style.transform=`rotate(${a.dir*(6+4*Math.sin(ts*2+a.ph))}deg)`;}
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
    (5000, '<div class="scene"><div class="kick">New Single</div></div>'),
    (8200, '<div class="scene"><div class="title">Moonlight<br>on the<br>Interstate</div>'
           '<div class="sig">Signal</div></div>'),
    (6200, '<div class="scene mid"><div class="bigsign"><div class="l1">Next Exit</div>'
           '<div class="l2">Anywhere</div><div class="l3">&#10230;</div></div></div>'),
    (9000, '<div class="scene"><div class="title" style="font-size:104px">Moonlight<br>on the Interstate</div>'
           '<div class="sig">Signal</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(
  title="Moonlight on the Interstate -Signal- (Promo Short)",
  desc="Next exit, anywhere. Moonlight on the Interstate -Signal-. A moonlit highway, wheels toward the city lights.",
  k="Signal", ep="Moonlight on the Interstate", tagline="Signal")

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
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sky"></div>
  <div id="moon"></div>
  <div id="city"></div>
  <div id="road"></div>
  <div id="roadsheen"><div id="moonrefl"></div></div>
  <div id="signpost"></div>
  <div id="sign"><div class="a">Next Exit</div><div class="b">Anywhere</div><div class="arw">&#10230;</div></div>
  <div id="car">
    <div id="c-body" class="cx"></div>
    <div id="c-deck" class="cx"></div>
    <div id="c-wsL" class="cx"></div>
    <div id="c-wsR" class="cx"></div>
    <div id="tlL" class="tl"></div>
    <div id="tlR" class="tl"></div>
    <div id="plate"></div>
  </div>
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
<audio id="bgm" src="moonlight-interstate-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "moonlight-interstate-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote moonlight-interstate-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
