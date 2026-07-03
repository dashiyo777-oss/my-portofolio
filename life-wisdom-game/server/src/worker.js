/**
 * 叡智の灯火 — 会員API (Cloudflare Worker / ES Module)
 * P1: /api/redeem (コード→JWT) と /api/content (Bearer→有料データ)
 *  - コード検証は CODE_SECRET でサーバー側生成（クライアントに式を置かない）
 *  - JWT は HS256 / 当月末まで有効
 *  - 有料データは D1 (content テーブル) からのみ返す＝丸コピー防止
 * 必要バインディング: env.DB (D1), env.JWT_SECRET, env.CODE_SECRET, env.ALLOW_ORIGIN
 */

const enc = new TextEncoder();

function b64url(buf) {
  let s = btoa(String.fromCharCode.apply(null, new Uint8Array(buf)));
  return s.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function b64urlStr(str) { return b64url(enc.encode(str)); }
function b64urlDecode(s) { return atob(s.replace(/-/g, "+").replace(/_/g, "/")); }

async function hmacRaw(secret, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return await crypto.subtle.sign("HMAC", key, enc.encode(msg));
}
async function hmacHex(secret, msg) {
  const sig = await hmacRaw(secret, msg);
  return Array.from(new Uint8Array(sig)).map(function (b) { return b.toString(16).padStart(2, "0"); }).join("");
}

export async function signJWT(payload, secret) {
  const header = { alg: "HS256", typ: "JWT" };
  const data = b64urlStr(JSON.stringify(header)) + "." + b64urlStr(JSON.stringify(payload));
  const sig = b64url(await hmacRaw(secret, data));
  return data + "." + sig;
}
export async function verifyJWT(token, secret) {
  const parts = (token || "").split(".");
  if (parts.length !== 3) return null;
  const data = parts[0] + "." + parts[1];
  const expected = b64url(await hmacRaw(secret, data));
  if (expected !== parts[2]) return null;
  let payload;
  try { payload = JSON.parse(b64urlDecode(parts[1])); } catch (e) { return null; }
  if (payload.exp && Math.floor(Date.now() / 1000) > payload.exp) return null;
  return payload;
}

export function monthKey(d) { return d.getUTCFullYear() * 100 + (d.getUTCMonth() + 1); }
function monthEndExp(d) { return Math.floor(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 1, 0, 0, 0) / 1000); }
export async function expectedCode(mk, secret) {
  const h = await hmacHex(secret, "code:" + mk);
  const n = (parseInt(h.slice(0, 8), 16) % 9000) + 1000;
  return "TOMO-" + n;
}

function cors(env, request) {
  const allow = (env && env.ALLOW_ORIGIN) || "*";
  let origin = "*";
  if (allow !== "*") {
    const list = allow.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    const reqOrigin = request && request.headers.get("Origin");
    origin = (reqOrigin && list.indexOf(reqOrigin) >= 0) ? reqOrigin : (list[0] || "*");
  }
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Authorization,Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin"
  };
}
function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ "Content-Type": "application/json; charset=utf-8" }, headers || {}) });
}

async function loadType(env, type) {
  const rs = await env.DB.prepare("SELECT payload FROM content WHERE type=?").bind(type).all();
  return (rs.results || []).map(function (r) { try { return JSON.parse(r.payload); } catch (e) { return null; } }).filter(Boolean);
}

// 簡易レート制限（IP×バケット）。limit回/windowSec を超えたら true。
async function limited(env, ip, bucket, limit, windowSec) {
  if (!env.DB || !ip) return false;
  const now = Date.now();
  try {
    const rs = await env.DB.prepare("SELECT COUNT(*) AS c FROM rl WHERE ip=? AND bucket=? AND ts > ?")
      .bind(ip, bucket, now - windowSec * 1000).all();
    const c = (rs.results && rs.results[0] && rs.results[0].c) || 0;
    if (c >= limit) return true;
    await env.DB.prepare("INSERT INTO rl (ip,bucket,ts) VALUES (?,?,?)").bind(ip, bucket, now).run();
    if (Math.random() < 0.02) { try { await env.DB.prepare("DELETE FROM rl WHERE ts < ?").bind(now - 3600 * 1000).run(); } catch (e) {} }
  } catch (e) {}
  return false;
}
async function fingerprint(token) {
  const h = await hmacHex("lic", token || "");
  return h.slice(0, 12);
}

