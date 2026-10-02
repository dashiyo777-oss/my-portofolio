# -*- coding: utf-8 -*-
"""「the sound with no name / NANASIGNAL（ナナシグナル）」 — promo short (9:16, ~27s).

Matches the jacket's graphic/glitch language: an off-white grunge canvas, black ink and
cyan/magenta paint splatters, bold lowercase type with an RGB split, a big audio waveform
pulsing to the beat, diagonal color slashes, and a glitched city skyline. Kinetic and
aggressive for an electronic/hip-hop manifesto: noise becomes music. Bilingual (JP + EN)
for a Japan/US audience, ages 10+.

On-screen text uses the rights-holder-supplied lyrics (selected lines), the title, the
artist, verified cover slogans (MUSIC HAS NO LABELS / Find Your Own Frequency) and generic
labels.

Deterministic render: exposes window.renderAt(ms) + window.TOTAL. BGM: nana-bgm.mp3.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

CSS = r"""
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:100%;height:100%;background:#e9e6df;overflow:hidden}
  #wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0a0a0c}
  #stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform:scale(var(--s,1));transform-origin:center center;
    font-family:'Montserrat',sans-serif;background:#efece6}
  #paper{position:absolute;inset:0;background:
     radial-gradient(ellipse 700px 500px at 22% 18%, rgba(255,255,255,.7), transparent 60%),
     radial-gradient(ellipse 600px 700px at 82% 78%, rgba(214,210,200,.6), transparent 62%),
     linear-gradient(160deg,#f2efe9 0%,#eae6de 52%,#e2ded5 100%)}
  #world{position:absolute;inset:0}
  .slash{position:absolute;transform-origin:50% 50%;mix-blend-mode:multiply;opacity:.85}
  #slashC{left:-140px;top:520px;width:1500px;height:70px;background:linear-gradient(90deg,transparent,#12a6e6 30%,#12a6e6 70%,transparent);transform:rotate(-24deg)}
  #slashM{left:-120px;top:1230px;width:1500px;height:54px;background:linear-gradient(90deg,transparent,#e5143d 30%,#e5143d 70%,transparent);transform:rotate(-24deg)}
  .splat{position:absolute}
  .blob{position:absolute;border-radius:46% 54% 60% 40%/50% 44% 56% 50%}
  #wave{position:absolute;left:0;top:820px;width:1080px;height:300px;display:flex;align-items:center;justify-content:center;gap:6px;z-index:3}
  .bar{width:12px;background:#111116;border-radius:3px}
  #city{position:absolute;left:0;bottom:0;width:1080px;height:340px;z-index:2}
  #cityghost{position:absolute;left:0;bottom:0;width:1080px;height:340px;z-index:1;opacity:.5}
  #flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 46%, rgba(255,255,255,.9), rgba(120,220,255,.4) 40%, transparent 72%);
    opacity:0;pointer-events:none;z-index:11;mix-blend-mode:screen}
  #grain{position:absolute;inset:0;opacity:.12;pointer-events:none;mix-blend-mode:multiply;z-index:12;
    background-image:radial-gradient(circle,#000 1px,transparent 1px);background-size:3px 3px}
  #scan{position:absolute;inset:0;opacity:.06;pointer-events:none;z-index:12;
    background:repeating-linear-gradient(0deg, rgba(0,0,0,.6) 0 1px, transparent 1px 4px)}
  .scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0;z-index:14}
  .scene.mid{justify-content:flex-start;padding:250px 76px 0}
  .scene.low{justify-content:flex-start;padding:196px 76px 0}
  .scene.hi{justify-content:flex-start;padding:150px 76px 0}
  .kick{font-family:'Montserrat',sans-serif;font-size:32px;letter-spacing:.5em;color:#111116;text-transform:uppercase;font-weight:800}
  .jp{font-family:'Noto Sans JP',sans-serif;font-size:66px;line-height:1.42;font-weight:900;color:#111116;letter-spacing:.01em}
  .jp .em{color:#e5143d}
  .jp .cy{color:#12a6e6}
  .ensub{font-family:'Montserrat',sans-serif;font-size:32px;letter-spacing:.14em;color:#4a4a52;font-weight:600;margin-top:18px;text-transform:uppercase}
  .big{font-family:'Anton',sans-serif;font-size:118px;line-height:.96;font-weight:400;color:#111116;letter-spacing:.005em;text-transform:lowercase;display:inline-block}
  .title{font-family:'Anton',sans-serif;font-size:150px;line-height:.9;color:#111116;letter-spacing:.01em;text-transform:lowercase}
  .artist{font-family:'Montserrat',sans-serif;font-size:40px;letter-spacing:.28em;color:#111116;text-transform:uppercase;font-weight:800;margin-top:20px}
  .artist small{font-family:'Noto Sans JP',sans-serif;font-weight:700;letter-spacing:.2em;font-size:30px}
  .freq{font-family:'Montserrat',sans-serif;font-style:italic;font-size:38px;color:#12a6e6;font-weight:600;margin-top:14px}
  .tag{margin-top:22px;font-family:'Montserrat',sans-serif;font-size:26px;letter-spacing:.42em;color:#111116;text-transform:uppercase;font-weight:800}
  .orn{display:flex;align-items:center;justify-content:center;gap:16px;margin:20px 0 6px}
  .orn i{display:block;width:80px;height:4px;background:#e5143d}
  .orn u{display:block;width:80px;height:4px;background:#12a6e6}
  #bar{position:absolute;left:0;bottom:0;height:6px;width:0;background:linear-gradient(90deg,#12a6e6,#e5143d);z-index:15}
  #ui{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:rgba(239,236,230,.92);backdrop-filter:blur(3px);z-index:20;gap:24px;padding:0 90px;text-align:center}
  #ui .k{font-family:'Montserrat',sans-serif;font-size:28px;letter-spacing:.4em;color:#111116;text-transform:uppercase;font-weight:800}
  #ui h1{font-family:'Anton',sans-serif;font-size:150px;color:#111116;line-height:.9;text-transform:lowercase}
  #ui p{font-family:'Montserrat',sans-serif;font-style:italic;font-size:38px;color:#12a6e6;font-weight:600}
  #play{font-family:'Montserrat',sans-serif;font-weight:800;font-size:30px;color:#efece6;background:#111116;border:none;
    border-radius:6px;padding:22px 66px;cursor:pointer;letter-spacing:.16em;text-transform:uppercase}
  #ui.hide{opacity:0;pointer-events:none;transition:opacity .5s}
"""

ENGINE = r"""
  function fit(){const s=Math.min(window.innerWidth/1080,window.innerHeight/1920);
    document.getElementById('stage').style.setProperty('--s',s);}
  window.addEventListener('resize',fit);fit();
  const stage=document.getElementById('stage'), world=document.getElementById('world'),
        clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), frac=v=>v-Math.floor(v),
        rnd=v=>frac(Math.sin(v*12.9898)*43758.5453);
  try{['118px "Anton"','150px "Anton"','66px "Noto Sans JP"','40px "Montserrat"']
      .forEach(f=>document.fonts.load(f));}catch(e){}
  const BPS=144/60;
  // paint splatters (black + cyan + magenta), placed like the jacket
  const cols={k:'#111116',c:'#12a6e6',m:'#e5143d'};
  const sp=[[820,150,150,'k'],[930,120,90,'m'],[760,300,80,'c'],[120,760,120,'k'],[240,900,80,'c'],
    [60,1180,120,'m'],[900,1000,110,'k'],[980,1180,80,'c'],[520,1500,120,'k'],[300,1620,90,'m'],[760,1560,90,'c'],[430,120,70,'m']];
  const SPL=[];
  sp.forEach((d,i)=>{const wrap=document.createElement('div');wrap.className='splat';wrap.style.left=d[0]+'px';wrap.style.top=d[1]+'px';
    const c=cols[d[3]];const b=document.createElement('div');b.className='blob';b.style.width=d[2]+'px';b.style.height=(d[2]*0.86)+'px';
    b.style.background=c;b.style.opacity=(d[3]=='k'?0.9:0.8);wrap.appendChild(b);
    for(let j=0;j<7;j++){const dot=document.createElement('div');const dz=4+((i*7+j*5)%16);
      dot.style.position='absolute';dot.style.width=dz+'px';dot.style.height=dz+'px';dot.style.borderRadius='50%';dot.style.background=c;
      dot.style.left=(d[2]*0.5+Math.cos(j*1.6+i)* (d[2]*0.6+ (j*11)%40))+'px';
      dot.style.top=(d[2]*0.43+Math.sin(j*1.6+i)* (d[2]*0.6+ (j*13)%40))+'px';dot.style.opacity=0.7;wrap.appendChild(dot);}
    wrap.dataset.ph=((i*29)%100)/100;world.insertBefore(wrap,document.getElementById('wave'));SPL.push(wrap);});
  // waveform bars
  const wave=document.getElementById('wave');const BARS=[];const N=52;
  for(let i=0;i<N;i++){const b=document.createElement('div');b.className='bar';
    const mid=1-Math.abs(i-(N-1)/2)/((N-1)/2);   // taller toward center
    b.dataset.base=0.28+mid*0.6; b.dataset.ph=(i*7%100)/100;
    if(i%9===4)b.style.background='#12a6e6'; if(i%11===7)b.style.background='#e5143d';
    wave.appendChild(b);BARS.push(b);}
  // city skyline (+ cyan ghost for glitch)
  function buildCity(el,col){let x=0,bi=3;const base=340;
    while(x<1080){const w=26+((bi*37)%54),h=70+((bi*53)%200);
      const b=document.createElement('div');b.style.position='absolute';b.style.left=x+'px';b.style.bottom='0';
      b.style.width=(w-4)+'px';b.style.height=h+'px';b.style.background=col;el.appendChild(b);x+=w+2;bi++;}}
  buildCity(document.getElementById('city'),'#111116');
  buildCity(document.getElementById('cityghost'),'#12a6e6');
  const cityghost=document.getElementById('cityghost'),flash=document.getElementById('flash'),bar=document.getElementById('bar');
  const scenes=SCENES, GL_FROM=GLFROM, GL_TO=GLTO;
  const total=scenes.reduce((a,s)=>a+s.d,0); window.TOTAL=total;
  const scenesEl=document.getElementById('scenes'); let t0=0; const S=[];
  scenes.forEach(sc=>{const w=document.createElement('div');w.innerHTML=sc.html;const el=w.firstElementChild;
    el.style.opacity=0;scenesEl.appendChild(el);S.push({el,start:t0,end:t0+sc.d});t0+=sc.d;});
  const GLI=[...document.querySelectorAll('.glitch')];
  function op(t,st,en){if(t<st||t>en)return 0;return clamp(Math.min((t-st)/450,(en-t)/400),0,1);}
  window.renderAt=function(t){
    const ts=t/1000, prog=t/total;
    const beat=Math.pow(1-frac(ts*BPS),2.2);            // sharp attack, decay
    const energy=clamp((t-GL_FROM)/900,0,1)*clamp((GL_TO-t)/900,0,1); // payoff burst window
    const shake=(beat*3+energy*5);
    world.style.transform=`translate(${(rnd(ts*9)-.5)*shake}px, ${(rnd(ts*9+3)-.5)*shake}px)`;
    for(const b of BARS){const base=+b.dataset.base, ph=+b.dataset.ph;
      const h=base*(0.42+0.58*beat) + 0.14*Math.sin(ts*6+ph*9) + energy*0.3*rnd(ts*5+ph);
      b.style.height=clamp(h,0.05,1.3)*230+'px';}
    // rgb-split glitch on flagged text
    const gx=2+beat*5+energy*10+ (rnd(ts*20)<0.12?rnd(ts*7)*10:0);
    for(const e of GLI){e.style.textShadow=`${gx.toFixed(1)}px 0 #e5143d, ${(-gx).toFixed(1)}px 0 #12a6e6`;}
    // city glitch offset
    const cg=(rnd(ts*13)-.5)*(6+energy*22);
    cityghost.style.transform=`translateX(${cg}px)`;
    flash.style.opacity=(energy*(0.25+0.4*beat)).toFixed(3);
    for(const w of SPL){const ph=+w.dataset.ph;w.style.transform=`scale(${1+0.03*Math.sin(ts*4+ph*6.28)+beat*0.02})`;}
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
      try{bgm.currentTime=0;bgm.volume=.95;bgm.play().catch(()=>{});}catch(e){}
      const start=performance.now();
      (function loop(){const t=performance.now()-start;window.renderAt(Math.min(t,total));
        if(t<total)requestAnimationFrame(loop);
        else{ui.classList.remove('hide');document.getElementById('play').textContent='REPLAY';}})();
      setTimeout(()=>{const fs=performance.now();(function fo(){const k=(performance.now()-fs)/1200;
        bgm.volume=Math.max(0,.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();}, total-1200);
    });
  }
"""

# scene timeline (snappy)
D = [2600, 4200, 4400, 5200, 4600, 6000]
S3 = D[0]+D[1]+D[2]           # payoff scene index 3 start
GL_FROM = S3 + 900
GL_TO   = S3 + D[3] - 700

scenes = [
    (D[0], '<div class="scene low"><div class="kick glitch">Music&nbsp;Has&nbsp;No&nbsp;Labels</div></div>'),
    (D[1], '<div class="scene mid"><div class="jp">誰かが「雑音」と<br>切り捨てた、その音。</div></div>'),
    (D[2], '<div class="scene mid"><div class="jp">未来はいつだって、<br><span class="cy">最初はノイズだった。</span></div>'
           '<div class="ensub">The future always starts as noise</div></div>'),
    (D[3], '<div class="scene hi"><div class="jp" style="margin-bottom:10px">鳴らせ、</div>'
           '<div class="big glitch">the sound<br>with no name</div></div>'),
    (D[4], '<div class="scene mid"><div class="jp">君の鼓動がビートなら、<br><span class="em">もう、始まってる。</span></div>'
           '<div class="ensub">If your heartbeat is the beat, it&rsquo;s already begun</div></div>'),
    (D[5], '<div class="scene hi"><div class="title glitch">the sound<br>with no name</div>'
           '<div class="orn"><i></i><u></u></div>'
           '<div class="artist">NANASIGNAL &nbsp;<small>ナナシグナル</small></div>'
           '<div class="freq">Find Your Own Frequency</div>'
           '<div class="tag">New Single &nbsp;&#9654;</div></div>'),
]

meta = dict(title="the sound with no name / NANASIGNAL (Promo Short)",
  desc="誰かが「雑音」と切り捨てた、その周波数で。未来はいつだって最初はノイズと呼ばれた。NANASIGNAL の新曲「the sound with no name」。Music has no labels.")

scenes_js = "[\n" + ",\n".join("    {d:%d, html:`%s`}" % (d, h) for (d, h) in scenes) + "\n  ]"
engine = (ENGINE.replace("SCENES", scenes_js).replace("GLFROM", str(GL_FROM)).replace("GLTO", str(GL_TO)))

BODY = r"""
  <div id="paper"></div>
  <div id="world">
    <div id="slashC" class="slash"></div>
    <div id="slashM" class="slash"></div>
    <div id="cityghost"></div>
    <div id="city"></div>
    <div id="wave"></div>
  </div>
  <div id="flash"></div>
  <div id="scan"></div>
  <div id="grain"></div>
  <div id="scenes"></div>
  <div id="bar"></div>
  <div id="ui">
    <div class="k">NANASIGNAL</div>
    <h1>the sound<br>with no name</h1>
    <p>Find Your Own Frequency</p>
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Montserrat:wght@600;800;900&family=Noto+Sans+JP:wght@700;900&display=swap">
<style>{CSS}</style>
</head>
<body>
<div id="wrap"><div id="stage">
{BODY}
</div></div>
<audio id="bgm" src="nana-bgm.mp3" preload="auto"></audio>
<script>{engine}</script>
</body>
</html>
"""
open(os.path.join(OUT, "nanasignal-short.html"), "w", encoding="utf-8").write(html)
print(f"wrote nanasignal-short.html  ({sum(d for d,_ in scenes)/1000:.1f}s, {len(scenes)} scenes; glitch {GL_FROM}->{GL_TO})")
