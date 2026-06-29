/*
 * Kiku（効く）— データ層 ＝ 将来のDBスキーマの正典
 * --------------------------------------------------------------
 * 設計意図（手戻り防止）:
 *  - ここで定義する形を、そのままバックエンドのテーブル設計に写せるようにする。
 *  - i18n は最初から構造化（{ ja, en }）。海外展開でカラム追加だけで他言語に拡張可。
 *  - 著作権配慮: contents は「動画そのもの」を持たない。運営が内容を理解して
 *    自分の言葉で書いた summary / steps（＝自前の二次著作物）と、出典への
 *    公式リンク source だけを持つ。＝「知見と評価を運ぶ」設計（CONCEPT.md §3）。
 *  - file:// で開くだけで動くよう、JSON ではなく window.APP_DATA に載せる
 *    （life-wisdom-game/data/gamedata.js と同方針）。
 *
 * 評価の二層（薬機法配慮 / CONCEPT.md §4）:
 *  - stats   … ユーザーの「体感」レビュー（resonated=効いた / notHelpful=自分には）
 *  - evidence… 科学的根拠の度合い（none / anecdotal / expert / study）
 *  - review  … 専門家監修の状態（unreviewed / expert）
 *  この3つを画面上でも必ず分離表示し、効能を断定しない。
 */
