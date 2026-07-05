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
| **估值方法** | P/E + DCF + 安全邊距 | **P/ARR(AI 股)or P/E(傳統股)+ 流通量風險 premium** + 安全邊距 |
| **歷史財務** | 5-10 年歷史 | **0-3 年(招股書)** |
| **Catalyst 分析** | 季度業績 / 行業趨勢 | **完整 catalyst timeline + priced-in 分析 + Step 6.5 comprehensive re-scan** |
| **流通量風險** | 唔特別處理 | **MUST analyze**(MiniMax -68% 前車之鑑) |
| **對標 framework** | 同業上市公司 | **同業上市 + 同業未上市(OpenAI / Anthropic / DeepSeek)** |
| **Decision framework** | Buy / Hold / Sell | **Wait for pullback / Buy on dip / 觀望** + 具體回調價位 |

---

## 框架 9 個 Step

### Step 0 — 🔴 Industry-Specific Framework Selection(由 鱘龍科技 case 提煉,2026-07-05)

**Universal rule**:唔可以將 AI 股 framework(P/ARR + catalyst pipeline)盲目應用落非 AI 股。一個 framework fit-all 通常**會出 critical valuation error**。

**Industry-specific framework 指引**(Step 0 之前必做):

| 行業 | 估值方法 | 核心 KPIs | 特殊風險點 |
|---|---|---|---|
| **AI / Tech / 高增長**(智譜 / MiniMax)| P/ARR + 退出倍數對標 OpenAI/Anthropic/DeepSeek | ARR / token 量 / MAU / API revenue / 開源 stars | catalyst pipeline + 流通量 + 推理成本變化 |
| **傳統消費 / Luxury food**(鱘龍科技 / 高端餐飲)| **P/E + DCF + 同業 P/E 對標** | **收入 / 淨利潤 / 毛利率 / 市佔率 / 銷售渠道** | **生物資產公允價值波動** + 消費下行 + 關稅 |
| **金融 / 保險 / 銀行** | P/B + 內含價值(EV)+ ROE | AUM / 淨息差 / 不良率 / 償付能力 | 利率 + 信貸週期 + 監管 |
| **地產** | NAV + 股息率 + P/B | 土地儲備 / 銷售面積 / 淨負債率 / 銷售均價 | 政策調控 + 流動性 + 利率 |
| **生物科技 / 創新藥** | pipeline NPV + 風險調整後銷售 | clinical phase / FDA approval / peak sales estimate | clinical 失敗 + FDA 延遲 + 競爭 |
| **能源 / 資源** | P/E + 油價 / 商品價 + 儲量倍數 | 儲量 / 產量 / 邊際成本 / 商品價格 path | 商品週期 + ESG + OPEC 政策 |
| **公用事業 / 電力** | DCF + 股息率 + 監管 ROA | 裝機容量 / 利用小時 / 上網電價 / ROA | 監管 + 補貼變化 + 利率 |

**鱘龍科技 case 嘅 critical lesson**(2026-07-05):
- 嗰 case 係 **luxury food(已盈利,46% 淨利率)** — 唔係 AI 嘅虧損場景
- 我**原本**想用 AI framework(P/ARR)— 但會**完全錯**(因為已經盈利 + 業務穩定)
- 改用 **P/E + 同業對標**先至啱
- **如果用 P/ARR 落 luxury food 公司**,**會做錯估值因為認列營收 vs 訂閱收入嘅性質唔同**

**Trigger rule**:在任何 deep-dive 開始之前,**先做 industry check**(1 web_search query 就夠):
```
[公司名] + [行業關鍵詞] + 估值方法
```
例如:
- 「智譜 AI 大模型 ARR 估值方法」
- 「鱘龍科技 魚子醬 P/E 對標」
- 「銀行股 PB 估值方法」

**Anti-pattern**:對**任何行業一律用 P/E + DCF** 太 generic;對**任何 early-stage 一律用 P/ARR** 太 biased。要**行業 specific**。

詳細 case 見 `references/case-study-2026-07-鱘龍科技-06715.md`。

---

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

### Step 3.5 — 🔴 Multi-Source Fact-Table Format(由 智譜GLM 例子教訓,2026-07-05)

**Universal rule**(對所有 ipo deep-dive 都必須用):**每個關鍵事實必須表格化,列 source 1/2/3**。

**Template**(每個關鍵事實用呢個 table format):

| 數據點 | 數值 | Source 1 | Source 2 | Source 3 | Fact check 結果 |
|---|---|---|---|---|---|
| 公司全名 | XXX | link1 | link2 | link3 | ✅ 一致 / ⚠️ 衝突 |

