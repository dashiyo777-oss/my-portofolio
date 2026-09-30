#!/usr/bin/env python3
"""官報（kanpo.go.jp）直近90日分を保存するスクリプト。

官報発行サイトは発行から原則90日間だけ全体をPDFで公開し、それ以降は
プライバシー配慮記事（破産・相続財産・行旅死亡人など）が消える。
消える前に、各号の「一括PDF」と「目次（記事タイトル一覧）」を保存する。

使い方:
    python3 kanpo/fetch_kanpo.py [--out DIR] [--since YYYYMMDD] [--skip-dates FILE] [--toc-only]

出力:
    DIR/pdf/YYYYMMDD/<号ID>full<開始><終了>.pdf   … 一括PDF（容量大・非公開で保管すること）
    kanpo/toc/YYYYMMDD.json                        … 目次（見出し・記事タイトル・ページ）
既にあるファイルはスキップするので、毎日実行すれば差分だけ取得される。
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request

BASE = "https://www.kanpo.go.jp/"
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (kanpo-archiver; personal research)"


def get(url, binary=False, retries=4):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            if i == retries - 1:
                raise
            print(f"  retry {url}: {e}", file=sys.stderr)
            time.sleep(2 ** (i + 1))


def list_issues():
    """トップページから {日付: {号ID: [一括PDFの(開始,終了)]}} を作る。"""
    top = get(BASE)
    issues = {}
    for date, issue in re.findall(r'\./(\d{8})/(\d{8}[a-z]\d{5})/\2(?:0000f|full)', top):
        issues.setdefault(date, {}).setdefault(issue, [])
    for date, issue, a, b in re.findall(r'\./(\d{8})/(\d{8}[a-z]\d{5})/\2full(\d{4})(\d{4})f\.html', top):
        rng = (a, b)
        if rng not in issues[date][issue]:
            issues[date][issue].append(rng)
    return issues


KIND = {"h": "本紙", "g": "号外", "c": "政府調達", "t": "特別号外", "m": "目録"}


def parse_toc(page):
    """号の目次ページから [{section, title, page}] を抜き出す。"""
    items = []
    for sec in re.findall(r"<section>(.*?)</section>", page, re.S):
        m = re.search(r'<h2 class="title">\s*<span class="text">(.*?)</span>', sec, re.S)
        section = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
        for t, p in re.findall(
            r'<a [^>]*>\s*<span class="text">(.*?)</span>\s*<span class="date">(.*?)</span>', sec, re.S
        ):
            items.append({
                "section": section,
                "title": html.unescape(re.sub(r"<[^>]+>", "", t)).strip(),
                "page": re.sub(r"\D", "", p) or None,
            })
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "data"), help="PDF保存先（非公開の場所に）")
    ap.add_argument("--since", default="00000000", help="この日付以降の号だけ取得")
    ap.add_argument("--skip-dates", help="保管済みの日付(YYYYMMDD)を1行ずつ書いたファイル。該当日は取得しない")
    ap.add_argument("--toc-only", action="store_true", help="目次だけ取得しPDFは落とさない")
    args = ap.parse_args()

    skip = set()
    if args.skip_dates and os.path.exists(args.skip_dates):
        with open(args.skip_dates) as f:
            skip = {line.strip() for line in f if line.strip()}

    toc_dir = os.path.join(HERE, "toc")
    os.makedirs(toc_dir, exist_ok=True)
    issues = list_issues()
    print(f"{len(issues)} 日分の官報を検出", file=sys.stderr)

    total = 0
    for date in sorted(issues):
        if date < args.since or date in skip:
            continue
        toc_path = os.path.join(toc_dir, f"{date}.json")
        day = {"date": date, "issues": []}
        for issue, ranges in sorted(issues[date].items()):
            d = f"{BASE}{date}/{issue}/"
            kind = KIND.get(issue[8], issue[8])
            entry = {"id": issue, "kind": kind, "number": int(issue[9:]), "pdfs": [], "items": []}
            try:
                entry["items"] = parse_toc(get(f"{d}{issue}0000f.html"))
            except Exception as e:  # noqa: BLE001
                print(f"  目次取得失敗 {issue}: {e}", file=sys.stderr)
            for a, b in ranges:
                name = f"{issue}full{a}{b}.pdf"
                url = f"{d}pdf/{name}"
                entry["pdfs"].append({"file": name, "url": url, "pages": f"{int(a)}-{int(b)}"})
                if args.toc_only:
                    continue
                dst = os.path.join(args.out, "pdf", date, name)
                if os.path.exists(dst) and os.path.getsize(dst) > 0:
                    continue
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                data = get(url, binary=True)
                with open(dst + ".part", "wb") as f:
                    f.write(data)
                os.replace(dst + ".part", dst)
                total += len(data)
                print(f"  {date} {kind} {name} {len(data)/1e6:.1f}MB", file=sys.stderr)
                time.sleep(0.5)  # 相手サーバーへの配慮
            day["issues"].append(entry)
        with open(toc_path, "w", encoding="utf-8") as f:
            json.dump(day, f, ensure_ascii=False, indent=1)
    print(f"完了: 新規 {total/1e6:.0f}MB", file=sys.stderr)


if __name__ == "__main__":
    main()
