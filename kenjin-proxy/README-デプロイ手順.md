# kenjin-proxy：デプロイ手順

賢人会議（kenjin-proxy）用の Cloudflare Worker。
`eichinohi.com` からのみ叩ける Claude Messages API プロキシです。

## 構成
- `worker.js` … Worker本体（完成品。原則そのまま使う）
- `wrangler.toml` … Worker設定（`name = "kenjin-proxy"`）

## 前提
- Cloudflare アカウント: dashiyo777（eichinohi.com と同じ）
- Worker「kenjin-proxy」はダッシュボードで作成済み（このデプロイで上書きされる）
- `wrangler` は `npx wrangler` で利用可能

## デプロイ手順（オーナーのローカル端末で実行）

> ⚠️ このリポジトリのリモート実行環境（Claude Code on the web）は
> Cloudflare にログインできず、シークレットの対話入力もできません。
> 下記はオーナー自身の端末で実行してください。

### 1. ログイン
```
cd kenjin-proxy
npx wrangler login
```
ブラウザが開き、dashiyo777 の Cloudflare アカウントで認可する。
確認: `npx wrangler whoami`

### 2. シークレット設定
```
npx wrangler secret put ANTHROPIC_API_KEY
```
プロンプトにAPIキーを直接入力する（画面・ファイル・Gitには残さない）。

### 3. デプロイ
```
npx wrangler deploy
```
表示されたURL（例: `https://kenjin-proxy.<subdomain>.workers.dev`）を控える。

### 4. 動作確認
```
curl -i https://kenjin-proxy.<subdomain>.workers.dev \
  -H "Origin: https://eichinohi.com" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"こんにちは"}]}'
```
`200` で Claude の JSON（`content` 配列を含む）が返れば成功。

#### 動作確認チェックリスト
- `OPTIONS` リクエストで `204` + CORSヘッダが返る
- 許可Origin（eichinohi.com）からのPOSTで `200` + Claude JSON
- 未許可Originからは `403`（`Origin not allowed`）
- `GET` は `405`（`POST only`）
- `messages` 無しは `400`（`messages required`）

## 調整可能な定数（worker.js冒頭）
- `MODEL = "claude-sonnet-4-6"` … 使用モデル
- `MAX_TOKENS = 1024` … 応答上限トークン
- `MAX_BODY_BYTES = 60000` … リクエストボディ上限
- `ALLOWED_ORIGINS` … 許可する公開ドメイン
