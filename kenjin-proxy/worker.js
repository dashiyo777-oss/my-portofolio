const ALLOWED_ORIGINS = [
  "https://eichinohi.com",
  "https://www.eichinohi.com",
];

const MODEL = "claude-sonnet-4-6";
const MAX_TOKENS = 1024;
const MAX_BODY_BYTES = 60000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = ALLOWED_ORIGINS.includes(origin);
    const cors = {
      "Access-Control-Allow-Origin": allowed ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== "POST") {
      return json({ error: { message: "POST only" } }, 405, cors);
    }
    if (!allowed) {
      return json({ error: { message: "Origin not allowed" } }, 403, cors);
    }
    let body;
    try {
      const raw = await request.text();
      if (raw.length > MAX_BODY_BYTES) {
        return json({ error: { message: "Request too large" } }, 413, cors);
      }
      body = JSON.parse(raw);
    } catch {
      return json({ error: { message: "Invalid JSON" } }, 400, cors);
    }
    if (!Array.isArray(body.messages) || body.messages.length === 0) {
      return json({ error: { message: "messages required" } }, 400, cors);
    }
    const payload = {
      model: MODEL,
      max_tokens: Math.min(Number(body.max_tokens) || MAX_TOKENS, MAX_TOKENS),
      messages: body.messages,
    };
    const upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify(payload),
    });
    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}
