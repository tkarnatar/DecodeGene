# 🤖 DeepSeek V4 Flash — English Narrative Generation Prompt

> 用途：為批量基因補寫**英文**白話敘事，讓前端切到 English 時也看得到英文比喻/摘要/建議。
> 生成結果存為 `data/processed/bulk_narratives_en.json`（以基因符號為 key）。

## 複製區（整段貼給 Flash）

```
You are a senior clinical genetic counselor and top genetics science writer for the DecodeGene project.
Write plain-language English narratives for bulk genes that are missing English narratives.

## Setup (read these files first)
1. data/processed/bulk_associations.json — an array of ~8710 genes; each entry has
   gene.symbol, disease.name, evidence.clinvar_pathogenic_count, evidence.star_rating, disease.severity_badge.
2. data/processed/bulk_narratives_en.json — a JSON object keyed by gene symbol (may not exist yet or be partial).
   These are the "already done" entries — SKIP them.

## Task
For every gene NOT present in bulk_narratives_en.json, sorted by evidence.clinvar_pathogenic_count descending,
produce one JSON object with these fields (all in English):
{
  "metaphor_title": "A vivid everyday-life metaphor title, starting with one emoji, e.g. '🧬 The DNA repair mechanic'",
  "metaphor_story": "A metaphor story, 3-5 sentences, explaining the gene's function and what happens when it mutates",
  "plain_summary": "A plain-language summary, 2-3 sentences, explaining the real-world meaning of carrying a mutation",
  "screening_advice": "Screening advice in safe wording (e.g. 'Consult a specialist to develop a personalized screening plan'), no fabricated ages or tests",
  "lifestyle_tips": ["Lifestyle tip 1", "Lifestyle tip 2", "Lifestyle tip 3"],
  "key_questions": ["Question to ask your doctor 1", "Question 2", "Question 3"],
  "myth": "A common misconception as a quoted question",
  "truth": "The scientific truth, starting with 'No,' or 'Not true,'"
}

## Grounded-generation rules (critical)
- Write ONLY from the provided evidence; never invent information not in it.
- Never fabricate specific drug names, exact screening ages, percentages, or dosages.
- Never turn "increased susceptibility / elevated risk" into "will definitely get the disease"; keep the tone warm and non-alarming.
- Do not generate academic summaries or evidence scores (those stay machine-derived).
- The "truth" must align with mainstream medical consensus; do not exaggerate.

## Writing
- Merge all results into data/processed/bulk_narratives_en.json (key = gene symbol),
  saving every ~100 genes, accumulating into the same file.
- Skip any gene already present in bulk_narratives_en.json (resumable).

## When done
- Report: how many completed, how many remaining, and the output file path.
- Paste 3 samples (one high-star, one mid-star, one low-star) for quality review.
```

---

## 備註
- 英文敘事與中文敘事分開存放（`bulk_narratives_en.json`），互不影響。
- 前端切到 English 時會優先顯示英文敘事，缺英文的基因回退到中文/英文疾病名。
- 產出後可請助手檢查品質（編造、焦慮措辭、一致性）。
