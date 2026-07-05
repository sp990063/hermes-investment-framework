---
name: ipo-catalyst-analysis
description: 針對新上市(< 12 個月)+ catalyst-driven + 流通量低嘅 IPO 股票嘅 deep-dive framework。基於 `investment-research` 但 specialised 處理 IPO 後估值發現 + catalyst pipeline 評估 + 流通量風險 + 5-way 中國大模型對標(或其他 catalyst 對標)。當用戶話「IPO analysis」「新上市研究」「catalyst stock」「上市 6 個月內」「新經濟股 IPO」時 trigger。Use this INSTEAD of `investment-research` for newly-listed stocks with active catalyst pipeline and limited free float.
---

# IPO + Catalyst 深度分析框架 (Hermes port)

對 $ARGUMENTS(新上市 + catalyst-driven 嘅股票)進行系統化投資分析。本 skill 係 `investment-research` 嘅 **specialised extension**,專門處理以下挑戰:

1. **估值發現未完成** — IPO < 12 個月,市場仲喺度 price discovery
2. **Catalyst pipeline active** — 公司定期有 material events(GLM-5 發布 / Coding Plan 漲價 / API 漲價等)
3. **流通量低** — Free float 通常 < 60%,容易被操控 + 波動性高
4. **歷史財務有限** — 招股書最多披露 3 年,而家市場 active 嘅係 forward-looking ARR / catalyst
5. **對標 framework 不同** — 已上市公司有 P/E / EV/EBITDA 對標,IPO 早期只能用 P/ARR / 對標未上市公司(OpenAI / Anthropic / DeepSeek)

---

## 同 `investment-research` 嘅差別

| 維度 | `investment-research` | `ipo-catalyst-analysis`(本 skill) |
|---|---|---|
| **適用對象** | 任何已上市公司 | **IPO < 12 個月** + catalyst pipeline active |
| **估值方法** | P/E + DCF + 安全邊距 | **P/ARR + 流通量風險 premium** + 安全邊距 |
| **歷史財務** | 5-10 年歷史 | **0-3 年(招股書)** |
| **Catalyst 分析** | 季度業績 / 行業趨勢 | **完整 catalyst timeline + priced-in 分析** |
| **流通量風險** | 唔特別處理 | **MUST analyze**(MiniMax -68% 前車之鑑) |
| **對標 framework** | 同業上市公司 | **同業上市 + 同業未上市(OpenAI / Anthropic / DeepSeek)** |
| **Decision framework** | Buy / Hold / Sell | **Wait for pullback / Buy on dip / 觀望** + 具體回調價位 |

---

## 框架 9 個 Step

### Step 1 — 前置:AI 偏見自覺

**信息豐富度評級**:default **B+ 級**(剛 IPO)

| 等級 | 特徵 | 應對策略 |
|---|---|---|
| **A 級** | 上市 6-12 個月,有 2-3 份季度業績 | 標準 4-master framework |
| **B+ 級(默認)** | 上市 < 6 個月,有招股書 + catalyst timeline | 呢個 skill 主要服務呢類 |
| **C 級** | 上市 < 1 個月,只有招股書 | 等 1 份季度業績先再分析 |

**IPO 早期特有嘅 AI 偏見**:

- ⚠️ **敘事偏差(高)**: 新經濟股 IPO 總有「下一個 X」嘅故事(GLM 對標 Claude / OpenAI 對標 AWS)
- ⚠️ **錨定效應(高)**: 招股價 / 上市首日收盤 容易被當做 anchor,但 IPO 6 個月內股價變化可以 +200% / -70%
- ⚠️ **共識偏差(高)**: IPO 期間大量券商報導,容易 over-trust consensus
- ⚠️ **倖存者偏差(中)**: 用已成功 IPO 嘅公司對標,忽略失敗案例(Lufax / 滴滴 / 蔚來)
- ⚠️ **catalyst pricing in 偏差**: 容易高估 catalyst 嘅持續影響力,低估「好消息已 priced in」

---

### Step 2 — 🔥 Catalyst Timeline 建構(本 skill 核心特色)

**最重要嘅 step**。IPO 後嘅每個 material event 都要 timeline + 記錄股價反應。

**Template**:

| 日期 | Event 類型 | 內容 | 股價反應 | 解讀 |
|---|---|---|---|---|
| YYYY-MM-DD | IPO | 招股價 HK$X | +Y% 首日 | 初始需求強度 |
| YYYY-MM-DD | 產品發布 | 新產品 / 新版本 | ±Y% | 技術領先驗證 |
| YYYY-MM-DD | 業績 | Q1 業績 | ±Y% | 商業化進展 |
| YYYY-MM-DD | 提價 / 限售 | Pricing power | ±Y% | 品牌定價權 |
| YYYY-MM-DD | 行業事件 | 對標公司發布 | ±Y% | 相對競爭力 |