**Fact Check 規則**:
- ✅ **一致**:3 source 都報同一個數字 → ✅ verified
- ⚠️ **衝突**:source 報唔同數字 → ⚠️ 公開 disclose,**揀高精度版本**(e.g. 36.1% 而非 35%)
- ⚠️ **單一 source**:只有 1 個 source → ⚠️ explicit 標記「需查第二 source」
- ⚠️ **估算**:冇直接 source,用計算 / 估算 → ⚠️ 標「estimated」

**鱘龍科技 fact check 啟示**(2026-07-05):
- 同一個 metric(2025 市佔率)2 source 報唔同(36.1% hket vs 35% 香港商報)→ 必須 disclose + 解釋(rounded vs precise)
- 估計總股本(163M based on H 股 10%)→ 必須 explicit 標記「估算,需查招股書」

**Anti-pattern**:寫「公司市佔率 36.1%」無 source → 報告 complete fail transparency check。

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

每次 refresh 都**必須跟足 Step 6.5**(下)嘅 comprehensive scan — incremental update 由 v1 加 1-2 個 catalyst 唔夠。

每次 refresh 必須檢查:

1. **股價 vs 之前估值**:股價升咗 / 跌咗幾多?之前嘅估值仲準唔準?
2. **Catalyst 兌現率**:預期 catalyst 實現咗幾多?修正下次 catalyst 預期
3. **對標公司變化**:OpenAI / Anthropic / DeepSeek 估值有冇變?
4. **管理層誠信 check**:有冇減持 / 內幕交易 / 重大失誤?
5. **行業趨勢**:AI / 新能源 / SaaS 等行業有冇 structural change?

Critical 警示:
- ⚠️ **Round 1 嘅 analysis 唔可以直接用 6 個月後**(可能完全 outdated)
- ⚠️ **每次 v1 → v2 必須清楚標記咩 update 咗**
- ⚠️ **如果 Round 2 完全推翻 Round 1 結論,要明確標注「結論翻轉」**
- 🔴 **唔可以做 incremental-only update** — 必須做 Step 6.5 comprehensive re-scan

### Step 6.5 — 🔴 Comprehensive Catalyst Re-Scan(對 IPO < 12 個月係 hard requirement)

**由 `2026-07-05 MiniMax v2.0 missed M3 catalyst` 嘅 failure case 提煉:**

呢個 step 嘅存在係**因為增量更新容易 miss critical events**。我嘅 MiniMax v2.0 報告完全 miss 咗 **MiniMax M3**(2026-06-01 發布)+ **智譜 GLM-5.2 開源**(2026-06-17)+ **智譜 GLM-5.1 SWE-Bench Pro 58.4**(2026 年初已發布)— 三個 major catalyst 全部都喺 v2.0 嘅 catalyst timeline 之外。

**Mandatory 動作**(每次 refresh 必須做全部):

| # | 動作 | 工具 / source |
|---|---|---|
| 1 | **過去 90 天嘅公司名 + 「發布」/「launch」/「release」** news search | `web_search` 多 query |
| 2 | **過去 90 天嘅公司名 + 「major version」** (e.g. `M3` / `GLM-5` / `V3` / `Pro` / `Ultra`) | `web_search` 多 query |
| 3 | **對手公司名 + 「對標」/「回應」/「回擊」** news search — parallel track 對手嘅 catalyst | `web_search` |
| 4 | **過去 90 天嘅 `site:[公司官網]` latest news** — 直接 source first party | `web_search` `site:` operator |
| 5 | **過去 90 天嘅 `site:[行業垂直 media, e.g. 36kr/ThePaper/Yahoo Finance]`** 深度報導 | `web_search` `site:` operator |
| 6 | **GitHub / HuggingFace releases**(如果公司有開源 model)| 官網直接 check |
| 7 | **券商研報最近 4 星期更新**(中金 / 招商 / 國信 / 東吳) | aastocks / 巨潮 |

**🔴 Major Version / 新 Model Launch Detection**:

**重大 signal keywords**(必須主動搵):
- 「發布 / launched / releases / introduces」
- 「新一代 / next-gen / major version / major update」
- 「超越 + 對標 model name」(e.g.「SWE-Bench Pro 超越 GPT-5.5」)
- 「完全開源 / open weights / fully open-source」
- 「多模態 / multimodal / 1M context」

