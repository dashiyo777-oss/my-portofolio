/**
 * ひらめき工房 AI プロキシ（Cloudflare Worker）
 *
 * フロント（index.html）から届いた Anthropic Messages API 用のリクエストボディを、
 * サーバー側に保管した APIキーを付けて api.anthropic.com へ中継する。
 * kenjin-proxy と同じ「キーはWorker側の環境変数に置く」方式。
 *
 * 必要な環境変数（Cloudflare ダッシュボード → 設定 → 変数）:
 *   ANTHROPIC_API_KEY  … Anthropic の APIキー（Secret / 暗号化推奨）
 *   ALLOWED_ORIGINS    … 許可するオリジンをカンマ区切りで指定（任意）
 *                        例: "https://eichinohi.com,https://dashiyo777-oss.github.io"
 *                        未設定なら全オリジンを許可（テスト用。公開時は必ず設定推奨）
 */

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowlist = parseAllowlist(env.ALLOWED_ORIGINS);
    const allowed = isAllowed(origin, allowlist);
    const cors = corsHeaders(origin, allowlist, allowed);

    // プリフライト
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== "POST") {
      return json({ error: { message: "POST のみ対応しています。" } }, 405, cors);
    }
    // オリジン制御（許可リストが設定されている場合のみ弾く）
    if (allowlist.length > 0 && !allowed) {
      return json({ error: { message: "許可されていないオリジンからのリクエストです。" } }, 403, cors);
    }
    if (!env.ANTHROPIC_API_KEY) {
      return json({ error: { message: "サーバー側で APIキーが未設定です。" } }, 500, cors);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: { message: "リクエスト形式が不正です。" } }, 400, cors);
    }

    // フロントが送ってきた項目だけを転送（余計なヘッダーは通さない）
    const payload = {
      model: body.model,
      max_tokens: body.max_tokens,
      system: body.system,
      messages: body.messages,
    };
    if (!payload.model || !payload.messages) {
      return json({ error: { message: "model と messages は必須です。" } }, 400, cors);
    }

    let upstream;
    try {
      upstream = await fetch(ANTHROPIC_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": ANTHROPIC_VERSION,
        },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      return json({ error: { message: "AI サーバーへの接続に失敗しました。" } }, 502, cors);
    }

    // Anthropic のレスポンス（JSON）をそのまま返す。フロント側は既存のまま解釈できる。
    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  },
};

function parseAllowlist(raw) {
  if (!raw) return [];
  return raw.split(",").map((s) => s.trim()).filter(Boolean);
}

function isAllowed(origin, allowlist) {
  if (allowlist.length === 0) return true; // 未設定 = 全許可
  return allowlist.includes(origin);
}

function corsHeaders(origin, allowlist, allowed) {
  // 許可リスト未設定なら "*"、設定済みなら許可されたオリジンのみ反射
  const allowOrigin = allowlist.length === 0 ? "*" : (allowed ? origin : allowlist[0]);
  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}
