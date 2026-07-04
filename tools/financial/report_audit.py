#!/usr/bin/env python3
"""
Hermes port of ai-berkshire's tools/report_audit.py.

Two-stage pre-publish gate for investment research reports:

  Stage 1 — extract: read a Markdown report, identify numeric data points
            (financial values, percentages, ratios), and output a JSON
            template with 15% random sampling for human verification.

  Stage 2 — verdict: take the filled-in fetched values from the JSON template
            and judge PASS/FAIL against the 1% tolerance rule. Reports with
            any FAIL must be corrected and re-audited before publishing.

Usage:
  python3 report_audit.py extract --report PATH
  python3 report_audit.py verdict --results JSON --report PATH
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import random
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Numeric-pattern extractor — covers common ways financial numbers appear
# in zh-Hant / en investment reports
# ---------------------------------------------------------------------------
NUMBER_PATTERNS = [
    # HK$24,199 / HK$24.1B / HK$24.1億
    (re.compile(r"(HK\$|US\$|NT\$|RMB￥|￥|€|£|\$)\s*([\d,]+(?:\.\d+)?)\s*(億|億港元|億美元|十億|billion|million|萬)?"),
     "currency_value"),
    # 24.5% / 12%
    (re.compile(r"(\d+(?:\.\d+)?)\s*%"), "percentage"),
    # PE 18x / P/E 18.2 / PB 1.5x
    (re.compile(r"\b(PE|P/E|PB|P/B|PS|P/S|EV/EBITDA|ROE|ROA|FCF\s*Yield|Dividend\s*Yield)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*x?\b", re.IGNORECASE),
     "ratio"),
    # standalone numbers with unit context (e.g. "市值: 4.65 兆")
    (re.compile(r"(?:市值|營收|收入|淨利潤|利潤|cash\s*flow|revenue|profit)\s*[:：]?\s*([\d,]+(?:\.\d+)?)\s*(億|十億|兆|billion|million|萬)?"),
     "metric_value"),
]

# Header-like context regex (the line above or containing the number)
HEADER_RE = re.compile(r"^#{1,6}\s*(.+)$", re.MULTILINE)


def _classify_number(match_text: str, full_match: re.Match) -> tuple[str, str, str]:
    """Return (raw, kind, unit_hint) for a match."""
    for pat, kind in NUMBER_PATTERNS:
        if pat.pattern == full_match.re.pattern:
            # Try to recover raw + unit
            groups = full_match.groups()
            if kind == "currency_value":
                currency = groups[0]
                value = groups[1]
                unit = groups[2] or ""
                return f"{currency}{value}{unit}", kind, unit
            if kind == "percentage":
                return f"{groups[0]}%", kind, "%"
            if kind == "ratio":
                return f"{groups[0]}={groups[1]}", kind, "x"
            if kind == "metric_value":
                value = groups[0]
                unit = groups[1] or ""
                return f"{value}{unit}", kind, unit
    return match_text, "unknown", ""


def _find_context(report_lines: list[str], line_idx: int, span: int = 3) -> str:
    """Find nearest header above line_idx; otherwise return nearby text."""
    for i in range(line_idx, -1, -1):
        m = HEADER_RE.match(report_lines[i])
        if m:
            return m.group(1).strip()
    # Fall back to surrounding text
    lo, hi = max(0, line_idx - span), min(len(report_lines), line_idx + span + 1)
    return " | ".join(line.strip() for line in report_lines[lo:hi] if line.strip())[:200]


def extract_data_points(report_text: str) -> list[dict]:
    """Walk the report, identify numeric data points with surrounding context."""
    lines = report_text.split("\n")
    points: list[dict] = []
    seen: set[str] = set()  # dedupe identical numbers in same context

    for line_idx, line in enumerate(lines):
        for pat, kind in NUMBER_PATTERNS:
            for m in pat.finditer(line):
                raw, k, unit = _classify_number(m.group(0), m)
                context = _find_context(lines, line_idx)
                dedupe_key = f"{raw}|{context[:60]}"
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                points.append({
                    "id": len(points) + 1,
                    "raw_text": raw,
                    "kind": k,
                    "unit_hint": unit,
                    "context": context,
                    "line_no": line_idx + 1,
                    "fetched_value": None,   # filled by user
                    "fetched_source": None,
                    "fetched_value2": None,  # secondary source for cross-validate
                    "fetched_source2": None,
                    "status": "PENDING",
                })
    return points


def cmd_extract(args) -> int:
    path = Path(args.report)
    if not path.exists():
        print(f"❌ Report not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    all_points = extract_data_points(text)

    # 15% random sample (with floor of 5 and ceiling of all)
    n = len(all_points)
    sample_size = max(5, min(n, int(round(n * 0.15))))
    if sample_size < n:
        sampled = random.sample(all_points, sample_size)
    else:
        sampled = all_points

    out = {
        "report_path": str(path),
        "total_data_points_detected": n,
        "sample_size": sample_size,
        "sample_pct": f"{sample_size / n * 100:.1f}%" if n else "n/a",
        "tolerance_pct": "1.0%",
        "instructions": (
            "Fill `fetched_value` and `fetched_source` for each item. "
            "Optionally provide `fetched_value2` + `fetched_source2` for "
            "cross-validation. Then run `verdict` with --results <this JSON>."
        ),
        "data_points": sampled,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def _to_decimal_safe(x: Any) -> Decimal | None:
    if x is None:
        return None
    try:
        s = str(x).replace(",", "").replace(" ", "").strip()
        # Strip ratio prefix like "PE=17" → "17", "PB:2.55" → "2.55"
        s = re.sub(r"^[A-Za-z]+\s*[=:.]\s*", "", s)
        # Strip currency prefixes
        s = re.sub(r"^[A-Z]*\$", "", s)
        # Strip unit suffixes common in financial reports
        s = re.sub(r"[xX]$", "", s)  # "17x" → "17"
        # Strip magnitude suffixes (convert to underlying value but flag for context)
        for suffix in ["億港元", "億美元", "十億", "億"]:
            if s.endswith(suffix):
                s = s[: -len(suffix)]
                break
        else:
            for suffix in ["兆", "萬", "million", "billion", "thousand"]:
                if s.endswith(suffix):
                    s = s[: -len(suffix)]
                    break
        # Strip trailing percent
        if s.endswith("%"):
            s = s[:-1]
        if not s:
            return None
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def _diff_pct(a: Decimal, b: Decimal) -> Decimal:
    if a == b == 0:
        return Decimal("0")
    avg = (a + b) / Decimal("2")
    if avg == 0:
        return Decimal("inf")
    return abs(a - b) / abs(avg)


def cmd_verdict(args) -> int:
    try:
        results = json.loads(args.results)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error in --results: {e}", file=sys.stderr)
        return 2

    tolerance = Decimal(str(results.get("tolerance_pct", "1.0").rstrip("%"))) / Decimal("100")

    fails: list[dict] = []
    passes: list[dict] = []
    skipped: list[dict] = []

    for pt in results.get("data_points", []):
        if not pt.get("fetched_value"):
            skipped.append(pt)
            pt["status"] = "SKIPPED (no fetched_value)"
            continue

        reported = _to_decimal_safe(pt["raw_text"])
        fetched = _to_decimal_safe(pt["fetched_value"])
        if reported is None or fetched is None:
            skipped.append(pt)
            pt["status"] = "SKIPPED (parse error)"
            continue

        diff = _diff_pct(reported, fetched)

        # Cross-validation against second source
        cross_diff = None
        if pt.get("fetched_value2"):
            fetched2 = _to_decimal_safe(pt["fetched_value2"])
            if fetched2 is not None:
                cross_diff = _diff_pct(fetched, fetched2)

        within = diff <= tolerance
        cross_ok = (cross_diff is None) or (cross_diff <= tolerance)

        if within and cross_ok:
            passes.append(pt)
            pt["status"] = "✅ PASS"
            pt["diff_pct"] = f"{diff * 100:.4f}%"
        else:
            fails.append(pt)
            pt["status"] = "❌ FAIL"
            pt["diff_pct"] = f"{diff * 100:.4f}%"
            if cross_diff is not None:
                pt["cross_diff_pct"] = f"{cross_diff * 100:.4f}%"

    n_total = len(passes) + len(fails) + len(skipped)
    n_audited = len(passes) + len(fails)

    out = {
        "report_path": results.get("report_path"),
        "tolerance_pct": f"{tolerance * 100:.2f}%",
        "summary": {
            "total_data_points": n_total,
            "audited": n_audited,
            "passes": len(passes),
            "fails": len(fails),
            "skipped": len(skipped),
            "pass_rate_pct": f"{(len(passes) / n_audited * 100):.2f}%" if n_audited else "n/a",
        },
        "verdict": "✅【准出】" if not fails else "❌【打回】",
        "fails": fails,
        "passes_summary": f"{len(passes)} items passed",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(file=sys.stderr)
    print(f"  Total: {n_total}  Audited: {n_audited}  Pass: {len(passes)}  Fail: {len(fails)}  Skip: {len(skipped)}", file=sys.stderr)
    print(f"  Verdict: {out['verdict']}", file=sys.stderr)
    if fails:
        print(f"\n  ❌ Failed items (correct report, re-audit):", file=sys.stderr)
        for f in fails:
            print(f"    #{f['id']:3d} [{f['kind']:14s}] raw={f['raw_text']:30s} fetched={f.get('fetched_value')} diff={f.get('diff_pct', 'n/a')}", file=sys.stderr)
    return 0 if not fails else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Hermes port of ai-berkshire report audit tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("extract", help="Extract a 15% data-point sample for human verification")
    s.add_argument("--report", required=True, help="Path to the markdown report")

    s = sub.add_parser("verdict", help="Judge filled-in results against 1% tolerance")
    s.add_argument("--results", required=True, help="JSON string of filled-in audit results")
    s.add_argument("--report", help="Optional report path for context")

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return {"extract": cmd_extract, "verdict": cmd_verdict}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())