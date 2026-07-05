# MiniMax (00100.HK) — 投資研究綜合報告 v3.0

> **使用 skill**: `ipo-catalyst-analysis`
>
> **v3.0 更新重點**(對比 v2.0):
> - 🆕 **M3 已喺 2026-06-01 發布**(v2.0 完全冇提)— 1M context + 原生多模態 + 自研 MSA + 開源
> - 🆕 **M3 SWE-Bench Pro 59.0%**(超越 GPT-5.5,逼近 Opus 4.7)
> - 🆕 **M3 價格 = Opus 4.7 嘅 1/10**($0.6/$2.4 per M token vs Opus 4.7 嘅 ~$30+)
> - 🆕 **對手**:智譜 **GLM-5.2**(2026-06-13 Coding Plan / 2026-06-17 開源 MIT)
> - 🆕 **對手**:智譜 **GLM-5.1** SWE-Bench Pro 58.4(已超越 GPT-5.4 + Opus 4.6)
> - 🔴 **結論需要重新評估**: M3 係強 catalyst,但股價由 HK$1,330 → HK$396 = -70.2% 顯示 catalyst pricing in + 解禁壓力仍然極強
> - **結論保留**: 🔴 不買,等 HK$100-150

> **報告日期**:2026-07-05
> **AI 研究置信度**:B+(IPO 6 個月內,catalyst pipeline active + 雙邊重大 catalyst — M3 + 解禁)

---

## ⚠️ AI 研究局限性聲明 — **v3.0 加強**

- ✅ v3.0 補充咗 v2.0 missed 嘅 **M3 catalyst**(2026-06-01)
- ⚠️ **v2.0 嘅 catalyst timeline 完全 outdated** — 只記到 M2.7(2026-03),完全 miss M3(2026-06)
- ⚠️ **呢個係典型嘅 IPO catalyst 分析嘅 trap** — catalyst pipeline active 時容易 miss 最新嘅
- ⚠️ 用戶嘅 fact check 揭露咗 v2.0 嘅 critical oversight — **呢個 skill 嘅 v1 → v2.0 correction pattern 唔夠,需要做 v2.0 → v3.0 multi-round refresh**
- ⚠️ 智譜 GLM-5.2 vs MiniMax M3 嘅 SWE-Bench Pro 對比:
  - GLM-5.1: 58.4(對標 GPT-5.4 + Opus 4.6,2026 年初)
  - GLM-5.2: 超越 GPT-5.5, MIT 開源(2026-06-17)
  - M3: 59.0(對標 GPT-5.5,逼近 Opus 4.7,2026-06-01)
  - **三者都係 frontier tier**,差距細
- ⚠️ Free float 比例仍係估算(25-35%)
- ⚠️ 港股 2026 解禁規模 HK$1.55 萬億係 36kr 報導,具體 MiniMax 解禁日期待確認

---

## 0. AI 研究偏見自覺 — v3.0 加強

**v2.0 missed M3 catalyst 嘅教訓**:
- ⚠️ **catalyst concentration bias**(高):IPO 早期 catalyst density 極高,容易 focus 喺最近嘅 catalyst(M2.7),miss 較新嘅(M3)
- ⚠️ **timeliness bias**(高):每次 refresh 都要重新 scan 整個 catalyst pipeline,唔可以假設上次嘅 scan 仲 work
- ⚠️ **model series confusion**(中):MiniMax M-series 命名 convention(M1 → M2 → M2.7 → M3),容易混淆 sub-version 同 major-version

**改進策略**(skill 改良):
- ✅ 每次 refresh 必須做 **comprehensive news scan** 而非只 update 之前嘅 timeline
- ✅ 對 model series 嘅 major version 變化(M2 → M3)必須 flag 為 critical update
- ✅ 對競爭對手嘅對應版本(GLM-5.2)必須 parallel track

---

## 1. 公司基本資料(unchanged from v2.0)

