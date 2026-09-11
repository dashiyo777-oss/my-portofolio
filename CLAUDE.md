# CLAUDE.md

## ライティング・ナレッジ

文章（記事・コラム・インタビュー・SNS発信・ポートフォリオ文章など）を書く・編集するタスクでは、必ず以下のナレッジに記載された「型」と「倫理」に従うこと。

- [`knowledge/professional-writing-blueprint.md`](knowledge/professional-writing-blueprint.md) — 社会を動かすプロフェッショナル・ライティングの極意（倫理 / ファクト・エビデンス / 文章構成 / インタビュー集約 / 執筆前チェックリスト）

主な原則の要約:
1. 倫理を最優先（プロボノ精神・嘘を売らない・こたつ記事の排除）
2. ファクトとエビデンスで裏打ち（一次情報・裏取り・反論の機会）
3. 構成で届ける（タイトル9割・1記事1テーマ・起承転結・数字の戦略配置）
4. インタビューは文脈を再構築（録音の再現ではなく編集で価値を生む）

## 宣伝ショート動画・ナレッジ

SNS向けの縦型宣伝ショート動画（YouTubeショート/Reels/TikTok）を作るタスクでは、以下に従うこと。

- [`knowledge/promo-short-video-blueprint.md`](knowledge/promo-short-video-blueprint.md) — 縦型9:16の宣伝ショートをコードだけで作りMP4化する型（倫理 / 構成 / HTML→決定論レンダリング→ffmpeg / 環境の落とし穴 / チェックリスト）
- 再利用スキル: [`.claude/skills/promo-short-video/`](.claude/skills/promo-short-video/SKILL.md)（テンプレートHTMLエンジン＋書き出しスクリプト同梱）

要約:
1. 引用は検証済み・出典明記のみ（実在人物に嘘を言わせない・画面に出典表示）
2. 1動画1テーマ／フックで状況を言い当てる／数字を1つ効かせる
3. `renderAt(t)` の決定論レンダリングで書き出す（リアルタイム画面録画は使わない）
4. MP4は H.264+AAC・`+faststart`・BGMフェード付き。多言語版は原文優先