**Critical analysis**:
- **Cumulative return since IPO**: 累計升幅 vs 基本面改善
- **Catalyst concentration**: 半年內有幾多 catalyst?(智譜 6 個月內 5 個 catalyst)
- **Priced-in assessment**: 邊啲 catalyst 已經 priced in?仲有幾多 upside?

---

### Step 3 — Round 1 數據收集

**Source priority**(IPO 早期):

1. **招股書**(必讀,完整 financial + business disclosure)
2. **港交所 / SEC 上市文件**(主要股東 + 風險因素)
3. **官方新聞稿 + 業績發佈**
4. **行業 news**(catalyst 報導)
5. **券商研究報告**(小心 consensus bias)
6. **社交媒體 sentiment**(Twitter / Reddit / 雪球)

**必須 verify 嘅數據點**:
- 招股價
- 上市首日收盤
- 當前股價 + 累計升幅
- 總股本 + 流通股 + free float 比例
- IPO 募資 + 用途
- 最近 4 個季度營收 + 經調整虧損
- 任何 ARR 披露
- 任何 catalyst event + 股價反應

---

### Step 4 — 🔥 P/ARR 三情景估值(本 skill 核心特色)

**對虧損 / zero-EPS 公司**,傳統 three-scenario PE 工具無用,必須用 **P/ARR 倍數法**:

```
2026E ARR × 退出倍數 = 隱含市值
```

**退出倍數對標 framework**:

| 公司類型 | 退出倍數 | 備註 |
|---|---|---|
| **OpenAI 等級**(全棧 + 護城河深)| **25x ARR** | baseline |
| **Anthropic 等級**(頂級 + 高速增長)| **30-40x ARR** | premium tier |
| **中國開源領導者**(Meta Llama 角色)| **20-25x ARR** | 開源擠壓 premium |
| **中國中間層 specialist**(Mistral / MiniMax 角色)| **12-20x ARR** | 細規模 |
| **高度投機 / 早期** | **< 15x ARR** | 高風險 |

**範例(智譜 GLM 2026-07)**:

| 情景 | 2026E API ARR(RMB)| 退出倍數 | 隱含市值(RMB) | vs 當前 HK$1,078B |
|---|---|---|---|---|
| 極樂觀 | 3,400M(+100%) | 40x(Anthropic 等級)| ¥136B | +36% |
| 樂觀 | 2,550M(+50%) | 30x(OpenAI 等級)| ¥76.5B | -23% |
| 中性 | 1,700M(持平) | 25x(OpenAI 等級)| ¥42.5B | -57% |
| 悲觀 | 1,360M(-20%) | 20x(開源平均)| ¥27.2B | -73% |

**安全邊距評估**:
- 極度樂觀 → 0% 安全邊距(可能 overpay)
- 中性 → 大幅下行(典型估值過熱信號)

---

### Step 5 — 🔥 流通量風險 premium(本 skill 核心特色)

**Low free float 嘅 IPO 股價發現**:
- Free float < 30%:極高操控風險,**股價可以 ±30% / 日**
- Free float 30-60%:中等風險,**典型 IPO 6 個月內**
- Free float > 60%:接近 normal trading,**成熟期**

**關鍵計算**:

```
Avg daily volume × 250 trading days = annual turnover
Annual turnover / free float = turnover ratio
```

如果 turnover ratio > 2x,**流通量極低**,任何大單都可能 push 價格 ±10%。

**流通量對應嘅溢價 / 折讓**:

| 流通量水平 | 估值 adjustment |
|---|---|
| Free float < 30% | -20% to -30% 估值 discount(但短期可能 +20% premium 因為 squeeze) |
| Free float 30-50% | -10% to -20% discount |
| Free float > 60% | normal |

**前車之鑑 — MiniMax 跌幅 -68%**:
- 2025 年 6 月高位 HK$1,330
- 2026 年 7 月低位 HK$427
- **跌幅 -67.97%** = 流通量低 + 高位接刀嘅後果

---

### Step 6 — 🔥 v1 → v2.0 Correction Pattern(本 skill 核心特色)

**任何 IPO < 12 個月嘅 analysis 必須做至少 2 輪 data refresh**:

- **Round 1**: IPO 後第 1-4 個星期(基於招股書 + 早期 catalyst)
- **Round 2**: IPO 後第 2-6 個月(基於 Q1 業績 + 完整 catalyst timeline)
- **Round 3**: IPO 後第 6-12 個月(基於 Q2 業績 + valuation 修正)