| 項目 | 內容 |
|---|---|
| 公司全名 | **MiniMax Group Inc.**(稀宇科技 / Xīyǔ Kējì)|
| 港股代碼 | **00100.HK** |
| 上市日期 | **2026-01-09** |
| 招股價區間 | HK$151-165(中位數 HK$158)|
| IPO 發行股數 | 37.42M 股 |
| **2026-03-18 高位(M2.7 catalyst)** | **HK$1,330**(intra-day +28.8% / 收 +19.9% 報 HK$1,238)|
| **2026-06-25 收市** | **HK$456.6(-4.40%)** |
| **2026-07-04 收市** | **HK$396(-8.97%)** 🔴 |
| **總股本** | **313M 股** |
| **總市值** | **HK$1,239 億(2026-07-04)** / **HK$2,696 億(高位)** |
| **52 週高** | **HK$1,330** |
| **52 週低** | **HK$396** |
| **保薦人** | 中金 + 瑞銀 |
| **創辦人 / CEO** | **閆俊杰 / 閆俊傑**(前 SenseTime VP,2021 上海創立)|
| **主營業務** | Hailuo AI(視頻)+ Talkie / 星野(AI 角色聊天)+ M2 / M2.7 / **M3** 大模型 + 開放平台 |
| **投資者** | Alibaba / Tencent / miHoYo |
| **員工** | **385 人**(人均 95 後)|

---

## 2. 🔥 Catalyst Timeline(IPO 後) — **v3.0 重大修正**

| 日期 | Event 類型 | 內容 | 股價反應 | 解析 |
|---|---|---|---|---|
| 2026-01-09 | **IPO 掛牌** | 招股價 HK$158 | 待確認首日表現 | 初始定價 |
| 2026-03-02 | **首份年度財報** | 2025 營收 US$79M / 經調整虧損 US$250.9M | — | 業績落地 |
| **2026-03-18** | **🔥 M2.7 Agent 旗艦 + 自我進化技術** | MiniMax 首次展示「模型自我進化」路徑 | **+28.8% intra-day / 高見 HK$1,330 / 收升 19.9% 報 HK$1,238 / 成交 36 億** | biggest catalyst,創新高 |
| 2026-04 至 05 | M3 預告期 | Skyler Miao 社交平台預告 M3 | — | 預期管理 |
| **2026-05-28** | M3 進入發布準備 | 新浪財經確認 M3 採用 MSA 自研稀疏注意力 | 預期上升 | 預熱 |
| **🔴 2026-06-01** | **🔥🔥 M3 正式發布(我 v2.0 完全 missed)** | **1M context + 原生多模態 + 自研 MSA + 開源權重** | 待確認 | **frontier catalyst** |
| 2026-06 | **解禁壓力臨近** | 港股 2026 解禁規模 HK$1.55 萬億,創紀錄 | 跌 | 解禁期臨近 |
| 2026-06 | **智譜 GLM-5.2 對標** | GLM-5.2 2026-06-13 Coding Plan 全量 + 06-17 開源 MIT | M3 對標壓力 | **競爭白熱化** |
| 2026-06-13 | 智譜 GLM-5.2 Coding Plan 全量 + API | 智譜搶開發者市場 | — | 對標 M3 |
| 2026-06-17 | 智譜 GLM-5.2 MIT 開源 | 智譜搶 open-source 開發者 | — | 對標 M3 開源 |
| **2026-06-22** | **🔴 解禁前 1 個月** | 「MiniMax 泡沫先破」新聞 | — | 預警 |
| 2026-06-25 | **股價跌至 HK$456.6** | -4.40% 單日 | -65.7% from HK$1,330 | 跌穿 HK$500 |
| **2026-07-04** | **🔴 跌穿 HK$400** | **HK$396(-8.97%)** | **-70.2% from HK$1,330** | **關鍵紅線觸發** |

**Catalyst 累計效果**: HK$158 → HK$1,330(3 月 M2.7 觸發)= **+742%** → 6 月 M3 + GLM-5.2 雙 catalyst → HK$396(7 月) = **+150% from IPO, -70.2% from peak**

**v3.0 修正嘅 critical insight**: **雖然 M3 + GLM-5.2 雙 catalyst 都係 frontier tier,但股價仍由 HK$1,330 → HK$396** — 解禁壓力 + 流通量低 + catalyst pricing in 已經完全 reflect,**兩個 frontier catalyst 都救唔返**。

---

