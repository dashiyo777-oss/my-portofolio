/**
 * 国会会議録検索システムから発言件数を取り直す（Google Apps Script）
 *
 * 2026-08-24、ブラウザで1件確認済みです。
 *   speaker=岸田文雄 / 2021-11-01〜2026-07-31 → numberOfRecords = 9540
 *   CSVの発言数9540と完全に一致したので、CSVはこのAPIのこのパラメータで
 *   作られていると確定しました。nameOfHouse は「両院」で、衆参の本会議・
 *   委員会・合同審査会をすべて含みます。
 *   氏名はスペースを詰めた形（岸田文雄）で引けます。
 *
 * 発言件数のほかに、応答には次も入っています。ここも同時に拾います。
 *   speakerGroup    会派  → 政党「（要確認）」48人を埋められる
 *   speakerYomi     よみ  → よみの欠損を埋められる
 *   speakerPosition 政府の役職 → 大臣などのポストだけ。一般の議員は null
 *
 * speakerPosition について（2026-08-24に麻生太郎で確認）:
 *   岸田文雄では「内閣総理大臣」が返るが、麻生太郎では null だった。
 *   これは政府の役職であって議員の身分ではない。CSVの役職欄の大半を占める
 *   「衆議院議員」「参議院議員」は院の列から機械的に作れるので、APIが要るのは
 *   大臣ポストの部分だけ。
 *
 * ただし会派と役職は「返ってきた1件の発言時点」の値です。日付も一緒に
 * 記録するので、古ければ fetchAffiliations() で引き直してください。
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

// ── 期間について（2026-08-24に判明）─────────────────────────
// 福島みずほで引くと、CSVの1,420に対して
//   until=2026-07-31 → 1,494
//   until=2026-06-30 → 1,472
// となり、どちらとも合わなかった。CSVの列名「2021.11〜2026.07」は
// 実際の集計範囲と一致していない。
//
// 岸田文雄と麻生太郎が一致したのは矛盾しない。麻生の最新発言は2024年11月で、
// 締めが手前でも数字が変わらないため。直近まで活発な人でだけズレが出る。
//
// したがって古い数字の締め日を突き止める意味は薄く、UNTIL を固定して
// 全件取り直すのが確実。取得日時を必ず記録するのはそのため。
//
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
var OUT_YOMI = 'APIよみ';
var OUT_GROUP = 'API会派';
var OUT_POS = 'API役職';
var OUT_ASOF = 'API会派の時点';
var OUT_FETCHED = 'API取得日時';

// 会派を引き直すときの開始日。直近の会派が欲しいので選挙後に置く。
var AFFIL_FROM = '2026-02-01';
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
  [OUT_MAIN, OUT_ALIAS, OUT_TOTAL, OUT_NOTE,
   OUT_YOMI, OUT_GROUP, OUT_POS, OUT_ASOF, OUT_FETCHED].forEach(function (name) {
    if (col[name] === undefined) {
      header.push(name);
      col[name] = header.length - 1;
      sheet.getRange(1, header.length).setValue(name);
    }
  });

  console.log('開始します。対象は最大 ' + (values.length - 1) + ' 行です。');
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
        say('連続で' + errors + '件失敗したので止めました。' + a.error);
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
      [a.count, b === null ? '' : b.count, total, note],
      a.count !== null ? a : b);
    done++;

    // 進捗をログに出す。無反応に見えると、動いているのか判断できないため。
    if (done % 10 === 0) {
      console.log(done + '件完了（' + r + '行目 ' + name + '）');
      SpreadsheetApp.flush();
    }
  }

  say('今回 ' + done + '件を取得しました。'
    + '空欄が残っていれば、もう一度実行してください。');
}


/**
 * 進捗の知らせ方。
 * スプレッドシートの画面から実行したときはポップアップを出し、
 * Apps Scriptのエディタから実行したときは実行ログに書く。
 * エディタにはポップアップの表示先がなく、getUi() をそのまま呼ぶと
 * 実行が止まったように見えるため、必ずここを通す。
 */
function say(message) {
  console.log(message);
  try {
    SpreadsheetApp.getUi().alert(message);
  } catch (e) {
    // エディタから実行した場合。ログに出ているので何もしない。
  }
}

/**
 * 1行ぶんの結果を書く。
 * 出力列は末尾に連続して並ぶので、1回のsetValuesでまとめて書く。
 * 1セルずつ書くと9往復になり、1行あたり1秒近く余計にかかって、
 * 6分の制限に早く当たってしまう。
 */
