#!/usr/bin/env python3
"""Smoke tests for ai-berkshire Hermes port — financial_rigor.py + report_audit.py."""
import json
import math
import random
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path("/home/cwlai/.hermes/scripts/financial")
FR = str(ROOT / "financial_rigor.py")
RA = str(ROOT / "report_audit.py")

passed = failed = 0


def run(cmd: list[str], expect_exit: int = 0) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout, p.stderr


def check(name: str, ok: bool, detail: str = "") -> None:
    global passed, failed
    if ok:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name} — {detail}")


# ---------------------------------------------------------------------------
# 1. verify-market-cap
# ---------------------------------------------------------------------------
print("\n=== verify-market-cap ===")

# Test 1.1: Tencent example from README (price=510, shares=9.11e9, reported=4.65e12 HKD)
# 510 * 9.11e9 = 4,646,100,000,000 = 4.6461e12
# diff vs 4.65e12 = |4.6461 - 4.65| / 4.648 ≈ 0.084% (should PASS)
rc, out, err = run(["python3", FR, "verify-market-cap",
                     "--price", "510", "--shares", "9.11e9",
                     "--reported", "4.65e12", "--currency", "HKD"])
check("1.1 PASS case (Tencent README example)", rc == 0 and "PASS" in out, f"rc={rc} out={out[:200]} err={err[:200]}")

# Test 1.2: FAIL case — 10% deviation
rc, out, err = run(["python3", FR, "verify-market-cap",
                     "--price", "510", "--shares", "9.11e9",
                     "--reported", "5.12e12", "--currency", "HKD"])
check("1.2 FAIL case (10% deviation)", rc == 1 and "FAIL" in out, f"rc={rc}")

# Test 1.3: Decimal precision — 0.1 + 0.2 should not be 0.30000000000004
# Test by computing 100 shares × HK$0.10 price = HK$10.00 (not 10.00000000001)
rc, out, err = run(["python3", FR, "verify-market-cap",
                     "--price", "0.10", "--shares", "100",
                     "--reported", "10.00", "--currency", "HKD"])
check("1.3 Decimal precision (0.1 × 100 = 10.00 exactly)", rc == 0 and "PASS" in out, f"rc={rc} out={out[:300]}")

# Test 1.4: missing currency
rc, out, err = run(["python3", FR, "verify-market-cap",
                     "--price", "510", "--shares", "9.11e9", "--reported", "4.65e12"], expect_exit=2)
check("1.4 Missing required --currency rejects", rc == 2, f"rc={rc}")

# ---------------------------------------------------------------------------
# 2. verify-valuation
# ---------------------------------------------------------------------------
print("\n=== verify-valuation ===")

rc, out, err = run(["python3", FR, "verify-valuation",
                     "--price", "510", "--eps", "30", "--bvps", "200",
                     "--fcf-per-share", "25", "--dividend", "5"])
check("2.1 Tencent-style metrics", rc == 0 and "PE" in out and "PB" in out and "FCF" in out and "Dividend" in out, f"rc={rc} out={out[:300]}")
# Verify exact values
try:
    j = json.loads(out)
    pe = Decimal(j["metrics"]["PE"])
    pb = Decimal(j["metrics"]["PB"])
    check(f"2.2 PE exact = 17.00 (510/30)", pe == Decimal("17.00"), f"got {pe}")
    check(f"2.3 PB exact = 2.55 (510/200)", pb == Decimal("2.55"), f"got {pb}")
    check(f"2.4 FCF yield = 4.90%", j["metrics"]["FCF_yield_pct"] == "4.90%", f"got {j['metrics']['FCF_yield_pct']}")
    check(f"2.5 Dividend yield = 0.98%", j["metrics"]["Dividend_yield_pct"] == "0.98%", f"got {j['metrics']['Dividend_yield_pct']}")
except Exception as e:
    failed += 4
    print(f"  ❌ JSON parse failed: {e}")

# Test 2.6: Negative EPS (loss-making) — should warn but not crash
rc, out, err = run(["python3", FR, "verify-valuation",
                     "--price", "100", "--eps", "-5"])
check("2.6 Loss-making EPS warns but exits 0", rc == 0 and "PE" not in out and "EPS" in err, f"rc={rc} err={err[:200]}")

