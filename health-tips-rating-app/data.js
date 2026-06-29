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
    { id: "legs",    name: { ja: "脚・むくみ",   en: "Legs & Swelling" }, icon: "🦶", color: "#2f9e8f" },
    { id: "stomach", name: { ja: "お腹・胃腸",   en: "Belly & Digestion" }, icon: "🫄", color: "#b8703a" },
    { id: "antiaging", name: { ja: "アンチエイジング", en: "Anti-aging" },  icon: "✨", color: "#c25b86" },
    { id: "brain",   name: { ja: "脳・認知ケア", en: "Brain & Cognition" }, icon: "🧠", color: "#4a86b8" },
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
      bio: { ja: "ムリなく続く節約の工夫。",              en: "Saving tips you can actually keep up." } },
    { id: "jin",    name: "Jin",        origin: "KR", color: "#5161b8",
      bio: { ja: "韓国発のセルフケア・美容健康法を紹介。",  en: "Self-care and wellness tips from Korea." } },
    { id: "ananya", name: "Ananya",     origin: "IN", color: "#b8703a", expert: true,
      bio: { ja: "ヨガ講師。アーユルヴェーダの暮らしの知恵。", en: "Yoga teacher. Everyday Ayurvedic wisdom." } },
    { id: "noi",    name: "Noi",        origin: "TH", color: "#2f9e8f",
      bio: { ja: "タイ式のリラックス・ストレッチを発信。",  en: "Thai-style relaxation and stretching." } },
    { id: "aki",    name: "Dr. Aki",    origin: "JP", color: "#4a86b8", expert: true,
      bio: { ja: "老年医学。脳と体の健康づくりを発信。",    en: "Geriatrician. Brain & body healthy-aging tips." } },
    { id: "emma",   name: "Emma",       origin: "US", color: "#c25b86",
      bio: { ja: "フェイスヨガ等のアンチエイジング習慣。",  en: "Anti-aging habits incl. face yoga." } }
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
    },

    // ── セルフケア拡充（首・肩） ──
    {
      id: "neck-scapula", genreId: "neck", contributorId: "mei", origin: "JP",
      title: { ja: "肩甲骨はがしで肩まわりを動かす", en: "Scapula mobility for stiff shoulders" },
      summary: {
        ja: "ひじを曲げて肩で大きく円を描き、肩甲骨を動かす運動。デスクワークで固まった肩まわりの可動域を広げる狙い。理学療法士の監修付き。",
        en: "Bend the elbows and draw big circles with the shoulders to move the shoulder blades. Aims to restore range of motion stiffened by desk work. Physiotherapist-reviewed."
      },
      steps: [
        { ja: "指先を肩に乗せ、ひじで大きく前回し10回。", en: "Fingertips on shoulders; circle elbows forward 10 times." },
        { ja: "後ろ回し10回。肩甲骨を寄せる意識で。", en: "Circle backward 10 times, squeezing the shoulder blades." }
      ],
      caution: { ja: "肩に痛みが出る角度は避ける。", en: "Avoid any angle that causes shoulder pain." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/scapula" },
      evidence: { level: "study", note: { ja: "肩の可動域運動は肩こりの自覚症状軽減に資する報告がある。", en: "Shoulder mobility exercise is reported to ease perceived stiffness." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["肩甲骨", "デスクワーク"],
      stats: { tried: 3600, resonated: 2680, notHelpful: 240 }
    },
    {
      id: "neck-chin-tuck", genreId: "neck", contributorId: "mei", origin: "US",
      title: { ja: "あご引き（チンタック）でスマホ首ケア", en: "Chin tucks for 'tech neck'" },
      summary: {
        ja: "あごを軽く引いて首の深層筋を働かせる、海外（米）の理学療法でも定番のエクササイズ。前に出た頭の位置を整える狙い。",
        en: "Gently draw the chin back to engage deep neck muscles — a staple in US physical therapy. Aims to correct a forward head posture."
      },
      steps: [
        { ja: "背すじを伸ばし、あごを水平に後ろへ引く（二重あごを作る）。", en: "Sit tall; pull the chin straight back (make a double chin)." },
        { ja: "5秒キープ×10回。痛みのない範囲で。", en: "Hold 5s × 10, within a pain-free range." }
      ],
      caution: { ja: "めまい・しびれが出たら中止。", en: "Stop if you feel dizzy or numb." },
      source: { type: "link", label: "Posture care (short)", url: "https://example.com/source/chin-tuck" },
      evidence: { level: "study", note: { ja: "頸部深層屈筋トレは首の不調軽減のエビデンスが比較的厚い。", en: "Deep neck flexor training has relatively solid evidence for neck relief." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["スマホ首", "姿勢", "海外発掘"],
      stats: { tried: 2900, resonated: 2210, notHelpful: 190 }
    },
    {
      id: "neck-ear-roll", genreId: "neck", contributorId: "jin", origin: "KR",
      title: { ja: "耳まわし＆首ストレッチで巡りを促す", en: "Ear rolls & neck stretch for circulation" },
      summary: {
        ja: "耳を軽くつまんで回し、首をゆっくり倒すリラックス法。韓国のセルフケア動画で人気の組み合わせを、安全な範囲で紹介。",
        en: "Pinch and roll the ears, then slowly tilt the neck — a relaxation combo popular in Korean self-care videos, shared within a safe range."
      },
      steps: [
        { ja: "耳の上・中・下をつまんで外へ軽く引き、5回ずつ回す。", en: "Pinch top/middle/lobe, pull out gently, roll 5× each." },
        { ja: "首を左右にゆっくり倒し、各10秒。", en: "Slowly tilt the neck side to side, 10s each." }
      ],
      caution: { ja: "強く引っぱらない。痛みが出たら中止。", en: "Don't pull hard. Stop if it hurts." },
      source: { type: "link", label: "셀프케어 (short)", url: "https://example.com/source/ear-roll" },
      evidence: { level: "anecdotal", note: { ja: "リラックス目的のセルフケア。医学的効果の主張は控えめに。", en: "Self-care for relaxation; medical claims are kept modest." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["リラックス", "海外発掘"],
      stats: { tried: 5300, resonated: 3100, notHelpful: 900 }
    },

    // ── セルフケア拡充（腰・お尻） ──
    {
      id: "back-cat-cow", genreId: "back", contributorId: "ananya", origin: "IN",
      title: { ja: "キャット&カウで背骨をしなやかに", en: "Cat–Cow to loosen the spine" },
      summary: {
        ja: "四つばいで背中を丸める・反らすを繰り返すヨガの基本。インド発のポーズで、こわばった背中〜腰をやさしく動かす。ヨガ講師の監修付き。",
        en: "On all fours, round and arch the back — a yoga basic from India. Gently mobilizes a stiff back and lower spine. Reviewed by a yoga teacher."
      },
      steps: [
        { ja: "四つばいになり、息を吐きながら背中を丸める。", en: "On all fours, exhale and round the back." },
        { ja: "息を吸いながら反らす。ゆっくり10往復。", en: "Inhale and arch. Slowly, 10 rounds." }
      ],
      caution: { ja: "手首・膝が痛い場合はタオルを敷く。反らしすぎない。", en: "Pad wrists/knees if sore. Don't over-arch." },
      source: { type: "link", label: "Yoga basics (short)", url: "https://example.com/source/cat-cow" },
      evidence: { level: "expert", note: { ja: "腰の不快感に対する軽い可動運動として広く勧められる。", en: "Widely recommended as gentle mobility for low-back discomfort." } },
      review: { status: "expert", by: "ananya" },
      minutes: 3, tags: ["ヨガ", "背骨", "海外発掘"],
      stats: { tried: 4400, resonated: 3200, notHelpful: 360 }
    },
    {
      id: "back-piriformis", genreId: "back", contributorId: "mei", origin: "JP",
      title: { ja: "お尻（梨状筋）ストレッチで腰を楽に", en: "Glute (piriformis) stretch for the lower back" },
      summary: {
        ja: "あおむけで足を組み、太ももを抱えてお尻を伸ばすストレッチ。座りっぱなしで固まるお尻まわりをゆるめ、腰の負担感をやわらげる狙い。",
        en: "Lying down, cross one ankle over the knee and hug the thigh to stretch the glutes. Aims to release a seated-stiff backside and ease the lower back."
      },
      steps: [
        { ja: "あおむけで右足首を左ひざに乗せる。", en: "On your back, place the right ankle on the left knee." },
        { ja: "左ももを抱えて手前に引き、30秒。左右おこなう。", en: "Hug the left thigh toward you, 30s. Do both sides." }
      ],
      caution: { ja: "股関節・膝に痛みがあれば無理をしない。", en: "Don't push if hips or knees hurt." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/piriformis" },
      evidence: { level: "study", note: { ja: "殿筋ストレッチは坐骨神経まわりの不快感緩和に用いられる。", en: "Glute stretches are used to ease discomfort around the sciatic area." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["ストレッチ", "坐骨"],
      stats: { tried: 2700, resonated: 1980, notHelpful: 240 }
    },

    // ── セルフケア拡充（目） ──
    {
      id: "eyes-jingming", genreId: "eyes", contributorId: "chen", origin: "CN",
      title: { ja: "目頭のツボ「晴明」を軽く押す", en: "Press the Jingming point by the eye" },
      summary: {
        ja: "目頭の少し上のくぼみ（晴明）を指でやさしく押す、中医で目の疲れに使われる定番。海外（中国）で広く紹介される方法を、強く押さない範囲で。",
        en: "Gently press the small hollow by the inner eye (Jingming/BL1), a staple in Chinese medicine for eye fatigue. Shared without pressing hard."
      },
      steps: [
        { ja: "目を閉じ、目頭のくぼみを指の腹で5秒押す×3。", en: "Eyes closed; press the inner-eye hollow with a fingertip 5s × 3." }
      ],
      caution: { ja: "眼球を押さない。爪を立てない。コンタクトは外す。", en: "Never press the eyeball. No nails. Remove contacts." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/jingming" },
      evidence: { level: "expert", note: { ja: "経穴指圧として一般的。視力改善の根拠ではなく休息目的。", en: "Common acupressure; for rest, not as proof of vision improvement." } },
      review: { status: "expert", by: "chen" },
      minutes: 1, tags: ["ツボ", "眼精疲労", "海外発掘"],
      stats: { tried: 3800, resonated: 2450, notHelpful: 520 }
    },

    // ── 脚・むくみ（新ジャンル） ──
    {
      id: "legs-calf-pump", genreId: "legs", contributorId: "mei", origin: "JP",
      title: { ja: "かかと上げでふくらはぎポンプ", en: "Calf raises as a 'second heart' pump" },
      summary: {
        ja: "立って、または座ってかかとを上げ下げし、ふくらはぎの筋ポンプで脚の巡りを促す。長時間同じ姿勢のむくみ対策に。",
        en: "Raise and lower the heels (standing or seated) to use the calf muscle pump and aid leg circulation. For swelling from long static postures."
      },
      steps: [
        { ja: "かかとをゆっくり上げて2秒キープ、下ろす。", en: "Slowly raise heels, hold 2s, lower." },
        { ja: "20回。デスクの下でもOK。", en: "20 reps. Works under a desk too." }
      ],
      caution: { ja: "ふらつく場合は壁や机につかまる。", en: "Hold a wall or desk if unsteady." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/calf-pump" },
      evidence: { level: "study", note: { ja: "下腿の筋ポンプは静脈還流を助けることが知られている。", en: "The calf muscle pump is known to aid venous return." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["むくみ", "デスクワーク"],
      stats: { tried: 4600, resonated: 3500, notHelpful: 300 }
    },
    {
      id: "legs-ankle-thai", genreId: "legs", contributorId: "noi", origin: "TH",
      title: { ja: "足首回し＆足裏ほぐしで脚すっきり", en: "Ankle rolls & foot release for tired legs" },
      summary: {
        ja: "足首をゆっくり回し、足裏を手でほぐすタイ式のリラックス法。一日歩いて疲れた脚を、寝る前にやさしくケア。",
        en: "Slowly roll the ankles and knead the soles — a Thai-style relaxation. Gentle care for legs tired after a day of walking, before bed."
      },
      steps: [
        { ja: "足首を内回し・外回し各10回。", en: "Roll each ankle inward/outward 10 times." },
        { ja: "親指で足裏を心地よい強さで30秒ほぐす。", en: "Knead the sole with the thumb at a pleasant pressure for 30s." }
      ],
      caution: { ja: "強く押しすぎない。傷や炎症がある所は避ける。", en: "Don't over-press. Avoid wounds or inflamed areas." },
      source: { type: "link", label: "ผ่อนคลาย (short)", url: "https://example.com/source/ankle-thai" },
      evidence: { level: "anecdotal", note: { ja: "リラックス目的。むくみ解消の医学的主張は控えめに。", en: "For relaxation; medical claims about swelling kept modest." } },
      review: { status: "unreviewed", by: null },
      minutes: 3, tags: ["リラックス", "海外発掘", "就寝前"],
      stats: { tried: 6200, resonated: 3900, notHelpful: 980 }
    },

    // ── お腹・胃腸（新ジャンル） ──
    {
      id: "stomach-warm-water", genreId: "stomach", contributorId: "ananya", origin: "IN",
      title: { ja: "朝いちばんに白湯をゆっくり飲む", en: "Sip warm water first thing in the morning" },
      summary: {
        ja: "起き抜けにコップ一杯の白湯（さゆ）をゆっくり飲む、アーユルヴェーダの定番習慣。胃腸をやさしく目覚めさせ、水分補給にもなる。",
        en: "Slowly drink a cup of warm water on waking — a classic Ayurvedic habit from India. Gently wakes the gut and rehydrates."
      },
      steps: [
        { ja: "やかんで沸かし、飲める温度（50℃前後）まで冷ます。", en: "Boil, then cool to a drinkable ~50°C." },
        { ja: "起床後にゆっくり一杯飲む。", en: "Sip one cup after waking." }
      ],
      caution: { ja: "やけどに注意。持病がある場合は主治医に相談。", en: "Avoid burns. Ask your doctor if you have a condition." },
      source: { type: "link", label: "Ayurveda daily (short)", url: "https://example.com/source/warm-water" },
      evidence: { level: "anecdotal", note: { ja: "水分補給は妥当。白湯特有の効能は科学的根拠が限定的。", en: "Hydration is sensible; specific 'warm-water' benefits have limited evidence." } },
      review: { status: "unreviewed", by: null },
      minutes: 5, tags: ["朝習慣", "海外発掘", "水分補給"],
      stats: { tried: 8100, resonated: 4200, notHelpful: 1900 }
    },
    {
      id: "stomach-wind-pose", genreId: "stomach", contributorId: "ananya", origin: "IN",
      title: { ja: "ガス抜きのポーズでお腹を楽に", en: "Knees-to-chest 'wind-relieving' pose" },
      summary: {
        ja: "あおむけで両膝を抱えてお腹を軽く圧迫するヨガのポーズ。張った感じのお腹をやさしくケアする。ヨガ講師の監修付き。",
        en: "Lying on your back, hug both knees to gently compress the belly — a yoga pose. Soothes a bloated-feeling stomach. Reviewed by a yoga teacher."
      },
      steps: [
        { ja: "あおむけで両膝を抱え、胸に引き寄せる。", en: "On your back, hug both knees toward the chest." },
        { ja: "ゆっくり呼吸しながら20〜30秒。", en: "Breathe slowly for 20–30s." }
      ],
      caution: { ja: "食後すぐは避ける。妊娠中・腹部手術後は控える。", en: "Avoid right after meals, during pregnancy, or post-abdominal surgery." },
      source: { type: "link", label: "Yoga for digestion (short)", url: "https://example.com/source/wind-pose" },
      evidence: { level: "expert", note: { ja: "軽い腹部ストレッチとして一般的。強い効能はうたわない。", en: "Common as a gentle abdominal stretch; no strong efficacy claim." } },
      review: { status: "expert", by: "ananya" },
      minutes: 2, tags: ["ヨガ", "お腹の張り", "海外発掘"],
      stats: { tried: 3400, resonated: 2300, notHelpful: 420 }
    },

    // ── アンチエイジング（新ジャンル） ──
    {
      id: "antiaging-slow-squat", genreId: "antiaging", contributorId: "mei", origin: "JP",
      title: { ja: "スロースクワットで「筋肉貯金」", en: "Slow squats to bank muscle for later life" },
      summary: {
        ja: "イスから立つ動作をゆっくり行う筋トレ。年齢とともに減りやすい下半身の筋肉を保ち、代謝や姿勢の土台を守る狙い。若々しさは筋肉量から、という考え方。",
        en: "Stand up from a chair slowly to train the legs. Aims to preserve lower-body muscle that declines with age, supporting metabolism and posture. Youthfulness starts with muscle."
      },
      steps: [
        { ja: "イスの前に立ち、4秒かけてゆっくり腰を下ろす。", en: "Stand before a chair; lower over 4 seconds." },
        { ja: "座る直前で止め、4秒で立つ。10回。", en: "Pause just above the seat, rise over 4s. 10 reps." }
      ],
      caution: { ja: "膝に痛みが出たら中止。ふらつく場合は手すりを使う。", en: "Stop if knees hurt. Use a rail if unsteady." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/slow-squat" },
      evidence: { level: "study", note: { ja: "加齢に伴う筋力低下の予防に筋トレが有効とする研究は厚い。", en: "Strength training is well-supported for preventing age-related muscle loss." } },
      review: { status: "expert", by: "mei" },
      minutes: 3, tags: ["筋トレ", "代謝", "サルコペニア予防"],
      stats: { tried: 5200, resonated: 3900, notHelpful: 360 }
    },
    {
      id: "antiaging-interval-walk", genreId: "antiaging", contributorId: "aki", origin: "JP",
      title: { ja: "インターバル速歩（速い・ゆっくりを交互）", en: "Interval walking (fast/slow alternating)" },
      summary: {
        ja: "「ややきつい速歩き3分→ゆっくり3分」を繰り返すウォーキング。日本の研究（信州大）で体力・生活習慣の指標改善が報告された、中高年に人気の方法。",
        en: "Alternate 3 min of brisk walking with 3 min easy. A method popular with midlife adults; Japanese research (Shinshu Univ.) reported gains in fitness and health markers."
      },
      steps: [
        { ja: "ややきつい速歩きを3分。", en: "Walk briskly (somewhat hard) for 3 min." },
        { ja: "ゆっくり歩きを3分。これを5セット、週4日が目安。", en: "Walk easy for 3 min. 5 sets, ~4 days/week." }
      ],
      caution: { ja: "持病・関節痛がある場合は医師に相談。暑い日は無理をしない。", en: "Consult a doctor if you have conditions or joint pain. Don't overdo it in heat." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/interval-walk" },
      evidence: { level: "study", note: { ja: "体力向上・生活習慣指標の改善を示す研究がある。", en: "Studies show improved fitness and metabolic markers." } },
      review: { status: "expert", by: "aki" },
      minutes: 30, tags: ["ウォーキング", "体力", "中高年"],
      stats: { tried: 6400, resonated: 4700, notHelpful: 540 }
    },
    {
      id: "antiaging-face-yoga", genreId: "antiaging", contributorId: "emma", origin: "US",
      title: { ja: "フェイスヨガで表情筋を動かす", en: "Face yoga to work the facial muscles" },
      summary: {
        ja: "頬や口まわりの表情筋を意識して動かす海外（米）発の習慣。小規模な研究で頬のハリ感の改善が報告されたが、効果には個人差があり過度な期待は禁物。",
        en: "Deliberately exercise the cheek and mouth muscles — a habit from the US. A small study reported firmer cheeks, but results vary; keep expectations modest."
      },
      steps: [
        { ja: "口に空気を含み、左右の頬へ数秒ずつ移す×5。", en: "Puff air, shift it cheek to cheek a few seconds each ×5." },
        { ja: "「あ・い・う・え・お」と大きく口を動かす×5。", en: "Mouth big vowels A-I-U-E-O ×5." }
      ],
      caution: { ja: "肌を強くこすらない。痛みや違和感が出たら中止。", en: "Don't rub the skin hard. Stop if uncomfortable." },
      source: { type: "link", label: "Face yoga (short)", url: "https://example.com/source/face-yoga" },
      evidence: { level: "anecdotal", note: { ja: "小規模研究はあるが根拠は限定的。体感の個人差が大きい。", en: "A small study exists but evidence is limited; experiences vary widely." } },
      review: { status: "unreviewed", by: null },
      minutes: 5, tags: ["表情筋", "海外発掘", "美容"],
      stats: { tried: 9200, resonated: 4600, notHelpful: 2400 }
    },
    {
      id: "antiaging-tongue-roll", genreId: "antiaging", contributorId: "jin", origin: "KR",
      title: { ja: "舌回し体操で口元・だ液ケア", en: "Tongue-rolling for the mouth area & saliva" },
      summary: {
        ja: "口を閉じて舌で歯ぐきの外側をぐるりとなぞる体操。口まわりの筋肉を動かし、だ液の分泌を促す狙い。韓国・日本のセルフケア動画で定番。",
        en: "With lips closed, sweep the tongue around the outside of the gums. Aims to work the mouth muscles and encourage saliva. A staple in Korean/Japanese self-care videos."
      },
      steps: [
        { ja: "口を閉じ、舌で歯の外側を右回り20回。", en: "Lips closed; circle the tongue outside the teeth, 20× clockwise." },
        { ja: "左回り20回。", en: "20× counter-clockwise." }
      ],
      caution: { ja: "顎に痛みが出たら回数を減らす。", en: "Reduce reps if the jaw hurts." },
      source: { type: "link", label: "셀프케어 (short)", url: "https://example.com/source/tongue-roll" },
      evidence: { level: "anecdotal", note: { ja: "口腔機能の体操として紹介される。効能の研究は限定的。", en: "Shared as an oral-function exercise; efficacy research is limited." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["口元", "海外発掘", "だ液"],
      stats: { tried: 7100, resonated: 3800, notHelpful: 1600 }
    },

    // ── 脳・認知ケア（新ジャンル / 認知症予防への関心） ──
    {
      id: "brain-cognicise", genreId: "brain", contributorId: "aki", origin: "JP",
      title: { ja: "コグニサイズ（運動＋頭の課題を同時に）", en: "Cognicise: move and think at the same time" },
      summary: {
        ja: "足踏みやステップをしながら計算やしりとりを行う「ながら運動」。日本の研究機関（国立長寿医療研究センター）が考案。認知機能の維持に役立つ可能性が研究されている。",
        en: "Step or march while doing math or word games — exercise plus a mental task. Developed by Japan's NCGG; studied for its potential to help maintain cognitive function."
      },
      steps: [
        { ja: "その場で足踏みしながら3の倍数で手をたたく。", en: "March in place; clap on every multiple of 3." },
        { ja: "慣れたらステップ＋しりとりなど課題を変える。", en: "Once used to it, switch tasks (e.g. step + word chain)." }
      ],
      caution: { ja: "転倒に注意し、安全な場所で。持病があれば医師に相談。", en: "Mind your footing; do it somewhere safe. Ask a doctor if you have conditions." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/cognicise" },
      evidence: { level: "study", note: { ja: "運動＋認知課題（デュアルタスク）と認知機能維持の関連を示す研究がある。発症を防ぐと断定はできない。", en: "Studies link dual-task exercise to maintained cognition; it cannot be claimed to 'prevent' disease." } },
      review: { status: "expert", by: "aki" },
      minutes: 10, tags: ["認知症予防", "デュアルタスク", "ながら運動"],
      stats: { tried: 7800, resonated: 5600, notHelpful: 680 }
    },
    {
      id: "brain-aerobic", genreId: "brain", contributorId: "aki", origin: "US",
      title: { ja: "有酸素運動で脳の健康を守る", en: "Aerobic exercise to protect brain health" },
      summary: {
        ja: "週に数回の早歩きなどの有酸素運動。海外の大規模研究で、習慣的な運動と認知症リスク低下や記憶に関わる脳領域の維持との関連が報告されている。",
        en: "Brisk walking and similar, several times a week. Large overseas studies link habitual exercise to lower dementia risk and preservation of memory-related brain regions."
      },
      steps: [
        { ja: "早歩きなど中強度の有酸素運動を1回20〜30分。", en: "20–30 min of moderate aerobic exercise like brisk walking." },
        { ja: "週に3〜5回を目安に続ける。", en: "Aim for 3–5 times a week." }
      ],
      caution: { ja: "心臓・関節に不安がある場合は医師に相談してから。", en: "Check with a doctor first if you have heart or joint concerns." },
      source: { type: "link", label: "Brain health (short)", url: "https://example.com/source/aerobic-brain" },
      evidence: { level: "study", note: { ja: "運動習慣と認知症リスク低下の関連を示す研究は多い（関連であり、確実な予防ではない）。", en: "Many studies associate exercise with lower dementia risk (association, not guaranteed prevention)." } },
      review: { status: "expert", by: "aki" },
      minutes: 25, tags: ["認知症予防", "有酸素", "海外発掘"],
      stats: { tried: 6900, resonated: 5100, notHelpful: 620 }
    },
    {
      id: "brain-finger", genreId: "brain", contributorId: "aki", origin: "JP",
      title: { ja: "指先の体操で脳に刺激", en: "Finger exercises to stimulate the brain" },
      summary: {
        ja: "左右の手で違う動きをする、利き手と逆の手を使うなど、指先を細かく動かす体操。脳への刺激として手軽に取り入れられるが、認知症予防の効果は断定できない。",
        en: "Move the fingers in fine, differing patterns (or use your non-dominant hand). An easy way to stimulate the brain, though effects on dementia can't be claimed."
      },
      steps: [
        { ja: "片手はグー・パー、もう片手は1本ずつ折る、を交互に。", en: "One hand fist/open, the other folds fingers one by one; alternate." },
        { ja: "歯みがきや箸を逆の手で試す。", en: "Try brushing teeth or chopsticks with the non-dominant hand." }
      ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/finger-brain" },
      evidence: { level: "expert", note: { ja: "脳トレ的な刺激として紹介される。予防効果の強い根拠はない。", en: "Shared as brain stimulation; no strong evidence of a preventive effect." } },
      review: { status: "expert", by: "aki" },
      minutes: 3, tags: ["脳トレ", "指先", "すきま時間"],
      stats: { tried: 5400, resonated: 3500, notHelpful: 760 }
    }
  ];

  window.APP_DATA = { genres: genres, contributors: contributors, contents: contents };
})();
