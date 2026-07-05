# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`ipo-catalyst-analysis` skill** — specialised framework for newly-listed (< 12 months) + catalyst-driven + low free float IPO stocks. Based on `investment-research` but adds: catalyst timeline analysis, P/ARR three-scenario valuation, free float risk premium, 5-way peer comparison, v1 → v2.0 correction pattern. See `skills/ipo-catalyst-analysis/SKILL.md` for full spec.
- **`examples/reports/2026-07-05-MiniMax-deep-dive-v3.md`** — real-world case study for `ipo-catalyst-analysis` skill. Demonstrates M3 catalyst correction (v2.0 missed M3 launch 2026-06-01, v3.0 added) and proposed skill improvements (Step 2.5 Comprehensive News Scan, Step 6.5 Major Version Detection, Step 7.5 Competitor Parallel Tracking, Step 9.5 Audit Trail).

### Fixed
- Example report (`examples/reports/2026-07-05-智譜GLM投資研究報告.md`) fact check:
  - Line 195: Sam Altman → Mark Zuckerberg / Yann LeCun (Meta Llama team, not OpenAI CEO)
  - Lines 348-356: Added "AI 模擬" disclaimer to investment master quotes (Buffett / Munger / Duan / Li Lu quotes are AI-simulated perspectives, not real attributions)

### Skill v1.2 Improvements (applied based on 鱘龍科技 case)
- **Step 0 — Industry-Specific Framework Selection** — added critical rule: don't apply AI framework (P/ARR + catalyst) blindly to non-AI stocks. Different industries need different valuation methods:
  - AI/Tech (loss-making): P/ARR + OpenAI/Anthropic comparables
  - Consumer/Food (profitable): P/E + DCF + comparable P/E
  - Financial/Insurance: P/B + embedded value + ROE
  - Real Estate: NAV + P/B
  - Biotech: pipeline NPV + risk-adjusted sales
- **Step 3.5 — Multi-Source Fact-Table Format** — every key fact must be tabulated with 3 sources; explicit ⚠️ markers for single-source / estimated / conflicting data
- **Step 6.5 — Comprehensive Catalyst Re-Scan** — for IPO < 12 months, every refresh must do a fresh news scan (not incremental update); model major version changes must be flagged within 24 hours
- **Step 9.5 — Fact Check Self-Audit** — 5 audit rules before publishing:
  1. List unverified critical data explicitly
  2. Estimated vs verified explicit classification
  3. Disclose same-metric multi-source differences
  4. Verify CEO/founder attribution
  5. Strip currency/commas from report_audit.py verdict

### `financial_rigor.py` v1.2 Improvements
- **`three-scenario-pe`** — new command for profitable companies (P/E-based). Use instead of `three-scenario` for consumer / financial / traditional industries
- **`three-scenario-pb`** — new command for financial companies (P/B-based). Use for banks / insurers / brokers
- Both reject loss-making inputs (EPS ≤ 0 for PE, BVPS ≤ 0 for PB) with helpful error messages
- Tagged `use_case` field in JSON output to clarify when to use each command
- Tests expanded: 31 → 44 (added 13 new test cases for PE/PB scenarios)

## [1.0.0] - 2026-07-05

### Added
- **19 skills** ported from [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire):
  - Tier 1 (core): `investment-research`, `investment-team`, `private-company-research`, `management-deep-dive`
  - Tier 2 (earnings/operations): `earnings-review`, `earnings-team`, `portfolio-review`, `thesis-tracker`, `thesis-drift`
  - Tier 3 (industry/screening): `industry-research`, `industry-funnel`, `quality-screen`, `bottleneck-hunter`
  - Tier 4 (workflow/base): `deep-company-series`, `investment-checklist`, `news-pulse`, `wechat-article`, `dyp-ask`, `financial-data`
- **2 Python tools** in `tools/financial/`:
  - `financial_rigor.py` — programmatic financial verification (5 commands: verify-market-cap, verify-valuation, cross-validate, three-scenario, benford)
  - `report_audit.py` — report data sampling & verdict (15% sample, 1% tolerance)
- **31 unit tests** in `tools/financial/tests/` (all passing)
- **Documentation**:
  - `README.md` — install + usage + structure
  - `docs/hermes-adapter-notes.md` — Claude Code → Hermes migration log
  - `docs/token-cost-guide.md` — per-skill token cost tiers
- **Example report**:
  - `examples/reports/2026-07-05-智譜GLM投資研究報告.md` — full 7-module report on 智譜 (02513.HK)

### Adapted for Hermes
- `delegate_task` 3-concurrent limit → 3+1 split (3 parallel perspectives + 1 sequential synthesis)
- On-demand `skill_view` loading
- Bilingual (Traditional Chinese + English) per user preference
- `cronjob` integration examples for scheduled thesis monitoring

### Verified
- ✅ 31/31 unit tests passing
- ✅ Market cap cross-validation against IPO disclosures (0.069% diff on 智譜)
- ✅ Three-scenario P/ARR valuation (loss-making AI company case)

[Unreleased]: https://github.com/sp990063/hermes-investment-framework/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/sp990063/hermes-investment-framework/releases/tag/v1.0.0