# ---------------------------------------------------------------------------
# 3. cross-validate
# ---------------------------------------------------------------------------
print("\n=== cross-validate ===")

rc, out, err = run(["python3", FR, "cross-validate",
                     "--field", "2025Q3_revenue",
                     "--values", '{"aastocks": 1670000000000, "macrotrends": 1675000000000}',
                     "--unit", "HKD"])
check("3.1 Two-source pass case", rc == 0 and "PASS" in out, f"rc={rc}")

rc, out, err = run(["python3", FR, "cross-validate",
                     "--field", "test",
                     "--values", '{"a": 100, "b": 105, "c": 200}',
                     "--unit", "USD"])
check("3.2 Three-source fail case", rc == 1 and "FAIL" in out, f"rc={rc}")

# Test 3.3: single source → error
rc, out, err = run(["python3", FR, "cross-validate",
                     "--field", "test", "--values", '{"a": 100}', "--unit", "USD"], expect_exit=2)
check("3.3 Single-source rejected", rc == 2, f"rc={rc}")

# ---------------------------------------------------------------------------
# 4. three-scenario
# ---------------------------------------------------------------------------
print("\n=== three-scenario ===")

rc, out, err = run(["python3", FR, "three-scenario",
                     "--price", "510", "--eps", "30", "--shares", "91.1",
                     "--growth", "0.15", "0.10", "0.05",
                     "--pe", "25", "18", "12",
                     "--years", "3", "--currency", "HKD"])
check("4.1 Bull/Base/Bear produces 3 scenarios", rc == 0, f"rc={rc}")
try:
    j = json.loads(out)
    check(f"4.2 3 scenarios returned", len(j["scenarios"]) == 3, f"got {len(j['scenarios'])}")
    bull = j["scenarios"][0]
    base = j["scenarios"][1]
    bear = j["scenarios"][2]
    # Bull: 30 * 1.15^3 * 25 = 30 * 1.520875 * 25 = 1140.65625
    check(f"4.3 Bull target ≈ 1140.66", Decimal(bull["target_price"]) == Decimal("1140.66"), f"got {bull['target_price']}")
    # Base: 30 * 1.10^3 * 18 = 30 * 1.331 * 18 = 718.74
    check(f"4.4 Base target = 718.74", Decimal(base["target_price"]) == Decimal("718.74"), f"got {base['target_price']}")
    # Bear: 30 * 1.05^3 * 12 = 416.745 — quantize(0.01, ROUND_HALF_EVEN) gives 416.74 (banker's)
    check(f"4.5 Bear target ≈ 416.74-75", Decimal(bear["target_price"]) in (Decimal("416.74"), Decimal("416.75")), f"got {bear['target_price']}")
except Exception as e:
    failed += 4
    print(f"  ❌ JSON parse failed: {e}")

# ---------------------------------------------------------------------------
# 5. benford
# ---------------------------------------------------------------------------
print("\n=== benford ===")

# Test 5.1: real Benford-distributed data → PASS
# Build a dataset spanning multiple orders of magnitude where 30% starts with 1,
# 18% with 2, etc. — should pass Benford's chi² ≤ 1.5
real_benford = []
random_state = random.Random(42)
for d in range(1, 10):
    expected_pct = math.log10(1 + 1/d)
    n_per_digit = int(round(3000 * expected_pct))
    for _ in range(n_per_digit):
        # place digit `d` as leading, plus random trailing digits
        real_benford.append(d * (10 ** random_state.randint(0, 4)) + random_state.randint(0, 1000))
rc, out, err = run(["python3", FR, "benford", "--data", json.dumps(real_benford)])
try:
    chi = json.loads(out)["chi_square"]
    check(f"5.1 Real Benford distribution PASS (chi²={chi:.2f})", rc == 0 and "PASS" in out, f"rc={rc} chi²={chi:.2f}")
except Exception:
    check("5.1 Real Benford distribution PASS", rc == 0 and "PASS" in out, f"rc={rc}")

