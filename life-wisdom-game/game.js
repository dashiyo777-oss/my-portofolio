/* 叡智の灯火 — MVP ゲームロジック（ビルド不要 / localStorage 永続）
   設計: ../SPEC.md  データ: data/sages.json + data/events.json (→ gamedata.js)
   方針メモ:
   - 無料=「灯火の声」(original)。課金=偉人フェーズ(premiumUnlocked)。高ランク偉人は叡智(wisdom)で解放(§4.3/§10.2)。
   - 聖典は神を一人称で演じず「聖典の言葉」として提示。顔画像を持たせない(§4.4)。
   - 決断は journal にスナップショット保存→「わが叡智の書」で後から辿れる(§6.6)。響き度(§6.7)も保存。 */
(function () {
  "use strict";
  var D = window.GAME_DATA;
  if (!D) { document.getElementById("app").innerHTML = "<p style='padding:24px'>データを読み込めませんでした。<br>data/gamedata.js を確認してください（build-data.py で生成）。</p>"; return; }

  var SAGES = {}; D.sages.sages.forEach(function (s) { SAGES[s.id] = s; });
  var RANKS = D.sages.ranks;             // {"1":{title,unlockWisdom}, ...}
  var EVENTS = D.events.events;
  var LEGENDS = (D.legends && D.legends.legends) || [];
  var SAVE_KEY = "lifewisdom.save.v1";
  var CODEX_KEY = "lifewisdom.codex.v1";   // 伝説の図鑑は人生(セーブ)を越えて引き継ぐ
  var REST_THRESHOLD = 25;
  var RARITY_LABEL = { common: "並", rare: "希", sacred: "神聖", legendary: "伝説" };

  // 叡智の位（段位）。偉人ランク(§4.3)とは別の、プレイヤー自身の格付け。生涯記録ベース＝下がらない。
  var POSITIONS = [
    { min: 0, title: "灯火の見習い", grade: "無級" },
    { min: 60, title: "学びの徒", grade: "五級" },
    { min: 150, title: "思索の人", grade: "三級" },
    { min: 280, title: "求道の人", grade: "一級" },
    { min: 430, title: "賢慮の士", grade: "初段" },
    { min: 620, title: "叡智の探究者", grade: "参段" },
    { min: 850, title: "達観の人", grade: "伍段" },
    { min: 1100, title: "心の師範", grade: "七段" },
    { min: 1400, title: "叡智の達人", grade: "九段" },
    { min: 1700, title: "賢聖", grade: "十段" },
    { min: 1950, title: "叡智名人", grade: "名人" },
    { min: 2200, title: "叡智皆伝", grade: "免許皆伝" }
  ];
  var ACCLAIM_KEY = "lifewisdom.acclaim.v1";   // 生涯記録（到達した言葉・制覇カテゴリ）。人生をやり直しても残る。

  var STAT_LABEL = { mind: "心", wisdom: "叡智", bonds: "絆", wealth: "財", passion: "情熱" };
  var CAT_LABEL = { work: "仕事", relationship: "人間関係", love: "恋愛", study: "学業", money: "お金", health: "健康", self: "自己" };
  var MOOD_LABEL = { down: "落ち込み", lost: "迷い", high: "高揚" };

  var app = document.getElementById("app");
  var state = load() || newGame();
  var codex = loadCodex();   // 見つけた伝説ID[]
  var acclaim = loadAcclaim();   // 生涯記録 { quotes:{key:1}, cats:{cat:1} }

  // ---------- セーブ/ロード ----------
  function newGame() {
    return {
      v: 1,
      stats: { mind: 60, wisdom: 0, bonds: 50, wealth: 50, passion: 50 },
      turn: 0, journal: [], seen: [], premiumUnlocked: false, favoriteSage: null
    };
  }
  function save() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); } catch (e) {} }
  function load() { try { var r = localStorage.getItem(SAVE_KEY); return r ? JSON.parse(r) : null; } catch (e) { return null; } }
  function resetGame() { state = newGame(); save(); showTitle(); }  // codex は意図的に残す（人生を越えて引き継ぐ叡智）

  // ---------- 伝説の図鑑（codex） ----------
  function loadCodex() { try { return JSON.parse(localStorage.getItem(CODEX_KEY)) || []; } catch (e) { return []; } }
  function saveCodex() { try { localStorage.setItem(CODEX_KEY, JSON.stringify(codex)); } catch (e) {} }
  function codexHas(id) { return codex.indexOf(id) >= 0; }
  function codexAdd(id) { if (!codexHas(id)) { codex.push(id); saveCodex(); } }

  // ---------- 叡智の位（段位・免許状） ----------
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
  // 伝説との遭遇判定：未収集かつ叡智条件を満たす伝説から、低確率で1枚（叡智が高いほど遭遇率UP）
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
  // 叡智(wisdom)は経験値として上限なく積む。他のステータスは 0–100。
  function applyStat(k, delta) {
    var before = state.stats[k] || 0;
    var nv = before + delta;
    state.stats[k] = (k === "wisdom") ? Math.max(0, Math.round(nv)) : clamp(nv);
    return state.stats[k] - before;
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function isScripture(id) { return id.indexOf("scripture") === 0; }

  function unlockedRank() {
    var r = 1; [1, 2, 3, 4, 5].forEach(function (k) { if (state.stats.wisdom >= RANKS[k].unlockWisdom) r = k; });
    return r;
  }
  function nextRankInfo() {
    var cur = unlockedRank();
    if (cur >= 5) return null;
    var nk = cur + 1;
    return { rank: nk, title: RANKS[nk].title, need: RANKS[nk].unlockWisdom, have: state.stats.wisdom, prevNeed: RANKS[cur].unlockWisdom };
  }
  // 助言の表示状態: "show" | "premium" | "rank"
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
    return sage.name.charAt(0);
  }
  function recomputeFavorite() {
    var c = {}; state.journal.forEach(function (j) {
      if (j.chosenSageId && j.chosenSageId !== "original" && !isScripture(j.chosenSageId)) c[j.chosenSageId] = (c[j.chosenSageId] || 0) + 1;
    });
    var best = null, n = 0; Object.keys(c).forEach(function (k) { if (c[k] > n) { n = c[k]; best = k; } });
    state.favoriteSage = best;
  }

  // ---------- 画面: ステータスバー ----------
  function statusbar() {
    var s = state.stats, nx = nextRankInfo();
    var wis = "";
    if (nx) {
      var span = nx.need - nx.prevNeed, prog = Math.max(0, Math.min(1, (nx.have - nx.prevNeed) / span));
      wis = '<div class="wisrow">叡智 ' + s.wisdom + ' ／ 次の境地「' + esc(nx.title) + '」まで あと ' + Math.max(0, nx.need - nx.have) +
        '<div class="wbar"><i style="width:' + (prog * 100).toFixed(0) + '%"></i></div></div>';
    } else {
      wis = '<div class="wisrow">叡智 ' + s.wisdom + ' ／ 最高の境地「' + esc(RANKS[5].title) + '」に到達</div>';
    }
    return '<div class="statusbar">' +
      '<span class="heart">❤️</span>' +
      '<span class="mindbar"><i style="width:' + s.mind + '%"></i></span>' +
      '<span class="rankchip">' + esc(RANKS[unlockedRank()].title) + '</span>' +
      '</div>' + wis;
  }

  // ---------- 画面: タイトル ----------
  function showTitle() {
    var has = state.journal.length > 0;
    var pg = playerProgress(); var pos = positionFor(pg.points);
    var posLine = (has || pg.points > 0)
      ? '<p class="title-pos">あなたの位 ― <b>' + esc(pos.title) + '</b><span class="grade">' + esc(pos.grade) + '</span></p>'
      : '';
    var html = '<div class="fade title-wrap">' +
      '<div class="flame">🪔</div>' +
      '<h1 class="title">叡智の灯火</h1>' +
      '<p class="subtitle">人生の岐路と、偉人たちの言葉</p>' +
      posLine +
      '</div>' +
      '<div class="title-actions">' +
      '<button class="btn gold" data-act="start">' + (has ? "つづきから歩む" : "人生をはじめる") + '</button>' +
      '<button class="btn ghost" data-act="book">わが叡智の書を見る' + (has ? "（" + state.journal.length + "）" : "") + '</button>' +
      '<button class="btn ghost" data-act="cert">叡智の免許状を見る</button>' +
      (has ? '<button class="btn ghost" data-act="reset">はじめからやり直す</button>' : "") +
      '</div>' +
      '<p class="codex-tease">✦ 伝説の言葉 ' + codex.length + ' / ' + LEGENDS.length + ' 蒐集 ✦</p>' +
      '<p class="tagline">迷ったとき、世界の偉人があなたの相談相手になる。<br>正解を選ぶのではなく、あなたに響いた言葉を選ぼう。</p>' +
      '<p class="notice">※ これは制作中のプロトタイプ（MVP）です。名言はすべて出典付きで裏取りしています。</p>';
    render(html);
  }

  // ---------- 画面: イベント ----------
  var currentEvent = null, currentLegend = null;
  function pickEvent() {
    var pool = EVENTS.filter(function (e) { return state.seen.indexOf(e.id) < 0; });
    if (pool.length === 0) { state.seen = []; pool = EVENTS.slice(); }
    return pool[Math.floor(Math.random() * pool.length)];
  }
  function proceed() {
    if (state.stats.mind < REST_THRESHOLD) { showRest(); return; }
    currentEvent = pickEvent();
    currentLegend = rollLegend();
    showEvent(currentEvent);
  }
  function showEvent(ev) {
    var legendHtml = currentLegend ? legendCard(currentLegend) : "";
    var cards = legendHtml + ev.advices.map(function (adv) { return adviceCard(ev, adv); }).join("");
    var paywall = state.premiumUnlocked ? "" :
      '<div class="paywall">' +
      '<h3>🕯 偉人フェーズ</h3>' +
      '<p>ここから先は、世界の偉人があなたの相談相手に。<br>出典付きの本物の言葉、そして高みの賢者たちへ。</p>' +
      '<button class="btn gold sm" data-act="unlock" style="display:inline-block">偉人フェーズを解放（デモ）</button>' +
      '</div>';
    var html = '<div class="fade">' + statusbar() +
      '<span class="eyebrow">' + esc(CAT_LABEL[ev.category] || ev.category) + ' ・ ' + esc(MOOD_LABEL[ev.mood] || ev.mood) + '</span>' +
      '<h2 class="event-title">' + esc(ev.title) + '</h2>' +
      '<p class="event-body">' + esc(ev.body) + '</p>' +
      '<p class="advice-help">心に響いた言葉を、ひとつ選ぼう。</p>' +
      paywall + cards +
      '<button class="btn ghost" data-act="book">わが叡智の書</button>' +
      '</div>';
    render(html);
  }
  function adviceCard(ev, adv) {
    var sage = SAGES[adv.sageId] || { name: adv.sageId, color: "#999" };
    var st = adviceState(adv);
    var scripture = isScripture(adv.sageId);
    var color = sage.color || "#999";

    if (st === "premium") {
      return '<div class="card locked" style="--c:' + color + '">' +
        '<div class="card-head"><span class="disc' + (scripture ? ' scripture' : '') + '">🔒</span>' +
        '<span class="sname">？？？</span><span class="badge">偉人フェーズ</span></div>' +
        '<p class="lockmsg">この言葉は <b>偉人フェーズ</b> で開きます。</p></div>';
    }
    if (st === "rank") {
      var need = RANKS[sage.rank].unlockWisdom;
      return '<div class="card locked" style="--c:' + color + '">' +
        '<div class="card-head"><span class="disc' + (scripture ? ' scripture' : '') + '">🔒</span>' +
        '<span class="sname">' + esc(sage.name) + '</span>' +
        '<span class="badge' + (scripture ? ' sacred' : '') + '">' + esc(RANKS[sage.rank].title) + '</span></div>' +
        '<p class="lockmsg">叡智 <b>' + need + '</b> で出会える（あと ' + Math.max(0, need - state.stats.wisdom) + '）。</p></div>';
    }
    // 表示可能
    var era = sage.era ? '<span class="era">' + esc(sage.era) + '</span>' : "";
    var rarity = adv.sageId === "original" ? null : rarityOf(adv.sageId, false);
    var pill = rarity ? '<span class="rar rar-' + rarity + '">' + RARITY_LABEL[rarity] + '</span>' : '<span class="rar rar-free">無料</span>';
    var note = adv.note ? '<p class="qnote">' + esc(adv.note) + '</p>' : "";
    var src = adv.source ? '<span class="source">— ' + esc(adv.source) + '</span>' : "";
    return '<button class="card tap" data-rarity="' + (rarity || "free") + '" style="--c:' + color + '" data-choose="' + esc(adv.sageId) + '">' +
      '<div class="card-head">' +
      '<span class="disc' + (scripture ? ' scripture' : '') + '">' + esc(discChar(sage)) + '</span>' +
      '<span class="sname">' + esc(sage.name) + era + '</span>' + pill +
      '</div>' +
      '<p class="quote">' + esc(adv.quote) + '</p>' + note + src +
      '</button>';
  }
  // 伝説カード（出会いの予兆だけ見せ、内容は祝福演出で明かす）
  function legendCard(legend) {
    var sage = SAGES[legend.sageId] || { color: "#caa45d" };
    return '<button class="card tap legend" data-rarity="legendary" style="--c:' + (sage.color || "#caa45d") + '" data-legend="' + esc(legend.id) + '">' +
      '<div class="card-head"><span class="disc legenddisc">✦</span>' +
      '<span class="sname">特別な来訪</span><span class="rar rar-legendary">✦ 伝説 ✦</span></div>' +
      '<p class="quote legend-teaser">いにしえの偉人が、あなたに言葉を贈ろうとしている……<br>そっと、受け取ってみますか。</p>' +
      '</button>';
  }

  // ---------- 決断 ----------
  function choose(ev, sageId) {
    var adv = null; ev.advices.forEach(function (a) { if (a.sageId === sageId) adv = a; });
    if (!adv || adviceState(adv) !== "show") return;
    var sage = SAGES[sageId] || {};
    var beforeMind = state.stats.mind, beforeRank = unlockedRank();
    var deltas = [];
    Object.keys(adv.effects || {}).forEach(function (k) {
      var diff = applyStat(k, adv.effects[k]); if (diff !== 0) deltas.push({ k: k, d: diff });
    });
    var rec = {
      ts: new Date().toISOString(), turn: state.turn + 1,
      eventId: ev.id, category: ev.category, mood: ev.mood, title: ev.title,
      chosenSageId: sageId, sageName: sage.name || sageId,
      quote: adv.quote, source: adv.source || "", note: adv.note || "",
      tradition: adv.tradition || null, isScripture: isScripture(sageId),
      mindBefore: beforeMind, mindAfter: state.stats.mind, playerNote: "", feedback: null
    };
    state.turn++; state.journal.push(rec);
    if (state.seen.indexOf(ev.id) < 0) state.seen.push(ev.id);
    currentLegend = null;  // 通常の言葉を選んだら、伝説はそっと去る
    var beforePos = positionFor(playerProgress().points);
    recordAcclaim(ev.id + ":" + sageId, ev.category);
    var positionUp = positionFor(playerProgress().points).title !== beforePos.title ? positionFor(playerProgress().points) : null;
    recomputeFavorite(); save();
    var rankedUp = unlockedRank() > beforeRank ? unlockedRank() : 0;
    showResult(state.journal.length - 1, deltas, rankedUp, positionUp);
  }

  // 伝説を受け取る：祝福演出 → 図鑑に蒐集 → 結果
  function chooseLegend(id) {
    var legend = null; LEGENDS.forEach(function (l) { if (l.id === id) legend = l; });
    if (!legend || codexHas(id)) return;
    var sage = SAGES[legend.sageId] || {};
    var beforeRank = unlockedRank();
    var deltas = [];
    Object.keys(legend.effects || {}).forEach(function (k) {
      var diff = applyStat(k, legend.effects[k]); if (diff !== 0) deltas.push({ k: k, d: diff });
    });
    var ev = currentEvent || {};
    var rec = {
      ts: new Date().toISOString(), turn: state.turn + 1,
      eventId: ev.id || "", category: ev.category || "self", mood: ev.mood || "", title: ev.title || "伝説との邂逅",
      chosenSageId: legend.sageId, sageName: sage.name || legend.sageId,
      quote: legend.quote, source: legend.source || "", note: legend.note || "",
      tradition: legend.tradition || null, isScripture: isScripture(legend.sageId),
      isLegend: true, legendId: legend.id, rarity: "legendary",
      mindBefore: state.stats.mind, mindAfter: state.stats.mind, playerNote: "", feedback: null
    };
    rec.mindBefore = rec.mindAfter; // 表示用（伝説は心も整う）
    var beforePos = positionFor(playerProgress().points);
    state.turn++; state.journal.push(rec); codexAdd(legend.id);
    recordAcclaim("legend:" + legend.id, ev.category || "self");
    var positionUp = positionFor(playerProgress().points).title !== beforePos.title ? positionFor(playerProgress().points) : null;
    if (ev.id && state.seen.indexOf(ev.id) < 0) state.seen.push(ev.id);
    currentLegend = null; recomputeFavorite(); save();
    var rankedUp = unlockedRank() > beforeRank ? unlockedRank() : 0;
    var idx = state.journal.length - 1;
    celebrate(legend, function () { showResult(idx, deltas, rankedUp, positionUp); });
  }

  // 祝福演出（全画面・光と粒子）
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
      '<div class="cel-label">✦ 伝説の言葉に出会った ✦</div>' +
      '<div class="cel-quote">' + esc(legend.quote) + '</div>' +
      '<div class="cel-from">— ' + esc(sage.name || legend.sageId) + (isScripture(legend.sageId) ? "（聖典）" : "") + '</div>' +
      (legend.source ? '<div class="cel-source">' + esc(legend.source) + '</div>' : "") +
      '<div class="cel-count">伝説 ' + found + ' / ' + total + ' 蒐集</div>' +
      '<button class="btn gold cel-btn">この叡智を受け取る</button>' +
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
      var up = x.d > 0; return '<span class="delta ' + (up ? "up" : "down") + '">' + esc(STAT_LABEL[x.k] || x.k) + " " + (up ? "+" : "") + x.d + '</span>';
    }).join("");
    var rankBanner = rankedUp ? '<p class="saved-toast">✨ 新たな境地「' + esc(RANKS[rankedUp].title) + '」に到達した</p>' : "";
    var posBanner = positionUp ? '<p class="pos-banner">🎖 昇位 ―「' + esc(positionUp.title) + '（' + esc(positionUp.grade) + '）」へ</p>' : "";
    var ribbon = rec.isLegend ? '<p class="rarity-ribbon legendary">✦ 伝説の言葉 ✦</p>'
      : (rec.isScripture ? '<p class="rarity-ribbon sacred">神聖なる導き</p>' : "");
    var html = '<div class="fade">' + ribbon +
      '<p class="result-quote">' + esc(rec.quote) + '</p>' +
      '<p class="result-from">— ' + esc(rec.sageName) + (rec.isScripture ? "（聖典の言葉）" : "") + '</p>' +
      (rec.source ? '<p class="result-source">' + esc(rec.source) + '</p>' : "") +
      (dhtml ? '<div class="deltas">' + dhtml + '</div>' : "") +
      rankBanner + posBanner +
      '<p class="saved-toast">📖 「わが叡智の書」に刻まれた</p>' +
      '<div class="fb" data-fbidx="' + idx + '">' +
      '<button data-fb="resonated">響いた ♡</button>' +
      '<button data-fb="not_now">今はそうでもない</button>' +
      '</div>' +
      '<button class="btn gold" data-act="next">人生をつづける</button>' +
      '<button class="btn ghost" data-act="book">わが叡智の書を見る</button>' +
      '</div>';
    render(html);
  }
  function setFeedback(idx, val) {
    if (!state.journal[idx]) return;
    state.journal[idx].feedback = (state.journal[idx].feedback === val) ? null : val;
    save();
    var box = app.querySelector(".fb");
    if (box) box.querySelectorAll("button").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-fb") === state.journal[idx].feedback);
    });
  }

  // ---------- 休息 ----------
  function showRest() {
    var lines = [
      "立ち止まる勇気もまた、強さ。",
      "今日はもう、よく頑張った。",
      "息を吸って、吐いて。それだけで充分。"
    ];
    var line = lines[Math.floor(Math.random() * lines.length)];
    state.stats.mind = clamp(state.stats.mind + 22); save();
    var html = '<div class="fade rest">' +
      '<div class="moon">🌙</div>' +
      '<p class="line">' + esc(line) + '</p>' +
      '<p class="muted small">心が少し、回復した（心 +22）</p>' +
      '<button class="btn gold" data-act="next">また歩き出す</button>' +
      '</div>';
    render(html);
  }

  // ---------- わが叡智の書 ----------
  var bookTab = "timeline", bookFilter = "all";
  function showBook() {
    var j = state.journal;
    if (j.length === 0 && codex.length === 0) {
      render('<div class="fade">' + bookHeader() +
        '<div class="empty">まだ何も記されていません。<br>人生を歩み、言葉を受け取りましょう。</div>' +
        '<button class="btn gold" data-act="start">人生をはじめる</button>' +
        '<button class="btn ghost" data-act="title">タイトルへ</button></div>');
      return;
    }
    var fav = state.favoriteSage ? SAGES[state.favoriteSage] : null;
    var resonated = j.filter(function (x) { return x.feedback === "resonated"; }).length;
    var summary = '<div class="summary">あなたは <b>' + j.length + '</b> の岐路を歩み、<b>' + resonated + '</b> の言葉に「響いた」と頷いた。' +
      (fav ? '<br>最も多く言葉を選んだのは <b>' + esc(fav.name) + '</b>。あなたの座右の賢者。' : "") + '</div>';

    var list, filters = "";
    if (bookTab === "codex") {
      list = codexHTML();
    } else if (bookTab === "timeline") {
      list = j.slice().reverse().map(entryHTML).join("") || '<div class="empty">まだ歩みはありません。</div>';
    } else {
      var items = j.filter(function (x) { return bookFilter === "all" || x.category === bookFilter; });
      // コレクション=言葉のお守り（重複した言葉はまとめず素直に列挙、新しい順）
      list = items.slice().reverse().map(entryHTML).join("") || '<div class="empty">この分類の記録はまだありません。</div>';
      var cats = ["all"].concat(Object.keys(CAT_LABEL));
      filters = '<div class="filters">' + cats.map(function (c) {
        return '<button class="chip' + (bookFilter === c ? " on" : "") + '" data-filter="' + c + '">' + (c === "all" ? "すべて" : esc(CAT_LABEL[c])) + '</button>';
      }).join("") + '</div>';
    }
    render('<div class="fade">' + bookHeader() +
      '<div class="tabs">' +
      '<button class="' + (bookTab === "timeline" ? "on" : "") + '" data-tab="timeline">歩み</button>' +
      '<button class="' + (bookTab === "collection" ? "on" : "") + '" data-tab="collection">お守り</button>' +
      '<button class="' + (bookTab === "codex" ? "on" : "") + '" data-tab="codex">伝説 ' + codex.length + '/' + LEGENDS.length + '</button>' +
      '</div>' + summary + filters + list +
      '<div class="footer-actions">' +
      '<button class="btn gold" data-act="start">人生をつづける</button>' +
      '<button class="btn ghost" data-act="title">タイトルへ</button>' +
      '</div></div>');
  }
  function bookHeader() {
    return '<div class="book-head"><span class="flame" style="font-size:24px">📖</span><h2>わが叡智の書</h2></div>';
  }
  function codexHTML() {
    var head = '<div class="codex-head">✦ 伝説の言葉 <b>' + codex.length + '</b> / ' + LEGENDS.length + ' 蒐集 ✦<br>' +
      '<span class="small muted">めったに現れぬ言葉。叡智を深めるほど、出会いは近づく。</span></div>';
    var grid = LEGENDS.map(function (l) {
      var sage = SAGES[l.sageId] || {};
      if (codexHas(l.id)) {
        return '<div class="legend-slot found" style="--c:' + (sage.color || "#caa45d") + '">' +
          '<div class="ls-head">✦ ' + esc(sage.name || l.sageId) + (isScripture(l.sageId) ? "（聖典）" : "") + '</div>' +
          '<div class="ls-quote">' + esc(l.quote) + '</div>' +
          '<div class="ls-src">' + esc(l.source || "") + '</div></div>';
      }
      return '<div class="legend-slot locked">' +
        '<div class="ls-head">？ ？ ？</div>' +
        '<div class="ls-quote">未だ見ぬ言葉 — 叡智 ' + (l.minWisdom || 0) + ' 以上で出会える</div></div>';
    }).join("");
    return head + '<div class="codex-grid">' + grid + '</div>';
  }
  function entryHTML(rec) {
    var sage = SAGES[rec.chosenSageId] || { color: "#bbb" };
    var d = new Date(rec.ts);
    var when = isNaN(d) ? "" : (d.getMonth() + 1) + "/" + d.getDate() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
    var fb = rec.feedback === "resonated" ? "♡ 響いた" : (rec.feedback === "not_now" ? "今はそうでもない" : "");
    return '<div class="entry" style="--c:' + (sage.color || "#bbb") + '">' +
      '<div class="when">第' + rec.turn + '話 ・ ' + esc(when) + ' ・ ' + esc(CAT_LABEL[rec.category] || rec.category) + '</div>' +
      '<div class="etitle">' + esc(rec.title) + '</div>' +
      '<div class="eq">' + esc(rec.quote) + '</div>' +
      '<div class="efrom">— ' + esc(rec.sageName) + (rec.isScripture ? "（聖典）" : "") + (rec.source ? " ／ " + esc(rec.source) : "") + '</div>' +
      (fb ? '<div class="fbmark">' + esc(fb) + '</div>' : "") +
      '</div>';
  }

  // ---------- 叡智の免許状（証明書） ----------
  function showCert() {
    var pg = playerProgress(); var pos = positionFor(pg.points); var nx = nextPosition(pg.points);
    var d = new Date();
    var ymd = d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日";
    var prog = "";
    if (nx) {
      var span = nx.min - pos.min, p = Math.max(0, Math.min(1, (pg.points - pos.min) / span));
      prog = '<div class="cert-next">次の位「' + esc(nx.title) + '（' + esc(nx.grade) + '）」まで あと ' + (nx.min - pg.points) + ' 点' +
        '<div class="wbar"><i style="width:' + (p * 100).toFixed(0) + '%"></i></div></div>';
    } else {
      prog = '<div class="cert-next">最高位「叡智皆伝」に到達。あなたは生涯の探究者。</div>';
    }
    var html = '<div class="fade">' +
      '<div class="certificate">' +
      '<div class="cert-corner tl"></div><div class="cert-corner tr"></div><div class="cert-corner bl"></div><div class="cert-corner br"></div>' +
      '<div class="cert-kicker">叡 智 之 證</div>' +
      '<div class="cert-sub">人生相談 叡智検定</div>' +
      '<div class="cert-pos">' + esc(pos.title) + '</div>' +
      '<div class="cert-grade">' + esc(pos.grade) + '</div>' +
      '<div class="cert-stats">' +
      '<div><b>' + pg.points + '</b><span>叡智ポイント</span></div>' +
      '<div><b>' + pg.quotes + '</b><span>到達した言葉</span></div>' +
      '<div><b>' + pg.legends + ' / ' + LEGENDS.length + '</b><span>伝説</span></div>' +
      '<div><b>' + pg.cats + ' / 7</b><span>制覇した悩み</span></div>' +
      '</div>' +
      '<div class="cert-foot"><span class="cert-date">' + esc(ymd) + ' 発行</span><span class="cert-seal">灯</span></div>' +
      '</div>' +
      prog +
      '<p class="notice">※ 位は「到達した言葉・伝説・制覇カテゴリ」の生涯記録で決まり、人生をやり直しても下がりません。</p>' +
      '<button class="btn gold" data-act="start">人生をつづける</button>' +
      '<button class="btn ghost" data-act="title">タイトルへ</button>' +
      '</div>';
    render(html);
  }

  // ---------- レンダリング & イベント委譲 ----------
  function render(html) { app.innerHTML = html; window.scrollTo(0, 0); }

  app.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act],[data-choose],[data-legend],[data-fb],[data-tab],[data-filter]");
    if (!t) return;
    if (t.hasAttribute("data-legend")) { chooseLegend(t.getAttribute("data-legend")); return; }
    if (t.hasAttribute("data-choose")) { choose(currentEvent, t.getAttribute("data-choose")); return; }
    if (t.hasAttribute("data-fb")) { var box = t.closest(".fb"); setFeedback(+box.getAttribute("data-fbidx"), t.getAttribute("data-fb")); return; }
    if (t.hasAttribute("data-tab")) { bookTab = t.getAttribute("data-tab"); showBook(); return; }
    if (t.hasAttribute("data-filter")) { bookFilter = t.getAttribute("data-filter"); showBook(); return; }
    var act = t.getAttribute("data-act");
    if (act === "start" || act === "next") proceed();
    else if (act === "book") showBook();
    else if (act === "cert") showCert();
    else if (act === "title") showTitle();
    else if (act === "unlock") { state.premiumUnlocked = true; save(); showEvent(currentEvent); }
    else if (act === "reset") { if (confirm("これまでの歩みと叡智の書が消えます。よろしいですか？")) resetGame(); }
  });

  showTitle();
})();
