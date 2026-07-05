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
        // 並び替え（好みとして永続）: "score" | "felt" | "tried" | "min"
        sort: s.sort || "score",
        // 保存（ブックマーク）: contentId -> true
        saved: s.saved || {},
        // contentId -> { tried:bool, feedback:"resonated"|"not_now"|null, tipped:int }
        user: s.user || {}
      };
    } catch (e) {
      return { lang: "ja", quality: "all", sort: "score", saved: {}, user: {} };
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
    heroSub:      { ja: "体感・科学的根拠・専門家監修で評価。“バズ”ではなく“効く”を。",
                    en: "Rated by experience, evidence & expert review — not by hype." },
    statTips:     { ja: "の知恵", en: "tips" },
    statGenres:   { ja: "ジャンル", en: "genres" },
    statCountries:{ ja: "カ国から発掘", en: "countries" },
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
    scoreAbout:   { ja: "効くスコアとは？", en: "About the Kiku Score" },
    scoreTitle:   { ja: "効くスコアとは", en: "What is the Kiku Score?" },
    watchVideo:   { ja: "動画で見る", en: "Watch on video" },
    searchYT:     { ja: "YouTubeで探す", en: "Search YouTube" },
    searchTT:     { ja: "TikTokで探す", en: "Search TikTok" },
    videoNote:    { ja: "外部サイト（YouTube / TikTok）が新しいタブで開きます。",
                    en: "Opens YouTube / TikTok in a new tab." },
    sortLabel:    { ja: "並び替え", en: "Sort by" },
    sort_score:   { ja: "効くスコア", en: "Kiku Score" },
    sort_felt:    { ja: "効いた率", en: "Worked %" },
    sort_tried:   { ja: "人気", en: "Popular" },
    sort_min:     { ja: "時短", en: "Quick" },
    daily:        { ja: "今日の知恵", en: "Tip of the day" },
    saveTip:      { ja: "☆ 保存", en: "☆ Save" },
    savedTip:     { ja: "★ 保存済み", en: "★ Saved" },
    share:        { ja: "シェア", en: "Share" },
    linkCopied:   { ja: "✓ リンクをコピーしました", en: "✓ Link copied" },
    savedFilter:  { ja: "保存済み", en: "Saved" },
    noSaved:      { ja: "保存した知恵はまだありません。カードの ☆ で保存できます。",
                    en: "No saved tips yet. Tap ☆ on a card to save one." }
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
  var savedOnly = false; // ★保存済みだけ表示（セッション内のみ）

  // ── 保存（ブックマーク） ──
  function isSaved(id) { return !!state.saved[id]; }
  function toggleSave(id) {
    if (state.saved[id]) delete state.saved[id]; else state.saved[id] = true;
    save();
  }
  function savedCount() { return Object.keys(state.saved).length; }

  // ── 今日の知恵（日付シードで日替わり） ──
  function dailyPick() {
    var d = new Date();
    var seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    return DATA.contents[seed % DATA.contents.length];
  }

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
    if (savedOnly) list = list.filter(function (c) { return isSaved(c.id); });
    var q = searchQuery.trim().toLowerCase();
    if (q) {
      list = list.filter(function (c) {
        var hay = [c.title.ja, c.title.en, c.summary.ja, c.summary.en].concat(c.tags || []).join(" ").toLowerCase();
        return hay.indexOf(q) >= 0;
      });
    }
    // 並び替え（同点は効くスコアで安定させる）
    switch (state.sort) {
      case "felt":
        return list.sort(function (a, b) { return feltRate(b) - feltRate(a) || scoreOf(b) - scoreOf(a); });
      case "tried":
        return list.sort(function (a, b) { return effectiveStats(b).tried - effectiveStats(a).tried || scoreOf(b) - scoreOf(a); });
      case "min":
        return list.sort(function (a, b) { return a.minutes - b.minutes || scoreOf(b) - scoreOf(a); });
      default:
        return list.sort(function (a, b) { return scoreOf(b) - scoreOf(a); });
    }
  }

  // ── ルーティング（#/ , #/g/<genre> , #/t/<tag> , #/c/<id>） ──
  function route() {
    var h = location.hash.replace(/^#\/?/, "");
    var parts = h.split("/");
    if (parts[0] === "c" && parts[1]) return renderDetail(decodeURIComponent(parts[1]));
    if (parts[0] === "u" && parts[1]) return renderContributor(decodeURIComponent(parts[1]));
    if (parts[0] === "score") return renderScore();
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

  // ── ヒーロー（トップの世界観・数値カウントアップ） ──
  function heroHtml() {
    var tips = DATA.contents.length;
    var genres = DATA.genres.length;
    var countries = (function () { var s = {}; DATA.contents.forEach(function (c) { s[c.origin] = 1; }); return Object.keys(s).length; })();
    return '' +
      '<section class="hero" aria-label="Kiku">' +
        '<div class="hero-blobs" aria-hidden="true"><span></span><span></span><span></span></div>' +
        '<div class="hero-grid" aria-hidden="true"></div>' +
        '<div class="hero-inner">' +
          '<span class="hero-badge">効 · Kiku</span>' +
          '<h1 class="hero-title">' + esc(t("tagline")) + "</h1>" +
          '<p class="hero-sub">' + esc(t("heroSub")) + "</p>" +
          '<div class="hero-stats">' +
            '<div class="hstat"><b class="cup" data-to="' + tips + '">0</b><small>' + esc(t("statTips")) + "</small></div>" +
            '<div class="hstat"><b class="cup" data-to="' + genres + '">0</b><small>' + esc(t("statGenres")) + "</small></div>" +
            '<div class="hstat"><b class="cup" data-to="' + countries + '">0</b><small>' + esc(t("statCountries")) + "</small></div>" +
          "</div>" +
        "</div>" +
        '<svg class="hero-wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true">' +
          '<path d="M0,40 C240,90 480,0 720,30 C960,60 1200,90 1440,40 L1440,80 L0,80 Z"></path></svg>' +
      "</section>";
  }

  var prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 数値カウントアップ
  function runCountUps() {
    Array.prototype.forEach.call(document.querySelectorAll(".cup"), function (elm) {
      var to = parseInt(elm.getAttribute("data-to"), 10) || 0;
      if (prefersReduced) { elm.textContent = to; return; }
      var start = null, dur = 900;
      function step(ts) {
        if (start === null) start = ts;
        var p = Math.min(1, (ts - start) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        elm.textContent = Math.round(to * eased);
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  // 円形スコアリング（SVG）
  function scoreRing(score) {
    var r = 33, circ = 2 * Math.PI * r;
    var off = circ * (1 - Math.max(0, Math.min(100, score)) / 100);
    return '<svg class="ring" viewBox="0 0 80 80" aria-hidden="true">' +
      '<circle class="ring-bg" cx="40" cy="40" r="' + r + '"></circle>' +
      '<circle class="ring-fg" cx="40" cy="40" r="' + r + '" stroke-dasharray="' + circ.toFixed(1) +
        '" stroke-dashoffset="' + circ.toFixed(1) + '" data-off="' + off.toFixed(1) + '"></circle>' +
      "</svg>";
  }
  function animateRings() {
    Array.prototype.forEach.call(document.querySelectorAll(".ring-fg"), function (elm) {
      var off = elm.getAttribute("data-off");
      if (prefersReduced) { elm.style.strokeDashoffset = off; return; }
      requestAnimationFrame(function () { requestAnimationFrame(function () { elm.style.strokeDashoffset = off; }); });
    });
  }

  // ── 今日の知恵（日替わりカード） ──
  function dailyHtml() {
    var c = dailyPick();
    if (!c) return "";
    var g = genreById(c.genreId);
    return '<a class="daily" href="#/c/' + c.id + '">' +
      '<span class="daily-label">☀ ' + esc(t("daily")) + '</span>' +
      '<span class="daily-title">' + esc(L(c.title)) + '</span>' +
      '<span class="daily-meta">' +
        '<span class="gtag" style="--c:' + g.color + '">' + g.icon + " " + esc(L(g.name)) + '</span>' +
        '<span>' + esc(t("kikuScore")) + ' <b>' + scoreOf(c) + '</b></span>' +
        '<span>⏱ ' + c.minutes + 'min</span>' +
      '</span></a>';
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
    if (!activeGenre && !activeTag) app.appendChild(el(heroHtml()));
    app.appendChild(el(
      '<main class="wrap' + ((!activeGenre && !activeTag) ? " has-hero" : "") + '">' +
        // 今日の知恵（日替わりピックアップ・トップのみ）
        ((!activeGenre && !activeTag) ? dailyHtml() : "") +
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
        '<div class="taglabel">' + esc(t("sortLabel")) + "</div>" +
        '<div class="seg" id="kikuSort">' +
          ["score", "felt", "tried", "min"].map(function (q) {
            return '<button class="segbtn ' + (state.sort === q ? "on" : "") + '" data-sort="' + q + '">' +
              esc(t("sort_" + q)) + "</button>";
          }).join("") +
        "</div>" +
        '<div class="taglabel">' + esc(t("tagsLabel")) + "</div>" +
        '<div class="chips tagrow">' + tagChips + "</div>" +
        '<div class="listhead"><span>' + esc(t("rankedBy")) + '</span>' +
          '<a class="scorelink" href="#/score">ⓘ ' + esc(t("scoreAbout")) + '</a>' +
          '<button class="savedbtn' + (savedOnly ? " on" : "") + '" id="savedToggle" type="button">★ ' +
            esc(t("savedFilter")) + ' <i>' + savedCount() + '</i></button>' +
          '<b id="kikuCount"></b></div>' +
        '<ol class="list" id="kikuList"></ol>' +
        '<p class="disclaimer">⚠ ' + esc(t("notMedical")) + "</p>" +
      "</main>"
    ));

    bindLang();
    bindSearch();
    bindQuality();
    bindSort();
    bindSavedToggle();
    fillList();
    runCountUps();
    window.scrollTo(0, 0);
  }

  // 並び替え: クリックで切替・永続化（検索フォーカス維持のためリストのみ更新）
  function bindSort() {
    var seg = document.getElementById("kikuSort");
    if (!seg) return;
    Array.prototype.forEach.call(seg.querySelectorAll("[data-sort]"), function (btn) {
      btn.onclick = function () {
        state.sort = btn.getAttribute("data-sort");
        save();
        Array.prototype.forEach.call(seg.querySelectorAll("[data-sort]"), function (b) {
          b.classList.toggle("on", b.getAttribute("data-sort") === state.sort);
        });
        fillList();
      };
    });
  }

  // ★保存済みだけ表示のトグル
  function bindSavedToggle() {
    var btn = document.getElementById("savedToggle");
    if (!btn) return;
    btn.onclick = function () {
      savedOnly = !savedOnly;
      btn.classList.toggle("on", savedOnly);
      fillList();
    };
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
      '<p class="empty">' + esc(t(savedOnly ? "noSaved" : "noResults")) + "</p>";
    // カード上の☆保存（リンク遷移を止めてトグル）
    Array.prototype.forEach.call(ol.querySelectorAll("[data-save]"), function (btn) {
      btn.onclick = function (e) {
        e.preventDefault();
        e.stopPropagation();
        var id = btn.getAttribute("data-save");
        toggleSave(id);
        btn.classList.toggle("on", isSaved(id));
        btn.textContent = isSaved(id) ? "★" : "☆";
        var tgl = document.getElementById("savedToggle");
        if (tgl) tgl.innerHTML = "★ " + esc(t("savedFilter")) + " <i>" + savedCount() + "</i>";
        if (savedOnly) fillList();
      };
    });
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
            '<button class="starbtn' + (isSaved(c.id) ? " on" : "") + '" type="button" data-save="' + c.id +
              '" aria-label="save">' + (isSaved(c.id) ? "★" : "☆") + "</button>" +
            '<span class="score"><b>' + scoreOf(c) + "</b><i>" + esc(t("kikuScore")) + "</i></span>" +
          "</div>" +
          '<h3>' + esc(L(c.title)) + "</h3>" +
          '<div class="metrics">' +
            '<span class="felt">👍 ' + feltRate(c) + "% <i>" + esc(t("feltRate")) + "</i></span>" +
            '<span class="pill mins">⏱ ' + c.minutes + "min</span>" +
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

        // 保存・シェア
        '<div class="actions">' +
          '<button class="actbtn' + (isSaved(c.id) ? " on" : "") + '" id="saveBtn" type="button">' +
            esc(t(isSaved(c.id) ? "savedTip" : "saveTip")) + "</button>" +
          '<button class="actbtn" id="shareBtn" type="button">↗ ' + esc(t("share")) + "</button>" +
        "</div>" +

        // タグ（クリックでジャンル横断）
        ((c.tags && c.tags.length) ?
          '<div class="dtags">' + c.tags.map(function (tag) {
            return '<a class="chip tagchip" href="#/t/' + encodeURIComponent(tag) + '"># ' + esc(tag) + "</a>";
          }).join("") + "</div>" : "") +

        // 効くスコアと内訳（透明性）
        '<section class="scorebox">' +
          '<a class="bigscore" href="#/score" title="' + esc(t("scoreAbout")) + '">' +
            scoreRing(scoreOf(c)) +
            '<span class="bs-num"><b>' + scoreOf(c) + '</b><i>' + esc(t("kikuScore")) + '</i><em>ⓘ</em></span></a>' +
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
    animateRings();
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
  // 公式埋め込み（公式の埋め込みプレーヤーを iframe 表示。動画の再配信ではない）
  // video: { youtube: "<id>", tiktok: "<id>", provider/ id (旧形式も可) }
  function embedHtml(c) {
    if (!c.video) return "";
    var v = c.video, out = "";
    var yt = v.youtube || (v.provider === "youtube" ? v.id : null);
    if (yt) {
      out += '<div class="embed"><iframe src="https://www.youtube.com/embed/' + esc(yt) +
        '" title="YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>';
    }
    if (v.tiktok) {
      out += '<div class="embed embed-vertical"><iframe src="https://www.tiktok.com/player/v1/' + esc(v.tiktok) +
        '" title="TikTok" frameborder="0" allow="encrypted-media; fullscreen" allowfullscreen></iframe></div>';
    }
    return out;
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

  // ── 効くスコアの基準ページ ──
  function renderScore() {
    var evRows = [
      ["study", EVIDENCE_W.study], ["expert", EVIDENCE_W.expert],
      ["anecdotal", EVIDENCE_W.anecdotal], ["none", EVIDENCE_W.none]
    ].map(function (r) {
      return "<tr><td>" + esc(t("ev_" + r[0])) + "</td><td>" + r[1].toFixed(2) + "</td></tr>";
    }).join("");
    var rvRows = [
      ["expert", REVIEW_W.expert], ["unreviewed", REVIEW_W.unreviewed]
    ].map(function (r) {
      return "<tr><td>" + esc(t("rv_" + r[0])) + "</td><td>" + r[1].toFixed(2) + "</td></tr>";
    }).join("");

    app.innerHTML = "";
    app.appendChild(el(header()));
    app.appendChild(el(
      '<main class="wrap detail">' +
        '<a class="back" href="#/">' + esc(t("back")) + "</a>" +
        "<h1>" + esc(t("scoreTitle")) + "</h1>" +
        '<p class="lead">' + esc(L({
          ja: "「バズ（再生数）」ではなく「本当に効くか」を表すための、透明なスコア（0〜100）です。次の4つの要素を重みづけして合算します。",
          en: "A transparent 0–100 score that reflects whether a tip actually works — not how viral it is. It combines four weighted factors."
        })) + "</p>" +

        '<section class="block"><h2>' + esc(L({ ja: "計算式", en: "Formula" })) + "</h2>" +
          '<p class="formula">' + esc(L({
            ja: "スコア = 100 ×（0.55×体感 ＋ 0.25×科学的根拠 ＋ 0.15×専門家監修 ＋ 0.05×人気）",
            en: "Score = 100 × (0.55×Experience + 0.25×Evidence + 0.15×Review + 0.05×Popularity)"
          })) + "</p></section>" +

        '<section class="block"><h2>' + esc(L({ ja: "4つの要素", en: "The four factors" })) + "</h2>" +
          '<div class="factor"><b>① ' + esc(t("felt")) + ' <span class="w">55%</span></b><p>' + esc(L({
            ja: "「効いた」と答えた割合。少数の票でも荒れにくいよう Wilson 下限で慎重に評価します。",
            en: "The share of people who said it worked — evaluated with a Wilson lower bound so few votes don't inflate it."
          })) + "</p></div>" +
          '<div class="factor"><b>② ' + esc(t("evidence")) + ' <span class="w">25%</span></b><p>' + esc(L({
            ja: "科学的根拠の度合い。4段階で重みづけします。",
            en: "The degree of scientific evidence, weighted in four levels."
          })) + '</p><table class="wtab">' + evRows + "</table></div>" +
          '<div class="factor"><b>③ ' + esc(t("supervision")) + ' <span class="w">15%</span></b><p>' + esc(L({
            ja: "専門家の監修があるか。",
            en: "Whether an expert has reviewed it."
          })) + '</p><table class="wtab">' + rvRows + "</table></div>" +
          '<div class="factor"><b>④ ' + esc(L({ ja: "人気", en: "Popularity" })) + ' <span class="w">5%</span></b><p>' + esc(L({
            ja: "試した人数。重みを意図的にごく小さく（5%）し、対数で伸びを抑えています。",
            en: "How many people tried it — deliberately tiny (5%) and log-dampened."
          })) + "</p></div>" +
        "</section>" +

        '<section class="block caution"><h2>💡 ' + esc(L({ ja: "この設計のねらい", en: "Why it's built this way" })) + "</h2><p>" + esc(L({
          ja: "人気（再生数）の重みはわずか5%。だから再生数が多くても、体感率や根拠・監修が低い動画は上位に来ません。「バズ」と「本当に効く」を分けるのが目的です。",
          en: "Popularity counts for only 5%. So a viral video with low experience, evidence, or review will not rank high. The goal is to separate 'viral' from 'actually works'."
        })) + "</p></section>" +

        '<p class="disclaimer">⚠ ' + esc(L({
          ja: "効くスコアは医療的な有効性の保証ではありません。体感と根拠を分けて分かりやすく示すための目安です。",
          en: "The Kiku Score is not a guarantee of medical effectiveness. It is a guide that separates experience from evidence."
        })) + "</p>" +
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

    // ☆保存（画面遷移せずボタンだけ更新）
    var saveBtn = document.getElementById("saveBtn");
    if (saveBtn) saveBtn.onclick = function () {
      toggleSave(c.id);
      saveBtn.classList.toggle("on", isSaved(c.id));
      saveBtn.textContent = t(isSaved(c.id) ? "savedTip" : "saveTip");
    };

    // シェア（Web Share API。非対応環境はリンクをコピー）
    var shareBtn = document.getElementById("shareBtn");
    if (shareBtn) shareBtn.onclick = function () {
      var payload = { title: L(c.title), text: L(c.summary), url: location.href };
      if (navigator.share) {
        navigator.share(payload).catch(function () {});
      } else if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(location.href).then(function () {
          shareBtn.textContent = t("linkCopied");
          setTimeout(function () { shareBtn.textContent = "↗ " + t("share"); }, 1800);
        });
      }
    };

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