(function () {
  "use strict";

  // ─────────────────────────────────────────────
  // ジャンル（目的から探せる入口）
  // ─────────────────────────────────────────────
  var genres = [
    { id: "neck",    name: { ja: "首・肩こり",   en: "Neck & Shoulder" }, icon: "🧣", color: "#2f8f83" },
    { id: "back",    name: { ja: "腰・股関節",   en: "Back & Hips" },     icon: "🦵", color: "#3b7dbf" },
    { id: "eyes",    name: { ja: "目の疲れ",     en: "Eye Strain" },      icon: "👁️", color: "#7a5cc4" },
    { id: "sleep",   name: { ja: "睡眠・自律神経", en: "Sleep" },          icon: "🌙", color: "#5161b8" },
    { id: "home",    name: { ja: "家事・収納",   en: "Home & Tidy" },     icon: "🧺", color: "#c8813a" },
    { id: "saving",  name: { ja: "節約・暮らし", en: "Saving" },          icon: "💴", color: "#3f9a5a" }
  ];

  // ─────────────────────────────────────────────
  // 貢献者（海外含む。チップの受け手）
  // ─────────────────────────────────────────────
  var contributors = [
    { id: "leo",    name: "Leo",        origin: "JP", color: "#2f8f83",
      bio: { ja: "生活の裏技を検証して紹介。",            en: "Tests and shares everyday life hacks." } },
    { id: "mei",    name: "Dr. Mei",    origin: "JP", color: "#3b7dbf", expert: true,
      bio: { ja: "理学療法士。動きの専門家。",            en: "Physiotherapist. Movement specialist." } },
    { id: "chen",   name: "陳先生",      origin: "CN", color: "#c0532f",
      bio: { ja: "中医（東洋医学）の知恵を発信。",        en: "Shares traditional Chinese medicine wisdom." } },
    { id: "sora",   name: "Sora",       origin: "JP", color: "#7a5cc4",
      bio: { ja: "睡眠と自律神経のセルフケア。",          en: "Self-care for sleep and the nervous system." } },
    { id: "marie",  name: "Marie",      origin: "FR", color: "#c8813a",
      bio: { ja: "暮らしを整える収納・家事術。",          en: "Tidying and home routines that stick." } },
    { id: "ken",    name: "Ken",        origin: "JP", color: "#3f9a5a",
      bio: { ja: "ムリなく続く節約の工夫。",              en: "Saving tips you can actually keep up." } }
  ];

  // ─────────────────────────────────────────────
  // コンテンツ（知見＋評価。動画は持たず出典リンクのみ）
  //
  // フィールド:
  //  id, genreId, contributorId
  //  title   {ja,en}            … 自前の見出し
  //  summary {ja,en}            … 運営が自分の言葉で要約（自前著作物）
  //  steps   [{ja,en}...]       … 手順（事実・手法。著作権の及ばない情報）
  //  caution {ja,en}            … 注意・禁忌（薬機法配慮）
  //  origin  "JP"|"CN"|...      … 発掘元の国（海外発掘の価値を可視化）
  //  source  { type, label, url}… 公式リンク/埋め込みのみ（再配信しない）
  //  evidence{ level, note{ja,en} } … 科学的根拠の度合い
  //  review  { status, by }     … 専門家監修の状態
  //  minutes 目安時間, tags[]
  //  stats   { tried, resonated, notHelpful } … 体感の集計（シード値）
  // ─────────────────────────────────────────────
  var contents = [
    {
      id: "neck-stuck-release", genreId: "neck", contributorId: "leo", origin: "JP",
      title: { ja: "首のつまりを一瞬でゆるめる", en: "Release a stiff neck in seconds" },
      summary: {
        ja: "胸鎖乳突筋（耳の下〜鎖骨の筋）を軽くつまんで上下にさする方法。長時間のスマホ姿勢でこわばった首まわりを、力を入れずにゆるめる狙い。",
        en: "Gently pinch and stroke the sternocleidomastoid (from below the ear to the collarbone). Aims to loosen a neck stiffened by long phone use, without forcing it."
      },
      steps: [
        { ja: "顔を横に向け、浮き出る筋を親指と人差し指で軽くつまむ。", en: "Turn your head; lightly pinch the muscle that stands out." },
        { ja: "痛気持ちいい強さで上下に10回さする。", en: "Stroke up and down 10 times at a 'good-pain' pressure." },
        { ja: "左右おこなう。痛みが強い日はやらない。", en: "Do both sides. Skip it on days it hurts sharply." }
      ],
      caution: { ja: "強く揉まない。めまい・しびれが出たら中止。頸動脈付近は避ける。", en: "Don't press hard. Stop if dizzy or numb. Avoid the carotid area." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/neck-stuck" },
      evidence: { level: "anecdotal", note: { ja: "体感報告が中心。筋膜への軽い刺激は一般的なセルフケア範囲。", en: "Mostly anecdotal; light fascia stimulation is common self-care." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["スマホ首", "デスクワーク"],
      stats: { tried: 1580, resonated: 712, notHelpful: 188 }
    },
    {
      id: "neck-god-point", genreId: "neck", contributorId: "chen", origin: "CN",
      title: { ja: "手のツボ「合谷」で首肩を軽く", en: "Ease neck & shoulders via the Hegu point" },
      summary: {
        ja: "親指と人差し指の骨が合わさる手前のくぼみ（合谷）を押す、中医で広く知られた方法。海外（中国）で大量に紹介されている定番を、安全な範囲に絞って紹介。",
        en: "Press the hollow before where the thumb and index bones meet (Hegu/LI4), a staple in Chinese medicine. We surface this widely-shared overseas tip, trimmed to a safe range."
      },
      steps: [
        { ja: "反対の親指で合谷を5秒押して離すを5回。", en: "Press Hegu 5s, release; repeat 5 times with the other thumb." },
        { ja: "呼吸を止めず、ゆっくり。", en: "Breathe slowly; don't hold your breath." }
      ],
      caution: { ja: "妊娠中は避けるとされる。強圧・長時間は控える。", en: "Said to be avoided during pregnancy. Avoid strong/long pressure." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/hegu" },
      evidence: { level: "expert", note: { ja: "鍼灸領域で広く用いられるが、首肩への効果の研究は限定的。", en: "Widely used in acupuncture; rigorous studies on neck relief are limited." } },
      review: { status: "expert", by: "chen" },
      minutes: 1, tags: ["ツボ", "海外発掘"],
      stats: { tried: 4120, resonated: 2510, notHelpful: 410 }
    },
    {
      id: "back-frog-legs", genreId: "back", contributorId: "mei", origin: "JP",
      title: { ja: "カエル足ストレッチで腰をゆるめる", en: "Frog-leg stretch to relax the lower back" },
      summary: {
        ja: "あおむけで足裏を合わせ、膝を外に開いて股関節まわりをゆるめる定番ストレッチ。理学療法士の監修コメント付き。",
        en: "Lying on your back, soles together, knees out — a classic stretch to relax the hips. Includes a physiotherapist's note."
      },
      steps: [
        { ja: "あおむけで足裏を合わせ、膝を楽に開く。", en: "On your back, put soles together, let knees fall open." },
        { ja: "30秒キープ×2。反動はつけない。", en: "Hold 30s × 2. No bouncing." }
      ],
      caution: { ja: "股関節に痛みがある人は無理をしない。", en: "Don't push if your hips already hurt." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/frog" },
      evidence: { level: "study", note: { ja: "股関節モビリティ運動は腰部の不快感軽減に資する報告がある。", en: "Hip-mobility work is reported to help reduce low-back discomfort." } },
      review: { status: "expert", by: "mei" },
      minutes: 3, tags: ["ストレッチ", "股関節"],
      stats: { tried: 2240, resonated: 1490, notHelpful: 210 }
    },
    {
      id: "back-hip-reset", genreId: "back", contributorId: "leo", origin: "JP",
      title: { ja: "股関節つまりを10回でスッキリ", en: "Loosen tight hips in 10 reps" },
      summary: {
        ja: "壁に手をつき、片脚を前後に10回ふって股関節を動かす朝のリセット。再生数が非常に多いが、体感レビューは賛否が分かれる例。",
        en: "Hand on a wall, swing one leg back and forth 10 times — a morning hip reset. Very high views, but体感 reviews are mixed — a good honesty example."
      },
      steps: [
        { ja: "壁に手をつき、片脚を前後に10回ふる。", en: "Hand on wall; swing one leg front-to-back 10 times." },
        { ja: "左右おこなう。", en: "Repeat on both sides." }
      ],
      caution: { ja: "ふらつく場合は支えを増やす。痛みが出たら中止。", en: "Add support if unsteady. Stop if it hurts." },
      source: { type: "link", label: "生活のコツ (short)", url: "https://example.com/source/hip-reset" },
      evidence: { level: "anecdotal", note: { ja: "軽い運動として一般的。劇的効果をうたう根拠は薄い。", en: "Fine as light movement; claims of dramatic effect are thin." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["朝ルーティン", "バズ動画"],
      stats: { tried: 9800, resonated: 3100, notHelpful: 2600 }
    },
    {
      id: "eyes-palming", genreId: "eyes", contributorId: "sora", origin: "JP",
      title: { ja: "手のひらで目を温めて疲れを流す", en: "Warm-palm rest for tired eyes" },
      summary: {
        ja: "手をこすって温め、目を覆って20秒休める。眼精疲労時の手軽な休息法。視力回復をうたう動画も多いが、ここでは「休める」目的に限定。",
        en: "Rub palms warm, cup them over closed eyes for 20s. A simple rest for eye fatigue. Many videos claim 'vision recovery' — we limit this to 'resting' only."
      },
      steps: [
        { ja: "手のひらをこすって温める。", en: "Rub palms together to warm them." },
        { ja: "目を閉じ、押さえずにふんわり覆って20秒。", en: "Close eyes; cover gently (no pressure) for 20s." }
      ],
      caution: { ja: "眼球を押さない。視力回復の治療ではない。", en: "Never press the eyeball. This is not a vision-recovery treatment." },
      source: { type: "link", label: "生活のコツ (short)", url: "https://example.com/source/palming" },
      evidence: { level: "anecdotal", note: { ja: "休息としては妥当。視力が戻る根拠はない。", en: "Reasonable as rest; no evidence vision is restored." } },
      review: { status: "unreviewed", by: null },
      minutes: 1, tags: ["眼精疲労", "休憩"],
      stats: { tried: 3050, resonated: 1820, notHelpful: 360 }
    },
    {
      id: "eyes-2020", genreId: "eyes", contributorId: "mei", origin: "JP",
      title: { ja: "20-20-20ルールで目を守る", en: "The 20-20-20 rule for screens" },
      summary: {
        ja: "20分ごとに20フィート（約6m）先を20秒見る、という眼科でも案内される習慣。地味だが根拠のある王道。",
        en: "Every 20 minutes, look 20 feet (≈6m) away for 20 seconds — a habit eye clinics often recommend. Unflashy but evidence-backed."
      },
      steps: [
        { ja: "20分ごとにタイマー。", en: "Set a timer every 20 minutes." },
        { ja: "遠くを20秒ぼんやり見る。", en: "Gaze ~6m away for 20 seconds." }
      ],
      caution: { ja: "症状が続く場合は眼科へ。", en: "See an eye doctor if symptoms persist." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/202020" },
      evidence: { level: "study", note: { ja: "デジタル眼精疲労の対策として広く推奨される。", en: "Widely recommended for digital eye strain." } },
      review: { status: "expert", by: "mei" },
      minutes: 1, tags: ["習慣", "デスクワーク"],
      stats: { tried: 5400, resonated: 3980, notHelpful: 290 }
    },
    {
      id: "sleep-478", genreId: "sleep", contributorId: "sora", origin: "US",
      title: { ja: "4-7-8呼吸で眠りに入る", en: "4-7-8 breathing to fall asleep" },
      summary: {
        ja: "4秒吸って7秒止め、8秒かけて吐く呼吸法。海外（米）で広まった入眠ルーティンを、安全に紹介。",
        en: "Inhale 4s, hold 7s, exhale 8s. A sleep-onset routine popularized overseas (US), shared safely."
      },
      steps: [
        { ja: "鼻から4秒吸う。", en: "Inhale through the nose for 4s." },
        { ja: "7秒止める。", en: "Hold for 7s." },
        { ja: "口から8秒吐く。4サイクル。", en: "Exhale through the mouth for 8s. 4 cycles." }
      ],
      caution: { ja: "息苦しさを感じたら通常呼吸へ。", en: "Return to normal breathing if uncomfortable." },
      source: { type: "link", label: "Sleep routine (short)", url: "https://example.com/source/478" },
      evidence: { level: "expert", note: { ja: "リラックス反応を促すとされるが、入眠効果の決定的研究は少ない。", en: "Thought to aid relaxation; definitive sleep studies are scarce." } },
      review: { status: "expert", by: "sora" },
      minutes: 2, tags: ["入眠", "海外発掘", "呼吸"],
      stats: { tried: 6100, resonated: 4020, notHelpful: 720 }
    },
    {
      id: "sleep-light", genreId: "sleep", contributorId: "mei", origin: "JP",
      title: { ja: "朝に光を浴びて体内時計を整える", en: "Morning light to reset your body clock" },
      summary: {
        ja: "起床後すぐ屋外の光を浴びると、夜の眠りが整いやすい。睡眠科学で土台とされる習慣。",
        en: "Getting outdoor light right after waking helps nighttime sleep settle. A foundation habit in sleep science."
      },
      steps: [
        { ja: "起床後30分以内に外の光を5〜15分。", en: "Get outdoor light for 5–15 min within 30 min of waking." }
      ],
      caution: { ja: "直射日光を直視しない。", en: "Don't stare at the sun." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/morning-light" },
      evidence: { level: "study", note: { ja: "概日リズム調整に関する研究の裏付けが厚い。", en: "Strongly supported by circadian-rhythm research." } },
      review: { status: "expert", by: "mei" },
      minutes: 10, tags: ["体内時計", "習慣"],
      stats: { tried: 3300, resonated: 2510, notHelpful: 180 }
    },
    {
      id: "home-fold", genreId: "home", contributorId: "marie", origin: "FR",
      title: { ja: "Tシャツを3秒でたたむ", en: "Fold a T-shirt in 3 seconds" },
      summary: {
        ja: "肩と裾をつまんで一気にたたむ収納術。海外の収納マスター動画の定番を、写真なしで手順だけ紹介。",
        en: "Pinch shoulder and hem, flip once. A staple from overseas tidying creators, described as steps only."
      },
      steps: [
        { ja: "Tシャツを平らに置く。", en: "Lay the shirt flat." },
        { ja: "肩口と同じ側の裾をつまみ、交差させて持ち上げる。", en: "Pinch the shoulder and the hem on the same side, cross, lift." },
        { ja: "ふって整える。", en: "Shake to straighten." }
      ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "百万人級の収納 (short)", url: "https://example.com/source/fold" },
      evidence: { level: "none", note: { ja: "健康とは無関係の生活術。効果検証の対象外。", en: "A life hack, not health-related; no efficacy claim." } },
      review: { status: "unreviewed", by: null },
      minutes: 1, tags: ["収納", "海外発掘", "時短"],
      stats: { tried: 7200, resonated: 5100, notHelpful: 640 }
    },
    {
      id: "home-bottle", genreId: "home", contributorId: "leo", origin: "JP",
      title: { ja: "水筒のパッキン汚れを重曹で落とす", en: "Clean bottle gaskets with baking soda" },
      summary: {
        ja: "重曹をぬるま湯に溶かして数分つけ置きし、細部の汚れをゆるめる方法。",
        en: "Soak gaskets in warm water with baking soda for a few minutes to loosen grime."
      },
      steps: [
        { ja: "ぬるま湯に重曹を小さじ1溶かす。", en: "Dissolve 1 tsp baking soda in warm water." },
        { ja: "パッキンを5分つけ、ブラシで軽くこする。", en: "Soak gaskets 5 min, brush gently." }
      ],
      caution: { ja: "素材により変色することがある。表示を確認。", en: "May discolor some materials; check labels." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/bottle" },
      evidence: { level: "anecdotal", note: { ja: "家事のコツ。健康効能の主張なし。", en: "A cleaning tip; no health claim." } },
      review: { status: "unreviewed", by: null },
      minutes: 6, tags: ["掃除", "重曹"],
      stats: { tried: 1900, resonated: 1280, notHelpful: 210 }
    },
    {
      id: "saving-fridge", genreId: "saving", contributorId: "ken", origin: "JP",
      title: { ja: "冷蔵庫の整理で食品ロスと電気代を減らす", en: "Organize the fridge to cut waste & power" },
      summary: {
        ja: "詰め込みすぎを避け、見える化することで食品ロスと無駄買いを減らす。冷気の循環で効率も上がりやすい。",
        en: "Avoid overpacking and make items visible to cut food waste and impulse buys. Better airflow can improve efficiency."
      },
      steps: [
        { ja: "「すぐ食べる」棚を1段つくる。", en: "Make one 'eat soon' shelf." },
        { ja: "詰め込みは7割までを目安に。", en: "Keep it about 70% full." }
      ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "生活のコツ (short)", url: "https://example.com/source/fridge" },
      evidence: { level: "expert", note: { ja: "省エネ・食品ロス削減の一般的な助言と整合。", en: "Consistent with common energy/food-waste advice." } },
      review: { status: "unreviewed", by: null },
      minutes: 15, tags: ["節約", "食品ロス"],
      stats: { tried: 2600, resonated: 1700, notHelpful: 240 }
    },
    {
      id: "saving-standby", genreId: "saving", contributorId: "ken", origin: "JP",
      title: { ja: "待機電力をまとめてオフ", en: "Kill standby power in one switch" },
      summary: {
        ja: "使っていない機器のコンセントを電源タップでまとめて切る、地味だが効く節電。",
        en: "Switch off unused devices together via a power strip — a small but real saving."
      },
      steps: [
        { ja: "テレビ周りなどをタップに集約。", en: "Group TV-area devices on one strip." },
        { ja: "外出・就寝時にまとめてオフ。", en: "Switch off when out or asleep." }
      ],
      caution: { ja: "録画機器や冷蔵庫など切ってはいけない物に注意。", en: "Don't cut power to recorders, fridges, etc." },
      source: { type: "link", label: "節約のコツ (short)", url: "https://example.com/source/standby" },
      evidence: { level: "study", note: { ja: "待機電力削減は消費電力低減として確認されている。", en: "Reducing standby power is a confirmed way to cut consumption." } },
      review: { status: "unreviewed", by: null },
      minutes: 10, tags: ["節電", "固定費"],
      stats: { tried: 4100, resonated: 3050, notHelpful: 300 }
    }
  ];

  window.APP_DATA = { genres: genres, contributors: contributors, contents: contents };
})();
