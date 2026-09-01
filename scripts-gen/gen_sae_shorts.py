# -*- coding: utf-8 -*-
"""Generate JP promo Shorts for 冴え手帖 -SAE- 脳活道場 (SAE Techo — Brain Dojo).
Unified engine (renderAt-driven): real-time playback + ?capture=1 frame export.
Facts sourced from sae.html (5 brain games, 脳年齢診断, 世界番付, 花あわせ, 今日の知恵).
"""
import os

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root

# JP-tuned palette (SAE = 叡智の灯火 family warm gold, with a jade accent for 花/growth)
CSS = r"""
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  :root{
    --white:#fdf6ec; --gold:#d69a2a; --amber:#e0a53a; --jade:#7fae86; --gray:#a89273;
    --bg-dark:#241a0d; --bg-mid:#33260f;
  }
  html,body{height:100%;background:#100b04;overflow:hidden}
  body{font-family:'Noto Serif JP','Hiragino Mincho ProN',serif;color:var(--white);
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
    text-align:center;padding:0 110px;opacity:0}
  .kicker{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.42em;color:var(--gold);
    font-weight:600;margin-bottom:40px}
  .lead{font-size:78px;font-weight:500;line-height:1.5;letter-spacing:.03em}
  .lead .glow{color:var(--amber)}
  .ep-title{font-size:100px;font-weight:700;line-height:1.2;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.35)}
  .num{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:30px;letter-spacing:.4em;color:var(--gray);
    margin-bottom:38px;font-weight:500}
  .worry{font-size:70px;font-weight:600;line-height:1.55;color:#f3e4c6}
  .worry::before{content:"\201C";color:var(--gold);opacity:.5}
  .worry::after{content:"\201D";color:var(--gold);opacity:.5}
  .card-name{font-size:74px;letter-spacing:.06em;color:var(--white);font-weight:700;margin-bottom:20px}
  .badge{display:inline-block;font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.2em;
    color:var(--bg-dark);background:var(--gold);border-radius:100px;padding:10px 34px;font-weight:600;margin-bottom:48px}
  .badge.jade{background:var(--jade)}
  .line{font-size:60px;font-weight:500;line-height:1.55;color:var(--white)}
  .how{font-family:'Noto Sans JP',system-ui,sans-serif;margin-top:46px;font-size:30px;color:var(--gray);letter-spacing:.05em}
  .names{font-size:56px;line-height:1.75;color:var(--white);font-weight:500}
  .names b{color:var(--amber);font-weight:700}
  .names .big{display:block;margin-top:36px;font-size:66px}
  .cta-title{font-size:104px;font-weight:700;letter-spacing:.04em;color:var(--white);text-shadow:0 0 50px rgba(214,154,42,.4)}
  .cta-jp{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:36px;color:var(--gold);margin-top:20px;letter-spacing:.16em}
  .cta-sub{font-size:46px;color:var(--gray);margin-top:34px}
  .cta-url{margin-top:60px;font-family:'Noto Sans JP',system-ui,sans-serif;font-size:46px;color:var(--white);
    border:2px solid var(--gold);border-radius:100px;padding:22px 56px;letter-spacing:.04em;background:rgba(214,154,42,.08)}
  .cta-free{font-family:'Noto Sans JP',system-ui,sans-serif;margin-top:34px;font-size:38px;color:var(--gray);letter-spacing:.1em}
  #bar{position:absolute;left:0;bottom:0;height:8px;width:0;background:linear-gradient(90deg,var(--gold),var(--amber));opacity:.85}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(16,11,4,.82);backdrop-filter:blur(4px);z-index:20;gap:40px;padding:0 110px;text-align:center}
  #ui .kick{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:32px;letter-spacing:.42em;color:var(--gold)}
  #ui h1{font-size:92px;font-weight:700;color:var(--white);line-height:1.15}
  #ui p{font-size:40px;color:var(--gray);line-height:1.6}
  #play{font-family:'Noto Sans JP',system-ui,sans-serif;font-size:46px;font-weight:700;color:#1a1207;background:var(--gold);
    border:none;border-radius:100px;padding:30px 84px;cursor:pointer;letter-spacing:.08em;box-shadow:0 10px 40px rgba(214,154,42,.4)}
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
        else{ui.classList.remove('hide');document.getElementById('play').textContent='↻ もう一度';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1500;
        bgm.volume=Math.max(0,.7*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1500);
    });
  }
"""