**處理規則**:
- ✅ **新 major version 發布 = MUST-ADD catalyst**,即使影響 +20% rating 都要加
- ✅ **對手嘅對標發布 = MUST-ADD**(平行 track)
- ✅ **報告 v(n+1) 開頭必須有「v(n) → v(n+1) Audit Trail」section** — 明確列出 missed catalysts(避免下次再 miss)
- ✅ **如果新 major version launch 而 v(n) timeline 冇**,**必須明確標注「v(n) missed X catalyst」**

**Anti-pattern**:「v1 寫嗰陣係咁,我只係 update 數字,唔需要重新 scan」— **呢個係 failure pattern**。Always comprehensive re-scan。

詳細嘅具體失敗 transcript 見 `references/case-study-2026-07-MiniMax-missed-M3.md`。

### P9.🔴v2.0 missed M3 catalyst — 增量 update 嘅 failure pattern(2026-07-05 真人真事)

**事件**:MiniMax v2.0 報告寫嘅 catalyst timeline **完全 miss 咗 M3(2026-06-01 發布)+ 智譜 GLM-5.2(2026-06-17 開源)+ 智譜 GLM-5.1 SWE-Bench Pro 58.4**(2026 年初)。

**為咩會 miss**:
- 我由 v1 demo(只講 M2)做 incremental update 去 v2.0
- v2.0 catalyst timeline 只係加咗 M2.7(2026-03-18)+ 解禁壓力
- **冇做 comprehensive re-scan** — 即係冇 search「MiniMax M3」/「過去 90 天 launch」/「對手 GLM-5.2」
- **結果**:valuation 嚴重 outdated,competitor comparison 完全 outdated

**影響**:
- ❌ MiniMax M3 SWE-Bench Pro 59.0%、超越 GPT-5.5、逼近 Opus 4.7 → **估值 catalyst 完全 miss**
- ❌ 智譜 GLM-5.2 MIT 開源 → **5-way peer comparison 嘅 智譜 row outdated**
- ❌ M3 嘅 1M context + native multimodal → **護城河評估 wrong(一粒星 level 嘅分別)**

**User 嘅 fact-check catch 到呢個 critical omission**,然後做咗 v2.0 → v3.0 comprehensive update:
- ✅ v3.0 加 M3 + GLM-5.2 + GLM-5.1 + SWE-Bench Pro comparison
- ✅ v3.0 開頭有「v2.0 → v3.0 Audit Trail」明確列出 missed catalysts
- ✅ v3.0 結論不變(🔴 不買,等 HK$100-150)— 但護城河 ★★★★(升一級)

**教訓**:**任何 refresh 都必須做 comprehensive re-scan**,即使看似 incremental。**MiniMax v2.0 missed M3 嘅 failure 同 v3.0 嘅 audit trail** 就係呢個 rule 嘅實證。

完整 transcript + 驗證見 `references/case-study-2026-07-MiniMax-missed-M3.md`。

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

### Step 9.5 — 🔴 Fact Check Self-Audit(由 智譜/MiniMax/鱘龍科技 3 個 case 提煉,2026-07-05)

**寫報告完成前必須做嘅 self-audit**:

#### Audit 1:未 verify 嘅關鍵數據 explicit 列出

```markdown
| 結論類型 | 基於 | 信心度 |
|---|---|---|
| 公司基本資料 | 3+ source verified | 高 |
| 2025 營收 / 利潤 | financial_rigor cross-validate PASS | 高 |
| **毛利率 / 經營現金流** | **未 verify,需查招股書** | **低** |
| 估值倍數(P/E)| 估算,基於估算總股本 | **低** |
```

#### Audit 2:估算 vs verified 必須 explicit 分類

- **verified**(✅):有任何 2 個獨立 source confirm
- **estimate**(⚠️):基於計算但無 direct source
- **unverified**(❌):連估算都做唔到,只是 awaiting IPO prospectus deep dive

**Anti-pattern**:把估算當 verified 寫。

#### Audit 3:同一 metric 多 source 嘅差異 explicit disclose

如果 2 source 報唔同,例如:
- hket: 市佔率 **36.1%**(precise)
- 香港商報: 市佔率 **35%**(rounded)

必須喺報告入面寫:
```
2025 市佔率:36.1%(hket precise)vs 35%(香港商報 rounded)— 採用 36.1% 為主
```

#### Audit 4:CEO / 創辦人 attribution fact-check

