/* 叡智の灯火 / Beacon of Wisdom — MVP（ビルド不要 / localStorage 永続 / 日英対応）
   設計: ../SPEC.md  データ: data/*.json (→ gamedata.js)
   i18n: L(ja,en) で文言を切替。本文/名言は data の *En フィールド or nameEn/quoteOriginal にフォールバック。 */
(function () {
  "use strict";
  var D = window.GAME_DATA;
  if (!D) { document.getElementById("app").innerHTML = "<p style='padding:24px'>データを読み込めませんでした。<br>gamedata.js を確認してください。</p>"; return; }

  var API = ((window.LWG_API || "") + "").replace(/\/+$/, "");   // 会員API。空なら従来どおりクライアント同梱で動作
  var SAGES = {}; D.sages.sages.forEach(function (s) { SAGES[s.id] = s; });
  var RANKS = D.sages.ranks;
  var EVENTS = D.events.events;
  var LEGENDS = (D.legends && D.legends.legends) || [];
  var SAVE_KEY = "lifewisdom.save.v1";
  var CODEX_KEY = "lifewisdom.codex.v1";
  var ACCLAIM_KEY = "lifewisdom.acclaim.v1";
  var LANG_KEY = "lifewisdom.lang.v1";
  var REST_THRESHOLD = 25;

  // ---------- i18n ----------
  var lang = (function () { try { return localStorage.getItem(LANG_KEY) === "en" ? "en" : "ja"; } catch (e) { return "ja"; } })();
  function setLang(l) { lang = (l === "en") ? "en" : "ja"; try { localStorage.setItem(LANG_KEY, lang); } catch (e) {} }
  function L(ja, en) { return lang === "en" ? en : ja; }

  var RARITY_LABEL = { common: ["並", "Common"], rare: ["希", "Rare"], sacred: ["神聖", "Sacred"], legendary: ["伝説", "Legendary"] };
  function rarityLabel(r) { var x = RARITY_LABEL[r] || ["", ""]; return lang === "en" ? x[1] : x[0]; }
  var STAT = { mind: ["心", "Mind"], wisdom: ["叡智", "Wisdom"], bonds: ["絆", "Bonds"], wealth: ["財", "Wealth"], passion: ["情熱", "Passion"] };
  function statLabel(k) { var x = STAT[k]; return x ? (lang === "en" ? x[1] : x[0]) : k; }
  var CAT = { work: ["仕事", "Work"], relationship: ["人間関係", "Relationships"], love: ["恋愛", "Love"], study: ["学業", "Study"], money: ["お金", "Money"], health: ["健康", "Health"], self: ["自己", "Self"] };
  var CAT_KEYS = ["work", "relationship", "love", "study", "money", "health", "self"];
  function catLabel(c) { var x = CAT[c]; return x ? (lang === "en" ? x[1] : x[0]) : c; }
  var MOOD = { down: ["落ち込み", "Down"], lost: ["迷い", "Lost"], high: ["高揚", "Uplifted"] };
  function moodLabel(m) { var x = MOOD[m]; return x ? (lang === "en" ? x[1] : x[0]) : m; }
  var CAT_ICON = { work: "💼", relationship: "🤝", love: "💗", study: "📚", money: "🪙", health: "🌱", self: "🧭" };
  function catIcon(c) { return CAT_ICON[c] || "•"; }
  var MOOD_ICON = { down: "🌧", lost: "🌫", high: "✨" };
  function moodIcon(m) { return MOOD_ICON[m] || ""; }
  var RANK_TITLE_EN = { 1: "The Kindler", 2: "Sprout of Learning", 3: "Questioner", 4: "Thinker", 5: "The Prudent", 6: "Great Sage", 7: "The Enlightened", 8: "Seeker of Legends", 9: "Sacred Guidance", 10: "Wisdom Mastery" };
  function rankTitle(r) { return lang === "en" ? (RANK_TITLE_EN[r] || RANKS[r].title) : RANKS[r].title; }
  var MAX_RANK = 10;

  // 会員（note 月額）判定：その月のコードを入れた月だけ有効＝毎月の更新が要る
  function monthKey(d) { return d.getFullYear() * 100 + (d.getMonth() + 1); }
  function expectedCode(d) { var m = monthKey(d); var n = ((m * 7919) % 9000) + 1000; return "TOMO-" + n; }
  function isPaid() { return state.paidMonth === monthKey(new Date()); }
  function sageTier(id) { var s = SAGES[id]; return (s && s.tier) ? s.tier : "paid"; }

  // 有料データをサーバーから取り込む（API利用時のみ）。無料seedに重複なくマージ。
  function applyPaidData(d) {
    if (!d) return;
    (d.sages || []).forEach(function (s) { if (s && s.id && !SAGES[s.id]) { SAGES[s.id] = s; D.sages.sages.push(s); } });
    (d.events || []).forEach(function (e) { if (e && e.id && !EVENTS.some(function (x) { return x.id === e.id; })) EVENTS.push(e); });
    (d.legends || []).forEach(function (l) { if (l && l.id && !LEGENDS.some(function (x) { return x.id === l.id; })) LEGENDS.push(l); });
  }
  function fetchPaid() {
    if (!API || !state.token) return Promise.resolve();
    return fetch(API + "/api/content", { headers: { "Authorization": "Bearer " + state.token } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function (d) { applyPaidData(d); });
  }

  // ---------- 音（Web Audioで原音合成・権利クリーン・外部依存なし） ----------
  var SOUND_KEY = "lifewisdom.sound.v1";
  var soundOn = (function () { try { return localStorage.getItem(SOUND_KEY) !== "off"; } catch (e) { return true; } })();
  var actx = null;
  function audioCtx() {
    if (!actx) { try { actx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { actx = null; } }
    if (actx && actx.state === "suspended" && actx.resume) { try { actx.resume(); } catch (e) {} }
    return actx;
  }
  // 単音（ゆるい立ち上がり＝クリック音を防ぐ）
  function tone(freq, dur, gain, delay) {
    var a = audioCtx(); if (!a || !soundOn) return;
    var t = a.currentTime + (delay || 0);
    var o = a.createOscillator(), g = a.createGain();
    o.type = "sine"; o.frequency.value = freq;
    o.connect(g); g.connect(a.destination);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + 0.05);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.start(t); o.stop(t + dur + 0.05);
  }
  // 鐘/おりん：複数の倍音をまとめ、ローパスで角を取り、ふわっと減衰
  function bell(parts, dur, gain, cutoff) {
    var a = audioCtx(); if (!a || !soundOn) return;
    var t = a.currentTime;
    var g = a.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + 0.07);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    var f = a.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = cutoff || 1600; f.Q.value = 0.6;
    g.connect(f); f.connect(a.destination);
    parts.forEach(function (p) {
      var o = a.createOscillator(); o.type = "sine"; o.frequency.value = p[0];
      var pg = a.createGain(); pg.gain.value = p[1];
      o.connect(pg); pg.connect(g); o.start(t); o.stop(t + dur + 0.1);
    });
  }
  function sfxChime() { bell([[587.33, 1], [880, 0.35], [1174.66, 0.14]], 2.2, 0.05, 1500); }                    // 決断＝柔らかなおりん（静か）
  function sfxSacred() { bell([[196, 1], [392, 0.5], [587.33, 0.28], [783.99, 0.14]], 3.2, 0.11, 2200); }         // 神聖・伝説＝深い鐘
  function sfxRest() { bell([[523.25, 1], [659.25, 0.6], [783.99, 0.5]], 1.8, 0.06, 1700); }                      // 休息＝やわらかな和音
  function toggleSound() { soundOn = !soundOn; try { localStorage.setItem(SOUND_KEY, soundOn ? "on" : "off"); } catch (e) {} if (soundOn) sfxChime(); }

  // 環境音（ゆるいパッド＋まれな風鈴・任意ON）
  var AMB_KEY = "lifewisdom.amb.v1";
  var ambientOn = (function () { try { return localStorage.getItem(AMB_KEY) === "on"; } catch (e) { return false; } })();
  var ambNodes = null;
  // BGM（楽曲ファイル・ループ再生）。タイトル右上 🎐 でON。
  var BGM_SRC = "bgm.mp3";
  var bgm = null;
  function startAmbient() {
    try {
      if (!bgm) { bgm = new Audio(BGM_SRC); bgm.loop = true; bgm.volume = 0.45; bgm.preload = "auto"; }
      var p = bgm.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  function stopAmbient() { try { if (bgm) bgm.pause(); } catch (e) {} }
  function toggleAmbient() { ambientOn = !ambientOn; try { localStorage.setItem(AMB_KEY, ambientOn ? "on" : "off"); } catch (e) {} if (ambientOn) startAmbient(); else stopAmbient(); }

  // ---------- 夜モード（ダーク） ----------
  var NIGHT_KEY = "lifewisdom.night.v1";
  var night = (function () { try { return localStorage.getItem(NIGHT_KEY) === "on"; } catch (e) { return false; } })();
  function applyNight() { try { if (night) app.classList.add("night"); else app.classList.remove("night"); } catch (e) {} }
  function toggleNight() { night = !night; try { localStorage.setItem(NIGHT_KEY, night ? "on" : "off"); } catch (e) {} applyNight(); }

  // 叡智の位（段位）。生涯記録ベース＝下がらない。
  var POSITIONS = [
    { min: 0, ja: "灯火の見習い", g: "無級", en: "Kindling Novice", eg: "Ungraded" },
    { min: 60, ja: "学びの徒", g: "五級", en: "Student of Learning", eg: "5th Kyū" },
    { min: 150, ja: "思索の人", g: "三級", en: "Thinker", eg: "3rd Kyū" },
    { min: 280, ja: "求道の人", g: "一級", en: "Seeker", eg: "1st Kyū" },
    { min: 430, ja: "賢慮の士", g: "初段", en: "Prudent One", eg: "1st Dan" },
    { min: 620, ja: "叡智の探究者", g: "参段", en: "Wisdom Seeker", eg: "3rd Dan" },
    { min: 850, ja: "達観の人", g: "伍段", en: "Enlightened One", eg: "5th Dan" },
    { min: 1100, ja: "心の師範", g: "七段", en: "Master of the Heart", eg: "7th Dan" },
    { min: 1400, ja: "叡智の達人", g: "九段", en: "Adept of Wisdom", eg: "9th Dan" },
    { min: 1700, ja: "賢聖", g: "十段", en: "Sage Saint", eg: "10th Dan" },
    { min: 1950, ja: "叡智名人", g: "名人", en: "Grandmaster of Wisdom", eg: "Meijin" },
    { min: 2200, ja: "叡智皆伝", g: "免許皆伝", en: "Wisdom Mastery", eg: "Full Mastery" }
  ];
  function posTitle(p) { return lang === "en" ? p.en : p.ja; }
  function posGrade(p) { return lang === "en" ? p.eg : p.g; }

  // ---------- 内容のローカライズ（データのフォールバック） ----------
  function sageName(sage) { return sage ? (lang === "en" && sage.nameEn ? sage.nameEn : sage.name) : ""; }
  function qText(o) { return lang === "en" ? (o.quoteEn || o.quoteOriginal || o.quote) : o.quote; }
  function evTitle(ev) { return lang === "en" ? (ev.titleEn || ev.title) : ev.title; }
  function evBody(ev) { return lang === "en" ? (ev.bodyEn || ev.body) : ev.body; }

  var app = document.getElementById("app");
  var state = load() || newGame();
  var codex = loadCodex();
  var acclaim = loadAcclaim();

  // ---------- セーブ/ロード ----------
  function newGame() {
    return { v: 1, stats: { mind: 60, wisdom: 0, bonds: 50, wealth: 50, passion: 50 }, turn: 0, journal: [], seen: [], paidMonth: 0, favoriteSage: null };
  }
  function save() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); } catch (e) {} }
  function load() { try { var r = localStorage.getItem(SAVE_KEY); return r ? JSON.parse(r) : null; } catch (e) { return null; } }
  function resetGame() { state = newGame(); save(); showTitle(); }

  function loadCodex() { try { return JSON.parse(localStorage.getItem(CODEX_KEY)) || []; } catch (e) { return []; } }
  function saveCodex() { try { localStorage.setItem(CODEX_KEY, JSON.stringify(codex)); } catch (e) {} }
  function codexHas(id) { return codex.indexOf(id) >= 0; }
  function codexAdd(id) { if (!codexHas(id)) { codex.push(id); saveCodex(); } }

  function loadAcclaim() { try { var r = JSON.parse(localStorage.getItem(ACCLAIM_KEY)); return (r && r.quotes) ? r : { quotes: {}, cats: {} }; } catch (e) { return { quotes: {}, cats: {} }; } }
  function saveAcclaim() { try { localStorage.setItem(ACCLAIM_KEY, JSON.stringify(acclaim)); } catch (e) {} }
  function recordAcclaim(quoteKey, category) {
    var changed = false;
    if (quoteKey && !acclaim.quotes[quoteKey]) { acclaim.quotes[quoteKey] = 1; changed = true; }
    if (category && !acclaim.cats[category]) { acclaim.cats[category] = 1; changed = true; }
    if (changed) saveAcclaim();
  }
  function playerProgress() {
    var q = Object.keys(acclaim.quotes).length, c = Object.keys(acclaim.cats).length, l = codex.length;
    return { points: q * 12 + l * 120 + c * 50, quotes: q, cats: c, legends: l };
  }
  function positionFor(points) { var p = POSITIONS[0]; for (var i = 0; i < POSITIONS.length; i++) { if (points >= POSITIONS[i].min) p = POSITIONS[i]; } return p; }
  function nextPosition(points) { for (var i = 0; i < POSITIONS.length; i++) { if (points < POSITIONS[i].min) return POSITIONS[i]; } return null; }

  function rarityOf(sageId, isLegend) {
    if (isLegend) return "legendary";
    if (isScripture(sageId)) return "sacred";
    var s = SAGES[sageId];
    if (s && s.rank >= 3) return "rare";
    return "common";
  }
  function rollLegend() {
    if (!isPaid()) return null;
    var eligible = LEGENDS.filter(function (l) { return !codexHas(l.id) && state.stats.wisdom >= (l.minWisdom || 0); });
    if (eligible.length === 0) return null;
    var p = 0.06 + Math.min(0.20, state.stats.wisdom / 1200);
    if (Math.random() >= p) return null;
    return eligible[Math.floor(Math.random() * eligible.length)];
  }

  // ---------- ヘルパ ----------
  function clamp(n) { return Math.max(0, Math.min(100, Math.round(n))); }
  function applyStat(k, delta) {
    var before = state.stats[k] || 0;
    var nv = before + delta;
    state.stats[k] = (k === "wisdom") ? Math.max(0, Math.round(nv)) : clamp(nv);
    return state.stats[k] - before;
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function isScripture(id) { return id.indexOf("scripture") === 0; }
  function scriptureTag() { return L("（聖典）", " (Scripture)"); }

  function unlockedRank() { var r = 1; for (var k = 1; k <= MAX_RANK; k++) { if (state.stats.wisdom >= RANKS[k].unlockWisdom) r = k; } return r; }
  function nextRankInfo() {
    var cur = unlockedRank();
    if (cur >= MAX_RANK) return null;
    var nk = cur + 1;
    return { rank: nk, need: RANKS[nk].unlockWisdom, have: state.stats.wisdom, prevNeed: RANKS[cur].unlockWisdom };
  }
  // 表示状態: "show" | "member"（会員限定）| "rank"（叡智で解放）
  function adviceState(adv) {
    if (adv.sageId === "original" || sageTier(adv.sageId) === "free") return "show";
    if (!isPaid()) return "member";
    var sage = SAGES[adv.sageId];
    if (sage && state.stats.wisdom < RANKS[sage.rank].unlockWisdom) return "rank";
    return "show";
  }
  function discChar(sage) {
    if (!sage) return "?";
    if (sage.field === "scripture") return "✦";
    return sageName(sage).charAt(0);
  }
  function recomputeFavorite() {
    var c = {}; state.journal.forEach(function (j) {
      if (j.chosenSageId && j.chosenSageId !== "original" && !isScripture(j.chosenSageId)) c[j.chosenSageId] = (c[j.chosenSageId] || 0) + 1;
    });
    var best = null, n = 0; Object.keys(c).forEach(function (k) { if (c[k] > n) { n = c[k]; best = k; } });
    state.favoriteSage = best;
  }

  // ---------- ステータスバー ----------
  function statusbar() {
    var s = state.stats, nx = nextRankInfo();
    var wis;
    if (nx) {
      var span = nx.need - nx.prevNeed, prog = Math.max(0, Math.min(1, (nx.have - nx.prevNeed) / span));
      var rem = Math.max(0, nx.need - nx.have);
      wis = '<div class="wisrow">' +
        L("叡智 " + s.wisdom + " ／ 次の境地「" + esc(rankTitle(nx.rank)) + "」まで あと " + rem,
          "Wisdom " + s.wisdom + " / " + rem + " to the next stage “" + esc(rankTitle(nx.rank)) + "”") +
        '<div class="wbar"><i style="width:' + (prog * 100).toFixed(0) + '%"></i></div></div>';
    } else {
      wis = '<div class="wisrow">' + L("叡智 " + s.wisdom + " ／ 最高の境地「" + esc(rankTitle(MAX_RANK)) + "」に到達",
        "Wisdom " + s.wisdom + " / Reached the highest stage “" + esc(rankTitle(MAX_RANK)) + "”") + '</div>';
    }
    return '<div class="statusbar">' +
      '<span class="heart">❤️</span>' +
      '<span class="mindbar"><i style="width:' + s.mind + '%"></i></span>' +
      '<span class="rankchip">' + esc(rankTitle(unlockedRank())) + '</span>' +
      '<span class="sb-ctrl" style="margin-left:auto;display:flex;gap:4px">' +
      '<button class="snd" data-act="night" title="' + L("夜モード", "Night mode") + '">' + (night ? "☀️" : "🌙") + '</button>' +
      '<button class="snd' + (ambientOn ? " on" : "") + '" data-act="ambient" title="' + L("BGM", "BGM") + '">🎐</button>' +
      '<button class="snd" data-act="sound" title="' + L("音のオン/オフ", "Sound on/off") + '">' + (soundOn ? "🔔" : "🔕") + '</button>' +
      '<button class="snd" data-act="title" title="' + L("タイトルへ", "Title") + '">🏠</button>' +
      '</span>' +
      '</div>' + wis;
  }

  function dailyRecall() {
    var pool = state.journal.filter(function (j) { return j.feedback === "resonated"; });
    if (pool.length === 0) pool = state.journal;
    if (pool.length === 0) return null;
    var day = Math.floor(Date.now() / 86400000);
    return pool[day % pool.length];
  }

  // ---------- タイトル ----------
  function showTitle() {
    curView = showTitle;
    var has = state.journal.length > 0;
    var pg = playerProgress(); var pos = positionFor(pg.points);
    var recall = dailyRecall();
    var recallInner = recall ? ('<span class="recall-k">' + L("🕯 今日、心に留めたい言葉", "🕯 A word to keep in your heart today") + '</span>' +
      '<p class="recall-q">' + esc(recall.quote) + '</p><span class="recall-f">— ' + esc(recall.sageName) + '</span>') : "";
    var recallHtml = (API || recallInner) ? '<div class="recall">' + recallInner + '</div>' : "";
    var posLine = (has || pg.points > 0)
      ? '<p class="title-pos">' + L("あなたの位 ― ", "Your rank — ") + '<b>' + esc(posTitle(pos)) + '</b><span class="grade">' + esc(posGrade(pos)) + '</span></p>'
      : '';
    var langToggle = '<div class="lang-toggle">' +
      '<button class="snd" data-act="night" title="' + L("夜モード", "Night mode") + '">' + (night ? "☀️" : "🌙") + '</button>' +
      '<button class="snd' + (ambientOn ? " on" : "") + '" data-act="ambient" title="' + L("環境音", "Ambient sound") + '">🎐</button>' +
      '<button class="snd" data-act="sound" title="' + L("音のオン/オフ", "Sound on/off") + '">' + (soundOn ? "🔔" : "🔕") + '</button>' +
      '<button class="' + (lang === "ja" ? "on" : "") + '" data-act="lang" data-lang="ja">日本語</button>' +
      '<button class="' + (lang === "en" ? "on" : "") + '" data-act="lang" data-lang="en">English</button></div>';
    var html = langToggle + '<div class="fade title-wrap">' +
      '<div class="flame">🪔</div>' +
      '<h1 class="title">' + L("叡智の灯火", "Beacon of Wisdom") + '</h1>' +
      '<p class="subtitle">' + L("人生の岐路と、偉人たちの言葉", "Life's crossroads, and the words of the wise") + '</p>' +
      posLine + '</div>' +
      '<div class="title-actions">' +
      '<button class="btn gold" data-act="' + (has ? "start" : "walk") + '">' + (has ? L("つづきから歩む", "Continue your journey") : L("人生を歩む", "Begin your life")) + '</button>' +
      '<button class="btn gold" data-act="consult">' + L("悩みを相談する", "Seek counsel") + '</button>' +
      '<button class="btn ghost" data-act="book">' + L("わが叡智の書を見る", "Open the Book of Wisdom") + (has ? "（" + state.journal.length + "）" : "") + '</button>' +
      '<button class="btn ghost" data-act="cert">' + L("叡智の免許状を見る", "View your certificate") + '</button>' +
      (isMaster() ? '<button class="btn gold hiden-open" data-act="hiden">' + L("📜 叡智皆伝の書をひらく", "📜 Open your Book of Mastery") + '</button>' : "") +
      (isPaid() ? "" : '<button class="btn ghost" data-act="membergate">' + L("会員コードを入力（note会員）", "Enter member code (note)") + '</button>') +
      (has ? '<button class="btn ghost" data-act="reset">' + L("はじめからやり直す", "Start a new life") + '</button>' : "") +
      '</div>' +
      (isPaid() ? '<p class="member-on">' + L("✓ 会員（今月有効）", "✓ Member (valid this month)") + '</p>' : "") +
      '<p class="codex-tease">' + L("✦ 伝説の言葉 " + codex.length + " / " + LEGENDS.length + " 蒐集 ✦", "✦ Legendary Words " + codex.length + " / " + LEGENDS.length + " collected ✦") + '</p>' +
      recallHtml +
      '<p class="tagline">' + L("迷ったとき、世界の偉人があなたの相談相手になる。<br>言葉を選び、暮らしに活かし、少しずつ賢くなっていく。",
        "When you are lost, the great minds of the world become your counsel.<br>Choose a word, live it, and grow a little wiser.") + '</p>' +
      '<p class="notice">' + L("※ これは制作中のプロトタイプ（MVP）です。名言はすべて出典付きで裏取りしています。<br>つらさが長く続くときは、どうか一人で抱えず、信頼できる人や専門の窓口に頼ってください。",
        "※ This is a prototype (MVP). Every quote is sourced and fact-checked.<br>If hardship persists, please don't carry it alone — reach out to someone you trust or a professional resource.") + '</p>';
    render(html);
    if (API) loadDaily();
  }

  // ---------- イベント ----------
  var currentEvent = null, currentLegend = null;
  var curView = showTitle;   // 現在の画面（音/夜モード切替後に同じ画面を再描画するため）
  var mode = "auto", consultCat = null;
  function pickEvent() {
    var avail = isPaid() ? EVENTS : EVENTS.filter(function (e) { return e.tier === "free"; });
    var pool;
    if (mode === "consult" && consultCat) {
      pool = avail.filter(function (e) { return e.category === consultCat && state.seen.indexOf(e.id) < 0; });
      if (pool.length === 0) pool = avail.filter(function (e) { return e.category === consultCat; });
    } else {
      pool = avail.filter(function (e) { return state.seen.indexOf(e.id) < 0; });
      if (pool.length === 0) { state.seen = []; pool = avail.slice(); }
    }
    if (pool.length === 0) return null;
    return pool[Math.floor(Math.random() * pool.length)];
  }
  function proceed() {
    if (state.stats.mind < REST_THRESHOLD) { showRest(); return; }
    var ev = pickEvent();
    if (!ev) { showMemberGate(); return; }
    currentEvent = ev;
    currentLegend = rollLegend();
    showEvent(currentEvent);
  }
  function freeCategories() { var m = {}; EVENTS.forEach(function (e) { if (e.tier === "free") m[e.category] = 1; }); return m; }
  function showConsult() {
    curView = showConsult;
    var fc = freeCategories(), paid = isPaid();
    var grid = CAT_KEYS.map(function (c) {
      if (!paid && !fc[c]) return '<button class="consult-cat locked" data-act="membergate"><span class="cc-ic">' + catIcon(c) + '</span>' + esc(catLabel(c)) + ' 🔒</button>';
      return '<button class="consult-cat" data-consultcat="' + c + '"><span class="cc-ic">' + catIcon(c) + '</span>' + esc(catLabel(c)) + '</button>';
    }).join("");
    render('<div class="fade">' + statusbar() +
      '<h2 class="event-title">' + L("どんなことで、悩んでいますか？", "What is troubling you?") + '</h2>' +
      '<p class="event-body">' + L("いま心にあるものを選ぶと、その悩みに効く言葉が訪れます。", "Choose what's on your heart, and words for that worry will come.") + '</p>' +
      '<div class="consult-grid">' + grid + '</div>' +
      '<button class="btn ghost" data-act="walk">' + L("おまかせで人生を歩む", "Let life unfold on its own") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div>');
  }
  // 会員コード入力バナー（note 月額）
  function memberBanner() {
    return '<div class="paywall">' +
      '<h3>' + L("🔑 会員エリア（note）", "🔑 Members area (note)") + '</h3>' +
      '<p>' + L("世界の偉人・聖典・伝説、そして多くの悩みは会員限定。<br>note会員ページの「今月のコード」を入れると解放されます。",
        "The world's sages, scriptures, legends and many worries are members-only.<br>Enter this month's code from the note members page to unlock.") + '</p>' +
      '<input class="code-input" autocapitalize="characters" placeholder="' + L("今月のコード（例: TOMO-1234）", "This month's code (e.g. TOMO-1234)") + '">' +
      '<button class="btn gold sm" data-act="redeem" style="display:inline-block">' + L("コードで解放", "Unlock with code") + '</button>' +
      '<div class="code-msg"></div>' +
      '</div>';
  }
  function showMemberGate() {
    curView = showMemberGate;
    render('<div class="fade">' + statusbar() +
      '<h2 class="event-title">' + L("ここから先は、会員エリアです", "Beyond here is the members area") + '</h2>' +
      '<p class="event-body">' + L("恋愛・学業などの悩み、世界の偉人・聖典・伝説、そして毎月の新しい言葉は会員限定。noteの会員ページの「今月のコード」で解放できます。",
        "Worries like love and study, the world's sages, scriptures and legends, and fresh words each month are members-only. Unlock with this month's code from the note members page.") + '</p>' +
      memberBanner() +
      '<button class="btn ghost" data-act="walk">' + L("無料で歩む", "Walk for free") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div>');
  }
  function showEvent(ev) {
    curView = function () { showEvent(ev); };
    var legendHtml = currentLegend ? legendCard(currentLegend) : "";
    var cards = legendHtml + ev.advices.map(function (adv) { return adviceCard(ev, adv); }).join("");
    var paywall = isPaid() ? "" : memberBanner();
    var consultBack = (mode === "consult") ? '<button class="btn ghost" data-act="consult">' + L("← 悩みを選び直す", "← Choose another worry") + '</button>' : "";
    var html = '<div class="fade">' + statusbar() +
      '<span class="eyebrow">' + catIcon(ev.category) + ' ' + esc(catLabel(ev.category)) + ' ・ ' + moodIcon(ev.mood) + ' ' + esc(moodLabel(ev.mood)) + '</span>' +
      '<h2 class="event-title">' + esc(evTitle(ev)) + '</h2>' +
      '<p class="event-body">' + esc(evBody(ev)) + '</p>' +
      '<p class="advice-help reading-hint">' + L("ひと呼吸おいて、言葉に耳を澄ませて……", "Take a breath, and listen for the words…") + '</p>' +
      paywall + cards +
      '<button class="btn ghost" data-act="book">' + L("わが叡智の書", "Book of Wisdom") + '</button>' +
      consultBack +
      '<button class="btn ghost" data-act="title">' + L("中断（タイトルへ）", "Pause (back to title)") + '</button>' +
      '</div>';
    render(html);
    gateReading(ev);
    if (API) loadEventStats(ev);
  }
  function gateReading(ev) {
    var ms = Math.max(800, Math.min(2200, 700 + ((lang === "en" ? (ev.bodyEn || ev.body) : ev.body) || "").length * 40));
    setTimeout(function () {
      var btns = app.querySelectorAll(".card.tap[disabled]");
      for (var i = 0; i < btns.length; i++) { btns[i].removeAttribute("disabled"); }
      var hint = app.querySelector(".reading-hint");
      if (hint) { hint.textContent = L("心に響いた言葉を、ひとつ選ぼう。", "Choose the one word that speaks to you."); hint.classList.add("ready"); }
    }, ms);
  }
  function adviceCard(ev, adv) {
    var sage = SAGES[adv.sageId] || { name: adv.sageId, color: "#999" };
    var st = adviceState(adv);
    var scripture = isScripture(adv.sageId);
    var color = sage.color || "#999";

    if (st === "member") {
      return '<div class="card locked" style="--c:' + color + '">' +
        '<div class="card-head"><span class="disc' + (scripture ? ' scripture' : '') + '">🔒</span>' +
        '<span class="sname">' + esc(sageName(sage)) + '</span><span class="badge">' + L("会員限定", "Members") + '</span></div>' +
        '<p class="lockmsg">' + L("この言葉は <b>会員</b> で開きます（今月のコードを入力）。", "This word opens for <b>members</b> (enter this month's code).") + '</p></div>';
    }
    if (st === "rank") {
      var need = RANKS[sage.rank].unlockWisdom, rem = Math.max(0, need - state.stats.wisdom);
      return '<div class="card locked" style="--c:' + color + '">' +
        '<div class="card-head"><span class="disc' + (scripture ? ' scripture' : '') + '">🔒</span>' +
        '<span class="sname">' + esc(sageName(sage)) + '</span>' +
        '<span class="badge' + (scripture ? ' sacred' : '') + '">' + esc(rankTitle(sage.rank)) + '</span></div>' +
        '<p class="lockmsg">' + L("叡智 <b>" + need + "</b> で出会える（あと " + rem + "）。", "Meet at Wisdom <b>" + need + "</b> (" + rem + " to go).") + '</p></div>';
    }
    var era = sage.era ? '<span class="era">' + esc(sage.era) + '</span>' : "";
    var rarity = adv.sageId === "original" ? null : rarityOf(adv.sageId, false);
    var pill = rarity ? '<span class="rar rar-' + rarity + '">' + rarityLabel(rarity) + '</span>' : '<span class="rar rar-free">' + L("無料", "Free") + '</span>';
    var note = (lang === "en" ? adv.noteEn : adv.note) ? '<p class="qnote">' + esc(lang === "en" ? adv.noteEn : adv.note) + '</p>' : "";
    var src = adv.source ? '<span class="source">— ' + esc(adv.source) + '</span>' : "";
    return '<button class="card tap" data-rarity="' + (rarity || "free") + '" style="--c:' + color + '" data-choose="' + esc(adv.sageId) + '" disabled>' +
      '<div class="card-head">' +
      '<span class="disc' + (scripture ? ' scripture' : '') + '">' + esc(discChar(sage)) + '</span>' +
      '<span class="sname">' + esc(sageName(sage)) + era + '</span>' + pill +
      '</div>' +
      '<p class="quote">' + esc(qText(adv)) + '</p>' + note + src +
      '</button>';
  }
  function legendCard(legend) {
    var sage = SAGES[legend.sageId] || { color: "#caa45d" };
    return '<button class="card tap legend" data-rarity="legendary" style="--c:' + (sage.color || "#caa45d") + '" data-legend="' + esc(legend.id) + '" disabled>' +
      '<div class="card-head"><span class="disc legenddisc">✦</span>' +
      '<span class="sname">' + L("特別な来訪", "A special visit") + '</span><span class="rar rar-legendary">' + L("✦ 伝説 ✦", "✦ Legendary ✦") + '</span></div>' +
      '<p class="quote legend-teaser">' + L("いにしえの偉人が、あなたに言葉を贈ろうとしている……<br>そっと、受け取ってみますか。",
        "An ancient sage is about to offer you words…<br>Will you quietly receive them?") + '</p>' +
      '</button>';
  }

  // ---------- 決断 ----------
  function choose(ev, sageId) {
    var adv = null; ev.advices.forEach(function (a) { if (a.sageId === sageId) adv = a; });
    if (!adv || adviceState(adv) !== "show") return;
    var sage = SAGES[sageId] || {};
    var beforeMind = state.stats.mind, beforeRank = unlockedRank();
    var deltas = [];
    Object.keys(adv.effects || {}).forEach(function (k) { var diff = applyStat(k, adv.effects[k]); if (diff !== 0) deltas.push({ k: k, d: diff }); });
    var rec = {
      ts: new Date().toISOString(), turn: state.turn + 1,
      eventId: ev.id, category: ev.category, mood: ev.mood, title: evTitle(ev),
      chosenSageId: sageId, sageName: sageName(sage) || sageId,
      quote: qText(adv), source: adv.source || "", note: (lang === "en" ? adv.noteEn : adv.note) || "",
      tradition: adv.tradition || null, isScripture: isScripture(sageId),
      mindBefore: beforeMind, mindAfter: state.stats.mind, playerNote: "", feedback: null
    };
    state.turn++; state.journal.push(rec);
    if (state.seen.indexOf(ev.id) < 0) state.seen.push(ev.id);
    currentLegend = null;
    var beforePos = positionFor(playerProgress().points);
    recordAcclaim(ev.id + ":" + sageId, ev.category);
    var positionUp = positionFor(playerProgress().points).min !== beforePos.min ? positionFor(playerProgress().points) : null;
    recomputeFavorite(); save();
    var rankedUp = unlockedRank() > beforeRank ? unlockedRank() : 0;
    showResult(state.journal.length - 1, deltas, rankedUp, positionUp);
  }

  function chooseLegend(id) {
    var legend = null; LEGENDS.forEach(function (l) { if (l.id === id) legend = l; });
    if (!legend || codexHas(id)) return;
    var sage = SAGES[legend.sageId] || {};
    var beforeRank = unlockedRank();
    var deltas = [];
    Object.keys(legend.effects || {}).forEach(function (k) { var diff = applyStat(k, legend.effects[k]); if (diff !== 0) deltas.push({ k: k, d: diff }); });
    var ev = currentEvent || {};
    var rec = {
      ts: new Date().toISOString(), turn: state.turn + 1,
      eventId: ev.id || "", category: ev.category || "self", mood: ev.mood || "", title: ev.id ? evTitle(ev) : L("伝説との邂逅", "A legendary encounter"),
      chosenSageId: legend.sageId, sageName: sageName(sage) || legend.sageId,
      quote: qText(legend), source: legend.source || "", note: (lang === "en" ? legend.noteEn : legend.note) || "",
      tradition: legend.tradition || null, isScripture: isScripture(legend.sageId),
      isLegend: true, legendId: legend.id, rarity: "legendary",
      mindBefore: state.stats.mind, mindAfter: state.stats.mind, playerNote: "", feedback: null
    };
    var beforePos = positionFor(playerProgress().points);
    state.turn++; state.journal.push(rec); codexAdd(legend.id);
    recordAcclaim("legend:" + legend.id, ev.category || "self");
    var positionUp = positionFor(playerProgress().points).min !== beforePos.min ? positionFor(playerProgress().points) : null;
    if (ev.id && state.seen.indexOf(ev.id) < 0) state.seen.push(ev.id);
    currentLegend = null; recomputeFavorite(); save();
    var rankedUp = unlockedRank() > beforeRank ? unlockedRank() : 0;
    var idx = state.journal.length - 1;
    celebrate(legend, function () { showResult(idx, deltas, rankedUp, positionUp); });
  }

  function celebrate(legend, done) {
    var sage = SAGES[legend.sageId] || {};
    var found = codex.length, total = LEGENDS.length;
    var ov = document.createElement("div");
    ov.className = "celebrate";
    var sparks = "";
    for (var i = 0; i < 20; i++) { sparks += '<i style="--i:' + i + '"></i>'; }
    ov.innerHTML =
      '<div class="cel-flash"></div>' +
      '<div class="cel-rays"></div>' +
      '<div class="cel-particles">' + sparks + '</div>' +
      '<div class="cel-inner">' +
      '<div class="cel-label">' + L("✦ 伝説の言葉に出会った ✦", "✦ You have met a Legendary Word ✦") + '</div>' +
      '<div class="cel-quote">' + esc(qText(legend)) + '</div>' +
      '<div class="cel-from">— ' + esc(sageName(sage) || legend.sageId) + (isScripture(legend.sageId) ? scriptureTag() : "") + '</div>' +
      (legend.source ? '<div class="cel-source">' + esc(legend.source) + '</div>' : "") +
      '<div class="cel-count">' + L("伝説 " + found + " / " + total + " 蒐集", "Legendary " + found + " / " + total + " collected") + '</div>' +
      '<button class="btn gold cel-btn">' + L("この叡智を受け取る", "Receive this wisdom") + '</button>' +
      '</div>';
    document.body.appendChild(ov);
    sfxSacred();
    requestAnimationFrame(function () { ov.classList.add("show"); });
    ov.querySelector(".cel-btn").addEventListener("click", function () {
      ov.classList.add("out");
      setTimeout(function () { ov.remove(); done(); }, 280);
    });
  }

  // ① 名言を画像化してシェア/保存（Canvas・外部依存なし）
  var lastRec = null;
  function wrapCanvas(ctx, text, maxW) {
    var lines = [], cur = "";
    if (/\s/.test(text)) {
      var ws = text.split(/\s+/);
      for (var w = 0; w < ws.length; w++) { var test = cur ? cur + " " + ws[w] : ws[w]; if (ctx.measureText(test).width > maxW && cur) { lines.push(cur); cur = ws[w]; } else cur = test; }
    } else {
      for (var i = 0; i < text.length; i++) { var t = cur + text[i]; if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = text[i]; } else cur = t; }
    }
    if (cur) lines.push(cur);
    return lines;
  }
  function drawShare(rec) {
    var W = 1080, H = 1350, c = document.createElement("canvas"); c.width = W; c.height = H;
    var x = c.getContext && c.getContext("2d"); if (!x) return;
    var dark = night;
    var g = x.createLinearGradient(0, 0, 0, H);
    if (dark) { g.addColorStop(0, "#2c2820"); g.addColorStop(1, "#1c1915"); } else { g.addColorStop(0, "#fbf6ec"); g.addColorStop(1, "#efe5d3"); }
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    var ink = dark ? "#ece3d2" : "#33291f", soft = dark ? "#b3a589" : "#6b5d4a", gold = "#caa45d", goldd = dark ? "#d8b772" : "#a9863f";
    x.strokeStyle = gold; x.lineWidth = 6; x.strokeRect(40, 40, W - 80, H - 80);
    x.strokeStyle = "rgba(202,164,93,.45)"; x.lineWidth = 2; x.strokeRect(58, 58, W - 116, H - 116);
    x.textAlign = "center"; x.textBaseline = "middle";
    var q = rec.quote, big = q.length > 64 ? 44 : (q.length > 32 ? 56 : 64), lh = Math.round(big * 1.5);
    x.font = "600 " + big + "px 'Noto Serif JP', serif"; x.fillStyle = ink;
    var lines = wrapCanvas(x, q, W - 220);
    var startY = H / 2 - (lines.length - 1) * lh / 2 - 60;
    lines.forEach(function (ln, i) { x.fillText(ln, W / 2, startY + i * lh); });
    var y = startY + lines.length * lh + 24;
    x.font = "500 40px 'Noto Serif JP', serif"; x.fillStyle = soft;
    x.fillText("— " + rec.sageName + (rec.isScripture ? "（聖典）" : ""), W / 2, y); y += 58;
    if (rec.source) { x.font = "400 28px 'Noto Serif JP', serif"; x.fillStyle = goldd; wrapCanvas(x, rec.source, W - 240).forEach(function (s) { x.fillText(s, W / 2, y); y += 38; }); }
    x.font = "500 36px 'Noto Serif JP', serif"; x.fillStyle = goldd; x.fillText("🪔 " + L("叡智の灯火", "Beacon of Wisdom"), W / 2, H - 116);
    x.font = "400 24px sans-serif"; x.fillStyle = soft; x.fillText("dashiyo777-oss.github.io/my-portofolio/life-wisdom-game/", W / 2, H - 74);
    var name = (lang === "en" ? "beacon-of-wisdom.png" : "叡智の灯火.png");
    function deliver(blob) {
      try { var f = new File([blob], name, { type: "image/png" }); if (navigator.canShare && navigator.canShare({ files: [f] })) { navigator.share({ files: [f], text: rec.quote + " — " + rec.sageName + "  #" + L("叡智の灯火", "BeaconOfWisdom") }).catch(function () {}); return; } } catch (e) {}
      var a = document.createElement("a"); a.download = name; a.href = URL.createObjectURL(blob); document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
    }
    if (c.toBlob) c.toBlob(deliver, "image/png"); else { var a = document.createElement("a"); a.download = name; a.href = c.toDataURL("image/png"); a.click(); }
  }
  function shareCard(rec) { if (!rec) return; if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { drawShare(rec); }); else drawShare(rec); }

  function showResult(idx, deltas, rankedUp, positionUp) {
    curView = function () { showResult(idx, deltas, rankedUp, positionUp); };
    var rec = state.journal[idx]; lastRec = rec;
    if (rec.isLegend) { /* 祝福演出で鳴らし済み */ } else if (rec.isScripture) { sfxSacred(); } else { sfxChime(); }
    var dhtml = deltas.map(function (x) {
      var up = x.d > 0; return '<span class="delta ' + (up ? "up" : "down") + '">' + esc(statLabel(x.k)) + " " + (up ? "+" : "") + x.d + '</span>';
    }).join("");
    var rankBanner = rankedUp ? '<p class="saved-toast">' + L("✨ 新たな境地「" + esc(rankTitle(rankedUp)) + "」に到達した", "✨ You reached a new stage: “" + esc(rankTitle(rankedUp)) + "”") + '</p>' : "";
    var masterBanner = (rankedUp === MAX_RANK) ? (function () { try { sfxSacred(); } catch (e) {} return '<button class="master-toast" data-act="hiden">' + L("📜 「叡智皆伝」に到達！秘伝の書がひらかれた ―― ひらく →", "📜 You reached Wisdom Mastery! Your secret book is revealed — open it →") + '</button>'; })() : "";
    var posBanner = positionUp ? '<p class="pos-banner">' + L("🎖 昇位 ―「" + esc(posTitle(positionUp)) + "（" + esc(posGrade(positionUp)) + "）」へ", "🎖 Promotion — to “" + esc(posTitle(positionUp)) + "” (" + esc(posGrade(positionUp)) + ")") + '</p>' : "";
    var ribbon = rec.isLegend ? '<p class="rarity-ribbon legendary">' + L("✦ 伝説の言葉 ✦", "✦ A Legendary Word ✦") + '</p>'
      : (rec.isScripture ? '<p class="rarity-ribbon sacred">' + L("神聖なる導き", "Sacred Guidance") + '</p>' : "");
    var html = '<div class="fade">' + ribbon +
      '<div class="scroll-card' + (rec.isLegend ? ' legendary' : (rec.isScripture ? ' sacred' : '')) + '">' +
      '<p class="result-quote">' + esc(rec.quote) + '</p>' +
      '<p class="result-from">— ' + esc(rec.sageName) + (rec.isScripture ? L("（聖典の言葉）", " (words of scripture)") : "") + '</p>' +
      (rec.source ? '<p class="result-source">' + esc(rec.source) + '</p>' : "") +
      '</div>' +
      (dhtml ? '<div class="deltas">' + dhtml + '</div>' : "") +
      rankBanner + masterBanner + posBanner +
      '<p class="saved-toast">' + L("📖 「わが叡智の書」に刻まれた", "📖 Inscribed in your Book of Wisdom") + '</p>' +
      '<p class="social-proof"></p>' +
      '<div class="fb" data-fbidx="' + idx + '">' +
      '<button data-fb="resonated">' + L("響いた ♡", "This resonated ♡") + '</button>' +
      '<button data-fb="not_now">' + L("今はそうでもない", "Not quite now") + '</button>' +
      '</div>' +
      '<div class="reflect" data-ridx="' + idx + '">' +
      '<button class="reflect-toggle" data-act="reflect-open">' + L("✎ この言葉を、暮らしにどう活かす？", "✎ How will you bring this into your life?") + '</button>' +
      '<div class="reflect-body" hidden>' +
      '<textarea class="reflect-input" rows="2" placeholder="' + L("今日からできる小さな一歩を、ひとこと…", "One small step you can take today…") + '"></textarea>' +
      '<button class="btn ghost sm" data-act="reflect-save">' + L("暮らしに活かすと、心に留める", "Keep it, and live it") + '</button>' +
      '</div></div>' +
      '<button class="btn gold" data-act="next">' + L("人生をつづける", "Continue your life") + '</button>' +
      '<button class="btn ghost" data-act="share">' + L("📤 この言葉を画像で残す", "📤 Save this word as an image") + '</button>' +
      '<button class="btn ghost" data-act="book">' + L("わが叡智の書を見る", "Open the Book of Wisdom") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("中断（タイトルへ）", "Pause (back to title)") + '</button>' +
      '</div>';
    render(html);
    if (API && rec.eventId && rec.chosenSageId) loadStats(rec.eventId + ":" + rec.chosenSageId);
  }
  function setFeedback(idx, val) {
    var rec = state.journal[idx];
    if (!rec) return;
    rec.feedback = (rec.feedback === val) ? null : val;
    save();
    var box = app.querySelector(".fb");
    if (box) box.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-fb") === rec.feedback); });
    if (API && rec.feedback) postFeedback(rec, rec.feedback);   // 響き度をサーバーへ集約（P2）
  }
  // 響き度を匿名でサーバーへ（fire-and-forget）
  function postFeedback(rec, val) {
    if (!API || !rec) return;
    try {
      fetch(API + "/api/feedback", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ eventId: rec.eventId, sageId: rec.chosenSageId, mood: rec.mood, fb: val }) }).catch(function () {});
    } catch (e) {}
  }
  // P3: 日替わりの「今日の一言」をサーバーから（API時のみ・失敗時は無表示）
  function loadDaily() {
    if (!API) return;
    fetch(API + "/api/daily?lang=" + lang).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.quote) return;
      var box = app.querySelector(".recall"); if (!box) return;
      box.innerHTML = '<span class="recall-k">' + L("🕯 今日、心に留めたい言葉", "🕯 A word to keep in your heart today") + '</span>' +
        '<p class="recall-q">' + esc(d.quote) + '</p><span class="recall-f">— ' + esc(d.sageName) + '</span>';
    }).catch(function () {});
  }
  // P3: 響き度で「多くの人に響いた」助言にバッジ（推薦の軽いヒント）
  function loadEventStats(ev) {
    if (!API) return;
    fetch(API + "/api/stats?event=" + encodeURIComponent(ev.id)).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.sages) return;
      var best = null, br = 0;
      Object.keys(d.sages).forEach(function (sid) { var s = d.sages[sid]; if (s.samples >= 5 && s.resonateRate > br) { br = s.resonateRate; best = sid; } });
      if (!best) return;
      var card = app.querySelector('.card.tap[data-choose="' + best + '"]'); if (!card) return;
      var head = card.querySelector(".card-head"); if (!head) return;
      var b = document.createElement("span"); b.className = "loved"; b.textContent = L("💛 多くの人に響いた", "💛 Resonated with many");
      head.appendChild(b);
    }).catch(function () {});
  }
  // 「○%が響いた」社会的証明（サンプルが十分なときだけ表示）
  function loadStats(key) {
    if (!API) return;
    fetch(API + "/api/stats?key=" + encodeURIComponent(key))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || !d.samples || d.samples < 5) return;
        var el = app.querySelector(".social-proof"); if (!el) return;
        var pct = Math.round(d.resonateRate * 100);
        el.textContent = L("この言葉を受けた人の " + pct + "% が「響いた」（" + d.samples + "人）",
          pct + "% of those who received this felt it resonated (" + d.samples + ")");
      }).catch(function () {});
  }

  // ---------- 休息 ----------
  function showRest() {
    curView = showRest;
    var lines = lang === "en"
      ? ["The courage to pause is also strength.", "You've done well today.", "Breathe in, breathe out. That alone is enough."]
      : ["立ち止まる勇気もまた、強さ。", "今日はもう、よく頑張った。", "息を吸って、吐いて。それだけで充分。"];
    var line = lines[Math.floor(Math.random() * lines.length)];
    state.stats.mind = clamp(state.stats.mind + 22); save();
    sfxRest();
    render('<div class="fade rest">' +
      '<div class="breath"><span class="moon">🌙</span></div>' +
      '<p class="breath-cue">' + L("ゆっくり、深呼吸……", "Breathe slowly, deeply…") + '</p>' +
      '<p class="line">' + esc(line) + '</p>' +
      '<p class="muted small">' + L("心が少し、回復した（心 +22）", "Your heart recovered a little (Mind +22)") + '</p>' +
      '<button class="btn gold" data-act="next">' + L("また歩き出す", "Walk on again") + '</button>' +
      '</div>');
  }

  // ---------- わが叡智の書 ----------
  var bookTab = "timeline", bookFilter = "all";
  function showBook() {
    var j = state.journal;
    if (j.length === 0 && codex.length === 0) {
      render('<div class="fade">' + bookHeader() +
        '<div class="empty">' + L("まだ何も記されていません。<br>人生を歩み、言葉を受け取りましょう。", "Nothing is written yet.<br>Walk your life and receive words.") + '</div>' +
        '<button class="btn gold" data-act="start">' + L("人生をはじめる", "Begin your life") + '</button>' +
        '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button></div>');
      return;
    }
    var fav = state.favoriteSage ? SAGES[state.favoriteSage] : null;
    var resonated = j.filter(function (x) { return x.feedback === "resonated"; }).length;
    var summary = '<div class="summary">' +
      L("あなたは <b>" + j.length + "</b> の岐路を歩み、<b>" + resonated + "</b> の言葉に「響いた」と頷いた。",
        "You have walked <b>" + j.length + "</b> crossroads and nodded “this resonated” to <b>" + resonated + "</b> words.") +
      (fav ? L("<br>最も多く言葉を選んだのは <b>" + esc(sageName(fav)) + "</b>。あなたの座右の賢者。",
        "<br>The sage you chose most is <b>" + esc(sageName(fav)) + "</b> — your guiding sage.") : "") + '</div>';

    var list, filters = "";
    if (bookTab === "codex") {
      list = codexHTML();
    } else if (bookTab === "timeline") {
      list = j.slice().reverse().map(entryHTML).join("") || '<div class="empty">' + L("まだ歩みはありません。", "No journey yet.") + '</div>';
    } else {
      var items = j.filter(function (x) { return bookFilter === "all" || x.category === bookFilter; });
      list = items.slice().reverse().map(entryHTML).join("") || '<div class="empty">' + L("この分類の記録はまだありません。", "No records in this category yet.") + '</div>';
      var cats = ["all"].concat(CAT_KEYS);
      filters = '<div class="filters">' + cats.map(function (c) {
        return '<button class="chip' + (bookFilter === c ? " on" : "") + '" data-filter="' + c + '">' + (c === "all" ? L("すべて", "All") : catIcon(c) + " " + esc(catLabel(c))) + '</button>';
      }).join("") + '</div>';
    }
    render('<div class="fade">' + bookHeader() +
      '<div class="tabs">' +
      '<button class="' + (bookTab === "timeline" ? "on" : "") + '" data-tab="timeline">' + L("歩み", "Journey") + '</button>' +
      '<button class="' + (bookTab === "collection" ? "on" : "") + '" data-tab="collection">' + L("お守り", "Charms") + '</button>' +
      '<button class="' + (bookTab === "codex" ? "on" : "") + '" data-tab="codex">' + L("伝説 ", "Legends ") + codex.length + '/' + LEGENDS.length + '</button>' +
      '</div>' + summary + filters + list +
      '<div class="footer-actions">' +
      '<button class="btn gold" data-act="start">' + L("人生をつづける", "Continue your life") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div></div>');
  }
  function bookHeader() {
    return '<div class="book-head"><span class="flame" style="font-size:24px">📖</span><h2>' + L("わが叡智の書", "Book of Wisdom") + '</h2></div>';
  }
  function codexHTML() {
    var head = '<div class="codex-head">' + L("✦ 伝説の言葉 <b>" + codex.length + "</b> / " + LEGENDS.length + " 蒐集 ✦", "✦ Legendary Words <b>" + codex.length + "</b> / " + LEGENDS.length + " collected ✦") + '<br>' +
      '<span class="small muted">' + L("めったに現れぬ言葉。叡智を深めるほど、出会いは近づく。", "Words that rarely appear. The deeper your wisdom, the closer the encounter.") + '</span></div>';
    var grid = LEGENDS.map(function (l) {
      var sage = SAGES[l.sageId] || {};
      if (codexHas(l.id)) {
        return '<div class="legend-slot found" style="--c:' + (sage.color || "#caa45d") + '">' +
          '<div class="ls-head">✦ ' + esc(sageName(sage) || l.sageId) + (isScripture(l.sageId) ? scriptureTag() : "") + '</div>' +
          '<div class="ls-quote">' + esc(qText(l)) + '</div>' +
          '<div class="ls-src">' + esc(l.source || "") + '</div></div>';
      }
      return '<div class="legend-slot locked">' +
        '<div class="ls-head">？ ？ ？</div>' +
        '<div class="ls-quote">' + L("未だ見ぬ言葉 — 叡智 " + (l.minWisdom || 0) + " 以上で出会える", "A word yet unseen — meet it at Wisdom " + (l.minWisdom || 0) + "+") + '</div></div>';
    }).join("");
    return head + '<div class="codex-grid">' + grid + '</div>';
  }
  function entryHTML(rec) {
    var sage = SAGES[rec.chosenSageId] || { color: "#bbb" };
    var d = new Date(rec.ts);
    var when = isNaN(d) ? "" : (d.getMonth() + 1) + "/" + d.getDate() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
    var fb = rec.feedback === "resonated" ? L("♡ 響いた", "♡ resonated") : (rec.feedback === "not_now" ? L("今はそうでもない", "not quite now") : "");
    var ep = L("第" + rec.turn + "話", "Ch. " + rec.turn);
    return '<div class="entry" style="--c:' + (sage.color || "#bbb") + '">' +
      '<div class="when">' + ep + ' ・ ' + esc(when) + ' ・ ' + catIcon(rec.category) + ' ' + esc(catLabel(rec.category)) + '</div>' +
      '<div class="etitle">' + esc(rec.title) + '</div>' +
      '<div class="eauthor" style="display:flex;align-items:center;gap:6px;margin:2px 0 6px;font-weight:700;color:var(--c)">' +
        '<span class="edisc" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:var(--c);color:#fff;font-size:12px">' + esc(discChar(sage)) + '</span>' +
        esc(rec.sageName) + (rec.isScripture ? scriptureTag() : "") + '</div>' +
      '<div class="eq">' + esc(rec.quote) + '</div>' +
      '<div class="efrom">— ' + esc(rec.sageName) + (rec.isScripture ? scriptureTag() : "") + (rec.source ? " ／ " + esc(rec.source) : "") + '</div>' +
      (rec.playerNote ? '<div class="enote">✎ ' + esc(rec.playerNote) + '</div>' : "") +
      (fb ? '<div class="fbmark">' + esc(fb) + '</div>' : "") +
      '</div>';
  }

  // ---------- 叡智の免許状 ----------
  function showCert() {
    var pg = playerProgress(); var pos = positionFor(pg.points); var nx = nextPosition(pg.points);
    var d = new Date();
    var ymd = lang === "en"
      ? ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear()
      : d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日";
    var prog;
    if (nx) {
      var span = nx.min - pos.min, p = Math.max(0, Math.min(1, (pg.points - pos.min) / span)), rem = nx.min - pg.points;
      prog = '<div class="cert-next">' + L("次の位「" + esc(posTitle(nx)) + "（" + esc(posGrade(nx)) + "）」まで あと " + rem + " 点",
        "Next rank “" + esc(posTitle(nx)) + "” (" + esc(posGrade(nx)) + ") — " + rem + " points to go") +
        '<div class="wbar"><i style="width:' + (p * 100).toFixed(0) + '%"></i></div></div>';
    } else {
      prog = '<div class="cert-next">' + L("最高位「叡智皆伝」に到達。あなたは生涯の探究者。", "You have reached the highest rank, Wisdom Mastery. A lifelong seeker.") + '</div>';
    }
    var html = '<div class="fade">' +
      '<div class="certificate">' +
      '<div class="cert-corner tl"></div><div class="cert-corner tr"></div><div class="cert-corner bl"></div><div class="cert-corner br"></div>' +
      '<div class="cert-kicker">' + L("叡 智 之 證", "Certificate of Wisdom") + '</div>' +
      '<div class="cert-sub">' + L("人生相談 叡智検定", "Wisdom Examination · Life Counsel") + '</div>' +
      '<div class="cert-pos">' + esc(posTitle(pos)) + '</div>' +
      '<div class="cert-grade">' + esc(posGrade(pos)) + '</div>' +
      '<div class="cert-stats">' +
      '<div><b>' + pg.points + '</b><span>' + L("叡智ポイント", "Wisdom Points") + '</span></div>' +
      '<div><b>' + pg.quotes + '</b><span>' + L("到達した言葉", "Words Reached") + '</span></div>' +
      '<div><b>' + pg.legends + ' / ' + LEGENDS.length + '</b><span>' + L("伝説", "Legends") + '</span></div>' +
      '<div><b>' + pg.cats + ' / 7</b><span>' + L("制覇した悩み", "Worries Mastered") + '</span></div>' +
      '</div>' +
      '<div class="cert-foot"><span class="cert-date">' + L(esc(ymd) + " 発行", "Issued " + esc(ymd)) + '</span><span class="cert-seal">灯</span></div>' +
      '</div>' +
      prog +
      '<p class="notice">' + L("※ 位は「到達した言葉・伝説・制覇カテゴリ」の生涯記録で決まり、人生をやり直しても下がりません。",
        "※ Your rank is based on lifetime records of words reached, legends, and worries — it never drops, even if you start a new life.") + '</p>' +
      '<button class="btn gold" data-act="start">' + L("人生をつづける", "Continue your life") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div>';
    render(html);
  }

  // ---------- 叡智皆伝の書（秘伝の書） ----------
  function isMaster() { return unlockedRank() >= MAX_RANK; }
  function isGrandMaster() { return isMaster() && codex.length >= LEGENDS.length; }
  function masterTitle() { return isGrandMaster() ? L("真・叡智皆伝", "True Mastery of Wisdom") : L("叡智皆伝", "Mastery of Wisdom"); }
  function resonatedList() {
    var r = state.journal.filter(function (j) { return j.feedback === "resonated" && j.quote; });
    if (r.length === 0) r = state.journal.filter(function (j) { return j.quote; });
    return r;
  }
  function hidenClosing() {
    if (isGrandMaster()) return L(
      "全ての伝説を集め、皆伝の頂に至った者へ。<br>知恵とは、覚えた言葉の数ではない。<br>それを暮らしに変えた、その手のぬくもりだ。<br>あなたが選んだ言葉のひとつひとつが、もう、あなたの一部になっている。<br>灯火は、役目を終える。<br>あとは——あなたが、照らす番だ。",
      "To the one who gathered every legend and reached the summit:<br>Wisdom is not the number of words you have learned,<br>but the warmth of the hands that turned them into a life.<br>Every word you chose has already become part of you.<br>The beacon's work is done.<br>Now — you are the light.");
    return L(
      "ここまで、よく歩いてきた。<br>あなたはもう、答えを外にばかり探す者ではない。<br>迷いの日に灯した小さな火は、いつしかあなた自身の光になった。<br>これからは、あなたが誰かの灯火となる番だ。<br>——その火を、絶やさぬように。",
      "You have walked far.<br>You no longer seek your answers only outside yourself.<br>The small flame you lit in your darkest days has become your own light.<br>Now it is your turn to be a beacon for others.<br>— Keep the fire burning.");
  }
  function showHiden() {
    curView = showHiden;
    if (!isMaster()) { showTitle(); return; }
    sfxSacred();
    var gm = isGrandMaster();
    var d = new Date();
    var ymd = lang === "en"
      ? ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear()
      : d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日";
    var res = resonatedList();
    var anth = res.slice(0, 14).map(function (r) {
      return '<div class="hiden-q">「' + esc(r.quote) + '」<span class="hiden-from">— ' + esc(r.sageName) + '</span></div>';
    }).join("") || '<p class="muted">' + L("まだ言葉が記されていません。", "No words are recorded yet.") + '</p>';
    var fav = state.favoriteSage && SAGES[state.favoriteSage] ? sageName(SAGES[state.favoriteSage]) : "—";
    var resonatedCount = state.journal.filter(function (j) { return j.feedback === "resonated"; }).length;
    var html = '<div class="fade hiden">' +
      '<div class="hiden-scroll' + (gm ? ' gm' : '') + '">' +
      '<div class="hiden-seal">' + (gm ? "皆" : "灯") + '</div>' +
      '<div class="hiden-kicker">' + L("秘 伝 之 書", "The Book of Secret Wisdom") + '</div>' +
      '<h2 class="hiden-name">' + esc(masterTitle()) + '</h2>' +
      '<p class="hiden-date">' + L(esc(ymd) + " 到達", "Attained " + esc(ymd)) + '</p>' +
      '<div class="hiden-stats">' +
      '<div><b>' + state.journal.length + '</b><span>' + L("歩んだ岐路", "Crossroads") + '</span></div>' +
      '<div><b>' + resonatedCount + '</b><span>' + L("響いた言葉", "Resonated") + '</span></div>' +
      '<div><b>' + codex.length + ' / ' + LEGENDS.length + '</b><span>' + L("伝説", "Legends") + '</span></div>' +
      '<div><b>' + esc(fav) + '</b><span>' + L("座右の賢者", "Guiding Sage") + '</span></div>' +
      '</div>' +
      '<div class="hiden-sec">' + L("◇ あなたの秘伝 ◇", "◇ Your Own Wisdom ◇") + '</div>' +
      '<p class="hiden-lead">' + L("旅の中で「響いた」と選んだ言葉。これは、あなただけの叡智の書。", "The words that resonated with you — a book of wisdom that is yours alone.") + '</p>' +
      '<div class="hiden-anth">' + anth + '</div>' +
      '<div class="hiden-sec">' + L("◇ 灯火からの、最後の言葉 ◇", "◇ The Beacon's Final Words ◇") + '</div>' +
      '<p class="hiden-closing">' + hidenClosing() + '</p>' +
      '</div>' +
      '<button class="btn gold" data-act="hidenshare">' + L("📜 皆伝の書を画像で残す・共有", "📜 Save & share your scroll") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div>';
    render(html);
  }
  function drawHiden() {
    var W = 1080, H = 1350, c = document.createElement("canvas"); c.width = W; c.height = H;
    var x = c.getContext && c.getContext("2d"); if (!x) return;
    var g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#2a2016"); g.addColorStop(1, "#161210");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    var ink = "#f0e6d2", gold = "#d8b772", soft = "#b3a589";
    x.strokeStyle = gold; x.lineWidth = 6; x.strokeRect(40, 40, W - 80, H - 80);
    x.strokeStyle = "rgba(216,183,114,.4)"; x.lineWidth = 2; x.strokeRect(58, 58, W - 116, H - 116);
    x.textAlign = "center"; x.textBaseline = "middle";
    x.beginPath(); x.arc(W / 2, 230, 72, 0, Math.PI * 2); x.fillStyle = gold; x.fill();
    x.fillStyle = "#171210"; x.font = "700 70px 'Noto Serif JP', serif"; x.fillText(isGrandMaster() ? "皆" : "灯", W / 2, 238);
    x.fillStyle = gold; x.font = "600 38px 'Noto Serif JP', serif"; x.fillText(L("秘 伝 之 書", "Book of Secret Wisdom"), W / 2, 360);
    x.fillStyle = ink; x.font = "700 96px 'Noto Serif JP', serif"; x.fillText(masterTitle(), W / 2, 460);
    var d = new Date(), ymd = lang === "en"
      ? ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear()
      : d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日";
    x.fillStyle = soft; x.font = "400 34px 'Noto Serif JP', serif"; x.fillText(L(ymd + " 到達", "Attained " + ymd), W / 2, 540);
    var rc = state.journal.filter(function (j) { return j.feedback === "resonated"; }).length;
    x.fillStyle = goldStr(); function goldStr() { return "#d8b772"; }
    x.font = "500 36px 'Noto Serif JP', serif";
    x.fillText(L("歩んだ岐路 " + state.journal.length + "　響いた言葉 " + rc + "　伝説 " + codex.length + "/" + LEGENDS.length,
      "Crossroads " + state.journal.length + " · Resonated " + rc + " · Legends " + codex.length + "/" + LEGENDS.length), W / 2, 620);
    var res = resonatedList().slice(0, 2), y = 760;
    x.fillStyle = "rgba(216,183,114,.5)"; x.font = "400 30px 'Noto Serif JP', serif"; x.fillText(L("◇ あなたの秘伝 ◇", "◇ Your Own Wisdom ◇"), W / 2, y); y += 70;
    res.forEach(function (r) {
      x.fillStyle = ink; x.font = "500 40px 'Noto Serif JP', serif";
      wrapCanvas(x, "「" + r.quote + "」", W - 200).forEach(function (ln) { x.fillText(ln, W / 2, y); y += 56; });
      x.fillStyle = soft; x.font = "400 28px 'Noto Serif JP', serif"; x.fillText("— " + r.sageName, W / 2, y); y += 64;
    });
    x.fillStyle = gold; x.font = "500 36px 'Noto Serif JP', serif"; x.fillText("🪔 " + L("叡智の灯火", "Beacon of Wisdom"), W / 2, H - 120);
    x.fillStyle = soft; x.font = "400 26px sans-serif"; x.fillText("eichinohi.com", W / 2, H - 76);
    var name = (lang === "en" ? "mastery-of-wisdom.png" : "叡智皆伝の書.png");
    function deliver(blob) {
      try { var f = new File([blob], name, { type: "image/png" }); if (navigator.canShare && navigator.canShare({ files: [f] })) { navigator.share({ files: [f], text: masterTitle() + " — " + L("叡智の灯火", "Beacon of Wisdom") + "  #" + L("叡智の灯火", "BeaconOfWisdom") + "  eichinohi.com" }).catch(function () {}); return; } } catch (e) {}
      var a = document.createElement("a"); a.download = name; a.href = URL.createObjectURL(blob); document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
    }
    if (c.toBlob) c.toBlob(deliver, "image/png"); else { var a = document.createElement("a"); a.download = name; a.href = c.toDataURL("image/png"); a.click(); }
  }
  function shareHiden() { if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawHiden); else drawHiden(); }

  // ---------- レンダリング & イベント委譲 ----------
  function render(html) { app.innerHTML = html; window.scrollTo(0, 0); }

  app.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act],[data-choose],[data-legend],[data-consultcat],[data-fb],[data-tab],[data-filter]");
    if (!t) return;
    if (ambientOn && (!bgm || bgm.paused)) startAmbient();   // 初回タップでBGMを再開（自動再生制限対策）
    if (t.hasAttribute("data-legend")) { chooseLegend(t.getAttribute("data-legend")); return; }
    if (t.hasAttribute("data-choose")) { choose(currentEvent, t.getAttribute("data-choose")); return; }
    if (t.hasAttribute("data-fb")) { var box = t.closest(".fb"); setFeedback(+box.getAttribute("data-fbidx"), t.getAttribute("data-fb")); return; }
    if (t.hasAttribute("data-tab")) { bookTab = t.getAttribute("data-tab"); showBook(); return; }
    if (t.hasAttribute("data-filter")) { bookFilter = t.getAttribute("data-filter"); showBook(); return; }
    if (t.hasAttribute("data-consultcat")) { mode = "consult"; consultCat = t.getAttribute("data-consultcat"); proceed(); return; }
    var act = t.getAttribute("data-act");
    if (act === "sound") { toggleSound(); (curView || showTitle)(); }
    else if (act === "ambient") { toggleAmbient(); (curView || showTitle)(); }
    else if (act === "share") { shareCard(lastRec); }
    else if (act === "night") { toggleNight(); (curView || showTitle)(); }
    else if (act === "lang") { setLang(t.getAttribute("data-lang")); (curView || showTitle)(); }
    else if (act === "walk") { mode = "auto"; consultCat = null; proceed(); }
    else if (act === "consult") showConsult();
    else if (act === "start" || act === "next") proceed();
    else if (act === "book") showBook();
    else if (act === "cert") showCert();
    else if (act === "hiden") showHiden();
    else if (act === "hidenshare") shareHiden();
    else if (act === "title") showTitle();
    else if (act === "membergate") { showMemberGate(); }
    else if (act === "redeem") {
      var cinp = app.querySelector(".code-input");
      var code = cinp ? (cinp.value || "").trim().toUpperCase() : "";
      var fail = function () { var m = app.querySelector(".code-msg"); if (m) m.textContent = L("コードが違います。note会員ページをご確認ください。", "Incorrect code. Please check the note members page."); };
      if (API) {
        var m0 = app.querySelector(".code-msg"); if (m0) m0.textContent = L("確認中…", "Verifying…");
        fetch(API + "/api/redeem", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ code: code }) })
          .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
          .then(function (d) { state.paidMonth = monthKey(new Date()); state.token = d.token; save(); return fetchPaid(); })
          .then(function () { if (currentEvent) showEvent(currentEvent); else showTitle(); })
          .catch(fail);
      } else if (code === expectedCode(new Date()).toUpperCase()) {
        state.paidMonth = monthKey(new Date()); save();
        if (currentEvent) showEvent(currentEvent); else showTitle();
      } else fail();
    }
    else if (act === "reflect-open") { var rb = app.querySelector(".reflect-body"); if (rb) rb.hidden = false; if (t.style) t.style.display = "none"; }
    else if (act === "reflect-save") {
      var rbox = t.closest ? t.closest(".reflect") : null;
      var ridx = (rbox && rbox.getAttribute) ? +rbox.getAttribute("data-ridx") : -1;
      var rinp = app.querySelector(".reflect-input");
      if (state.journal[ridx]) { state.journal[ridx].playerNote = rinp ? rinp.value : ""; save(); }
      if (rbox) rbox.innerHTML = '<p class="reflect-done">' + L("✓ 暮らしに活かす一歩を、心に留めた", "✓ You kept a step to live by") + '</p>';
    }
    else if (act === "reset") { if (confirm(L("これまでの歩みと叡智の書が消えます。よろしいですか？", "Your journey and Book of Wisdom will be erased. Are you sure?"))) resetGame(); }
  });

  applyNight();
  showTitle();
  if (API && state.token && isPaid()) fetchPaid().then(function () { showTitle(); }).catch(function () {});
})();
