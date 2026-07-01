/*
 * Kiku（効く）— アプリ本体
 * --------------------------------------------------------------
 * 役割:
 *  - ランキングスコアの算出（「バズ＝高評価」を防ぐ透明な式 / SPEC.md §4）
 *  - 画面描画（ホーム/ランキング・詳細）とハッシュルーティング
 *  - 体感評価・「やってみた」記録・チップ（mock）の状態管理（localStorage）
 *  - 日英 i18n（海外展開の土台 / CONCEPT.md §1）
 * 依存なし・素のJS。index.html を開くだけで動く。
 */
(function () {
  "use strict";

  var DATA = window.APP_DATA;
  var LS_KEY = "kiku.state.v1";

  // ── 状態（端末内・localStorage 永続） ──
  // 将来サーバ集計に移すとき、この形がそのまま API 入出力になる想定。
  var state = loadState();

  function loadState() {
    try {
      var s = JSON.parse(localStorage.getItem(LS_KEY) || "{}");
      var browserLang = (navigator.language || "ja").slice(0, 2) === "en" ? "en" : "ja";
      return {
        lang: s.lang || browserLang,
        // 信頼性フィルタ（好みとして永続）: "all" | "expert" | "study" | "reviewed"
        quality: s.quality || "all",
        // contentId -> { tried:bool, feedback:"resonated"|"not_now"|null, tipped:int }
        user: s.user || {}
      };
    } catch (e) {
      return { lang: "ja", quality: "all", user: {} };
    }
  }
  function save() { localStorage.setItem(LS_KEY, JSON.stringify(state)); }
  function userOf(id) {
    if (!state.user[id]) state.user[id] = { tried: false, feedback: null, tipped: 0 };
    return state.user[id];
  }

  // ── i18n ──
  var STR = {
    brand:        { ja: "効く", en: "Kiku" },
    tagline:      { ja: "本当に効く生活の知恵を、ランクで。", en: "Life tips that actually work — ranked." },
    all:          { ja: "すべて", en: "All" },
    rankedBy:     { ja: "効くスコア順", en: "By Kiku Score" },
    kikuScore:    { ja: "効くスコア", en: "Kiku Score" },
    why:          { ja: "スコアの内訳", en: "Score breakdown" },
    felt:         { ja: "体感レビュー", en: "User experience" },
    feltRate:     { ja: "「効いた」割合", en: "“It worked” rate" },
    evidence:     { ja: "科学的根拠", en: "Scientific evidence" },
    supervision:  { ja: "専門家監修", en: "Expert review" },
    reach:        { ja: "試した人", en: "People who tried" },
    steps:        { ja: "やり方", en: "How to" },
    caution:      { ja: "注意", en: "Caution" },
    source:       { ja: "出典（元の投稿）", en: "Source (original post)" },
    openSource:   { ja: "元の投稿を見る ↗", en: "View original post ↗" },
    by:           { ja: "提供", en: "By" },
    from:         { ja: "発掘元", en: "Found in" },
    didTry:       { ja: "やってみた", en: "I tried it" },
    didTryDone:   { ja: "やってみた ✓", en: "Tried ✓" },
    askFeedback:  { ja: "あなたには効きましたか？", en: "Did it work for you?" },
    resonated:    { ja: "効いた", en: "It worked" },
    notNow:       { ja: "自分には今ひとつ", en: "Not for me" },
    thanks:       { ja: "フィードバックありがとう！評価に反映しました。", en: "Thanks! Your feedback is counted." },
    tip:          { ja: "チップを贈る", en: "Send a tip" },
    tipDesc:      { ja: "効果を実感したら、貢献者へ感謝を。", en: "Felt the benefit? Thank the contributor." },
    tipThanks:    { ja: "に贈りました。ありがとう！", en: "— sent. Thank you!" },
    tipDemo:      { ja: "※デモです。実際の決済は行われません。", en: "Demo only — no real payment is made." },
    back:         { ja: "← 一覧へ", en: "← Back" },
    notMedical:   { ja: "本アプリは医療行為ではありません。体調に不安があるときは専門機関へご相談ください。",
                    en: "This app is not medical advice. If unwell, please consult a professional." },
    ev_none:      { ja: "対象外", en: "N/A" },
    ev_anecdotal: { ja: "体験談レベル", en: "Anecdotal" },
    ev_expert:    { ja: "専門家の見解", en: "Expert opinion" },
    ev_study:     { ja: "研究の裏付け", en: "Study-backed" },
    rv_unreviewed:{ ja: "未監修", en: "Not reviewed" },
    rv_expert:    { ja: "監修済み", en: "Reviewed" },
    empty:        { ja: "このジャンルはまだありません。", en: "Nothing here yet." },
    rankLabel:    { ja: "位", en: "" },
    searchPh:     { ja: "キーワードで検索（例: 認知症予防、海外発掘）", en: "Search (e.g. tag, keyword)" },
    tagsLabel:    { ja: "タグで横断", en: "Filter by tag" },
    clear:        { ja: "クリア", en: "Clear" },
    results:      { ja: "件", en: " results" },
    noResults:    { ja: "条件に合う情報が見つかりませんでした。", en: "No matching tips found." },
    relatedTags:  { ja: "タグ", en: "Tags" },
    qualityLabel: { ja: "信頼性で絞る", en: "Filter by trust" },
    q_all:        { ja: "すべて", en: "All" },
    q_expert:     { ja: "専門家以上", en: "Expert+" },
    q_study:      { ja: "研究の裏付け", en: "Study-backed" },
    q_reviewed:   { ja: "監修済み", en: "Reviewed" },
    contributions:{ ja: "提供した知恵", en: "Contributions" },
    tipsReceived: { ja: "受け取った感謝（デモ）", en: "Thanks received (demo)" },
    expertBadge:  { ja: "専門家", en: "Expert" },
    viewProfile:  { ja: "プロフィールを見る →", en: "View profile →" },
    related:      { ja: "関連する知恵", en: "Related tips" },
    itemsUnit:    { ja: "件", en: "" },
    watchVideo:   { ja: "動画で見る", en: "Watch on video" },
    searchYT:     { ja: "YouTubeで探す", en: "Search YouTube" },
    searchTT:     { ja: "TikTokで探す", en: "Search TikTok" },
    videoNote:    { ja: "外部サイト（YouTube / TikTok）が新しいタブで開きます。",
                    en: "Opens YouTube / TikTok in a new tab." }
  };
  function t(key) { return (STR[key] && STR[key][state.lang]) || key; }
  function L(obj) { if (!obj) return ""; return obj[state.lang] || obj.ja || obj.en || ""; }

  // ─────────────────────────────────────────────
  // ランキングの核：効くスコア（CONCEPT.md §4 をコード化）
  //
  //  score = 100 * (0.55*W + 0.25*E + 0.15*S + 0.05*P)
  //   W: 体感「効いた」率の Wilson 下限（少数票に強い）
  //   E: 科学的根拠の重み
  //   S: 専門家監修の重み
  //   P: 試した人数（reach）を log で強く減衰 → 人気だけでは上位に行けない
  //
  //  ねらい: バズ（再生数）と「本当に効く」を分離する。
  //          人気(P)の重みは僅か0.05。再生数が多くても体感率や根拠が低ければ沈む。
  // ─────────────────────────────────────────────
  var EVIDENCE_W = { none: 0.10, anecdotal: 0.35, expert: 0.70, study: 1.00 };
  var REVIEW_W   = { unreviewed: 0.30, expert: 1.00 };

  function wilsonLowerBound(pos, neg) {
    var n = pos + neg;
    if (n === 0) return 0;
    var z = 1.96, phat = pos / n;
    return (phat + z * z / (2 * n) - z * Math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n);
  }

  // ユーザー自身の評価をシード集計に合算（個人の声も全体に効く）
  function effectiveStats(c) {
    var u = state.user[c.id];
    var tried = c.stats.tried + (u && u.tried ? 1 : 0);
    var resonated = c.stats.resonated + (u && u.feedback === "resonated" ? 1 : 0);
    var notHelpful = c.stats.notHelpful + (u && u.feedback === "not_now" ? 1 : 0);
    return { tried: tried, resonated: resonated, notHelpful: notHelpful };
  }

  function scoreOf(c) {
    var s = effectiveStats(c);
    var W = wilsonLowerBound(s.resonated, s.notHelpful);
    var E = EVIDENCE_W[c.evidence.level] != null ? EVIDENCE_W[c.evidence.level] : 0.1;
    var S = REVIEW_W[c.review.status] != null ? REVIEW_W[c.review.status] : 0.3;
    var P = Math.min(1, Math.log10(s.tried + 1) / 4); // 1万試行で約1.0
    return Math.round(100 * (0.55 * W + 0.25 * E + 0.15 * S + 0.05 * P));
  }
  function feltRate(c) {
    var s = effectiveStats(c);
    var n = s.resonated + s.notHelpful;
    return n === 0 ? 0 : Math.round((s.resonated / n) * 100);
  }

  // 横断フィルタの状態（検索語はハッシュに載せず、ジャンル/タグに重ねられる）
  var searchQuery = "";
  var currentFilter = { genre: null, tag: null };

  // 全タグを出現頻度順で集計（タグ横断のための一覧）
  function allTags() {
    var counts = {};
    DATA.contents.forEach(function (c) {
      (c.tags || []).forEach(function (tag) { counts[tag] = (counts[tag] || 0) + 1; });
    });
    return Object.keys(counts).map(function (k) { return { tag: k, count: counts[k] }; })
      .sort(function (a, b) { return b.count - a.count || a.tag.localeCompare(b.tag); });
  }

  // 信頼性（科学的根拠／監修）で絞る
  function passQuality(c) {
    switch (state.quality) {
      case "study":    return c.evidence.level === "study";
      case "expert":   return c.evidence.level === "expert" || c.evidence.level === "study";
      case "reviewed": return c.review.status === "expert";
      default:         return true;
    }
  }

  // 現在のフィルタ＋検索語に一致するコンテンツ（スコア順）
  function matchedContents() {
    var list = DATA.contents.slice();
    if (currentFilter.genre) list = list.filter(function (c) { return c.genreId === currentFilter.genre; });
    if (currentFilter.tag) list = list.filter(function (c) { return (c.tags || []).indexOf(currentFilter.tag) >= 0; });
    if (state.quality !== "all") list = list.filter(passQuality);
    var q = searchQuery.trim().toLowerCase();
    if (q) {
      list = list.filter(function (c) {
        var hay = [c.title.ja, c.title.en, c.summary.ja, c.summary.en].concat(c.tags || []).join(" ").toLowerCase();
        return hay.indexOf(q) >= 0;
      });
    }
    return list.sort(function (a, b) { return scoreOf(b) - scoreOf(a); });
  }

  // ── ルーティング（#/ , #/g/<genre> , #/t/<tag> , #/c/<id>） ──
  function route() {
    var h = location.hash.replace(/^#\/?/, "");
    var parts = h.split("/");
    if (parts[0] === "c" && parts[1]) return renderDetail(decodeURIComponent(parts[1]));
    if (parts[0] === "u" && parts[1]) return renderContributor(decodeURIComponent(parts[1]));
    if (parts[0] === "g" && parts[1]) { currentFilter = { genre: parts[1], tag: null }; return renderHome(); }
    if (parts[0] === "t" && parts[1]) { currentFilter = { genre: null, tag: decodeURIComponent(parts[1]) }; return renderHome(); }
    currentFilter = { genre: null, tag: null };
    return renderHome();
  }

  // ── 描画ヘルパ ──
  var app = document.getElementById("app");
  function el(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
  function esc(str) { return String(str).replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }
  function genreById(id) { return DATA.genres.filter(function (g) { return g.id === id; })[0]; }
  function contributorById(id) { return DATA.contributors.filter(function (g) { return g.id === id; })[0]; }
  function evidenceClass(lv) { return "ev-" + lv; }

  function header() {
    var langBtn = '<button class="lang" id="langToggle">' + (state.lang === "ja" ? "EN" : "日本語") + "</button>";
    return '' +
      '<header class="topbar">' +
        '<a class="brand" href="#/">' +
          '<span class="brand-mark">効</span>' +
          '<span class="brand-text"><b>' + esc(t("brand")) + '</b><small>' + esc(t("tagline")) + "</small></span>" +
        "</a>" + langBtn +
      "</header>";
  }

  function evidencePill(c) {
    return '<span class="pill ' + evidenceClass(c.evidence.level) + '" title="' + esc(L(c.evidence.note)) + '">' +
      "🔬 " + esc(t("ev_" + c.evidence.level)) + "</span>";
  }
  function reviewPill(c) {
    var cls = c.review.status === "expert" ? "rv-expert" : "rv-unreviewed";
    return '<span class="pill ' + cls + '">' + (c.review.status === "expert" ? "✔ " : "○ ") + esc(t("rv_" + c.review.status)) + "</span>";
  }

  // ── ホーム / ランキング（検索＋ジャンル＋タグ横断） ──
  function renderHome() {
    var activeGenre = currentFilter.genre, activeTag = currentFilter.tag;

    var genreChips = '<a class="chip ' + (!activeGenre ? "on" : "") + '" href="#/">' + esc(t("all")) + "</a>" +
      DATA.genres.map(function (g) {
        return '<a class="chip ' + (activeGenre === g.id ? "on" : "") + '" href="#/g/' + g.id + '" style="--c:' + g.color + '">' +
          g.icon + " " + esc(L(g.name)) + "</a>";
      }).join("");

    var tagChips = allTags().map(function (o) {
      var on = activeTag === o.tag ? "on" : "";
      return '<a class="chip tagchip ' + on + '" href="#/t/' + encodeURIComponent(o.tag) + '"># ' +
        esc(o.tag) + ' <i>' + o.count + "</i></a>";
    }).join("");

    app.innerHTML = "";
    app.appendChild(el(header()));
    app.appendChild(el(
      '<main class="wrap">' +
        // 検索ボックス
        '<div class="searchbar">' +
          '<span class="si">🔍</span>' +
          '<input id="kikuSearch" type="search" placeholder="' + esc(t("searchPh")) + '" value="' + esc(searchQuery) + '" autocomplete="off">' +
          '<button id="kikuSearchClear" class="sclear" aria-label="clear">×</button>' +
        "</div>" +
        '<div class="chips">' + genreChips + "</div>" +
        // 信頼性フィルタ（科学的根拠／監修で絞る）
        '<div class="taglabel">' + esc(t("qualityLabel")) + "</div>" +
        '<div class="seg" id="kikuQuality">' +
          ["all", "expert", "study", "reviewed"].map(function (q) {
            return '<button class="segbtn ' + (state.quality === q ? "on" : "") + '" data-q="' + q + '">' +
              esc(t("q_" + q)) + "</button>";
          }).join("") +
        "</div>" +
        '<div class="taglabel">' + esc(t("tagsLabel")) + "</div>" +
        '<div class="chips tagrow">' + tagChips + "</div>" +
        '<div class="listhead"><span>' + esc(t("rankedBy")) + '</span><b id="kikuCount"></b></div>' +
        '<ol class="list" id="kikuList"></ol>' +
        '<p class="disclaimer">⚠ ' + esc(t("notMedical")) + "</p>" +
      "</main>"
    ));

    bindLang();
    bindSearch();
    bindQuality();
    fillList();
    window.scrollTo(0, 0);
  }

  // 信頼性フィルタ: クリックで切替・永続化。リストとボタンのみ更新（検索フォーカス維持）
  function bindQuality() {
    var seg = document.getElementById("kikuQuality");
    if (!seg) return;
    Array.prototype.forEach.call(seg.querySelectorAll("[data-q]"), function (btn) {
      btn.onclick = function () {
        state.quality = btn.getAttribute("data-q");
        save();
        Array.prototype.forEach.call(seg.querySelectorAll("[data-q]"), function (b) {
          b.classList.toggle("on", b.getAttribute("data-q") === state.quality);
        });
        fillList();
      };
    });
  }

  // リストだけを再描画（検索入力中にフォーカスを保つため、入力欄は作り直さない）
  function fillList() {
    var list = matchedContents();
    var ol = document.getElementById("kikuList");
    var cnt = document.getElementById("kikuCount");
    if (cnt) cnt.textContent = list.length + t("results");
    if (!ol) return;
    ol.innerHTML = list.length ? list.map(function (c, i) { return rankCard(c, i + 1); }).join("") :
      '<p class="empty">' + esc(t("noResults")) + "</p>";
  }

  function bindSearch() {
    var input = document.getElementById("kikuSearch");
    var clear = document.getElementById("kikuSearchClear");
    if (input) input.oninput = function () { searchQuery = input.value; fillList(); };
    if (clear) clear.onclick = function () { searchQuery = ""; if (input) { input.value = ""; input.focus(); } fillList(); };
  }

  function rankCard(c, rank) {
    var g = genreById(c.genreId);
    var medal = rank <= 3 ? '<span class="medal m' + rank + '">' + rank + "</span>" :
      '<span class="medal">' + rank + "</span>";
    return '' +
      '<li class="card"><a href="#/c/' + c.id + '">' +
        medal +
        '<div class="card-body">' +
          '<div class="card-top">' +
            '<span class="gtag" style="--c:' + g.color + '">' + g.icon + " " + esc(L(g.name)) + "</span>" +
            '<span class="score"><b>' + scoreOf(c) + "</b><i>" + esc(t("kikuScore")) + "</i></span>" +
          "</div>" +
          '<h3>' + esc(L(c.title)) + "</h3>" +
          '<div class="metrics">' +
            '<span class="felt">👍 ' + feltRate(c) + "% <i>" + esc(t("feltRate")) + "</i></span>" +
            evidencePill(c) + reviewPill(c) +
          "</div>" +
        "</div>" +
      "</a></li>";
  }

  // ── 詳細 ──
  function renderDetail(id) {
    var c = DATA.contents.filter(function (x) { return x.id === id; })[0];
    if (!c) return renderHome(null);
    var g = genreById(c.genreId), au = contributorById(c.contributorId);
    var u = userOf(c.id);
    var s = effectiveStats(c);

    var stepsHtml = c.steps.map(function (st, i) {
      return '<li><span class="num">' + (i + 1) + "</span>" + esc(L(st)) + "</li>";
    }).join("");

    var feedbackBlock = u.feedback
      ? '<p class="fb-done">' + esc(t("thanks")) + "</p>"
      : '<div class="fb"><p>' + esc(t("askFeedback")) + "</p>" +
          '<button class="fb-yes" data-fb="resonated">👍 ' + esc(t("resonated")) + "</button>" +
          '<button class="fb-no" data-fb="not_now">🤔 ' + esc(t("notNow")) + "</button></div>";

    app.innerHTML = "";
    app.appendChild(el(header()));
    app.appendChild(el(
      '<main class="wrap detail">' +
        '<a class="back" href="' + (g ? "#/g/" + g.id : "#/") + '">' + esc(t("back")) + "</a>" +

        '<span class="gtag" style="--c:' + g.color + '">' + g.icon + " " + esc(L(g.name)) + "</span>" +
        "<h1>" + esc(L(c.title)) + "</h1>" +
        '<p class="lead">' + esc(L(c.summary)) + "</p>" +

        // タグ（クリックでジャンル横断）
        ((c.tags && c.tags.length) ?
          '<div class="dtags">' + c.tags.map(function (tag) {
            return '<a class="chip tagchip" href="#/t/' + encodeURIComponent(tag) + '"># ' + esc(tag) + "</a>";
          }).join("") + "</div>" : "") +

        // 効くスコアと内訳（透明性）
        '<section class="scorebox">' +
          '<div class="bigscore"><b>' + scoreOf(c) + '</b><i>' + esc(t("kikuScore")) + "</i></div>" +
          '<div class="breakdown">' +
            '<div class="bd"><span>' + esc(t("felt")) + '</span><b>👍 ' + feltRate(c) + "%</b><small>" +
              esc(t("reach")) + " " + s.tried.toLocaleString() + "</small></div>" +
            '<div class="bd"><span>' + esc(t("evidence")) + "</span>" + evidencePill(c) +
              '<small>' + esc(L(c.evidence.note)) + "</small></div>" +
            '<div class="bd"><span>' + esc(t("supervision")) + "</span>" + reviewPill(c) + "</div>" +
          "</div>" +
        "</section>" +

        // やり方
        '<section class="block"><h2>' + esc(t("steps")) + ' <small>· ' + c.minutes + 'min</small></h2>' +
          '<ol class="steps">' + stepsHtml + "</ol></section>" +

        // 注意（薬機法配慮）
        (L(c.caution) && L(c.caution) !== "—" ?
          '<section class="block caution"><h2>⚠ ' + esc(t("caution")) + "</h2><p>" + esc(L(c.caution)) + "</p></section>" : "") +

        // 動画で見る（公式埋め込み or 実検索リンク・再配信しない）
        '<section class="block"><h2>▶ ' + esc(t("watchVideo")) + "</h2>" +
          embedHtml(c) +
          '<div class="videobtns">' +
            '<a class="vbtn yt" href="' + youtubeSearch(c) + '" target="_blank" rel="noopener noreferrer">▶ ' + esc(t("searchYT")) + "</a>" +
            '<a class="vbtn tt" href="' + tiktokSearch(c) + '" target="_blank" rel="noopener noreferrer">♪ ' + esc(t("searchTT")) + "</a>" +
          "</div>" +
          '<p class="origin">' + esc(t("from")) + ": " + flag(c.origin) + '</p>' +
          '<small class="videonote">' + esc(t("videoNote")) + "</small>" +
        "</section>" +

        // 貢献者＋チップ
        '<section class="block contributor">' +
          (au ? '<a class="who wholink" href="#/u/' + au.id + '">' : '<div class="who">') +
            '<span class="avatar" style="background:' + (au ? au.color : "#888") + '">' +
            (au ? esc(au.name.slice(0, 1)) : "?") + "</span>" +
            "<div><b>" + esc(t("by")) + " " + (au ? esc(au.name) : "?") + (au && au.expert ? ' <span class="exp">✔</span>' : "") +
            "</b><small>" + (au ? esc(L(au.bio)) : "") + "</small>" +
            (au ? '<small class="profilelink">' + esc(t("viewProfile")) + "</small>" : "") +
            "</div>" + (au ? "</a>" : "</div>") +
          '<div class="tipbox"><p>' + esc(t("tipDesc")) + "</p>" +
            '<div class="tipbtns">' +
              [100, 300, 500].map(function (v) { return '<button class="tipbtn" data-tip="' + v + '">¥' + v + "</button>"; }).join("") +
            "</div>" +
            (u.tipped ? '<p class="tipped">¥' + u.tipped + " " + (au ? esc(au.name) : "") + esc(t("tipThanks")) + "</p>" : "") +
            '<small class="demo">' + esc(t("tipDemo")) + "</small>" +
          "</div>" +
        "</section>" +

        // やってみた → 体感フィードバック
        '<section class="block tryblock">' +
          '<button class="trybtn ' + (u.tried ? "done" : "") + '" id="tryBtn">' +
            (u.tried ? esc(t("didTryDone")) : esc(t("didTry"))) + "</button>" +
          (u.tried ? feedbackBlock : "") +
        "</section>" +

        // 関連する知恵
        (function () {
          var rel = relatedTo(c, 3);
          if (!rel.length) return "";
          return '<section class="block related"><h2>' + esc(t("related")) + "</h2>" +
            rel.map(miniCard).join("") + "</section>";
        })() +

        '<p class="disclaimer">⚠ ' + esc(t("notMedical")) + "</p>" +
      "</main>"
    ));

    bindLang();
    bindDetail(c);
    window.scrollTo(0, 0);
  }

  function flag(code) {
    var map = {
      JP: { ja: "🇯🇵 日本", en: "🇯🇵 Japan" }, CN: { ja: "🇨🇳 中国", en: "🇨🇳 China" },
      US: { ja: "🇺🇸 アメリカ", en: "🇺🇸 USA" }, FR: { ja: "🇫🇷 フランス", en: "🇫🇷 France" },
      KR: { ja: "🇰🇷 韓国", en: "🇰🇷 Korea" }, IN: { ja: "🇮🇳 インド", en: "🇮🇳 India" },
      TH: { ja: "🇹🇭 タイ", en: "🇹🇭 Thailand" }, IT: { ja: "🇮🇹 イタリア", en: "🇮🇹 Italy" }
    };
    return map[code] ? L(map[code]) : code;
  }

  // 貢献者ごとの集計
  function contentsByContributor(uid) {
    return DATA.contents.filter(function (c) { return c.contributorId === uid; })
      .sort(function (a, b) { return scoreOf(b) - scoreOf(a); });
  }
  function tipsReceivedBy(uid) {
    return contentsByContributor(uid).reduce(function (sum, c) {
      var u = state.user[c.id];
      return sum + (u && u.tipped ? u.tipped : 0);
    }, 0);
  }
  // 動画検索リンク（全件で“実際の動画”に飛べるようにする。リンクなので著作権も安全）
  // 検索語は UI 言語に依存させず常に日本語で組む（元コンテンツが日本語圏中心のため、
  // 英語UIで英語タイトルが混ざって的外れな結果になるのを防ぐ）。
  // c.videoKw があれば、その厳選キーワードを優先（項目ごとに命中精度を上げられる）。
  function videoQuery(c) {
    var kw = c.videoKw || (c.title.ja + " " + (c.tags && c.tags[0] ? c.tags[0] : "") + " やり方");
    return encodeURIComponent(kw.replace(/[（）()「」]/g, " ").replace(/\s+/g, " ").trim());
  }
  function youtubeSearch(c) { return "https://www.youtube.com/results?search_query=" + videoQuery(c); }
  function tiktokSearch(c) { return "https://www.tiktok.com/search?q=" + videoQuery(c); }
  // 公式埋め込み（許諾済み/公式埋め込み可能な動画IDがある場合のみ。再配信ではない）
  function embedHtml(c) {
    if (!c.video) return "";
    if (c.video.provider === "youtube" && c.video.id) {
      return '<div class="embed"><iframe src="https://www.youtube.com/embed/' + esc(c.video.id) +
        '" title="YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
    }
    return "";
  }

  // 関連する知恵（共有タグ数→スコアで上位。自分自身は除外）
  function relatedTo(c, n) {
    var tags = c.tags || [];
    return DATA.contents.filter(function (x) { return x.id !== c.id; })
      .map(function (x) {
        var shared = (x.tags || []).filter(function (tg) { return tags.indexOf(tg) >= 0; }).length;
        var sameGenre = x.genreId === c.genreId ? 1 : 0;
        return { c: x, rel: shared * 2 + sameGenre };
      })
      .filter(function (o) { return o.rel > 0; })
      .sort(function (a, b) { return b.rel - a.rel || scoreOf(b.c) - scoreOf(a.c); })
      .slice(0, n || 3).map(function (o) { return o.c; });
  }

  // コンパクトカード（関連・貢献者ページで使う）
  function miniCard(c) {
    var g = genreById(c.genreId);
    return '<a class="mini" href="#/c/' + c.id + '">' +
      '<span class="mini-score">' + scoreOf(c) + "</span>" +
      '<span class="mini-body">' +
        '<span class="gtag" style="--c:' + g.color + '">' + g.icon + " " + esc(L(g.name)) + "</span>" +
        '<span class="mini-title">' + esc(L(c.title)) + "</span>" +
        '<span class="mini-metrics">👍 ' + feltRate(c) + "% · " + esc(t("ev_" + c.evidence.level)) + "</span>" +
      "</span></a>";
  }

  // ── 貢献者ページ ──
  function renderContributor(uid) {
    var au = contributorById(uid);
    if (!au) return renderHome();
    var list = contentsByContributor(uid);
    var tips = tipsReceivedBy(uid);

    app.innerHTML = "";
    app.appendChild(el(header()));
    app.appendChild(el(
      '<main class="wrap detail">' +
        '<a class="back" href="#/">' + esc(t("back")) + "</a>" +

        '<section class="block profile">' +
          '<span class="avatar big" style="background:' + au.color + '">' + esc(au.name.slice(0, 1)) + "</span>" +
          '<div class="profile-info">' +
            "<h1>" + esc(au.name) + (au.expert ? ' <span class="exp-badge">✔ ' + esc(t("expertBadge")) + "</span>" : "") + "</h1>" +
            '<p class="profile-bio">' + esc(L(au.bio)) + "</p>" +
            '<p class="origin">' + esc(t("from")) + ": " + flag(au.origin) + "</p>" +
          "</div>" +
        "</section>" +

        '<div class="profile-stats">' +
          '<div class="pstat"><b>' + list.length + '</b><small>' + esc(t("contributions")) + "</small></div>" +
          '<div class="pstat"><b>¥' + tips.toLocaleString() + '</b><small>' + esc(t("tipsReceived")) + "</small></div>" +
        "</div>" +

        '<div class="listhead"><span>' + esc(t("contributions")) + '</span><b>' + list.length + esc(t("itemsUnit")) + "</b></div>" +
        '<div class="minilist">' + list.map(miniCard).join("") + "</div>" +

        '<p class="disclaimer">⚠ ' + esc(t("notMedical")) + "</p>" +
      "</main>"
    ));
    bindLang();
    window.scrollTo(0, 0);
  }

  // ── イベント束ね ──
  function bindLang() {
    var b = document.getElementById("langToggle");
    if (b) b.onclick = function () { state.lang = state.lang === "ja" ? "en" : "ja"; save(); route(); };
  }

  function bindDetail(c) {
    var u = userOf(c.id);

    var tryBtn = document.getElementById("tryBtn");
    if (tryBtn) tryBtn.onclick = function () { u.tried = true; save(); renderDetail(c.id); };

    Array.prototype.forEach.call(document.querySelectorAll("[data-fb]"), function (btn) {
      btn.onclick = function () { u.feedback = btn.getAttribute("data-fb"); save(); renderDetail(c.id); };
    });

    Array.prototype.forEach.call(document.querySelectorAll("[data-tip]"), function (btn) {
      btn.onclick = function () {
        u.tipped = (u.tipped || 0) + parseInt(btn.getAttribute("data-tip"), 10);
        save(); renderDetail(c.id);
      };
    });
  }

  window.addEventListener("hashchange", route);
  route();
})();