每一個 attributed quote 必須 verify 公司 + 角色:
- Sam Altman = **OpenAI CEO**(closed-source),**唔係 Meta Llama**
- Mark Zuckerberg + Yann LeCun = Meta 開源路線代表
- 智譜 CEO = **張鵬**(清華系),**唔係「對標 Meta Llama 嘅 Sam Altman」**

#### Audit 5:`report_audit.py` 嘅 verdict tool raw_text strict 比較

`fetched_value` 必須 strip currency prefix + 逗號 + 百分號:

```
❌ "HK$2,418"        vs "2418"       ← verdict FAIL
✅ "HK$2,418"        vs "2418"        + 提供原始 + 純數字兩個欄位
```

完整 audit template 見 `references/case-study-2026-07-鱘龍科技-06715.md` §Fact Check Self-Audit。

**Step 9.5 嘅存在原因**:智譜/MiniMax/鱘龍科技 3 份 report 嘅 fact check 失敗(由 user fact-check 揭露)— 由 0% 全 verify 到 100% PASS tool verdict 嘅漸進改善過程。如果新一個 session 直接做 IPO research,**必須**跟 Step 9.5 嘅 audit rule。

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

## Pitfalls — 2026-07 Real-World 教訓(from 智譜 GLM + MiniMax deep-dive)

呢啲都係 2026 年 7 月做嘅 2 個真實 deep-dive **實際遇到** 嘅 pitfall,下一個 session 必須避開:

### P1.**認列營收 ≠ ARR**(致命估值錯誤)

| 指標 | 智譜 2025 真實數字 | 用佢做 P/ARR 倍數嘅結果 |
|---|---|---|
| 認列營收(GAAP)| RMB 7.24 億 | ÷ 7.24 → **148 倍 P/S**(離譜)|
| **API ARR**(2026-03, Q1 only)| **RMB 17 億** | ÷ 17 → **57 倍 P/ARR**(合理)|
| **總 ARR 估算**(API + Coding + 私有化)| **RMB 25-35 億** | ÷ 30 → **30-40x P/ARR**(對標範圍)|

**教訓**:**估值必須查最近披露嘅 ARR**,絕對唔可以用認列營收做 P/ARR 倍數嘅分母。

### P2.**`.financial_rigor.py` 嘅單位陷阱:億 vs M vs B**

**詳細見 `~/.hermes/skills/finance/financial-data/SKILL.md` §Unit Trap**。本 skill-specific 嘅兩種失敗模式:

| 失敗 | 數字 | 原因 |
|---|---|---|
| 智譜 IPO HK$41.7 億(預期淨額)vs gross HK$43.5 億 | 4.18% diff | **混淆 gross vs net proceeds**(兩個都對,唔可以 mix)|
| MiniMax 2026-06-25 HK$456.6 × 313M 股 = HK$1,432 億 | ✅ PASS | 但 source 報嘅係 HK$1,432 億,**唔係 free float 嘅 520 億** |

**教訓**:**每次驗算前必須 clarify「呢個係 total / free float / gross / net」**,然後再對號入座。

### P3.**`.report_audit.py verdict` 嘅 raw_text 嚴格字串比對**

即使數值完全一樣,以下 raw_text / fetched_value 對會 verdict FAIL:

```
"HK$2,418"        vs "2418"      ← 前者有 "HK$" + ","
"US$300"          vs "300"       ← 前者有 "US$"
"57%"             vs "57"        ← 前者有 "%"
"0.03%"           vs "0.03"      ← 前者有 "%"
```

**應對**:**填 `fetched_value` 時必須 strip currency prefix + 逗號 + 百分號**。如果報告 raw_text 必須保留嗰啲字符,**同時填多個欄位**:`fetched_value_raw` (= 同 raw_text) + `fetched_value_num` (= 純數字)。完整案例見 `references/case-study-2026-07-智譜GLM.md` §報告抽檢。

### P4.**4 大師 quotes 容易誤導讀者為真實 quote**

我喺 demo report 寫過:
```
> **巴菲特**:「呢盤生意嘅護城河我睇得到⋯」
```
讀者可能誤以為真實 quote。**必須加 disclaimer**:

```markdown
> ⚠️ **Disclaimer**: 以下「巴菲特 / 芒格 / 段永平 / 李錄」嘅引言係
> **AI 模擬嘅「佢哋可能會點講」風格點評**,**唔係真實 quote**。
> 四位大師本人從未對呢間公司發表過公開言論。如要做真實 quote,
> 必須查 4 位嘅公開訪問、年報、寫作。
```

**教訓**:**任何 4-master framework 嘅 output,都必須係引言段加呢段 disclaimer**(其他 3 個 master quotes skills 都應該 echo 呢個 pattern)。

