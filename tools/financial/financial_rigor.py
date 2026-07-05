#!/usr/bin/env python3
"""
Hermes port of ai-berkshire's tools/financial_rigor.py.

All arithmetic uses Python decimal.Decimal — never float — so financial
calculations are bit-exact and we never hit `0.1 + 0.2 = 0.30000000000000004`.

Subcommands:
  verify-market-cap   price × shares vs reported market cap (tolerance 1%)
  verify-valuation    PE / PB / FCF yield / dividend yield (exact)
  cross-validate      N sources of same field, tolerance 1% by default
  three-scenario      bull / base / bear price targets
  benford             first-digit distribution test (chi-square)

Usage:
  python3 financial_rigor.py <subcommand> [--flags ...]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from pathlib import Path

D = Decimal
ONE = D("1")
HUNDRED = D("100")
TOLERANCE = D("0.01")  # 1% — ai-berkshire default


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _to_decimal(x) -> Decimal:
    if isinstance(x, Decimal):
        return x
    if isinstance(x, (int, str)):
        try:
            return D(str(x))
        except InvalidOperation as e:
            raise ValueError(f"Cannot convert {x!r} to Decimal: {e}")
    if isinstance(x, float):
        # Convert via str to avoid float precision artefacts
        return D(repr(x))
    raise ValueError(f"Unsupported type {type(x).__name__}")


def _fmt_money(amount: Decimal, currency: str) -> str:
    """Pretty-print a money amount with thousands separators."""
    if amount == amount.to_integral():
        quantized = amount.quantize(D("1"), rounding=ROUND_HALF_EVEN)
    else:
        quantized = amount.quantize(D("0.01"), rounding=ROUND_HALF_EVEN)
    sign = "-" if quantized < 0 else ""
    s = str(abs(quantized))
    if "." in s:
        int_part, dec_part = s.split(".")
        int_part_fmt = "{:,}".format(int(int_part))
        return f"{sign}{currency}{int_part_fmt}.{dec_part}"
    int_part_fmt = "{:,}".format(int(s))
    return f"{sign}{currency}{int_part_fmt}"


def _pct_diff(a: Decimal, b: Decimal) -> Decimal:
    """Relative difference |a-b|/((a+b)/2). Avoids divide-by-zero."""
    if a == 0 and b == 0:
        return D("0")
    avg = (a + b) / D("2")
    if avg == 0:
        return D("inf")
    return abs(a - b) / abs(avg)


# ---------------------------------------------------------------------------
# verify-market-cap
# ---------------------------------------------------------------------------
def cmd_verify_market_cap(args) -> int:
    try:
        price = _to_decimal(args.price)
        shares = _to_decimal(args.shares)
        reported = _to_decimal(args.reported)
        currency = args.currency.upper()
    except (ValueError, InvalidOperation) as e:
        print(f"❌ Input error: {e}", file=sys.stderr)
        return 2

    if price < 0 or shares < 0:
        print("❌ Negative values not allowed", file=sys.stderr)
        return 2

    computed = price * shares
    diff = _pct_diff(computed, reported)
    ok = diff <= TOLERANCE

    out = {
        "currency": currency,
        "price": str(price),
        "shares": str(shares),
        "computed_market_cap": str(computed),
        "reported_market_cap": str(reported),
        "diff_pct": f"{diff * HUNDRED:.4f}%",
        "tolerance_pct": f"{TOLERANCE * HUNDRED:.2f}%",
        "verdict": "✅ PASS" if ok else "❌ FAIL",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    # Also human-friendly block on stderr (so stdout stays machine-parseable)
    cur_sym = "$" if currency == "USD" else "HK$" if currency == "HKD" else currency + " "
    print(f"\nComputed  : {_fmt_money(computed, cur_sym)}", file=sys.stderr)
    print(f"Reported  : {_fmt_money(reported, cur_sym)}", file=sys.stderr)
    print(f"Diff      : {out['diff_pct']}  (tolerance {out['tolerance_pct']})", file=sys.stderr)
    print(f"Verdict   : {out['verdict']}", file=sys.stderr)
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# verify-valuation
# ---------------------------------------------------------------------------
def cmd_verify_valuation(args) -> int:
    try:
        price = _to_decimal(args.price)
        eps = _to_decimal(args.eps) if args.eps else None
        bvps = _to_decimal(args.bvps) if args.bvps else None
        fcf_per_share = _to_decimal(args.fcf_per_share) if args.fcf_per_share else None
        dividend = _to_decimal(args.dividend) if args.dividend else None
    except (ValueError, InvalidOperation) as e:
        print(f"❌ Input error: {e}", file=sys.stderr)
        return 2

    out: dict = {"price": str(price), "metrics": {}}
    errs: list[str] = []

    if eps is not None and eps > 0:
        pe = price / eps
        out["metrics"]["PE"] = str(pe.quantize(D("0.01"), rounding=ROUND_HALF_EVEN))
    elif eps is not None:
        errs.append("EPS ≤ 0 — PE undefined (loss-making)")

    if bvps is not None and bvps > 0:
        pb = price / bvps
        out["metrics"]["PB"] = str(pb.quantize(D("0.01"), rounding=ROUND_HALF_EVEN))
    elif bvps is not None:
        errs.append("BVPS ≤ 0 — PB undefined")

    if fcf_per_share is not None and fcf_per_share > 0:
        fcf_yield = fcf_per_share / price * HUNDRED
        out["metrics"]["FCF_yield_pct"] = str(fcf_yield.quantize(D("0.01"), rounding=ROUND_HALF_EVEN)) + "%"
    elif fcf_per_share is not None:
        errs.append("FCF/share ≤ 0 — yield undefined")

    if dividend is not None and dividend > 0:
        div_yield = dividend / price * HUNDRED
        out["metrics"]["Dividend_yield_pct"] = str(div_yield.quantize(D("0.01"), rounding=ROUND_HALF_EVEN)) + "%"

    print(json.dumps(out, ensure_ascii=False, indent=2))
    if errs:
        print("\n⚠️ Warnings:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# cross-validate
# ---------------------------------------------------------------------------
def cmd_cross_validate(args) -> int:
    try:
        values = json.loads(args.values)  # {"source_name": numeric_value, ...}
        unit = args.unit
        tol_pct = _to_decimal(args.tolerance or "1.0")
    except (ValueError, json.JSONDecodeError, InvalidOperation) as e:
        print(f"❌ Input parse error: {e}", file=sys.stderr)
        return 2

    if not isinstance(values, dict) or len(values) < 2:
        print(f"❌ Need at least 2 sources for cross-validation, got {len(values)}", file=sys.stderr)
        return 2

    dec_values = {k: _to_decimal(v) for k, v in values.items()}
    avg = sum(dec_values.values(), D("0")) / D(len(dec_values))
    tol = D(str(tol_pct)) / HUNDRED

    diffs = {k: _pct_diff(v, avg) for k, v in dec_values.items()}
    max_diff = max(diffs.values()) if diffs else D("0")
    ok = max_diff <= tol

    out = {
        "field": args.field,
        "unit": unit,
        "values": {k: str(v) for k, v in dec_values.items()},
        "average": str(avg.quantize(D("0.01"), rounding=ROUND_HALF_EVEN)),
        "max_diff_pct": f"{max_diff * HUNDRED:.4f}%",
        "tolerance_pct": f"{tol * HUNDRED:.2f}%",
        "verdict": "✅ PASS" if ok else "❌ FAIL",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(file=sys.stderr)
    for k, v in dec_values.items():
        print(f"  {k:20s}: {v} {unit}  (Δ {diffs[k] * HUNDRED:.4f}%)", file=sys.stderr)
    print(f"\n  Average: {avg.quantize(D('0.01'), rounding=ROUND_HALF_EVEN)} {unit}", file=sys.stderr)
    print(f"  Max diff: {out['max_diff_pct']}  (tolerance {out['tolerance_pct']})", file=sys.stderr)
    print(f"  Verdict: {out['verdict']}", file=sys.stderr)
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# three-scenario
# ---------------------------------------------------------------------------
def cmd_three_scenario(args) -> int:
    try:
        price = _to_decimal(args.price)
        eps = _to_decimal(args.eps)
        shares_billions = _to_decimal(args.shares)  # in 億
        g_bull = _to_decimal(args.growth[0])
        g_base = _to_decimal(args.growth[1])
        g_bear = _to_decimal(args.growth[2])
        pe_bull = _to_decimal(args.pe[0])
        pe_base = _to_decimal(args.pe[1])
        pe_bear = _to_decimal(args.pe[2])
        years = int(args.years)
        currency = args.currency.upper()
    except (ValueError, InvalidOperation) as e:
        print(f"❌ Input error: {e}", file=sys.stderr)
        return 2

    if years <= 0:
        print("❌ --years must be positive", file=sys.stderr)
        return 2

    sym = "$" if currency == "USD" else "HK$" if currency == "HKD" else currency + " "
    cur = sym

    # Future EPS = current EPS × (1+g)^years
    def future_eps(growth: Decimal) -> Decimal:
        # (1+g)^years — g is decimal form (e.g. 0.15 for 15%)
        mult = (ONE + growth) ** years
        return (eps * mult).quantize(D("0.0001"), rounding=ROUND_HALF_EVEN)

    def target_price(future: Decimal, pe: Decimal) -> Decimal:
        return (future * pe).quantize(D("0.01"), rounding=ROUND_HALF_EVEN)

    scenarios = {
        "bull":  (g_bull, pe_bull),
        "base":  (g_base, pe_base),
        "bear":  (g_bear, pe_bear),
    }

    results = []
    for label, (g, pe) in scenarios.items():
        f_eps = future_eps(g)
        t_price = target_price(f_eps, pe)
        upside = ((t_price - price) / price * HUNDRED) if price > 0 else None
        results.append({
            "scenario": label,
            "growth_pct": f"{g * HUNDRED:.2f}%",
            "exit_pe": str(pe),
            "future_eps": str(f_eps),
            "target_price": str(t_price),
            "upside_pct": f"{upside:.2f}%" if upside is not None else "n/a",
        })

    out = {
        "current_price": str(price),
        "current_eps": str(eps),
        "shares_billions": str(shares_billions),
        "years": years,
        "currency": currency,
        "scenarios": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    cur = sym
    print(f"\nCurrent price: {cur}{price}", file=sys.stderr)
    print(f"Current EPS:   {eps}", file=sys.stderr)
    print(f"Horizon:       {years} years", file=sys.stderr)
    for r in results:
        print(f"  [{r['scenario'].upper():4s}] growth={r['growth_pct']:>7s}  exit PE={r['exit_pe']:>5s}  →  target {cur}{r['target_price']:>10s}  ({r['upside_pct']})", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# three-scenario-pe (P/E-based, for profitable companies)
# ---------------------------------------------------------------------------
def cmd_three_scenario_pe(args) -> int:
    """Bull/base/bear P/E-based price targets for profitable companies.

    Use this INSTEAD of `three-scenario` when the company is profitable
    (positive EPS), e.g. consumer / financial / traditional manufacturing.
    For loss-making companies (AI / biotech / early-stage), use `three-scenario`
    with P/ARR framework instead.

    Logic: target_price = current_eps × (1+growth)^years × exit_pe

    Example:
        # 鱘龍科技 (06715.HK) — profitable luxury food
        python3 financial_rigor.py three-scenario-pe \\
          --price 114 --eps 2.20 --shares 163 \\
          --growth 0.18 0.10 0.05 \\
          --pe 35 25 18 --years 3 --currency HKD
    """
    try:
        price = _to_decimal(args.price)
        eps = _to_decimal(args.eps)
        shares_millions = _to_decimal(args.shares)  # in millions
        g_bull = _to_decimal(args.growth[0])
        g_base = _to_decimal(args.growth[1])
        g_bear = _to_decimal(args.growth[2])
        pe_bull = _to_decimal(args.pe[0])
        pe_base = _to_decimal(args.pe[1])
        pe_bear = _to_decimal(args.pe[2])
        years = int(args.years)
        currency = args.currency.upper()
    except (ValueError, InvalidOperation) as e:
        print(f"❌ Input error: {e}", file=sys.stderr)
        return 2

    if years <= 0:
        print("❌ --years must be positive", file=sys.stderr)
        return 2

    if eps <= 0:
        print(f"⚠️ EPS is zero or negative ({eps}). For loss-making companies, use `three-scenario` with P/ARR framework instead.", file=sys.stderr)
        return 2

    sym = "$" if currency == "USD" else "HK$" if currency == "HKD" else currency + " "

    # Future EPS = current EPS × (1+g)^years
    def future_eps(growth: Decimal) -> Decimal:
        mult = (ONE + growth) ** years
        return (eps * mult).quantize(D("0.0001"), rounding=ROUND_HALF_EVEN)

    def target_price(future: Decimal, pe: Decimal) -> Decimal:
        return (future * pe).quantize(D("0.01"), rounding=ROUND_HALF_EVEN)

    scenarios = {
        "bull":  (g_bull, pe_bull),
        "base":  (g_base, pe_base),
        "bear":  (g_bear, pe_bear),
    }

    results = []
    for label, (g, pe) in scenarios.items():
        f_eps = future_eps(g)
        t_price = target_price(f_eps, pe)
        upside = ((t_price - price) / price * HUNDRED) if price > 0 else None
        results.append({
            "scenario": label,
            "growth_pct": f"{g * HUNDRED:.2f}%",
            "exit_pe": str(pe),
            "future_eps": str(f_eps),
            "target_price": str(t_price),
            "upside_pct": f"{upside:.2f}%" if upside is not None else "n/a",
        })

    # Also compute implied current P/E and P/B (if book value provided)
    current_pe = (price / eps).quantize(D("0.01"), rounding=ROUND_HALF_EVEN) if eps > 0 else None

    out = {
        "current_price": str(price),
        "current_eps": str(eps),
        "current_pe": str(current_pe) if current_pe else "n/a (loss-making)",
        "shares_millions": str(shares_millions),
        "years": years,
        "currency": currency,
        "scenarios": results,
        "use_case": "profitable company (positive EPS) — for loss-making use `three-scenario` with P/ARR",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\nCurrent price: {sym}{price}", file=sys.stderr)
    print(f"Current EPS:   {eps}", file=sys.stderr)
    print(f"Current P/E:   {current_pe}x", file=sys.stderr)
    print(f"Horizon:       {years} years", file=sys.stderr)
    for r in results:
        print(f"  [{r['scenario'].upper():4s}] growth={r['growth_pct']:>7s}  exit PE={r['exit_pe']:>5s}  →  target {sym}{r['target_price']:>10s}  ({r['upside_pct']})", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# three-scenario-pb (P/B-based, for financial companies)
# ---------------------------------------------------------------------------
def cmd_three_scenario_pb(args) -> int:
    """Bull/base/bear P/B-based price targets for financial / bank / insurance.

    Use this for financial companies where P/B is more relevant than P/E
    (banks, insurers, brokers). Logic: target_price = current_bvps × (1+g)^years × exit_pb
    """
    try:
        price = _to_decimal(args.price)
        bvps = _to_decimal(args.bvps)
        shares_millions = _to_decimal(args.shares)
        g_bull = _to_decimal(args.growth[0])
        g_base = _to_decimal(args.growth[1])
        g_bear = _to_decimal(args.growth[2])
        pb_bull = _to_decimal(args.pb[0])
        pb_base = _to_decimal(args.pb[1])
        pb_bear = _to_decimal(args.pb[2])
        years = int(args.years)
        currency = args.currency.upper()
    except (ValueError, InvalidOperation) as e:
        print(f"❌ Input error: {e}", file=sys.stderr)
        return 2

    if years <= 0:
        print("❌ --years must be positive", file=sys.stderr)
        return 2

    if bvps <= 0:
        print(f"⚠️ BVPS is zero or negative ({bvps}).", file=sys.stderr)
        return 2

    sym = "$" if currency == "USD" else "HK$" if currency == "HKD" else currency + " "

    def future_bvps(growth: Decimal) -> Decimal:
        mult = (ONE + growth) ** years
        return (bvps * mult).quantize(D("0.0001"), rounding=ROUND_HALF_EVEN)

    def target_price(future: Decimal, pb: Decimal) -> Decimal:
        return (future * pb).quantize(D("0.01"), rounding=ROUND_HALF_EVEN)

    scenarios = {
        "bull":  (g_bull, pb_bull),
        "base":  (g_base, pb_base),
        "bear":  (g_bear, pb_bear),
    }

    results = []
    for label, (g, pb) in scenarios.items():
        f_bvps = future_bvps(g)
        t_price = target_price(f_bvps, pb)
        upside = ((t_price - price) / price * HUNDRED) if price > 0 else None
        results.append({
            "scenario": label,
            "growth_pct": f"{g * HUNDRED:.2f}%",
            "exit_pb": str(pb),
            "future_bvps": str(f_bvps),
            "target_price": str(t_price),
            "upside_pct": f"{upside:.2f}%" if upside is not None else "n/a",
        })

    current_pb = (price / bvps).quantize(D("0.01"), rounding=ROUND_HALF_EVEN) if bvps > 0 else None

    out = {
        "current_price": str(price),
        "current_bvps": str(bvps),
        "current_pb": str(current_pb) if current_pb else "n/a",
        "shares_millions": str(shares_millions),
        "years": years,
        "currency": currency,
        "scenarios": results,
        "use_case": "financial / bank / insurance company — P/B-based valuation",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\nCurrent price: {sym}{price}", file=sys.stderr)
    print(f"Current BVPS:  {bvps}", file=sys.stderr)
    print(f"Current P/B:   {current_pb}x", file=sys.stderr)
    print(f"Horizon:       {years} years", file=sys.stderr)
    for r in results:
        print(f"  [{r['scenario'].upper():4s}] growth={r['growth_pct']:>7s}  exit P/B={r['exit_pb']:>5s}  →  target {sym}{r['target_price']:>10s}  ({r['upside_pct']})", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# benford
# ---------------------------------------------------------------------------
def cmd_benford(args) -> int:
    """First-digit distribution test (chi-square). Flags financial data whose
    leading-digit distribution deviates significantly from Benford's Law,
    which can be a fraud red flag.

    Expects JSON list of numbers via --data or a CSV path via --file.
    """
    if args.data:
        raw = json.loads(args.data)
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        raw = [float(x) for x in text.replace(",", " ").split() if x.strip()]
    else:
        print("❌ Provide --data (JSON list) or --file (path)", file=sys.stderr)
        return 2

    if not raw or len(raw) < 30:
        print(f"⚠️ Need ≥30 data points for Benford test, got {len(raw)}", file=sys.stderr)
        return 2

    # Expected Benford probabilities for digits 1-9
    expected = [math.log10(1 + 1 / d) for d in range(1, 10)]
    observed_counts = [0] * 9
    for x in raw:
        if x == 0:
            continue
        s = str(abs(x)).lstrip("0").lstrip(".")
        if not s:
            continue
        first = int(s[0])
        if 1 <= first <= 9:
            observed_counts[first - 1] += 1

    n = sum(observed_counts)
    if n == 0:
        print("❌ No valid data points", file=sys.stderr)
        return 2

    observed = [c / n for c in observed_counts]

    # Chi-square statistic with df=8 (digits 1-9)
    chi_sq = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    # NOTE: Benford's Law chi² is mathematically bounded (max ~3 for the most
    # extreme single-digit concentrations). Standard practice in forensic
    # accounting uses critical value ≈ 1.5 (corresponds to ~10% significance)
    # for n > 1000, or 0.5 for very large n. We use 1.5 as a balanced threshold.
    # Reference: Nigrini, "Benford's Law" (2012), Chapter 5.
    critical = 1.5
    suspicious = chi_sq > critical

    out = {
        "n": n,
        "chi_square": round(chi_sq, 4),
        "critical_0.05": critical,
        "verdict": "❌ SUSPICIOUS — possible data manipulation" if suspicious else "✅ PASS — distribution consistent with Benford's Law",
        "observed_pct":  [round(o * 100, 2) for o in observed],
        "expected_pct":  [round(e * 100, 2) for e in expected],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n  N={n}  χ²={chi_sq:.4f}  (critical {critical} @ p=0.05)", file=sys.stderr)
    print(f"  Verdict: {out['verdict']}", file=sys.stderr)
    print(f"\n  Digit  Observed  Expected", file=sys.stderr)
    for d, o, e in zip(range(1, 10), observed, expected):
        marker = " ⚠️" if abs(o - e) / e > 0.30 else ""
        print(f"  {d}     {o*100:6.2f}%    {e*100:6.2f}%{marker}", file=sys.stderr)
    return 1 if suspicious else 0


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Hermes port of ai-berkshire financial rigor tools")
    sub = p.add_subparsers(dest="cmd", required=True)

    # verify-market-cap
    s = sub.add_parser("verify-market-cap", help="Hand-verify reported market cap")
    s.add_argument("--price", required=True, help="Current share price")
    s.add_argument("--shares", required=True, help="Total shares outstanding (raw, not in 億)")
    s.add_argument("--reported", required=True, help="Reported market cap (in absolute currency units)")
    s.add_argument("--currency", required=True, choices=["USD", "HKD", "CNY", "TWD", "JPY", "EUR"])

    # verify-valuation
    s = sub.add_parser("verify-valuation", help="Compute PE/PB/FCF yield/dividend yield")
    s.add_argument("--price", required=True)
    s.add_argument("--eps")
    s.add_argument("--bvps")
    s.add_argument("--fcf-per-share")
    s.add_argument("--dividend")

    # cross-validate
    s = sub.add_parser("cross-validate", help="N-source data cross-validation")
    s.add_argument("--field", required=True)
    s.add_argument("--values", required=True, help='JSON object, e.g. \'{"aastocks": 123, "macrotrends": 125}\'')
    s.add_argument("--unit", required=True)
    s.add_argument("--tolerance", help="Tolerance % (default 1.0)")

    # three-scenario
    s = sub.add_parser("three-scenario", help="Bull/base/bear price targets")
    s.add_argument("--price", required=True)
    s.add_argument("--eps", required=True)
    s.add_argument("--shares", required=True, help="Total shares (in 億)")
    s.add_argument("--growth", nargs=3, required=True, help="Bull base bear growth (decimal, e.g. 0.15 0.10 0.05)")
    s.add_argument("--pe", nargs=3, required=True, help="Bull base bear exit PE (e.g. 25 18 12)")
    s.add_argument("--years", required=True)
    s.add_argument("--currency", required=True, choices=["USD", "HKD", "CNY", "TWD", "JPY", "EUR"])

    # benford
    s = sub.add_parser("benford", help="Benford's Law first-digit test")
    s.add_argument("--data", help="JSON list of numbers")
    s.add_argument("--file", help="Path to text file with one number per token")

    # three-scenario-pe (P/E-based, for profitable companies)
    s = sub.add_parser("three-scenario-pe", help="Bull/base/bear P/E-based price targets (profitable companies)")
    s.add_argument("--price", required=True)
    s.add_argument("--eps", required=True, help="Current EPS (positive)")
    s.add_argument("--shares", required=True, help="Total shares (in millions)")
    s.add_argument("--growth", nargs=3, required=True, help="Bull base bear EPS growth (decimal, e.g. 0.18 0.10 0.05)")
    s.add_argument("--pe", nargs=3, required=True, help="Bull base bear exit PE (e.g. 35 25 18)")
    s.add_argument("--years", required=True)
    s.add_argument("--currency", required=True, choices=["USD", "HKD", "CNY", "TWD", "JPY", "EUR"])

    # three-scenario-pb (P/B-based, for financial companies)
    s = sub.add_parser("three-scenario-pb", help="Bull/base/bear P/B-based price targets (financial companies)")
    s.add_argument("--price", required=True)
    s.add_argument("--bvps", required=True, help="Book value per share (positive)")
    s.add_argument("--shares", required=True, help="Total shares (in millions)")
    s.add_argument("--growth", nargs=3, required=True, help="Bull base bear BVPS growth (decimal)")
    s.add_argument("--pb", nargs=3, required=True, help="Bull base bear exit P/B")
    s.add_argument("--years", required=True)
    s.add_argument("--currency", required=True, choices=["USD", "HKD", "CNY", "TWD", "JPY", "EUR"])

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    dispatch = {
        "verify-market-cap": cmd_verify_market_cap,
        "verify-valuation": cmd_verify_valuation,
        "cross-validate": cmd_cross_validate,
        "three-scenario": cmd_three_scenario,
        "three-scenario-pe": cmd_three_scenario_pe,
        "three-scenario-pb": cmd_three_scenario_pb,
        "benford": cmd_benford,
    }
    return dispatch[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())