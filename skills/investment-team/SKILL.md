---
name: investment-team
description: 4 大師視角(段永平/巴菲特/芒格/李錄)並行深度投研團隊。用 Hermes delegate_task 啟動 background subagent 做獨立研究,Team Lead 綜合 4 份 report 出一份完整決策。當用戶話「投研團隊」「team 分析」「4 個 agent 並行研究」時 trigger。
---

# 投研團隊:四角色並行分析框架 (Hermes port)

對 $ARGUMENTS 進行團隊化投資研究分析。Hermes 透過 `delegate_task` 啟動多個獨立 background subagent 做真嘅並行研究,模擬真實投研團隊協作。

**Reference**:見 `references/hk-ai-dual-pilot-2026-07.md` 嘅 MiniMax + 智譜 GLM 雙雄 case study(港股大模型 IPO 範式),含已驗證數據 + pitfalls 摘要。

**Hermes 限制說明**:Hermes `delegate_task` batch mode 最多 3 個 task per turn。本 skill 用 **3 並行 + 1 sequential**(合併「行業 / 風險」分析到 risk_assessor,獨立 spawn business / financial / risk 三個 agent,收到結果後再 spawn 第 4 個 — 李錄文明趨勢 agent)。

如果你嘅 Hermes config 容許 `max_concurrent_children: 4`,可以改成 batch 4 並行。Default 用 3+1 模式。

---

## 執行流程

### 第一步:展示團隊框架

向用戶展示以下團隊結構,確認後啟動:

| 角色 | 職責 | 分析框架 |
|---|---|---|
| **team-lead**(你自己) | 統籌協調、匯總研判、輸出最終報告 | 四大師綜合框架 |
| **business-analyst** | 商業模式 & 護城河分析 | 段永平視角 |
| **financial-analyst** | 財務報表 & 估值分析 | 巴菲特視角 |
| **risk-assessor** | 行業格局 + 風險 + 文明趨勢 | 芒格 + 李錄視角(合併) |

### 第一步半:AI 研究偏見評估

喺創建團隊前,先向用戶展示該公司嘅「AI 可研究性」評估:

**信息豐富度評級**(決定研究策略):

| 等級 | 特徵 | 研究策略調整 |
|---|---|---|
| **A 級**(信息充裕) | 上市多年、券商覆蓋廣 | 團隊重點放喺**反面檢驗**同**非共識視角**,避免輸出與市場一致嘅「正確嘅廢話」 |
| **B 級**(信息適中) | 上市不久、覆蓋有限 | 每個 agent 嘅推算數據必須標註置信度,team-lead 匯總時標註「數據充分度」 |
| **C 級**(信息稀缺) | 冷門 / 新上市 / 新興市場 | 團隊轉為「第一性原理模式」:唔追求報告完整性,聚焦商業本質嘅幾個核心問題 |

**關鍵提醒**:資料多 ≠ 確定性高,資料少 ≠ 確定性低。AI 能輸出嘅置信度 ≠ 投資嘅真實確定性。確定性嚟自商業模式本身,唔嚟自資料數量。

將評級結果告知每個 agent,影響其研究方式。

### 第二步:啟動 3 個並行 subagent

用 `delegate_task` 同時啟動 3 個 background subagent,**必須喺同一條 message 入面 batch**。Hermes 用 `tasks` array 而唔係 `goal`:

```
delegate_task(
  tasks=[
    {
      "goal": "分析 {公司名} 嘅商業模式、護城河同用戶價值(段永平視角)...",
      "context": "段永平視角:好生意嘅 5 個特徵...",
      "toolsets": ["web", "terminal", "file"]
    },
    {
      "goal": "分析 {公司名} 嘅財務數據、盈利能力同估值(巴菲特視角)...",
      "context": "巴菲特視角:護城河 + 安全邊際...",
      "toolsets": ["web", "terminal", "file"]
    },
    {
      "goal": "評估 {公司名} 嘅投資風險、管理層質量、行業競爭(芒格+李錄視角)...",
      "context": "芒格式逆向 + 李錄文明趨勢...",
      "toolsets": ["web", "terminal", "file"]
    }
  ]
)
```