// ───────────────────────────────────────────────────────────────
// 静的サイト計測ハブ（議員ランキング等）。1x1 GIF ビーコンで hits に記録。
// 計測したいサイトをここに登録すると、ダッシュボード/日次レポートに自動で出る。
const SITES = {
  politicians: { label: "議員ランキング", emoji: "🏛" },
  sage_free: { label: "賢人会議（無料）", emoji: "🧙" },
  sage_member: { label: "賢人会議（会員）", emoji: "🧙" }
};

// 賢人会議（AI対話プロキシ）の設定。会員は無制限、非会員はIP×窓で無料枠のみ。
const SAGE_MODEL = "claude-sonnet-4-6";
const SAGE_MAX_TOKENS = 1000;
const SAGE_FREE_LIMIT = 20;              // 非会員の無料呼び出し回数（IP×窓）
const SAGE_FREE_WINDOW = 7 * 24 * 3600;  // 集計窓（秒）= 7日

let _hitsReady = false;
async function ensureHits(env) {
  if (_hitsReady || !env.DB) return;
  try {
    await env.DB.prepare("CREATE TABLE IF NOT EXISTS hits (site TEXT, ts INTEGER, ip TEXT, ref TEXT)").run();
    try { await env.DB.prepare("CREATE INDEX IF NOT EXISTS idx_hits_site_ts ON hits (site, ts)").run(); } catch (e) {}
    _hitsReady = true;
  } catch (e) {}
}
// 1x1 透明GIF（ビーコン応答用）。
const GIF1x1 = Uint8Array.from([0x47,0x49,0x46,0x38,0x39,0x61,0x01,0x00,0x01,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0xff,0xff,0xff,0x21,0xf9,0x04,0x01,0x00,0x00,0x00,0x00,0x2c,0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0x02,0x02,0x44,0x01,0x00,0x3b]);
function gif1x1(h) {
  return new Response(GIF1x1, { status: 200, headers: Object.assign({}, h || {}, {
    "Content-Type": "image/gif",
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache"
  }) });
}
// 計測ビーコン: /api/hit?site=politicians&r=乱数  → hits に記録して 1x1 GIF を返す。
async function hit(request, env, h) {
  const url = new URL(request.url);
  const site = (url.searchParams.get("site") || "site").slice(0, 32).replace(/[^A-Za-z0-9_-]/g, "") || "site";
  await ensureHits(env);
  const ip = request.headers.get("CF-Connecting-IP") || "";
  // 同一IP×サイトは30分に1回だけ計上（ユニーク訪問の近似・ボット連打を抑制）
  const dup = await limited(env, ip, "hit:" + site, 1, 1800);
  if (!dup) {
    const ref = (request.headers.get("Referer") || "").slice(0, 300);
    try { await env.DB.prepare("INSERT INTO hits (site,ts,ip,ref) VALUES (?,?,?,?)").bind(site, Date.now(), ip, ref).run(); } catch (e) {}
  }
  return gif1x1(h);
}
// サイト単位のアクセス集計。
async function computeHits(env, site) {
  await ensureHits(env);
  const now = Date.now(), d1 = now - 86400000, d7 = now - 7 * 86400000;
  async function n(sql, binds) {
    try { var st = env.DB.prepare(sql); var rs = await st.bind.apply(st, binds).all(); return (rs.results && rs.results[0] && rs.results[0].c) || 0; } catch (e) { return -1; }
  }
  const total = await n("SELECT COUNT(*) AS c FROM hits WHERE site=?", [site]);
  const last24h = await n("SELECT COUNT(*) AS c FROM hits WHERE site=? AND ts > ?", [site, d1]);
  const last7d = await n("SELECT COUNT(*) AS c FROM hits WHERE site=? AND ts > ?", [site, d7]);
  const uniq24h = await n("SELECT COUNT(DISTINCT ip) AS c FROM hits WHERE site=? AND ts > ?", [site, d1]);
  return { site: site, total: total, last24h: last24h, last7d: last7d, uniq24h: uniq24h };
}
// サイト単位の日次推移（JST）。グラフ用。
async function computeHitSeries(env, site, days) {
  await ensureHits(env);
  const now = Date.now(), since = now - days * 86400000;
  const m = {};
  try {
    const rs = await env.DB.prepare("SELECT strftime('%Y-%m-%d', ts/1000, 'unixepoch', '+9 hours') AS d, COUNT(*) AS c FROM hits WHERE site=? AND ts > ? GROUP BY d").bind(site, since).all();
    (rs.results || []).forEach(function (r) { m[r.d] = r.c; });
  } catch (e) {}
  const labels = [], hits = [];
  for (var i = days - 1; i >= 0; i--) {
    var d = new Date(now - i * 86400000 + 9 * 3600000).toISOString().slice(0, 10);
    labels.push(d.slice(5)); hits.push(m[d] || 0);
  }
  return { labels: labels, hits: hits };
}

