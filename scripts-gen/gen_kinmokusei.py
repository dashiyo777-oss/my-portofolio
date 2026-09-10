# -*- coding: utf-8 -*-
"""「十月の金木犀 / 花明り」 — YouTube promo short (warm autumn first-love ballad).
For a 15+ audience: a golden-hour hillside lane — osmanthus in bloom, orange petals
drifting, a leaning bicycle and a gas lamp, a young couple walking hand in hand down
toward the sunset city. Carries verified lyric lines (rights-holder supplied).
Unified engine (renderAt). BGM: kinmokusei-bgm.mp3 (33s chorus segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#2a1c0e;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:#f6ecc8;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:linear-gradient(#e2a460 0%,#eebc70 24%,#f6cf82 40%,#ffe1a2 52%,#f0b878 66%,#caa060 82%,#8a6a40 100%)}
  #sunglow{position:absolute;left:62%;top:46%;transform:translate(-50%,-50%);width:820px;height:640px;
    background:radial-gradient(ellipse at center, rgba(255,240,200,.9), rgba(255,214,120,.4) 40%, transparent 70%)}
  #sun{position:absolute;left:62%;top:47%;transform:translate(-50%,-50%);width:180px;height:180px;border-radius:50%;
    background:radial-gradient(circle,#fff6e0,#ffe6a8 60%,rgba(255,214,120,0) 74%)}
  .cloud{position:absolute;height:56px;border-radius:60px;background:rgba(255,214,150,.5);opacity:.6;filter:blur(9px)}
  #city{position:absolute;left:0;top:46%;width:100%;height:8%;background:linear-gradient(#9a7852,#7a5c3a);
    clip-path:polygon(0 60%,8% 60%,8% 40%,12% 40%,12% 58%,18% 58%,18% 30%,21% 30%,21% 54%,28% 54%,28% 44%,34% 44%,34% 62%,40% 62%,40% 36%,44% 36%,44% 56%,50% 56%,50% 46%,56% 46%,56% 60%,62% 60%,62% 34%,66% 34%,66% 56%,72% 56%,72% 42%,78% 42%,78% 60%,84% 60%,84% 38%,90% 38%,90% 56%,96% 56%,96% 48%,100% 48%,100% 100%,0 100%)}
  #river{position:absolute;left:32%;top:53%;width:36%;height:5%;background:linear-gradient(rgba(255,224,150,.7),rgba(255,200,110,.3));filter:blur(2px)}
  /* hillside lane */
  #wallL{position:absolute;left:0;top:50%;width:34%;height:50%;background:linear-gradient(100deg,#5a4630,#3a2c1c);
    clip-path:polygon(0 0,100% 22%,64% 100%,0 100%)}
  #wallR{position:absolute;right:0;top:50%;width:30%;height:50%;background:linear-gradient(-100deg,#6a5238,#46341f);
    clip-path:polygon(0 26%,100% 0,100% 100%,40% 100%)}
  #path{position:absolute;left:50%;top:52%;transform:translateX(-50%);width:100%;height:48%;
    background:linear-gradient(#c89a58 0%,#c69652 40%,#a87e42 100%);clip-path:polygon(43% 0,57% 0,100% 100%,0 100%)}
  #pathlight{position:absolute;left:50%;top:52%;transform:translateX(-50%);width:100%;height:48%;
    background:linear-gradient(rgba(255,224,150,.5),transparent 60%);clip-path:polygon(46% 0,54% 0,78% 100%,22% 100%);pointer-events:none}
  /* osmanthus (upper-left) */
  #leaves{position:absolute;left:-40px;top:-30px;width:520px;height:520px;
    background:radial-gradient(circle at 40% 30%, rgba(40,54,26,.9), transparent 66%)}
  .kmok{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffc03a,#e89010);opacity:0;box-shadow:0 0 4px rgba(240,150,20,.5)}
  /* lamp */
  #lamppole{position:absolute;left:398px;top:640px;width:8px;height:360px;background:#2a2014}
  #lampglow{position:absolute;left:360px;top:600px;width:180px;height:180px;border-radius:50%;
    background:radial-gradient(circle,rgba(255,206,110,.7),transparent 66%)}
  #lampbulb{position:absolute;left:388px;top:604px;width:30px;height:40px;border-radius:8px;
    background:radial-gradient(circle,#fff0c8,#ffbf5e 60%,#e0902a);box-shadow:0 0 26px 8px rgba(255,190,90,.6)}
  /* bicycle (lower-left) */
  #bike{position:absolute;left:118px;bottom:150px;z-index:3;opacity:.92}
  .fpetal{position:absolute;width:16px;height:11px;border-radius:60% 0 60% 0;background:#e89a24;opacity:.85;z-index:2}
  /* couple (walking away, down the lane) */
  #cprim{position:absolute;left:486px;top:980px;width:120px;height:150px;z-index:4;filter:blur(.4px)}
  #cprim>*{background:rgba(255,220,150,.5)!important}
  #couple{position:absolute;left:484px;top:978px;width:120px;height:150px;z-index:5}
  .person{position:absolute;bottom:0;background:#2a1c10}
  #pman{left:6px;width:52px;height:150px;clip-path:polygon(34% 0,66% 0,74% 16%,66% 30%,72% 60%,64% 100%,52% 64%,48% 100%,36% 60%,28% 30%,34% 16%)}
  #pwoman{right:4px;width:54px;height:132px;clip-path:polygon(36% 0,64% 0,72% 16%,66% 32%,80% 100%,20% 100%,34% 32%,28% 16%)}
  #chands{position:absolute;left:54px;bottom:74px;width:16px;height:8px;background:#2a1c10;z-index:6}
  .petal{position:absolute;width:16px;height:11px;border-radius:60% 0 60% 0;background:#f2a828;opacity:0}
  .mote{position:absolute;width:6px;height:6px;border-radius:50%;background:radial-gradient(circle,#fff0c8,#e8b050 60%,transparent 70%);opacity:0}
  #grain{position:absolute;inset:0;opacity:.07;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px;z-index:8}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:8;
    background:radial-gradient(120% 96% at 50% 42%, transparent 52%, rgba(60,36,12,.5) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
    text-align:center;padding:120px 70px 0;opacity:0;z-index:10}
  .scene.mid{justify-content:center;padding-top:0}
  .kick{font-size:28px;letter-spacing:.5em;color:#fff2d6;font-weight:600;text-transform:uppercase;margin-bottom:20px;
    text-shadow:0 2px 14px rgba(90,50,10,.9)}
  .title{font-size:118px;line-height:1.14;font-weight:600;color:#fff4dc;letter-spacing:.1em;
    text-shadow:0 3px 22px rgba(80,44,8,.95),0 0 46px rgba(120,70,20,.6)}
  .orn{display:flex;align-items:center;justify-content:center;gap:22px;margin:28px 0 18px;color:#ffe6b0}
  .orn i{display:block;width:140px;height:1px;background:linear-gradient(90deg,transparent,#ffe6b0,transparent)}
  .orn b{font-size:38px;color:#ffdf9a}
  .artist{font-size:56px;letter-spacing:.36em;color:#fff0d2;font-weight:500;text-shadow:0 2px 16px rgba(80,44,8,.9)}
  .lyric{font-size:62px;line-height:1.7;font-weight:600;color:#fff6e2;letter-spacing:.05em;
    text-shadow:0 3px 20px rgba(70,38,6,1),0 0 40px rgba(60,32,4,.85)}
  .lyric .em{color:#ffdf8a}
  .tag{margin-top:32px;font-size:28px;letter-spacing:.44em;color:#fff2d6;text-transform:uppercase;text-shadow:0 2px 14px rgba(90,50,10,.9)}
  #bar{position:absolute;left:0;bottom:0;height:6px;width:0;background:linear-gradient(90deg,#e8901a,#ffdf8a);opacity:.9;z-index:11}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(60,36,14,.82);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 70px;text-align:center}
  #ui .k{font-size:28px;letter-spacing:.44em;color:#ffdf9a;text-transform:uppercase}
  #ui h1{font-size:100px;font-weight:600;color:#fff4dc;line-height:1.12;letter-spacing:.08em}
  #ui p{font-size:44px;letter-spacing:.34em;color:#fff0d2}
  #play{font-family:'Noto Serif JP',serif;font-size:38px;font-weight:600;color:#4a2c0c;background:#ffdf9a;border:none;
    border-radius:100px;padding:26px 74px;cursor:pointer;letter-spacing:.14em;box-shadow:0 10px 40px rgba(255,200,110,.4)}
  #play:hover{background:#ffe9b8}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  // clouds
  const CL=[]; [['16%','14%',300],['54%','8%',360],['32%','24%',240]].forEach((c,i)=>{const e=document.createElement('div');
    e.className='cloud';e.style.left=c[0];e.style.top=c[1];e.style.width=c[2]+'px';stage.appendChild(e);CL.push({e,i});});
  // osmanthus flower cluster (upper-left)
  const KM=[]; for(let i=0;i<90;i++){const e=document.createElement('div');e.className='kmok';
    const r=Math.sqrt((i*997)%100/100)*300; const a=((i*137.5)%360)*Math.PI/180;
    const x=40+Math.cos(a)*r*0.9; const y=-10+Math.sin(a)*r*0.7 + (i%5)*6;
    const sz=6+((i*7)%8);e.style.left=x+'px';e.style.top=y+'px';e.style.width=sz+'px';e.style.height=sz+'px';
    e.dataset.ph=((i*13)%100)/100;stage.appendChild(e);KM.push(e);}
  // fallen petals scattered on the lane
  for(let i=0;i<12;i++){const e=document.createElement('div');e.className='fpetal';
    e.style.left=(360+((i*97)%360))+'px';e.style.top=(1500+((i*53)%320))+'px';
    e.style.transform=`rotate(${(i*47)%360}deg) scale(${0.8+(i%3)*0.3})`;stage.appendChild(e);}
  // couple rim clone
  const couple=document.getElementById('couple'),cprim=document.getElementById('cprim');
  [...couple.children].forEach(c=>{const a=c.cloneNode();a.style.transform=(c.style.transform||'')+' translateX(3px)';cprim.appendChild(a);});
  // petals + motes
  const PET=[]; for(let i=0;i<20;i++){const e=document.createElement('div');e.className='petal';e.style.left=((i*43)%100)+'%';
    e.dataset.dur=6+((i*37)%40)/10;e.dataset.ph=((i*29)%100)/100;e.dataset.sway=40+((i*17)%50);e.style.zIndex=7;stage.appendChild(e);PET.push(e);}
  const MO=[]; for(let i=0;i<18;i++){const e=document.createElement('div');e.className='mote';e.style.left=((i*61)%100)+'%';
    e.dataset.dur=8+((i*47)%40)/10;e.dataset.ph=((i*31)%100)/100;e.style.zIndex=7;stage.appendChild(e);MO.push(e);}
  const sun=document.getElementById('sun'),sunglow=document.getElementById('sunglow'),lampbulb=document.getElementById('lampbulb'),
        lampglow=document.getElementById('lampglow'),bar=document.getElementById('bar');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/880,(en-t)/600),0,1);}
  function flick(ts){return 0.9+0.1*Math.sin(ts*5.5);}
  window.renderAt=function(t){
    const ts=t/1000;
    sun.style.transform=`translate(-50%,-50%) scale(${1+0.03*Math.sin(ts/2.4)})`;
    sunglow.style.opacity=(0.85+0.15*Math.sin(ts/2.0)).toFixed(3);
    lampbulb.style.opacity=flick(ts).toFixed(3); lampglow.style.opacity=(0.85*flick(ts)).toFixed(3);
    for(const c of CL){c.e.style.transform=`translateX(${Math.sin(ts/12+c.i)*20+ts*3}px)`;}
    for(const e of KM){const ph=+e.dataset.ph;e.style.opacity=(0.7+0.3*Math.sin(ts*1.3+ph*6.28)).toFixed(2);
      e.style.transform=`translate(${Math.sin(ts*0.8+ph*3)*3}px,${Math.sin(ts*1.0+ph*4)*2}px)`;}
    for(const p of PET){const pr=frac(ts/(+p.dataset.dur)+ +p.dataset.ph);p.style.top=(-40+pr*1980)+'px';
      p.style.transform=`translateX(${Math.sin(pr*6.28+ +p.dataset.ph*6)*(+p.dataset.sway)}px) rotate(${pr*420}deg)`;
      p.style.opacity=(Math.sin(pr*Math.PI)*0.85).toFixed(2);}
    for(const m of MO){const pr=frac(ts/(+m.dataset.dur)+ +m.dataset.ph);m.style.top=(1760-pr*1500)+'px';
      m.style.opacity=(Math.sin(pr*Math.PI)*0.55).toFixed(2);}
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
    (4600, '<div class="scene"><div class="kick">New Single</div></div>'),
    (7000, '<div class="scene"><div class="title">十月の金木犀</div>'
           '<div class="orn"><i></i><b>&#10047;</b><i></i></div>'
           '<div class="artist">花明り</div></div>'),
    (6400, '<div class="scene mid"><div class="lyric">金木犀、ゆれる街角。<br><span class="em">香りがそっと、言葉に変わる。</span></div></div>'),
    (6400, '<div class="scene mid"><div class="lyric">ひとことにして<br><span class="em">「大好きです」。</span><br>世界中が、金色に染まる。</div></div>'),
    (5600, '<div class="scene"><div class="title">十月の金木犀</div>'
           '<div class="orn"><i></i><b>&#10047;</b><i></i></div>'
           '<div class="artist">花明り</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="十月の金木犀 / 花明り (Promo Short)",
  desc="金木犀の香りが、半年ぶんの想いを言葉に変える。花明りの新曲「十月の金木犀」。",
  k="花明り", ep="十月の金木犀", tagline="花明り")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sunglow"></div>
  <div id="sun"></div>
  <div id="city"></div>
  <div id="river"></div>
  <div id="wallL"></div>
  <div id="wallR"></div>
  <div id="path"></div>
  <div id="pathlight"></div>
  <div id="leaves"></div>
  <div id="lampglow"></div>
  <div id="lamppole"></div>
  <div id="lampbulb"></div>
  <svg id="bike" width="300" height="200" viewBox="0 0 300 200"><g fill="none" stroke="#231910" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><circle cx="64" cy="142" r="52"/><circle cx="232" cy="142" r="52"/><path d="M64 142 L104 74 L150 142 L232 142 L168 74 L104 74 M150 142 L168 74 M104 74 L86 66 M168 74 L186 72"/></g></svg>
  <div id="cprim"></div>
  <div id="couple"><div id="pman" class="person"></div><div id="pwoman" class="person"></div><div id="chands"></div></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="vig"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">花明り</div>
    <h1>十月の金木犀</h1>
    <p>New Single</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="kinmokusei-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "kinmokusei-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote kinmokusei-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
