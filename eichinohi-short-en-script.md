# Eichi no Tomoshibi — English Promo Shorts (overseas campaign)

**Product**: 叡智の灯火 / *Eichi no Tomoshibi* — "The Lamp of Wisdom" — a life-simulation where 27 great minds of history speak to your crossroads. → https://eichinohi.com

**Series**: "The Lamp of Wisdom" — 3 vertical Shorts (9:16 / 1080×1920), ~40s each, BGM included.
Finished MP4s (ready to upload) + editable HTML sources are committed alongside this file.
Generator: [`scripts-gen/gen_en_shorts.py`](scripts-gen/gen_en_shorts.py) → run `python3 scripts-gen/gen_en_shorts.py` to regenerate the HTML.

| Episode | File (video / source) | Sages | Theme |
|---|---|---|---|
| EN #1 — When you lose your way | `eichinohi-short-en-1.mp4` / `eichinohi-short-en-1.html` | Mother Teresa, Marie Curie, Helen Keller | loneliness · confidence · suffering |
| EN #2 — Don't quit | `eichinohi-short-en-2.mp4` / `eichinohi-short-en-2.html` | Abraham Lincoln, Muhammad Ali, Eleanor Roosevelt | grit · perseverance · courage |
| EN #3 — At the crossroads | `eichinohi-short-en-3.mp4` / `eichinohi-short-en-3.html` | Miyamoto Musashi, Seneca, Sun Tzu | decision · direction · strategy |

## Structure (each Short)

`Hook → Series badge → (Worry → Sage's words) ×3 → "27 great minds" → CTA (eichinohi.com / PLAY FREE)`

## Quotes used (verified — authentic English where the original was English)

**EN #1**
- Mother Teresa (1910–1997): "Loneliness and the feeling of being unwanted is the most terrible poverty." — widely recorded
- Marie Curie (1867–1934): "Life is not easy for any of us. But what of that? We must have perseverance, and above all, confidence in ourselves." — *Madame Curie*, 1937
- Helen Keller (1880–1968): "Although the world is full of suffering, it is also full of the overcoming of it." — *Optimism*, 1903

**EN #2**
- Abraham Lincoln (1809–1865): "Always bear in mind that your own resolution to succeed is more important than any other." — Letter to Isham Reavis, 1855
- Muhammad Ali (1942–2016): "I hated every minute of training, but I said: 'Don't quit. Suffer now and live the rest of your life as a champion.'" — *In His Own Words*
- Eleanor Roosevelt (1884–1962): "You must do the things you think you cannot do." — *You Learn by Living*, 1960

**EN #3**
- Miyamoto Musashi (1584–1645): "I have no regret for what I have done." — *Dokkōdō*, 1645
- Seneca (c. 4 BC–AD 65): "If one does not know to which port one is sailing, no wind is favorable." — *Letters*, 71
- Sun Tzu (c. 544–496 BC): "Know the enemy and know yourself, and in a hundred battles you will never be in peril." — *The Art of War*

All lines are drawn from the game's own **verified** dataset (primary-source citations). No invented "quotes."

## Suggested YouTube description (per episode — swap the sages/line)

> When you lose your way, what would the wise say?
> Mother Teresa · Marie Curie · Helen Keller — real words to light your path.
> *Eichi no Tomoshibi* — a life-sim where 27 great minds speak to your crossroads. Play free ▶ https://eichinohi.com
> #wisdom #quotes #stoicism #motivation #EichiNoTomoshibi

## Re-rendering the MP4s

1. Serve the repo (`python3 -m http.server`) and open `eichinohi-short-en-N.html?capture=1`.
2. The page exposes `window.renderAt(ms)` and `window.TOTAL`; screenshot each frame at 30fps (headless Chromium).
3. Encode the JPEG sequence with the BGM: H.264 (yuv420p) + AAC, fade the audio in/out.

To just watch/record instead: open `eichinohi-short-en-N.html` (no `?capture`), press **▶ Play** — it plays with BGM and can be screen-recorded.