function writeRow(sheet, rowNumber, col, vals, meta) {
  // 取得日時は必ず残す。会議録は後から追加されるので、同じクエリでも
  // 引いた日によって数字が変わる。いつ時点かが書けない数字は再現できない。
  var stamp = Utilities.formatDate(new Date(),
    Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm');
  var m = meta || {};

  var pairs = [
    [col[OUT_MAIN], vals[0]],
    [col[OUT_ALIAS], vals[1]],
    [col[OUT_TOTAL], vals[2]],
    [col[OUT_NOTE], vals[3]],
    [col[OUT_YOMI], m.yomi || ''],
    [col[OUT_GROUP], m.group || ''],
    [col[OUT_POS], m.position || ''],
    [col[OUT_ASOF], m.date || ''],
    [col[OUT_FETCHED], stamp]
  ];

  var min = pairs[0][0];
  var max = pairs[0][0];
  for (var i = 1; i < pairs.length; i++) {
    if (pairs[i][0] < min) min = pairs[i][0];
    if (pairs[i][0] > max) max = pairs[i][0];
  }

  // 連続していればまとめて1回で書く
  if (max - min + 1 === pairs.length) {
    var line = new Array(pairs.length);
    for (var j = 0; j < pairs.length; j++) {
      line[pairs[j][0] - min] = pairs[j][1];
    }
    sheet.getRange(rowNumber, min + 1, 1, pairs.length).setValues([line]);
    return;
  }

  // 並びが崩れている場合（列を手で足したときなど）は1セルずつ
  for (var k = 0; k < pairs.length; k++) {
    sheet.getRange(rowNumber, pairs[k][0] + 1).setValue(pairs[k][1]);
  }
}


/**
 * 政党が「（要確認）」の行だけ、選挙後の会派を引き直す。
 * fetchSpeeches のあとに実行してください。48人ぶんなので数分で終わります。
 */
function fetchAffiliations() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var values = sheet.getDataRange().getValues();
  var header = values[0];
  var col = {};
  header.forEach(function (h, i) { col[String(h).trim()] = i; });

  if (col['政党'] === undefined) throw new Error('「政党」列がありません。');
  [OUT_GROUP, OUT_ASOF].forEach(function (name) {
    if (col[name] === undefined) {
      header.push(name);
      col[name] = header.length - 1;
      sheet.getRange(1, header.length).setValue(name);
    }
  });

  var done = 0;
  for (var r = 1; r < values.length; r++) {
    var party = String(values[r][col['政党']] || '').trim();
    if (party !== '（要確認）') continue;

    var name = String(values[r][col[NAME_COL]] || '').trim();
    if (!name) continue;

    var res = callApi(name.replace(/[\s　]/g, ''), AFFIL_FROM, UNTIL);
    Utilities.sleep(SLEEP_MS);
    if (res.error) continue;

    sheet.getRange(r + 1, col[OUT_GROUP] + 1).setValue(res.group || '(該当なし)');
    sheet.getRange(r + 1, col[OUT_ASOF] + 1).setValue(res.date || '');
    done++;
  }
  say(done + '人ぶんの会派を ' + AFFIL_FROM + ' 以降の発言から引き直しました。');
}

/**
 * 1人ぶんの発言件数を返す。
 * CSVの氏名は「岸田 文雄」のようにスペース入りなので、詰めた形でも引く。
 */
function countSpeeches(name) {
  // 詰めた形（岸田文雄）を先に試す。CSVはスペース入りだが、APIはこちらで引ける。
  // 順序を逆にすると全員ぶん2回問い合わせることになり、時間が倍かかる。
  var squeezed = name.replace(/[\s　]/g, '');
  var candidates = squeezed !== name ? [squeezed, name] : [name];

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

function callApi(speaker, from, until) {
  var url = 'https://kokkai.ndl.go.jp/api/speech'
    + '?speaker=' + encodeURIComponent(speaker)
    + '&from=' + (from || FROM)
    + '&until=' + (until || UNTIL)
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
    // 会派・よみ・役職も同じ応答に入っているので拾う。
    // ただし「返ってきた1件の発言時点」の値なので、日付も一緒に持つ。
    var rec = (json.speechRecord && json.speechRecord[0]) || {};
    return {
      count: Number(n),
      error: null,
      yomi: rec.speakerYomi || '',
      group: rec.speakerGroup || '',
      position: rec.speakerPosition || '',
      date: rec.date || ''
    };
  } catch (e) {
    return { count: null, error: String(e) };
  }
}
