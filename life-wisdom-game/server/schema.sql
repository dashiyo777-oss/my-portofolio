-- 叡智の灯火 会員API スキーマ (Cloudflare D1 / SQLite)
CREATE TABLE IF NOT EXISTS content (
  type       TEXT NOT NULL,            -- 'sage' | 'event' | 'legend'
  id         TEXT NOT NULL,
  tier       TEXT,                     -- 'paid'
  payload    TEXT NOT NULL,            -- JSON文字列（そのままクライアントへ）
  updated_at INTEGER,
  PRIMARY KEY (type, id)
);

-- 響き度（P2で本格運用）。匿名集計のための生ログ。
CREATE TABLE IF NOT EXISTS feedback (
  ts        INTEGER NOT NULL,
  event_id  TEXT,
  sage_id   TEXT,
  mood      TEXT,
  fb        TEXT                       -- 'resonated' | 'not_now'
);
CREATE INDEX IF NOT EXISTS idx_feedback_key ON feedback (event_id, sage_id);

-- レート制限（簡易・IP×バケット×時刻）
CREATE TABLE IF NOT EXISTS rl (
  ip     TEXT,
  bucket TEXT,
  ts     INTEGER
);
CREATE INDEX IF NOT EXISTS idx_rl ON rl (ip, bucket, ts);

-- 配信監査（流出元の追跡用・テキストは改変しない＝名言の正確性を守る）
CREATE TABLE IF NOT EXISTS deliveries (
  ts  INTEGER,
  lic TEXT,      -- 会員トークンの短いフィンガープリント
  ip  TEXT
);