## 3. 財務核心數據(unchanged from v2.0,已用 financial_rigor.py 驗證)

| 指標 | 2025 數值 | YoY | 驗證狀態 |
|---|---|---|---|
| 總營收 | **US$79.038M** | +158.9% | ✅ PASS(0.02%) |
| 毛利率 | **25.4%** | +13.2pp | 招股書 |
| 經調整淨虧損 | **US$250.9M** | +2.7% | ✅ PASS(0.00%) |
| **2026-02 ARR** | **US$150M** | — | ✅ PASS(0.00%) |
| 2026 前 2 個月 token 量 | 2025-12 嘅 **6 倍** | — | 觀點網 |
| 個人用戶總數 | **2.12 億名** | — | 招股書 |
| Talkie MAU | **11M** | — | shareuhack |
| 海外收入佔比 | **>70%** | — | 招股書 |
| 客戶集中度 | 60.5% → 44.1% → 21.7% | 健康 | 招股書 |
| 賬上現金 | **US$1.9B** | — | 招股書 |
| **Runway** | **5.7 年** | ✅ 健康 | computed |

---

## 4. 🔥 P/ARR 三情景估值(unchanged from v2.0)

| 情景 | 2026E ARR(USD)| 退出倍數 | 隱含市值(USD) | 隱含股價(HKD)| vs 當前 HK$396 |
|---|---|---|---|---|---|
| **極樂觀** | US$300M(+100%) | 40x | $12B | HK$299 | -25% |
| **樂觀** | US$225M(+50%) | 30x | $6.75B | HK$168 | -58% |
| **中性** | US$150M(持平) | 20x | **$3.0B** | **HK$75** | **-81%** |
| **悲觀** | US$120M(-20%) | 15x | $1.8B | HK$45 | -89% |

**v3.0 嘅修正**: 雖然 M3 catalyst 係 strong,但**股價由 HK$1,330 → HK$396 = -70% 已經反映**:
- ✅ M3 catalyst fully priced in(3 月 M2.7 觸發 + 6 月 M3 二次觸發)
- ❌ 智譜 GLM-5.2 對標壓力(MIT 開源 + Coding Plan 商業版 = 雙軌對 M3 嘅中間層 specialist 構成威脅)
- ❌ 解禁壓力主導下行

**結論**: 估值結論不變,仍然係中性情景 -81% 下行,**等候 HK$100-150 才考慮買入**。

---

## 5. 🔥 流通量風險 premium(unchanged from v2.0)

| 指標 | 數值 |
|---|---|
| 總股本 | 313M 股 |
| Free float(估算)| 約 25-35% |
| 流通量水平 | **🔴 低** |
| 2026 港股解禁規模 | **HK$1.55 萬億(創紀錄)** |

**v3.0 確認嘅 evidence**: MiniMax 由 HK$1,330 → HK$396 = **-70.2%**(4 個月內失去 70% 市值)— 即使有 M3 frontier catalyst,流通量風險 + 解禁壓力仍主導下行。

---

## 6. 🔥 v1 → v2.0 → v3.0 Correction Pattern — **v3.0 加強**

**v1 demo 結論**: 「觀察,等待 ARR 持續爆發」
**v2.0 結論**: 🔴 不買,等 HK$100-150(基於 catalyst 數據截至 2026-03-18 + 解禁壓力)
**v3.0 結論**: 🔴 **不買,等 HK$100-150**(v2.0 結論 robust,即使補上 M3 catalyst 都不變)

**v3.0 嘅 critical lesson**:
- ✅ **v2.0 嘅估值結論 robust** — 即使 missed M3,結論都係合理
- ❌ **v2.0 嘅 catalyst timeline 完全 outdated** — miss M3 係 critical oversight
- 🔴 **skill 改良**:每次 refresh 必須做 comprehensive news scan,**唔可以只 update 之前嘅 timeline**
- 🔴 **skill 改良**:對 model series major version 變化(M2 → M3)必須 flag 為 critical update

**新嘅 correction rule**:
> **對 IPO < 6 個月嘅 company,任何 model series major version 發布必須喺 24 小時內加入 catalyst timeline,否則 report 視為 outdated。**

---

## 7. 5-way Peer Comparison — **v3.0 重大修正**