### 第三步:3 個 subagent prompt 模板

每個 subagent 收到自己嘅 goal + context,獨立研究,獨立寫一份 markdown report,返回 summary。

#### Agent 1 — business-analyst (段永平視角)

**Goal**: 分析 {公司名} 嘅商業模式、護城河同用戶價值。

**必須涵蓋**:
1. 商業模式本質:核心生意定義、收入結構拆解
2. 平台 / 產品飛輪效應如何運轉
3. 護城河分析(逐一驗證 5 類):品牌 / 轉換成本 / 網絡效應 / 規模效應 / 技術壁壘
4. 用戶 / 客戶價值:為各方創造咗咩獨特價值
5. 業務矩陣與協同效應
6. 段永平「好生意」標準評估:差異化、定價權、可持續競爭優勢

**研究方法**:
- 用 `web_search` + `web_extract` 搜最新公開信息(年報、行業報告、新聞)
- 財務數據必須來自兩個獨立來源,按 `~/.hermes/skills/finance/financial-data/SKILL.md` 規範執行(美股:macrotrends+stockanalysis;港股:aastocks+macrotrends;A 股:東方財富+巨潮資訊),兩源誤差 > 1% 須標記
- 善用 `~/.hermes/scripts/financial/financial_rigor.py` 做程式化驗算

**輸出格式**:返回完整 markdown report(800-1500 字),含表格同明確結論。最後附 5 句「鏡子測試」陳述。

#### Agent 2 — financial-analyst (巴菲特視角)

**Goal**: 分析 {公司名} 嘅財務數據、盈利能力同估值。

**必須涵蓋**:
1. 近 3-5 年營收、淨利潤、經營利潤趨勢
2. 盈利能力指標:ROE、ROA、毛利率、經營利潤率
3. 現金流分析:經營性現金流、自由現金流、資本開支
4. 資產負債表健康度:現金儲備、負債率、流動性
5. 估值分析:PE/PS/PB/EV 等,與歷史及同業對比
6. 安全邊際評估:內在價值 vs 當前股價

**金融嚴謹性驗證(必須使用 Bash 調用工具,禁止心算)**:

```bash
# 市值驗算
python3 ~/.hermes/scripts/financial/financial_rigor.py verify-market-cap \
  --price {價格} --shares {股本} --reported {報告市值} --currency {幣種}

# 估值驗算
python3 ~/.hermes/scripts/financial/financial_rigor.py verify-valuation \
  --price {價格} --eps {EPS} --bvps {每股淨資產}

# 三情景估值
python3 ~/.hermes/scripts/financial/financial_rigor.py three-scenario \
  --price {價格} --eps {EPS} --shares {股本億} \
  --growth {樂觀增速} {中性增速} {悲觀增速} \
  --pe {樂觀PE} {中性PE} {悲觀PE} --years 3 --currency {幣種}
```

將工具輸出結果直接嵌入報告中作為驗證記錄。

#### Agent 3 — risk-assessor (芒格 + 李錄視角,合併)

**Goal**: 評估 {公司名} 嘅投資風險、管理層質量、行業競爭同文明趨勢。

**必須涵蓋**:
1. **芒格式逆向思考**:列出「呢間公司可能失敗嘅所有路徑」(表格:路徑 / 概率 / 影響程度)
2. **跨學科分析**:用網絡效應理論、技術採納曲線、競爭博弈等模型交叉驗證
3. **偏誤自查**:敘事偏差、錨定效應、倖存者偏差
4. **管理層評估**(段永平 + 巴菲特):CEO 能力圈、誠信度、戰略眼光、資本配置能力、歷史決策質量
5. **監管風險**:當前及潛在監管影響
6. **競爭風險**:各競爭對手威脅程度評估
7. **業務風險**:新業務虧損、擴張不確定性
8. **宏觀風險**:經濟週期、行業週期影響
9. **公司治理**:股權結構、關聯交易、股東回報政策
10. **長期確定性**:10 年後公司會點?咩可能顛覆其商業模式?
11. **李錄文明趨勢**:判斷所在行業係咪處於「文明級範式轉移」;歷史技術革命類比(蒸汽機 / 電力 / 互聯網 / AI);TAM 增長曲線與天花板分析;技術路線風險