**每次 refresh 必須檢查**:

1. **股價 vs 之前估值**:股價升咗 / 跌咗幾多?之前嘅估值仲準唔準?
2. **Catalyst 兌現率**:預期 catalyst 實現咗幾多?修正下次 catalyst 預期
3. **對標公司變化**:OpenAI / Anthropic / DeepSeek 估值有冇變?
4. **管理層誠信 check**:有冇減持 / 內幕交易 / 重大失誤?
5. **行業趨勢**:AI / 新能源 / SaaS 等行業有冇 structural change?

**Critical 警示**:
- ⚠️ **Round 1 嘅 analysis 唔可以直接用 6 個月後**(可能完全 outdated)
- ⚠️ **每次 v1 → v2 必須清楚標記咩 update 咗**
- ⚠️ **如果 Round 2 完全推翻 Round 1 結論,要明確標注「結論翻轉」**

---

### Step 7 — 5-way Peer Comparison(本 skill 核心特色)

**對中國 AI 大模型公司嘅對標 framework**:

| 公司 | 估值 | 2026 ARR | 開源策略 | 商業模式 | 護城河強度 |
|---|---|---|---|---|---|
| **智譜(02513.HK)** | US$138B | RMB 1.7B(Q1 API)| GLM 開源 + Coding Plan | 雙軌 | ★★★★★ |
| **月之暗面** | US$20B | US$100M+(3 月)| K2.5 開源 | API + app | ★★★ |
| **DeepSeek** | US$45B | 未公開 | V4-Pro 開源 | API + B2B | ★★★★ |
| **MiniMax** | US$38B | US$150M(2 月)| 部分開源 | API + apps | ★★★ |
| **阿里通義** | 阿里市值一部份 | 未公開 | Qwen 開源 | API + 雲 | ★★★★ |

**對其他行業嘅對標 framework**:參考以上結構,但用相應嘅同業。

---

### Step 8 — 4 大師視角分析

跟 `investment-research` 嘅 4 大師視角,但 specialisation:

#### 段永平「right business + right people + right price」
- **right business**: IPO 早期嘅 narrative 通常吸引人,但要 check 商業模式嘅 unit economics
- **right people**: Founder 通常仍喺位,但要 check IPO 後有冇 senior departures
- **right price**: **本 skill 最強調嘅 dimension** — 等候回調到合理安全邊距

#### 巴菲特「moat + management + margin of safety」
- **moat**: IPO 早期 moat 通常未經驗證,要看 catalyst 嘅 pricing power signal
- **management**: 看 catalyst execution rate(GLM 半年 5 個 catalyst = 極強)
- **margin of safety**: **必須等候 30-50% 安全邊距**,因為 IPO 6 個月內估值發現未穩定

#### 芒格「inversion + 多學科」
- **inversion**: 「高位接刀嘅後果」= MiniMax -68%,要時刻問「如果我而家買咗,3 個月後最壞情況係咩?」
- **多學科**: 結合 network effect theory + 技術採納曲線 + 競爭博弈

#### 李錄「civilizational paradigm shift + 10-year framing」
- **civilizational**: AI / 新能源 / 生物科技 屬於文明級範式轉移
- **10-year framing**: 問「10 年後呢間公司仲會喺度嗎?」如果係 → 即使短期估值高都可以考慮

---

### Step 9 — 綜合決策備忘錄 + 具體回調價位

**Decision framework**(本 skill 嘅核心 output):

| 策略 | 建議模板 |
|---|---|
| **空倉者** | **等候回調至 X-Y 才買入**(具體價格區間,對應 Nx P/ARR + 安全邊距 Z%) |
| **持倉者** | **減倉 A-B%**,等候回調再加 / 完全 hold / sell signal |
| **賣出信號** | 具體 catalyst 失敗 / 對手超越 / 行業 structural change |
| **加倉信號** | 具體回調價位 / 新 catalyst 確認 / 對標突破 |

**必須包含嘅具體內容**:

1. **合理買入區間(3 個 scenarios)**:
   - 極度保守:價格 / 倍數 / 安全邊距
   - 合理:價格 / 倍數 / 安全邊距
   - 投機性:價格 / 倍數 / 安全邊距

2. **紅線清單**(任何一條觸發 = 重新評估):
   - 股價跌穿 / 升穿關鍵位
   - 對手公司 catalyst 超越
   - 公司 catalyst 失敗
   - 行業 structural change