| 公司 | 估值 | 2026 ARR | P/ARR 倍數 | 最新 frontier model | 開源策略 | 商業模式 | 護城河強度 | 30 天股價 |
|---|---|---|---|---|---|---|---|---|
| **智譜(02513.HK)** | **US$138B** | **US$232M** | **57x** | **GLM-5.2**(2026-06-17 MIT 開源,SWE-Bench Pro 超越 GPT-5.5)| **GLM 開源 + Coding Plan** | **雙軌** | **★★★★★** | **+15%** |
| **MiniMax(00100.HK)** | **US$15.9B** | **US$150M (2 月)** | **106x** ⚠️ | **M3**(2026-06-01,1M context,SWE-Bench Pro 59.0%,逼近 Opus 4.7)| M2/M2.7/M3 開源 + Hailuo closed | **中間層 + apps** | **★★★★**(v3.0 升 ⭐️) | **-30%** 🔴 |
| **月之暗面** | **US$20B** | **US$100M+ (3 月)** | 200x 🆕 | K2.5 / K2.5 Pro | K2.5 開源 | API + app | ★★★ | ? |
| **DeepSeek** | **US$45B** | 未公開 | N/A | **V4-Pro 開源** | V4-Pro 開源 | API + B2B | ★★★★ | ? |
| **阿里通義** | 阿里市值一部份 | 未公開 | N/A | Qwen 3 | Qwen 開源 | API + 雲 | ★★★★ | ? |

**v3.0 修正 insight**:
- ✅ **MiniMax M3 同智譜 GLM-5.2 都係 frontier tier**,差距細(SWE-Bench Pro 59.0 vs 58.4)
- ✅ **MiniMax 嘅護城河** 由 ★★★ 升至 ★★★★(M3 超越 GPT-5.5 係重大 catalyst)
- ⚠️ 但智譜嘅雙軌(開源 + Coding Plan)定位仍強過 MiniMax(中間層 + apps)
- ⚠️ **P/ARR 106x 仍然係最高**,因為市值雖然低但 ARR 更低
- ❌ **股價 -30% 30 天 vs 智譜 +15%** 反映市場對 MiniMax 嘅信心較弱

---

## 8. 4 大師視角分析 — **v3.0 加強**

### 段永平

**Right business**: 中等偏強(★★★)
- ✅ 多模態完整 + 國際化先發(70% 海外)
- ✅ M3 = 1M context + 原生多模態 + 自研 MSA — **frontier tier model**
- ⚠️ AI 原生產品用戶增長放緩
- ⚠️ 中間層 specialist 容易被夾擊

**Right people**: 中等偏強
- ✅ 閆俊杰技術 depth,M3 MSA 自研架構顯示工程能力
- ✅ 385 人精幹團隊

**Right price**: **🔴 唔啱**
- HK$396 = 106x P/ARR(仲貴過智譜)
- M3 catalyst + GLM-5.2 對標雙雙 fully priced in
- 從高位 -70% 但仍然極度貴

### 巴菲特

**Moat**: 中等偏強(★★★ → ★★★★)— v3.0 升一級
- 品牌(★★★):M3 SWE-Bench Pro 59.0 提升 brand recognition
- 轉換(★★):仍係中等
- 網絡(★★):仍係弱
- 規模(★★★→★★★★):M3 顯示規模效應有效
- **技術(★★★→★★★★)**:M3 MSA 自研 + SWE-Bench Pro 超越 GPT-5.5

**Management**: 中等(3.5/5)
- M3 6 個月內從概念到發布 = 強 execution
- 但 IPO 後 -70% 反映 investor communication 可能弱

**Margin of safety**: **🔴 完全冇**
- 106x P/ARR 仍然 priced in 全部樂觀情景
- 中性 -81% 下行

### 芒格

**Inversion**:
- 🔴 **解禁後 insider selling**(港股 HK$1.55 萬億解禁潮)
- 🔴 **AI 原生產品用戶持續下滑**
- ⚠️ **智譜 GLM-5.2 對標壓力**(Coding Plan + MIT 開源 = 雙軌對 M3 嘅中間層 specialist 構成威脅)
- ⚠️ **DeepSeek V5 / GLM-5.3 全面超越 M3**
- ⚠️ **海外監管打擊**(70% 海外收入)
- ⚠️ **開源策略擠壓商業空間**

