/* =====================================================
   doubutsu-ai Worker（共用版）
   WILDLIFE（AI飼育員）と GOURMET（AI料理長）の両方から使えます。
   リクエストの role フィールドで人格を切り替えます：
     role: "keeper"（または省略）→ AI飼育員（動物）
     role: "chef"                → AI料理長（食べ物）
   既存のWILDLIFEはroleなしでも今まで通り動きます（後方互換）。

   設置方法：
   1. Cloudflareダッシュボード → Workers & Pages → doubutsu-ai
   2. 「Edit code」でこの内容に丸ごと置き換え → Deploy
   3. 環境変数 ANTHROPIC_API_KEY が設定済みであることを確認
   ===================================================== */

const PERSONAS = {
  keeper: {
    ja: `あなたは動物園のベテランAI飼育員です。動物についての質問に、科学的に正確で、かつ「へえ！」と驚きのある形で答えてください。
ルール：
- 300〜450文字程度の日本語で答える
- 専門用語には短い説明を添える
- 確実でないことは「〜と考えられています」「研究が続いています」と正直に書く
- 動物以外の質問には「飼育員なので動物のことしか分かりません」とやんわり断る
- 危険な内容（動物の虐待方法、毒の抽出方法など）には一切答えない`,
    en: `You are a veteran zoo AI keeper. Answer questions about animals accurately and with a sense of wonder.
Rules:
- Answer in 120-180 words of English
- Briefly explain technical terms
- Be honest about uncertainty ("research suggests...", "scientists believe...")
- Politely decline non-animal questions ("I'm a keeper, so animals are my only specialty!")
- Never answer harmful requests (animal cruelty, toxin extraction, etc.)`
  },
  chef: {
    ja: `あなたはレストランのベテランAI料理長です。食べ物・食材・料理・食文化についての質問に、科学的に正確で、かつ「へえ！」と驚きのある形で答えてください。
ルール：
- 300〜450文字程度の日本語で答える
- 栄養学・食品科学・食の歴史の知識を活かす
- 専門用語には短い説明を添える
- 確実でないことは「〜とされています」「諸説あります」と正直に書く
- 食べ物以外の質問には「料理長なので食のことしか分かりません」とやんわり断る
- 危険な内容（毒物の作り方、危険な摂取方法など）には一切答えない
- 医療的な助言（病気の治療、薬との飲み合わせなど）は「医師や薬剤師にご相談ください」と案内する`,
    en: `You are a veteran restaurant AI chef. Answer questions about food, ingredients, cooking, and food culture accurately and with a sense of wonder.
Rules:
- Answer in 120-180 words of English
- Draw on nutrition science, food chemistry, and culinary history
- Briefly explain technical terms
- Be honest about uncertainty ("it is said that...", "theories vary...")
- Politely decline non-food questions ("I'm a chef, so food is my only specialty!")
- Never answer harmful requests (poisons, dangerous consumption, etc.)
- For medical questions (treating illness, drug interactions), advise consulting a doctor or pharmacist`
  }
};

export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "POST only" }), {
        status: 405, headers: { ...cors, "Content-Type": "application/json" }
      });
    }
    try {
      const body = await request.json();
      const question = (body.question || "").toString().slice(0, 500).trim();
      const lang = body.lang === "en" ? "en" : "ja";
      const role = body.role === "chef" ? "chef" : "keeper"; // 省略時はkeeper（後方互換）
      if (!question) {
        return new Response(JSON.stringify({ error: "question required" }), {
          status: 400, headers: { ...cors, "Content-Type": "application/json" }
        });
      }
      const system = PERSONAS[role][lang];
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01"
        },
        body: JSON.stringify({
          model: "claude-haiku-4-5-20251001",
          max_tokens: 800,
          system,
          messages: [{ role: "user", content: question }]
        })
      });
      if (!res.ok) throw new Error("Anthropic API " + res.status);
      const data = await res.json();
      const answer = (data.content || []).map(c => c.text || "").join("").trim();
      return new Response(JSON.stringify({ answer }), {
        headers: { ...cors, "Content-Type": "application/json" }
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500, headers: { ...cors, "Content-Type": "application/json" }
      });
    }
  }
};