3. **monitoring cadence**:
   - 短期(1-4 星期):catalyst watch
   - 中期(1-3 個月):quarterly review
   - 長期(6-12 個月):re-evaluate valuation framework

---

## 報告輸出要求

**文件名格式**: `~/YYYY-MM-DD-[公司名]IPO-deep-dive.md` 或 `~/.hermes/skills/finance/reports/YYYY-MM-DD-[公司名]IPO-deep-dive.md`

**必須包含嘅 sections**:

1. **🔴 v2.0 更新重點**(如果有 v1)
2. ⚠️ AI 研究局限性聲明
3. **0. 前置:AI 研究偏見自覺**(B+ 級 by default)
4. **1. 第一步:數據收集 + Catalyst Timeline**
5. **2. 第二步:生意本質**(段永平)
6. **3. 第三步:護城河**(巴菲特)
7. **4. 第四步:逆向思考**(芒格)
8. **5. 第五步:管理層**(段永平 + 巴菲特)
9. **6. 第六步:行業與文明趨勢**(李錄)
10. **7. 第七步:估值與安全邊際**(P/ARR 三情景 + 流通量 premium)
11. **8. 第八步:綜合決策備忘錄 + 4 大師點評**
12. **9. 數據抽檢**(用 `report_audit.py extract + verdict`)
13. **10. AI 分析置信度 vs 投資確定性聲明**

---

## Token 控制建議

| Phase | Token cost | 備註 |
|---|---|---|
| **Round 1 數據收集** | ~15-20k | 招股書 + 早期 news |
| **Catalyst timeline 建構** | ~5k | critical step |
| **P/ARR 三情景 + 流通量分析** | ~5k | critical step |
| **4 大師視角** | ~15-20k | 同 `investment-research` |
| **數據抽檢** | ~3k | 15% sample |
| **總計** | **~40-55k** | 比 `investment-research` 略多 |

---

## Real-world examples

睇 `examples/reports/2026-07-05-智譜GLM-deep-dive.md` 嘅 v2.0 報告,展示呢個 framework 嘅完整 output。

---

## 同其他 skills 嘅配合

| Skill | 配合方式 |
|---|---|
| `investment-research` | 本 skill 係佢嘅 specialised extension,**唔可以並行用** |
| `quality-screen` | 用嚟做 IPO 前嘅 quality screen,**IPO 前嘅 screening** |
| `private-company-research` | 對標未上市公司(OpenAI / Anthropic)時,睇下 `private-company-research` 嘅 framework |
| `news-pulse` | 持續監察 catalyst,特別係 Round 2 / Round 3 refresh |
| `thesis-tracker` | 持倉後,用 `thesis-tracker` 持續 track thesis drift |

---

## 適用場景 checklist

**Use this skill 嘅 trigger 條件**:

- [ ] 公司 IPO < 12 個月
- [ ] 公司有 active catalyst pipeline(過去 6 個月有 ≥ 2 個 material events)
- [ ] Free float < 60%(典型 IPO 6 個月內)
- [ ] 公司係新經濟 / 高增長 / 虧損 or 微利
- [ ] User 想做 deep-dive 而非 quick screen

**Use `investment-research` 而非本 skill 嘅 trigger**:

- [ ] 公司已上市 > 12 個月
- [ ] 公司有穩定盈利 + 分紅
- [ ] Free float > 60%
- [ ] 屬於成熟行業(銀行 / 公用事業 / 必需消費)

**Use `quality-screen` 而非本 skill 嘅 trigger**:

- [ ] 只想做 quick quality screen
- [ ] 未決定做 deep-dive

---

## Pitfalls 常見錯誤

1. ⚠️ **唔可以用 v1 analysis 做 v2 decision** — IPO 6 個月內每次 refresh 都係獨立 analysis
2. ⚠️ **唔可以忽略 free float risk** — MiniMax -68% 係前車之鑑
3. ⚠️ **唔可以 over-trust catalyst** — 「好消息 priced in」係常見錯誤
4. ⚠️ **唔可以只睇單一對標** — 必須 5-way peer comparison
5. ⚠️ **唔可以 skip 流通量 premium** — 直接影響 valuation
6. ⚠️ **唔可以忽略 bearish scenarios** — IPO 6 個月內悲觀情景下行可以 -50-70%

---

## 結語

IPO + catalyst-driven 股票嘅 analysis 係 **最容易被高估嘅時段**。呢個 skill 嘅核心 philosophy 係:

> **「Right business 唔等於 right price。IPO 後嘅高估值通常 fully reflect catalyst,等候 30-50% 回調先買入係最 robust 嘅 strategy。」**