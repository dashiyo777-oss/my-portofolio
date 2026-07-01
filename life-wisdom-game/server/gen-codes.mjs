/**
 * 月替わりアクセスコード一覧を表示（note会員ページに貼る用）。
 * サーバーの CODE_SECRET と同じ値を渡すこと（コードはこの秘密に依存）。
 * 使い方:  CODE_SECRET="あなたの秘密" node server/gen-codes.mjs 18
 *          （引数 = 生成する月数。既定12）
 */
import { expectedCode, monthKey } from "./src/worker.js";

const secret = process.env.CODE_SECRET;
if (!secret) { console.error("環境変数 CODE_SECRET を設定してください（サーバーと同じ値）。"); process.exit(1); }
const months = parseInt(process.argv[2] || "12", 10);

const now = new Date();
console.log("| 月 | コード |");
console.log("|---|---|");
for (let i = 0; i < months; i++) {
  const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1));
  const mk = monthKey(d);
  const code = await expectedCode(mk, secret);
  const label = d.getUTCFullYear() + "-" + String(d.getUTCMonth() + 1).padStart(2, "0");
  console.log(`| ${label} | \`${code}\` |`);
}
