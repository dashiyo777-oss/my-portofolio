# -*- coding: utf-8 -*-
"""Generate English promo Shorts (standalone HTML) for 叡智の灯火 / Eichi no Tomoshibi.
One unified engine drives both interactive playback and deterministic ?capture=1 rendering.
"""
import os, json

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  :root{
    --white:#fdf6ec; --gold:#c8860a; --amber:#d4863a; --brown:#c47a3a;
    --gray:#a08060; --bg-dark:#2e1c0a; --bg-mid:#3a2210;
  }
  html,body{height:100%;background:#120a03;overflow:hidden}
  body{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;
    color:var(--white);display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;
    transform:scale(var(--s,0.4));transform-origin:center center;
    background:radial-gradient(120% 80% at 50% 18%, #4a2c10 0%, var(--bg-dark) 42%, #1c1005 78%, #120a03 100%);
    overflow:hidden;box-shadow:0 0 120px rgba(0,0,0,.6)}
  .ember{position:absolute;width:6px;height:6px;border-radius:50%;
    background:radial-gradient(circle,#ffd98a,#c8860a 60%,transparent 70%);opacity:0;filter:blur(.5px)}
  #flame{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:120px;height:170px;opacity:0}
  #flame .core{position:absolute;left:50%;bottom:0;transform:translateX(-50%);
    width:70px;height:120px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;
    background:linear-gradient(to top,#fff6d8,#ffcf6b 40%,#e08a2a 75%,#b5591a);
    box-shadow:0 0 60px 20px rgba(224,138,42,.55),0 0 140px 60px rgba(200,134,10,.28);transform-origin:bottom center}
  #flame .halo{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
    width:420px;height:420px;border-radius:50%;
    background:radial-gradient(circle, rgba(224,138,42,.22), transparent 60%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:0 100px;opacity:0}
  .kicker{font-family:'Montserrat',system-ui,sans-serif;font-size:30px;letter-spacing:.5em;
    color:var(--gold);font-weight:500;margin-bottom:44px;text-transform:uppercase}
  .lead{font-size:80px;font-weight:400;line-height:1.5;letter-spacing:.01em;font-style:italic}
  .lead .glow{color:var(--amber);font-style:italic}
  .ep-title{font-size:104px;font-weight:600;line-height:1.15;color:var(--white);
    text-shadow:0 0 50px rgba(200,134,10,.35)}
  .q-tag{font-family:'Montserrat',system-ui,sans-serif;font-size:26px;letter-spacing:.5em;
    color:var(--gray);margin-bottom:44px;text-transform:uppercase}
  .worry{font-size:70px;font-weight:400;line-height:1.5;color:#f4e2c4;font-style:italic}
  .worry::before{content:"\201C";color:var(--gold);opacity:.5}
  .worry::after{content:"\201D";color:var(--gold);opacity:.5}
  .sage-name{font-family:'Montserrat',system-ui,sans-serif;font-size:40px;letter-spacing:.22em;
    color:var(--gold);font-weight:600;text-transform:uppercase;margin-bottom:14px}
  .sage-era{font-family:'Montserrat',system-ui,sans-serif;font-size:26px;letter-spacing:.18em;
    color:var(--gray);font-weight:400;margin-bottom:52px}
  .quote{font-size:60px;font-weight:400;line-height:1.55;color:var(--white)}
  .quote.sm{font-size:52px;line-height:1.5}
  .src{font-family:'Montserrat',system-ui,sans-serif;margin-top:56px;font-size:26px;
    color:var(--gray);letter-spacing:.06em}
  .names{font-size:56px;line-height:1.7;color:var(--white);font-weight:400}
  .names b{color:var(--amber);font-weight:600;font-style:italic}
  .names .big{display:block;margin-top:40px;font-size:64px;font-style:italic}
  .cta-title{font-size:118px;font-weight:600;letter-spacing:.02em;color:var(--white);
    text-shadow:0 0 50px rgba(200,134,10,.4)}
  .cta-jp{font-family:'Noto Serif JP',serif;font-size:40px;color:var(--gold);margin-top:18px;letter-spacing:.2em}
  .cta-sub{font-size:44px;color:var(--gray);margin-top:36px;font-style:italic}
  .cta-url{margin-top:64px;font-size:60px;color:var(--white);border:2px solid var(--gold);
    border-radius:100px;padding:24px 66px;letter-spacing:.06em;background:rgba(200,134,10,.08)}
  .cta-free{font-family:'Montserrat',system-ui,sans-serif;margin-top:36px;font-size:34px;
    color:var(--gray);letter-spacing:.1em}
  #bar{position:absolute;left:0;bottom:0;height:8px;width:0;
    background:linear-gradient(90deg,var(--gold),var(--amber));opacity:.85}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(18,10,3,.82);backdrop-filter:blur(4px);z-index:20;gap:40px;padding:0 100px;text-align:center}
  #ui .kick{font-family:'Montserrat',system-ui,sans-serif;font-size:30px;letter-spacing:.5em;
    color:var(--gold);text-transform:uppercase}
  #ui h1{font-size:96px;font-weight:600;color:var(--white);line-height:1.1}
  #ui p{font-size:38px;color:var(--gray);line-height:1.6;font-style:italic}
  #play{font-family:'Montserrat',system-ui,sans-serif;font-size:44px;font-weight:600;color:#1c1005;
    background:var(--gold);border:none;border-radius:100px;padding:30px 84px;cursor:pointer;
    letter-spacing:.08em;box-shadow:0 10px 40px rgba(200,134,10,.4)}
  #play:hover{background:var(--amber)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage');
  const EM=[];
  for(let i=0;i<18;i++){
    const x=((i*137.5)%100)/100*1080, dur=6+((i*53)%60)/10, phase=((i*29)%100)/100;
    const e=document.createElement('div');e.className='ember';e.style.left=x+'px';e.style.top='0px';
    stage.appendChild(e);EM.push({e,dur,phase});
  }
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes');
  const flame=document.getElementById('flame');
  const core=flame.querySelector('.core'), halo=flame.querySelector('.halo');
  const bar=document.getElementById('bar');
  let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;
    const el=w.firstElementChild; el.style.opacity=0; scenesEl.appendChild(el);
    S.push({el,start:t0,end:t0+sc.d}); t0+=sc.d;});
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  function op(t,st,en){if(t<st||t>en)return 0;
    return clamp(Math.min((t-st)/700,(en-t)/500),0,1);}
  window.renderAt=function(t){
    flame.style.opacity=clamp(t/800,0,1);
    core.style.transform=`translateX(-50%) scaleY(${1+0.06*Math.sin(t/210)}) scaleX(${1-0.04*Math.sin(t/250)})`;
    halo.style.transform=`translate(-50%,-50%) scale(${1+0.10*Math.sin(t/520)})`;
    halo.style.opacity=(0.5+0.35*(0.5+0.5*Math.sin(t/520))).toFixed(3);
    for(const m of EM){const prog=frac((t/1000)/m.dur+m.phase);
      m.e.style.top=(1520-prog*2700)+'px';
      m.e.style.transform=`scale(${0.6+prog*0.6})`;
      m.e.style.opacity=(Math.sin(prog*Math.PI)*0.85).toFixed(3);}
    for(const s of S){s.el.style.opacity=op(t,s.start,s.end);}
    if(bar) bar.style.width=(clamp(t/total,0,1)*100)+'%';
  };
  window.renderAt(0);
  const params=new URLSearchParams(location.search);
  const ui=document.getElementById('ui');
  if(params.has('capture')){ ui.style.display='none'; bar.style.display='none'; }
  else {
    const bgm=document.getElementById('bgm');
    document.getElementById('play').addEventListener('click',()=>{
      ui.classList.add('hide');
      try{bgm.currentTime=0;bgm.volume=.7;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(now){const t=performance.now()-start;
        window.renderAt(Math.min(t,total));
        if(t<total){requestAnimationFrame(loop);}
        else{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1200;
          bgm.volume=Math.max(0,.7*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();
          ui.classList.remove('hide');document.getElementById('play').textContent='↻ Replay';}
      })(start);
      // fade bgm near end
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.7*(1-k));if(k<1)requestAnimationFrame(fo);})();}, total-1500);
    });
  }
