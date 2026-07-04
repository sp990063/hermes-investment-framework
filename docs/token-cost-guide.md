# Token Cost Guide

Different skills consume different amounts of context. **Always start with the lightest skill and only escalate if warranted.**

## Cost tiers

### Tier 0 — Trivial (< 3k tokens)
- `thesis-tracker` — tracking an existing investment thesis (no new research)
- `news-pulse` — real-time market headlines digest

### Tier 1 — Light (~5k tokens)
- `quality-screen` — multi-factor stock screening
- `investment-checklist` — pre-investment decision validation
- `dyp-ask` — quick Q&A on Duan Yongping methodology

### Tier 2 — Medium (~10-15k tokens)
- `industry-research` — sector overview
- `management-deep-dive` — single-founder focus
- `earnings-review` — quarterly results analysis

### Tier 3 — Heavy (~30-50k tokens)
- `investment-research` — single-company sequential deep-dive (7 modules)
- `private-company-research` — pre-IPO analysis (less data, harder)

### Tier 4 — Expensive (~50-100k+ tokens)
- `investment-team` — multi-perspective team (3-4 parallel subagents)
- `earnings-team` — multi-agent earnings call review

## Recommended workflow

```
┌─────────────────────────────────────────────────────┐
│  Step 1: quality-screen (Tier 1)                     │
│  Goal: Identify 5-10 candidates from broad universe │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Step 2: industry-research (Tier 2)                 │
│  Goal: Understand sector dynamics + competitive map │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  Step 3a: investment-research (Tier 3, sequential)  │
│       OR                                            │
│  Step 3b: investment-team (Tier 4, parallel)        │
│  Goal: Full 4-master deep-dive                      │
└─────────────────────────────────────────────────────┘
```

## When to skip tiers

- **Skip quality-screen** if user already names a specific ticker
- **Skip industry-research** if user already has sector context
- **Skip investment-team** if a single-agent research is sufficient
- **Use thesis-tracker** instead of full research for existing positions

## When to escalate

- ❌ **Don't escalate** if the lighter skill already gives a clear pass/fail signal
- ✅ **Escalate** when the answer is "needs more research" rather than "buy/pass"
- ✅ **Escalate** when stakes are high (large position size, irreversible decision)

## Specific scenario: HK IPO stocks (e.g. MiniMax, 智譜 GLM)

For a recently IPO'd stock with limited historical coverage:

| Phase | Skill | Why |
|---|---|---|
| 1 | `news-pulse` | Get latest news, sentiment |
| 2 | `quality-screen` | Multi-factor screen to assess basic quality |
| 3 | `private-company-research` | Even though listed, treat as quasi-private due to short trading history |
| 4 | `investment-team` | Full multi-perspective deep-dive |

## Cost-saving tips

1. **Cache results**: Save reports to disk (`write_file`) so subsequent queries don't re-research.
2. **Use context_from**: In cron jobs, pass prior research as context rather than re-running.
3. **Narrow scope**: Instead of "analyse the AI sector", say "compare 智譜 vs MiniMax on moats + valuation".
4. **Stop early**: If Step 1 already reveals a clear disqualifier, don't escalate.