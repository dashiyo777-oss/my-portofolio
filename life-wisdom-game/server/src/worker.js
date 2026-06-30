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
  const key = new URL(request.url).searchParams.get("key") || "";
  if (!env.USAGE_KEY || key !== env.USAGE_KEY) return json({ error: "unauthorized" }, 401, h);
  return json(await computeUsage(env), 200, h);
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
  const text = lines.join("\n");
  try {
    await fetch(env.REPORT_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content: text, text: text }) });
  } catch (e) {}
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
      if (url.pathname === "/api/feedback" && request.method === "POST") return await feedback(request, env, h);
      if (url.pathname === "/api/stats" && request.method === "GET") return await stats(request, env, h);
      if (url.pathname === "/api/daily" && request.method === "GET") return await daily(request, env, h);
      if (url.pathname === "/api/usage" && request.method === "GET") return await usage(request, env, h);
      return json({ error: "not_found" }, 404, h);
    } catch (e) {
      return json({ error: "server_error" }, 500, h);
    }
  }
};