"""

def page(meta, scenes):
    scenes_js = "[\n" + ",\n".join(
        "    {d:%d, html:`%s`}" % (d, html) for (d, html) in scenes
    ) + "\n  ]"
    engine = ENGINE.replace("SCENES", scenes_js)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@400;500;600&family=Noto+Serif+JP:wght@400;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap">
  <div id="stage">
    <div id="flame"><div class="halo"></div><div class="core"></div></div>
    <div id="scenes"></div>
    <div id="bar"></div>
    <div id="ui">
      <div class="kick">{meta['kicker']}</div>
      <h1>{meta['ep']}</h1>
      <p>{meta['tagline']}</p>
      <button id="play">&#9654; Play</button>
    </div>
  </div>
</div>
<audio id="bgm" src="eichinohi-site/bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""

# ---- shared scene builders ----
def hook(text):        return f'<div class="scene"><div class="lead">{text}</div></div>'
def badge(k,ep):       return f'<div class="scene"><div class="kicker">{k}</div><div class="ep-title">{ep}</div></div>'
def worry(n,text):     return f'<div class="scene"><div class="q-tag">{n}</div><div class="worry">{text}</div></div>'
def sage(name,era,quote,src,sm=False):
    cls="quote sm" if sm else "quote"
    return (f'<div class="scene"><div class="sage-name">{name}</div><div class="sage-era">{era}</div>'
            f'<div class="{cls}">{quote}</div><div class="src">{src}</div></div>')
def names(line,big):   return f'<div class="scene"><div class="names">{line}<span class="big">{big}</span></div></div>'
def cta():
    return ('<div class="scene"><div class="cta-title">Eichi no Tomoshibi</div>'
            '<div class="cta-jp">叡智の灯火</div>'
            '<div class="cta-sub">Words from 27 great minds to light your path</div>'
            '<div class="cta-url">eichinohi.com</div>'
            '<div class="cta-free">&#9654; PLAY FREE</div></div>')

# ---- the three videos ----
VIDEOS = []

# EN #1 — When you lose your way
VIDEOS.append(dict(
  file="eichinohi-short-en-1.html",
  meta=dict(title="Eichi no Tomoshibi — When You Lose Your Way (Wisdom Short EN #1)",
            desc="A life-sim where 27 great minds speak to your crossroads. Mother Teresa, Marie Curie, Helen Keller.",
            kicker="The Lamp of Wisdom", ep="When you lose your way",
            tagline="When the night is dark, what would the wise say?"),
  scenes=[
    (3500, hook('Some nights,<br>we all <span class="glow">lose our way</span>.')),
    (3000, badge('The Lamp of Wisdom','When you<br>lose your way')),
    (2600, worry('Alone','I feel completely alone.')),
    (6200, sage('Mother Teresa','1910 – 1997','Loneliness and the feeling<br>of being unwanted is the<br>most terrible poverty.','&mdash; widely recorded', sm=True)),
    (2600, worry('Doubt','I have no confidence in myself.')),
    (7000, sage('Marie Curie','1867 – 1934','Life is not easy for any of us.<br>But what of that?<br>We must have perseverance,<br>and above all, confidence<br>in ourselves.','&mdash; Madame Curie, 1937', sm=True)),
    (2600, worry('Pain','The world feels full of pain.')),
    (6200, sage('Helen Keller','1880 – 1968','Although the world is<br>full of suffering,<br>it is also full of<br>the overcoming of it.','&mdash; Optimism, 1903', sm=True)),
    (3000, names('Confucius &middot; Curie &middot; Ali &middot;<br>Helen Keller &middot; Musashi…','27 great minds<br>to light your way.')),
    (4000, cta()),
  ]))

# EN #2 — Don't quit
VIDEOS.append(dict(
  file="eichinohi-short-en-2.html",
  meta=dict(title="Eichi no Tomoshibi — Don't Quit (Wisdom Short EN #2)",
            desc="A life-sim where 27 great minds speak to your crossroads. Lincoln, Muhammad Ali, Eleanor Roosevelt.",
            kicker="The Lamp of Wisdom", ep="Don't quit",
            tagline="When you want to give up, what would the wise say?"),
  scenes=[
    (3500, hook('There is a moment<br>you want to <span class="glow">give up</span>.')),
    (3000, badge('The Lamp of Wisdom',"Don't quit")),
    (2600, worry('Overwhelmed','There is too much. I am breaking.')),
    (6400, sage('Abraham Lincoln','1809 – 1865','Always bear in mind<br>that your own resolution<br>to succeed is more<br>important than any other.','&mdash; Letter, 1855', sm=True)),
    (2600, worry('Exhausted','I want to quit.')),
    (7000, sage('Muhammad Ali','1942 – 2016','I hated every minute<br>of training, but I said:<br>&lsquo;Don&rsquo;t quit. Suffer now<br>and live the rest of your<br>life as a champion.&rsquo;','&mdash; In His Own Words', sm=True)),
    (2600, worry('Afraid','I want to try &mdash; but I&rsquo;m afraid.')),
    (6000, sage('Eleanor Roosevelt','1884 – 1962','You must do the things<br>you think you cannot do.','&mdash; You Learn by Living, 1960')),
    (3000, names('Lincoln &middot; Ali &middot; Curie &middot;<br>Roosevelt &middot; Gandhi…','27 great minds<br>to keep you going.')),
    (4000, cta()),
  ]))

# EN #3 — At the crossroads
VIDEOS.append(dict(
  file="eichinohi-short-en-3.html",
  meta=dict(title="Eichi no Tomoshibi — At the Crossroads (Wisdom Short EN #3)",
            desc="A life-sim where 27 great minds speak to your crossroads. Miyamoto Musashi, Seneca, Sun Tzu.",
            kicker="The Lamp of Wisdom", ep="At the crossroads",
            tagline="When you must choose, what would the wise say?"),
  scenes=[
    (3500, hook('Sooner or later,<br>everyone must <span class="glow">choose</span>.')),
    (3000, badge('The Lamp of Wisdom','At the<br>crossroads')),
    (2600, worry('Regret','I can&rsquo;t decide. I fear regret.')),
    (6000, sage('Miyamoto Musashi','1584 – 1645','I have no regret<br>for what I have done.','&mdash; Dokkōdō, 1645')),
    (2600, worry('Direction','I don&rsquo;t know what I want.')),
    (6400, sage('Seneca','c. 4 BC – AD 65','If one does not know<br>to which port<br>one is sailing,<br>no wind is favorable.','&mdash; Letters, 71', sm=True)),
    (2600, worry('The Battle','A great battle ahead.<br>What if I lose?')),
    (6400, sage('Sun Tzu','c. 544 – 496 BC','Know the enemy<br>and know yourself,<br>and in a hundred battles<br>you will never be in peril.','&mdash; The Art of War', sm=True)),
    (3000, names('Musashi &middot; Seneca &middot; Sun Tzu &middot;<br>Confucius &middot; Zhuge Liang…','27 great minds<br>for every crossroad.')),
    (4000, cta()),
  ]))

for v in VIDEOS:
    html = page(v['meta'], v['scenes'])
    path = os.path.join(OUT_DIR, v['file'])
    open(path,'w',encoding='utf-8').write(html)
    total = sum(d for d,_ in v['scenes'])
    print(f"wrote {v['file']}  ({total/1000:.1f}s, {len(v['scenes'])} scenes)")
