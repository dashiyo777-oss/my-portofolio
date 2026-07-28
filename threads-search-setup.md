# Threads キーワード探索ツール ― セットアップ手順書

`threads-search.html` を実際に動かすための、トークン取得手順です。
**公式APIのみを使い、規約違反はしません。** ただし途中に「Metaのアプリ審査」という関門があります。ここでは、そこも含めて正直に書きます。

---

## この道具でできること・できないこと（再確認）

| できること ✅ | できないこと ❌ |
|---|---|
| キーワードで公開投稿を検索 | 他人のフォロワー数を取る |
| アカウント名・URL・投稿抜粋・最新投稿日 | 他人の投稿の閲覧数を取る |
| 「そのテーマで露出が多い順」に並べる | **フォロワー数順に並べる** |

→ フォロワー数・閲覧数は、公式APIが**そもそも他人分を返さない**ため不可能です（スクレイピングすれば取れますが規約違反＆アカウント凍結リスクのため採用しません）。

---

## 全体の流れ（5ステップ）

```
① アプリを作る  →  ② Threadsを追加＆権限設定  →  ③ 自分を「テスター」に
                                                        ↓
      ⑤ ツールに貼って実行  ←  ④ トークン発行（短期→長期に交換）
```

所要：初回は 20〜40分ほど。2回目以降はトークン再発行だけ（数分）。

---

## ① Meta のアプリを作る

1. [Meta for Developers](https://developers.facebook.com/) にThreads（Instagram）と同じアカウントでログイン。
2. 右上 **マイアプリ → アプリを作成**。
3. ユースケースの選択で **「Threads API を利用」** 系を選ぶ（表記はUI更新で変わることあり。「Threads」と付くものを選べばOK）。
4. アプリ名（自分が分かればなんでも可・例：`my-threads-search`）を入れて作成。

## ② Threads を追加して権限（スコープ）を設定

1. 左メニューの **ユースケース**（または「製品を追加」）から **Threads** を開く。
2. 権限（Permissions）の一覧で、最低限これらを **追加/リクエスト**：
   - `threads_basic` … 基本情報（必須）
   - `threads_keyword_search` … **キーワード検索（このツールの心臓部）**
3. 左メニュー **Threads → 設定** に、
   - **Threads App ID** と **Threads App Secret** が表示されます（後で使う）。
   - **リダイレクトURI** を1つ登録（例：`https://localhost/` でも可。自分で受け取れるURLならなんでも）。

> ⚠️ **ここが関門**：`threads_keyword_search` は本番公開には **アプリ審査（App Review）が必要**です。
> ただし **開発モード（アプリ管理者＝あなた本人／テスター）** なら、審査前でも自分のアカウントで試せるのが通常です。まずは開発モードのまま次へ進みましょう。

## ③ 自分を「Threadsテスター」にする

1. アプリの **役割（Roles）→ Threadsテスター** に、自分のThreadsユーザー名を追加。
2. 自分の **Threadsアプリ（スマホ）→ 設定 → アカウント → ウェブサイトの許可 / 招待** から、テスター招待を **承認**。
   （招待を承認しないとトークンが権限を持てません）

## ④ トークンを発行する（短期 → 長期に交換）

### 4-1. 認可して「コード」を得る

ブラウザで次のURLを開きます（`{...}` を自分の値に置換）。

```
https://threads.net/oauth/authorize
  ?client_id={Threads App ID}
  &redirect_uri={登録したリダイレクトURI}
  &scope=threads_basic,threads_keyword_search
  &response_type=code
```

- Threadsで「許可」すると、リダイレクトURIに `?code=XXXXentry...` が付いて戻ります。
- URLの **`code=` の後ろ**（末尾の `#_` は除く）をコピー。

### 4-2. 短期トークンに交換（POST）

ターミナルなどで：

```bash
curl -X POST "https://graph.threads.net/oauth/access_token" \
  -d "client_id={Threads App ID}" \
  -d "client_secret={Threads App Secret}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri={登録したリダイレクトURI}" \
  -d "code={4-1でコピーしたコード}"
```

→ `{"access_token":"THxxxx...","user_id":...}` が返ります（有効約1時間）。

### 4-3. 長期トークン（60日）に交換（GET）

```bash
curl "https://graph.threads.net/access_token\
?grant_type=th_exchange_token\
&client_secret={Threads App Secret}\
&access_token={4-2で得た短期トークン}"
```

→ `{"access_token":"THxxxx...","expires_in":5184000}`（=60日）。
**この `access_token` がツールに貼る本番トークンです。**

> 🔁 **失効前の延長**：60日以内に一度でも使えば、次で延長できます。
> ```bash
> curl "https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={長期トークン}"
> ```

## ⑤ ツールに貼って実行

1. `threads-search.html` をブラウザで開く。
2. **キーワード** と、④で得た **長期トークン** を入力。
3. 「この条件で探す」を押す。
4. 結果が出たら **CSVで書き出す** で保存も可能。

- 共用PCでなければ「**トークンをこの端末に記憶**」にチェックしておくと次回入力不要（localStorageに保存。通信先はThreads APIのみ）。

---

## うまくいかないとき

| 症状 | 対処 |
|---|---|
| `(#10) Application does not have permission` 等 | `threads_keyword_search` が未付与／テスター承認漏れ／審査未通過。②③を再確認。 |
| `Failed to fetch` / CORS エラー | ブラウザから `graph.threads.net` を直接呼べない場合。ツール下部の **APIプロキシURL** に自分のCloudflare Worker等を設定（このリポジトリの `sae-rank-worker.js` が参考）。 |
| `Invalid OAuth access token` | トークン失効（60日超）。④をやり直すか `refresh_access_token` で延長。 |
| 結果が0件 | キーワードを変える／検索タイプを `RECENT` に切替。 |

---

## よくある質問

**Q. 審査なしで本当に使える？**
A. 開発モードで「自分（管理者/テスター）」の認可なら、多くの場合 `keyword_search` を試せます。うまくいかない場合は Meta のアプリ審査（`threads_keyword_search` の Advanced Access）を申請してください。これは公式が用意した正規ルートで、規約違反ではありません。

**Q. フォロワー数順は本当に無理？**
A. 公式APIの範囲では無理です。合法的に全部満たす方法は存在しません。このツールは「露出量（ヒット投稿数）順」で代替しています。

**Q. トークンは安全？**
A. あなたのブラウザ（localStorage）にだけ保存され、送信先はThreads API（またはあなたが指定したプロキシ）だけです。GitHubやサーバーには送られません。共用端末では「記憶」を外してください。

---

_公式ドキュメント：[Threads API](https://developers.facebook.com/docs/threads) / [Keyword Search](https://developers.facebook.com/docs/threads/keyword-search)_