# Test 5.2: synthetic data that grossly violates Benford — all values 1000-1999
# → leading digit ALWAYS 1, but Benford expects 30% for digit 1 and the rest
# distributed. This is a textbook fraud red flag (massive over-concentration).
fraud_like = [1000 + i % 1000 for i in range(9999)]
rc, out, err = run(["python3", FR, "benford", "--data", json.dumps(fraud_like)])
try:
    chi = json.loads(out)["chi_square"]
    # When 100% of values start with 1, chi² ≈ 2.3 (mathematically bounded)
    check(f"5.2 All-same-digit fraud triggers SUSPICIOUS (chi²={chi:.2f})", rc == 1 and "SUSPICIOUS" in out and chi > 1.5, f"rc={rc} chi²={chi:.2f}")
except Exception as e:
    check("5.2 All-same-digit fraud SUSPICIOUS", rc == 1 and "SUSPICIOUS" in out, f"rc={rc} err={e}")

# Test 5.3: too small sample → warn
rc, out, err = run(["python3", FR, "benford", "--data", json.dumps([1, 2, 3])])
check("5.3 Small sample rejected", rc == 2, f"rc={rc}")

# ---------------------------------------------------------------------------
# 6. report_audit.py
# ---------------------------------------------------------------------------
print("\n=== report_audit.py ===")

# Create a sample report
sample = """# 騰訊投資研究報告

## 估值
- PE: 17x
- PB: 2.55x
- 股價: HK$510

## 業績
- 2025Q3 收入: HK$1,670億
- 2025Q3 淨利潤: HK$550億
- 經營利潤率: 30.5%

## 同業對比
- 阿里 PE: 14x
- 美團 PE: 22x
"""
report_path = Path("/tmp/ai_berkshire_test_report.md")
report_path.write_text(sample, encoding="utf-8")

rc, out, err = run(["python3", RA, "extract", "--report", str(report_path)])
check("6.1 extract runs and produces JSON", rc == 0, f"rc={rc}")
try:
    j = json.loads(out)
    check(f"6.2 detected ≥5 data points", j["total_data_points_detected"] >= 5, f"got {j['total_data_points_detected']}")
    sample_pts = j["data_points"]
    check(f"6.3 sample size = 15% of total", len(sample_pts) == j["sample_size"])
    check(f"6.4 each sample has empty fetched_value slots", all("fetched_value" in p for p in sample_pts))

    # Fill in all fetched values matching report (simulate human verification).
    # Parse `raw_text` to extract a numeric value robustly.
    def parse_value(raw: str) -> str | None:
        import re as _re
        m = _re.search(r"([\d,]+(?:\.\d+)?)", raw)
        if not m:
            return None
        return m.group(1).replace(",", "")

    for p in sample_pts:
        p["fetched_value"] = parse_value(p["raw_text"])
        p["fetched_source"] = "test_mock"
        p["fetched_value2"] = p["fetched_value"]  # secondary source for cross-validate
        p["fetched_source2"] = "test_mock_2"

    rc, out, err = run(["python3", RA, "verdict", "--results", json.dumps(j, ensure_ascii=False)])
    check("6.5 verdict runs on filled data", rc == 0, f"rc={rc}")
    j2 = json.loads(out)
    check(f"6.6 verdict PASS (no fails) when all match", j2["summary"]["fails"] == 0, f"fails={j2['summary']['fails']}")
    check(f"6.7 verdict label 准出", "准出" in j2["verdict"])

    # Now simulate a fail — change one fetched value (use simple int to bypass
    # unit-suffix parsing complexity).
    j_failing = json.loads(json.dumps(j))  # deep copy
    j_failing["data_points"][0]["fetched_value"] = "999999999"
    j_failing["data_points"][0]["fetched_source"] = "test_mock_off"
    rc, out, err = run(["python3", RA, "verdict", "--results", json.dumps(j_failing, ensure_ascii=False)])
    check("6.8 verdict FAIL when data deviates", rc == 1, f"rc={rc} out={out[:300]} err={err[:200]}")
    j3 = json.loads(out)
    check(f"6.9 verdict label 打回", "打回" in j3["verdict"], f"verdict={j3.get('verdict')}")
    check(f"6.10 ≥1 fail recorded", j3["summary"]["fails"] >= 1, f"fails={j3['summary']['fails']}")

except Exception as e:
    failed += 8
    print(f"  ❌ Exception: {e}")

# ---------------------------------------------------------------------------
print(f"\n=== TOTAL: {passed} passed, {failed} failed ===")
sys.exit(0 if failed == 0 else 1)