# Hermes Investment Framework

> **A 4-master investment research framework (Buffett / Munger / Duan Yongping / Li Lu) ported to [Hermes Agent](https://github.com/nousresearch/hermes-agent).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hermes Skills](https://img.shields.io/badge/Hermes-skills-blue)](https://hermes-agent.nousresearch.com/docs)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## What is this?

This is a **Hermes-native port** of [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire), an investment-research framework that synthesizes four legendary investor methodologies:

| Master | Methodology focus |
|---|---|
| **Warren Buffett** | Moats, management quality, intrinsic value & margin of safety |
| **Charlie Munger** | Inversion thinking ("how can this fail?"), multidisciplinary models |
| **段永平 (Duan Yongping)** | "Right business + right people + right price" — consumer + founder mindset |
| **李錄 (Li Lu)** | Civilizational paradigm shifts, 10-year certainty, secular trends |

The original framework runs on Claude Code Agent Teams. This port adapts it to **Hermes Agent's `delegate_task` + `skill_view` architecture**.

---

## What's included

### 📚 20 Skills (in `skills/`)
Organised by use case:

**Tier 1 — Core research (5 skills)**
- `investment-research` — single-company sequential deep-dive (7-module framework)
- `investment-team` — multi-perspective team analysis (parallel subagents)
- **`ipo-catalyst-analysis` — IPO < 12 月 + catalyst-driven + 流通量低嘅 specialised framework**
- `private-company-research` — pre-IPO / non-listed companies
- `management-deep-dive` — CEO/founder quality assessment

**Tier 2 — Earnings & operations (4 skills)**
- `earnings-review` — quarterly results analysis
- `earnings-team` — earnings call multi-agent review
- `portfolio-review` — portfolio health check
- `thesis-tracker` / `thesis-drift` — investment thesis lifecycle

**Tier 3 — Industry & screening (4 skills)**
- `industry-research` / `industry-funnel` — sector mapping
- `quality-screen` — multi-factor stock screen
- `bottleneck-hunter` — supply-chain bottleneck analysis

**Tier 4 — Workflow & base (5 skills)**
- `deep-company-series` — continuous research on a single company
- `investment-checklist` — pre-investment decision checklist
- `news-pulse` — real-time market intelligence
- `wechat-article` — Chinese-language article summarisation
- `dyp-ask` / `financial-data` — base data utilities

### 🛠️ 2 Python tools (in `tools/financial/`)
- `financial_rigor.py` — programmatic financial verification (market cap, valuation, cross-validation, 3-scenario valuation, Benford's law)
- `report_audit.py` — report data sampling & verdict (15% sample, 1% tolerance)
- `tests/` — 31 unit tests for the financial tools

### 📖 Documentation (in `docs/`)
- `hermes-adapter-notes.md` — Hermes vs Claude Code differences
- `token-cost-guide.md` — token usage guidance per skill

### 📊 Examples (in `examples/`)
- Sample report from a real research run on 智譜 GLM (02513.HK)

---

## Installation

### Prerequisites
- [Hermes Agent](https://github.com/nousresearch/hermes-agent) installed
- Python 3.11+ (Hermes' default)

### 1. Clone the repo
```bash
git clone https://github.com/sp990063/hermes-investment-framework.git
cd hermes-investment-framework
```

### 2. Install skills
```bash
# Copy skills to your Hermes skills directory
cp -r skills/* ~/.hermes/skills/finance/

# Or symlink (recommended for development)
ln -s $(pwd)/skills/* ~/.hermes/skills/finance/
```

### 3. Install Python tools
```bash
# Either install as-is
mkdir -p ~/.hermes/scripts/financial
cp tools/financial/*.py ~/.hermes/scripts/financial/
chmod +x ~/.hermes/scripts/financial/*.py

# Or symlink
ln -s $(pwd)/tools/financial/financial_rigor.py ~/.hermes/scripts/financial/financial_rigor.py
ln -s $(pwd)/tools/financial/report_audit.py ~/.hermes/scripts/financial/report_audit.py
```

### 4. Verify installation
```bash
# Run the test suite
python3 tools/financial/tests/test_financial_rigor.py

# Check skills are loadable
hermes skill list | grep finance
```

You should see **31/31 tests pass** and **19 finance skills** listed.

---

## Quick start

### Single-company deep-dive (sequential)
```
User: "research 智譜 GLM (02513.HK)"
```
Hermes triggers the `investment-research` skill — a 7-module sequential framework:
1. **Data collection** — financials + 2-source cross-validation
2. **Business essence** — Duan Yongping's "right business"
3. **Moats** — Buffett's 5 moat types
4. **Inversion thinking** — Munger's failure paths
5. **Management** — Duan + Buffett founder assessment
6. **Civilizational trends** — Li Lu's 10-year framing
7. **Valuation & margin of safety** — 3-scenario P/ARR or P/E

### Multi-perspective team (parallel)
```
User: "use investment-team to analyse 智譜 vs MiniMax"
```
Hermes triggers `investment-team` skill — dispatches 3+ parallel subagents
(段永平 / 巴菲特 / 芒格+李錄), then synthesises a final decision memo.

⚠️ **Note**: Hermes `delegate_task` is capped at **3 concurrent children**.
The Claude Code original supports 4+. See `docs/hermes-adapter-notes.md`
for the adaptation strategy (3+1 split).

### Quick screening
```
User: "screen HK AI stocks for quality + reasonable valuation"
```
Hermes triggers `quality-screen` skill — light-weight multi-factor screen
**before** committing to the expensive `investment-research` workflow.

---

## Token cost guide

Different skills have different token footprints. **Always start with the
lightest skill and only escalate if warranted.**

| Skill | Token cost (typical) | When to use |
|---|---|---|
| `quality-screen` | ~5k | Initial screening |
| `news-pulse` | ~3k | Real-time monitoring |
| `thesis-tracker` | ~2k | Tracking existing thesis |
| `investment-checklist` | ~5k | Pre-investment validation |
| `industry-research` | ~10k | Sector overview |
| `management-deep-dive` | ~15k | Founder quality focus |
| `earnings-review` | ~15k | Quarterly analysis |
| `investment-research` | ~30-50k | Deep-dive single company |
| `investment-team` | ~50-100k | Multi-perspective team |

> **Workflow**: `quality-screen` → `industry-research` → `investment-research` (or `investment-team`)
> **Don't** jump straight to `investment-team` without screening first.

---

## Hermes vs Claude Code adaptations

This port adapts the original Claude Code framework to Hermes:

| Claude Code | Hermes | Reason |
|---|---|---|
| `TeamCreate` + 4 parallel `Task` agents | `delegate_task` with 3 parallel + 1 sequential | Hermes `delegate_task` capped at 3 concurrent |
| `Skill` tool with auto-discovery | `skill_view` tool + manual load | Hermes uses on-demand loading |
| Slash commands (`.claude/commands/`) | Hermes `/slash-commands` + skills | Same UX, different mechanism |
| `Read` / `Write` tools for reports | `read_file` / `write_file` | Compatible |

See [`docs/hermes-adapter-notes.md`](docs/hermes-adapter-notes.md) for the
full adaptation log.

---

## Real-world example

See [`examples/reports/2026-07-05-智譜GLM投資研究報告.md`](examples/reports/2026-07-05-智譜GLM投資研究報告.md)
for a complete 7-module research report on 智譜 (02513.HK) including:
- 段永平 business essence analysis
- Buffett 5-moat verification
- Munger 5 failure-path scenarios
- Li Lu civilizational trend positioning
- 3-scenario P/ARR valuation table

---

## Repository structure

```
hermes-investment-framework/
├── README.md                  ← you are here
├── LICENSE                    ← MIT
├── .gitignore
├── skills/                    ← 19 Hermes skills (SKILL.md format)
│   ├── investment-research/
│   ├── investment-team/
│   └── ...
├── tools/
│   └── financial/
│       ├── financial_rigor.py
│       ├── report_audit.py
│       └── tests/
│           └── test_financial_rigor.py
├── examples/
│   └── reports/
│       └── 2026-07-05-智譜GLM投資研究報告.md
└── docs/
    ├── hermes-adapter-notes.md
    └── token-cost-guide.md
```

---

## Contributing

PRs welcome! Especially:
- New skills (e.g. ESG analysis, options strategies)
- New language support (Japanese, Korean)
- New data source integrations
- Bug fixes in financial tools
- Additional example reports

---

## Disclaimer

⚠️ **Educational and research purposes only. Not investment advice.**

Past performance does not guarantee future results. All financial data sourced from
public filings (招股書, annual reports) and major financial news outlets. Always
do your own due diligence. AI analysis has known limitations — see each report's
"AI 研究局限性聲明" section.

---

## Credits

- **Original framework**: [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) (MIT)
- **Hermes port**: [sp990063](https://github.com/sp990063)
- **Hermes Agent**: [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent)

---

## License

MIT — see [LICENSE](LICENSE).

---

**Built with ❤️ for value investors using AI agents**