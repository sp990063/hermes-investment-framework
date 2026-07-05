# P/E Hallucination Discrepancy Report — 2026-07-05

> **Trigger**: 用戶問「其他股票的PE是否正確?」觸發全 5 隻中概股 Yahoo Finance 即時 Valuation Measures table fact-check
> **結果**: **全部 5 隻 P/E 估算 100% 錯**(除百度 79.28x 已修正 + Lenovo 19.53x 接近)
> **教訓**: 之前嘅 stock price fact-check rule(Audit 6)雖然有寫,但**從未 fact-check P/E metric**,直接導致全部估值結論錯晒

---

## 🚨 慘痛數據

### 5 隻中概股真實估值 vs 我嘅估算

| 股票 | Code | 真實股價 | 真實 Trailing P/E | 真實 Forward P/E | 我估算嘅股價 | 我估算嘅 P/E | 結論反轉? |
|---|---|---|---|---|---|---|---|
| **騰訊** | 00700.HK | **HK$431.20** | **15.48x** | 12.32x | HK$580 ❌ | 23.39x ❌ | ✅ **YES**(deep value 而非合理)|
| **小米** | 01810.HK | **HK$22.96** | **12.76x** | 14.93x | HK$21.64 ⚠️ | 9.41x ❌ | ✅ **YES**(合理而非 deep value)|
| **百度** | 09888.HK | HK$110.90 ✅ | **79.28x** | 24.63x | HK$110.90 ✅ | 79.28x ✅ | ✅ **已修正**(偏高)|
| **阿里** | 09988.HK | **HK$94.10** | **14.83x** | 15.20x | HK$117 ❌ | 5.87x ❌ | ✅ **YES**(接近 deep value 而非超平)|
| **Lenovo** | 00992.HK | HK$21.30 ✅ | **19.53x** | 15.53x | HK$21.30 ✅ | 19.63x ⚠️ | ⚠️ 接近啱 |

### 完整結論反轉表

| 股票 | 我之前嘅結論 | Yahoo 真實結論 | 修正 |
|---|---|---|---|
| **騰訊 0700** | 🟢 合理(P/E 23.39x)| 🟢 **deep value + AI + 王者遊戲(Trailing 15.48x)** | **真正買入首選!** |
| **小米 1810** | 🟢 **deep value**(P/E 9.41x)| 🟡 合理(Trailing 12.76x)| 已消化升幅,等回調 |
| **阿里 9988** | 🟢 **deep value**(P/E 5.87x)| 🟢 接近 deep value(Trailing 14.83x)| OK,Qwen + 雲增長 catalyst |
| **百度 9888** | 🟢 deep value → 🟡 偏高 | 🟡 偏高(GAAP TTM 79.28x)| 已修正 |
| **Lenovo 0992** | 🟡 略貴(P/E 19.63x)| 🟡 略貴(P/E 19.53x)| ✅ 接近啱 |

---

## 🔍 Root Cause 分析

### 1. **P/E 從未 fact-check**

之前 skill 嘅 Step 9.5 雖然有 **Audit 6(Stock Price Fact-Check)**,但**從未將 P/E metric 列入 mandatory fact-check**。我寫報告時直接用:
- 我自己估算嘅 EPS(annualized 季度 EPS × 4)— **錯晒** for Baidu 等 GAAP-loss 公司
- 或者用 Investing.com SERP snippet 嘅 P/E — **嚴重過時**

### 2. **GAAP vs Non-GAAP EPS 混亂**

百度 case 教訓最清楚:
- Q1 2026 Non-GAAP EPS RMB 18.55 → 我用 × 4 = RMB 74 annualized
- 但 GAAP TTM EPS = -US$0.12(仍虧損)
- 結果 P/E 估算 5.49x vs 真實 79.28x — **錯 14.4x**

### 3. **騰訊股價錯(580 → 431.20)**

之前嘅股價 HK$580 來源唔清,**應該係**:
- 估計用 2026 H1 高位(騰訊 6 月曾試 HK$600+)
- 或 Investing.com SERP 顯示 7 月 2 日高開,被當 close

**真實 7/3 close = HK$431.20**(由 Yahoo Finance Valuation Measures table 即時 verify)

---

## 🛠️ Permanent Fix(v1.3 Skill Update)

**新增 Step 9.5 audit rules**:

### Audit 7 — 🔴 P/E (Trailing + Forward) Fact-Check (CRITICAL)

**Trigger**: 任何 deep-dive / earnings review / news pulse 報告入面**寫到「P/E 倍數」**。

**Hard requirement**:

1. **必須用 Yahoo Finance Valuation Measures table 即時 verify**(唔可以自己估算):
   ```
   https://finance.yahoo.com/quote/{code}.HK/key-statistics/
   ```
   - Trailing P/E(過去 4 季 GAAP EPS 計算)
   - Forward P/E(分析師預期未來 12 個月共識)

2. **不可以**用以下方法估算 P/E:
   - ❌ 單季 EPS × 4 = 年度化 EPS → 再除股價
   - ❌ Investing.com SERP snippet
   - ❌ Subagent 自己報嘅 P/E
   - ❌ 我自己估算嘅 EPS

