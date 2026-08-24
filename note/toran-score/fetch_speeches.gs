/**
 * 国会会議録検索システムから発言件数を取り直す（Google Apps Script）
 *
 * ⚠ このスクリプトは書いた環境から国会会議録検索システムに接続できなかったため、
 *    実際のレスポンスで動作確認できていません。
 *    走らせる前に、必ず下の「STEP 0」をブラウザで実行して、
 *    APIの応答が想定どおりか自分の目で確かめてください。
 *
 * ── STEP 0：先にブラウザで1件だけ確かめる ─────────────────────
 * 次のURLをブラウザのアドレスバーに貼って開きます。
 *
 *   https://kokkai.ndl.go.jp/api/speech?speaker=岸田文雄&from=2021-11-01&until=2026-07-31&maximumRecords=1&recordPacking=json
 *
 * 確かめること:
 *   1. numberOfRecords という項目があり、数字が入っているか
 *   2. その数字が、CSVの岸田文雄の発言数9540と近いか
 *      → 大きく違うなら、CSVの「発言」の定義が違います。
 *        委員会を含むのか、答弁を含むのか、ここで決着させてください
 *   3. 氏名にスペースを入れる／入れないで結果が変わるか
 *      （CSVは「岸田 文雄」ですが、APIは「岸田文雄」で引ける場合があります）
 *
 * この3点が確認できるまで、STEP 1に進まないでください。
 *
 * ── STEP 1：シートを用意する ──────────────────────────────
 * toran-clean.csv を Google スプレッドシートに読み込みます。
 * 1行目が見出しで、次の列があることを確認してください。
 *
 *   氏名 / 統合元氏名（本名。空でも可）
 *
 * ── STEP 2：スクリプトを貼る ──────────────────────────────
 * 拡張機能 → Apps Script を開き、このファイルの中身を貼って保存します。
 *
 * ── STEP 3：実行する ────────────────────────────────────
 * 関数 fetchSpeeches を実行します。初回は権限の確認が出ます。
 *
 * Apps Scriptは1回6分で止まります。712人だと途中で切れますが、
 * 書き込み済みの行は飛ばすので、止まったらもう一度実行してください。
 * 全部埋まるまで、何度か繰り返します。
 */

// ── 設定（ここだけ触れば挙動が変わります）──────────────────────
var FROM = '2021-11-01';        // CSVの発言数の期間に合わせる
var UNTIL = '2026-07-31';
var SLEEP_MS = 1200;            // 1件ごとに待つ時間。相手のサーバーへの礼儀
var NAME_COL = '氏名';
var ALIAS_COL = '統合元氏名';    // 本名。無ければ空でよい
var STOP_AFTER_ERRORS = 5;      // これだけ連続で失敗したら止める

// 書き込む列（無ければ自動で作ります）
var OUT_MAIN = 'API発言数(通称)';
var OUT_ALIAS = 'API発言数(本名)';
var OUT_TOTAL = 'API発言数(判定)';
var OUT_NOTE = 'API備考';
// ────────────────────────────────────────────────────

