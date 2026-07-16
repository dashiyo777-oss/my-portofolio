# eichinohi.com 配信用（フラット版）

このフォルダの中身は、**すべてルート直下**で動くように作ってあります。
フォルダ（data/ や audio/）は不要。GitHubに**ファイルを全部まとめてドラッグ**するだけでOK。

## アップロードするファイル（この5つだけ）
- `index.html`
- `style.css`
- `game.js`
- `gamedata.js`
- `bgm.mp3`

> sages.json / events.json / legends.json などは**ゲーム実行には不要**（gamedata.js に同梱済み）。アップロード不要です。

## 手順（eichinohi リポジトリへ）
1. `github.com/dashiyo777-oss/eichinohi` を開く →「Add file」→「Upload files」
2. 上の**5ファイルを一度にドラッグ**（フォルダごとではなく、ファイルを選択）
3. 緑の「**Commit changes**」を押す
   - ※ 空リポジトリでは「Commit directly to the main branch」の選択肢は出ません。押せば main が作られます。
4. 反映後、`https://dashiyo777-oss.github.io/eichinohi/` で表示確認（Pages有効化後）

## このあと（設定）
- Settings → Pages → Source: Deploy from a branch / main / (root)
- Custom domain: `eichinohi.com` → Enforce HTTPS
- Cloudflare DNS:
  - A `@` → `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
  - CNAME `www` → `dashiyo777-oss.github.io`（プロキシOFF＝グレー雲）
