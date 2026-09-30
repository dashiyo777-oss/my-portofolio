#!/usr/bin/env python3
"""目次(toc/*.json)から「裁判所公告（破産・相続・失踪など）」が占めるページ数を数える。

目次の各記事には開始ページしかないため、次の記事の開始ページ（最後なら号の最終ページ+1）
までを、その記事のページ数とみなす。政府調達は対象外。
"""
import collections
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
COURT = re.compile("破産|相続|失踪|免責|再生関係|公示催告|除権")

total = collections.Counter()
court = collections.Counter()
days = issues = 0
for f in sorted(glob.glob(os.path.join(HERE, "toc", "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    days += 1
    for i in d["issues"]:
        if i["kind"] == "政府調達" or not i["pdfs"]:
            continue
        issues += 1
        end = max(int(p["pages"].split("-")[1]) for p in i["pdfs"])
        total[i["kind"]] += end
        items = sorted(((int(it["page"]), it) for it in i["items"] if it["page"]), key=lambda x: x[0])
        for n, (page, it) in enumerate(items):
            if it["section"] == "公告" and COURT.search(it["title"]):
                later = [p for p, _ in items[n + 1:] if p > page]
                court[i["kind"]] += max((later[0] if later else end + 1) - page, 1)

print(f"{days}日分・{issues}号（政府調達を除く）")
for k in sorted(total, key=total.get, reverse=True):
    print(f"  {k}: 全{total[k]}ページ中 裁判所公告 {court[k]}ページ（{court[k] / total[k]:.1%}）")
T, C = sum(total.values()), sum(court.values())
print(f"  合計: 全{T}ページ中 裁判所公告 {C}ページ（{C / T:.1%}）")
