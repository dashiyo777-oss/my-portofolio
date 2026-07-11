// =====================================================
// 冴え手帖 世界番付 Worker (sae-rank)
// KVネームスペース「RANK」をバインドして使います
// エンドポイント:
//   POST /submit  {g:"hana"|"rush", id, n(よびな), s(スコア)}
//   GET  /top?g=hana&n=20
// =====================================================
export default {
  async fetch(req, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (req.method === "OPTIONS") return new Response(null, { headers: cors });
    const url = new URL(req.url);
    const json = (o, s = 200) =>
      new Response(JSON.stringify(o), { status: s, headers: { ...cors, "Content-Type": "application/json" } });
    const GAMES = ["hana", "rush"];
    const yearJST = () => new Date(Date.now() + 9 * 3600 * 1000).getUTCFullYear(); // 日本時間の年

    // ---- スコア送信 ----
    if (req.method === "POST" && url.pathname === "/submit") {
      let b;
      try { b = await req.json(); } catch (e) { return json({ error: "bad json" }, 400); }
      const g = String(b.g || "");
      if (!GAMES.includes(g)) return json({ error: "bad game" }, 400);
      const id = String(b.id || "").replace(/[^a-zA-Z0-9]/g, "").slice(0, 16);
      if (id.length < 6) return json({ error: "bad id" }, 400);
      const name = String(b.n || "").replace(/[<>&"'`]/g, "").trim().slice(0, 8) || "名無し";
      const s = Math.floor(Number(b.s));
      if (!(s > 0 && s < 10000000)) return json({ error: "bad score" }, 400);

      const key = g + ":" + yearJST() + ":" + id;
      const prev = await env.RANK.get(key, "json");
      const best = prev ? Math.max(prev.s, s) : s;   // 自己ベストのみ保持・よびな変更は常に反映
      await env.RANK.put(key, JSON.stringify({ n: name, s: best, t: Date.now() }));
      return json({ ok: true, best });
    }

    // ---- 上位取得（年別・省略時は今年） ----
    if (req.method === "GET" && url.pathname === "/top") {
      const g = url.searchParams.get("g");
      if (!GAMES.includes(g)) return json({ error: "bad game" }, 400);
      const y = String(Number(url.searchParams.get("y")) || yearJST());
      const n = Math.min(50, Number(url.searchParams.get("n") || 20));
      const prefix = g + ":" + y + ":";
      const list = await env.RANK.list({ prefix, limit: 1000 });
      const rows = [];
      for (const k of list.keys) {
        const v = await env.RANK.get(k.name, "json");
        if (v) rows.push({ id: k.name.slice(prefix.length), n: v.n, s: v.s });
      }
      rows.sort((a, b) => b.s - a.s);
      return json({ year: Number(y), top: rows.slice(0, n), total: rows.length });
    }

    // ---- 歴代横綱（各年の1位） ----
    if (req.method === "GET" && url.pathname === "/champions") {
      const g = url.searchParams.get("g");
      if (!GAMES.includes(g)) return json({ error: "bad game" }, 400);
      const list = await env.RANK.list({ prefix: g + ":", limit: 1000 });
      const byYear = {};
      for (const k of list.keys) {
        const parts = k.name.split(":");           // g:year:id
        if (parts.length !== 3) continue;
        const y = Number(parts[1]);
        const v = await env.RANK.get(k.name, "json");
        if (!v) continue;
        if (!byYear[y] || v.s > byYear[y].s) byYear[y] = { y, n: v.n, s: v.s };
      }
      const champs = Object.values(byYear).sort((a, b) => b.y - a.y);
      return json({ champions: champs, currentYear: yearJST() });
    }

    return json({ error: "not found" }, 404);
  }
};
