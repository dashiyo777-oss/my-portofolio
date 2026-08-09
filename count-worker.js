// =====================================================
// 叡智の灯火 訪問カウンター Worker (eichi-count)
// KVネームスペース「COUNTS」をバインドして使います
//
// 背景: 外部無料サービス counterapi.dev v1 が 2026-08-07 に廃止され、
//       カウント一覧が全滅したため、自前 Cloudflare Worker + KV へ移行。
//
// エンドポイント（counterapi v1 とパス互換にして移行を容易化）:
//   GET /<ns>/up   … +1 して現在値を返す（各アプリページの読込カウント用）
//   GET /<ns>      … 増やさず読むだけ（ダッシュボードの読み取り専用取得）
//   GET /all       … 記録済み全ネームスペースの現在値をまとめて返す
//
// レスポンス例: { "ns":"meisaku", "count":123 }
//              /all → { "counts": { "meisaku":123, "sae":45 } }
//
// KVキー: "c:<ns>"（値は数値の文字列）
// =====================================================
export default {
  async fetch(req, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (req.method === "OPTIONS") return new Response(null, { headers: cors });

    const json = (o, s = 200) =>
      new Response(JSON.stringify(o), { status: s, headers: { ...cors, "Content-Type": "application/json" } });

    if (req.method !== "GET") return json({ error: "method not allowed" }, 405);

    const url = new URL(req.url);
    // 先頭・末尾のスラッシュを除いてパスを分解: "/meisaku/up" -> ["meisaku","up"]
    const parts = url.pathname.replace(/^\/+|\/+$/g, "").split("/").filter(Boolean);

    // ---- 全件取得（ダッシュボードのバッチ用） ----
    if (parts.length === 1 && parts[0] === "all") {
      const counts = {};
      let cursor;
      do {
        const list = await env.COUNTS.list({ prefix: "c:", limit: 1000, cursor });
        for (const k of list.keys) {
          const ns = k.name.slice(2); // "c:" を除去
          const v = await env.COUNTS.get(k.name);
          counts[ns] = v ? (parseInt(v, 10) || 0) : 0;
        }
        cursor = list.list_complete ? null : list.cursor;
      } while (cursor);
      return json({ counts });
    }

    // ---- ネームスペース名のバリデーション ----
    const ns = (parts[0] || "").toLowerCase();
    if (!/^[a-z0-9-]{1,40}$/.test(ns)) return json({ error: "bad ns" }, 400);
    const key = "c:" + ns;

    // ---- +1 して返す（/<ns>/up） ----
    if (parts.length === 2 && parts[1] === "up") {
      const cur = parseInt((await env.COUNTS.get(key)) || "0", 10) || 0;
      const next = cur + 1;
      await env.COUNTS.put(key, String(next));
      return json({ ns, count: next });
    }

    // ---- 読み取り専用（/<ns>） ----
    if (parts.length === 1) {
      const cur = parseInt((await env.COUNTS.get(key)) || "0", 10) || 0;
      return json({ ns, count: cur });
    }

    return json({ error: "not found" }, 404);
  }
};