async function redeem(request, env, h) {
  const ip = request.headers.get("CF-Connecting-IP") || "";
  if (await limited(env, ip, "redeem", 10, 60)) return json({ error: "rate_limited" }, 429, h);
  let body; try { body = await request.json(); } catch (e) { return json({ error: "bad_request" }, 400, h); }
  const code = (body && body.code ? String(body.code) : "").trim().toUpperCase();
  const mk = monthKey(new Date());
  const want = (await expectedCode(mk, env.CODE_SECRET)).toUpperCase();
  if (!code || code !== want) return json({ error: "invalid_code" }, 401, h);
  const exp = monthEndExp(new Date());
  const token = await signJWT({ m: mk, exp: exp }, env.JWT_SECRET);
  return json({ token: token, exp: exp, month: mk }, 200, h);
}

// Gumroad ライセンス検証（海外課金）。env.GUMROAD_PRODUCT_ID か GUMROAD_PRODUCT_PERMALINK が必要。
async function gumroadVerify(env, license) {
  const params = new URLSearchParams();
  if (env.GUMROAD_PRODUCT_ID) params.set("product_id", env.GUMROAD_PRODUCT_ID);
  else if (env.GUMROAD_PRODUCT_PERMALINK) params.set("product_permalink", env.GUMROAD_PRODUCT_PERMALINK);
  params.set("license_key", license);
  params.set("increment_uses_count", "false");
  const r = await fetch("https://api.gumroad.com/v2/licenses/verify", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString()
  });
  if (!r.ok) return null;
  return await r.json();
}
function licenseActive(data) {
  if (!data || data.success !== true) return false;
  const p = data.purchase || {};
  if (p.refunded || p.chargebacked || p.disputed) return false;
  // サブスク商品なら、終了/解約/支払い失敗が入っていないこと
  if (p.subscription_ended_at || p.subscription_cancelled_at || p.subscription_failed_at) return false;
  return true;
}
async function redeemLicense(request, env, h) {
  const ip = request.headers.get("CF-Connecting-IP") || "";
  if (await limited(env, ip, "lic", 10, 60)) return json({ error: "rate_limited" }, 429, h);
  if (!env.GUMROAD_PRODUCT_ID && !env.GUMROAD_PRODUCT_PERMALINK) return json({ error: "not_configured" }, 503, h);
  let body; try { body = await request.json(); } catch (e) { return json({ error: "bad_request" }, 400, h); }
  const license = (body && body.license ? String(body.license) : "").trim();
  if (!license) return json({ error: "bad_request" }, 400, h);
  let data; try { data = await gumroadVerify(env, license); } catch (e) { data = null; }
  if (!licenseActive(data)) return json({ error: "invalid_license" }, 401, h);
  const mk = monthKey(new Date());
  const exp = monthEndExp(new Date());
  const token = await signJWT({ m: mk, exp: exp, src: "gum" }, env.JWT_SECRET);
  try {
    const lic = await fingerprint(license);
    await env.DB.prepare("INSERT INTO deliveries (ts,lic,ip) VALUES (?,?,?)").bind(Date.now(), lic, ip).run();
  } catch (e) {}
  return json({ token: token, exp: exp, month: mk }, 200, h);
}

async function content(request, env, h) {
  const auth = request.headers.get("Authorization") || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  const payload = await verifyJWT(token, env.JWT_SECRET);
  if (!payload || payload.m !== monthKey(new Date())) return json({ error: "unauthorized" }, 401, h);
  const [sages, events, legends] = await Promise.all([loadType(env, "sage"), loadType(env, "event"), loadType(env, "legend")]);
  const lic = await fingerprint(token);
  try { await env.DB.prepare("INSERT INTO deliveries (ts,lic,ip) VALUES (?,?,?)").bind(Date.now(), lic, request.headers.get("CF-Connecting-IP") || "").run(); } catch (e) {}
  return json({ sages: sages, events: events, legends: legends, lic: lic }, 200, h);
}

