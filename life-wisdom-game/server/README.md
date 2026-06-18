# 叡智の灯火 — 会員API（Cloudflare Workers + D1）

有料コンテンツをサーバーからのみ配信し、丸コピーを防ぐためのバックエンド（SPEC §17）。
**フロント（GitHub Pages）はそのまま。** API を立てて URL を設定した時だけ有料がサーバー取得に切り替わる（未設定なら従来どおりクライアント同梱で動く）。

## 構成
- `src/worker.js` … Worker 本体（`/api/redeem` `/api/content` `/api/feedback` `/api/health`）
- `wrangler.toml` … 設定（D1バインディング・CORSオリジン）
- `schema.sql` … D1スキーマ（content / feedback）
- `build-seed.py` … 有料データ → `seed.sql` 生成（`python3 server/build-seed.py`）
- `gen-codes.mjs` … 月替わりコード一覧を表示（note掲示用）

## デプロイ手順（初回）
```bash
npm i -g wrangler
wrangler login

# 1) D1 作成 → 出力された database_id を wrangler.toml に貼る
wrangler d1 create eichi-db

# 2) スキーマ & 有料データ投入
python3 server/build-seed.py
wrangler d1 execute eichi-db --remote --file server/schema.sql
wrangler d1 execute eichi-db --remote --file server/seed.sql

# 3) 秘密鍵を設定（長いランダム文字列を2つ）
wrangler secret put JWT_SECRET
wrangler secret put CODE_SECRET

# 4) デプロイ
cd server && wrangler deploy
#  → https://eichi-no-tomoshibi-api.<account>.workers.dev が払い出される
```

## フロント側の切替（本番をサーバー化する時）
1. `index.html` の読み込みを **`data/gamedata.js`（全部）→ `data/gamedata.free.js`（無料のみ）** に変更
2. `index.html` の先頭で API URL を設定：
   ```html
   <script>window.LWG_API = "https://eichi-no-tomoshibi-api.<account>.workers.dev";</script>
   ```
3. これで有料（偉人・聖典・伝説）は**会員コード→JWT→API取得**になり、クライアントには無料分しか残らない。
   - `LWG_API` が空なら従来挙動（クライアント同梱）。段階移行できる。

## 月替わりコード（note会員ページに貼る）
```bash
CODE_SECRET="（wrangler secret に入れたのと同じ値）" node server/gen-codes.mjs 18
```
- 表示された当月の行を、**毎月初め**にメンバー限定ページへ。
- コードは当月のみ有効（翌月は新コード）。サーバー検証なので**クライアント解析では破れない**。

## 動作確認
```bash
curl https://.../api/health
curl -X POST https://.../api/redeem -H 'content-type: application/json' -d '{"code":"TOMO-XXXX"}'
curl https://.../api/content -H 'Authorization: Bearer <返ってきたtoken>'
curl -X POST https://.../api/feedback -H 'content-type: application/json' -d '{"eventId":"e1","sageId":"jobs","mood":"down","fb":"resonated"}'
curl 'https://.../api/stats?key=e1:jobs'
```

## 注意
- 有料部分はネット必須（無料版は従来どおりオフライン可）。
- スケール：D1/Workers 無料枠で個人運用は十分。秘密鍵は絶対に公開しない。
- P2 で `/api/feedback` の集計（響き度の堀）を本格化。
