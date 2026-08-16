# 🤖 DeepSeek V4 Flash 批量生成敘事 — 可重複使用的 Prompt

> 用法：切換到 DeepSeek V4 Flash 後，把下面「複製區」整段貼給它即可。
> 它會讀取 `data/processed/bulk_associations.json`、跳過已完成、批次生成白話敘事、寫回 `data/processed/bulk_narratives.json`。

---

## 複製區（整段貼給 Flash）

```
你是 DecodeGene 專案的資深臨床遺傳諮詢師與基因科普作家。請為專案裡「缺白話敘事」的批量基因補寫敘事。

## 前置（先讀這兩個檔案）
1. data/processed/bulk_associations.json —— 約 8710 個基因的 JSON 陣列，每條含
   gene.symbol、disease.name、evidence.clinvar_pathogenic_count、evidence.star_rating、disease.severity_badge。
2. data/processed/bulk_narratives.json —— 以基因符號為 key 的物件，已有約 3300 條，這是「已完成」清單。

## 任務
對每一個「不在 bulk_narratives.json 中」的基因，依 evidence.clinvar_pathogenic_count 從高到低，
逐一產出一個 JSON 物件，欄位如下（全部簡體中文）：
{
  "chinese_name": "基因中文名（無法確認就留空字串）",
  "disease_chinese_name": "疾病中文名（翻譯 disease.name，專有名詞保留原樣或音譯，type N 翻成「N 型」）",
  "metaphor_title": "生活比喻標題，含一個 emoji，例如「🧬 細胞裡的【DNA 維修工】」",
  "metaphor_story": "生活比喻故事，3-5 句，用日常事物解釋基因功能與突變後果",
  "plain_summary": "白話摘要，2-3 句，說明攜帶突變的實際意義",
  "screening_advice": "篩檢建議（安全表述，例如「建議諮詢專科醫師制定個體化篩檢方案」，不編造年齡或檢查細節）",
  "lifestyle_tips": ["生活建議 1", "生活建議 2", "生活建議 3"],
  "key_questions": ["就醫時可問醫生的問題 1", "問題 2", "問題 3"],
  "myth": "大眾常見迷思（用引號包起來的問句）",
  "truth": "科學真相，用「不是」或「錯」開頭糾正迷思"
}

## 嚴格的「有根據生成」規則
- 只根據證據輸入撰寫，嚴禁編造具體藥物名稱、確切篩檢年齡、百分比數字、劑量。
- 不得把「易感/風險升高」說成「一定會生病」；語氣溫和、不製造焦慮。
- 不要生成 academic_summary 或任何證據分數——那些保留機器值。
- 辟謠的「真相」必須符合主流醫學共識，不誇大。

## 寫入方式
- 把所有結果「合併」進 data/processed/bulk_narratives.json（key = 基因符號），
  每完成約 100 個就寫檔一次，累積合併。
- bulk_narratives.json 裡「已存在」的基因一律跳過（斷點續跑，重跑不會重做）。

## 完成後回報
- 補了多少個、剩多少個、寫入哪個檔案。
- 抽 3 個範例（一個高星、一個中星、一個低星）貼給我看，供我審核品質。
```

---

## 補疾病中文名（後續批次，僅在早期資料缺此欄位時才需要）

早期生成的敘事可能缺 `disease_chinese_name`。若需單獨補齊，
用 `python -m pipeline.generate_narratives --disease-names-only`，或貼下面這段：

### 複製區（補疾病中文名用）
```
你是生物醫學翻譯專家。請把英文疾病名稱翻譯成簡體中文疾病名稱。

任務：
1. 讀取 data/processed/bulk_narratives.json（以基因符號為 key 的物件）。
2. 找出所有「缺少 disease_chinese_name 欄位」的條目。
3. 對每一條，把它的英文疾病名（data/processed/bulk_associations.json 對應基因的 disease.name）翻譯成簡體中文。
4. 把翻譯結果寫回該條目的 disease_chinese_name 欄位，分批存檔、斷點續跑。

翻譯規則：
- 專有名詞（人名、地名，如 Alport、Bethlem、Angelman）保留原樣或通行音譯。
- 疾病類型詞：syndrome→综合征、deficiency→缺乏症、dystrophy→营养不良、cardiomyopathy→心肌病、
  myopathy→肌病、anemia→贫血、ataxia→共济失调、epilepsy→癫痫、dysplasia→发育不良、
  deafness→耳聋、immunodeficiency→免疫缺陷、susceptibility→易感性、disease→病、disorder→障碍。
- 尾部「type N」翻成「N 型」。

完成後回報補了多少個、剩多少個未補。
```

---

## 變更語言
- 想改成**繁體中文**：把指令裡的「簡體中文」改成「繁體中文」。
  注意：目前專案既有的 20 個精選基因是簡體，改成繁體會造成不一致。

## 備註
- 生成結果 `bulk_narratives.json` 是本地產物（約 3-4MB），可提交也可不提交。
- 生成後可請助手檢查品質（JSON 完整性、是否有編造藥物/年齡/百分比、是否製造焦慮、語言一致性）。