async function feedback(request, env, h) {
  const ip = request.headers.get("CF-Connecting-IP") || "";
  if (await limited(env, ip, "fb", 120, 60)) return json({ ok: true, skipped: true }, 200, h);
  let b; try { b = await request.json(); } catch (e) { return json({ error: "bad_request" }, 400, h); }
  try {
    await env.DB.prepare("INSERT INTO feedback (ts,event_id,sage_id,mood,fb) VALUES (?,?,?,?,?)")
      .bind(Date.now(), String(b.eventId || ""), String(b.sageId || ""), String(b.mood || ""), String(b.fb || "")).run();
  } catch (e) {}
  return json({ ok: true }, 200, h);
}

// 「○%が響いた」集計（匿名・読み取り）。?key="eventId:sageId" or ?event=ID（イベント内の全偉人）
async function stats(request, env, h) {
  const url = new URL(request.url);
  const event = url.searchParams.get("event");
  if (event) {
    const rs = await env.DB.prepare("SELECT sage_id, fb, COUNT(*) AS c FROM feedback WHERE event_id=? GROUP BY sage_id, fb").bind(event).all();
    const m = {};
    (rs.results || []).forEach(function (r) { const s = m[r.sage_id] || (m[r.sage_id] = { resonated: 0, not_now: 0 }); if (r.fb === "resonated") s.resonated = r.c; else if (r.fb === "not_now") s.not_now = r.c; });
    const out = {};
    Object.keys(m).forEach(function (k) { const s = m[k], n = s.resonated + s.not_now; out[k] = { resonated: s.resonated, not_now: s.not_now, samples: n, resonateRate: n ? s.resonated / n : 0 }; });
    return json({ event: event, sages: out }, 200, h);
  }
  const key = url.searchParams.get("key") || "";
  const i = key.indexOf(":");
  if (i < 0) return json({ error: "bad_key" }, 400, h);
  const ev = key.slice(0, i), sg = key.slice(i + 1);
  const rs = await env.DB.prepare("SELECT fb, COUNT(*) AS c FROM feedback WHERE event_id=? AND sage_id=? GROUP BY fb").bind(ev, sg).all();
  let res = 0, not = 0;
  (rs.results || []).forEach(function (r) { if (r.fb === "resonated") res = r.c; else if (r.fb === "not_now") not = r.c; });
  const samples = res + not;
  return json({ key: key, resonated: res, not_now: not, samples: samples, resonateRate: samples ? res / samples : 0 }, 200, h);
}

// 日替わりの「今日の一言」（サーバー配信・日付で決定論的・聖典/原文除外）
let _dailyCache = {};
async function daily(request, env, h) {
  const lang = (new URL(request.url).searchParams.get("lang") === "en") ? "en" : "ja";
  const day = Math.floor(Date.now() / 86400000);
  const ck = day + ":" + lang;
  if (_dailyCache[ck]) return json(_dailyCache[ck], 200, h);
  const [events, sages] = await Promise.all([loadType(env, "event"), loadType(env, "sage")]);
  const nameOf = {}; sages.forEach(function (s) { nameOf[s.id] = (lang === "en" && s.nameEn) ? s.nameEn : s.name; });
  const pool = [];
  events.slice().sort(function (a, b) { return a.id < b.id ? -1 : 1; }).forEach(function (e) {
    (e.advices || []).forEach(function (a) {
      if (a.sageId === "original" || a.sageId.indexOf("scripture") === 0) return;
      pool.push({ eventId: e.id, sageId: a.sageId, sageName: nameOf[a.sageId] || a.sageId, source: a.source || "",
        quote: (lang === "en" ? (a.quoteEn || a.quoteOriginal || a.quote) : a.quote) });
    });
  });
  if (pool.length === 0) return json({ error: "empty" }, 404, h);
  const pick = pool[day % pool.length];
  _dailyCache = {}; _dailyCache[ck] = pick;
  return json(pick, 200, h);
}

