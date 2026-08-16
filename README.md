# 🧬 DecodeGene (解码基因)

### 面向大众与科研人员的开源基因-健康知识图谱与智能科普平台
### An open-source, consumer-friendly gene-disease knowledge graph & AI health intelligence platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](https://vitejs.dev)
[![DeepSeek Enabled](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://deepseek.com)
[![Tests](https://github.com/tkarnatar/DecodeGene/actions/workflows/ci.yml/badge.svg)](https://github.com/tkarnatar/DecodeGene/actions)

> **语言 / Language**: 本页面为中英双语。The documentation is bilingual (中文 / English).
> The web app also ships with a one-click **中文 / English** UI switcher.

<div align="center">
  <img src="assets/banner.png" alt="DecodeGene 解码基因" width="100%" />
</div>

---

## 🌟 项目使命 · Our Mission

> **中文**: 传统的生物医学数据库（ClinVar、OMIM、NCBI）充满了晦涩的专业术语（如 *Heterozygous frameshift*、*Incomplete penetrance*），普通大众拿到基因检测报告或看到家族病史时，往往感到无助与焦虑。**DecodeGene** 致力于打破知识壁垒，将权威科学数据通过 **生动比喻、交互式图谱、白话文报告翻译、生活预防指南** 与 **DeepSeek AI 助手**，转化为普通人一看就懂的健康常识。

> **English**: Traditional biomedical databases (ClinVar, OMIM, NCBI) are full of impenetrable jargon (*heterozygous frameshift*, *incomplete penetrance*). When ordinary people receive a genetic test report or see a family history, they often feel helpless and anxious. **DecodeGene** breaks down that wall — turning authoritative scientific data into plain language through **vivid metaphors, interactive visualizations, a plain-language report translator, lifestyle prevention guides**, and a **DeepSeek AI assistant**.

---

## ✨ 核心功能 · Core Features

| 功能 Feature | 说明 Description |
| :--- | :--- |
| 🗣️ **白话文比喻** Visual Metaphor Engine | 把分子机制翻译成生活画面（如 BRCA1 = "DNA 汽车维修工"）。Turns molecular mechanisms into everyday images (BRCA1 = "the DNA car mechanic"). |
| 📄 **报告翻译机** Report Decoder | 粘贴检测报告，自动给出客观解读、风险对比与行动指南。Paste a report, get an objective explanation, risk comparison and action plan. |
| 🩺 **就医提问清单** Doctor Checklist | 一键生成《门诊就医提问卡》，可复制到微信或打印。Generate a clinic question card you can copy or print. |
| 🧬 **家族遗传模拟器** Family Simulator | 选择遗传模式与父母状态，动态推算下一代患病概率。Pick an inheritance pattern and parental status to estimate offspring risk. |
| 🛡️ **预防指南** Prevention Advice | 权威筛查年龄、体检项目与生活方式红黑榜。Screening ages, checkups and lifestyle do's & don'ts. |
| ❌ **谣言粉碎机** Myth Buster | 破除"天赋基因""突变必病"等伪科学。Debunk pseudoscience like "talent genes" and "mutation = doom". |
| 🤖 **AI 问医生** AI Assistant | DeepSeek 驱动的白话文问答与报告翻译（可选）。DeepSeek-powered plain-language Q&A and report translation (optional). |
| 🌐 **中英双语** Bilingual UI | 前端一键切换 中文 / English。One-click UI language switch. |

---

## 🚀 快速开始 · Quick Start

### 环境要求 · Requirements
- Python 3.10+
- Node.js 18+（前端 Frontend）

### 后端 · Backend

```bash
# 中文 / English
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

pip install -r backend/requirements.txt

# 从项目根目录启动 (from repo root)
uvicorn backend.app.main:app --reload
# 或 (or) 进入 backend 目录: uvicorn app.main:app --reload
```

### 前端 · Frontend

```bash
cd frontend
npm install
npm run dev
# 打开 Open http://localhost:5173
```

### 一键启动 · One-command launcher

```bash
python run_dev.py            # 同时启动后端 + 前端 (starts both)
python run_dev.py --backend-only
python run_dev.py --frontend-only
```

### 可选：启用 AI · Optional: enable DeepSeek AI

```bash
# 复制并填写 API Key (copy & fill in your key)
cp backend/.env.example backend/.env   # 编辑 DEEPSEEK_API_KEY
```

> 不配置 Key 也能运行，AI 功能会自动降级为本地模板回答。Without a key, AI features fall back to local template answers.

---

## 🧪 测试 · Tests

```bash
pip install pytest
pytest tests -q
```

---

## 🏗️ 目录结构 · Project Structure

```text
DecodeGene/
├── data/                       # 离线数据 (offline data)
│   ├── sample/                 # 精选样本数据集 (curated sample dataset)
│   └── processed/              # 管道生成的知识库 (pipeline output)
├── pipeline/                   # 数据摄取与清洗管道 (data pipeline)
│   ├── apis/                   # Open Targets / ClinVar API 适配器
│   └── parsers/                # 标准化与通俗化打标 (metaphor library)
├── backend/                    # FastAPI 后端
│   └── app/
│       ├── api/v1/             # REST 接口 (genes, search, checklist, AI…)
│       ├── services/           # 遗传概率计算器、清单生成、AI 智能体
│       ├── models/             # Pydantic 数据模型
│       └── core/               # 配置、知识库、拼音检索
├── frontend/                   # React + Vite 前端 (bilingual UI)
├── tests/                      # pytest 自动化测试
├── docs/                       # 项目规划、数据源手册、执行蓝图
└── run_dev.py                  # 一键启动脚本
```

---

## 📊 数据与扩展 · Data & How to Expand

DecodeGene 内置一个**精心筛选的示例知识库**（当前 **20 个基因**，每个含通俗比喻、科研证据、筛查建议、就医清单与辟谣卡）。This is a **curated sample**, not exhaustive.

### 目前收录的基因 · Currently included genes

**遗传性肿瘤综合征 Hereditary cancer syndromes**: `BRCA1` `BRCA2` `TP53` `PALB2` `MLH1` `APC` `RET` `EGFR`

**神经/代谢/血液等单基因病 Neuro / metabolic / blood disorders**: `APOE` `CFTR` `G6PD` `MTHFR` `HFE` `HBB` `SMN1` `DMD` `PAH`

**心血管与用药个体化 Cardiovascular & pharmacogenomics**: `LDLR` `ALDH2` `CYP2C19`

### 如何扩充 · How to expand

1. **手工精选（推荐，保证通俗质量）** Curated (recommended, best plain-language quality):
   在 `pipeline/parsers/metaphors.py` 的 `EXTRA_ASSOCIATIONS` 里添加新基因条目，然后重新生成数据。
   Add a new entry in `EXTRA_ASSOCIATIONS`, then re-run the pipeline.

2. **实时批量（拉取权威评分）** Bulk live enrichment:
   ```bash
   python -m pipeline.run_pipeline --live
   ```
   该命令会为所有已收录基因拉取 Open Targets 关联分与 ClinVar 致病性数据。
   Fetches Open Targets scores + ClinVar pathogenicity for every included gene.

3. **大规模自动化（数千基因）** Large-scale automated ingestion:
   参见 `docs/data_sources.md`，可下载 ClinVar `variant_summary.txt.gz`、GenCC TSV、HPO 注释等全量数据并批量入库（自动打分），再由人工/ AI 补充通俗比喻。
   See `docs/data_sources.md` — bulk-import ClinVar / GenCC / HPO dumps, auto-scored, then enrich metaphors manually or with AI.

---

## 🤝 参与贡献 · Contributing

我们欢迎任何形式的贡献（代码、翻译、数据、文档）！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

Contributions of all kinds are welcome (code, translations, data, docs)! See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## ⚠️ 免责声明与伦理准则 · Medical Disclaimer

> **中文**: DecodeGene 仅供**科学普及、学术研究与健康常识参考**，不能替代专业医师、临床遗传咨询师的临床诊断和医疗决策。涉及任何实际医疗、用药或检测决策，请务必咨询具有执业资质的专业医务人员。

> **English**: DecodeGene is for **educational and research purposes only** and is not a substitute for professional medical diagnosis or treatment. For any real medical, medication, or testing decision, always consult a licensed healthcare professional or genetic counselor.

---

## 📄 许可证 · License

本项目采用 [MIT License](LICENSE)。Licensed under the [MIT License](LICENSE).
