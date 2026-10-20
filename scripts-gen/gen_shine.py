# -*- coding: utf-8 -*-
"""
Shine Like I Don't Care / Rolling All Stars — 縦型9:16 宣伝ショート（スワッグ・ブルースロック / 5歳以上の日米向け）
ジャケット準拠：ネオンの夜のダイブバー。左に赤い「BAR」ネオンと雨の街（ボケ・歩く人影）、右に光るジュークボックス、
吊りランプ、磨かれたバーカウンター（ウイスキーのグラス・ボトル・中折れ帽・レコード）、立てかけたギター、
サングラス＆レザーの男がスツールで頬杖、紫煙。タイトルは筆文字（Shine Like=黄／I Don't Care=白）＋Rolling All Stars。
画面テキストは「タイトルとアーティスト」のみ（歌詞テロップなし・ユーザー指示）。映像はビート同期で魅せる。
ビート同期：134BPM（beat 446.9ms, 先頭ダウンビート +85ms）。キックでジュークの光とネオンが脈打ち、サビでスポットがブルーム。
BGM: shine-bgm.mp3 (source 2:42/162s の転調サビ2→サビ3(ホーンMAX) 116s〜：歌詞が明瞭、ギターデュエルは回避)。
決定論レンダリング：window.renderAt(t_ms)/window.TOTAL。?capture=1 でUI非表示。
"""
import os
OUT=os.path.join(os.path.dirname(__file__),"..","shine.html")

CSS=r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0a0604;overflow:hidden}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0a0604}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;transform-origin:top left;
  font-family:"Anton","Arial Black",sans-serif;background:#1a0f0a}