def page(meta, scenes):
    scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, html) for (d, html) in scenes) + "\n  ]"
    engine = ENGINE.replace("SCENES", scenes_js)
    return f"""<!DOCTYPE html>
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
  <div id="flame"><div class="halo"></div><div class="core"></div></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="kick">{meta['kicker']}</div>
    <h1>{meta['ep']}</h1>
    <p>{meta['tagline']}</p>
    <button id="play">&#9654; 再生</button>
  </div>
</div></div>
<audio id="bgm" src="sae-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""

# ---- scene helpers ----
def hook(t):        return f'<div class="scene"><div class="lead">{t}</div></div>'
def badge(k, ep):   return f'<div class="scene"><div class="kicker">{k}</div><div class="ep-title">{ep}</div></div>'
def moment(n, t):   return f'<div class="scene"><div class="num">{n}</div><div class="worry">{t}</div></div>'
def card(name, dom, line, how, jade=False):
    b = "badge jade" if jade else "badge"
    return (f'<div class="scene"><div class="card-name">{name}</div>'
            f'<div class="{b}">{dom}</div><div class="line">{line}</div>'
            f'<div class="how">{how}</div></div>')
def names(line, big): return f'<div class="scene"><div class="names">{line}<span class="big">{big}</span></div></div>'
def cta(sub):
    return ('<div class="scene"><div class="cta-title">冴え手帖 -SAE-</div>'
            '<div class="cta-jp">脳活道場 ｜ 叡智の灯火</div>'
            f'<div class="cta-sub">{sub}</div>'
            '<div class="cta-url">ryuzaburo7.itch.io/sae-techo</div>'
            '<div class="cta-free">&#9654; 無料でプレイ</div></div>')

VIDEOS = []

# SAE #1 — 5種目トレーニング
VIDEOS.append(dict(
  file="sae-short-1.html",
  meta=dict(title="冴え手帖 -SAE-｜1日3分、脳が冴える 5種目トレーニング（宣伝ショート #1）",
            desc="計算・記憶・注意・集中・反射。5つの脳力を1日3分で鍛える脳活道場 冴え手帖 -SAE-。",
            kicker="冴え手帖 -SAE-", ep="1日3分、脳が冴える",
            tagline="計算・記憶・注意・集中・反射。5つの脳力をまるごと。"),
  scenes=[
    (3500, hook('最近、<span class="glow">“あれ”</span>が<br>思い出せない。')),
    (3000, badge('冴え手帖 -SAE- 脳活道場', '5種目で<br>脳を鍛える')),
    (3600, card('けいさん道場', '処理速度', 'かんたんな計算を、<br>素早く。', '見た瞬間に答える瞬発力')),
    (3600, card('数字おぼえ', '記憶力', '見て、覚えて、<br>入力する。', 'ワーキングメモリを鍛える')),
    (3600, card('順番タッチ', '注意・切替', '1 → 2 → 3、<br>順にタッチ。', '注意の切り替えを速く')),
    (3600, card('いろよみ', '集中・抑制', '文字ではなく<br>“色”を答える。', '思い込みを抑える集中力')),
    (3600, card('後出しじゃんけん', '判断・反射', '指示どおりに、<br>後出しで勝つ。', '瞬間の判断と反射')),
    (3200, names('処理速度・記憶・注意・<br>集中・反射——', '5つの力を、<br>まるごと。')),
    (4000, cta('1日3分、遊んで脳を動かす')),
  ]))

# SAE #2 — 脳年齢診断
VIDEOS.append(dict(
  file="sae-short-2.html",
  meta=dict(title="冴え手帖 -SAE-｜あなたの脳年齢は？ 脳年齢診断（宣伝ショート #2）",
            desc="5種目のスコアから“脳の冴え”を数値化。世界番付で自己ベストを競う脳活道場 冴え手帖 -SAE-。",
            kicker="冴え手帖 -SAE-", ep="あなたの脳年齢は？",
            tagline="その“うっかり”、数分でチェック。"),
  scenes=[
    (3500, hook('その<span class="glow">“うっかり”</span>、<br>脳からのサインかも。')),
    (3000, badge('冴え手帖 -SAE- 脳活道場', '脳年齢<br>診断')),
    (2800, moment('CHECK 1', 'あの人の名前が、<br>すぐ出てこない。')),
    (2800, moment('CHECK 2', '頭の切り替えに、<br>時間がかかる。')),
    (2800, moment('CHECK 3', '計算が、前より<br>遅くなった気がする。')),
    (5600, card('脳年齢診断', '数分でわかる', 'スコアから、<br>“脳の冴え”を数値化。', '5種目の結果から算出')),
    (5200, card('世界番付', 'ランキング', '自己ベストを更新して、<br>世界と競う。', '「冴えラッシュ」番付に挑戦', jade=True)),
    (4000, cta('今の自分を知って、鍛える')),
  ]))

# SAE #3 — 花あわせ
VIDEOS.append(dict(
  file="sae-short-3.html",
  meta=dict(title="冴え手帖 -SAE-｜花あわせ 花札で、脳が冴える（宣伝ショート #3）",
            desc="美しい花札「花あわせ」。役を作って得点を競い、遊びながら脳を動かす 冴え手帖 -SAE-。",
            kicker="冴え手帖 -SAE-", ep="花あわせ",
            tagline="花札で遊びながら、頭が冴える。"),
  scenes=[
    (3500, hook('花札、<br><span class="glow">ちゃんと</span>遊べる？')),
    (3000, badge('冴え手帖 -SAE- 脳活道場', '花あわせ')),
    (5200, card('美しい花札', '四季の花', '四季の花を、<br>手のひらで。', '目でも楽しむ和の意匠', jade=True)),
    (5200, card('かんたんルール', '役づくり', '役を作って、<br>得点を競う。', '初めてでもすぐ遊べる')),
    (5200, card('世界番付', '“ここまで咲いた”', '自己ベストを、<br>世界と競う。', '花あわせの記録に挑戦', jade=True)),
    (3200, names('美しい札で、<br>役を組み立てる——', '遊びながら、<br>頭が冴える。')),
    (4000, cta('花札で、楽しく脳活')),
  ]))

for v in VIDEOS:
    html = page(v['meta'], v['scenes'])
    open(os.path.join(OUT_DIR, v['file']), 'w', encoding='utf-8').write(html)
    total = sum(d for d, _ in v['scenes'])
    print(f"wrote {v['file']}  ({total/1000:.1f}s, {len(v['scenes'])} scenes)")
