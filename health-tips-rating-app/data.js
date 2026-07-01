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
    { id: "head",    name: { ja: "頭痛",         en: "Headache" },        icon: "🤕", color: "#b8584a" },
    { id: "skin",    name: { ja: "肌・髪",       en: "Skin & Hair" },     icon: "🧴", color: "#d18aa0" },
    { id: "mind",    name: { ja: "メンタル・ストレス", en: "Mind & Stress" }, icon: "🫧", color: "#5aa0b8" },
    { id: "diet",    name: { ja: "食事・栄養",   en: "Diet & Nutrition" }, icon: "🥗", color: "#6a9e3f" },
    { id: "immune",  name: { ja: "免疫・風邪",   en: "Immunity & Colds" }, icon: "🤧", color: "#c2913a" },
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
      bio: { ja: "フェイスヨガ等のアンチエイジング習慣。",  en: "Anti-aging habits incl. face yoga." } },
    { id: "hana",   name: "Dr. Hana",   origin: "JP", color: "#d18aa0", expert: true,
      bio: { ja: "皮膚科医。肌と髪のケア。",              en: "Dermatologist. Skin & hair care." } },
    { id: "mina",   name: "Dr. Mina",   origin: "JP", color: "#6a9e3f", expert: true,
      bio: { ja: "管理栄養士。食事と栄養の専門家。",      en: "Registered dietitian. Food & nutrition." } },
    { id: "yui",    name: "Dr. Yui",    origin: "JP", color: "#5aa0b8", expert: true,
      bio: { ja: "臨床心理士。ストレスとの付き合い方。",  en: "Clinical psychologist. Living with stress." } },
    { id: "tomo",   name: "Dr. Tomo",   origin: "JP", color: "#4a86b8", expert: true,
      bio: { ja: "歯科医。口と歯の健康づくり。",          en: "Dentist. Oral health." } },
    { id: "luca",   name: "Luca",       origin: "IT", color: "#6a9e3f",
      bio: { ja: "地中海式の食習慣を発信。",              en: "Shares Mediterranean eating habits." } }
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
      video: { youtube: "jCt0aF7yB8M", tiktok: "7263545390593592582" },
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
      video: { youtube: "SQGwEFuKWdo", tiktok: "7362734824198589712" },
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
      video: { youtube: "NzSUEn42NFs", tiktok: "7488290697167047941" },
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
      video: { youtube: "rpnrWCutLw8", tiktok: "7184727289484102913" },
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
    },

    // ── 首・肩こり（追加） ──
    {
      id: "neck-shrug", genreId: "neck", contributorId: "mei", origin: "JP",
      title: { ja: "肩すくめ＆ストンで肩こりリセット", en: "Shrug-and-drop to reset shoulders" },
      summary: { ja: "肩をぐっと持ち上げて一気に脱力する動き。力を入れて抜くことで、こり固まった肩の緊張をゆるめる狙い。",
                 en: "Lift the shoulders hard, then let them drop. Tensing and releasing aims to loosen tight shoulders." },
      steps: [ { ja: "息を吸いながら肩を耳に近づけ5秒。", en: "Inhale, raise shoulders toward ears for 5s." },
               { ja: "息を吐いてストンと脱力。5回。", en: "Exhale and drop. 5 times." } ],
      caution: { ja: "首に痛みが出たら中止。", en: "Stop if your neck hurts." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/shrug" },
      evidence: { level: "study", note: { ja: "筋緊張のセルフリリースとして一般的に勧められる。", en: "Commonly recommended as self-release for muscle tension." } },
      review: { status: "expert", by: "mei" },
      minutes: 1, tags: ["肩こり", "デスクワーク"],
      stats: { tried: 3100, resonated: 2300, notHelpful: 230 }
    },
    {
      id: "neck-hot-towel", genreId: "neck", contributorId: "leo", origin: "JP",
      title: { ja: "蒸しタオルで首肩を温める", en: "Warm towel on the neck & shoulders" },
      summary: { ja: "濡らして温めたタオルを首肩に当て、血流をうながして緊張をゆるめる定番ケア。",
                 en: "Lay a warm, damp towel on the neck and shoulders to encourage blood flow and ease tension." },
      steps: [ { ja: "濡らしたタオルを電子レンジで温める（熱すぎ注意）。", en: "Microwave a damp towel (not too hot)." },
               { ja: "首肩に5〜10分当てる。", en: "Apply to neck/shoulders for 5–10 min." } ],
      caution: { ja: "やけどに注意。炎症・腫れがある時は温めない。", en: "Avoid burns. Don't heat inflamed or swollen areas." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/hot-towel" },
      evidence: { level: "expert", note: { ja: "温熱は筋緊張の緩和に用いられる一般的な方法。", en: "Heat is a common approach to relieve muscle tension." } },
      review: { status: "unreviewed", by: null },
      minutes: 10, tags: ["温活", "肩こり"],
      stats: { tried: 4200, resonated: 3100, notHelpful: 400 }
    },

    // ── 腰・股関節（追加） ──
    {
      id: "back-pelvic-tilt", genreId: "back", contributorId: "mei", origin: "JP",
      title: { ja: "骨盤の傾け運動でこわばりをほどく", en: "Pelvic tilts to ease a stiff back" },
      summary: { ja: "あおむけ・ひざ立てで骨盤を前後にゆっくり傾ける運動。腰まわりを小さく動かしてこわばりをほどく。",
                 en: "Lying with knees up, slowly tilt the pelvis back and forth. Small movements ease lower-back stiffness." },
      steps: [ { ja: "あおむけでひざを立てる。", en: "Lie on your back, knees bent." },
               { ja: "腰を床に押しつける・反らすをゆっくり10回。", en: "Press the low back down, then arch, slowly ×10." } ],
      caution: { ja: "痛みの出る範囲では行わない。", en: "Don't move into painful ranges." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/pelvic-tilt" },
      evidence: { level: "study", note: { ja: "腰部の軽い可動運動として広く用いられる。", en: "Widely used as gentle lumbar mobility work." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["腰痛", "体幹"],
      stats: { tried: 2600, resonated: 1950, notHelpful: 250 }
    },
    {
      id: "back-prone-extension", genreId: "back", contributorId: "mei", origin: "US",
      title: { ja: "うつ伏せ上体反らしで腰をいたわる", en: "Prone press-up for the lower back" },
      summary: { ja: "うつ伏せでひじ立て、上体をゆっくり起こす海外（米）の理学療法で知られる動き。長く前かがみだった腰をやさしく反らす。",
                 en: "Lying face-down, prop on elbows and gently lift the upper body — known in US physical therapy. Gently extends a long-flexed back." },
      steps: [ { ja: "うつ伏せでひじを肩の下に置く。", en: "Face-down, elbows under shoulders." },
               { ja: "上体をゆっくり起こし数秒、戻す。10回。", en: "Lift the upper body a few seconds, lower. ×10." } ],
      caution: { ja: "脚へのしびれが出たら中止し受診を。", en: "Stop and see a doctor if numbness reaches the legs." },
      source: { type: "link", label: "Back care (short)", url: "https://example.com/source/prone-ext" },
      evidence: { level: "study", note: { ja: "一部の腰痛で症状軽減に用いられるが、合わない例もある。", en: "Used for some back pain, though not suitable for everyone." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["腰痛", "海外発掘"],
      stats: { tried: 3300, resonated: 2200, notHelpful: 520 }
    },

    // ── 目の疲れ（追加） ──
    {
      id: "eyes-blink", genreId: "eyes", contributorId: "mei", origin: "JP",
      title: { ja: "意識的なまばたきでドライアイ対策", en: "Conscious blinking for dry eyes" },
      summary: { ja: "画面に集中するとまばたきが減りがち。ゆっくり閉じて開くまばたきを意識して、目の乾きをやわらげる。",
                 en: "We blink less when glued to screens. Deliberate, full blinks help relieve dryness." },
      steps: [ { ja: "2秒かけてしっかり閉じ、開く×10。", en: "Close fully over 2s, then open ×10." } ],
      caution: { ja: "強い乾き・痛みが続くなら眼科へ。", en: "See an eye doctor if dryness or pain persists." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/blink" },
      evidence: { level: "expert", note: { ja: "ドライアイ対策として一般に案内される。", en: "Commonly advised for dry-eye relief." } },
      review: { status: "expert", by: "mei" },
      minutes: 1, tags: ["ドライアイ", "デスクワーク"],
      stats: { tried: 2400, resonated: 1700, notHelpful: 240 }
    },
    {
      id: "eyes-warm-towel", genreId: "eyes", contributorId: "sora", origin: "JP",
      title: { ja: "蒸しタオルで目元を温める", en: "Warm towel over the eyes" },
      summary: { ja: "温めたタオルを目の上にのせて休める方法。目元の血流をうながし、疲れ感をやわらげる。",
                 en: "Rest a warm towel over closed eyes. Encourages blood flow around the eyes and eases fatigue." },
      steps: [ { ja: "濡らしたタオルを温める（熱すぎ注意）。", en: "Warm a damp towel (not too hot)." },
               { ja: "目を閉じて上にのせ5分。", en: "Close eyes, lay it on for 5 min." } ],
      caution: { ja: "やけど注意。目の感染・炎症時は避ける。", en: "Avoid burns; skip if eyes are infected or inflamed." },
      source: { type: "link", label: "生活のコツ (short)", url: "https://example.com/source/eye-warm" },
      evidence: { level: "anecdotal", note: { ja: "休息・温熱としては妥当。視力改善の根拠ではない。", en: "Fine as warmth/rest; not evidence of vision improvement." } },
      review: { status: "unreviewed", by: null },
      minutes: 5, tags: ["眼精疲労", "温活", "就寝前"],
      stats: { tried: 3600, resonated: 2400, notHelpful: 420 }
    },

    // ── 睡眠（追加） ──
    {
      id: "sleep-bath", genreId: "sleep", contributorId: "sora", origin: "JP",
      title: { ja: "就寝90分前の入浴で寝つきを整える", en: "Bathe ~90 min before bed" },
      summary: { ja: "寝る1〜2時間前にぬるめのお風呂に入ると、その後の体温低下とともに眠気が訪れやすいとされる。",
                 en: "A warm bath 1–2 hours before bed; the following drop in body temperature is thought to invite sleepiness." },
      steps: [ { ja: "就寝90分前に38〜40℃で10〜15分入浴。", en: "Soak 10–15 min at 38–40°C, ~90 min before bed." } ],
      caution: { ja: "のぼせ・脱水に注意。熱すぎる湯は避ける。", en: "Avoid overheating/dehydration; skip very hot water." },
      source: { type: "link", label: "Sleep routine (short)", url: "https://example.com/source/bath" },
      evidence: { level: "study", note: { ja: "就寝前の入浴と寝つき改善の関連を示す研究がある。", en: "Studies link a pre-bed warm bath to easier sleep onset." } },
      review: { status: "expert", by: "sora" },
      minutes: 15, tags: ["入眠", "体温", "習慣"],
      stats: { tried: 5100, resonated: 3800, notHelpful: 480 }
    },
    {
      id: "sleep-box", genreId: "sleep", contributorId: "sora", origin: "US",
      title: { ja: "ボックス呼吸（4-4-4-4）で落ち着く", en: "Box breathing (4-4-4-4) to calm down" },
      summary: { ja: "4秒吸う・止める・吐く・止めるを繰り返す呼吸法。海外（米）で集中・リラックスに広く使われる。",
                 en: "Inhale, hold, exhale, hold — 4s each. Widely used overseas (US) for focus and calm." },
      steps: [ { ja: "4秒吸う→4秒止める。", en: "Inhale 4s → hold 4s." },
               { ja: "4秒吐く→4秒止める。4サイクル。", en: "Exhale 4s → hold 4s. 4 cycles." } ],
      caution: { ja: "息苦しさを感じたら通常呼吸へ。", en: "Return to normal breathing if uncomfortable." },
      source: { type: "link", label: "Calm routine (short)", url: "https://example.com/source/box" },
      evidence: { level: "expert", note: { ja: "リラックス反応を促すとされる。効果には個人差。", en: "Thought to trigger relaxation; effects vary." } },
      review: { status: "expert", by: "sora" },
      minutes: 2, tags: ["呼吸", "リラックス", "海外発掘"],
      stats: { tried: 5800, resonated: 3900, notHelpful: 700 }
    },
    {
      id: "sleep-no-screen", genreId: "sleep", contributorId: "aki", origin: "JP",
      title: { ja: "寝る前30分はスマホを置く", en: "Put the phone down 30 min before bed" },
      summary: { ja: "就寝前の強い光や情報刺激は眠りの妨げになりやすい。寝る30分前は画面を離れる習慣を。",
                 en: "Bright light and stimulating content before bed can disrupt sleep. Step away from screens 30 min before." },
      steps: [ { ja: "就寝30分前にスマホを別室や手の届かない所へ。", en: "Move the phone away 30 min before bed." },
               { ja: "読書やストレッチなど穏やかな活動に。", en: "Switch to calm activities like reading or stretching." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/no-screen" },
      evidence: { level: "study", note: { ja: "就寝前のスクリーン使用と睡眠の質低下の関連が報告される。", en: "Pre-bed screen use is linked to poorer sleep quality." } },
      review: { status: "expert", by: "aki" },
      minutes: 1, tags: ["習慣", "デジタル"],
      stats: { tried: 8800, resonated: 4300, notHelpful: 2600 }
    },

    // ── 脚・むくみ（追加） ──
    {
      id: "legs-elevate", genreId: "legs", contributorId: "mei", origin: "JP",
      title: { ja: "脚を心臓より高く上げて休める", en: "Elevate legs above the heart" },
      summary: { ja: "クッションに脚をのせ、心臓より高くして休む方法。重力で下にたまった血液・水分の戻りを助ける。",
                 en: "Rest with legs propped above heart level on a cushion. Helps blood and fluid that pooled by gravity return." },
      steps: [ { ja: "あおむけでクッションに脚をのせる。", en: "Lie down, rest legs on a cushion." },
               { ja: "10〜15分そのまま休む。", en: "Relax for 10–15 min." } ],
      caution: { ja: "しびれが出たら下ろす。持病がある人は医師に相談。", en: "Lower legs if numb. Consult a doctor if you have conditions." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/elevate" },
      evidence: { level: "expert", note: { ja: "むくみの一時的な軽減に一般的に勧められる。", en: "Commonly advised for temporary swelling relief." } },
      review: { status: "expert", by: "mei" },
      minutes: 12, tags: ["むくみ", "就寝前"],
      stats: { tried: 5600, resonated: 4200, notHelpful: 380 }
    },
    {
      id: "legs-calf-stretch", genreId: "legs", contributorId: "mei", origin: "JP",
      title: { ja: "ふくらはぎ伸ばしで脚を軽く", en: "Calf stretch for lighter legs" },
      summary: { ja: "壁に手をついて後ろ脚のふくらはぎを伸ばすストレッチ。歩き疲れた脚やこわばりをゆるめる。",
                 en: "Hands on a wall, stretch the back-leg calf. Eases tired, stiff legs after walking." },
      steps: [ { ja: "壁に手をつき片脚を後ろへ。かかとを床につけて20秒。", en: "Hand on wall, one leg back, heel down, 20s." },
               { ja: "左右おこなう。", en: "Do both sides." } ],
      caution: { ja: "痛みの手前で止める。", en: "Stop before pain." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/calf-stretch" },
      evidence: { level: "study", note: { ja: "ストレッチは柔軟性維持に有効とされる。", en: "Stretching is supported for maintaining flexibility." } },
      review: { status: "expert", by: "mei" },
      minutes: 2, tags: ["ストレッチ", "むくみ"],
      stats: { tried: 2900, resonated: 2100, notHelpful: 260 }
    },

    // ── お腹・胃腸（追加） ──
    {
      id: "stomach-fermented", genreId: "stomach", contributorId: "mina", origin: "JP",
      title: { ja: "発酵食品を毎日少しずつ", en: "A little fermented food every day" },
      summary: { ja: "ヨーグルト・納豆・みそなどの発酵食品を日々少量とる食習慣。腸内環境を意識した王道のアプローチ。",
                 en: "Have a little yogurt, natto, or miso daily. A classic, gut-minded eating habit." },
      steps: [ { ja: "1日1品、発酵食品を取り入れる。", en: "Include one fermented food per day." },
               { ja: "食物繊維と組み合わせるとなお良い。", en: "Pair with fiber for better effect." } ],
      caution: { ja: "塩分の摂りすぎに注意。アレルギーに留意。", en: "Watch salt intake; mind allergies." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/fermented" },
      evidence: { level: "study", note: { ja: "発酵食品と腸内環境に関する研究が進む（万能ではない）。", en: "Research on fermented foods and gut health is growing (not a cure-all)." } },
      review: { status: "expert", by: "mina" },
      minutes: 5, tags: ["腸活", "食習慣"],
      stats: { tried: 6200, resonated: 4300, notHelpful: 720 }
    },
    {
      id: "stomach-fiber-water", genreId: "stomach", contributorId: "mina", origin: "JP",
      title: { ja: "食物繊維と水分でお通じを整える", en: "Fiber + water for regularity" },
      summary: { ja: "野菜・海藻・果物などの食物繊維と、こまめな水分を意識する食習慣。お通じのリズムを整える土台。",
                 en: "Be mindful of fiber (vegetables, seaweed, fruit) and steady water intake — a foundation for regularity." },
      steps: [ { ja: "毎食、野菜や海藻を一品足す。", en: "Add a vegetable or seaweed dish each meal." },
               { ja: "水分をこまめにとる。", en: "Sip water throughout the day." } ],
      caution: { ja: "急な繊維の増やしすぎは張りの原因に。徐々に。", en: "Increasing fiber too fast can bloat; go gradually." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/fiber" },
      evidence: { level: "study", note: { ja: "食物繊維・水分と排便の関連は広く支持される。", en: "Fiber and fluids are well-supported for bowel regularity." } },
      review: { status: "expert", by: "mina" },
      minutes: 5, tags: ["腸活", "食習慣", "便秘"],
      stats: { tried: 4800, resonated: 3500, notHelpful: 520 }
    },

    // ── 家事・収納（追加） ──
    {
      id: "home-melamine", genreId: "home", contributorId: "leo", origin: "JP",
      title: { ja: "メラミンスポンジで水あか落とし", en: "Melamine sponge for water stains" },
      summary: { ja: "水で濡らしたメラミンスポンジで蛇口や鏡の水あかをこする掃除術。",
                 en: "Scrub water stains off taps and mirrors with a damp melamine sponge." },
      steps: [ { ja: "スポンジを水で濡らして軽く絞る。", en: "Wet the sponge and wring lightly." },
               { ja: "水あか部分をやさしくこする。", en: "Gently scrub the stained spot." } ],
      caution: { ja: "コーティングや光沢面は傷つくことがある。目立たない所で試す。", en: "May scratch coatings/glossy surfaces; test first." },
      source: { type: "link", label: "生活の裏技 (short)", url: "https://example.com/source/melamine" },
      evidence: { level: "none", note: { ja: "掃除術。健康効能の主張なし。", en: "A cleaning tip; no health claim." } },
      review: { status: "unreviewed", by: null },
      minutes: 5, tags: ["掃除", "水あか"],
      stats: { tried: 3400, resonated: 2500, notHelpful: 360 }
    },
    {
      id: "home-baking-deodor", genreId: "home", contributorId: "leo", origin: "JP",
      title: { ja: "重曹で靴箱・冷蔵庫の消臭", en: "Deodorize with baking soda" },
      summary: { ja: "小皿やコップに重曹を入れて置くだけのにおい対策。靴箱や冷蔵庫などこもりがちな場所に。",
                 en: "Leave baking soda in a small dish to tackle odors in shoe cabinets, fridges, and other stuffy spots." },
      steps: [ { ja: "重曹を小皿に入れて気になる場所に置く。", en: "Put baking soda in a dish where it smells." },
               { ja: "1〜2か月で取り替える。", en: "Replace every 1–2 months." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "生活のコツ (short)", url: "https://example.com/source/deodor" },
      evidence: { level: "anecdotal", note: { ja: "生活術。消臭効果は条件により差がある。", en: "A life hack; deodorizing varies by situation." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["消臭", "重曹"],
      stats: { tried: 2700, resonated: 1900, notHelpful: 300 }
    },

    // ── 節約（追加） ──
    {
      id: "saving-mealprep", genreId: "saving", contributorId: "ken", origin: "JP",
      title: { ja: "作り置きで外食・コンビニを減らす", en: "Batch-cook to cut eating out" },
      summary: { ja: "休日にまとめて数品仕込んでおく食費の節約術。平日の外食やコンビニ頼みを減らせる。",
                 en: "Cook several dishes in one go on a day off to cut weekday takeout and convenience-store spending." },
      steps: [ { ja: "休日に主菜・副菜を2〜3品仕込む。", en: "Prep 2–3 dishes on a day off." },
               { ja: "小分けで冷蔵・冷凍。", en: "Portion and refrigerate/freeze." } ],
      caution: { ja: "保存期間・衛生に注意。", en: "Mind storage time and hygiene." },
      source: { type: "link", label: "節約のコツ (short)", url: "https://example.com/source/mealprep" },
      evidence: { level: "expert", note: { ja: "食費削減の手段として家計の助言と整合。", en: "Consistent with common household-budget advice." } },
      review: { status: "unreviewed", by: null },
      minutes: 60, tags: ["節約", "自炊", "時短"],
      stats: { tried: 3900, resonated: 2900, notHelpful: 420 }
    },
    {
      id: "saving-sim", genreId: "saving", contributorId: "ken", origin: "JP",
      title: { ja: "格安SIMで通信費を見直す", en: "Switch to a low-cost SIM" },
      summary: { ja: "使い方に合った格安SIMに乗り換えて、毎月の固定費（通信費）を下げる定番の節約。",
                 en: "Move to a low-cost SIM that fits your usage to cut a recurring fixed cost." },
      steps: [ { ja: "直近のデータ使用量を確認。", en: "Check your recent data usage." },
               { ja: "使い方に合うプランへ乗り換える。", en: "Switch to a matching plan." } ],
      caution: { ja: "通信品質や手続きを事前に確認。", en: "Check coverage and the switch process first." },
      source: { type: "link", label: "節約のコツ (short)", url: "https://example.com/source/sim" },
      evidence: { level: "expert", note: { ja: "固定費削減として家計改善の王道。", en: "A staple of cutting fixed household costs." } },
      review: { status: "unreviewed", by: null },
      minutes: 30, tags: ["節約", "固定費"],
      stats: { tried: 5200, resonated: 4000, notHelpful: 460 }
    },

    // ── アンチエイジング（追加） ──
    {
      id: "antiaging-sunscreen", genreId: "antiaging", contributorId: "hana", origin: "US",
      title: { ja: "毎日の日焼け止めで光老化を防ぐ", en: "Daily sunscreen against photo-aging" },
      summary: { ja: "シミ・しわの大きな原因は紫外線（光老化）。曇りや室内でも、日々の日焼け止めが最も確実なアンチエイジング習慣の一つ。",
                 en: "UV (photo-aging) is a major cause of spots and wrinkles. Daily sunscreen — even on cloudy days — is one of the most reliable anti-aging habits." },
      steps: [ { ja: "朝、顔・首・手の甲に適量を塗る。", en: "Apply to face, neck, and hands each morning." },
               { ja: "屋外が長い日は塗り直す。", en: "Reapply on long days outdoors." } ],
      caution: { ja: "肌に合わない場合は使用を中止。", en: "Stop use if it irritates your skin." },
      source: { type: "link", label: "Skin care (short)", url: "https://example.com/source/sunscreen" },
      evidence: { level: "study", note: { ja: "日焼け止めと光老化抑制の関連はエビデンスが厚い。", en: "Sunscreen's role in reducing photo-aging is well-supported." } },
      review: { status: "expert", by: "hana" },
      minutes: 2, tags: ["美容", "紫外線", "海外発掘", "習慣"],
      stats: { tried: 7400, resonated: 5800, notHelpful: 540 }
    },
    {
      id: "antiaging-protein", genreId: "antiaging", contributorId: "mina", origin: "JP",
      title: { ja: "たんぱく質を毎食しっかりとる", en: "Get enough protein at every meal" },
      summary: { ja: "筋肉・肌・髪の材料になるたんぱく質を毎食意識してとる食習慣。加齢に伴う筋肉減少の対策の土台。",
                 en: "Be mindful of protein at each meal — the building block of muscle, skin, and hair. A foundation against age-related muscle loss." },
      steps: [ { ja: "毎食、肉・魚・卵・大豆などを一品。", en: "Include meat/fish/egg/soy at each meal." } ],
      caution: { ja: "腎臓など持病がある場合は医師に相談。", en: "Consult a doctor if you have kidney or other conditions." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/protein" },
      evidence: { level: "study", note: { ja: "高齢期の十分なたんぱく質摂取は筋肉維持に重要とされる。", en: "Adequate protein in older age is considered important for muscle." } },
      review: { status: "expert", by: "mina" },
      minutes: 5, tags: ["食習慣", "筋肉", "サルコペニア予防"],
      stats: { tried: 5300, resonated: 3900, notHelpful: 480 }
    },

    // ── 脳・認知ケア（追加） ──
    {
      id: "brain-sleep7", genreId: "brain", contributorId: "aki", origin: "JP",
      title: { ja: "7時間前後の睡眠で脳を休める", en: "Around 7 hours of sleep for the brain" },
      summary: { ja: "睡眠は脳の老廃物処理や記憶の整理に関わる。極端に短い・長い睡眠を避け、7時間前後を目安にする。",
                 en: "Sleep relates to clearing brain waste and consolidating memory. Avoid very short or long sleep; aim around 7 hours." },
      steps: [ { ja: "就寝・起床の時刻をなるべく一定に。", en: "Keep bedtime and wake time fairly consistent." } ],
      caution: { ja: "不眠が続く場合は医療機関へ。", en: "See a clinic if insomnia persists." },
      source: { type: "link", label: "Brain health (short)", url: "https://example.com/source/sleep7" },
      evidence: { level: "study", note: { ja: "睡眠と認知機能・健康の関連を示す研究は多い。", en: "Many studies link sleep with cognition and health." } },
      review: { status: "expert", by: "aki" },
      minutes: 1, tags: ["認知症予防", "睡眠", "習慣"],
      stats: { tried: 6700, resonated: 4800, notHelpful: 620 }
    },
    {
      id: "brain-reading", genreId: "brain", contributorId: "aki", origin: "JP",
      title: { ja: "音読・読書で脳を使う習慣", en: "Reading aloud to keep the brain active" },
      summary: { ja: "音読や読書、新しいことの学習など「頭を使う活動」を日課にする。脳に刺激を与える手軽な習慣。",
                 en: "Make reading aloud, reading, or learning something new a daily habit — easy ways to keep the brain engaged." },
      steps: [ { ja: "1日10分、声に出して読む。", en: "Read aloud for 10 min a day." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/reading" },
      evidence: { level: "expert", note: { ja: "知的活動と認知維持の関連が示唆される（断定はできない）。", en: "Mental activity is suggested to support cognition (not conclusive)." } },
      review: { status: "expert", by: "aki" },
      minutes: 10, tags: ["脳トレ", "習慣"],
      stats: { tried: 4100, resonated: 2900, notHelpful: 540 }
    },
    {
      id: "brain-social", genreId: "brain", contributorId: "aki", origin: "JP",
      title: { ja: "人とのつながりを保つ", en: "Keep up social connections" },
      summary: { ja: "会話や交流など社会的なつながりは、心と脳の健康に関わるとされる。孤立を避ける小さな行動を大切に。",
                 en: "Conversation and social ties relate to mental and brain health. Small acts against isolation matter." },
      steps: [ { ja: "週に数回、家族・友人と話す機会をつくる。", en: "Make time to talk with family/friends a few times a week." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "Brain health (short)", url: "https://example.com/source/social" },
      evidence: { level: "study", note: { ja: "社会的孤立と認知症リスクの関連を示す研究がある。", en: "Studies link social isolation with dementia risk." } },
      review: { status: "expert", by: "aki" },
      minutes: 10, tags: ["認知症予防", "つながり", "メンタル"],
      stats: { tried: 4600, resonated: 3400, notHelpful: 520 }
    },

    // ── 頭痛（新ジャンル） ──
    {
      id: "head-neck-warm", genreId: "head", contributorId: "mei", origin: "JP",
      title: { ja: "首・後頭部を温めてゆるめる（緊張型）", en: "Warm the neck for tension headaches" },
      summary: { ja: "肩首のこりからくる緊張型の頭重感に、後頭部〜首を温めて筋肉をゆるめるセルフケア。",
                 en: "For tension-type heaviness from neck/shoulder stiffness, warm the back of the head and neck to relax muscles." },
      steps: [ { ja: "蒸しタオルで後頭部〜首を5〜10分温める。", en: "Warm the nape and neck 5–10 min with a warm towel." } ],
      caution: { ja: "突然の激しい頭痛、しびれ、ろれつ困難は救急受診を。", en: "Seek emergency care for sudden severe headache, numbness, or slurred speech." },
      source: { type: "link", label: "健康の小ワザ (short)", url: "https://example.com/source/head-warm" },
      evidence: { level: "anecdotal", note: { ja: "緊張型頭痛のセルフケアとして紹介される。診断・治療ではない。", en: "Shared as self-care for tension headache; not diagnosis or treatment." } },
      review: { status: "unreviewed", by: null },
      minutes: 8, tags: ["緊張型頭痛", "温活", "肩こり"],
      stats: { tried: 4500, resonated: 2900, notHelpful: 760 }
    },
    {
      id: "head-hydrate", genreId: "head", contributorId: "aki", origin: "JP",
      title: { ja: "水分不足の頭痛を防ぐ", en: "Prevent dehydration headaches" },
      summary: { ja: "水分不足は頭痛の引き金になりうる。こまめな水分補給で予防を意識する。",
                 en: "Dehydration can trigger headaches. Steady fluid intake helps prevent them." },
      steps: [ { ja: "のどが渇く前にこまめに水を飲む。", en: "Sip water before you feel thirsty." } ],
      caution: { ja: "持病で水分制限がある人は医師の指示に従う。", en: "Follow your doctor if you have fluid restrictions." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/head-hydrate" },
      evidence: { level: "expert", note: { ja: "脱水と頭痛の関連は一般に知られる。", en: "Dehydration is a recognized headache trigger." } },
      review: { status: "expert", by: "aki" },
      minutes: 1, tags: ["頭痛予防", "水分補給", "習慣"],
      stats: { tried: 3800, resonated: 2700, notHelpful: 420 }
    },
    {
      id: "head-rest-dark", genreId: "head", contributorId: "aki", origin: "JP",
      title: { ja: "暗く静かな場所で休む（片頭痛）", en: "Rest in a dark, quiet room (migraine)" },
      summary: { ja: "光や音に敏感になりやすい片頭痛では、暗く静かな環境で休むことがつらさをやわらげる助けになる。",
                 en: "With migraines (often light/sound sensitive), resting in a dark, quiet room can help ease the episode." },
      steps: [ { ja: "光と音を遮り、横になって休む。", en: "Block light and sound; lie down and rest." } ],
      caution: { ja: "頻繁・激しい・いつもと違う頭痛は受診を。市販薬の使いすぎに注意。", en: "See a doctor for frequent, severe, or unusual headaches; avoid overusing OTC painkillers." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/head-rest" },
      evidence: { level: "expert", note: { ja: "片頭痛の急性期の一般的な対処として案内される。", en: "Commonly advised for managing an acute migraine." } },
      review: { status: "expert", by: "aki" },
      minutes: 20, tags: ["片頭痛", "休息"],
      stats: { tried: 4200, resonated: 3100, notHelpful: 520 }
    },

    // ── 肌・髪（新ジャンル） ──
    {
      id: "skin-moisture", genreId: "skin", contributorId: "hana", origin: "JP",
      title: { ja: "入浴後すぐの保湿で乾燥を防ぐ", en: "Moisturize right after bathing" },
      summary: { ja: "肌は入浴後に乾燥しやすい。お風呂上がりすぐに保湿剤を塗ることで、うるおいを保ちやすくする。",
                 en: "Skin dries out after bathing. Applying moisturizer right after helps lock in hydration." },
      steps: [ { ja: "タオルで軽く押さえる程度に水気をとる。", en: "Pat skin dry gently." },
               { ja: "数分以内に保湿剤を塗る。", en: "Apply moisturizer within a few minutes." } ],
      caution: { ja: "刺激・赤みが出たら使用を中止。", en: "Stop if you get irritation or redness." },
      source: { type: "link", label: "Skin care (short)", url: "https://example.com/source/moisture" },
      evidence: { level: "study", note: { ja: "入浴後の保湿は乾燥肌ケアの基本として支持される。", en: "Post-bath moisturizing is well-supported for dry skin." } },
      review: { status: "expert", by: "hana" },
      minutes: 3, tags: ["保湿", "乾燥肌", "習慣"],
      stats: { tried: 5100, resonated: 3900, notHelpful: 420 }
    },
    {
      id: "skin-lukewarm", genreId: "skin", contributorId: "hana", origin: "JP",
      title: { ja: "ぬるま湯でやさしく洗顔", en: "Wash your face with lukewarm water" },
      summary: { ja: "熱すぎるお湯やこすりすぎは肌のうるおいを奪いがち。ぬるま湯でやさしく洗うのが基本。",
                 en: "Hot water and scrubbing strip the skin. Washing gently with lukewarm water is the basic." },
      steps: [ { ja: "32〜34℃くらいのぬるま湯で洗う。", en: "Wash with lukewarm water (~32–34°C)." },
               { ja: "ゴシゴシせず押さえて拭く。", en: "Pat dry without rubbing." } ],
      caution: { ja: "肌トラブルが続くなら皮膚科へ。", en: "See a dermatologist if skin trouble persists." },
      source: { type: "link", label: "Skin care (short)", url: "https://example.com/source/lukewarm" },
      evidence: { level: "expert", note: { ja: "やさしい洗顔はスキンケアの基本として広く案内される。", en: "Gentle washing is widely advised as skincare basics." } },
      review: { status: "expert", by: "hana" },
      minutes: 2, tags: ["洗顔", "乾燥肌"],
      stats: { tried: 4300, resonated: 3100, notHelpful: 480 }
    },
    {
      id: "skin-scalp", genreId: "skin", contributorId: "jin", origin: "KR",
      title: { ja: "頭皮マッサージで地肌をほぐす", en: "Scalp massage to loosen the skin" },
      summary: { ja: "指の腹で頭皮を動かすようにマッサージするセルフケア。韓国の美容ルーティンで人気。",
                 en: "Massage the scalp by moving the skin with your fingertips. Popular in Korean beauty routines." },
      steps: [ { ja: "指の腹で頭皮を円を描くように動かす。", en: "Move the scalp in circles with fingertips." },
               { ja: "生え際から頭頂へ1〜2分。", en: "From hairline to crown, 1–2 min." } ],
      caution: { ja: "爪を立てない。炎症がある時は避ける。", en: "No nails; avoid if the scalp is inflamed." },
      source: { type: "link", label: "셀프케어 (short)", url: "https://example.com/source/scalp" },
      evidence: { level: "anecdotal", note: { ja: "リラックス目的。育毛などの効果は根拠が限定的。", en: "For relaxation; benefits like hair growth are not well-evidenced." } },
      review: { status: "unreviewed", by: null },
      minutes: 2, tags: ["頭皮", "海外発掘", "リラックス"],
      stats: { tried: 6800, resonated: 3700, notHelpful: 1500 }
    },

    // ── メンタル・ストレス（新ジャンル） ──
    {
      id: "mind-54321", genreId: "mind", contributorId: "yui", origin: "US",
      title: { ja: "5-4-3-2-1グラウンディングで落ち着く", en: "5-4-3-2-1 grounding to settle down" },
      summary: { ja: "見える5つ・聞こえる4つ…と五感に注意を向け、今ここに意識を戻す海外発のストレス対処法。",
                 en: "Name 5 things you see, 4 you hear, and so on — a grounding technique to return attention to the present." },
      steps: [ { ja: "見える物5・聞こえる音4・触れる物3を挙げる。", en: "Name 5 sights, 4 sounds, 3 touches." },
               { ja: "におい2・味1まで続ける。", en: "Continue to 2 smells, 1 taste." } ],
      caution: { ja: "つらさが強い・続く時は専門の窓口に相談を。", en: "If distress is strong or lasting, reach out to a professional." },
      source: { type: "link", label: "Calm routine (short)", url: "https://example.com/source/54321" },
      evidence: { level: "expert", note: { ja: "不安時のグラウンディングとして広く用いられる。", en: "Widely used as grounding for anxiety." } },
      review: { status: "expert", by: "yui" },
      minutes: 3, tags: ["ストレス", "不安", "海外発掘"],
      stats: { tried: 6300, resonated: 4400, notHelpful: 760 }
    },
    {
      id: "mind-journaling", genreId: "mind", contributorId: "yui", origin: "JP",
      title: { ja: "気持ちを紙に書き出す", en: "Write your feelings on paper" },
      summary: { ja: "頭の中のモヤモヤを紙に書き出して外に出すセルフケア。考えの整理と気持ちの落ち着きを助ける。",
                 en: "Put swirling thoughts on paper to get them out of your head. Helps organize thoughts and calm down." },
      steps: [ { ja: "今の気持ちを思いつくまま3分書く。", en: "Write whatever you feel for 3 minutes." } ],
      caution: { ja: "つらい記憶で苦しくなったら中断し、必要なら相談を。", en: "Stop if painful memories overwhelm you; seek support if needed." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/journaling" },
      evidence: { level: "study", note: { ja: "表現的筆記とストレス軽減の関連を示す研究がある。", en: "Studies link expressive writing with reduced stress." } },
      review: { status: "expert", by: "yui" },
      minutes: 3, tags: ["ストレス", "セルフケア"],
      stats: { tried: 4700, resonated: 3300, notHelpful: 560 }
    },
    {
      id: "mind-forest", genreId: "mind", contributorId: "yui", origin: "JP",
      title: { ja: "自然の中をゆっくり歩く（森林浴）", en: "Walk slowly in nature (forest bathing)" },
      summary: { ja: "公園や緑の中をゆっくり歩き、五感で自然を感じる「森林浴」。日本発の考え方で、気分の落ち着きに関心が高い。",
                 en: "Walk slowly through greenery, sensing nature — 'forest bathing' (shinrin-yoku), a concept from Japan studied for calming mood." },
      steps: [ { ja: "緑のある場所を15〜30分ゆっくり歩く。", en: "Walk slowly 15–30 min where there's greenery." } ],
      caution: { ja: "熱中症・花粉など体調に合わせて。", en: "Mind heat and pollen for your condition." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/forest" },
      evidence: { level: "study", note: { ja: "自然環境とストレス指標改善の関連を示す研究がある。", en: "Studies link natural settings with improved stress markers." } },
      review: { status: "expert", by: "yui" },
      minutes: 20, tags: ["ストレス", "森林浴", "ウォーキング"],
      stats: { tried: 5400, resonated: 4100, notHelpful: 540 }
    },

    // ── 食事・栄養（新ジャンル） ──
    {
      id: "diet-mediterranean", genreId: "diet", contributorId: "luca", origin: "IT",
      title: { ja: "地中海式の食べ方を取り入れる", en: "Borrow from Mediterranean eating" },
      summary: { ja: "野菜・豆・魚・オリーブオイル・全粒穀物を中心にする地中海式の食習慣。海外（伊）由来で、健康との関連研究が豊富。",
                 en: "Center meals on vegetables, beans, fish, olive oil, and whole grains — Mediterranean eating from Italy, with rich research on health." },
      steps: [ { ja: "野菜・豆・魚を増やし、油はオリーブオイルへ。", en: "Add vegetables/beans/fish; use olive oil." },
               { ja: "精製した食品を控えめに。", en: "Go easy on refined foods." } ],
      caution: { ja: "持病・アレルギーは主治医や栄養士に相談。", en: "Consult a doctor/dietitian for conditions or allergies." },
      source: { type: "link", label: "Mediterranean (short)", url: "https://example.com/source/mediterranean" },
      evidence: { level: "study", note: { ja: "地中海食と健康指標の関連を示す研究が豊富。", en: "A large body of research links it with health markers." } },
      review: { status: "expert", by: "mina" },
      minutes: 10, tags: ["食習慣", "海外発掘", "栄養"],
      stats: { tried: 6100, resonated: 4500, notHelpful: 640 }
    },
    {
      id: "diet-veggie-first", genreId: "diet", contributorId: "mina", origin: "JP",
      title: { ja: "野菜から食べる（ベジファースト）", en: "Eat vegetables first" },
      summary: { ja: "食事の最初に野菜や汁物をとる食べ方。食後の血糖の上がり方をゆるやかにする狙いで知られる。",
                 en: "Start meals with vegetables or soup. Known for aiming to slow the post-meal blood-sugar rise." },
      steps: [ { ja: "食事の最初に野菜・汁物を食べる。", en: "Begin meals with vegetables or soup." },
               { ja: "次に主菜、最後に主食。", en: "Then mains, then carbs last." } ],
      caution: { ja: "治療中の人は主治医の指示を優先。", en: "If under treatment, follow your doctor first." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/veggie-first" },
      evidence: { level: "study", note: { ja: "食べる順番と食後血糖の関連を示す研究がある。", en: "Studies link eating order with post-meal blood sugar." } },
      review: { status: "expert", by: "mina" },
      minutes: 1, tags: ["食習慣", "血糖", "栄養"],
      stats: { tried: 7000, resonated: 5000, notHelpful: 900 }
    },
    {
      id: "diet-chew", genreId: "diet", contributorId: "mina", origin: "JP",
      title: { ja: "よく噛んでゆっくり食べる", en: "Chew well, eat slowly" },
      summary: { ja: "一口ごとによく噛んでゆっくり食べる習慣。満腹感を得やすく、食べすぎ防止の助けになるとされる。",
                 en: "Chew each bite well and eat slowly. Thought to help you feel full and avoid overeating." },
      steps: [ { ja: "一口30回を目安に噛む。", en: "Aim for ~30 chews per bite." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/chew" },
      evidence: { level: "expert", note: { ja: "ゆっくり食べることと食べすぎ抑制の関連が示唆される。", en: "Eating slowly is suggested to help curb overeating." } },
      review: { status: "expert", by: "mina" },
      minutes: 1, tags: ["食習慣", "ダイエット"],
      stats: { tried: 5500, resonated: 3700, notHelpful: 900 }
    },

    // ── 免疫・風邪（新ジャンル） ──
    {
      id: "immune-handwash", genreId: "immune", contributorId: "aki", origin: "JP",
      title: { ja: "正しい手洗いで感染を防ぐ", en: "Proper handwashing to prevent infection" },
      summary: { ja: "石けんで指の間や爪まで丁寧に洗う基本のケア。風邪や感染症の予防として最も確実な方法の一つ。",
                 en: "Wash thoroughly with soap, including between fingers and nails — one of the most reliable ways to prevent colds and infections." },
      steps: [ { ja: "石けんで20〜30秒、指の間・爪・手首まで洗う。", en: "Soap 20–30s: between fingers, nails, wrists." },
               { ja: "流水でしっかりすすぐ。", en: "Rinse well under running water." } ],
      caution: { ja: "—", en: "—" },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/handwash" },
      evidence: { level: "study", note: { ja: "手洗いと感染症予防の関連はエビデンスが厚い。", en: "Handwashing's role in preventing infection is well-supported." } },
      review: { status: "expert", by: "aki" },
      minutes: 1, tags: ["風邪予防", "衛生", "習慣"],
      stats: { tried: 7600, resonated: 6000, notHelpful: 520 }
    },
    {
      id: "immune-humidity", genreId: "immune", contributorId: "aki", origin: "JP",
      title: { ja: "のどの保湿と加湿で乾燥対策", en: "Keep the throat and air moist" },
      summary: { ja: "乾燥はのどの防御を弱めやすい。加湿やこまめな水分・マスクで、のどのうるおいを保つ。",
                 en: "Dry air can weaken the throat's defenses. Humidify, sip water, or use a mask to keep the throat moist." },
      steps: [ { ja: "室内を加湿し、こまめに水分をとる。", en: "Humidify the room and sip water often." } ],
      caution: { ja: "加湿器は清潔に保つ（カビ防止）。", en: "Keep humidifiers clean to prevent mold." },
      source: { type: "link", label: "健康の小知識 (short)", url: "https://example.com/source/humidity" },
      evidence: { level: "expert", note: { ja: "乾燥対策はのどのケアとして一般に勧められる。", en: "Managing dryness is commonly advised for throat care." } },
      review: { status: "expert", by: "aki" },
      minutes: 2, tags: ["風邪予防", "乾燥", "のど"],
      stats: { tried: 4400, resonated: 3200, notHelpful: 480 }
    }
  ];

  // ─────────────────────────────────────────────
  // 動画検索の厳選キーワード（id → 検索語）
  //  ねらい: YouTube/TikTok で開いたとき、上位1〜3位が“その知恵の動画”に
  //         なるよう、世間でよく使われる呼び名＋短い文脈語で命中率を上げる。
  //  ここに無い項目は app.js 側が「タイトル＋タグ＋やり方」で自動生成する。
  // ─────────────────────────────────────────────
  var VIDEO_KW = {
    "neck-stuck-release": "胸鎖乳突筋 ほぐし 首こり",
    "neck-god-point": "合谷 ツボ 肩こり",
    "back-frog-legs": "カエル足 ストレッチ 腰",
    "back-hip-reset": "股関節 リセット 足振り",
    "eyes-palming": "パーミング 目 疲れ",
    "eyes-2020": "20-20-20ルール 目",
    "sleep-478": "4-7-8呼吸法 寝る",
    "sleep-light": "朝日 光 体内時計 睡眠",
    "home-fold": "Tシャツ 早くたたむ 方法",
    "home-bottle": "水筒 パッキン 掃除 重曹",
    "saving-fridge": "冷蔵庫 整理 節約",
    "saving-standby": "待機電力 節約 方法",
    "neck-scapula": "肩甲骨はがし やり方",
    "neck-chin-tuck": "チンタック スマホ首",
    "neck-ear-roll": "耳 マッサージ 首こり",
    "back-cat-cow": "キャットアンドカウ ヨガ",
    "back-piriformis": "梨状筋 ストレッチ お尻",
    "eyes-jingming": "晴明 ツボ 目",
    "legs-calf-pump": "かかと上げ ふくらはぎ むくみ",
    "legs-ankle-thai": "足首回し むくみ",
    "stomach-warm-water": "白湯 朝 飲み方",
    "stomach-wind-pose": "ガス抜きのポーズ ヨガ",
    "antiaging-slow-squat": "スロースクワット やり方",
    "antiaging-interval-walk": "インターバル速歩 やり方",
    "antiaging-face-yoga": "フェイスヨガ ほうれい線",
    "antiaging-tongue-roll": "舌回し体操 やり方",
    "brain-cognicise": "コグニサイズ やり方",
    "brain-aerobic": "有酸素運動 認知症 予防",
    "brain-finger": "指体操 脳トレ",
    "neck-shrug": "肩すくめ ストレッチ 肩こり",
    "neck-hot-towel": "蒸しタオル 首こり 温め",
    "back-pelvic-tilt": "骨盤 傾ける 体操 腰",
    "back-prone-extension": "マッケンジー体操 腰",
    "eyes-blink": "まばたき 体操 ドライアイ",
    "eyes-warm-towel": "蒸しタオル 目 疲れ",
    "sleep-bath": "入浴 就寝前 睡眠 90分",
    "sleep-box": "ボックス呼吸 4-4-4-4",
    "sleep-no-screen": "寝る前 スマホ やめる 睡眠",
    "legs-elevate": "足 むくみ 上げる 寝る",
    "legs-calf-stretch": "ふくらはぎ ストレッチ 壁",
    "stomach-fermented": "発酵食品 腸活",
    "stomach-fiber-water": "食物繊維 便秘 改善",
    "home-melamine": "メラミンスポンジ 水垢",
    "home-baking-deodor": "重曹 消臭 使い方",
    "saving-mealprep": "作り置き 節約",
    "saving-sim": "格安SIM 乗り換え 節約",
    "antiaging-sunscreen": "日焼け止め 毎日 光老化",
    "antiaging-protein": "たんぱく質 食事 高齢",
    "brain-sleep7": "睡眠時間 認知症 予防",
    "brain-reading": "音読 脳トレ",
    "brain-social": "社会的つながり 認知症 予防",
    "head-neck-warm": "緊張型頭痛 首 温め",
    "head-hydrate": "頭痛 水分不足 予防",
    "head-rest-dark": "片頭痛 対処 休む",
    "skin-moisture": "入浴後 保湿 乾燥肌",
    "skin-lukewarm": "ぬるま湯 洗顔 やり方",
    "skin-scalp": "頭皮マッサージ やり方",
    "mind-54321": "5-4-3-2-1 グラウンディング 不安",
    "mind-journaling": "書く 気持ち 整理 ストレス",
    "mind-forest": "森林浴 効果 リラックス",
    "diet-mediterranean": "地中海食 やり方",
    "diet-veggie-first": "ベジファースト 血糖値",
    "diet-chew": "よく噛む ダイエット",
    "immune-handwash": "正しい手洗い 方法",
    "immune-humidity": "のど 乾燥 加湿 風邪予防"
  };
  contents.forEach(function (c) { if (VIDEO_KW[c.id]) c.videoKw = VIDEO_KW[c.id]; });

  window.APP_DATA = { genres: genres, contributors: contributors, contents: contents };
})();
