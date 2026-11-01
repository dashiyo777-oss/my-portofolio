#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国会会議録検索システムから取り直した結果を検証して、採用値を決める。

fetch_speeches.gs が書き出したシートをCSVで受け取り、
どの数字を信じてよいかを判定して「確定発言数」列を足す。

    python3 reconcile.py 取得済み.csv -o 確定版.csv

── 2026-08-24 に判明した2つの落とし穴 ───────────────────────

1. 本名で引くと別人を拾う
   会議録は通称で記録される。本名（戸籍名）で大量にヒットするのは
   同姓の別人を拾っているためで、値としては使えない。

     徳永 エリ   通称    900 / 本名「鈴木 エリ」 14,202
     蓮舫       通称    957 / 本名「齊藤 蓮舫」  9,283
     森 ゆうこ   通称    197 / 本名「森 裕子」    8,751

   fetch_speeches.gs は大きいほうを採る設計だったため、43件中29件で
   水増しを採用していた（合計 63,188件）。ここでは通称の値だけを使う。

2. 通称でも同姓同名の別人を拾うことがある
   応答に含まれる speakerYomi と、名簿のよみを突き合わせれば検出できる。
   食い違えば別人。長音記号の有無は表記ゆれなので無視する。
"""

import argparse
import csv
import io
import sys
import unicodedata
from collections import Counter

COL_NAME = "氏名"
COL_YOMI = "よみ"
COL_ALIAS = "統合元氏名"
COL_API_MAIN = "API発言数(通称)"
COL_API_ALIAS = "API発言数(本名)"
COL_API_YOMI = "APIよみ"
COL_API_GROUP = "API会派"
COL_HOUSE = "院"

OUT_FIXED = "確定発言数"
OUT_FLAG = "確定の根拠"

DIET = ("衆議院", "参議院")


def norm_yomi(s):
    """よみを比べるための正規化。長音記号と空白の違いは無視する。"""
    s = unicodedata.normalize("NFKC", s or "")
    s = "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)
    for ch in ("ー", "－", "-", " ", "　"):
        s = s.replace(ch, "")
    return s


def num(row, col):
    v = (row.get(col) or "").strip()
    try:
        return float(v)
    except ValueError:
        return None


def reconcile(rows):
    stats = Counter()
    for r in rows:
        main = num(r, COL_API_MAIN)
        alias = num(r, COL_API_ALIAS)
        csv_yomi = norm_yomi(r.get(COL_YOMI))
        api_yomi = norm_yomi(r.get(COL_API_YOMI))

        # 採用するのは常に通称の値。本名は別人を拾うので使わない。
        if main is None:
            r[OUT_FIXED] = ""
            r[OUT_FLAG] = "未取得"
            stats["未取得"] += 1
            continue

        r[OUT_FIXED] = str(int(main))

        if not api_yomi:
            # 発言0件だとよみを返す材料がない。0なら整合的。
            r[OUT_FLAG] = "確定（発言0）" if main == 0 else "要確認（よみ未取得）"
            stats[r[OUT_FLAG]] += 1
        elif not csv_yomi:
            r[OUT_FLAG] = "要確認（名簿によみなし）"
            stats[r[OUT_FLAG]] += 1
        elif csv_yomi == api_yomi:
            r[OUT_FLAG] = "確定"
            stats["確定"] += 1
        else:
            r[OUT_FIXED] = ""
            r[OUT_FLAG] = "別人の疑い（よみ不一致: %s ≠ %s）" % (
                r.get(COL_YOMI, "").strip(), r.get(COL_API_YOMI, "").strip())
            stats["別人の疑い"] += 1

        # 本名で大きく出た場合は、捨てた事実を残す
        if alias is not None and main is not None and alias > main * 1.5:
            r[OUT_FLAG] += "／本名検索は%d件だが不採用" % int(alias)
            stats["本名を不採用"] += 1
    return stats


def main():
    ap = argparse.ArgumentParser(description="取得結果の検証と採用値の決定")
    ap.add_argument("csv")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    with io.open(args.csv, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields, rows = rd.fieldnames, list(rd)

    stats = reconcile(rows)
    diet = [r for r in rows if r.get(COL_HOUSE) in DIET]

    print("入力 %d行 / 国会議員 %d人" % (len(rows), len(diet)))
    print("\n=== 判定 ===")
    for k, v in stats.most_common():
        print("  %-26s %d" % (k, v))

    fixed = [r for r in diet if (r[OUT_FIXED] or "").strip()]
    print("\n=== 採用できた国会議員 ===")
    print("  %d / %d 人" % (len(fixed), len(diet)))
    if fixed:
        vals = sorted(float(r[OUT_FIXED]) for r in fixed)
        print("  合計 %s件  中央値 %.0f  最大 %.0f"
              % (format(int(sum(vals)), ","), vals[len(vals) // 2], vals[-1]))

    bad = [r for r in diet if "別人" in r[OUT_FLAG]]
    if bad:
        print("\n=== 別人の疑いで除外 %d人（名簿かAPIの氏名を要確認）===" % len(bad))
        for r in bad:
            print("  %-14s %s → API %s（%s件）"
                  % (r[COL_NAME], r.get(COL_YOMI, ""), r.get(COL_API_YOMI, ""),
                     (r.get(COL_API_MAIN) or "").strip()))

    unk = [r for r in diet if "要確認" in r[OUT_FLAG]]
    if unk:
        print("\n=== よみで裏が取れなかった %d人（値は採用、目視推奨）===" % len(unk))
        for r in unk[:15]:
            print("  %-14s %s件" % (r[COL_NAME], r[OUT_FIXED]))

    if args.out:
        out_fields = fields + [f for f in (OUT_FIXED, OUT_FLAG) if f not in fields]
        with io.open(args.out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print("\n書き出し: %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
