# note の記事別アクセス（ビュー・スキ・コメント）を CSV で一括ダウンロードする

作成：2026-11-28
目的：アクセス状況のスクショを何枚も撮る手間をなくし、1クリックで全記事の数字をファイルにする。

## 大事な注意（先に読んでください）

- これは、note の公式に公開された機能ではありません。note のダッシュボード画面が裏で使っている読み込み先（`/api/v1/stats/pv`）を、**自分のブラウザで、自分のログイン状態のまま**呼び出すだけのものです。ID・パスワードはどこにも送りません。
- note 側の仕様変更で、ある日動かなくなる可能性があります。そのときはエラーの文言を教えてください。
- 取りすぎを避けるため、**週1回（金曜）程度**の利用にとどめてください。
- このスクリプトは、作成時点で実際の note アカウントでは動作確認できていません（作成者はログインできないため）。最初の1回は、エラーが出たらその文言をそのまま送ってください。
- **インプレッション（IMP）は、この方法では取れない可能性が高い**です。IMPは、PC版ダッシュボードの上部の合計欄を週1回、スクショ1枚で記録してください。

## 使い方（パソコンのChromeなど。スマホでは使いにくいです）

### 最初の1回だけ：ブックマークを作る
1. ブラウザのブックマークバーで右クリック →「ページを追加」。
2. 名前：`note統計CSV`
3. URL 欄に、下の「ブックマークレット」のコードを**1行まるごと**貼り付けて保存。

### 毎週金曜：ダウンロード
1. note にログインした状態で、`https://note.com/sitesettings/stats` を開く（アクセス状況の画面）。
2. ブックマークの `note統計CSV` をクリック。
3. 期間をきかれるので、`weekly`（週）／`monthly`（月）／`all`（全期間）のどれかを入力してOK。
   - 比較用には `all`（全期間の累計）がおすすめ。毎週同じ期間で取れば、差し引きで「その週に増えた分」が出せます。
4. `note_stats_週や期間_日付.csv` がダウンロードされる。
5. そのCSVファイルを、チャットにそのまま添付する。こちらで分野分け・8〜14日後PV・当たり率（PV10以上）を集計します。

## ブックマークレット（URL欄に貼る1行）

```
javascript:(async()=>{try{const f=prompt('期間を入力（all / monthly / weekly）','all');if(!f)return;const rows=[];let p=1,stop=false;while(!stop&&p<=60){const r=await fetch('/api/v1/stats/pv?filter='+encodeURIComponent(f)+'&page='+p+'&sort=pv',{credentials:'include'});if(!r.ok)throw new Error('HTTP '+r.status+'（ログインしているか、アクセス状況の画面で実行しているか確認してください）');const j=await r.json();const d=(j&&j.data)||{};const list=d.note_stats||[];list.forEach(n=>rows.push(n));stop=(d.last_page===true)||list.length===0;p++;await new Promise(s=>setTimeout(s,500));}if(!rows.length){alert('データが0件でした。画面の期間や、ログイン状態を確認してください。');return;}const keys=[...new Set(rows.flatMap(o=>Object.keys(o).filter(k=>typeof o[k]!=='object'||o[k]===null)))];const esc=v=>{v=(v===null||v===undefined)?'':String(v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;};const csv='﻿'+[keys.join(',')].concat(rows.map(o=>keys.map(k=>esc(o[k])).join(','))).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));const t=new Date();a.download='note_stats_'+f+'_'+t.getFullYear()+String(t.getMonth()+1).padStart(2,'0')+String(t.getDate()).padStart(2,'0')+'.csv';document.body.appendChild(a);a.click();a.remove();alert(rows.length+'件をダウンロードしました。');}catch(e){alert('エラー：'+e.message);}})();
```

## うまく動かないとき
- 「HTTP 401／403」：ログインが切れています。note にログインし直して、アクセス状況の画面で実行してください。
- 「HTTP 404」や「データが0件」：note の仕様が変わった可能性があります。表示された文言を送ってください。別の方法を考えます。
- 何も起きない：ブックマークのURL欄の先頭が `javascript:` になっているか確認してください（貼り付け時に消えるブラウザがあります）。

## それでも難しい場合の代わり
- PC版の「アクセス状況」の一覧で、ページ全体を選んで（Ctrl＋A）コピーし、テキストのままチャットに貼る。スクショ20枚より軽く、こちらで数字を読み取れます。
