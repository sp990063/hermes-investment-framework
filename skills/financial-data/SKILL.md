---
name: financial-data
description: 投資研究嘅數據獲取 + 交叉驗證規範。每個關鍵數據必須來自 2 個獨立來源,誤差 > 1% 須標記。用於 investment-research / investment-team / earnings-* / portfolio-review 等涉及財務數字嘅 skill 之前預載。
---

# 財務數據獲取與交叉驗證規範

本規範適用於所有涉及企業財務數據嘅研究。**每個關鍵數據必須來自兩個獨立來源,誤差 > 1% 須標記。**

---

## 數據源優先級

### 美股(PDD、騰訊 ADR、網易 ADR 等)

| 優先級 | 來源 | URL | 獲取方式 |
|---|---|---|---|
| 1(主) | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | 直接訪問,無需註冊 |
| 2(副) | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | 直接訪問,無需註冊 |
| 原始一手 | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q 原文 |

### 港股(騰訊 0700、網易 9999、美團 3690 等)

| 優先級 | 來源 | URL | 獲取方式 |
|---|---|---|---|
| 1(主) | **aastocks** | aastocks.com/tc/stocks/analysis/company-fundamental | 直接訪問 |
| 2(副) | **macrotrends**(ADR 代碼) | 騰訊用 TCEHY,網易用 NTES | 直接訪問 |
| 原始一手 | HKEX 披露易 | hkexnews.hk | 年報 PDF |

### A 股(三七互娛、吉比特等)

| 優先級 | 來源 | URL | 獲取方式 |
|---|---|---|---|
| 1(主) | **東方財富** | eastmoney.com → 搜股票代碼 → 財務報表 | 直接訪問 |
| 2(副) | **巨潮資訊** | cninfo.com.cn | 原始年報/季報 PDF |

---

## 執行規範

### 第一步:獲取數據

對每個財務指標(收入、淨利潤、毛利率、經營現金流、資產負債率等),分別從**來源 1**和**來源 2**取數。

### 第二步:誤差計算與標記

```
誤差率 = |來源1數值 - 來源2數值| / 來源1數值 × 100%
```

| 誤差 | 處理方式 |
|---|---|
| ≤ 1% | ✅ 一致,取來源 1 數值,標註兩個來源 |
| 1% ~ 5% | ⚠️ 標記「數據存在差異」,註明兩個數值,說明可能原因(匯率/會計口徑) |
| > 5% | ❌ 標記「數據存在重大差異」,必須查原始財報核實,不得直接使用 |

### 第三步:數據呈現格式

每個關鍵數據必須按以下格式標註:

```
收入：1,239億元 ✅
  - macrotrends: 1,241億元
  - stockanalysis: 1,237億元
  - 誤差: 0.3%
```

差異示例:

```
淨利潤：245億元 ⚠️ 數據存在差異
  - macrotrends: 245億元（GAAP）
  - stockanalysis: 278億元（Non-GAAP）
  - 誤差: 13.5% — 原因：會計口徑不同（GAAP vs Non-GAAP）
```

---

## 常見差異原因(不一定是數據錯誤)

| 原因 | 說明 |
|---|---|
| GAAP vs Non-GAAP | 最常見,尤其是利潤類數據 |
| 匯率換算 | 港幣/人民幣/美元換算時間點不同 |
| 財年定義 | 自然年 vs 財年(如蘋果財年 10 月結束) |
| 合併口徑 | 是否含少數股東權益 |
| 數據更新滯後 | 某平台尚未更新最新一期財報 |

---

## 特別規則

1. **未上市公司**(米哈遊、莉莉絲等):只有一手數據來源時,數據前標記 `[估計]`,不執行交叉驗證
2. **季度數據 vs 年度數據**:優先使用年度數據做交叉驗證,季度數據部分來源可能有滯後
3. **原始財報優先**:若兩個來源均與原始財報(10-K/年報 PDF)不符,以原始財報為準,標記來源錯誤

---

## 工具化執行(推薦)

用 Python tool 做程式化交叉驗證 + 市場值手算:

```bash
# 市值驗算
python3 ~/.hermes/scripts/financial/financial_rigor.py verify-market-cap \
  --price {股價} --shares {總股本} --reported {報告市值} --currency HKD

# 多源交叉驗證
python3 ~/.hermes/scripts/financial/financial_rigor.py cross-validate \
  --field "2025Q3_revenue" \
  --values '{"aastocks": 1670000000000, "macrotrends": 1675000000000}' \
  --unit HKD

# Benford 定律檢測(造假財報早期警訊)
python3 ~/.hermes/scripts/financial/financial_rigor.py benford \
  --data '[<comma-separated numbers>]'
```

**優點:** Decimal precision、machine-parseable JSON output、stderr 顯示人類 readable summary。

---

## 快速索引

| 場景 | 主要來源 | 備用來源 |
|---|---|---|
| PDD / 拼多多 | macrotrends.net/stocks/charts/PDD | stockanalysis.com/stocks/pdd |
| 騰訊 | macrotrends.net/stocks/charts/TCEHY | aastocks(0700.HK) |
| 網易 | macrotrends.net/stocks/charts/NTES | aastocks(9999.HK) |
| 三七互娛 | eastmoney.com(002555) | cninfo.com.cn |
| 吉比特 | eastmoney.com(603444) | cninfo.com.cn |
| Nintendo | macrotrends.net/stocks/charts/NTDOY | stockanalysis.com/stocks/ntdoy |
| Capcom | macrotrends(CCOEY) | stockanalysis(CCOEY) |