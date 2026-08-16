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

## 品質升級 Pass（高星基因逐條打磨）

英文敘事全量完成後，中低星基因用「類別模板」即可，但**高證據基因（star ≥ 4）值得逐條打磨成專屬比喻**，與中文版品質看齊。貼下面這段給 Flash：

### 複製區（品質升級用）
```
You are a senior clinical genetic counselor and top genetics science writer.
Upgrade the English narratives for HIGH-EVIDENCE genes in DecodeGene.

## Setup (read first)
1. data/processed/bulk_associations.json — array of ~8710 genes; each has
   gene.symbol, disease.name, evidence.star_rating, evidence.clinvar_pathogenic_count.
2. data/processed/bulk_narratives_en.json — keyed by gene symbol (existing English narratives).

## Task
For every gene with evidence.star_rating >= 4 (about 3070 genes), REWRITE the narrative so it is
UNIQUE and SPECIFIC to that gene's disease — no generic template wording.

How to tell template vs specific:
- TEMPLATE = the story does NOT name the actual disease (says "a condition" / "a disorder" generically, e.g. "linked to a condition whose effects vary from person to person"). REWRITE these.
- SPECIFIC = the story already names the real disease (e.g. "Lynch syndrome", "cystic fibrosis"). SKIP these.

For each gene to rewrite, produce a JSON object (all English):
{
  "metaphor_title": "A unique vivid metaphor tied to THIS gene's function/disease, with one emoji",
  "metaphor_story": "3-5 sentences explaining THIS gene's function and the specific consequence of its mutation, naming the disease and using a concrete everyday analogy",
  "plain_summary": "2-3 sentences on the real-world meaning of carrying THIS mutation",
  "screening_advice": "Safe screening wording tied to THIS condition (no fabricated ages/tests)",
  "lifestyle_tips": ["3 tips relevant to THIS condition"],
  "key_questions": ["3 questions specific to THIS condition"],
  "myth": "A common misconception about THIS specific condition",
  "truth": "The truth, starting with 'No,' or 'Not true,'"
}

## How to be specific (examples)
- "Lynch syndrome" → DNA proofreading / regular colonoscopy, NOT "a condition".
- "cystic fibrosis" → thick mucus blocking airways.
- "hypertrophic cardiomyopathy" → thickened heart muscle.
Ground the metaphor in the ACTUAL disease.name.

## Rules (unchanged)
- No fabricated drug names, ages, percentages, or dosages.
- Never turn "increased risk" into "will definitely get sick"; keep the tone warm.
- Do not generate academic summaries or evidence scores.

## Writing
- Merge results into data/processed/bulk_narratives_en.json (key = gene symbol),
  saving every ~100 genes, resumable (skip genes already upgraded).
- Only touch star_rating >= 4 genes; leave all others unchanged.

## Report
- How many upgraded, how many skipped (already specific), plus 3 samples.
```

---

## 備註
- 英文敘事與中文敘事分開存放（`bulk_narratives_en.json`），互不影響。
- 前端切到 English 時會優先顯示英文敘事，缺英文的基因回退到中文/英文疾病名。
- 產出後可請助手檢查品質（編造、焦慮措辭、一致性）。

