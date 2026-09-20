# -*- coding: utf-8 -*-
"""Generate EN + ES promo Shorts for 冴え手帖 -SAE- (SAE Techo — Brain Dojo).
Strings taken from sae.html's trilingual P(ja,en,es) data. Latin-serif tuned.
Unified engine (renderAt): real-time playback + ?capture=1 frame export.
BGM: sae-bgm-en.mp3 (instrumental, language-neutral).
"""
import os
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  :root{
    --white:#fdf6ec; --gold:#d69a2a; --amber:#e0a53a; --jade:#7fae86; --gray:#a89273;
    --bg-dark:#241a0d; --bg-mid:#33260f;
  }
  html,body{height:100%;background:#100b04;overflow:hidden}
  body{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;color:var(--white);
    display:flex;align-items:center;justify-content:center}
  #wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1080px;height:1920px;flex:none;
    transform:scale(var(--s,0.4));transform-origin:center center;
    background:radial-gradient(120% 80% at 50% 20%, #4a3416 0%, var(--bg-dark) 44%, #1a1207 80%, #100b04 100%);
    overflow:hidden;box-shadow:0 0 120px rgba(0,0,0,.6)}
  .ember{position:absolute;width:7px;height:7px;border-radius:50%;
    background:radial-gradient(circle,#ffe6a6,#d69a2a 60%,transparent 70%);opacity:0;filter:blur(.5px)}
  #flame{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:130px;height:180px;opacity:0}
  #flame .core{position:absolute;left:50%;bottom:0;transform:translateX(-50%);
    width:78px;height:128px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;
    background:linear-gradient(to top,#fff6d8,#ffd67a 40%,#e59a2a 75%,#b5661a);
    box-shadow:0 0 60px 22px rgba(224,150,42,.5),0 0 150px 66px rgba(214,154,42,.26);transform-origin:bottom center}
  #flame .halo{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:440px;height:440px;
    border-radius:50%;background:radial-gradient(circle, rgba(224,150,42,.2), transparent 60%)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:0 100px;opacity:0}
  .kicker{font-family:'Montserrat',system-ui,sans-serif;font-size:28px;letter-spacing:.34em;color:var(--gold);
    font-weight:600;margin-bottom:40px;text-transform:uppercase}
  .lead{font-size:76px;font-weight:500;line-height:1.45;font-style:italic}
  .lead .glow{color:var(--amber);font-style:italic}
  .ep-title{font-size:96px;font-weight:600;line-height:1.15;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.35)}
  .num{font-family:'Montserrat',system-ui,sans-serif;font-size:26px;letter-spacing:.34em;color:var(--gray);
    margin-bottom:36px;font-weight:500;text-transform:uppercase}
  .worry{font-size:66px;font-weight:500;line-height:1.5;color:#f3e4c6;font-style:italic}
  .worry::before{content:"\201C";color:var(--gold);opacity:.5}
  .worry::after{content:"\201D";color:var(--gold);opacity:.5}
  .card-name{font-size:66px;letter-spacing:.02em;color:var(--white);font-weight:600;margin-bottom:20px}
  .badge{display:inline-block;font-family:'Montserrat',system-ui,sans-serif;font-size:27px;letter-spacing:.16em;
    color:var(--bg-dark);background:var(--gold);border-radius:100px;padding:10px 32px;font-weight:600;
    margin-bottom:46px;text-transform:uppercase}
  .badge.jade{background:var(--jade)}
  .line{font-size:56px;font-weight:500;line-height:1.5;color:var(--white)}
  .how{font-family:'Montserrat',system-ui,sans-serif;margin-top:44px;font-size:28px;color:var(--gray);letter-spacing:.03em}
  .names{font-size:50px;line-height:1.7;color:var(--white);font-weight:500}
  .names b{color:var(--amber);font-weight:600;font-style:italic}
  .names .big{display:block;margin-top:34px;font-size:62px;font-style:italic}
  .cta-title{font-size:88px;font-weight:600;letter-spacing:.02em;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.4)}
  .cta-jp{font-family:'Montserrat',system-ui,sans-serif;font-size:30px;color:var(--gold);margin-top:20px;letter-spacing:.12em;text-transform:uppercase}
  .cta-sub{font-size:44px;color:var(--gray);margin-top:32px;font-style:italic}
  .cta-url{margin-top:56px;font-family:'Montserrat',system-ui,sans-serif;font-size:42px;color:var(--white);
    border:2px solid var(--gold);border-radius:100px;padding:22px 50px;letter-spacing:.02em;background:rgba(214,154,42,.08)}
  .cta-free{font-family:'Montserrat',system-ui,sans-serif;margin-top:32px;font-size:34px;color:var(--gray);letter-spacing:.1em;text-transform:uppercase}
  #bar{position:absolute;left:0;bottom:0;height:8px;width:0;background:linear-gradient(90deg,var(--gold),var(--amber));opacity:.85}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(16,11,4,.82);backdrop-filter:blur(4px);z-index:20;gap:38px;padding:0 100px;text-align:center}
  #ui .kick{font-family:'Montserrat',system-ui,sans-serif;font-size:28px;letter-spacing:.34em;color:var(--gold);text-transform:uppercase}
  #ui h1{font-size:84px;font-weight:600;color:var(--white);line-height:1.15}
  #ui p{font-size:38px;color:var(--gray);line-height:1.6;font-style:italic}
  #play{font-family:'Montserrat',system-ui,sans-serif;font-size:42px;font-weight:600;color:#1a1207;background:var(--gold);
    border:none;border-radius:100px;padding:28px 78px;cursor:pointer;letter-spacing:.08em;box-shadow:0 10px 40px rgba(214,154,42,.4)}
  #play:hover{background:var(--amber)}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .6s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage');
  const EM=[];
  for(let i=0;i<20;i++){const x=((i*137.5)%100)/100*1080, dur=6+((i*53)%60)/10, phase=((i*29)%100)/100;
    const e=document.createElement('div');e.className='ember';e.style.left=x+'px';e.style.top='0px';stage.appendChild(e);
    EM.push({e,dur,phase});}
  const scenes=SCENES;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'), flame=document.getElementById('flame');
  const core=flame.querySelector('.core'), halo=flame.querySelector('.halo'), bar=document.getElementById('bar');
  let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v);
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/700,(en-t)/500),0,1);}
  window.renderAt=function(t){
    flame.style.opacity=clamp(t/800,0,1);
    core.style.transform=`translateX(-50%) scaleY(${1+0.06*Math.sin(t/210)}) scaleX(${1-0.04*Math.sin(t/250)})`;
    halo.style.transform=`translate(-50%,-50%) scale(${1+0.10*Math.sin(t/520)})`;
    halo.style.opacity=(0.5+0.35*(0.5+0.5*Math.sin(t/520))).toFixed(3);
    for(const m of EM){const prog=frac((t/1000)/m.dur+m.phase);
      m.e.style.top=(1520-prog*2700)+'px';m.e.style.transform=`scale(${0.6+prog*0.6})`;
      m.e.style.opacity=(Math.sin(prog*Math.PI)*0.8).toFixed(3);}
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
      try{bgm.currentTime=0;bgm.volume=.7;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent=PLAY_AGAIN;}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.7*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

def page(meta, scenes, play_again):
    scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
    engine = ENGINE.replace("SCENES", scenes_js).replace("PLAY_AGAIN", repr(play_again))
    return f"""<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Montserrat:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
  <div id="flame"><div class="halo"></div><div class="core"></div></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="kick">{meta['kicker']}</div>
    <h1>{meta['ep']}</h1>
    <p>{meta['tagline']}</p>
    <button id="play">&#9654; {meta['play']}</button>
  </div>
</div></div>
<audio id="bgm" src="sae-bgm-en.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""

def hook(t):        return f'<div class="scene"><div class="lead">{t}</div></div>'
def badge(k, ep):   return f'<div class="scene"><div class="kicker">{k}</div><div class="ep-title">{ep}</div></div>'
def moment(n, t):   return f'<div class="scene"><div class="num">{n}</div><div class="worry">{t}</div></div>'
def card(name, dom, line, how, jade=False):
    b = "badge jade" if jade else "badge"
    return (f'<div class="scene"><div class="card-name">{name}</div>'
            f'<div class="{b}">{dom}</div><div class="line">{line}</div><div class="how">{how}</div></div>')
def names(line, big): return f'<div class="scene"><div class="names">{line}<span class="big">{big}</span></div></div>'
def cta(brand_jp, sub, free):
    return ('<div class="scene"><div class="cta-title">SAE Techo</div>'
            f'<div class="cta-jp">{brand_jp}</div>'
            f'<div class="cta-sub">{sub}</div>'
            '<div class="cta-url">ryuzaburo7.itch.io/sae-techo</div>'
            f'<div class="cta-free">&#9654; {free}</div></div>')

VIDEOS = []

# ============ ENGLISH ============
EN_BRAND = "Brain Dojo &nbsp;|&nbsp; Eichi no Hi"
VIDEOS.append(dict(file="sae-short-en-1.html", play_again="↻ Replay",
  meta=dict(lang="en", title="SAE Techo — 3 Minutes a Day, Sharpen Your Mind (Brain Short EN #1)",
    desc="Five brain games train speed, memory, attention, focus and reflex. SAE Techo — Brain Dojo.",
    kicker="SAE Techo — Brain Dojo", ep="3 minutes a day,<br>sharper mind", play="Play",
    tagline="Speed, memory, attention, focus, reflex — all in one."),
  scenes=[
    (3500, hook('Lately, the word<br>just <span class="glow">won&rsquo;t come</span>.')),
    (3000, badge('SAE Techo — Brain Dojo', 'Train with<br>5 games')),
    (3600, card('Math Dash', 'Speed', 'Quick mental math.', 'Answer the instant you see it')),
    (3600, card('Number Recall', 'Memory', 'See, remember, type.', 'Train your working memory')),
    (3600, card('Trail Touch', 'Attention', 'Tap 1 &rarr; 2 &rarr; 3,<br>in order.', 'Switch your focus faster')),
    (3600, card('Color Match', 'Focus', 'Name the ink color,<br>not the word.', 'Resist the obvious answer')),
    (3600, card('RPS Reflex', 'Reflex', 'Win or lose —<br>on command.', 'Split-second decisions')),
    (3200, names('Speed &middot; Memory &middot; Attention &middot;<br>Focus &middot; Reflex —', 'all in one.')),
    (4000, cta(EN_BRAND, 'Three minutes a day to move your mind', 'Play free')),
  ]))
VIDEOS.append(dict(file="sae-short-en-2.html", play_again="↻ Replay",
  meta=dict(lang="en", title="SAE Techo — What's Your Brain Age? (Brain Short EN #2)",
    desc="Turn your sharpness into a number from five games, and compete on the world rankings. SAE Techo.",
    kicker="SAE Techo — Brain Dojo", ep="What&rsquo;s your<br>brain age?", play="Play",
    tagline="That little slip? Check it in minutes."),
  scenes=[
    (3500, hook('That little <span class="glow">slip</span>?<br>Your brain may be<br>signaling.')),
    (3000, badge('SAE Techo — Brain Dojo', 'Brain Age<br>Check')),
    (2800, moment('Check 1', 'A name that<br>won&rsquo;t come to you.')),
    (2800, moment('Check 2', 'Switching tasks<br>takes longer.')),
    (2800, moment('Check 3', 'Mental math feels<br>slower than before.')),
    (5600, card('Brain Age Check', 'In minutes', 'Turn your sharpness<br>into a number.', 'Scored from all 5 games')),
    (5200, card('World Rankings', 'Leaderboard', 'Beat your best.<br>Compete with the world.', 'Climb the SAE Rush ranks', jade=True)),
    (4000, cta(EN_BRAND, 'Know where you are, then train', 'Play free')),
  ]))
VIDEOS.append(dict(file="sae-short-en-3.html", play_again="↻ Replay",
  meta=dict(lang="en", title="SAE Techo — Hana-Awase, Play and Sharpen (Brain Short EN #3)",
    desc="Beautiful hanafuda: form yaku, score points, and let your mind sharpen as you play. SAE Techo.",
    kicker="SAE Techo — Brain Dojo", ep="Hana-Awase", play="Play",
    tagline="Play hanafuda, and your mind sharpens."),
  scenes=[
    (3500, hook('Can you still play<br><span class="glow">hanafuda</span>?')),
    (3000, badge('SAE Techo — Brain Dojo', 'Hana-Awase')),
    (5200, card('Beautiful cards', 'Four seasons', 'The flowers of the seasons,<br>in your hand.', 'Japanese art to enjoy', jade=True)),
    (5200, card('Simple rules', 'Build yaku', 'Form combos,<br>score points.', 'Easy from your first game')),
    (5200, card('World Rankings', '&ldquo;Best bloom&rdquo;', 'Take your best bloom<br>to the world.', 'Chase the Hana-Awase record', jade=True)),
    (3200, names('Beautiful cards,<br>combos to build —', 'play, and your<br>mind sharpens.')),
    (4000, cta(EN_BRAND, 'Sharpen your mind, the fun way', 'Play free')),
  ]))

# ============ SPANISH ============
ES_BRAND = "Dojo Cerebral &nbsp;|&nbsp; Eichi no Hi"
VIDEOS.append(dict(file="sae-short-es-1.html", play_again="↻ Repetir",
  meta=dict(lang="es", title="SAE Techo — 3 minutos al día, mente más ágil (Short Cerebral ES #1)",
    desc="Cinco juegos entrenan rapidez, memoria, atención, concentración y reflejos. SAE Techo — Dojo Cerebral.",
    kicker="SAE Techo — Dojo Cerebral", ep="3 minutos al día,<br>mente ágil", play="Jugar",
    tagline="Rapidez, memoria, atención, concentración, reflejos — todo en uno."),
  scenes=[
    (3500, hook('Últimamente, la palabra<br><span class="glow">no llega</span>.')),
    (3000, badge('SAE Techo — Dojo Cerebral', 'Entrena con<br>5 juegos')),
    (3600, card('Cálculo Rápido', 'Rapidez', 'Cálculo mental veloz.', 'Responde al instante')),
    (3600, card('Memoria Numérica', 'Memoria', 'Mira, recuerda,<br>escribe.', 'Entrena tu memoria de trabajo')),
    (3600, card('Toque en Orden', 'Atención', 'Toca 1 &rarr; 2 &rarr; 3,<br>en orden.', 'Cambia el foco más rápido')),
    (3600, card('Color y Palabra', 'Concentración', 'Di el color de la tinta,<br>no la palabra.', 'Resiste lo obvio')),
    (3600, card('Reflejo Manos', 'Reflejos', 'Gana o pierde,<br>a la orden.', 'Decisiones en un instante')),
    (3200, names('Rapidez &middot; Memoria &middot; Atención &middot;<br>Concentración &middot; Reflejos —', 'todo en uno.')),
    (4000, cta(ES_BRAND, 'Tres minutos al día para mover la mente', 'Jugar gratis')),
  ]))
VIDEOS.append(dict(file="sae-short-es-2.html", play_again="↻ Repetir",
  meta=dict(lang="es", title="SAE Techo — ¿Cuál es tu edad cerebral? (Short Cerebral ES #2)",
    desc="Convierte tu agilidad en un número con cinco juegos y compite en la clasificación mundial. SAE Techo.",
    kicker="SAE Techo — Dojo Cerebral", ep="¿Cuál es tu<br>edad cerebral?", play="Jugar",
    tagline="¿Ese pequeño olvido? Compruébalo en minutos."),
  scenes=[
    (3500, hook('¿Ese pequeño <span class="glow">olvido</span>?<br>Tu cerebro podría<br>estar avisando.')),
    (3000, badge('SAE Techo — Dojo Cerebral', 'Chequeo de<br>Edad Cerebral')),
    (2800, moment('Prueba 1', 'Un nombre que<br>no llega.')),
    (2800, moment('Prueba 2', 'Cambiar de tarea<br>cuesta más.')),
    (2800, moment('Prueba 3', 'Calcular se siente<br>más lento que antes.')),
    (5600, card('Edad Cerebral', 'En minutos', 'Convierte tu agilidad<br>en un número.', 'Calculado con los 5 juegos')),
    (5200, card('Clasificación Mundial', 'Ranking', 'Supera tu récord.<br>Compite con el mundo.', 'Sube en SAE Rush', jade=True)),
    (4000, cta(ES_BRAND, 'Conoce dónde estás y entrena', 'Jugar gratis')),
  ]))
VIDEOS.append(dict(file="sae-short-es-3.html", play_again="↻ Repetir",
  meta=dict(lang="es", title="SAE Techo — Hana-Awase, juega y agudiza (Short Cerebral ES #3)",
    desc="Hermosas cartas hanafuda: forma jugadas, suma puntos y agudiza tu mente al jugar. SAE Techo.",
    kicker="SAE Techo — Dojo Cerebral", ep="Hana-Awase", play="Jugar",
    tagline="Juega hanafuda, y tu mente se agudiza."),
  scenes=[
    (3500, hook('¿Aún sabes jugar<br><span class="glow">hanafuda</span>?')),
    (3000, badge('SAE Techo — Dojo Cerebral', 'Hana-Awase')),
    (5200, card('Cartas hermosas', 'Cuatro estaciones', 'Las flores de las estaciones,<br>en tu mano.', 'Arte japonés para disfrutar', jade=True)),
    (5200, card('Reglas sencillas', 'Forma jugadas', 'Forma combinaciones,<br>suma puntos.', 'Fácil desde la primera partida')),
    (5200, card('Clasificación Mundial', '&ldquo;Mejor flor&rdquo;', 'Lleva tu mejor flor<br>al mundo.', 'Persigue el récord de Hana-Awase', jade=True)),
    (3200, names('Cartas hermosas,<br>jugadas que formar —', 'juega, y tu mente<br>se agudiza.')),
    (4000, cta(ES_BRAND, 'Agudiza tu mente, jugando', 'Jugar gratis')),
  ]))

for v in VIDEOS:
    html = page(v['meta'], v['scenes'], v['play_again'])
    open(os.path.join(OUT_DIR, v['file']), 'w', encoding='utf-8').write(html)
    total = sum(d for d, _ in v['scenes'])
    print(f"wrote {v['file']}  ({total/1000:.1f}s, {len(v['scenes'])} scenes)")
