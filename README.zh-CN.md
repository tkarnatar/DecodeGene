🌐 [English](README.md) · [中文](README.zh-CN.md)

# 🧬 DecodeGene (解码基因)

### 面向大众与科研人员的开源基因-健康知识图谱与智能科普平台

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](https://vitejs.dev)
[![DeepSeek Enabled](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://deepseek.com)
[![Tests](https://github.com/tkarnatar/DecodeGene/actions/workflows/ci.yml/badge.svg)](https://github.com/tkarnatar/DecodeGene/actions)

<div align="center">
  <img src="assets/banner.png" alt="DecodeGene 解码基因" width="100%" />
</div>

> 前端内建一键 **中文 / English** 界面切换。

---

## 🌟 项目使命

传统的生物医学数据库（ClinVar、OMIM、NCBI）充满了晦涩的专业术语（如 *Heterozygous frameshift*、*Incomplete penetrance*），普通大众拿到基因检测报告或看到家族病史时，往往感到无助与焦虑。**DecodeGene** 致力于打破知识壁垒，将权威科学数据通过 **生动比喻、交互式图谱、白话文报告翻译、生活预防指南** 与 **DeepSeek AI 助手**，转化为普通人一看就懂的健康常识。

---

## ✨ 核心功能

| 功能 | 说明 |
| :--- | :--- |
| 🗣️ **白话文比喻引擎** | 把分子机制翻译成生活画面（如 BRCA1 = "DNA 汽车维修工"）。 |
| 📄 **报告翻译机** | 粘贴检测报告，自动给出客观解读、风险对比与行动指南。 |
| 🩺 **就医提问清单** | 一键生成《门诊就医提问卡》，可复制到微信或打印。 |
| 🧬 **家族遗传模拟器** | 选择遗传模式与父母状态，动态推算下一代患病概率。 |
| 🛡️ **预防指南** | 权威筛查年龄、体检项目与生活方式红黑榜。 |
| ❌ **谣言粉碎机** | 破除"天赋基因""突变必病"等伪科学。 |
| 🤖 **AI 问医生** | DeepSeek 驱动的白话文问答与报告翻译（可选）。 |
| 🌐 **中英双语界面** | 一键切换 中文 / English。 |

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+（前端）

### 后端

```bash
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

pip install -r backend/requirements.txt

# 从项目根目录启动
uvicorn backend.app.main:app --reload
# 或：cd backend && uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
# 打开 http://localhost:5173
```

### 一键启动

```bash
python run_dev.py            # 同时启动后端 + 前端
python run_dev.py --backend-only
python run_dev.py --frontend-only
```

### 可选：启用 DeepSeek AI

```bash
cp backend/.env.example backend/.env   # 填入 DEEPSEEK_API_KEY
```

> 不配置 Key 也能运行，AI 功能会自动降级为本地模板回答。

---

## 🧪 测试

```bash
pip install pytest
pytest tests -q
```

---

## 🏗️ 目录结构

```text
DecodeGene/
├── data/                       # 离线数据
│   ├── sample/                 # 精选样本数据集
│   └── processed/              # 管道生成的知识库
├── pipeline/                   # 数据摄取管道
│   ├── apis/                   # Open Targets / ClinVar 适配器
│   └── parsers/                # 标准化与通俗比喻库
├── backend/                    # FastAPI 后端
│   └── app/
│       ├── api/v1/             # REST 接口 (genes, search, checklist, AI…)
│       ├── services/           # 遗传概率计算器、清单生成、AI 智能体
│       ├── models/             # Pydantic 数据模型
│       └── core/               # 配置、知识库、拼音检索
├── frontend/                   # React + Vite 前端 (双语界面)
├── tests/                      # pytest 自动化测试
├── docs/                       # 项目规划、数据源手册、执行蓝图
└── run_dev.py                  # 一键启动脚本
```

---

## 📊 数据与扩展

DecodeGene 内置两层数据：

- **20 个精选基因** —— 每个含通俗比喻、科研证据、筛查建议、就医清单与辟谣卡。
- **8700+ 个批量基因** —— 从 ClinVar 全量 dump 自动导入，含基因符号、疾病名与致病性证据（供专业模式使用）。

### 精选基因（含比喻）

**遗传性肿瘤综合征**：`BRCA1` `BRCA2` `TP53` `PALB2` `MLH1` `APC` `RET` `EGFR`

**神经/代谢/血液等单基因病**：`APOE` `CFTR` `G6PD` `MTHFR` `HFE` `HBB` `SMN1` `DMD` `PAH`

**心血管与用药个体化**：`LDLR` `ALDH2` `CYP2C19`

### 如何扩充

1. **手工精选（推荐，保通俗质量）**：在 `pipeline/parsers/metaphors.py`（`METAPHORS` + `EXTRA_ASSOCIATIONS`）添加新条目，然后重新运行管道。
2. **批量导入 ClinVar**：`python -m pipeline.run_pipeline --bulk` 下载 ClinVar `variant_summary.txt.gz` 并生成数千条基因-疾病关联（可用 `--max-genes` 限制数量）。
3. **实时批量**：`python -m pipeline.run_pipeline --live` 为所有精选基因拉取 Open Targets 关联分与 ClinVar 致病性数据。
4. **大规模自动化**：参见 `docs/data_sources.md`，批量导入 ClinVar / GenCC / HPO 全量数据（自动打分），再由人工或 AI 补充通俗比喻。

---

## 🤝 参与贡献

欢迎任何形式的贡献（代码、翻译、数据、文档）！请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) 与 [CODE_OF_CONDUCT.zh-CN.md](CODE_OF_CONDUCT.zh-CN.md)。

---

## ⚠️ 免责声明

DecodeGene 仅供**科学普及、学术研究与健康常识参考**，不能替代专业医师、临床遗传咨询师的临床诊断和医疗决策。涉及任何实际医疗、用药或检测决策，请务必咨询具有执业资质的专业医务人员。

---

## 📄 许可证

本项目采用 [MIT License](LICENSE)。
