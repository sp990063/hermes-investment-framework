# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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