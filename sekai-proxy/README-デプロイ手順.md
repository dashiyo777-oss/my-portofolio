# 世界の見方サーチ：デプロイ手順（Claude Code用）

## 構成
- `sekai-proxy/worker.js` … Cloudflare Worker本体（完成品。原則そのまま使う）
- `sekai-proxy/wrangler.toml` … Worker設定（KVのidだけ書き換えが必要）
- `site/index.html` … 公開ページ（先頭のWORKER_URLとMEMBER_URLだけ書き換えが必要）

賢人会議（kenjin-proxy）と同じCloudflareアカウント・同じ流儀でデプロイすること。
kenjin-proxyの既存構成（デプロイ方法・eichinohi.comへのページ配置方法）を先に確認し、それに合わせる。

## デプロイ手順

### 1. KV作成
```
wrangler kv namespace create SEKAI_USAGE
```
表示された id を `wrangler.toml` の `REPLACE_WITH_KV_NAMESPACE_ID` に貼る。

### 2. Secrets設定（オーナーに値を確認）
```
wrangler secret put ANTHROPIC_API_KEY   # kenjin-proxyと同じキーで可
wrangler secret put MONTHLY_CODE        # 今月のメンバーコード（例: SEKAI0726）
```
※コードやAPIキーは絶対にGitにコミットしない。

### 3. Workerデプロイ
```
wrangler deploy
```
デプロイ後のURL（例: https://sekai-proxy.xxxx.workers.dev）を控える。

### 4. フロント配置
- `site/index.html` の先頭にある `WORKER_URL` を手順3のURLに書き換える
- `MEMBER_URL` をnoteメンバーシップ案内ページに書き換える（オーナーに確認）
- eichinohi.com の配下（例: /sekai/）に、既存ページと同じ方法で配置する
- worker.js の `ALLOWED_ORIGINS` が実際の公開ドメインと一致しているか確認
  （サブドメインやGitHub Pagesの場合はここに追加が必要）

### 5. 動作確認チェックリスト
1. キーワード検索が完走し、日本＋選択国のカードとINSIGHTが表示される
2. 韓国・中国を含めて検索し、出力にハングル・中国語が混ざらない
3. 無料10回→11回目でロック画面（MEMBERS ONLY）になる
4. 正しいコードで解除でき、誤コード連打（6回目）で429が返る
5. メンバーで4回目の実行→「本日の上限」表示になる
6. スマホ幅（375px）で表示が崩れない
7. 別ブラウザ（別clientId）では回数が独立している

## 毎月の運用（オーナー向け）
1. 月初に新しいコードを決める
2. `wrangler secret put MONTHLY_CODE` で更新
3. noteメンバー限定エリアに新コードを掲載
4. 前月に解除したユーザーは、月が変わると自動で再ロックされる（Worker側で判定）
5. Anthropic Console（console.anthropic.com → Billing / Usage）で消費額を確認
   - 概算原価：30〜50円/実行。赤字傾向なら worker.js の DAILY_LIMIT を下げる

## 調整可能な定数（worker.js冒頭）
- `FREE_LIMIT = 10` … 無料の累計回数
- `DAILY_LIMIT = 3` … メンバーの1日あたり回数
- web検索の `max_uses: 2` … 1カ国あたりの検索回数上限（増やすと精度↑コスト↑）
