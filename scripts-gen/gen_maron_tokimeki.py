# -*- coding: utf-8 -*-
"""「トキメキ上書き中 / Maron」 — YouTube promo short (Y2K kawaii pixel-pop).
Maron, original take: a "LOVE.EXE update" love song — retro OS window loading to 100%,
pixel hearts, sticky-note confessions, a daily mission checklist, a heart countdown.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
On-screen words are verified from the cover (title / Maron / UPDATE LOVE.EXE / the notes / mission / 3..2..1).
BGM: tokimeki-bgm.mp3 (32s segment).
"""
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;background:#ffe3f4;overflow:hidden}
  body{font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN',system-ui,sans-serif;color:#6a3d8f;
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    overflow:hidden;background:linear-gradient(158deg,#ffd9ef 0%,#ffcfeb 26%,#f0d9ff 62%,#ddc4ff 100%)}
  .spark{position:absolute;color:#fff;opacity:0;text-shadow:0 0 8px rgba(255,140,200,.8);font-size:28px}
  .ph{position:absolute;color:#ff5fa2;opacity:0;font-size:34px;text-shadow:2px 2px 0 #fff}
  .petal{position:absolute;width:20px;height:14px;border-radius:60% 0 60% 0;background:#ffbfe0;opacity:0}
  /* decorative sticky notes (verified phrases) */
  .note{position:absolute;padding:16px 18px;font-size:26px;font-weight:700;line-height:1.4;color:#8a4fae;
    box-shadow:3px 5px 10px rgba(150,90,190,.28);transform:rotate(-4deg);max-width:270px;border-radius:4px}
  .note.p{background:#ffd4ea}.note.y{background:#fff3b0;color:#a07a2a}.note.b{background:#cfe4ff;color:#4a6fae}.note.v{background:#e6d6ff}
  #grain{position:absolute;inset:0;opacity:.05;pointer-events:none;mix-blend-mode:overlay;
    background-image:radial-gradient(circle,#fff 1px,transparent 1px);background-size:3px 3px}
  #vig{position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 92% at 50% 46%, transparent 62%, rgba(180,120,190,.22) 100%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:0 90px;opacity:0;z-index:6}
  /* title */
  .kick{font-family:'Courier New',monospace;font-size:30px;letter-spacing:.34em;color:#ff3d8b;font-weight:700;
    background:#fff;padding:8px 22px;border:3px solid #ff5fa2;border-radius:100px;margin-bottom:34px;box-shadow:3px 3px 0 #d9b3ff}
  .title{font-size:150px;line-height:.98;font-weight:900;color:#ff2e88;letter-spacing:.02em;
    text-shadow:5px 5px 0 #8a5cf0, -2px -2px 0 #fff, 2px 2px 0 #fff;}
  .maron{font-family:Georgia,serif;font-style:italic;font-weight:700;font-size:82px;color:#ff4d94;margin-top:16px;
    text-shadow:3px 3px 0 #fff, 5px 5px 0 rgba(138,92,240,.5)}
  .maron .d{color:#b98cff}
  /* retro window */
  .win{width:720px;background:#fff6fb;border:5px solid #ff4d94;border-radius:12px;box-shadow:10px 10px 0 rgba(138,92,240,.35);overflow:hidden}
  .wtitle{background:#ff4d94;color:#fff;font-family:'Courier New',monospace;font-weight:700;font-size:34px;letter-spacing:.04em;
    padding:16px 20px;display:flex;align-items:center;justify-content:space-between}
  .wtitle .x{width:36px;height:36px;background:#fff;color:#ff4d94;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:26px}
  .wbody{padding:40px 46px 46px;text-align:center}
  .wheart{font-size:150px;color:#ff3d8b;line-height:1;text-shadow:4px 4px 0 #ffb3d4;display:inline-block}
  .wlabel{font-family:'Courier New',monospace;font-size:34px;color:#a05fc0;margin:20px 0 16px;letter-spacing:.02em}
  .wbarout{height:44px;border:4px solid #ff8dc0;border-radius:10px;background:#ffe6f4;overflow:hidden}
  .wbarfill{height:100%;width:0;background:repeating-linear-gradient(90deg,#ff4d94 0 22px,#ff77b0 22px 30px)}
  .wpct{font-family:'Courier New',monospace;font-size:34px;color:#ff3d8b;font-weight:700;margin-top:12px}
  .wdone{font-family:'Courier New',monospace;font-size:48px;color:#ff2e88;font-weight:700;margin-top:18px;letter-spacing:.02em;opacity:0}
  .wbtns{display:flex;gap:26px;justify-content:center;margin-top:30px}
  .wbtn{font-family:'Courier New',monospace;font-size:34px;font-weight:700;color:#ff3d8b;background:#ffe6f4;border:4px solid #ff8dc0;
    border-radius:8px;padding:12px 44px;box-shadow:4px 4px 0 rgba(138,92,240,.3)}
  /* mission card */
  .miss{background:#fffdf5;border:5px solid #ffb3d4;border-radius:18px;box-shadow:10px 10px 0 rgba(138,92,240,.28);padding:44px 54px;max-width:820px}
  .miss h3{font-size:56px;color:#ff3d8b;font-weight:900;margin-bottom:30px;letter-spacing:.04em}
  .miss .it{display:flex;align-items:center;gap:22px;font-size:52px;font-weight:700;color:#7a4fae;margin:16px 0;opacity:0;transform:translateX(-14px)}
  .miss .ck{width:52px;height:52px;border:5px solid #ff5fa2;border-radius:8px;color:#ff2e88;font-size:44px;display:flex;align-items:center;justify-content:center}
  .miss .up{font-size:78px;color:#ff2e88;font-weight:900;margin-top:28px;text-shadow:3px 3px 0 #ffd0e6}
  /* countdown */
  .cdlabel{font-family:'Courier New',monospace;font-size:40px;color:#8a5cf0;letter-spacing:.14em;margin-bottom:24px;
    background:#fff;padding:10px 30px;border:3px solid #b98cff;border-radius:100px}
  .cd{font-size:200px;font-weight:900;color:#ff2e88;letter-spacing:.04em;text-shadow:5px 5px 0 #8a5cf0,-2px -2px 0 #fff}
  .tag{margin-top:30px;font-family:'Courier New',monospace;font-size:32px;letter-spacing:.3em;color:#ff3d8b;font-weight:700}
  #bar{position:absolute;left:0;bottom:0;height:8px;width:0;background:repeating-linear-gradient(90deg,#ff4d94 0 20px,#ffb3d4 20px 28px);opacity:.95;z-index:9}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(255,214,238,.9);backdrop-filter:blur(4px);z-index:20;gap:30px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Courier New',monospace;font-size:30px;letter-spacing:.34em;color:#ff3d8b;font-weight:700}
  #ui h1{font-size:120px;font-weight:900;color:#ff2e88;line-height:1;text-shadow:4px 4px 0 #8a5cf0,-2px -2px 0 #fff}
  #ui p{font-family:Georgia,serif;font-style:italic;font-size:54px;color:#ff4d94}
  #play{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:40px;font-weight:900;color:#fff;background:#ff4d94;border:none;
    border-radius:100px;padding:26px 76px;cursor:pointer;letter-spacing:.1em;box-shadow:5px 5px 0 rgba(138,92,240,.4)}
  #play:hover{background:#ff2e88}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  const SP=[]; for(let i=0;i<26;i++){const e=document.createElement('div');e.className='spark';e.textContent=(i%2?'✦':'✧');
    e.style.left=((i*37)%100)+'%';e.style.top=((i*53)%100)+'%';e.dataset.ph=((i*17)%100)/100;
    e.style.fontSize=(20+(i%3)*12)+'px';stage.appendChild(e);SP.push(e);}
  const PH=[]; for(let i=0;i<16;i++){const e=document.createElement('div');e.className='ph';e.textContent='♥';
    e.style.left=((i*61)%100)+'%';e.dataset.dur=6+((i*53)%40)/10;e.dataset.ph=((i*29)%100)/100;
    e.style.fontSize=(24+(i%4)*12)+'px';stage.appendChild(e);PH.push(e);}
  const PE=[]; for(let i=0;i<14;i++){const e=document.createElement('div');e.className='petal';
    e.style.left=((i*43)%100)+'%';e.dataset.dur=7+((i*47)%40)/10;e.dataset.ph=((i*31)%100)/100;
    e.dataset.sway=30+((i*13)%40);stage.appendChild(e);PE.push(e);}
  const bar=document.getElementById('bar');
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/620,(en-t)/460),0,1);}
  const fill=document.getElementById('barfill'),pct=document.getElementById('barpct'),done=document.getElementById('barcomplete'),
        wheart=document.getElementById('wheart'),cd=document.getElementById('cdnum');
  const S2=[SCENE2START,SCENE2START+SCENE2DUR], MITEMS=[];
  window.renderAt=function(t){
    const ts=t/1000;
    for(const e of SP){const ph=+e.dataset.ph;const v=0.5+0.5*Math.sin(ts*2.2+ph*6.28);
      e.style.opacity=(v*v*0.95).toFixed(2);e.style.transform=`scale(${0.6+v*0.6}) rotate(${ts*40+ph*360}deg)`;}
    for(const e of PH){const p=frac(ts/(+e.dataset.dur)+ +e.dataset.ph);e.style.top=(1720-p*1800)+'px';
      e.style.transform=`translateX(${Math.sin(p*6.28+ +e.dataset.ph*6)*24}px) scale(${0.7+Math.sin(p*3.14)*0.4})`;
      e.style.opacity=(Math.sin(p*Math.PI)*0.85).toFixed(2);}
    for(const e of PE){const p=frac(ts/(+e.dataset.dur)+ +e.dataset.ph);e.style.top=(1760-p*1900)+'px';
      e.style.left='';e.style.transform=`translateX(${Math.sin(p*6.28+ +e.dataset.ph*6)*(+e.dataset.sway)}px) rotate(${p*360}deg)`;
      e.style.opacity=(Math.sin(p*Math.PI)*0.7).toFixed(2);}
    // update-window loading progress (scene 2 local)
    if(fill){const p=clamp((t-S2[0])/(SCENE2DUR-1600),0,1);
      fill.style.width=(p*100)+'%'; pct.textContent=Math.round(p*100)+'%';
      done.style.opacity=(p>=0.99?clamp((p-0.99)*80,0,1):0).toFixed(2);}
    if(wheart) wheart.style.transform=`scale(${1+0.09*Math.abs(Math.sin(ts*4))})`;
    if(cd){const local=t-SCENE4START; const seq=['3','2','1','♥'];
      const idx=clamp(Math.floor(local/1050),0,3); cd.textContent=seq[idx];
      const f=frac(local/1050); cd.style.transform=`scale(${1.25-0.25*Math.min(f*3,1)})`;}
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    // mission items pop in
    if(MITEMS.length){const local=t-SCENE3START;
      MITEMS.forEach((it,i)=>{const o=clamp((local-500-i*700)/500,0,1);it.style.opacity=o;it.style.transform=`translateX(${(1-o)*-14}px)`;});}
    if(bar) bar.style.width=(clamp(t/total,0,1)*100)+'%';
  };
  MITEMS.push(...document.querySelectorAll('.miss .it'));
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

D1,D2,D3,D4,D5 = 4800,8000,6400,4800,5400
S2START=D1; S3START=D1+D2; S4START=D1+D2+D3

scenes = [
    (D1, '<div class="scene"><div class="kick">NEW SINGLE</div>'
         '<div class="title">トキメキ<br>上書き中</div>'
         '<div class="maron">&#10022; Maron &#10022;</div></div>'),
    (D2, '<div class="scene"><div class="win"><div class="wtitle"><span>UPDATE LOVE.EXE</span><span class="x">&#10005;</span></div>'
         '<div class="wbody"><div class="wheart" id="wheart">&#9829;</div>'
         '<div class="wlabel">LOVE DATA LOADING...</div>'
         '<div class="wbarout"><div class="wbarfill" id="barfill"></div></div>'
         '<div class="wpct" id="barpct">0%</div>'
         '<div class="wdone" id="barcomplete">INSTALL COMPLETE! &#9829;</div>'
         '<div class="wbtns"><span class="wbtn">YES</span><span class="wbtn">OK</span></div></div></div></div>'),
    (D3, '<div class="scene"><div class="miss"><h3>今日のミッション</h3>'
         '<div class="it"><span class="ck">&#10003;</span>笑顔でいく</div>'
         '<div class="it"><span class="ck">&#10003;</span>目が合ったらOK</div>'
         '<div class="it"><span class="ck">&#10003;</span>話せたら神!!</div>'
         '<div class="up">&#9829; LOVE UP!!</div></div></div>'),
    (D4, '<div class="scene"><div class="cdlabel">カウントダウン</div>'
         '<div class="cd"><span id="cdnum">3</span></div></div>'),
    (D5, '<div class="scene"><div class="title" style="font-size:120px">トキメキ<br>上書き中</div>'
         '<div class="maron">&#10022; Maron &#10022;</div>'
         '<div class="tag">NEW SINGLE &nbsp;&#9829;</div></div>'),
]

# decorative sticky notes (verified cover phrases)
NOTES = [
  ("p","left:40px;top:150px","きみ仕様に<br>更新中♡"),
  ("y","left:60px;top:1560px;transform:rotate(3deg)","今日も好きが<br>増えた！"),
  ("b","right:50px;top:200px;transform:rotate(4deg)","このハートビート<br>インストール完了"),
  ("v","right:44px;top:1540px;transform:rotate(-3deg)","世界で1番<br>キミ仕様"),
  ("p","left:44px;top:840px;transform:rotate(-6deg)","バグでもいい<br>止まらないでよ"),
]

meta = dict(title="トキメキ上書き中 / Maron (Promo Short)",
  desc="LOVE.EXE、インストール完了。Maronのキラキラ・ピクセルポップ新曲「トキメキ上書き中」。",
  k="Maron", ep="トキメキ上書き中", tagline="Maron")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js)
  .replace("SCENE2START", str(S2START)).replace("SCENE2DUR", str(D2))
  .replace("SCENE3START", str(S3START)).replace("SCENE4START", str(S4START)))
notes_html = "".join(f'<div class="note {c}" style="{s}">{txt}</div>' for c,s,txt in NOTES)
html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@700;900&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  {notes_html}
  <div id="scenes"></div>
  <div id="grain"></div>
  <div id="vig"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">Maron</div>
    <h1>トキメキ上書き中</h1>
    <p>&#10022; New Single &#10022;</p>
    <button id="play">&#9654; Play</button>
  </div>
</div></div>
<audio id="bgm" src="tokimeki-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "tokimeki-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote tokimeki-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
