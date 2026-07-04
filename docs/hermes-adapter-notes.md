# Hermes Adapter Notes

Detailed log of adaptations made when porting [ai-berkshire](https://github.com/xbtlin/ai-berkshire) from Claude Code to Hermes Agent.

## 1. Parallel agent limit

**Claude Code**: `TeamCreate` + unlimited `Task` agents in parallel (typical 4-master team = 4 agents).

**Hermes**: `delegate_task` capped at **3 concurrent children** per parent (config: `delegation.max_concurrent_children`). Also `max_spawn_depth=1` by default (no nesting).

### Adaptation: 3+1 split
The 4-master team is dispatched as **3 parallel + 1 sequential**:

```
Round 1 (parallel, 3 subagents):
  - 段永平視角 (business + people)
  - 巴菲特視角 (financials + valuation)
  - 芒格+李錄視角 (risk + civilizational trends)

Round 2 (sequential, 1 subagent):
  - Synthesis agent: integrate 3 perspectives + run mirror test + produce final memo
```

**Trade-off**: Synthesis quality is slightly lower than a fully parallel 4-agent model because the synthesis agent only sees condensed summaries of each perspective, not the full research context. In practice this is fine because:
- Each perspective subagent already follows the same 4-master framework
- The synthesis agent's job is *integration*, not *new research*
- Token cost is ~40% lower than a true 4-agent model

## 2. Skill discovery

**Claude Code**: `Skill` tool auto-discovers skills from `.claude/skills/` and `~/.claude/skills/`.

**Hermes**: `skill_view(name=...)` for explicit loading. `skills_list()` for discovery.

### Adaptation
Each `SKILL.md` retains the standard YAML frontmatter format. Users invoke skills by name in natural language — Hermes' router matches the description field.

## 3. Slash commands

**Claude Code**: `.claude/commands/research.md` becomes `/research`.

**Hermes**: Same pattern via Hermes' `/slash-commands` mechanism. The skill loader handles the mapping.

### Adaptation
No changes needed — Hermes reads the same `.md` files in the skills directory.

## 4. File I/O

**Claude Code**: `Read` / `Write` / `Edit` tools.

**Hermes**: `read_file` / `write_file` / `patch`.

### Adaptation
All skill instructions use Hermes tool names. The `patch` tool is preferred over sed/awk.

## 5. Python tool integration

**Claude Code**: Skills can directly run Python via `Bash`.

**Hermes**: Skills reference `~/.hermes/scripts/` tools. The `tools/` directory in this repo is the source-of-truth copy; users copy or symlink to `~/.hermes/scripts/financial/`.

### Tool output convention
All financial tools follow: `stdout=JSON, stderr=human`. This allows both piping to other tools and direct human viewing.

## 6. Test framework

**Claude Code**: Tests typically use pytest with project-local fixtures.

**Hermes**: Same — `~/.hermes/scripts/financial/tests/test_financial_rigor.py` uses pytest conventions. 31/31 tests passing at time of port.

## 7. Token cost considerations

Hermes' `delegate_task` dispatches full subagent contexts, so parallel fan-outs consume tokens aggressively. **Cost-aware workflow**:

| Phase | Recommended skill |
|---|---|
| 1. Initial screen | `quality-screen` (light) |
| 2. Sector overview | `industry-research` (medium) |
| 3. Deep-dive | `investment-research` (sequential) OR `investment-team` (parallel) |

Don't jump straight to `investment-team` without screening first.

## 8. Cron / scheduled analysis

**Claude Code**: Manual invocation.

**Hermes**: `cronjob` tool for scheduled research runs (e.g. weekly thesis-drift check, daily news-pulse).

### Example use case
```yaml
name: Weekly thesis-drift check
schedule: "0 9 * * 1"  # Monday 9am
prompt: "Run thesis-tracker on all positions in ~/portfolio.md. Flag any positions with >15% drift."
skills: [thesis-tracker, news-pulse]
deliver: telegram
```

## 9. Memory

**Claude Code**: `CLAUDE.md` files in project root.

**Hermes**: `~/.hermes/memory/` for persistent facts.

### Adaptation
Important user preferences (e.g. "user prefers concise responses", "user language = Traditional Chinese") are saved to memory, not duplicated in skill files.

## 10. Multi-language support

**Claude Code**: Skills are typically English.

**Hermes**: Built-in multi-language. All skills in this port are **bilingual** (Traditional Chinese + English) to match the original ai-berkshire conventions + user preference.

---

## Summary

The port preserves the **methodology** of the original (4-master synthesis framework) while adapting to Hermes' **architectural constraints** (3-concurrent limit, on-demand skill loading, cron integration). The end result is a **lighter, cheaper, more modular** framework that still produces research reports of comparable quality to the Claude Code original.