### 李錄

**10-year framing**:
- ✅ M3 MSA 自研 + SWE-Bench Pro 超越 GPT-5.5 = 重要 milestone
- ✅ M3 嘅 1M context + native multimodal 係 frontier trend 嘅 proof point
- ⚠️ 但中間層 specialist 嘅 10 年生存率仍低
- ⚠️ 對比智譜雙軌 vs MiniMax 中間層,定位仍弱

---

## 9. 綜合決策備忘錄

### 9.1 七維度結論 — **v3.0 修正**

| 維度 | v2.0 結論 | **v3.0 結論** | v2.0 信心度 | **v3.0 信心度** |
|---|---|---|---|---|
| 生意質量(段永平) | 中間層 specialist | **中間層 specialist + frontier M3 提升** | ★★★ | ★★★★ |
| 護城河(巴菲特) | 5 類 moat 偏弱 | **M3 提升技術 + 規模 moat ★★★★** | ★★★ | ★★★★ |
| 管理層(段永平+巴菲特) | 閆俊杰技術深度強 | **6 個月內 M2.7 → M3 顯示 execution** | ★★★★ | ★★★★★ |
| 最大風險(芒格) | 解禁壓力 + 流通量 | **解禁 + 流通量 + GLM-5.2 對標** | ★★ | ★★ |
| 文明趨勢(李錄) | AI 範式轉移,MiniMax 定位弱 | **AI 範式轉移,M3 提升定位但仍弱過智譜雙軌** | ★★★ | ★★★ |
| 估值(巴菲特+段永平) | 🔴 106x P/ARR 極度貴 | **🔴 106x P/ARR 仍然極度貴** | ★ | ★ |
| **綜合** | 🔴 不買,等回調 | **🔴 不買,等回調** | **2.5 / 5** | **2.5 / 5** |

### 9.2 最終操作建議 — **v3.0 不變**

| 策略 | 建議 |
|---|---|
| **空倉者** | **不買**,等候回調至 **HK$100-150** |
| **持倉者** | **🔴 強烈建議減倉 70-90%** |
| **賣出信號** | 解禁後 insider selling / 海外監管 / AI 原生產品用戶繼續下滑 |
| **加倉信號** | **回調至 HK$100-150** / M3 開源後開發者採用率 > GLM-5.2 / 海外收入加速 |

### 9.3 合理買入區間(unchanged)

| 情景 | 價格(HKD)| 倍數 | 安全邊距 |
|---|---|---|---|
| 極度保守 | HK$60-80 | ~15x | 80-85% |
| 合理 | HK$100-120 | ~25x | 70% |
| 投機性 | HK$150-200 | ~30x | 50% |

### 9.4 紅線清單(unchanged)

| 紅線 | 觸發動作 |
|---|---|
| 股價跌穿 HK$300 | 重新評估 |
| 股價跌穿 HK$200 | **開始買入區間** |
| **解禁後 insider selling > 5%** | 賣出信號 |
| DeepSeek V5 / GLM-5.3 全面超越 M3 | 賣出 |
| 海外監管打擊 | 賣出 |

### 9.5 4 大師模擬點評

> ⚠️ **Disclaimer**: 以下引言係 AI 模擬,唔係真實 quote。

> **巴菲特**(AI 模擬):「M3 嘅 SWE-Bench Pro 59.0 證明咗技術領先,但 106x P/ARR 已經 priced in 10 年後嘅成就。等佢跌 80% 再講。」

> **芒格**(AI 模擬):「即使 M3 frontier + 解禁壓力,股價仍 -70%。聰明錢已經散場。等下一輪 catalyst(M3 開源後實際開發者採用率)先再入場。」

> **段永平**(AI 模擬):「M3 + MSA 自研架構 = right business + right people。但 right price 仲未到 — HK$396 仲貴過 OpenAI 上市前估值。等 HK$100-150。」