#world{position:absolute;inset:-30px;transform-origin:50% 56%}
/* bar interior */
#room{position:absolute;inset:0;background:
  radial-gradient(60% 46% at 60% 42%, rgba(80,44,20,.7), rgba(30,16,8,.2) 44%, transparent 70%),
  linear-gradient(180deg,#160d08 0%,#241510 40%,#2c1a10 66%,#180e08 100%)}
#backwall{position:absolute;left:300px;right:0;top:0;height:1180px;background:
  repeating-linear-gradient(90deg,rgba(20,12,8,.5) 0 3px,transparent 3px 70px),linear-gradient(180deg,#3a2316,#241510)}
.frame{position:absolute;border:4px solid #4a3420;background:#120b07;box-shadow:0 4px 10px rgba(0,0,0,.4)}
#shelf{position:absolute;left:360px;right:60px;top:300px;height:14px;background:linear-gradient(180deg,#4a3420,#2a1a0f);z-index:2}
/* left window: rainy neon street + BAR neon */
#window{position:absolute;left:24px;top:110px;width:300px;height:830px;z-index:2;border-radius:6px;
  background:linear-gradient(180deg,#141f3a 0%,#1a2846 50%,#122038 100%);box-shadow:inset 0 0 0 12px #2a1a10,0 0 40px rgba(0,0,0,.5)}
.wbokeh{position:absolute;border-radius:50%;filter:blur(4px)}
.wped{position:absolute;bottom:60px;width:34px;border-radius:30px 30px 0 0;background:#0a0f1e}
#wrain{position:absolute;inset:12px;overflow:hidden;z-index:2}
.wstreak{position:absolute;width:2px;background:linear-gradient(180deg,transparent,rgba(170,200,255,.35),transparent)}
#barneon{position:absolute;left:46px;top:150px;width:140px;height:220px;z-index:3;font-family:"Anton",sans-serif;
  color:#ff556a;font-size:120px;line-height:.9;letter-spacing:4px;text-align:center;font-weight:900;
  text-shadow:0 0 10px #ff2e3e,0 0 26px #ff2e3e,0 0 50px #ff2e3e}
/* jukebox (right) */
#juke{position:absolute;right:-10px;top:560px;width:330px;height:760px;z-index:3}
#jukebody{position:absolute;left:20px;bottom:0;width:290px;height:620px;border-radius:150px 150px 20px 20px;
  background:linear-gradient(180deg,#e0a23e 0%,#b87a28 40%,#7a4e18 100%);box-shadow:0 0 50px 10px rgba(255,170,70,.35),inset 0 0 0 10px #5a3a14}
#jukearch{position:absolute;left:34px;top:0;width:262px;height:320px;border-radius:140px 140px 0 0;border:18px solid transparent;z-index:4}
.jtube{position:absolute;left:34px;top:0;width:262px;height:320px;border-radius:140px 140px 0 0;border-style:solid;border-bottom:none}
#jukescreen{position:absolute;left:66px;top:150px;width:198px;height:150px;border-radius:12px;z-index:4;
  background:linear-gradient(180deg,#2a1708,#140b04);box-shadow:inset 0 0 20px rgba(255,180,90,.5)}
.jgrid{position:absolute;background:rgba(255,206,130,.5);border-radius:2px}
#jukeglow{position:absolute;left:0;top:120px;width:330px;height:560px;z-index:3;pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(46% 42% at 52% 50%,rgba(255,180,90,.6),transparent 70%)}
/* hanging lamp over the bar */
#lampwire{position:absolute;left:720px;top:0;width:4px;height:230px;background:#1a110a;z-index:4}
#lamp{position:absolute;left:672px;top:220px;width:100px;height:70px;border-radius:50% 50% 46% 46%;z-index:4;
  background:radial-gradient(circle at 50% 30%,#fff0c8,#e8a63a 70%);box-shadow:0 0 50px 20px rgba(255,180,80,.5)}
#lampcone{position:absolute;left:600px;top:270px;width:244px;height:520px;z-index:3;pointer-events:none;mix-blend-mode:screen;
  background:linear-gradient(180deg,rgba(255,196,110,.5),transparent 80%);clip-path:polygon(38% 0,62% 0,100% 100%,0 100%);filter:blur(8px)}
/* smoke haze */
#haze{position:absolute;left:0;right:0;top:400px;height:800px;z-index:5;pointer-events:none}
.smoke{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(180,160,140,.14),transparent 70%);filter:blur(16px)}
/* the man (silhouette, sunglasses, leather, hand to face) */
#man{position:absolute;left:380px;bottom:360px;width:420px;height:720px;z-index:6;transform-origin:50% 100%}
#mhair{position:absolute;left:158px;top:4px;width:234px;height:214px;background:linear-gradient(110deg,#090507,#171016 72%,#2a1c24);
  border-radius:52% 48% 44% 40% / 62% 58% 42% 40%;transform:rotate(-3deg)}
#mhairlit{position:absolute;left:158px;top:4px;width:234px;height:214px;z-index:8;pointer-events:none;mix-blend-mode:screen;
  background:linear-gradient(250deg,rgba(255,180,90,.5),transparent 40%);border-radius:52% 48% 44% 40% / 62% 58% 42% 40%}
#mhead{position:absolute;left:198px;top:96px;width:146px;height:160px;background:#0a0608;border-radius:46% 54% 50% 50% / 50% 50% 50% 50%}
#mglasses{position:absolute;left:250px;top:150px;width:96px;height:30px;background:#060406;border-radius:8px;z-index:7;transform:rotate(4deg)}
#mglasses::after{content:"";position:absolute;left:8px;top:6px;width:40px;height:5px;border-radius:4px;background:linear-gradient(90deg,rgba(180,210,255,.9),transparent);transform:rotate(-6deg)}
#mbody{position:absolute;left:70px;bottom:0;width:340px;height:520px;background:linear-gradient(100deg,#070406,#150f12 72%);
  clip-path:polygon(34% 0,52% 4%,66% 2%,78% 14%,100% 40%,100% 100%,0 100%,4% 42%,22% 16%)}
#marm{position:absolute;left:250px;top:180px;width:120px;height:330px;background:linear-gradient(100deg,#070406,#140e11);z-index:6;
  clip-path:polygon(44% 0,86% 30%,78% 64%,100% 100%,36% 100%,8% 60%,18% 24%);transform-origin:70% 100%}
#mhand{position:absolute;left:300px;top:150px;width:80px;height:92px;background:#0a0608;border-radius:40% 50% 50% 46%;z-index:7;transform:rotate(-10deg)}
#mrim{position:absolute;left:380px;bottom:360px;width:420px;height:720px;z-index:8;pointer-events:none;mix-blend-mode:screen;opacity:.7;
  background:linear-gradient(255deg,rgba(255,186,96,.7),transparent 42%)}
#cig{position:absolute;left:372px;top:218px;width:12px;height:12px;border-radius:50%;z-index:9;
  background:radial-gradient(circle,#ffe6a0,#ff6a2a 60%,#c03a10);box-shadow:0 0 16px 6px rgba(255,120,50,.7)}
#cigsmoke{position:absolute;left:372px;top:150px;width:60px;height:200px;z-index:8;pointer-events:none}
/* bar counter (foreground) */
#bar{position:absolute;left:-40px;right:-40px;bottom:0;height:430px;z-index:10;
  background:linear-gradient(180deg,#5a3418 0%,#3a2010 30%,#241208 100%)}
#bartop{position:absolute;left:-40px;right:-40px;bottom:388px;height:46px;z-index:10;
  background:linear-gradient(180deg,#7a4a22,#4a2c14);box-shadow:0 8px 24px rgba(0,0,0,.5)}
#barref{position:absolute;left:0;right:0;bottom:0;height:388px;z-index:10;pointer-events:none;overflow:hidden}
.bglint{position:absolute;bottom:0;width:10px;height:100%;border-radius:6px;filter:blur(5px)}
/* objects on the bar */
#glass{position:absolute;left:560px;bottom:150px;width:120px;height:140px;z-index:12}
#glassbody{position:absolute;left:10px;bottom:0;width:100px;height:120px;border-radius:8px 8px 14px 14px;
  background:linear-gradient(180deg,rgba(220,230,245,.22),rgba(200,215,235,.14));box-shadow:inset 0 0 14px rgba(255,200,120,.3),0 6px 14px rgba(0,0,0,.4)}
#whisky{position:absolute;left:16px;bottom:6px;width:88px;height:64px;border-radius:6px 6px 10px 10px;background:linear-gradient(180deg,#e09a34,#a85e1a)}
.ice{position:absolute;border-radius:5px;background:rgba(235,245,255,.45);box-shadow:inset 0 0 6px rgba(255,255,255,.5)}
#glassglint{position:absolute;left:24px;bottom:18px;width:10px;height:70px;border-radius:6px;background:linear-gradient(180deg,rgba(255,255,255,.7),transparent);z-index:12;filter:blur(1px)}
#bottle{position:absolute;right:120px;bottom:150px;width:70px;height:220px;z-index:11;border-radius:30px 30px 10px 10px;
  background:linear-gradient(90deg,#2a3a2a,#4a6a44 50%,#2a3a2a);box-shadow:0 8px 16px rgba(0,0,0,.4)}
#bottle::before{content:"";position:absolute;left:24px;top:-26px;width:22px;height:30px;background:#2a3a2a}
#bottle::after{content:"";position:absolute;left:8px;top:70px;width:54px;height:80px;border-radius:4px;background:rgba(240,230,200,.85)}
#fedora{position:absolute;right:220px;bottom:150px;width:170px;height:80px;z-index:11}
#fedora::before{content:"";position:absolute;left:0;bottom:0;width:170px;height:26px;border-radius:50%;background:#140d08}
#fedora::after{content:"";position:absolute;left:34px;bottom:14px;width:100px;height:64px;border-radius:50px 50px 20px 20px;background:#1c130b}
#vinyl{position:absolute;left:40px;bottom:120px;width:150px;height:60px;z-index:11}
.disc{position:absolute;border-radius:50%;background:radial-gradient(circle at 50% 50%,#2a1a10 0 22%,#0a0608 23% 46%,#2a1a10 47% 50%,#0a0608 51%);box-shadow:0 4px 10px rgba(0,0,0,.4)}
/* guitar leaning (left foreground) */
#guitar{position:absolute;left:10px;bottom:240px;width:150px;height:560px;z-index:11;transform:rotate(10deg);transform-origin:bottom center}
#gbody{position:absolute;left:20px;bottom:0;width:120px;height:170px;border-radius:46% 46% 48% 48%/40% 40% 60% 60%;
  background:radial-gradient(circle at 40% 30%,#e8b84a,#b8781e 60%,#6a4410);box-shadow:0 6px 16px rgba(0,0,0,.4)}
#gbody::after{content:"";position:absolute;left:40%;top:36%;width:28px;height:28px;border-radius:50%;background:#1a0f06}
#gneck{position:absolute;left:62px;bottom:150px;width:24px;height:400px;border-radius:8px;background:linear-gradient(90deg,#3a2414,#5a3c20)}
#ghead{position:absolute;left:52px;top:-4px;width:44px;height:56px;border-radius:6px;background:#241508}
/* spotlight on the man + neon overlays */
#spot{position:absolute;left:300px;top:420px;width:620px;height:1020px;z-index:9;pointer-events:none;mix-blend-mode:screen;opacity:.3;
  background:radial-gradient(40% 40% at 50% 40%,rgba(255,196,110,.62),transparent 66%)}
#neonwash{position:absolute;inset:0;z-index:12;pointer-events:none;mix-blend-mode:screen;opacity:.0;
  background:radial-gradient(50% 30% at 14% 24%,rgba(255,60,80,.4),transparent 60%),radial-gradient(44% 40% at 90% 52%,rgba(255,180,80,.4),transparent 64%)}
#embers{position:absolute;inset:0;z-index:12;pointer-events:none}
.ember{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,200,120,.95),rgba(255,150,70,0) 70%)}
#flash{position:absolute;inset:0;z-index:14;pointer-events:none;background:#fff;opacity:0;mix-blend-mode:screen}
/* text (title + artist only) */
#titlewrap{position:absolute;left:30px;right:30px;top:140px;text-align:center;z-index:16;opacity:0}
.t1{font-family:"Anton","Arial Black",sans-serif;font-size:150px;line-height:.86;letter-spacing:1px;color:#ffd23d;font-style:italic;transform:skewX(-7deg);
  text-shadow:0 5px 0 #000,0 0 30px rgba(255,210,60,.6),4px 4px 0 rgba(120,70,0,.5)}
.t2{font-family:"Anton","Arial Black",sans-serif;font-size:150px;line-height:.86;letter-spacing:1px;color:#fff;font-style:italic;transform:skewX(-7deg);
  text-shadow:0 5px 0 #000,0 0 30px rgba(255,255,255,.4),4px 4px 0 rgba(60,60,60,.5)}
.tund{width:60%;height:5px;margin:16px auto 10px;background:linear-gradient(90deg,transparent,#e8c060,transparent)}
.tart{font-family:"Anton","Arial Black",sans-serif;font-size:50px;letter-spacing:8px;color:#f0d79a;font-style:italic;transform:skewX(-7deg);text-shadow:0 2px 10px rgba(0,0,0,.8)}
#cta{position:absolute;left:30px;right:30px;top:560px;text-align:center;z-index:16;opacity:0}
.badge{display:inline-block;font-family:"Anton",sans-serif;font-size:34px;letter-spacing:6px;color:#1a0f06;background:linear-gradient(90deg,#ffd23d,#ff8a2e);padding:8px 26px;border-radius:8px;margin-bottom:20px;transform:skewX(-7deg)}
.cta-s{font-family:"Anton",sans-serif;font-size:40px;letter-spacing:3px;color:#ffd23d;margin-top:18px;font-style:italic}
.cta-b{font-family:"Anton",sans-serif;font-size:34px;letter-spacing:9px;color:#f0d79a;margin-top:10px;opacity:.92}
#grain{position:absolute;inset:0;z-index:17;pointer-events:none;opacity:.06;background:repeating-radial-gradient(circle at 30% 40%,rgba(255,255,255,.3) 0 1px,transparent 1px 3px)}
#vig{position:absolute;inset:0;pointer-events:none;z-index:18;background:radial-gradient(128% 80% at 50% 46%,transparent 48%,rgba(4,2,1,.72) 100%)}
#ui{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:30}
#play{width:150px;height:150px;border-radius:50%;border:none;cursor:pointer;color:#1a0f06;font-size:60px;background:linear-gradient(135deg,#ffd23d,#ff8a2e);box-shadow:0 10px 40px rgba(0,0,0,.6)}
#bar2{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(255,255,255,.14);z-index:30}
#barf{height:100%;width:0;background:linear-gradient(90deg,#ffd23d,#ff8a2e)}
body.capture #ui,body.capture #bar2{display:none}
"""

BODY=r"""
<div id="wrap"><div id="stage">
 <div id="world">
  <div id="room"></div>
  <div id="backwall"></div><div id="framef"></div><div id="shelf"></div>
  <div id="window"><div id="wbokehf"></div><div id="wpedf"></div><div id="wrain"></div></div>
  <div id="barneon">BAR</div>
  <div id="juke"><div id="jukeglow"></div><div id="jukebody"></div><div id="jtubef"></div><div id="jukescreen"></div><div id="jgridf"></div></div>
  <div id="lampcone"></div><div id="lampwire"></div><div id="lamp"></div>
  <div id="haze"></div>
  <div id="spot"></div>
  <div id="man"><div id="mbody"></div><div id="marm"></div><div id="mhair"></div><div id="mhairlit"></div><div id="mhead"></div><div id="mglasses"></div><div id="mhand"></div></div>
  <div id="mrim"></div><div id="cigsmoke"></div><div id="cig"></div>
  <div id="guitar"><div id="gneck"></div><div id="ghead"></div><div id="gbody"></div></div>
  <div id="bar"></div><div id="barref"></div><div id="bartop"></div>
  <div id="vinyl"></div>
  <div id="glass"><div id="glassbody"></div><div id="whisky"></div><div id="icef"></div></div><div id="glassglint"></div>
  <div id="bottle"></div><div id="fedora"></div>
  <div id="neonwash"></div>
  <div id="embers"></div>
  <div id="flash"></div>
 </div>
 <div id="titlewrap"><div class="t1">SHINE LIKE</div><div class="t2">I DON'T CARE</div><div class="tund"></div><div class="tart">ROLLING ALL STARS</div></div>
 <div id="cta"><span class="badge">NEW SINGLE</span><div class="t1" style="font-size:118px">SHINE LIKE</div><div class="t2" style="font-size:118px">I DON'T CARE</div><div class="tart" style="margin-top:12px">ROLLING ALL STARS</div><div class="cta-s">配信中 / Streaming Now</div><div class="cta-b">LEO MUSIC</div></div>
 <div id="grain"></div>
 <div id="vig"></div>
 <div id="ui"><button id="play">&#9654;</button></div>
 <div id="bar2"><div id="barf"></div></div>
</div></div>
<audio id="bgm" src="shine-bgm.mp3" preload="auto"></audio>
"""

ENGINE=r"""
const stage=document.getElementById('stage');
function fit(){const s=Math.min(innerWidth/1080,innerHeight/1920);stage.style.transform='scale('+s+')';
  document.getElementById('wrap').style.width=innerWidth+'px';}
addEventListener('resize',fit);fit();
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
let _s=909011;function rnd(){_s=(_s*1103515245+12345)&0x7fffffff;return _s/0x7fffffff;}
function mk(p,st,cls){const d=document.createElement('div');if(cls)d.className=cls;if(st)d.style.cssText+=st;p.appendChild(d);return d;}

// wall frames (dim photos)
const frf=document.getElementById('framef');
for(let i=0;i<9;i++){const w=50+rnd()*70,h=60+rnd()*80;mk(frf,'left:'+(380+rnd()*640)+'px;top:'+(60+rnd()*320)+'px;width:'+w+'px;height:'+h+'px;z-index:2;transform:rotate('+((rnd()-0.5)*8)+'deg)','frame');}
// window bokeh (rainy neon street) + pedestrians
const wb=document.getElementById('wbokehf');const WB=['rgba(255,80,90,.8)','rgba(90,150,255,.7)','rgba(255,190,100,.8)','rgba(255,120,200,.7)'];
for(let i=0;i<24;i++){const r=10+rnd()*34;mk(wb,'left:'+(rnd()*280)+'px;top:'+(120+rnd()*560)+'px;width:'+r+'px;height:'+r+'px;background:'+WB[(rnd()*4)|0]+';opacity:'+(0.4+rnd()*0.5),'wbokeh');}
const wp=document.getElementById('wpedf');const peds=[];
for(let i=0;i<4;i++){const h=160+rnd()*90;const e=mk(wp,'left:'+(30+i*70+rnd()*20)+'px;height:'+h+'px;opacity:.9','wped');peds.push({el:e,x:30+i*70,sp:6+rnd()*8,base:rnd()*300});}
// window rain
const wr=document.getElementById('wrain');const wstreaks=[];
for(let i=0;i<30;i++){const hh=30+rnd()*90;const e=mk(wr,'left:'+(rnd()*280)+'px;top:'+(rnd()*800)+'px;height:'+hh+'px;transform:rotate(6deg)','wstreak');wstreaks.push({el:e,y:parseFloat(e.style.top),sp:200+rnd()*300});}
// jukebox arch neon tubes (concentric, chase)
const jt=document.getElementById('jtubef');const jtubes=[];const JC=['#ff3b3b','#ff8a2e','#ffd23d','#ff5aa0'];
for(let i=0;i<4;i++){const e=mk(jt,'left:'+(34+i*16)+'px;top:'+(i*16)+'px;width:'+(262-i*32)+'px;height:'+(320-i*16)+'px;border-radius:'+(140-i*16)+'px '+(140-i*16)+'px 0 0;border:7px solid '+JC[i]+';border-bottom:none;box-shadow:0 0 14px '+JC[i]+';z-index:4','jtube');jtubes.push({el:e,c:JC[i],ph:i});}
// jukebox screen grid
const jg=document.getElementById('jgridf');const jgrid=[];
for(let r=0;r<4;r++)for(let c=0;c<6;c++){const e=mk(jg,'left:'+(72+c*32)+'px;top:'+(158+r*36)+'px;width:24px;height:22px;z-index:4','jgrid');jgrid.push({el:e,ph:rnd()*6.28});}
// smoke
const hz=document.getElementById('haze');const smokes=[];
for(let i=0;i<7;i++){const w=200+rnd()*260;const e=mk(hz,'width:'+w+'px;height:'+w+'px','smoke');smokes.push({el:e,x:rnd()*900+100,y:rnd()*700,sp:8+rnd()*14,ph:rnd()*6.28});}
// cigarette smoke wisps
const cs=document.getElementById('cigsmoke');const cigw=[];
for(let i=0;i<8;i++){const e=mk(cs,'position:absolute;width:'+(14+rnd()*14)+'px;height:'+(14+rnd()*14)+'px;border-radius:50%;background:radial-gradient(circle,rgba(200,190,180,.4),transparent 70%);filter:blur(4px)','');cigw.push({el:e,base:rnd()*200,sp:30+rnd()*30,amp:10+rnd()*16,ph:rnd()*6.28});}
// bar reflections
const br=document.getElementById('barref');const bglints=[];const BG=['#ff5a5a','#ffb24a','#ffd23d','#8aa0ff'];
for(let i=0;i<12;i++){const e=mk(br,'left:'+(rnd()*1080)+'px;background:linear-gradient(180deg,'+BG[(rnd()*4)|0]+'cc,transparent)','bglint');bglints.push({el:e,ph:rnd()*6.28});}
// whiskey ice
const icef=document.getElementById('icef');
mk(icef,'left:26px;bottom:14px;width:30px;height:26px','ice');mk(icef,'left:54px;bottom:26px;width:26px;height:24px','ice');
// vinyl discs
const vf=document.getElementById('vinyl');
mk(vf,'left:0;bottom:0;width:140px;height:140px;transform:rotate(-8deg)','disc');mk(vf,'left:18px;bottom:8px;width:120px;height:120px','disc');
// embers
const ef=document.getElementById('embers');const embers=[];
for(let i=0;i<26;i++){const w=3+rnd()*9;const e=mk(ef,'width:'+w+'px;height:'+w+'px','ember');embers.push({el:e,x:rnd()*1080,sp:10+rnd()*30,amp:16+rnd()*40,ph:rnd()*6.28,base:rnd()*1920});}

const world=document.getElementById('world'),barneon=document.getElementById('barneon'),lamp=document.getElementById('lamp'),lampcone=document.getElementById('lampcone'),
  jukeglow=document.getElementById('jukeglow'),spot=document.getElementById('spot'),neonwash=document.getElementById('neonwash'),cig=document.getElementById('cig'),
  man=document.getElementById('man'),marm=document.getElementById('marm'),flash=document.getElementById('flash'),
  titlewrap=document.getElementById('titlewrap'),cta=document.getElementById('cta'),glassglint=document.getElementById('glassglint');

const BEAT=446.9, OFF=85;               // 134bpm, first downbeat +85ms
// BGM = source 116s.. (chorus2 key-up -> chorus3 horns max). climax builds to the end.
const CL_IN=2000, CL_PK=25500;
function smooth(t,a,b){if(t<=a)return 0;if(t>=b)return 1;const x=(t-a)/(b-a);return x*x*(3-2*x);}

window.renderAt=function(t){
  const ts=t/1000;
  const bp=(((t-OFF)%BEAT)+BEAT)%BEAT/BEAT;
  const kick=Math.pow(Math.max(0,1-bp*1.7),2);
  const beatN=Math.floor((t-OFF)/BEAT);
  const down=(((beatN%4)+4)%4===0)?1:0.55;
  const climax=smooth(t,CL_IN,CL_PK);
  const energy=0.6+0.4*climax;
  // cool thump (subtle, not bouncy)
  world.style.transform='scale('+(1.01+0.01*kick*energy)+')';
  // BAR neon: flicker + beat pulse
  const flk=(rnd()<0.04)?0.5:1;
  barneon.style.opacity=(flk*(0.7+0.3*kick*down)).toFixed(3);
  barneon.style.textShadow='0 0 10px #ff2e3e,0 0 '+(26+20*kick)+'px #ff2e3e,0 0 '+(50+40*kick*down)+'px #ff2e3e';
  // jukebox tubes chase + pulse
  for(const tb of jtubes){const ph=(beatN+tb.ph);const on=0.4+0.6*Math.abs(Math.sin(ts*2.0+tb.ph*1.1));
    tb.el.style.opacity=((on*(0.7+0.4*kick))*energy).toFixed(3);
    tb.el.style.boxShadow='0 0 '+(10+18*kick)+'px '+tb.c;}
  jukeglow.style.opacity=(0.5+0.3*kick+0.2*climax).toFixed(3);
  for(const g of jgrid){g.el.style.opacity=(0.25+0.6*Math.abs(Math.sin(ts*3+g.ph))*(0.6+0.5*kick)).toFixed(3);}
  // hanging lamp swing + pulse
  lamp.style.transform='translateX('+(Math.sin(ts*0.8)*8).toFixed(1)+'px)';
  lamp.style.boxShadow='0 0 '+(50+30*kick)+'px '+(20+14*kick)+'px rgba(255,180,80,'+(0.5+0.2*kick)+')';
  lampcone.style.opacity=(0.4+0.2*kick+0.1*climax).toFixed(3);
  // smoke drift (rises slowly, wraps)
  for(const s of smokes){const x=s.x+Math.sin(ts*0.2+s.ph)*30;const y=((s.y - ts*s.sp)%800+800)%800;
    s.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';
    s.el.style.opacity=(0.45+0.3*Math.sin(ts*0.3+s.ph)).toFixed(3);}
  // window rain + pedestrians drift
  for(const w of wstreaks){let y=((w.y+ts*w.sp)%820);w.el.style.transform='translateY('+y.toFixed(1)+'px)';w.el.style.opacity=.5;}
  for(const p of peds){let x=((p.base+ts*p.sp)%360)-30;p.el.style.transform='translateX('+(x-p.x).toFixed(1)+'px)';}
  // spotlight on the man blooms with the chorus
  spot.style.opacity=(0.28+0.1*kick+0.5*climax).toFixed(3);
  spot.style.transform='scale('+(1+0.1*climax+0.02*kick)+')';
  neonwash.style.opacity=(0.2+0.5*climax).toFixed(3);
  // cigarette ember glow + flare on beat; smoke rises
  cig.style.opacity=(0.7+0.3*Math.abs(Math.sin(ts*1.3))+0.2*kick).toFixed(3);
  cig.style.boxShadow='0 0 '+(16+10*kick)+'px '+(6+4*kick)+'px rgba(255,120,50,.75)';
  for(const c of cigw){let y=200-((ts*c.sp+c.base)%200);const prog=1-y/200;
    c.el.style.transform='translate('+(Math.sin(ts*1.1+c.ph+prog*3)*c.amp).toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(0.6+prog*1.3)+')';
    c.el.style.opacity=((prog<0.15?prog/0.15:1-smooth(prog,0.5,1))*0.5).toFixed(3);}
  // man subtle cool nod on strong beats
  man.style.transform='translateY('+(-4*kick*down).toFixed(1)+'px) rotate('+(Math.sin(ts*0.5)*0.4).toFixed(2)+'deg)';
  // bar reflections shimmer
  for(const b of bglints){b.el.style.opacity=((0.25+0.4*Math.abs(Math.sin(ts*2+b.ph)))*(0.6+0.4*kick)).toFixed(3);b.el.style.transform='scaleY('+(1+0.25*kick)+')';}
  // whiskey glint
  glassglint.style.opacity=(0.4+0.5*Math.abs(Math.sin(ts*1.6))+0.2*kick).toFixed(3);
  // embers rise
  for(const e of embers){let y=1960-((ts*e.sp+e.base)%2100);let x=e.x+Math.sin(ts*0.5+e.ph)*e.amp;
    const op=(y>1760?smooth(y,1960,1740):(y<140?smooth(y,-60,140):1));
    e.el.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';e.el.style.opacity=(op*(0.3+0.5*kick+0.3*climax)).toFixed(3);}
  // title reveals (only title+artist): big open 0.3-5s, re-flash ~13s, blaze 20.5-26.5s
  const tOpen=Math.min(smooth(t,300,1100),1-smooth(t,4600,5200));
  const tFlash=Math.min(smooth(t,12600,12900),1-smooth(t,13900,14300))*0.9;
  const tBlaze=Math.min(smooth(t,20500,21300),1-smooth(t,26300,26900));
  const tvis=Math.max(tOpen,tFlash,tBlaze);
  titlewrap.style.opacity=tvis.toFixed(3);
  titlewrap.style.transform='scale('+(1+0.03*kick*(tBlaze>0?1:0.4)+0.04*tBlaze)+')';
  // CTA 26.7-30
  const cvis=smooth(t,26700,27400);
  cta.style.opacity=cvis.toFixed(3);
  cta.style.transform='scale('+(0.98+0.02*cvis+0.02*kick)+')';
  // beat flash accents at the climax downbeats
  flash.style.opacity=(0.1*kick*down*climax).toFixed(3);
};

const bgm=document.getElementById('bgm');const barf=document.getElementById('barf');let t0=0;const TOTAL=30000;window.TOTAL=TOTAL;
function play(){document.getElementById('ui').style.display='none';
  try{bgm.currentTime=0;bgm.play();}catch(e){}
  t0=performance.now();
  (function loop(){const t=performance.now()-t0;const tt=Math.min(t,TOTAL);window.renderAt(tt);
    barf.style.width=(100*tt/TOTAL)+'%';if(t<TOTAL)requestAnimationFrame(loop);})();
  setTimeout(()=>{const s0=performance.now();(function fo(){const k=(performance.now()-s0)/1200;
    bgm.volume=Math.max(0,0.95*(1-k));if(k<1)requestAnimationFrame(fo);else bgm.pause();})();},TOTAL-1200);
}
document.getElementById('play').addEventListener('click',play);
window.renderAt(0);
"""

html=f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shine Like I Don't Care / Rolling All Stars</title>
<style>{CSS}</style></head>
<body>
{BODY}
<script>
{ENGINE}
</script>
</body></html>"""
with open(OUT,"w",encoding="utf-8") as f:f.write(html)
print("wrote",os.path.abspath(OUT),len(html),"bytes")