### 第四步:接收 3 份 subagent report,啟動第 4 個

3 份 subagent 自動返回 summary 嘅同時,**自己(team-lead)用埋同樣工具讀取** — 用 `read_file` 讀每份 report 嘅 markdown 全文。

讀完之後,**啟動第 4 個 sequential subagent** — 「李錄文明趨勢深度分析」(獨立 vision,避免過度塞入 risk-assessor):

```
delegate_task(
  goal="基於以下 3 份 report,從李錄'文明演進'視角分析 {公司名} ...",
  context="將 3 份 report 內容貼上,再要求李錄視角獨立分析...",
  toolsets=["web", "terminal", "file"]
)
```

### 第五步:綜合最終報告

綜合 4 份分析報告,輸出以下結構嘅最終報告:

---

#### 1. 一句話結論

> 用一段話(50-100 字)概括是否值得投資及核心邏輯

#### 2. 四維評分總表

| 維度 | 框架 | 評分(1-5 星) | 核心判斷 |
|---|---|---|---|
| 商業模式 & 護城河 | 段永平 | ★★★★☆ | 雙邊網絡效應強勁,飛輪運轉 |
| 財務 & 估值 | 巴菲特 | ★★★★☆ | 核心業務利潤率改善,估值低 |
| 行業 & 競爭 | 芒格 | ★★★☆☆ | 抖音入侵,格局有風險 |
| 風險 & 文明趨勢 | 李錄 | ★★★★☆ | 順應文明趨勢但非範式轉移 |

**綜合評分**:X / 5

#### 3. 核心數據速覽

關鍵財務和經營指標表格(近 2 年對比,標註數據源)

#### 4. 各維度分析摘要

每個維度摘取 3-5 條最重要嘅發現

#### 5. 投資論點(Bull vs Bear)

- 🟢 看多邏輯(5-7 條)
- 🔴 看空邏輯(5-7 條)

#### 6. 巴菲特買入前 Checklist

| # | 檢查項 | 通過? | 說明 |

10 個核心檢查項,逐一評估

#### 7. 最終投資建議

- 定性判斷表(生意質量 / 管理層 / 估值 / 時機)
- 分層操作建議表(激進型 / 穩健型 / 保守型 → 建議 + 價格區間)
- 關鍵催化劑(加倉信號 / 減倉信號各 3-5 條)

#### 8. 總結段落

100-200 字嘅最終總結

---

### 第六步:保存報告

將完整最終報告寫入 `~/{公司名}投資研究報告_{日期}.md`(日期格式 YYYYMMDD)。

### 第七步:數據抽檢(準出流程)

```bash
# Step 1 — 提取抽檢清單(15% 隨機抽樣)
python3 ~/.hermes/scripts/financial/report_audit.py extract \
  --report <報告文件路徑>

# Step 2 — 對清單每項從可靠信源取數(按 financial-data 規範)

# Step 3 — 輸出準出 / 打回判決
python3 ~/.hermes/scripts/financial/report_audit.py verdict \
  --results '<填好嘅 JSON>' \
  --report <報告文件名>
```

- **【準出】**:全部通過 → 報告可發布
- **【打回】**:有不通過 → 修正後重審

---

## 重要注意事項