### P5.**MiniMax 「-68%」vs「-70.2%」嘅 anchor 效應**

我之前 demo 寫嘅係「-68%」基於 HK$1,330 → HK$427。但實際最新數字係:
- **HK$1,330 → HK$396(2026-07-04) = -70.2%**
- 仲衰過我 demo 寫嘅 -68%

**教訓**:**任何 drawn-down 計算都用最新一日 close,而非「典型 / 預估」數字**。

### P6.**Profitability framework 既 net loss vs adjusted loss**

| 指標 | 智譜 | MiniMax |
|---|---|---|
| 認列淨虧損(GAAP)| RMB 47.18 億 | US$XXX(未見)|
| **經調整淨虧損(Non-GAAP)**| **RMB 31.82 億** | **US$250.9M** |
| 用呢個做 ÷ cash → runway | 2.5 年(2025-09 估算)| 5.7 年(2025-09 估算)|

**教訓**:**runway 計採用經調整淨虧損(Non-GAAP)做分母**。但同時報埋 GAAP 虧損做 reference。

### P7.**創辦人 / CEO attribution 易混淆**

我之前 demo 寫過:
> 「決策風格:技術深度型 + 開源信仰派(對標 Meta Llama 嘅 Sam Altman)」

**Sam Altman = OpenAI CEO**,OpenAI 係 **closed-source**,從來唔係「對標 Meta Llama 嘅開源路線」。Meta Llama 嘅代表人物係 **Mark Zuckerberg + Yann LeCun**,OpenAI 同 Meta 係 AI 開源/閉源嘅兩極。

**教訓**:**任何 CEO attribution 寫之前,fact-check 至少 2 個 source**(Wikipedia + 公司官網 + 招股書)。

### P8.**v1 → v2 refresh嘅 systematic trigger**

唔係每次都要做 full refresh(v1 → v2 重做所有 9 step),**輕量級 trigger** 包括:

| Trigger | 動作 | Token cost |
|---|---|---|
| **股價變化 ±20% from v1 baseline** | 重做 module 7(估值)| ~3k |
| **新 catalyst(IPO 後新嘅 material event)**| 加到 timeline(無需重做) | ~1k |
| **對標公司估值變化(OpenAI / Anthropic / DeepSeek)**| 重做 module 4 + 7 | ~5k |
| **行內 structural change**(出口管制 / 大模型新法)| 重做 module 6 + 8 | ~5k |
| **季度業績出爐** | 重做 module 1 + 3 + 7 | ~10k |
| **超過 6 個月無 refresh** | **FULL v1 → v2.0 reset + Step 6.5 comprehensive re-scan** | ~40k |

**重要**:任何「輕量 trigger」(股價 / 新 catalyst / 對標 / 行業)即使看似 incremental,都**必須**跟 Step 6.5 comprehensive re-scan rule(see Step 6.5)— incremental-only 更新係 MiniMax v2.0 missed M3 嘅失敗 pattern。

**工具**:`scripts/check-v2-refresh.py` 自動偵測 trigger(輸入 v1 baseline data)。

---

## Support Files

本 skill 嘅深入細節喺以下 files:

| File | 用途 |
|---|---|
| `references/case-study-2026-07-智譜GLM.md` | 智譜 GLM 完整 v1 → v2 case study,含具體驗算失敗 / 修正 |
| `references/case-study-2026-07-MiniMax.md` | MiniMax v2.0 case study,展示流通量風險 -70% 真實 outcome |
| `references/case-study-2026-07-MiniMax-missed-M3.md` | **🔴 MiniMax v2.0 missed M3 catalyst 嘅 failure transcript** — Step 6.5 嘅存在原因 |
| `references/case-study-2026-07-鱘龍科技-06715.md` | **🔴 鱘龍科技 case — non-AI industry test,啟發 Step 0 + 1.5 + 9.5 三個 critical skill section**(Industry-specific framework + Multi-source fact table + Fact check self-audit) |
| `templates/ipo-deep-dive-template.md` | 起始 template(copy + modify) |
| `scripts/check-v2-refresh.py` | 自動偵測 v1 → v2 refresh trigger |
| `scripts/fetch-financial-data.py` | 程序化 web search + financial_rigor wrapper |

**主 SKILL.md 係 framework + pitfalls**,**references/ 係具體 case study details**(唔重複 SKILL.md 內容),**templates/ 同 scripts/ 係 reusable artifacts**。

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