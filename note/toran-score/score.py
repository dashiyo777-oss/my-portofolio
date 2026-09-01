#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TORAN 国会活動量スコア — 再現可能な採点器

このスクリプトは「実績」や「優秀さ」を測るものではありません。
入力CSVにある4つの活動量（発言・質問主意書・議員立法の発議／賛成）だけを、
院ごとの相対順位に直して加重合計したものです。
何を測っていないかは README.md の「限界」に全部書いてあります。

使い方:
    python3 score.py 入力.csv -o 出力.csv
    python3 score.py 入力.csv --compare      # 既存の総合スコア列と突き合わせる
"""

import argparse
import csv
import io
import sys
from collections import defaultdict

# ── 採点パラメータ（ここだけ変えれば式が変わる。変えたら README の更新履歴に残すこと）──

WEIGHTS = {
    "発言数(2021.11〜2026.07)": 0.30,   # 本会議・委員会での発言回数
    "質問主意書(第207〜221回)": 0.20,   # 文書質問。提出には手間がかかる
    "議員立法(発議)": 0.30,             # 発議者になること。4つの中で最も重い
    "議員立法(賛成者)": 0.20,           # 賛成者として署名すること。発議より軽い
}

# 採点対象にする「院」。国会での活動量を測る指標なので、国会議員だけを母集団にする。
SCORED_HOUSES = ("衆議院", "参議院")

# パーセンタイルを取る比較グループ。衆参は発言機会の総量が違うので院内で比べる。
GROUP_BY = "院"

# 比較グループ内で「値を持つ人」がこの割合を下回る列は、その院では未収集とみなして採点から外す。
# 例: 参議院の「議員立法(賛成者)」は262人中1人しか値がなく、順位づけの材料にならない。
MIN_COVERAGE = 0.05

# ランクの切り方（相対評価。上位何%かを表す。絶対的な合格ラインではない）
RANK_CUTS = [
    (0.05, "A"),
    (0.15, "A-"),
    (0.30, "B+"),
    (0.50, "B"),
    (0.70, "B-"),
    (0.85, "C+"),
    (1.00, "C"),
]

# ──────────────────────────────────────────────────────────────


# 院ごとに採点から外した列（未収集・全員同値）を記録する
DROPPED = {}


def to_num(raw):
    """空欄は None（＝未取得）、それ以外は数値。'0' は「0という記録」であって未取得ではない。"""
    s = (raw or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def percentile_ranks(values):
    """値のリスト → 0.0〜1.0 の順位。同値は平均順位（tie は同じ点になる）。"""
    n = len(values)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg / (n - 1) if n > 1 else 0.5
        i = j + 1
    return ranks


def load(path):
    with io.open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def score(rows):
    """rows を書き換えて、採点結果の列を足して返す。"""
    cols = list(WEIGHTS)

    for r in rows:
        vals = {c: to_num(r.get(c)) for c in cols}
        r["_vals"] = vals
        r["_missing"] = [c for c, v in vals.items() if v is None]
        r["_target"] = r.get(GROUP_BY) in SCORED_HOUSES

    # 採点できるのは「対象の院」かつ「4列すべて取得済み」の人だけ
    scorable = [r for r in rows if r["_target"] and not r["_missing"]]

    groups = defaultdict(list)
    for r in scorable:
        groups[r[GROUP_BY]].append(r)

    for gname, members in groups.items():
        # その院で全員が同じ値の列は、情報を持たないので採点から外す。
        # 例: 参議院の「議員立法(賛成者)」は未収集で全員0。
        #     残った列の重みを合計1.0に再正規化して、院をまたいでも桁が揃うようにする。
        live = [c for c in cols
                if len({m["_vals"][c] for m in members}) > 1
                and sum(1 for m in members if m["_vals"][c] > 0)
                >= MIN_COVERAGE * len(members)]
        dropped = [c for c in cols if c not in live]
        if dropped:
            DROPPED[gname] = dropped
        wsum = sum(WEIGHTS[c] for c in live) or 1.0

        pct = {c: percentile_ranks([m["_vals"][c] for m in members]) for c in live}
        for i, m in enumerate(members):
            m["_pct"] = {c: pct[c][i] for c in live}
            m["_raw"] = sum(WEIGHTS[c] * pct[c][i] for c in live) / wsum

        ordered = sorted(members, key=lambda m: -m["_raw"])
        n = len(ordered)
        for i, m in enumerate(ordered):
            m["活動量スコア"] = str(int(round(m["_raw"] * 100)))
            q = (i + 1) / n
            m["活動量ランク"] = next(label for cut, label in RANK_CUTS if q <= cut)
            m["院内順位"] = f"{i + 1}/{n}"
            for c in cols:
                m[f"%{c}"] = (f"{m['_pct'][c] * 100:.1f}"
                              if c in m["_pct"] else "未収集")

    # 採点できなかった人には、できなかった理由を書く
    for r in rows:
        if "活動量スコア" in r:
            continue
        r["活動量スコア"] = ""
        r["院内順位"] = ""
        if not r["_target"]:
            r["活動量ランク"] = f"対象外（{r.get(GROUP_BY, '')}）"
        else:
            r["活動量ランク"] = "未取得（" + "・".join(
                c.split("(")[0] for c in r["_missing"]
            ) + "）"
        for c in cols:
            r[f"%{c}"] = ""

    return rows


def write(rows, path, src_fields):
    added = ["活動量スコア", "活動量ランク", "院内順位"] + [f"%{c}" for c in WEIGHTS]
    fields = src_fields + [f for f in added if f not in src_fields]
    with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def report(rows):
    tgt = [r for r in rows if r["_target"]]
    done = [r for r in rows if r["活動量スコア"] != ""]
    print(f"母集団（{'・'.join(SCORED_HOUSES)}）: {len(tgt)}人")
    print(f"採点完了: {len(done)}人  未取得: {len(tgt) - len(done)}人  "
          f"対象外: {len(rows) - len(tgt)}人")
    for h in SCORED_HOUSES:
        g = [r for r in done if r["院"] == h]
        if g:
            print(f"  {h}: {len(g)}人")
    print("\n重み: " + " / ".join(f"{c.split('(')[0]} {w:.0%}" for c, w in WEIGHTS.items()))
    for g, cs in DROPPED.items():
        print(f"  ※ {g} は「{'・'.join(cs)}」が未収集のため採点から除外し、"
              f"残りの重みを再正規化しました")


def compare(rows):
    """既存の総合スコア列があれば、新スコアと突き合わせる。"""
    both = [r for r in rows
            if r["活動量スコア"] != "" and (r.get("総合スコア") or "").strip() not in ("", "0")]
    if not both:
        print("\n突き合わせ対象なし（既存の総合スコア列が空）")
        return
    print(f"\n=== 既存スコアとの突き合わせ（{len(both)}人）===")
    print(f"{'氏名':<12}{'既存':>5}{'新':>5}{'差':>6}   院内順位")
    for r in sorted(both, key=lambda r: -abs(float(r["活動量スコア"]) - float(r["総合スコア"])))[:15]:
        old, new = float(r["総合スコア"]), float(r["活動量スコア"])
        print(f"{r['氏名']:<12}{old:>5.0f}{new:>5.0f}{new - old:>+6.0f}   {r['院内順位']}")
    diffs = [float(r["活動量スコア"]) - float(r["総合スコア"]) for r in both]
    n = len(diffs)
    mean = sum(diffs) / n
    var = sum((d - mean) ** 2 for d in diffs) / n
    print(f"\n差の平均 {mean:+.1f}  標準偏差 {var ** 0.5:.1f}  "
          f"最大 {max(diffs, key=abs):+.0f}")
    within = sum(1 for d in diffs if abs(d) <= 5)
    print(f"±5点以内に収まる人: {within}/{n}")


def main():
    ap = argparse.ArgumentParser(description="TORAN 国会活動量スコア")
    ap.add_argument("csv", help="入力CSV")
    ap.add_argument("-o", "--out", help="出力CSV")
    ap.add_argument("--compare", action="store_true", help="既存の総合スコア列と突き合わせる")
    a = ap.parse_args()

    with io.open(a.csv, encoding="utf-8-sig", newline="") as fh:
        src_fields = csv.DictReader(fh).fieldnames

    rows = score(load(a.csv))
    report(rows)
    if a.compare:
        compare(rows)
    if a.out:
        write(rows, a.out, src_fields)
        print(f"\n書き出し: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
