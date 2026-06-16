/* 叡智の灯火 / Beacon of Wisdom — MVP（ビルド不要 / localStorage 永続 / 日英対応）
   設計: ../SPEC.md  データ: data/*.json (→ gamedata.js)
   i18n: L(ja,en) で文言を切替。本文/名言は data の *En フィールド or nameEn/quoteOriginal にフォールバック。 */
(function () {
  "use strict";
  var D = window.GAME_DATA;
  if (!D) { document.getElementById("app").innerHTML = "<p style='padding:24px'>データを読み込めませんでした。<br>data/gamedata.js を確認してください（build-data.py で生成）。</p>"; return; }

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
  var RANK_TITLE_EN = { 1: "Apprentice Sage", 2: "Sage", 3: "Great Sage", 4: "Legendary Sage", 5: "Sacred Guidance" };
  function rankTitle(r) { return lang === "en" ? (RANK_TITLE_EN[r] || RANKS[r].title) : RANKS[r].title; }

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
    return { v: 1, stats: { mind: 60, wisdom: 0, bonds: 50, wealth: 50, passion: 50 }, turn: 0, journal: [], seen: [], premiumUnlocked: false, favoriteSage: null };
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
    if (!state.premiumUnlocked) return null;
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

  function unlockedRank() { var r = 1; [1, 2, 3, 4, 5].forEach(function (k) { if (state.stats.wisdom >= RANKS[k].unlockWisdom) r = k; }); return r; }
  function nextRankInfo() {
    var cur = unlockedRank();
    if (cur >= 5) return null;
    var nk = cur + 1;
    return { rank: nk, need: RANKS[nk].unlockWisdom, have: state.stats.wisdom, prevNeed: RANKS[cur].unlockWisdom };
  }
  function adviceState(adv) {
    if (adv.sageId === "original") return "show";
    if (!state.premiumUnlocked) return "premium";
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
      wis = '<div class="wisrow">' + L("叡智 " + s.wisdom + " ／ 最高の境地「" + esc(rankTitle(5)) + "」に到達",
        "Wisdom " + s.wisdom + " / Reached the highest stage “" + esc(rankTitle(5)) + "”") + '</div>';
    }
    return '<div class="statusbar">' +
      '<span class="heart">❤️</span>' +
      '<span class="mindbar"><i style="width:' + s.mind + '%"></i></span>' +
      '<span class="rankchip">' + esc(rankTitle(unlockedRank())) + '</span>' +
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
    var has = state.journal.length > 0;
    var pg = playerProgress(); var pos = positionFor(pg.points);
    var recall = dailyRecall();
    var recallHtml = recall ? '<div class="recall"><span class="recall-k">' + L("🕯 今日、心に留めたい言葉", "🕯 A word to keep in your heart today") + '</span>' +
      '<p class="recall-q">' + esc(recall.quote) + '</p>' +
      '<span class="recall-f">— ' + esc(recall.sageName) + '</span></div>' : "";
    var posLine = (has || pg.points > 0)
      ? '<p class="title-pos">' + L("あなたの位 ― ", "Your rank — ") + '<b>' + esc(posTitle(pos)) + '</b><span class="grade">' + esc(posGrade(pos)) + '</span></p>'
      : '';
    var langToggle = '<div class="lang-toggle">' +
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
      (has ? '<button class="btn ghost" data-act="reset">' + L("はじめからやり直す", "Start a new life") + '</button>' : "") +
      '</div>' +
      '<p class="codex-tease">' + L("✦ 伝説の言葉 " + codex.length + " / " + LEGENDS.length + " 蒐集 ✦", "✦ Legendary Words " + codex.length + " / " + LEGENDS.length + " collected ✦") + '</p>' +
      recallHtml +
      '<p class="tagline">' + L("迷ったとき、世界の偉人があなたの相談相手になる。<br>言葉を選び、暮らしに活かし、少しずつ賢くなっていく。",
        "When you are lost, the great minds of the world become your counsel.<br>Choose a word, live it, and grow a little wiser.") + '</p>' +
      '<p class="notice">' + L("※ これは制作中のプロトタイプ（MVP）です。名言はすべて出典付きで裏取りしています。<br>つらさが長く続くときは、どうか一人で抱えず、信頼できる人や専門の窓口に頼ってください。",
        "※ This is a prototype (MVP). Every quote is sourced and fact-checked.<br>If hardship persists, please don't carry it alone — reach out to someone you trust or a professional resource.") + '</p>';
    render(html);
  }

  // ---------- イベント ----------
  var currentEvent = null, currentLegend = null;
  var mode = "auto", consultCat = null;
  function pickEvent() {
    var pool;
    if (mode === "consult" && consultCat) {
      pool = EVENTS.filter(function (e) { return e.category === consultCat && state.seen.indexOf(e.id) < 0; });
      if (pool.length === 0) pool = EVENTS.filter(function (e) { return e.category === consultCat; });
    } else {
      pool = EVENTS.filter(function (e) { return state.seen.indexOf(e.id) < 0; });
      if (pool.length === 0) { state.seen = []; pool = EVENTS.slice(); }
    }
    return pool[Math.floor(Math.random() * pool.length)];
  }
  function proceed() {
    if (state.stats.mind < REST_THRESHOLD) { showRest(); return; }
    currentEvent = pickEvent();
    currentLegend = rollLegend();
    showEvent(currentEvent);
  }
  function showConsult() {
    var grid = CAT_KEYS.map(function (c) { return '<button class="consult-cat" data-consultcat="' + c + '">' + esc(catLabel(c)) + '</button>'; }).join("");
    render('<div class="fade">' + statusbar() +
      '<h2 class="event-title">' + L("どんなことで、悩んでいますか？", "What is troubling you?") + '</h2>' +
      '<p class="event-body">' + L("いま心にあるものを選ぶと、その悩みに効く言葉が訪れます。", "Choose what's on your heart, and words for that worry will come.") + '</p>' +
      '<div class="consult-grid">' + grid + '</div>' +
      '<button class="btn ghost" data-act="walk">' + L("おまかせで人生を歩む", "Let life unfold on its own") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("タイトルへ", "Back to title") + '</button>' +
      '</div>');
  }
  function showEvent(ev) {
    var legendHtml = currentLegend ? legendCard(currentLegend) : "";
    var cards = legendHtml + ev.advices.map(function (adv) { return adviceCard(ev, adv); }).join("");
    var paywall = state.premiumUnlocked ? "" :
      '<div class="paywall">' +
      '<h3>' + L("🕯 偉人フェーズ", "🕯 The Sages' Phase") + '</h3>' +
      '<p>' + L("ここから先は、世界の偉人があなたの相談相手に。<br>出典付きの本物の言葉、そして高みの賢者たちへ。",
        "Beyond here, the great minds of the world become your counsel.<br>Real, sourced words — and the higher sages await.") + '</p>' +
      '<button class="btn gold sm" data-act="unlock" style="display:inline-block">' + L("偉人フェーズを解放（デモ）", "Unlock the Sages' Phase (demo)") + '</button>' +
      '</div>';
    var consultBack = (mode === "consult") ? '<button class="btn ghost" data-act="consult">' + L("← 悩みを選び直す", "← Choose another worry") + '</button>' : "";
    var html = '<div class="fade">' + statusbar() +
      '<span class="eyebrow">' + esc(catLabel(ev.category)) + ' ・ ' + esc(moodLabel(ev.mood)) + '</span>' +
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

    if (st === "premium") {
      return '<div class="card locked" style="--c:' + color + '">' +
        '<div class="card-head"><span class="disc' + (scripture ? ' scripture' : '') + '">🔒</span>' +
        '<span class="sname">？？？</span><span class="badge">' + L("偉人フェーズ", "Sages' Phase") + '</span></div>' +
        '<p class="lockmsg">' + L("この言葉は <b>偉人フェーズ</b> で開きます。", "This word opens in the <b>Sages' Phase</b>.") + '</p></div>';
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
    for (var i = 0; i < 14; i++) { sparks += '<i style="--i:' + i + '"></i>'; }
    ov.innerHTML =
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
    requestAnimationFrame(function () { ov.classList.add("show"); });
    ov.querySelector(".cel-btn").addEventListener("click", function () {
      ov.classList.add("out");
      setTimeout(function () { ov.remove(); done(); }, 280);
    });
  }

  function showResult(idx, deltas, rankedUp, positionUp) {
    var rec = state.journal[idx];
    var dhtml = deltas.map(function (x) {
      var up = x.d > 0; return '<span class="delta ' + (up ? "up" : "down") + '">' + esc(statLabel(x.k)) + " " + (up ? "+" : "") + x.d + '</span>';
    }).join("");
    var rankBanner = rankedUp ? '<p class="saved-toast">' + L("✨ 新たな境地「" + esc(rankTitle(rankedUp)) + "」に到達した", "✨ You reached a new stage: “" + esc(rankTitle(rankedUp)) + "”") + '</p>' : "";
    var posBanner = positionUp ? '<p class="pos-banner">' + L("🎖 昇位 ―「" + esc(posTitle(positionUp)) + "（" + esc(posGrade(positionUp)) + "）」へ", "🎖 Promotion — to “" + esc(posTitle(positionUp)) + "” (" + esc(posGrade(positionUp)) + ")") + '</p>' : "";
    var ribbon = rec.isLegend ? '<p class="rarity-ribbon legendary">' + L("✦ 伝説の言葉 ✦", "✦ A Legendary Word ✦") + '</p>'
      : (rec.isScripture ? '<p class="rarity-ribbon sacred">' + L("神聖なる導き", "Sacred Guidance") + '</p>' : "");
    var html = '<div class="fade">' + ribbon +
      '<p class="result-quote">' + esc(rec.quote) + '</p>' +
      '<p class="result-from">— ' + esc(rec.sageName) + (rec.isScripture ? L("（聖典の言葉）", " (words of scripture)") : "") + '</p>' +
      (rec.source ? '<p class="result-source">' + esc(rec.source) + '</p>' : "") +
      (dhtml ? '<div class="deltas">' + dhtml + '</div>' : "") +
      rankBanner + posBanner +
      '<p class="saved-toast">' + L("📖 「わが叡智の書」に刻まれた", "📖 Inscribed in your Book of Wisdom") + '</p>' +
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
      '<button class="btn ghost" data-act="book">' + L("わが叡智の書を見る", "Open the Book of Wisdom") + '</button>' +
      '<button class="btn ghost" data-act="title">' + L("中断（タイトルへ）", "Pause (back to title)") + '</button>' +
      '</div>';
    render(html);
  }
  function setFeedback(idx, val) {
    if (!state.journal[idx]) return;
    state.journal[idx].feedback = (state.journal[idx].feedback === val) ? null : val;
    save();
    var box = app.querySelector(".fb");
    if (box) box.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-fb") === state.journal[idx].feedback); });
  }

  // ---------- 休息 ----------
  function showRest() {
    var lines = lang === "en"
      ? ["The courage to pause is also strength.", "You've done well today.", "Breathe in, breathe out. That alone is enough."]
      : ["立ち止まる勇気もまた、強さ。", "今日はもう、よく頑張った。", "息を吸って、吐いて。それだけで充分。"];
    var line = lines[Math.floor(Math.random() * lines.length)];
    state.stats.mind = clamp(state.stats.mind + 22); save();
    render('<div class="fade rest">' +
      '<div class="moon">🌙</div>' +
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
        return '<button class="chip' + (bookFilter === c ? " on" : "") + '" data-filter="' + c + '">' + (c === "all" ? L("すべて", "All") : esc(catLabel(c))) + '</button>';
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
      '<div class="when">' + ep + ' ・ ' + esc(when) + ' ・ ' + esc(catLabel(rec.category)) + '</div>' +
      '<div class="etitle">' + esc(rec.title) + '</div>' +
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

  // ---------- レンダリング & イベント委譲 ----------
  function render(html) { app.innerHTML = html; window.scrollTo(0, 0); }

  app.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act],[data-choose],[data-legend],[data-consultcat],[data-fb],[data-tab],[data-filter]");
    if (!t) return;
    if (t.hasAttribute("data-legend")) { chooseLegend(t.getAttribute("data-legend")); return; }
    if (t.hasAttribute("data-choose")) { choose(currentEvent, t.getAttribute("data-choose")); return; }
    if (t.hasAttribute("data-fb")) { var box = t.closest(".fb"); setFeedback(+box.getAttribute("data-fbidx"), t.getAttribute("data-fb")); return; }
    if (t.hasAttribute("data-tab")) { bookTab = t.getAttribute("data-tab"); showBook(); return; }
    if (t.hasAttribute("data-filter")) { bookFilter = t.getAttribute("data-filter"); showBook(); return; }
    if (t.hasAttribute("data-consultcat")) { mode = "consult"; consultCat = t.getAttribute("data-consultcat"); proceed(); return; }
    var act = t.getAttribute("data-act");
    if (act === "lang") { setLang(t.getAttribute("data-lang")); showTitle(); }
    else if (act === "walk") { mode = "auto"; consultCat = null; proceed(); }
    else if (act === "consult") showConsult();
    else if (act === "start" || act === "next") proceed();
    else if (act === "book") showBook();
    else if (act === "cert") showCert();
    else if (act === "title") showTitle();
    else if (act === "unlock") { state.premiumUnlocked = true; save(); if (currentEvent) showEvent(currentEvent); else proceed(); }
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

  showTitle();
})();
