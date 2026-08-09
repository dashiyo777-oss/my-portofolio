# 訪問カウンター Worker（eichi-count）デプロイ手順

外部無料サービス **counterapi.dev v1 が 2026-08-07 に廃止**され、カウント一覧
（`count-dashboard.html`）が全項目「取得不可」になったため、自前の
**Cloudflare Worker + KV** に移行しました。本ファイルはそのデプロイ手順です。

- Worker 本体: [`count-worker.js`](count-worker.js)
- 参照している URL: `https://eichi-count.dashiyo777.workers.dev`
  （`count-dashboard.html` と各アプリページのカウントスニペットがこの URL を叩きます）

> ⚠️ 累計値は **0 からの再スタート**です（旧 counterapi v1 は停止済みで API から
> 旧値を取得できないため）。旧累計値を引き継ぎたくなった場合は末尾の「補足」を参照。

---

## エンドポイント仕様

| メソッド・パス   | 用途                                   | 例                                   |
| ---------------- | -------------------------------------- | ------------------------------------ |
| `GET /<ns>/up`   | +1 して現在値を返す（各ページの計測）  | `/meisaku/up` → `{"ns":"meisaku","count":123}` |
| `GET /<ns>`      | 増やさず読むだけ（ダッシュボード用）   | `/meisaku` → `{"ns":"meisaku","count":123}` |
| `GET /all`       | 記録済み全 ns の現在値をまとめて返す   | `/all` → `{"counts":{"meisaku":123,...}}` |

- `ns` は `[a-z0-9-]`（1〜40文字）のみ許可。
- 旧 counterapi と**パス互換**（`/<ns>/up`）なので、各アプリページはホスト名を
  差し替えるだけで移行済みです。

---

## デプロイ（Cloudflare ダッシュボード操作）

既存の `sae-rank` などと同じ要領です。

1. **KV ネームスペースを作成**
   - Workers & Pages → KV → *Create a namespace* → 名前を `COUNTS` にする。

2. **Worker を作成**
   - Workers & Pages → *Create* → *Create Worker* → 名前を `eichi-count` にする
     （URL が `https://eichi-count.dashiyo777.workers.dev` になる）。
   - *Edit code* を開き、[`count-worker.js`](count-worker.js) の内容を丸ごと貼り付けて *Deploy*。

3. **KV をバインド**
   - その Worker の *Settings* → *Variables and Secrets* → *KV Namespace Bindings* →
     *Add binding*。
   - **Variable name**: `COUNTS`（コード内の `env.COUNTS` と一致させる）
   - **KV namespace**: 手順1で作った `COUNTS` を選択 → *Save and Deploy*。

4. **動作確認**（ターミナル）
   ```bash
   # +1 して読む
   curl -s https://eichi-count.dashiyo777.workers.dev/meisaku/up
   # → {"ns":"meisaku","count":1}

   # 増やさず読む（ダッシュボードと同じ経路）
   curl -s https://eichi-count.dashiyo777.workers.dev/meisaku
   # → {"ns":"meisaku","count":1}

   # 全件
   curl -s https://eichi-count.dashiyo777.workers.dev/all
   # → {"counts":{"meisaku":1}}
   ```

5. **反映確認**
   - `count-dashboard.html` を開くと、記録済み ns が数値表示に変わります
     （未計測の ns は 0）。
   - 各アプリページ（例 `meisaku-techo.html`）を開くとその ns が +1 されます。

> Worker 名を `eichi-count` 以外にする場合は、`count-dashboard.html` の
> `var WORKER = '...'` と、各アプリページの `https://eichi-count.dashiyo777.workers.dev`
> を実際の URL に合わせて書き換えてください。

---

## 補足: 後から旧累計値を初期値として入れたい場合

旧ダッシュボードは成功時に端末の `localStorage['eichi-counts']` に累計スナップショット
を保存しています。8/7 の廃止**前**にこの画面を開いた端末が残っていれば、そこに最後の
累計値があります。ブラウザの DevTools コンソールで次を実行すると取り出せます。

```js
JSON.parse(localStorage.getItem('eichi-counts'))
// → {"meisaku":1234,"sae":567,...}
```

取り出した値は、一時的に `GET /<ns>/set?v=<n>` のような初期化エンドポイントを
`count-worker.js` に足すか、Cloudflare の KV 画面で各キー `c:<ns>` に手入力すれば
引き継げます（必要になったら対応します）。