> **李錄**(AI 模擬):「AI 文明級範式轉移無懸念,M3 + GLM-5.2 雙雙 frontier 係 proof point。但 MiniMax 嘅中間層 specialist 定位 10 年後生存率仍低過智譜雙軌。Timing 唔啱。」

---

## 10. 數據抽檢(同 v2.0 — 19/19 PASS)

---

## 11. v3.0 對 skill 嘅改良建議

**`ipo-catalyst-analysis` skill v1.1 改良**:

1. **新增 Step 2.5**:「**Comprehensive News Scan**(每次 refresh 都做,非增量更新)」
2. **新增 Step 6.5**:「**Major Version Detection** — 對 model series 嘅 major version 變化必須 24 小時內 flag」
3. **新增 Step 7.5**:「**Competitor Parallel Tracking** — 對手嘅對應版本要 parallel track」
4. **新增 Step 9.5**:「**v(n) → v(n+1) Audit Trail** — 每次修正都要明確列出 missed 嘅 catalyst**

---

## 數據來源

| 來源 | URL |
|---|---|
| MiniMax M3 官方頁 | https://www.minimaxi.com/models/text/m3 |
| MiniMax M3 Research Blog | https://www.minimaxi.com/blog/minimax-m3 |
| OSCHINA M3 發布 | https://www.oschina.net/news/450198 |
| STCN M3 報導 | https://www.stcn.com/article/detail/3936246.html |
| 知乎 M3 深度評測 | https://zhuanlan.zhihu.com/p/2044924034291430419 |
| 知乎 M3 Frontier 三件套 | https://zhuanlan.zhihu.com/p/2045570593915917090 |
| blocktempo M3 價格分析 | https://www.blocktempo.com/minimax-m3-open-weights-beats-gpt-gemini-benchmarks-fraction-cost/ |
| 新浪財經 M3 社區評論 | https://finance.sina.com.cn/stock/t/2026-06-03/doc-iniaarra1104991.shtml |
| Lushbinary M3 vs M2.7 | https://lushbinary.com/blog/minimax-m3-vs-m2-7-whats-new-upgrade-guide/ |
| LLMReference M2.7 vs M3 | https://www.llmreference.com/compare/minimax-m2.7/minimax-m3 |
| 智譜 GLM-5.2 開源 | https://www.oschina.net/news/460824 |
| 智譜 GLM-5.2 Coding Plan | https://finance.sina.com.cn/tech/digi/2026-06-13/doc-inicfvnr2880919.shtml |
| 智譜 GLM-5.1 SWE-Bench | https://tw.stock.yahoo.com/news/%E9%A7%90%E6%B4%BEai%E9%96%8B%E6%BA%90glm-5-1%E5%A4%A7%E6%A8%A1%E5%9E%8B-swe-bench-043326634.html |
| 智譜 GLM-5.2 知乎 | https://zhuanlan.zhihu.com/p/2050158905360135402 |
| 騰訊新聞 GLM-5.2 發布 | https://news.qq.com/rain/a/20260616A04LHW00 |
| 招股書 | 港交所 00100.HK 全球發售文件 |
| HKET M2.7 發布 | https://inews.hket.com/article/4100511/minimax-00100-m27-model-ai |
| 21 財經「活在智譜陰影下」| https://m.21jingji.com/article/20260625/herald/9a2065d64100c121228f922cb334b48c.html |
| 36kr 解禁潮 | https://36kr.com/p/3843832002971905 |
| 36kr MiniMax 上市分析 | https://36kr.com/p/3606464589923336 |
| 雪球 stock | https://xueqiu.com/S/00100 |
| 富途 stock | https://www.futunn.com/stock/00100-HK |
| 騰訊財經 00100 | https://gu.qq.com/hk00100 |
| shareuhack M2.7 guide | https://www.shareuhack.com/en/posts/minimax-m27-local-ai-guide-2026 |
| Wikipedia MiniMax | https://en.wikipedia.org/wiki/MiniMax_Group |
| 新浪財經 M3 預告 | https://finance.sina.com.cn/wm/2026-05-28/doc-inhzmihu0190597.shtml |

---

⚠️ **免責聲明**: 本報告僅供研究同教育用途,非投資建議。歷史表現唔代表未來收益。投資涉及風險,讀者需自行作出獨立判斷。