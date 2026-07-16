// sekai-proxy: 世界の見方サーチ用 Cloudflare Worker
// Secrets: ANTHROPIC_API_KEY, MONTHLY_CODE（毎月 wrangler secret put MONTHLY_CODE で更新）
// KV: SEKAI_USAGE

const FREE_LIMIT = 10;   // 無料の累計回数（キーワード実行単位）
const DAILY_LIMIT = 3;   // メンバーの1日あたり回数
const MAX_KEYWORD_LEN = 50;

const COUNTRIES = {
  JP: { name: "日本", lang: "日本語" },
  US: { name: "アメリカ", lang: "英語" },
  CN: { name: "中国", lang: "中国語" },
  KR: { name: "韓国", lang: "韓国語" },
  GB: { name: "イギリス", lang: "英語" },
  FR: { name: "フランス", lang: "フランス語" },
  DE: { name: "ドイツ", lang: "ドイツ語" },
  RU: { name: "ロシア", lang: "ロシア語" },
  IN: { name: "インド", lang: "英語・ヒンディー語" },
  QA: { name: "中東（アルジャジーラ等）", lang: "アラビア語・英語" },
};

const ALLOWED_ORIGINS = [
  "https://eichinohi.com",
  "https://www.eichinohi.com",
];

// ---- 日付（日本時間基準） ----
function jstNow() { return new Date(Date.now() + 9 * 3600 * 1000); }
function monthKey() {
  const d = jstNow();
  return d.getUTCFullYear() + "-" + String(d.getUTCMonth() + 1).padStart(2, "0");
}
function dayKey() { return jstNow().toISOString().slice(0, 10); }

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers });
}
async function getInt(kv, key) {
  const v = await kv.get(key);
  return v ? parseInt(v, 10) || 0 : 0;
}

// ---- プロンプト ----
function countryPrompt(keyword, c) {
  return `あなたは一次情報・公平性・読者価値を最優先する国際報道の比較アナリストです。キーワード「${keyword}」について、${c.name}の主要メディア（${c.lang}）が最近どう報じているかをWeb検索で調べてください。現地メディアの報道を優先してください。

【言語の絶対ルール】
- 出力はすべて日本語。ハングル・中国語・英語・その他外国語の文をそのまま出力しない。見出しや引用も必ず日本語に翻訳する。
- メディア名は日本で一般的な表記を使う（例：朝鮮日報、中央日報、人民日報、環球時報、ニューヨーク・タイムズ、ル・モンド）。

【書き方のルール】
- 事実（報道されている出来事・数字）と解釈（メディアの見方）を混同しない。
- 煽り・断定を避け、証拠の強さを超えた表現をしない。
- 報道が見つからない場合は、その旨を正直にsummaryに書く。

必ず以下のJSON形式のみで回答してください。前置き・解説・コードブロック記号は一切書かないでください。

{"summary":"この国のメディア全体の論調を2〜3文で（日本語）","tone":"論調を一言で（例：警戒的・楽観的・批判的・実務的）","points":["特徴的な視点1","視点2","視点3"],"outlets":[{"name":"メディア名（日本語表記）","angle":"そのメディアの切り口を1文で（日本語）"}]}

outletsは2〜3件。すべて日本語で書いてください。`;
}

function comparePrompt(keyword, jpResult, others) {
  return `あなたは一次情報・公平性・読者価値を最優先する編集者です。キーワード「${keyword}」について、各国メディアの論調まとめが以下にあります。

日本: ${JSON.stringify(jpResult)}
他国: ${JSON.stringify(others)}

日本の報道と各国の報道の「見方の違い」を分析してください。

【ルール】
- 出力はすべて日本語。外国語をそのまま出力しない。
- 海外報道を並べるだけにしない。国内報道を一律に低く扱わない。
- 「日本は危ない」で終えない。煽り・断定的な予測をしない。
- 事実と解釈を分け、差が「なぜ生まれるか」まで踏み込む。

必ず以下のJSON形式のみで回答してください。前置き・コードブロック記号は不要です。

{"one_line":"日本と世界の視点差をひとことで（1文）","insights":["日本との具体的な違い・共通点を1文ずつ、3〜4件"],"why":"その差が生まれる背景・理由を1〜2文で","watch":"今後注視すべき具体的な指標・会議・政策・企業行動を1文で"}`;
}

