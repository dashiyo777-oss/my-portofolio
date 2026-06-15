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
  var SAVE_KEY = "lifewisdom.save.v1";
  var REST_THRESHOLD = 25;

  var STAT_LABEL = { mind: "心", wisdom: "叡智", bonds: "絆", wealth: "財", passion: "情熱" };
  var CAT_LABEL = { work: "仕事", relationship: "人間関係", love: "恋愛", study: "学業", money: "お金", health: "健康", self: "自己" };
  var MOOD_LABEL = { down: "落ち込み", lost: "迷い", high: "高揚" };

  var app = document.getElementById("app");
  var state = load() || newGame();

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
  function resetGame() { state = newGame(); save(); showTitle(); }

  // ---------- ヘルパ ----------
  function clamp(n) { return Math.max(0, Math.min(100, Math.round(n))); }
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
    var html = '<div class="fade title-wrap">' +
      '<div class="flame">🪔</div>' +
      '<h1 class="title">叡智の灯火</h1>' +
      '<p class="subtitle">人生の岐路と、偉人たちの言葉</p>' +
      '</div>' +
      '<div class="title-actions">' +
      '<button class="btn gold" data-act="start">' + (has ? "つづきから歩む" : "人生をはじめる") + '</button>' +
      '<button class="btn ghost" data-act="book">わが叡智の書を見る' + (has ? "（" + state.journal.length + "）" : "") + '</button>' +
      (has ? '<button class="btn ghost" data-act="reset">はじめからやり直す</button>' : "") +
      '</div>' +
      '<p class="tagline">迷ったとき、世界の偉人があなたの相談相手になる。<br>正解を選ぶのではなく、あなたに響いた言葉を選ぼう。</p>' +
      '<p class="notice">※ これは制作中のプロトタイプ（MVP）です。名言はすべて出典付きで裏取りしています。</p>';
    render(html);
  }

  // ---------- 画面: イベント ----------
  var currentEvent = null;
  function pickEvent() {
    var pool = EVENTS.filter(function (e) { return state.seen.indexOf(e.id) < 0; });
    if (pool.length === 0) { state.seen = []; pool = EVENTS.slice(); }
    return pool[Math.floor(Math.random() * pool.length)];
  }
  function proceed() {
    if (state.stats.mind < REST_THRESHOLD) { showRest(); return; }
    currentEvent = pickEvent();
    showEvent(currentEvent);
  }
  function showEvent(ev) {
    var cards = ev.advices.map(function (adv) { return adviceCard(ev, adv); }).join("");
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
    var badge = adv.sageId === "original" ? '<span class="badge">無料</span>'
      : '<span class="badge' + (scripture ? ' sacred' : '') + '">' + esc(RANKS[sage.rank] ? RANKS[sage.rank].title : "") + '</span>';
    var note = adv.note ? '<p class="qnote">' + esc(adv.note) + '</p>' : "";
    var src = adv.source ? '<span class="source">— ' + esc(adv.source) + '</span>' : "";
    return '<button class="card tap" style="--c:' + color + '" data-choose="' + esc(adv.sageId) + '">' +
      '<div class="card-head">' +
      '<span class="disc' + (scripture ? ' scripture' : '') + '">' + esc(discChar(sage)) + '</span>' +
      '<span class="sname">' + esc(sage.name) + era + '</span>' + badge +
      '</div>' +
      '<p class="quote">' + esc(adv.quote) + '</p>' + note + src +
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
      var b = state.stats[k] || 0; state.stats[k] = clamp(b + adv.effects[k]);
      var diff = state.stats[k] - b; if (diff !== 0) deltas.push({ k: k, d: diff });
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
    recomputeFavorite(); save();
    var rankedUp = unlockedRank() > beforeRank ? unlockedRank() : 0;
    showResult(state.journal.length - 1, deltas, rankedUp);
  }

  function showResult(idx, deltas, rankedUp) {
    var rec = state.journal[idx];
    var dhtml = deltas.map(function (x) {
      var up = x.d > 0; return '<span class="delta ' + (up ? "up" : "down") + '">' + esc(STAT_LABEL[x.k] || x.k) + " " + (up ? "+" : "") + x.d + '</span>';
    }).join("");
    var rankBanner = rankedUp ? '<p class="saved-toast">✨ 新たな境地「' + esc(RANKS[rankedUp].title) + '」に到達した</p>' : "";
    var html = '<div class="fade">' +
      '<p class="result-quote">' + esc(rec.quote) + '</p>' +
      '<p class="result-from">— ' + esc(rec.sageName) + (rec.isScripture ? "（聖典の言葉）" : "") + '</p>' +
      (rec.source ? '<p class="result-source">' + esc(rec.source) + '</p>' : "") +
      (dhtml ? '<div class="deltas">' + dhtml + '</div>' : "") +
      rankBanner +
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
    if (j.length === 0) {
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

    var list;
    if (bookTab === "timeline") {
      list = j.slice().reverse().map(entryHTML).join("");
    } else {
      var items = j.filter(function (x) { return bookFilter === "all" || x.category === bookFilter; });
      // コレクション=言葉のお守り（重複した言葉はまとめず素直に列挙、新しい順）
      list = items.slice().reverse().map(entryHTML).join("") || '<div class="empty">この分類の記録はまだありません。</div>';
    }
    var filters = "";
    if (bookTab === "collection") {
      var cats = ["all"].concat(Object.keys(CAT_LABEL));
      filters = '<div class="filters">' + cats.map(function (c) {
        return '<button class="chip' + (bookFilter === c ? " on" : "") + '" data-filter="' + c + '">' + (c === "all" ? "すべて" : esc(CAT_LABEL[c])) + '</button>';
      }).join("") + '</div>';
    }
    render('<div class="fade">' + bookHeader() +
      '<div class="tabs">' +
      '<button class="' + (bookTab === "timeline" ? "on" : "") + '" data-tab="timeline">歩み</button>' +
      '<button class="' + (bookTab === "collection" ? "on" : "") + '" data-tab="collection">叡智のお守り</button>' +
      '</div>' + summary + filters + list +
      '<div class="footer-actions">' +
      '<button class="btn gold" data-act="start">人生をつづける</button>' +
      '<button class="btn ghost" data-act="title">タイトルへ</button>' +
      '</div></div>');
  }
  function bookHeader() {
    return '<div class="book-head"><span class="flame" style="font-size:24px">📖</span><h2>わが叡智の書</h2></div>';
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

  // ---------- レンダリング & イベント委譲 ----------
  function render(html) { app.innerHTML = html; window.scrollTo(0, 0); }

  app.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act],[data-choose],[data-fb],[data-tab],[data-filter]");
    if (!t) return;
    if (t.hasAttribute("data-choose")) { choose(currentEvent, t.getAttribute("data-choose")); return; }
    if (t.hasAttribute("data-fb")) { var box = t.closest(".fb"); setFeedback(+box.getAttribute("data-fbidx"), t.getAttribute("data-fb")); return; }
    if (t.hasAttribute("data-tab")) { bookTab = t.getAttribute("data-tab"); showBook(); return; }
    if (t.hasAttribute("data-filter")) { bookFilter = t.getAttribute("data-filter"); showBook(); return; }
    var act = t.getAttribute("data-act");
    if (act === "start" || act === "next") proceed();
    else if (act === "book") showBook();
    else if (act === "title") showTitle();
    else if (act === "unlock") { state.premiumUnlocked = true; save(); showEvent(currentEvent); }
    else if (act === "reset") { if (confirm("これまでの歩みと叡智の書が消えます。よろしいですか？")) resetGame(); }
  });

  showTitle();
})();
