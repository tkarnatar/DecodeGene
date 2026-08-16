# 🤖 用 DeepSeek V4 Flash 為 3000 個基因生成白話敘事 — 完整指令

> 這份指令讓你**不用寫程式**，也能用 DeepSeek V4 Flash（或其他模型）批次為批量基因撰寫白話解釋。
> 專案已內建自動化腳本 `pipeline/generate_narratives.py`，兩者擇一即可。

---

## 一、兩種執行方式

### 方式 A：自動化腳本（推薦，需 API Key）
```bash
# 先測試前 10 個
python -m pipeline.generate_narratives --limit 10

# 全部 3000 個（斷點續跑、增量存檔）
python -m pipeline.generate_narratives
```
腳本會自動讀取 `backend/.env` 的 `DEEPSEEK_API_KEY`，輸出 `data/processed/bulk_narratives.json`，
後端啟動時會自動把敘事合併進知識庫（**證據欄位永遠保留 ClinVar 機器值，不被 AI 覆寫**）。

### 方式 B：手動切換模型（不用 API Key）
把下面「系統 Prompt」貼給 DeepSeek V4 Flash，再依序餵入每個基因的「證據輸入」，收集 JSON 輸出即可。

---

## 二、系統 Prompt（直接複製貼上）

```
你是一名資深臨床遺傳諮詢師與頂級基因科普作家。你的任務是為「基因-疾病」條目
撰寫面向大眾的白話解釋（生活比喻、摘要、篩檢建議、就醫提問、辟謠）。

語氣要求：溫和、客觀、極度通俗，嚴禁未加解釋的晦澀術語，堅決避免引發基因焦慮。

嚴格的「有根據生成」規則：
1. 只根據使用者提供的「證據輸入」撰寫，不得編造證據中沒有的資訊。
2. 嚴禁編造具體藥物名稱、確切篩檢年齡、確切百分比數字、具體劑量。
   篩檢建議一律使用安全表述，例如「建議諮詢專科醫師制定個體化篩檢方案」。
3. 生活比喻要生動貼近日常，但不得誤導（不得暗示「必然得病」）。
4. 不得把「易感/風險升高」說成「一定會生病」。
5. 辟謠的「真相」必須符合主流醫學共識，不誇大。
```

---

## 三、輸出 JSON Schema

每個基因輸出**一個 JSON 物件**，欄位如下（皆為**簡體中文**，若要繁體把「簡體」改成「繁體」即可）：

```json
{
  "chinese_name": "基因中文名（若無法確認可留空字串）",
  "metaphor_title": "生活比喻標題，含一個 emoji，例如「🧬 細胞裡的【DNA 維修工】」",
  "metaphor_story": "生活比喻故事，3-5 句，用日常事物解釋該基因的功能與突變後果",
  "plain_summary": "白話摘要，2-3 句，說明攜帶突變的實際意義，不製造焦慮",
  "screening_advice": "篩檢建議，安全表述，不編造年齡或檢查細節",
  "lifestyle_tips": ["生活建議 1", "生活建議 2", "生活建議 3"],
  "key_questions": ["就醫時可問醫生的問題 1", "問題 2", "問題 3"],
  "myth": "大眾常見迷思（用引號包起來的問句）",
  "truth": "科學真相，用「不是」或「錯」開頭糾正迷思"
}
```

> 注意：**不要**讓 AI 生成 `academic_summary`（科研摘要）或任何證據分數——那些欄位由 ClinVar 機器資料提供，避免 AI 幻覺。

---

## 四、證據輸入格式（每次餵一個基因）

```json
{
  "gene_symbol": "TTN",
  "disease_name": "Hypertrophic cardiomyopathy 9",
  "clinvar_pathogenic_count": 11842,
  "star_rating": 5,
  "severity_badge": "🟢 明确致病基因"
}
```

完整證據清單在 `data/processed/bulk_associations.json`（已按致病變異數從高到低排序）。

---

## 五、批次執行流程

1. 從 `bulk_associations.json` 依序取出每個基因的 `gene_symbol` 與 `disease.name` 等證據欄位。
2. 每次只餵**一個基因**的證據輸入，要求輸出一個 JSON。
3. 收集所有 JSON，組合成以基因符號為 key 的物件：
   ```json
   { "NF1": { ... }, "TTN": { ... }, "ATM": { ... } }
   ```
4. 存成 `data/processed/bulk_narratives.json`，後端啟動時自動合併。

---

## 六、注意事項

- **斷點續跑**：每完成一批就存檔，中斷後跳過已完成基因。
- **優先處理高證據基因**：依 `clinvar_pathogenic_count` 從高到低，最重要的先寫。
- **品質把關**：建議先抽樣人工審核 10-20 個高風險基因的輸出，再放量。
- **免責聲明**：所有 AI 生成內容須視為「待審核」，前端會標示，且不影響機器證據欄位。
