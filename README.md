🌐 [English](README.md) · [中文](README.zh-CN.md)

# 🧬 DecodeGene

### An open-source, consumer-friendly gene-disease knowledge graph & AI health intelligence platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](https://vitejs.dev)
[![DeepSeek Enabled](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://deepseek.com)
[![Tests](https://github.com/tkarnatar/DecodeGene/actions/workflows/ci.yml/badge.svg)](https://github.com/tkarnatar/DecodeGene/actions)

<div align="center">
  <img src="assets/banner.png" alt="DecodeGene banner" width="100%" />
</div>

> The web app ships with a one-click **中文 / English** UI switcher.

---

## 🌟 Our Mission

Traditional biomedical databases (ClinVar, OMIM, NCBI) are full of impenetrable jargon (*heterozygous frameshift*, *incomplete penetrance*). When ordinary people receive a genetic test report or see a family history, they often feel helpless and anxious. **DecodeGene** breaks down that wall — turning authoritative scientific data into plain language through **vivid metaphors, interactive visualizations, a plain-language report translator, lifestyle prevention guides**, and a **DeepSeek AI assistant**.

---

## ✨ Core Features

| Feature | Description |
| :--- | :--- |
| 🗣️ **Visual Metaphor Engine** | Turns molecular mechanisms into everyday images (e.g. BRCA1 = "the DNA car mechanic"). |
| 📄 **Report Decoder** | Paste a test report and get an objective explanation, risk comparison and action plan. |
| 🩺 **Doctor Checklist** | Generate a clinic question card you can copy or print. |
| 🧬 **Family Inheritance Simulator** | Pick an inheritance pattern and parental status to estimate offspring risk. |
| 🛡️ **Prevention Advice** | Evidence-based screening ages, checkups and lifestyle do's & don'ts. |
| ❌ **Myth Buster** | Debunks pseudoscience like "talent genes" and "mutation = doom". |
| 🤖 **AI Assistant** | DeepSeek-powered plain-language Q&A and report translation (optional). |
| 🌐 **Bilingual UI** | One-click **中文 / English** UI language switch. |

---

## 🚀 Quick Start

### Requirements
- Python 3.10+
- Node.js 18+ (frontend)

### Backend

```bash
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

pip install -r backend/requirements.txt

# from the repo root
uvicorn backend.app.main:app --reload
# or: cd backend && uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

### One-command launcher

```bash
python run_dev.py            # starts both backend + frontend
python run_dev.py --backend-only
python run_dev.py --frontend-only
```

### Optional: enable the DeepSeek AI

```bash
cp backend/.env.example backend/.env   # fill in DEEPSEEK_API_KEY
```

> Without a key the app still works — AI features fall back to local template answers.

---

## 🧪 Tests

```bash
pip install pytest
pytest tests -q
```

---

## 🏗️ Project Structure

```text
DecodeGene/
├── data/                       # offline data
│   ├── sample/                 # curated sample dataset
│   └── processed/              # pipeline output
├── pipeline/                   # data ingestion pipeline
│   ├── apis/                   # Open Targets / ClinVar adapters
│   └── parsers/                # normalization + metaphor library
├── backend/                    # FastAPI backend
│   └── app/
│       ├── api/v1/             # REST endpoints (genes, search, checklist, AI…)
│       ├── services/           # inheritance calculator, checklist, AI agent
│       ├── models/             # Pydantic schemas
│       └── core/               # config, knowledge base, pinyin search
├── frontend/                   # React + Vite (bilingual UI)
├── tests/                      # pytest suite
├── docs/                       # project plan, data sources, execution blueprint
└── run_dev.py                  # one-command launcher
```

---

## 📊 Data & How to Expand

DecodeGene ships with two layers of data:

- **20 curated genes** — each with a plain-language metaphor, evidence, screening advice, a doctor checklist and a myth-buster card.
- **8,700+ bulk genes** — auto-imported from the ClinVar full dump, with gene symbol, disease name and pathogenicity evidence (for Expert Mode).

### Curated genes (with metaphors)

**Hereditary cancer syndromes**: `BRCA1` `BRCA2` `TP53` `PALB2` `MLH1` `APC` `RET` `EGFR`

**Neuro / metabolic / blood disorders**: `APOE` `CFTR` `G6PD` `MTHFR` `HFE` `HBB` `SMN1` `DMD` `PAH`

**Cardiovascular & pharmacogenomics**: `LDLR` `ALDH2` `CYP2C19`

### How to expand

1. **Curated (recommended, best plain-language quality):** add a new entry in `pipeline/parsers/metaphors.py` (`METAPHORS` + `EXTRA_ASSOCIATIONS`), then re-run the pipeline.
2. **Bulk import from ClinVar:** `python -m pipeline.run_pipeline --bulk` downloads the ClinVar `variant_summary.txt.gz` and generates thousands of gene-disease associations (with `--max-genes` to cap the count).
3. **Bulk live enrichment:** `python -m pipeline.run_pipeline --live` fetches Open Targets scores + ClinVar pathogenicity for every curated gene.
4. **Large-scale automated ingestion:** see `docs/data_sources.md` — bulk-import ClinVar / GenCC / HPO dumps (auto-scored), then enrich metaphors manually or with AI.

---

## 🤝 Contributing

Contributions of all kinds are welcome (code, translations, data, docs)! See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## ⚠️ Medical Disclaimer

DecodeGene is for **educational and research purposes only** and is not a substitute for professional medical diagnosis or treatment. For any real medical, medication, or testing decision, always consult a licensed healthcare professional or genetic counselor.

---

## 📄 License

Licensed under the [MIT License](LICENSE).
