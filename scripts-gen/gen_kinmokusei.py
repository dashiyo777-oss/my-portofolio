# -*- coding: utf-8 -*-
"""「十月の金木犀 / 花明り」 — YouTube promo short (warm autumn first-love ballad).
Emotion-first remake: golden-hour light and depth — soft bokeh, a sun bloom, osmanthus
petals swirling in the light, and a couple from behind (she rests her head on his
shoulder) rim-lit by the sunset. A slow push-in, and at "世界中が金色に染まる" the whole
frame blooms gold. Verified title/artist + rights-holder-supplied lyric lines.
Unified engine (renderAt). BGM: kinmokusei-bgm.mp3 (33s chorus segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#2a180a;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:#fff2d8;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:#160c05}
  /* --- world (everything that slowly pushes in) --- */
  #world{position:absolute;inset:-6%;transform-origin:52% 46%}
  #sky{position:absolute;inset:0;
    background:linear-gradient(#7a3f18 0%,#b46a26 20%,#e39a38 38%,#ffce6e 50%,#ffe39a 56%,#f0ad4c 70%,#b0702e 86%,#5e3a1a 100%)}
  #sunbloom{position:absolute;left:52%;top:47%;transform:translate(-50%,-50%);width:1000px;height:900px;border-radius:50%;
    background:radial-gradient(circle, rgba(255,248,224,.95), rgba(255,224,150,.5) 30%, rgba(255,196,96,.16) 55%, transparent 74%)}
  #rays{position:absolute;left:52%;top:47%;width:1700px;height:1700px;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg, rgba(255,236,180,.10) 0deg 6deg, transparent 6deg 18deg);
    -webkit-mask-image:radial-gradient(circle,transparent 8%,#000 34%,transparent 66%);
            mask-image:radial-gradient(circle,transparent 8%,#000 34%,transparent 66%)}
  .bok{position:absolute;border-radius:50%;opacity:0;
    background:radial-gradient(circle at 40% 38%, rgba(255,240,200,.9), rgba(255,206,120,.5) 55%, rgba(255,180,90,0) 78%)}
  .branch{position:absolute;width:560px;height:520px;
    background:radial-gradient(circle at 44% 40%, rgba(38,44,22,.86), rgba(38,44,22,.3) 52%, transparent 72%)}
  #brL{left:-150px;top:-140px} #brR{right:-170px;top:-180px;transform:scaleX(-1)}
  .kmok{position:absolute;border-radius:50%;background:radial-gradient(circle,#ffc63e,#e8901a);opacity:0}
  /* hero osmanthus branch (foreground, backlit by the sun) */
  #cglow{position:absolute;left:50%;top:1360px;transform:translateX(-50%);width:640px;height:300px;border-radius:50%;
    background:radial-gradient(ellipse at center, rgba(255,214,140,.42), transparent 66%);filter:blur(8px)}
  #hbranch{position:absolute;left:0;top:640px;width:1080px;height:1280px;z-index:5;transform-origin:46% 100%}
  #hbranch svg{position:absolute;inset:0;overflow:visible}
  .leaf{position:absolute;background:#1d1207;border-radius:0 100% 0 100%;transform:translate(-50%,-50%) rotate(var(--r))}
  .leaf.rim{background:linear-gradient(135deg, rgba(255,226,150,.8), rgba(255,186,96,.05) 62%);z-index:6;filter:blur(.4px)}
  .fcl{position:absolute;transform:translate(-50%,-50%);z-index:7}
  .fglow{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;
    background:radial-gradient(circle, rgba(255,214,120,.9), rgba(255,170,70,.32) 46%, transparent 72%);filter:blur(3px)}
  .flo{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 38%, #ffe6a0, #f2a326 62%, #d9820f);
    box-shadow:0 0 8px rgba(255,190,90,.85)}
  /* petals + motes */
  .petal{position:absolute;border-radius:62% 0 62% 0;
    background:linear-gradient(140deg,#ffd06a,#ef9a1e);box-shadow:0 0 6px rgba(240,150,20,.4);opacity:0;z-index:6}
  .mote{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff4d6,#f0bf6a 55%,transparent 72%);opacity:0;z-index:6}
  /* bloom + grade */
  #bloom{position:absolute;inset:0;pointer-events:none;z-index:12;opacity:0;
    background:radial-gradient(120% 90% at 52% 46%, rgba(255,240,200,.95), rgba(255,214,140,.7) 40%, rgba(255,190,110,.35) 70%, rgba(255,180,90,.12) 100%)}
  #grain{position:absolute;inset:0;opacity:.06;pointer-events:none;mix-blend-mode:overlay;z-index:9;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;z-index:9;
    background:radial-gradient(120% 100% at 52% 40%, transparent 50%, rgba(50,26,6,.55) 100%)}
  /* text */
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
    text-align:center;padding:0 96px 300px;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:460px 84px 0}
  .kick{font-size:26px;letter-spacing:.56em;color:#fff0d0;font-weight:500;text-transform:uppercase;
    text-shadow:0 2px 18px rgba(70,38,8,.9)}
  .lyric{font-size:66px;line-height:1.66;font-weight:500;color:#fff6e4;letter-spacing:.07em;
    text-shadow:0 2px 26px rgba(60,30,4,.98),0 0 48px rgba(60,30,4,.7)}
  .lyric .em{color:#ffd97e}
  .big{font-size:106px;line-height:1.24;font-weight:600;color:#fff8ea;letter-spacing:.02em;display:inline-block;
    text-shadow:0 3px 30px rgba(50,24,4,1),0 0 60px rgba(255,210,130,.5)}
  .title{font-size:120px;line-height:1.12;font-weight:600;color:#fff8ea;letter-spacing:.12em;
    text-shadow:0 3px 30px rgba(50,24,4,.98),0 0 56px rgba(255,214,140,.55)}
  .orn{display:flex;align-items:center;justify-content:center;gap:22px;margin:30px 0 16px;color:#ffe6ac}
  .orn i{display:block;width:130px;height:1px;background:linear-gradient(90deg,transparent,#ffe6ac,transparent)}
  .orn b{font-size:34px;color:#ffdb8a}
  .artist{font-size:54px;letter-spacing:.4em;color:#fff2d2;font-weight:500;text-shadow:0 2px 18px rgba(60,30,6,.9)}
  .tag{margin-top:30px;font-size:26px;letter-spacing:.5em;color:#ffe6ac;text-transform:uppercase;text-shadow:0 2px 14px rgba(70,38,8,.9)}
  #bar{position:absolute;left:0;bottom:0;height:5px;width:0;background:linear-gradient(90deg,#e8901a,#ffdf8a);opacity:.85;z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(50,26,8,.8);backdrop-filter:blur(4px);z-index:20;gap:28px;padding:0 90px;text-align:center}
  #ui .k{font-size:26px;letter-spacing:.5em;color:#ffdb8a;text-transform:uppercase}
  #ui h1{font-size:100px;font-weight:600;color:#fff8ea;line-height:1.12;letter-spacing:.1em}
  #ui p{font-size:44px;letter-spacing:.36em;color:#fff2d2}
  #play{font-family:'Noto Serif JP',serif;font-size:38px;font-weight:600;color:#4a2c0c;background:#ffdb8a;border:none;
    border-radius:100px;padding:26px 74px;cursor:pointer;letter-spacing:.14em;box-shadow:0 10px 40px rgba(255,200,110,.4)}
  #play:hover{background:#ffe9b8}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v), sm=v=>v*v*(3-2*v);
  // big soft bokeh (depth)
  const BOK=[]; const bd=[[180,760,150,10],[860,600,120,26],[300,520,90,16],[720,880,170,8],[520,420,70,30],
    [140,1040,110,20],[900,980,130,12],[420,1180,90,22],[640,560,60,32],[240,700,60,28],
    [800,460,80,24],[500,900,110,14],[360,980,70,26],[700,1220,100,18]];
  bd.forEach((d,i)=>{const e=document.createElement('div');e.className='bok';e.style.left=d[0]+'px';e.style.top=d[1]+'px';
    e.style.width=d[2]+'px';e.style.height=d[2]+'px';e.style.filter='blur('+d[3]+'px)';
    e.dataset.ph=((i*23)%100)/100;e.dataset.amp=8+(i%4)*6;world.appendChild(e);BOK.push(e);});
  // osmanthus flowers on the two branches
  const KM=[]; [document.getElementById('brL'),document.getElementById('brR')].forEach((br,bi)=>{
    for(let i=0;i<46;i++){const e=document.createElement('div');e.className='kmok';
      const a=((i*137.5)%360)*Math.PI/180, r=Math.sqrt(((i*613)%100)/100)*220;
      const x=250+Math.cos(a)*r, y=210+Math.sin(a)*r*0.9; const sz=6+((i*7)%8);
      e.style.left=x+'px';e.style.top=y+'px';e.style.width=sz+'px';e.style.height=sz+'px';
      e.dataset.ph=((i*13)%100)/100;br.appendChild(e);KM.push(e);}});
  // hero osmanthus branch: a clean bezier stem, leaves, and glowing blossom clusters
  const HB=document.getElementById('hbranch');
  const P0=[318,1280],P1=[300,930],P2=[648,600],P3=[770,150];
  const B=u=>{const m=1-u;return[m*m*m*P0[0]+3*m*m*u*P1[0]+3*m*u*u*P2[0]+u*u*u*P3[0],
                                   m*m*m*P0[1]+3*m*m*u*P1[1]+3*m*u*u*P2[1]+u*u*u*P3[1]];};
  const Tan=u=>{const m=1-u;const dx=3*m*m*(P1[0]-P0[0])+6*m*u*(P2[0]-P1[0])+3*u*u*(P3[0]-P2[0]);
                const dy=3*m*m*(P1[1]-P0[1])+6*m*u*(P2[1]-P1[1])+3*u*u*(P3[1]-P2[1]);
                return Math.atan2(dy,dx)*180/Math.PI;};
  // stem as one clean tapered path (thick near base, thin at tip)
  const svgNS='http://www.w3.org/2000/svg';
  const svg=document.createElementNS(svgNS,'svg');svg.setAttribute('viewBox','0 0 1080 1280');
  let d='M'+P0[0]+' '+P0[1]+' C '+P1[0]+' '+P1[1]+', '+P2[0]+' '+P2[1]+', '+P3[0]+' '+P3[1];
  const stem=document.createElementNS(svgNS,'path');stem.setAttribute('d',d);stem.setAttribute('fill','none');
  stem.setAttribute('stroke','#1d1207');stem.setAttribute('stroke-width','15');stem.setAttribute('stroke-linecap','round');
  const stemR=document.createElementNS(svgNS,'path');stemR.setAttribute('d',d);stemR.setAttribute('fill','none');
  stemR.setAttribute('stroke','rgba(255,220,140,.5)');stemR.setAttribute('stroke-width','4');stemR.setAttribute('stroke-linecap','round');
  stemR.setAttribute('transform','translate(3,-2)');
  svg.appendChild(stem);svg.appendChild(stemR);HB.appendChild(svg);
  // leaves in opposite pairs along the stem
  const LU=[0.14,0.26,0.37,0.47,0.56,0.65,0.73,0.81,0.88];
  LU.forEach((u,i)=>{const p=B(u),ang=Tan(u),len=150-90*u,off=26+18*(1-u);
    [[-1, ang-58],[1, ang+58]].forEach(([s,r],k)=>{
      const nx=p[0]+Math.cos((ang+90*s)*Math.PI/180)*off, ny=p[1]+Math.sin((ang+90*s)*Math.PI/180)*off;
      const mk=(cls,extra)=>{const e=document.createElement('div');e.className='leaf'+cls;
        e.style.width=(len*0.34)+'px';e.style.height=len+'px';e.style.left=nx+'px';e.style.top=ny+'px';
        e.style.setProperty('--r',(r-45+extra)+'deg');HB.appendChild(e);return e;};
      mk('',0); mk(' rim',0);});});
  // glowing blossom clusters near the sunlit upper branch
  const FCL=[]; const FU=[0.50,0.60,0.69,0.77,0.84,0.90,0.955];
  FU.forEach((u,i)=>{const p=B(u),spread=54-30*u;
    const cl=document.createElement('div');cl.className='fcl';cl.style.left=p[0]+'px';cl.style.top=p[1]+'px';
    const g=document.createElement('div');g.className='fglow';const gs=150-70*u;g.style.width=gs+'px';g.style.height=gs+'px';cl.appendChild(g);
    const n=7+((i*3)%4);
    for(let j=0;j<n;j++){const f=document.createElement('div');f.className='flo';const a=(j*137.5)*Math.PI/180,rr=Math.sqrt((j+1)/n)*spread;
      const fs=9+((i*5+j*7)%7);f.style.width=fs+'px';f.style.height=fs+'px';
      f.style.left=(Math.cos(a)*rr)+'px';f.style.top=(Math.sin(a)*rr*0.9)+'px';
      f.style.transform='translate(-50%,-50%)';cl.appendChild(f);}
    cl.dataset.ph=((i*29)%100)/100;HB.appendChild(cl);FCL.push(cl);});
  // petals (osmanthus) swirling + motes
  const PET=[]; for(let i=0;i<32;i++){const e=document.createElement('div');e.className='petal';
    const fg=i%4===0; const sz=fg?24:13; e.style.width=sz+'px';e.style.height=(sz*0.7)+'px';
    if(fg)e.style.filter='blur(2px)'; e.style.left=((i*37)%100)+'%';
    e.dataset.dur=6+((i*29)%50)/10;e.dataset.ph=((i*53)%100)/100;e.dataset.sway=50+((i*17)%90);e.dataset.fg=fg?1:0;
    stage.appendChild(e);PET.push(e);}
  const MO=[]; for(let i=0;i<20;i++){const e=document.createElement('div');e.className='mote';const sz=4+(i%3)*3;
    e.style.width=sz+'px';e.style.height=sz+'px';e.style.left=((i*61)%100)+'%';
    e.dataset.dur=8+((i*41)%40)/10;e.dataset.ph=((i*31)%100)/100;stage.appendChild(e);MO.push(e);}
  const sunbloom=document.getElementById('sunbloom'),rays=document.getElementById('rays'),
        cglow=document.getElementById('cglow'),bloom=document.getElementById('bloom'),bar=document.getElementById('bar');
  const scenes=SCENES, BLOOM_FROM=BLOOMFROM, BLOOM_PEAK=BLOOMPEAK;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/1000,(en-t)/700),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    // slow cinematic push-in + tiny drift
    world.style.transform=`scale(${1+0.10*prog}) translate(${Math.sin(ts/8)*6}px, ${-prog*14}px)`;
    const grow=1+0.04*Math.sin(ts/2.2);
    sunbloom.style.transform=`translate(-50%,-50%) scale(${grow})`;
    sunbloom.style.opacity=(0.9+0.1*Math.sin(ts/1.8)).toFixed(3);
    rays.style.transform=`translate(-50%,-50%) rotate(${ts*1.6}deg)`;
    cglow.style.opacity=(0.7+0.3*Math.sin(ts/2.0)).toFixed(3);
    for(const b of BOK){const ph=+b.dataset.ph, amp=+b.dataset.amp;
      b.style.opacity=(0.22+0.5*(0.5+0.5*Math.sin(ts*0.6+ph*6.28))).toFixed(3);
      b.style.transform=`translate(${Math.sin(ts*0.5+ph*6)*amp}px, ${-((ts*6+ph*40)%60)}px)`;}
    for(const e of KM){const ph=+e.dataset.ph;e.style.opacity=(0.55+0.4*Math.sin(ts*1.1+ph*6.28)).toFixed(2);}
    for(const p of PET){const pr=frac(ts/(+p.dataset.dur)+ +p.dataset.ph), fg=+p.dataset.fg;
      p.style.top=(-60+pr*2040)+'px';
      p.style.transform=`translateX(${Math.sin(pr*6.28+ +p.dataset.ph*8)*(+p.dataset.sway)}px) rotate(${pr*(fg?520:380)}deg)`;
      p.style.opacity=(Math.sin(pr*Math.PI)*(fg?0.75:0.9)).toFixed(2);}
    for(const m of MO){const pr=frac(ts/(+m.dataset.dur)+ +m.dataset.ph);m.style.top=(1900-pr*1700)+'px';
      m.style.transform=`translateX(${Math.sin(pr*7+ +m.dataset.ph)*30}px)`;m.style.opacity=(Math.sin(pr*Math.PI)*0.6).toFixed(2);}
    // golden bloom around the emotional payoff
    let bl=0;
    if(t>BLOOM_FROM){ const up=clamp((t-BLOOM_FROM)/(BLOOM_PEAK-BLOOM_FROM),0,1);
      bl=sm(up)*0.6; if(t>BLOOM_PEAK) bl=0.6-clamp((t-BLOOM_PEAK)/1600,0,1)*0.28; }
    bloom.style.opacity=bl.toFixed(3);
    // the branch sways gently; blossoms breathe with light
    HB.style.transform=`rotate(${Math.sin(ts/3.4)*0.9}deg)`;
    for(const c of FCL){const ph=+c.dataset.ph;c.style.opacity=(0.72+0.28*Math.sin(ts*1.3+ph*6.28)).toFixed(3);}
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

# scene timeline
D = [3600, 5600, 5800, 6400, 6600]
S1,S2,S3,S4,S5 = 0, D[0], D[0]+D[1], D[0]+D[1]+D[2], D[0]+D[1]+D[2]+D[3]
BLOOM_FROM = S4 + 2600      # bloom starts mid-payoff line
BLOOM_PEAK = S4 + D[3] - 200  # peaks as the line lands / title arrives

scenes = [
    (D[0], '<div class="scene"><div class="kick">New Single</div></div>'),
    (D[1], '<div class="scene mid"><div class="lyric">夕暮れの帰り道、<br>ふいに香る 金木犀。</div></div>'),
    (D[2], '<div class="scene mid"><div class="lyric">香りがそっと、<br><span class="em">言葉に変わる。</span></div></div>'),
    (D[3], '<div class="scene mid"><div class="lyric">ひとことにして<br><span class="big em">「大好きです」</span><br>世界中が、金色に染まる。</div></div>'),
    (D[4], '<div class="scene mid"><div class="title">十月の金木犀</div>'
           '<div class="orn"><i></i><b>&#10047;</b><i></i></div>'
           '<div class="artist">花明り</div><div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="十月の金木犀 / 花明り (Promo Short)",
  desc="夕暮れにふいに香る金木犀。半年ぶんの想いが、ひとことになる。花明りの新曲「十月の金木犀」。",
  k="花明り", ep="十月の金木犀")

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
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="world">
    <div id="sky"></div>
    <div id="sunbloom"></div>
    <div id="rays"></div>
    <div id="brL" class="branch"></div>
    <div id="brR" class="branch"></div>
    <div id="cglow"></div>
    <div id="hbranch"></div>
  </div>
  <div id="bloom"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="scenes"></div>
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
print(f"wrote kinmokusei-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; bloom {BLOOM_FROM}->{BLOOM_PEAK})")
