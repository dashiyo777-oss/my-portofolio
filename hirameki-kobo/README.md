# ひらめき工房（claude.ai 外で動く版）

思いつきを「工程表 → 製品設計 → 概略図面 → コスト見積 → 権利・宣伝・販売・入金」まで運ぶ個人向け支援ツール。
claude.ai アーティファクト専用だった仕組みを、外部で動くように移植したもの。

## 構成

| ファイル | 役割 |
|---|---|
| `index.html` | 本体（フロント）。ブラウザで開くだけで動く。データは端末の localStorage に保存。|
| `worker.js` | AI 呼び出し用の Cloudflare Worker。APIキーをサーバー側に隠して Anthropic API へ中継する。|
| `wrangler.toml` | wrangler CLI でデプロイする場合の設定。|

## 移植で変わった点（claude.ai 版からの差分）

- **AI呼び出し**: `api.anthropic.com` 直叩き → Cloudflare Worker (`worker.js`) 経由に変更。
  APIキーは Worker の環境変数 `ANTHROPIC_API_KEY` に置く（kenjin-proxy と同方式）。
- **データ保存**: claude.ai 専用の `window.storage` → ブラウザの `localStorage` に変更（同一端末内に保存）。
- **維持したもの**: JSON途中切れの自動修復 `repairJson()`、SVG の `</svg>` 補完とサニタイズ、
  プロンプトの字数・1行JSON制約はそのまま。壊していない。

---

## セットアップ手順

### 1. Worker をデプロイ（APIキーを隠す箱を用意する）

**A. スマホだけで（Cloudflare ダッシュボード）**

1. https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Create Worker**
2. 名前を `hirameki-proxy` にして **Deploy**（中身は後で差し替え）
3. **Edit code** を開き、`worker.js` の内容を全部貼り付けて **Deploy**
4. その Worker の **Settings → Variables and Secrets** で以下を登録:
   - `ANTHROPIC_API_KEY`（type: **Secret**）… Anthropic のАPIキー
   - `ALLOWED_ORIGINS`（type: Text・任意）… 公開ドメインをカンマ区切り
     例: `https://eichinohi.com,https://dashiyo777-oss.github.io`
     （未設定でも動くが、公開時は設定推奨。誰でも叩けると API 課金を悪用される）
5. 画面に出る Worker の URL（例 `https://hirameki-proxy.<サブドメイン>.workers.dev`）をコピー

**B. PC で wrangler CLI を使う場合**

```
npm i -g wrangler
wrangler login
wrangler secret put ANTHROPIC_API_KEY   # プロンプトにキーを貼る
# 必要なら wrangler.toml の [vars] に ALLOWED_ORIGINS を記入
wrangler deploy
```

### 2. フロントに Worker の URL を設定

`index.html` の先頭付近、`AI_ENDPOINT` の行をデプロイした URL に書き換える:

```js
const AI_ENDPOINT = "https://hirameki-proxy.dashiyo777.workers.dev";
```

### 3. 公開（どちらでも可）

- **GitHub Pages**: このリポジトリの Pages を有効化 → `/hirameki-kobo/` で開ける
- **Cloudflare Pages（eichinohi.com）**: 静的サイトとして配信

---

## 動作確認チェックリスト

- [ ] `index.html` をブラウザで開き、「＋ ひらめきを記す」で1件記帳 → 一覧に出る
- [ ] ページを再読込しても記帳が残る（localStorage 保存の確認）
- [ ] 詳細画面で「AIで工程表を作る」→ 工程表が生成される（Worker 経由の確認）
- [ ] 設計書・概略図面・コスト見積・深掘り相談がそれぞれ生成される
- [ ] ブラウザの開発者ツール Network で、リクエスト先が `AI_ENDPOINT`（Worker）になっている

## 既知の制限・次の一手

- **保存は端末ローカル（localStorage）**。別端末とは同期しない。同期が必要なら Supabase 化（HANDOVER 第2段階）。
- **Worker は原則ドメイン制限すべき**（`ALLOWED_ORIGINS`）。将来はパスコード方式（note有料連動）で収益化ゲートも可能。
- モデルは `AI_MODEL`（既定 `claude-sonnet-4-6`）で1箇所管理。変更はここだけ書き換える。
