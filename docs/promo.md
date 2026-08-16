# 📣 推廣文案 Promo Copy

> 中英文貼文草稿，可直接複製到 Reddit / Hacker News / PTT / Dcard。

---

## English — Show HN / Reddit (r/bioinformatics, r/genetics, r/SideProject)

**Title:** Show HN: DecodeGene — an open-source platform that makes genetic reports understandable

**Body:**

Traditional genetic databases (ClinVar, OMIM) are full of jargon like *heterozygous frameshift* and *incomplete penetrance*. When ordinary people get a genetic test report, they often feel lost and anxious.

I built DecodeGene to fix that: it turns **8,700+ gene-disease associations** into plain-language explanations using everyday metaphors ("BRCA1 is the DNA car mechanic").

What it does:
- 📄 **Report translator** — paste a variant (e.g. `BRCA1 c.5266dupC, Pathogenic`) → plain-language explanation + concrete next steps
- 🧬 **Family inheritance simulator** — pick AD/AR/X-linked + parent status → offspring risk %
- 🩺 **Doctor checklist generator** — a printable list of questions to ask at the clinic
- ❌ **Myth buster** — debunks "talent genes" and "mutation = doom"
- 🌐 **Bilingual** — full EN / 中文 UI switch

**Tech:** FastAPI + React/Vite, data auto-imported from ClinVar (8,710 genes) + 20 hand-curated genes, optional DeepSeek AI (works offline without a key).

- Demo: https://decodegene.onrender.com
- Repo: https://github.com/tkarnatar/DecodeGene

Everything (code + data + narratives) is open under MIT. Feedback is very welcome — especially from geneticists / bioinformaticians on the medical accuracy of the plain-language summaries.

---

## 中文 — PTT (Soft_Job) / Dcard / 巴哈姆特

**標題：**【分享】DecodeGene — 把基因檢測報告變成人人都看得懂的開源平台

**內文：**

基因資料庫（ClinVar、OMIM）充滿了「雜合移碼突變」「不完全外顯率」這種天書。普通人拿到基因檢測報告，常常又慌又無助。

我做了 DecodeGene，把 **8,700 多個基因-疾病關聯**用生活比喻翻譯成白話（BRCA1 = 細胞裡的 DNA 汽車維修工）。

功能：
- 📄 報告翻譯機：貼上突變位點 → 白話解釋 + 下一步該做什麼
- 🧬 家族遺傳模擬器：選顯性/隱性/X連鎖 → 下一代患病機率
- 🩺 就醫提問清單：生成一份可印出來問醫生的清單
- ❌ 謠言粉碎機：破解「天賦基因」「測出突變=死定了」等迷思
- 🌐 中英雙語切換

技術：FastAPI + React/Vite，資料自動從 ClinVar 匯入（8,710 個基因）+ 20 個手工精選基因，可選接 DeepSeek AI（沒 Key 也能離線跑）。

- Demo：https://decodegene.onrender.com
- 開源（MIT）：https://github.com/tkarnatar/DecodeGene

歡迎回饋，尤其是醫護/生醫背景的朋友，幫我看看白話解釋的醫學準確度。

---

## 附註 Notes

- Demo 在 Render 免費層，**閒置 15 分鐘會休眠**，首次開啟要等 30-60 秒。貼文裡可加一句提醒訪客「若首次載入慢，請稍等或重新整理」。
- 發文時建議附 1-2 張截圖（首頁 + 報告翻譯機）。
