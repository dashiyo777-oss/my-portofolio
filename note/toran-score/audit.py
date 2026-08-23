#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TORAN 名簿CSV 内部監査

外部に問い合わせずに、CSVの中だけで確かめられる矛盾を洗い出します。
制度上の定数（衆議院465＝小選挙区289＋比例176、参議院の比例100）と
突き合わせるので、一次資料に当たれない環境でもここまでは検証できます。

使い方:
    python3 audit.py 名簿.csv              # 監査結果を表示
    python3 audit.py 名簿.csv --clean 出力.csv   # 重複行を除いたCSVを書き出す
"""

import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import Counter, defaultdict

# ── 制度上の定数（ここが変わったら更新する）──
SEATS = {
    "衆議院": {"総数": 465, "小選挙区": 289, "比例": 176},
    "参議院": {"総数": 248, "選挙区": 148, "比例": 100},
}
ACTIVITY_COLS = [
    "発言数(2021.11〜2026.07)",
    "質問主意書(第207〜221回)",
    "議員立法(発議)",
    "議員立法(賛成者)",
]
# 国会議員ではないので議席数の検算対象から外す区分
NON_DIET = ("首長", "候補", "元議員")


def kata2hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def norm(s):
    s = kata2hira(unicodedata.normalize("NFKC", s))
    for a, b in (("子", "こ"), ("良", "ら"), (" ", ""), ("　", "")):
        s = s.replace(a, b)
    return s


def name_parts(n):
    p = n.strip("[]").strip().split()
    return (p[0], p[-1]) if len(p) > 1 else ("", p[0])


def blank(r, col):
    return (r.get(col) or "").strip() == ""


class Audit:
    def __init__(self, rows):
        self.rows = rows
        self.findings = []

    def add(self, level, title, detail, ids=()):
        self.findings.append((level, title, detail, list(ids)))

    # ── 1. 議席数が制度と合うか ───────────────────────────
    def check_seats(self):
        for house, spec in SEATS.items():
            g = [r for r in self.rows if r["院"] == house]
            hirei = [r for r in g if r["選挙区"].startswith("比例")]
            n, exp = len(g), spec["総数"]
            if n != exp:
                self.add("重大", f"{house}の人数が定数と違う",
                         f"CSV {n}人 / 定数 {exp}人（差 {n - exp:+}）")
            if len(hirei) != spec["比例"]:
                self.add("重大", f"{house}の比例が定数と違う",
                         f"CSV {len(hirei)}人 / 定数 {spec['比例']}人")
            else:
                self.add("情報", f"{house}の比例は定数どおり",
                         f"{len(hirei)}人")

        # 衆議院の小選挙区は1区1人。重複はどちらかが誤り。
        sho = [r for r in self.rows
               if r["院"] == "衆議院" and not r["選挙区"].startswith("比例")]
        c = Counter(r["選挙区"] for r in sho)
        dup = {k: v for k, v in c.items() if v > 1}
        if dup:
            self.add("重大", "衆議院の小選挙区に複数人がいる", str(dup))
        else:
            self.add("情報", "衆議院の小選挙区は1区1人",
                     f"{len(c)}区（定数{SEATS['衆議院']['小選挙区']}）")

    # ── 2. [ ]付きの本名行（同一人物の重複） ─────────────────
    def check_alias_rows(self):
        br = [(i, r) for i, r in enumerate(self.rows) if r["氏名"].startswith("[")]
        if not br:
            return []
        pairs, orphan = [], []
        for i, r in br:
            prev = self.rows[i - 1] if i > 0 else None
            ok = (prev is not None
                  and prev["院"] == r["院"]
                  and not prev["氏名"].startswith("["))
            if not ok:
                orphan.append(r)
                continue
            bs, bm = name_parts(r["氏名"])
            ps, pm = name_parts(prev["氏名"])
            how = ("姓が一致" if bs and norm(bs) == norm(ps)
                   else "名が一致" if norm(bm) == norm(pm)
                   else "要目視")
            pairs.append((r, prev, how))

        certain = [p for p in pairs if p[2] != "要目視"]
        eyeball = [p for p in pairs if p[2] == "要目視"]
        self.add("重大", "[ ]付きの氏名は直前行と同一人物の重複",
                 f"{len(pairs)}件（うち姓名が機械的に一致 {len(certain)}件 / "
                 f"読みでの判断が要る {len(eyeball)}件）",
                 [r["ID"] for r, _, _ in pairs])
        if orphan:
            self.add("要確認", "[ ]付きだが直前行と対応しない",
                     f"{len(orphan)}件", [r["ID"] for r in orphan])
        return pairs

    # ── 3. 行の中で矛盾している ─────────────────────────
    def check_contradictions(self):
        bad = []
        for r in self.rows:
            y, p, h = r["役職"], r["政党"], r["院"]
            if y == "（要確認）":
                continue
            if y in ("衆議院議員", "参議院議員") and y[:3] != h:
                bad.append((r, f"役職={y} だが院={h}"))
            m = re.match(r"^(自由民主党|立憲民主党|公明党|日本共産党|"
                         r"日本維新の会|国民民主党)", y)
            if m:
                party = m.group(1).replace("自由民主党", "自民党")
                if p != party:
                    bad.append((r, f"役職は{m.group(1)}の党職だが政党={p}"))
        for r, why in bad:
            self.add("重大", "行の中で矛盾", f"{r['氏名']}: {why}", [r["ID"]])
        if not bad:
            self.add("情報", "行内の矛盾なし", "")

    # ── 4. 欠損 ────────────────────────────────────
    def check_missing(self):
        for col, label in (("政党", "政党が未確定"),
                           ("よみ", "よみが空"),
                           ("選挙区", "選挙区が空")):
            miss = [r for r in self.rows
                    if blank(r, col) or r[col] == "（要確認）"]
            if miss:
                by = Counter(r["院"] for r in miss)
                self.add("要確認", label, f"{len(miss)}人 {dict(by)}",
                         [r["ID"] for r in miss])

        nodata = [r for r in self.rows
                  if any(blank(r, c) for c in ACTIVITY_COLS)]
        if nodata:
            by = Counter(r["院"] for r in nodata)
            self.add("要確認", "活動量の素材列が空",
                     f"{len(nodata)}人 {dict(by)}  ※0点ではなく未取得として扱うこと",
                     [r["ID"] for r in nodata])

    # ── 5. 同姓同名 ──────────────────────────────────
    def check_dup_names(self):
        by = defaultdict(list)
        for r in self.rows:
            if not r["氏名"].startswith("["):
                by[r["氏名"]].append(r)
        for nm, g in by.items():
            if len(g) > 1:
                where = " / ".join(f"{r['ID']}({r['院']}・{r['政党']}・{r['選挙区']})"
                                   for r in g)
                self.add("要確認", "同じ氏名が複数行",
                         f"{nm}: {where} ← 同姓同名か重複登録か要判定",
                         [r["ID"] for r in g])

    # ── 6. 作業がどこまで進んでいるか ──────────────────────
    def check_progress(self):
        for col, done_if in (("役職", lambda v: v != "（要確認）"),
                             ("ランク", lambda v: v != "未評価"),
                             ("総合スコア", lambda v: v not in ("", "0"))):
            pos = [i for i, r in enumerate(self.rows) if done_if(r[col])]
            if not pos or len(pos) == len(self.rows):
                continue
            span = f"行位置 {min(pos)}〜{max(pos)}"
            contiguous = (max(pos) - min(pos) + 1) == len(pos)
            self.add("情報", f"「{col}」が入っているのは一部だけ",
                     f"{len(pos)}/{len(self.rows)}人・{span}"
                     + ("（連続＝作業順の産物）" if contiguous
                        else "（とびとび）"))

    def run(self):
        self.check_seats()
        pairs = self.check_alias_rows()
        self.check_contradictions()
        self.check_missing()
        self.check_dup_names()
        self.check_progress()
        return pairs


def report(a):
    order = {"重大": 0, "要確認": 1, "情報": 2}
    for level in ("重大", "要確認", "情報"):
        items = [f for f in a.findings if f[0] == level]
        if not items:
            continue
        print(f"\n{'=' * 60}\n【{level}】{len(items)}件\n{'=' * 60}")
        for _, title, detail, ids in items:
            print(f"● {title}")
            if detail:
                print(f"    {detail}")
            if ids and len(ids) <= 12:
                print(f"    ID: {', '.join(ids)}")
            elif ids:
                print(f"    ID: {', '.join(ids[:12])} ほか{len(ids) - 12}件")
    assert order  # 並び順の意図を明示するためだけの参照


def merge_pairs(pairs):
    """本名行の活動量を通称行に取り込む。

    片方が空ならもう片方を採る。両方に違う値があるときは大きいほうを採り、
    呼び出し側に返して一次資料での確認を促す。足し合わせないのは、
    同じ発言が両方の表記で二重に数えられている可能性を否定できないため。
    """
    merged = 0
    conflicts = []
    for honmyo, tsusho, _ in pairs:   # honmyo=[ ]付きの本名行（消す） / tsusho=残す行
        tsusho["統合元ID"] = honmyo["ID"]
        took = False
        for c in ACTIVITY_COLS:
            a, b = tsusho[c].strip(), honmyo[c].strip()
            if a == "" and b != "":
                tsusho[c] = b
                took = True
            elif a != "" and b != "" and float(a) != float(b):
                # 片方が0なら「その表記では拾えなかった」だけなので大きいほうを採る。
                # 両方が非ゼロで食い違うときだけ、同じ発言が二重に数えられて
                # いるのか表記ごとに分かれているのか判別できないので報告する。
                if float(a) and float(b):
                    conflicts.append((tsusho["氏名"], c, float(a), float(b)))
                tsusho[c] = str(int(max(float(a), float(b))))
        merged += took
    return merged, conflicts


def main():
    ap = argparse.ArgumentParser(description="TORAN 名簿CSV 内部監査")
    ap.add_argument("csv")
    ap.add_argument("--clean", metavar="出力.csv",
                    help="[ ]付きの重複行を除いたCSVを書き出す")
    args = ap.parse_args()

    with io.open(args.csv, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields, rows = rd.fieldnames, list(rd)

    print(f"入力: {args.csv}  {len(rows)}行")
    a = Audit(rows)
    pairs = a.run()
    report(a)

    if args.clean:
        merged, conflicts = merge_pairs(pairs)
        drop = {r["ID"] for r, _, _ in pairs}
        kept = [r for r in rows if r["ID"] not in drop]
        out_fields = fields + ["統合元ID"]
        with io.open(args.clean, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(kept)
        print(f"\n書き出し: {args.clean}（{len(kept)}行）")
        print(f"  本名表記の重複 {len(drop)}行を、直前の通称行に統合しました。")
        print(f"  うち活動量を本名行から補えたのは {merged}件です。")
        if conflicts:
            print(f"\n  ⚠ 通称と本名の両方に非ゼロの値があり食い違った {len(conflicts)}件は"
                  f"大きいほうを採りました。\n"
                  f"     同じ発言の二重計上か表記ごとの分割か判別できないので、"
                  f"一次資料での確認が要ります:")
            for nm, col, a, b in conflicts:
                print(f"    {nm:<14}{col.split('(')[0]:<12}通称={a:g} / 本名={b:g}"
                      f" → 採用 {max(a, b):g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