1. **3 個 subagent 必須並行啟動** — 喺同一個 `delegate_task` call 入面用 `tasks` array,3 個 goal 同時跑
2. **subagent 透過 `context` 收到 4 大師視角 + 數據源規範**
3. **數據準確性** — 要求 agent 使用 `web_search` 搜最新數據,關鍵數據交叉驗證
4. **結論要明確** — 不迴避給出買入 / 觀望 / 迴避建議同具體價格區間
5. **所有分析必須有數據支撐** — 附數據來源
6. **耐心等待** — 3 個 agent 研究需要幾分鐘,實時向用戶更新進度
7. **反偏見意識** — team-lead 喺匯總時必須評估:各 agent 嘅分析是否受限於資料充裕度?是否與市場共識過度趨同?最終報告需包含「信息豐富度評級」同「AI 研究局限性聲明」
8. **信息稀缺時嘅誠實原則** — 寧可喺報告中留白標註「數據不足」,亦唔好用推測填滿框架偽裝確定性
9. **Token 控制** — 4 個 subagent + team-lead 會燒 token。輕量決策先用 `quality-screen`,確認值得先深入先用本 skill

---

## ⚠️ 重要 Pitfalls(由實際執行錯誤得出)

### Pitfall 1: Subagent 可能被 timeout 中斷

**症狀**:`[ASYNC DELEGATION BATCH COMPLETE — <id>]` 但 status = `interrupted`,所有 task 返「no summary」。

**原因**:
- Subagent 自己執行時間過長(典型 web_search × 多 + 大量 markdown 寫作 → 燒 token → batch 時間超限)
- Hermes batch 有隱式 timeout(實際長度視 config 但 ~5 分鐘內嘅深研究有風險)

**補救方案**(順序由 team-lead 即時採用):

| 方案 | 觸發條件 | 操作 |
|---|---|---|
| **A. Re-dispatch**(信心高時) | 用戶要 4 個獨立視角嘅嚴謹度 | 用更窄 scope re-dispatch,例如將每個 agent 限時 1 分鐘 + 限制 markdown 長度 |
| **B. Team-lead 自建 4 視角**(默認推薦) | 用戶要快 + 你已經有 domain context | 用已搜集嘅招股書 / 新聞數據,自己扮 4 個視角寫綜合報告,標註「team-lead 用已搜集數據重構,非獨立 subagent」 |
| **C. 轉 single-agent sequential** | 想要嚴謹 + 唔趕時間 | 改用 `/investment-research` 跑 deep-dive(7 模組 sequential) |

**重要**:唔好默認等 subagent 返結果之後先動。**Dispatch 同時,team-lead 應該自己開始用 web_search / web_extract 累積 domain context**,咁 subagent 一旦 failed 即時有 fallback。

### Pitfall 2: 虧損大模型公司唔可以用 PE-based three-scenario

`financial_rigor.py three-scenario` 嘅核心係 `future_eps × exit_pe`。**虧損公司 EPS 為負 → 隱含市值為負 → 完全冇意義**。

**解決**:用 **P/ARR 倍數法**手動計,例如:

```
2026E ARR × 退出倍數 = 隱含市值

樂觀: US$600M × 30x = US$18,000M(對標 OpenAI 25-40x)
中性: US$300M × 20x = US$6,000M
悲觀: US$150M × 12x = US$1,800M
```

對標 OpenAI(25x)、Anthropic(40x)、Mistral(25-50x)嘅倍數範圍,**挑公司特性揀倍數**:
- 閉源 + 護城河深 → 30-40x
- 開源領導者(GLM 角色) → 20-25x
- 中間層 specialist → 12-20x
- 高度投機 → < 15x

### Pitfall 3: 用戶問「研究 X 同 Y」時要準備横向對比表

**唔好**為每間公司寫獨立 report 就交差,**一定要出對比表**:
- 收入規模 / 增速 / 毛利率
- IPO 估值 vs 對標同業(OpenAI / Anthropic / 商湯)
- 護城河評分對比
- Catalyst timeline(發布日 / 業績日)

對比表係 investment-team 嘅核心 deliverable,**唔係各自 report**。