// 運営者専用：今月（と来月）の会員コードを確認。?key=USAGE_KEY で保護。
async function adminCode(request, env) {
  const url = new URL(request.url);
  const key = url.searchParams.get("key") || "";
  if (!env.USAGE_KEY || key !== env.USAGE_KEY) return new Response("unauthorized", { status: 401 });
  if (!env.CODE_SECRET) return new Response("CODE_SECRET 未設定", { status: 503 });
  const now = new Date();
  const mkNow = monthKey(now);
  const nextDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1, 0, 0, 0));
  const mkNext = monthKey(nextDate);
  const codeNow = await expectedCode(mkNow, env.CODE_SECRET);
  const codeNext = await expectedCode(mkNext, env.CODE_SECRET);
  // 切り替えは「翌月1日の 00:00 UTC = 09:00 JST」。
  const switchJst = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1, 0, 0, 0) + 9 * 3600000).toISOString().slice(0, 16).replace("T", " ");
  function ym(mk) { return Math.floor(mk / 100) + "年" + (mk % 100) + "月"; }
  const html = '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1"><title>会員コード確認（運営者用）</title>' +
    '<style>body{font-family:system-ui,-apple-system,"Hiragino Sans",sans-serif;background:#f6efe2;color:#33291f;margin:0;padding:22px}' +
    '.wrap{max-width:560px;margin:0 auto}h1{font-size:1.15rem}.box{background:#fff;border:1px solid #e0d3bb;border-radius:14px;padding:16px;margin:12px 0}' +
    '.lbl{font-size:.8rem;color:#6b5d4a}.code{font-size:2rem;font-weight:700;color:#a9863f;letter-spacing:1px;margin:4px 0;user-select:all}' +
    '.now{border-color:#a9863f}.next{opacity:.85}.meta{font-size:.8rem;color:#6b5d4a;line-height:1.7}</style></head><body><div class="wrap">' +
    '<h1>🔑 会員コード確認（運営者用）</h1>' +
    '<div class="box now"><div class="lbl">いま有効なコード（' + ym(mkNow) + '）— これをnoteに貼る</div>' +
    '<div class="code">' + codeNow + '</div></div>' +
    '<div class="box next"><div class="lbl">次のコード（' + ym(mkNext) + '）— ' + switchJst + ' JST から有効</div>' +
    '<div class="code">' + codeNext + '</div></div>' +
    '<p class="meta">・コードは毎月「1日 09:00（JST）」に自動で切り替わります。<br>' +
    '・1日の朝9時を過ぎたら、上の「次のコード」が「いま有効」になります。忘れずにnoteを更新してください。<br>' +
    '・このページは合言葉付きURL。他人に共有しないでください。</p>' +
    '</div></body></html>';
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
}