3. **GAAP vs Non-GAAP 必須 explicit 標明**:
   - Yahoo Finance Trailing P/E = **GAAP TTM basis**
   - Q1 2026 Non-GAAP EPS RMB 18.55 **唔可以直接** 用 annualized 估算 P/E
   - 如要用 Non-GAAP EPS 計算,**必須 disclose** 「Non-GAAP basis」並用 Forward P/E 對比

4. **報告入面 explicit 寫**:
   ```
   Trailing P/E: 15.48x (Yahoo Finance 7/3 close)
   Forward P/E: 12.32x (Yahoo Finance 7/3 close)
   Source: https://finance.yahoo.com/quote/0700.HK/key-statistics/
   ```

### Audit 8 — 🔴 P/Sales, Market Cap, 52-Week Range Fact-Check 🆕

**Trigger**: 報告入面**寫到「P/Sales」、「市值」、「52-week high/low」**。

**Hard requirement**: 同樣必須 Yahoo Finance Valuation Measures table verify,不可估算。

---

## 📊 教訓 — 我嘅 100% P/E 估算錯誤率

| 失敗類型 | 影響 | 教訓 |
|---|---|---|
| **騰訊 P/E 高估 1.51x**(23.39 vs 15.48)| 結論由「合理」誤判為 deep value | Forward P/E 12.32x 才是 deep value |
| **小米 P/E 低估 1.36x**(9.41 vs 12.76)| 結論由「deep value」誤判為合理 | Q2 業績雖 +33%/+75% 但估值已 price in |
| **阿里 P/E 低估 2.53x**(5.87 vs 14.83)| 結論由「超 deep value」誤判為接近 deep value | 真正 PE 14.83x 合理但唔係超平 |
| **百度 P/E 低估 14.4x**(5.49 vs 79.28)| 結論由「deep value」誤判為偏高 | GAAP TTM 仍虧損 |
| **Lenovo P/E 接近啱**(19.63 vs 19.53)| ✅ 接近啱(0.5% diff)| Lenovo subagent fact-check 部分成功 |

**結論**:**5 隻入面 4 隻結論完全反轉**(騰訊、小米、阿里、百度),1 隻接近啱(Lenovo)。我之前嘅 investment 結論 **100% 不可信**。

---

## 🎯 Action Items

### 必須做

1. ✅ **Update skill v1.2 → v1.3** — 加入 Step 9.5 Audit 7 (P/E) + Audit 8 (P/Sales)
2. ✅ **寫 discrepancy report**(本文件)
3. ✅ **Update CHANGELOG v1.3**
4. ⏳ **Update 百度 v2.0 → v2.1**(已部分完成)
5. ⏳ **Re-write 騰訊 v2.0.1 → v3.0**(結論由「合理」改為「🟢 deep value」)
6. ⏳ **Re-write 小米 v4.0 → v5.0**(結論由「deep value」改為「🟡 合理」)
7. ⏳ **Re-write 阿里 v3.0 → v4.0**(結論由「deep value」改為「🟢 接近 deep value」)
8. ⏳ **Lenovo v1.0** ✅ 接近啱,無需重寫

### 永久 fix

- ✅ **任何 deep-dive 必須 query Yahoo Finance Valuation Measures table**(由 skill 強制)
- ✅ **唔可以用自己估算 P/E**
- ✅ **GAAP vs Non-GAAP 必須 explicit disclose**

---

## 📚 Lessons Learned(累積由智譜/MiniMax/鱘龍科技 → 5 隻中概股)

### 6 個 lessons(累積由 2026-07-05 全部 case 提煉)

1. **Stock price fact-check 必須 2+ sources** (由 4 隻中概股 subagent hallucination 提煉)
2. **P/E fact-check 必須 Yahoo Finance 即時 table** (由今次 P/E 100% 錯判提煉)
3. **GAAP vs Non-GAAP 必須 explicit 分開** (由百度 5.49x vs 79.28x 提煉)
4. **Industry-specific framework 必須選啱** (由鱘龍科技 P/E 框架提煉)
5. **估值結論必須由真實 P/E 推導,不可由估算推導** (由今次反轉表提煉)
6. **Final report verdict 必須用 Yahoo Finance 即時 valuation table 校驗** (新加)

### 永久 fix priority

| Priority | Fix | Status |
|---|---|---|
| 🔴 P0 | Yahoo Finance Valuation Measures table fact-check | ✅ v1.3 |
| 🔴 P0 | GAAP vs Non-GAAP explicit disclose | ✅ v1.3 |
| 🟡 P1 | Subagent delegation prompt 必加 P/E fact-check rule | 待做 |
| 🟡 P1 | Re-write 4 份 reports | 待做 |

---

**Discrepancy Report End**

> **Author**: Hermes Agent
> **Date**: 2026-07-05
> **Session ID**: Telegram DM `~`
> **Related**: skills/ipo-catalyst-analysis/SKILL.md v1.3, examples/reports/*-deep-dive-v*.md
> **Permanent**: 紀錄喺 `~/.hermes/skills/finance/reports/2026-07-05-P-E-discrepancy-report.md`