function fetchSpeeches() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var values = sheet.getDataRange().getValues();
  var header = values[0];

  var col = {};
  header.forEach(function (h, i) { col[String(h).trim()] = i; });

  if (col[NAME_COL] === undefined) {
    throw new Error('「' + NAME_COL + '」という列が見つかりません。1行目を確認してください。');
  }

  // 出力列を用意する
  [OUT_MAIN, OUT_ALIAS, OUT_TOTAL, OUT_NOTE].forEach(function (name) {
    if (col[name] === undefined) {
      header.push(name);
      col[name] = header.length - 1;
      sheet.getRange(1, header.length).setValue(name);
    }
  });

  var errors = 0;
  var done = 0;

  for (var r = 1; r < values.length; r++) {
    var row = values[r];
    var name = String(row[col[NAME_COL]] || '').trim();
    if (!name) continue;

    // すでに埋まっている行は飛ばす（再実行で続きから進むため）
    var already = row[col[OUT_TOTAL]];
    if (already !== '' && already !== undefined && already !== null) continue;

    var alias = ALIAS_COL !== undefined && col[ALIAS_COL] !== undefined
      ? String(row[col[ALIAS_COL]] || '').trim()
      : '';

    var a = countSpeeches(name);
    Utilities.sleep(SLEEP_MS);

    var b = null;
    if (alias) {
      b = countSpeeches(alias);
      Utilities.sleep(SLEEP_MS);
    }

    if (a.error && (!alias || b.error)) {
      errors++;
      writeRow(sheet, r + 1, col, ['', '', '', 'ERROR: ' + a.error]);
      if (errors >= STOP_AFTER_ERRORS) {
        SpreadsheetApp.getUi().alert(
          '連続で' + errors + '件失敗したので止めました。\n' + a.error);
        return;
      }
      continue;
    }
    errors = 0;

    // 通称と本名の判定。
    // 両方に同じ数が出たら、同じ発言を二重に数えている疑いが濃い。
    var note = '';
    var total;
    if (b === null) {
      total = a.count;
    } else if (a.count === b.count) {
      total = a.count;
      note = '通称と本名が同数。同じ発言を二重計上している可能性';
    } else if (b.count === 0) {
      total = a.count;
    } else if (a.count === 0) {
      total = b.count;
      note = '通称では0件。本名でのみ拾えた';
    } else {
      total = Math.max(a.count, b.count);
      note = '両方に別々の値。大きいほうを採用したが要目視（' +
        a.count + ' / ' + b.count + '）';
    }

    writeRow(sheet, r + 1, col,
      [a.count, b === null ? '' : b.count, total, note]);
    done++;

    // 6分制限に当たる前に自分から抜ける（次回は続きから）
    if (done % 50 === 0) SpreadsheetApp.flush();
  }

  SpreadsheetApp.getUi().alert('今回 ' + done + '件を取得しました。\n' +
    '空欄が残っていれば、もう一度実行してください。');
}

function writeRow(sheet, rowNumber, col, vals) {
  sheet.getRange(rowNumber, col[OUT_MAIN] + 1).setValue(vals[0]);
  sheet.getRange(rowNumber, col[OUT_ALIAS] + 1).setValue(vals[1]);
  sheet.getRange(rowNumber, col[OUT_TOTAL] + 1).setValue(vals[2]);
  sheet.getRange(rowNumber, col[OUT_NOTE] + 1).setValue(vals[3]);
}

/**
 * 1人ぶんの発言件数を返す。
 * CSVの氏名は「岸田 文雄」のようにスペース入りなので、詰めた形でも引く。
 */
function countSpeeches(name) {
  var candidates = [name];
  var squeezed = name.replace(/[\s　]/g, '');
  if (squeezed !== name) candidates.push(squeezed);

  var lastError = null;
  for (var i = 0; i < candidates.length; i++) {
    var res = callApi(candidates[i]);
    if (res.error) { lastError = res.error; continue; }
    if (res.count > 0) return res;      // 引けた形を採用
    lastError = null;
  }
  if (lastError) return { count: null, error: lastError };
  return { count: 0, error: null };     // 本当に0件
}

function callApi(speaker) {
  var url = 'https://kokkai.ndl.go.jp/api/speech'
    + '?speaker=' + encodeURIComponent(speaker)
    + '&from=' + FROM
    + '&until=' + UNTIL
    + '&maximumRecords=1'
    + '&recordPacking=json';

  try {
    var resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = resp.getResponseCode();
    if (code !== 200) {
      return { count: null, error: 'HTTP ' + code };
    }
    var json = JSON.parse(resp.getContentText());
    var n = json.numberOfRecords;
    if (n === undefined || n === null) {
      return { count: null, error: 'numberOfRecords が応答にありません' };
    }
    return { count: Number(n), error: null };
  } catch (e) {
    return { count: null, error: String(e) };
  }
}