// ---- Anthropic API 呼び出し ----
async function callAnthropic(env, prompt, useSearch) {
  const body = {
    model: "claude-sonnet-4-6",
    max_tokens: 1500,
    messages: [{ role: "user", content: prompt }],
  };
  if (useSearch) {
    // コスト対策：Web検索は1呼び出しあたり最大2回
    body.tools = [{ type: "web_search_20250305", name: "web_search", max_uses: 2 }];
  }
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error.message || "APIエラー");
  const text = (data.content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n");
  const cleaned = text.replace(/```json|```/g, "").trim();
  const s = cleaned.indexOf("{");
  const e = cleaned.lastIndexOf("}");
  if (s === -1 || e === -1) throw new Error("結果の解析に失敗しました");
  return JSON.parse(cleaned.slice(s, e + 1));
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const okOrigin = ALLOWED_ORIGINS.includes(origin);
    const headers = {
      "Access-Control-Allow-Origin": okOrigin ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json; charset=utf-8",
    };
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
    if (request.method !== "POST") return json({ error: "POSTのみ対応" }, 405, headers);
    if (origin && !okOrigin) return json({ error: "許可されていないアクセス元です" }, 403, headers);

    let body;
    try { body = await request.json(); } catch { return json({ error: "リクエスト形式が不正です" }, 400, headers); }
    const cid = String(body.clientId || "").slice(0, 64);
    if (!cid) return json({ error: "clientIdが必要です" }, 400, headers);

    const kv = env.SEKAI_USAGE;
    const path = new URL(request.url).pathname;

    try {
      // ---- 状態確認 ----
      if (path === "/status") {
        const count = await getInt(kv, `u:${cid}:count`);
        const member = (await kv.get(`u:${cid}:member`)) === monthKey();
        const d = member ? await getInt(kv, `u:${cid}:d:${dayKey()}`) : 0;
        return json({
          freeRemaining: Math.max(0, FREE_LIMIT - count),
          isMember: member,
          dailyRemaining: member ? Math.max(0, DAILY_LIMIT - d) : null,
          month: monthKey(),
        }, 200, headers);
      }

      // ---- コード解除 ----
      if (path === "/unlock") {
        const failKey = `u:${cid}:ulfail`;
        const fails = await getInt(kv, failKey);
        if (fails >= 5) {
          return json({ ok: false, error: "試行回数が多すぎます。1分ほどおいて再度お試しください。" }, 429, headers);
        }
        if (String(body.code || "").trim() !== "" && String(body.code || "").trim() === env.MONTHLY_CODE) {
          await kv.put(`u:${cid}:member`, monthKey());
          return json({ ok: true }, 200, headers);
        }
        await kv.put(failKey, String(fails + 1), { expirationTtl: 60 });
        return json({ ok: false }, 200, headers);
      }

      // ---- 1回分の消費（キーワード実行の開始時に呼ぶ） ----
      if (path === "/consume") {
        const member = (await kv.get(`u:${cid}:member`)) === monthKey();
        if (member) {
          const dk = `u:${cid}:d:${dayKey()}`;
          const d = await getInt(kv, dk);
          if (d >= DAILY_LIMIT) {
            return json({ error: "limit", message: `本日の上限（${DAILY_LIMIT}回）に達しました。明日またご利用ください。` }, 402, headers);
          }
          await kv.put(dk, String(d + 1), { expirationTtl: 172800 });
          return json({ ok: true, isMember: true, dailyRemaining: DAILY_LIMIT - d - 1 }, 200, headers);
        }
        const count = await getInt(kv, `u:${cid}:count`);
        if (count >= FREE_LIMIT) {
          return json({ error: "limit", message: "無料利用分が終了しました。" }, 402, headers);
        }
        await kv.put(`u:${cid}:count`, String(count + 1));
        return json({ ok: true, isMember: false, freeRemaining: FREE_LIMIT - count - 1 }, 200, headers);
      }

      // ---- 1カ国分の検索 ----
      if (path === "/search") {
        // 簡易レート制限（1分10回）
        const rlKey = `u:${cid}:rl:${Math.floor(Date.now() / 60000)}`;
        const rl = await getInt(kv, rlKey);
        if (rl >= 10) {
          return json({ error: "rate", message: "アクセスが集中しています。少しおいて再度お試しください。" }, 429, headers);
        }
        await kv.put(rlKey, String(rl + 1), { expirationTtl: 120 });

        const member = (await kv.get(`u:${cid}:member`)) === monthKey();
        const count = await getInt(kv, `u:${cid}:count`);
        if (!member && (count < 1 || count > FREE_LIMIT)) {
          return json({ error: "limit", message: "利用枠がありません。" }, 402, headers);
        }

        const keyword = String(body.keyword || "").trim().slice(0, MAX_KEYWORD_LEN);
        const c = COUNTRIES[body.countryCode];
        if (!keyword || !c) return json({ error: "パラメータが不正です" }, 400, headers);

        const result = await callAnthropic(env, countryPrompt(keyword, c), true);
        return json({ ok: true, result }, 200, headers);
      }

      // ---- 日本×世界の比較 ----
      if (path === "/compare") {
        const keyword = String(body.keyword || "").trim().slice(0, MAX_KEYWORD_LEN);
        if (!keyword || !body.jpResult || !body.others) {
          return json({ error: "パラメータが不正です" }, 400, headers);
        }
        const result = await callAnthropic(env, comparePrompt(keyword, body.jpResult, body.others), false);
        return json({ ok: true, result }, 200, headers);
      }

      return json({ error: "not found" }, 404, headers);
    } catch (e) {
      return json({ error: "server", message: "処理に失敗しました。時間をおいて再度お試しください。" }, 500, headers);
    }
  },
};
