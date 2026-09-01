# -*- coding: utf-8 -*-
"""花あわせ (SAE) YouTube promo short, scored to Maron「百億年前のパズル」.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
BGM: hana-awase-maron-bgm.mp3 (34s segment of the song). Song credited on screen.
"""
import os
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  :root{--white:#fdf6ec;--gold:#d69a2a;--amber:#e0a53a;--jade:#7fae86;--gray:#a89273;--bg-dark:#241a0d;}
  html,body{height:100%;background:#100b04;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:var(--white);display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;transform:scale(var(--s,0.4));transform-origin:center center;
    background:radial-gradient(120% 78% at 50% 78%, #7a3a12 0%, #4a2c10 26%, var(--bg-dark) 55%, #150d05 82%, #0a0603 100%);
    overflow:hidden;box-shadow:0 0 120px rgba(0,0,0,.6)}
  /* starfield top, sunset glow bottom — echoes the song artwork's mood */
  #sky{position:absolute;inset:0;background:
    radial-gradient(60% 40% at 50% 92%, rgba(255,150,40,.28), transparent 70%),
    radial-gradient(120% 70% at 50% 8%, rgba(40,30,70,.55), transparent 60%)}
  .star{position:absolute;width:3px;height:3px;border-radius:50%;background:#fff;opacity:.0}
  .petal{position:absolute;width:9px;height:9px;border-radius:60% 0 60% 0;background:linear-gradient(#ffd9a0,#e0a53a);opacity:0}
  #sun{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:150px;height:150px;border-radius:50%;opacity:0;
    background:radial-gradient(circle,#fff4d6 0%,#ffcf6b 40%,#e59a2a 66%,rgba(181,102,26,0) 72%);
    box-shadow:0 0 90px 30px rgba(224,150,42,.45),0 0 200px 80px rgba(214,154,42,.22)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px;opacity:0}
  .kicker{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.42em;color:var(--gold);font-weight:600;margin-bottom:40px}
  .lead{font-size:82px;font-weight:600;line-height:1.5;letter-spacing:.03em}
  .lead .glow{color:var(--amber)}
  .ep-title{font-size:108px;font-weight:700;line-height:1.2;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.4)}
  .card-name{font-size:74px;letter-spacing:.06em;color:var(--white);font-weight:700;margin-bottom:20px}
  .badge{display:inline-block;font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.2em;color:var(--bg-dark);
    background:var(--gold);border-radius:100px;padding:10px 34px;font-weight:600;margin-bottom:48px}
  .badge.jade{background:var(--jade)}
  .line{font-size:62px;font-weight:600;line-height:1.55;color:var(--white)}
  .how{font-family:'Noto Sans JP',system-ui,sans-serif;margin-top:46px;font-size:30px;color:var(--gray);letter-spacing:.05em}
  .names{font-size:60px;line-height:1.7;color:var(--white);font-weight:600}
  .names .big{display:block;margin-top:34px;font-size:70px;color:var(--amber)}
  .cta-title{font-size:104px;font-weight:700;letter-spacing:.04em;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.4)}
  .cta-jp{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:36px;color:var(--gold);margin-top:20px;letter-spacing:.16em}
  .cta-sub{font-size:46px;color:var(--gray);margin-top:34px}
  .cta-url{margin-top:56px;font-family:'Noto Sans JP',system-ui,sans-serif;font-size:46px;color:var(--white);border:2px solid var(--gold);
    border-radius:100px;padding:22px 56px;letter-spacing:.04em;background:rgba(214,154,42,.08)}
  .cta-free{font-family:'Noto Sans JP',system-ui,sans-serif;margin-top:30px;font-size:38px;color:var(--gray);letter-spacing:.1em}
  #credit{position:absolute;left:0;right:0;top:70px;text-align:center;font-family:'Noto Sans JP',system-ui,sans-serif;
    font-size:32px;color:var(--gray);letter-spacing:.1em;opacity:0}
  #bar{position:absolute;left:0;bottom:0;height:8px;width:0;background:linear-gradient(90deg,var(--gold),var(--amber));opacity:.85}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(16,11,4,.82);
    backdrop-filter:blur(4px);z-index:20;gap:38px;padding:0 110px;text-align:center}
  #ui .kick{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.42em;color:var(--gold)}
  #ui h1{font-size:92px;font-weight:700;color:var(--white);line-height:1.15}
  #ui p{font-size:38px;color:var(--gray);line-height:1.6}
  #ui .song{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:30px;color:var(--amber)}
  #play{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:46px;font-weight:700;color:#1a1207;background:var(--gold);border:none;
    border-radius:100px;padding:30px 84px;cursor:pointer;letter-spacing:.08em;box-shadow:0 10px 40px rgba(214,154,42,.4)}
  #play:hover{background:var(--amber)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), sky=document.getElementById('sky'), sun=document.getElementById('sun');
  const STAR=[], PETAL=[];
  for(let i=0;i<46;i++){const x=((i*47)%100)/100*1080, y=((i*83)%100)/100*820;
    const e=document.createElement('div');e.className='star';e.style.left=x+'px';e.style.top=y+'px';
    e.dataset.ph=((i*29)%100)/100;e.dataset.dur=2+((i*31)%40)/10;stage.appendChild(e);STAR.push(e);}
  for(let i=0;i<16;i++){const x=((i*137.5)%100)/100*1080, dur=7+((i*53)%50)/10, phase=((i*29)%100)/100, sway=30+((i*17)%40);
    const e=document.createElement('div');e.className='petal';e.style.left=x+'px';stage.appendChild(e);
    PETAL.push({e,dur,phase,sway,x});}
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'), bar=document.getElementById('bar'), credit=document.getElementById('credit');
  let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/700,(en-t)/500),0,1);}
  window.renderAt=function(t){
    sun.style.opacity=clamp(t/1400,0,1)*0.95;
    sun.style.transform=`translateX(-50%) scale(${1+0.03*Math.sin(t/900)})`;
    for(const e of STAR){const ph=+e.dataset.ph, du=+e.dataset.dur;
      e.style.opacity=(0.25+0.6*(0.5+0.5*Math.sin(t/1000/du*6.28+ph*6.28))).toFixed(2);}
    for(const p of PETAL){const prog=frac((t/1000)/p.dur+p.phase);
      p.e.style.top=(1560-prog*1900)+'px';
      p.e.style.left=(p.x+Math.sin(prog*6.28)*p.sway)+'px';
      p.e.style.transform=`rotate(${prog*360}deg)`;
      p.e.style.opacity=(Math.sin(prog*Math.PI)*0.7).toFixed(2);}
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    // persistent song credit fades in after 1s, out at the very end
    if(credit) credit.style.opacity=(clamp((t-1000)/1200,0,1)*clamp((total-t)/800,0,1)*0.9).toFixed(2);
    if(bar) bar.style.width=(clamp(t/total,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search), ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar.style.display='none'; }
  else {
    const bgm=document.getElementById('bgm');
    document.getElementById('play').addEventListener('click',()=>{
      ui.classList.add('hide');
      try{bgm.currentTime=0;bgm.volume=.8;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent='↻ もう一度';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.8*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

def hook(t):        return f'<div class="scene"><div class="lead">{t}</div></div>'
def badge(k, ep):   return f'<div class="scene"><div class="kicker">{k}</div><div class="ep-title">{ep}</div></div>'
def card(name, dom, line, how, jade=False):
    b = "badge jade" if jade else "badge"
    return (f'<div class="scene"><div class="card-name">{name}</div><div class="{b}">{dom}</div>'
            f'<div class="line">{line}</div><div class="how">{how}</div></div>')
def names(line, big): return f'<div class="scene"><div class="names">{line}<span class="big">{big}</span></div></div>'
def cta():
    return ('<div class="scene"><div class="cta-title">冴え手帖 -SAE-</div>'
            '<div class="cta-jp">脳活道場 ｜ 花あわせ</div>'
            '<div class="cta-sub">花札で遊びながら、頭が冴える</div>'
            '<div class="cta-url">ryuzaburo7.itch.io/sae-techo</div>'
            '<div class="cta-free">&#9654; 無料でプレイ</div></div>')

scenes = [
    (4200, hook('めくるたび、<br>四季が<span class="glow">ひらく</span>。')),
    (3400, badge('冴え手帖 -SAE- 脳活道場', '花あわせ')),
    (5000, card('美しい花札', '四季の花', '四季の花を、<br>手のひらで。', '目でも楽しむ和の意匠', jade=True)),
    (5000, card('かんたんルール', '役づくり', '役を作って、<br>得点を競う。', '初めてでもすぐ遊べる')),
    (5000, card('世界番付', '“ここまで咲いた”', '自己ベストを、<br>世界と競う。', '花あわせの記録に挑戦', jade=True)),
    (3200, names('美しい札で、<br>役を組み立てる——', '遊びながら、<br>頭が冴える。')),
    (4200, cta()),
]

meta = dict(
  title="花あわせ｜冴え手帖 -SAE-（宣伝ショート・百億年前のパズル）",
  desc="四季の花を手のひらで。花札「花あわせ」で遊びながら脳が冴える 冴え手帖 -SAE-。BGM: 百億年前のパズル / Maron",
  kicker="冴え手帖 -SAE-", ep="花あわせ", tagline="花札で遊びながら、頭が冴える。",
  song="&#9834; 百億年前のパズル / Maron")

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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;600;700&family=Noto+Sans+JP:wght@500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="sky"></div>
  <div id="sun"></div>
  <div id="scenes"></div>
  <div id="credit">{meta['song']}</div>
  <div id="bar"></div>
  <div id="ui">
    <div class="kick">{meta['kicker']}</div>
    <h1>{meta['ep']}</h1>
    <p>{meta['tagline']}</p>
    <div class="song">{meta['song']}</div>
    <button id="play">&#9654; 再生</button>
  </div>
</div></div>
<audio id="bgm" src="hana-awase-maron-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT_DIR, "hana-awase-maron.html"), "w", encoding="utf-8").write(html)
print(f"wrote hana-awase-maron.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes)")