// 利用状況の集計（D1から）。/api/usage と 日次レポートの両方で使う。
async function computeUsage(env) {
  const now = Date.now(), d1 = now - 86400000, d7 = now - 7 * 86400000;
  async function one(sql, binds) {
    try { var st = env.DB.prepare(sql); var rs = await (binds && binds.length ? st.bind.apply(st, binds) : st).all(); return (rs.results && rs.results[0]) || null; } catch (e) { return null; }
  }
  function c(row) { return row ? (row.c || 0) : -1; }
  const fbTotal = c(await one("SELECT COUNT(*) AS c FROM feedback"));
  const fb24 = c(await one("SELECT COUNT(*) AS c FROM feedback WHERE ts > ?", [d1]));
  const fb7 = c(await one("SELECT COUNT(*) AS c FROM feedback WHERE ts > ?", [d7]));
  const delTotal = c(await one("SELECT COUNT(*) AS c FROM deliveries"));
  const del24 = c(await one("SELECT COUNT(*) AS c FROM deliveries WHERE ts > ?", [d1]));
  const topRow = await one("SELECT event_id, COUNT(*) AS c FROM feedback WHERE ts > ? GROUP BY event_id ORDER BY c DESC LIMIT 1", [d1]);
  let res24 = null;
  try {
    const rs = await env.DB.prepare("SELECT fb, COUNT(*) AS c FROM feedback WHERE ts > ? GROUP BY fb").bind(d1).all();
    let r = 0, n = 0; (rs.results || []).forEach(function (x) { if (x.fb === "resonated") r = x.c; n += x.c; });
    res24 = { resonated: r, samples: n, rate: n ? Math.round(r / n * 100) : 0 };
  } catch (e) {}
  return {
    ts: now, month: monthKey(new Date()),
    feedback: { total: fbTotal, last24h: fb24, last7d: fb7 },
    deliveries: { total: delTotal, last24h: del24 },
    topWorry24h: topRow ? { id: topRow.event_id, count: topRow.c } : null,
    resonate24h: res24
  };
}
// ?key=env.USAGE_KEY で保護した利用状況JSON。
async function usage(request, env, h) {
  const url = new URL(request.url);
  const key = url.searchParams.get("key") || "";
  if (!env.USAGE_KEY || key !== env.USAGE_KEY) return json({ error: "unauthorized" }, 401, h);
  if (url.searchParams.get("send") === "1") { try { await sendDailyReport(env); } catch (e) {} }
  return json(await computeUsage(env), 200, h);
}
// 日次の推移（JSTの日付ごとに集計）。グラフ用。
async function computeSeries(env, days) {
  const now = Date.now(), since = now - days * 86400000;
  async function byDay(table) {
    try {
      const rs = await env.DB.prepare("SELECT strftime('%Y-%m-%d', ts/1000, 'unixepoch', '+9 hours') AS d, COUNT(*) AS c FROM " + table + " WHERE ts > ? GROUP BY d").bind(since).all();
      const m = {}; (rs.results || []).forEach(function (r) { m[r.d] = r.c; }); return m;
    } catch (e) { return {}; }
  }
  const fbMap = await byDay("feedback"), delMap = await byDay("deliveries");
  const labels = [], feedback = [], deliveries = [];
  for (var i = days - 1; i >= 0; i--) {
    var d = new Date(now - i * 86400000 + 9 * 3600000).toISOString().slice(0, 10);
    labels.push(d.slice(5)); feedback.push(fbMap[d] || 0); deliveries.push(delMap[d] || 0);
  }
  return { labels: labels, feedback: feedback, deliveries: deliveries };
}
// ブックマーク用の利用ダッシュボード（グラフつきHTML）。?key=USAGE_KEY で保護。
async function dashboard(request, env) {
  const url = new URL(request.url);
  const key = url.searchParams.get("key") || "";
  if (!env.USAGE_KEY || key !== env.USAGE_KEY) return new Response("unauthorized", { status: 401 });
  const site = url.searchParams.get("site");
  if (site) return await siteDashboard(env, site);
  const u = await computeUsage(env), s = await computeSeries(env, 30);
  const rr = (u.resonate24h && u.resonate24h.samples) ? (u.resonate24h.rate + "%") : "—";
  const top = u.topWorry24h ? u.topWorry24h.id + "（" + u.topWorry24h.count + "）" : "—";
  const html = '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1"><title>叡智の灯火 — 利用ダッシュボード</title>' +
    '<style>body{font-family:system-ui,-apple-system,"Hiragino Sans",sans-serif;background:#f6efe2;color:#33291f;margin:0;padding:18px}' +
    '.wrap{max-width:760px;margin:0 auto}h1{font-size:1.2rem}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:14px 0}' +
    '.card{background:#fff;border:1px solid #e0d3bb;border-radius:12px;padding:12px;text-align:center}.card b{font-size:1.5rem;color:#a9863f;display:block}' +
    '.card span{font-size:.78rem;color:#6b5d4a}canvas{background:#fff;border:1px solid #e0d3bb;border-radius:12px;padding:10px;margin-top:6px}' +
    '.meta{font-size:.8rem;color:#6b5d4a;margin-top:10px}</style></head><body><div class="wrap">' +
    '<h1>🏮 叡智の灯火 — 利用ダッシュボード</h1>' +
    '<div class="cards">' +
    '<div class="card"><b>' + u.feedback.last24h + '</b><span>昨日の反応</span></div>' +
    '<div class="card"><b>' + u.feedback.last7d + '</b><span>7日の反応</span></div>' +
    '<div class="card"><b>' + u.feedback.total + '</b><span>累計の反応</span></div>' +
    '<div class="card"><b>' + rr + '</b><span>響き度（昨日）</span></div>' +
    '</div><canvas id="c" height="170"></canvas>' +
    '<p class="meta">直近30日の日次推移（JST）／ よく選ばれた悩み（昨日）: ' + top + '<br>更新：開くたびに最新（このページをブックマークしてください）</p>' +
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script><script>' +
    'var L=' + JSON.stringify(s.labels) + ',F=' + JSON.stringify(s.feedback) + ',D=' + JSON.stringify(s.deliveries) + ';' +
    'new Chart(document.getElementById("c"),{type:"line",data:{labels:L,datasets:[' +
    '{label:"反応(feedback)",data:F,borderColor:"#a9863f",backgroundColor:"rgba(202,164,93,.15)",fill:true,tension:.3},' +
    '{label:"ライセンス",data:D,borderColor:"#6fa8a0",fill:false,tension:.3}]},' +
    'options:{plugins:{legend:{labels:{boxWidth:12}}},scales:{y:{beginAtZero:true,ticks:{precision:0}}}}});' +
    '</script></div></body></html>';
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
// 静的サイト（議員ランキング等）の計測ダッシュボード。?key=USAGE_KEY&site=politicians
async function siteDashboard(env, site) {
  const meta = SITES[site] || { label: site, emoji: "📊" };
  const h = await computeHits(env, site), s = await computeHitSeries(env, site, 30);
  const html = '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1"><title>' + meta.label + ' — 計測ダッシュボード</title>' +
    '<style>body{font-family:system-ui,-apple-system,"Hiragino Sans",sans-serif;background:#f6efe2;color:#33291f;margin:0;padding:18px}' +
    '.wrap{max-width:760px;margin:0 auto}h1{font-size:1.2rem}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:14px 0}' +
    '.card{background:#fff;border:1px solid #e0d3bb;border-radius:12px;padding:12px;text-align:center}.card b{font-size:1.5rem;color:#a9863f;display:block}' +
    '.card span{font-size:.78rem;color:#6b5d4a}canvas{background:#fff;border:1px solid #e0d3bb;border-radius:12px;padding:10px;margin-top:6px}' +
    '.meta{font-size:.8rem;color:#6b5d4a;margin-top:10px}</style></head><body><div class="wrap">' +
    '<h1>' + meta.emoji + ' ' + meta.label + ' — 計測ダッシュボード</h1>' +
    '<div class="cards">' +
    '<div class="card"><b>' + h.last24h + '</b><span>昨日のアクセス</span></div>' +
    '<div class="card"><b>' + h.uniq24h + '</b><span>昨日のユニーク</span></div>' +
    '<div class="card"><b>' + h.last7d + '</b><span>7日のアクセス</span></div>' +
    '<div class="card"><b>' + h.total + '</b><span>累計のアクセス</span></div>' +
    '</div><canvas id="c" height="170"></canvas>' +
    '<p class="meta">直近30日の日次推移（JST）／ ユニークは同一IPを30分に1回として概算<br>更新：開くたびに最新（このページをブックマークしてください）</p>' +
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script><script>' +
    'var L=' + JSON.stringify(s.labels) + ',H=' + JSON.stringify(s.hits) + ';' +
    'new Chart(document.getElementById("c"),{type:"line",data:{labels:L,datasets:[' +
    '{label:"アクセス",data:H,borderColor:"#a9863f",backgroundColor:"rgba(202,164,93,.15)",fill:true,tension:.3}]},' +
    'options:{plugins:{legend:{labels:{boxWidth:12}}},scales:{y:{beginAtZero:true,ticks:{precision:0}}}}});' +
    '</script></div></body></html>';
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
// 日次レポートを Discord/Slack の Webhook へ送る（env.REPORT_WEBHOOK）。
async function sendDailyReport(env) {
  if (!env.REPORT_WEBHOOK) return;
  const u = await computeUsage(env);
  const jst = new Date(u.ts + 9 * 3600000).toISOString().slice(0, 10);
  const res = u.resonate24h;
  const lines = [
    "🏮 叡智の灯火 — 日次レポート（" + jst + " JST）",
    "■ ゲーム内の反応（feedback）",
    "　・昨日: " + u.feedback.last24h + " 件 ／ 7日: " + u.feedback.last7d + " 件 ／ 累計: " + u.feedback.total + " 件",
    "■ 響き度（昨日）: " + (res && res.samples ? res.rate + "%（" + res.samples + "件）" : "—"),
    "■ よく選ばれた悩み（昨日）: " + (u.topWorry24h ? u.topWorry24h.id + "（" + u.topWorry24h.count + "件）" : "—"),
    "■ ライセンス利用: 昨日 " + u.deliveries.last24h + " ／ 累計 " + u.deliveries.total
  ];
  if (env.USAGE_KEY) lines.push("📈 推移グラフ: https://api.eichinohi.com/dashboard?key=" + env.USAGE_KEY);
  // 静的サイト（議員ランキング等）のアクセス
  for (const site of Object.keys(SITES)) {
    try {
      const hh = await computeHits(env, site), m = SITES[site];
      lines.push("");
      lines.push("■ " + m.emoji + " " + m.label + "：昨日 " + hh.last24h + "（ユニーク " + hh.uniq24h + "） ／ 7日 " + hh.last7d + " ／ 累計 " + hh.total);
      if (env.USAGE_KEY) lines.push("　📈 https://api.eichinohi.com/dashboard?key=" + env.USAGE_KEY + "&site=" + site);
    } catch (e) {}
  }
  const text = lines.join("\n");
  try {
    await fetch(env.REPORT_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content: text, text: text }) });
  } catch (e) {}
}

