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

function cors(env) {
  return {
    "Access-Control-Allow-Origin": (env && env.ALLOW_ORIGIN) || "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Authorization,Content-Type",
    "Access-Control-Max-Age": "86400"
  };
}
function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: Object.assign({ "Content-Type": "application/json; charset=utf-8" }, headers || {}) });
}

async function loadType(env, type) {
  const rs = await env.DB.prepare("SELECT payload FROM content WHERE type=?").bind(type).all();
  return (rs.results || []).map(function (r) { try { return JSON.parse(r.payload); } catch (e) { return null; } }).filter(Boolean);
}

async function redeem(request, env, h) {
  let body; try { body = await request.json(); } catch (e) { return json({ error: "bad_request" }, 400, h); }
  const code = (body && body.code ? String(body.code) : "").trim().toUpperCase();
  const mk = monthKey(new Date());
  const want = (await expectedCode(mk, env.CODE_SECRET)).toUpperCase();
  if (!code || code !== want) return json({ error: "invalid_code" }, 401, h);
  const exp = monthEndExp(new Date());
  const token = await signJWT({ m: mk, exp: exp }, env.JWT_SECRET);
  return json({ token: token, exp: exp, month: mk }, 200, h);
}

async function content(request, env, h) {
  const auth = request.headers.get("Authorization") || "";
  const token = auth.replace(/^Bearer\s+/i, "");
  const payload = await verifyJWT(token, env.JWT_SECRET);
  if (!payload || payload.m !== monthKey(new Date())) return json({ error: "unauthorized" }, 401, h);
  const [sages, events, legends] = await Promise.all([loadType(env, "sage"), loadType(env, "event"), loadType(env, "legend")]);
  return json({ sages: sages, events: events, legends: legends }, 200, h);
}

async function feedback(request, env, h) {
  let b; try { b = await request.json(); } catch (e) { return json({ error: "bad_request" }, 400, h); }
  try {
    await env.DB.prepare("INSERT INTO feedback (ts,event_id,sage_id,mood,fb) VALUES (?,?,?,?,?)")
      .bind(Date.now(), String(b.eventId || ""), String(b.sageId || ""), String(b.mood || ""), String(b.fb || "")).run();
  } catch (e) {}
  return json({ ok: true }, 200, h);
}

// 「○%が響いた」集計（匿名・読み取り）。key = "eventId:sageId"
async function stats(request, env, h) {
  const key = new URL(request.url).searchParams.get("key") || "";
  const i = key.indexOf(":");
  if (i < 0) return json({ error: "bad_key" }, 400, h);
  const ev = key.slice(0, i), sg = key.slice(i + 1);
  const rs = await env.DB.prepare("SELECT fb, COUNT(*) AS c FROM feedback WHERE event_id=? AND sage_id=? GROUP BY fb").bind(ev, sg).all();
  let res = 0, not = 0;
  (rs.results || []).forEach(function (r) { if (r.fb === "resonated") res = r.c; else if (r.fb === "not_now") not = r.c; });
  const samples = res + not;
  return json({ key: key, resonated: res, not_now: not, samples: samples, resonateRate: samples ? res / samples : 0 }, 200, h);
}

export default {
  async fetch(request, env) {
    const h = cors(env);
    if (request.method === "OPTIONS") return new Response(null, { headers: h });
    const url = new URL(request.url);
    try {
      if (url.pathname === "/api/health") return json({ ok: true, month: monthKey(new Date()) }, 200, h);
      if (url.pathname === "/api/redeem" && request.method === "POST") return await redeem(request, env, h);
      if (url.pathname === "/api/content" && request.method === "GET") return await content(request, env, h);
      if (url.pathname === "/api/feedback" && request.method === "POST") return await feedback(request, env, h);
      if (url.pathname === "/api/stats" && request.method === "GET") return await stats(request, env, h);
      return json({ error: "not_found" }, 404, h);
    } catch (e) {
      return json({ error: "server_error" }, 500, h);
    }
  }
};
