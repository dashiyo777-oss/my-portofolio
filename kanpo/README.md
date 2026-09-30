# kanpo — 官報の保存と集計

官報発行サイト（https://www.kanpo.go.jp/ ・内閣府）は発行から90日間だけ官報全体を公開し、
その後はプライバシー配慮記事（破産・相続などの裁判所公告ほか）を閲覧できなくする
（官報の発行に関する内閣府令 第15条・第18条）。note記事の一次情報として、消える前に保存・集計する。

| ファイル | 内容 |
| --- | --- |
| `fetch_kanpo.py` | 直近90日分の一括PDFと目次を取得（取得済みはスキップ） |
| `count_court_pages.py` | 目次から裁判所公告のページ数・割合を集計 |
| `toc/YYYYMMDD.json` | 各号の目次（区分・記事タイトル・開始ページ・PDFのURL）。個人名は含まない |
| `data/` | 一括PDFの保存先。**個人情報を含むため git 管理外（.gitignore）・公開しない** |

```sh
python3 kanpo/fetch_kanpo.py              # PDF + 目次
python3 kanpo/fetch_kanpo.py --toc-only   # 目次だけ更新
python3 kanpo/count_court_pages.py
```

PDF本体の長期保管は、非公開リポジトリ（`kanpo-archive`）の GitHub Actions で毎日行う想定。