// 賢人会議 AI中継。当月有効なJWTを持つ会員は無制限、非会員はIPごとに無料枠のみ。
async function sage(request, env, h) {
  if (!env.ANTHROPIC_API_KEY) return json({ error: { message: "not_configured" } }, 503, h);
  const ip = request.headers.get("CF-Connecting-IP") || "";
  // 会員判定（当月有効なトークンなら会員 = 無制限）
  let member = false;
  const auth = request.headers.get("Authorization") || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  if (token) {
    try { const payload = await verifyJWT(token, env.JWT_SECRET); if (payload && payload.m === monthKey(new Date())) member = true; } catch (e) {}
  }
  // 非会員は無料枠の回数制限（会員はスキップ＝カウントしない）
  if (!member) {
    const over = await limited(env, ip, "sage", SAGE_FREE_LIMIT, SAGE_FREE_WINDOW);
    if (over) return json({ error: { type: "quota", message: "free_limit_reached" } }, 402, h);
  }
  let body; try { body = await request.json(); } catch (e) { return json({ error: { message: "bad_request" } }, 400, h); }
  if (!Array.isArray(body.messages) || body.messages.length === 0) return json({ error: { message: "messages required" } }, 400, h);
  const payload = {
    model: SAGE_MODEL,
    max_tokens: Math.min(Number(body.max_tokens) || SAGE_MAX_TOKENS, SAGE_MAX_TOKENS),
    messages: body.messages
  };
  let up;
  try {
    up = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
      body: JSON.stringify(payload)
    });
  } catch (e) { return json({ error: { message: "upstream_error" } }, 502, h); }
  const text = await up.text();
  // 利用計測（監視ダッシュボード/日次レポート用）
  try { await ensureHits(env); await env.DB.prepare("INSERT INTO hits (site,ts,ip,ref) VALUES (?,?,?,?)").bind(member ? "sage_member" : "sage_free", Date.now(), ip, "").run(); } catch (e) {}
  return new Response(text, { status: up.status, headers: Object.assign({}, h, { "Content-Type": "application/json; charset=utf-8" }) });
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(sendDailyReport(env));
  },
  async fetch(request, env) {
    const h = cors(env, request);
    if (request.method === "OPTIONS") return new Response(null, { headers: h });
    const url = new URL(request.url);
    try {
      if (url.pathname === "/api/health") return json({ ok: true, month: monthKey(new Date()) }, 200, h);
      if (url.pathname === "/api/redeem" && request.method === "POST") return await redeem(request, env, h);
      if (url.pathname === "/api/redeem-license" && request.method === "POST") return await redeemLicense(request, env, h);
      if (url.pathname === "/api/content" && request.method === "GET") return await content(request, env, h);
      if (url.pathname === "/api/sage" && request.method === "POST") return await sage(request, env, h);
      if (url.pathname === "/api/feedback" && request.method === "POST") return await feedback(request, env, h);
      if (url.pathname === "/api/stats" && request.method === "GET") return await stats(request, env, h);
      if (url.pathname === "/api/daily" && request.method === "GET") return await daily(request, env, h);
      if (url.pathname === "/api/usage" && request.method === "GET") return await usage(request, env, h);
      if (url.pathname === "/api/hit" && request.method === "GET") return await hit(request, env, h);
      if (url.pathname === "/api/admin-code" && request.method === "GET") return await adminCode(request, env);
      if (url.pathname === "/dashboard" && request.method === "GET") return await dashboard(request, env);
      return json({ error: "not_found" }, 404, h);
    } catch (e) {
      return json({ error: "server_error" }, 500, h);
    }
  }
};
