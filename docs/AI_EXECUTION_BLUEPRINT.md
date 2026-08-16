# 🤖 OpenCode Go / DeepSeek v4 Pro & Flash 执行蓝图与分步指令集 (大众科普增强版)
### AI Agent Step-by-Step Implementation Blueprint for DecodeGene

> **说明**: 本蓝图专为 **OpenCode Go**（搭载 **DeepSeek v4 Pro** 或 **DeepSeek v4 Flash**）设计。
> 已经过针对**普通大众受众**的全面优化，包含**白话文翻译机、就诊提问清单、生活比喻引擎、家族遗传模拟器**等模块。

---

## 🎯 模型推荐分配

- **DeepSeek v4 Pro**: 负责 **Task 1 (数据模型与通俗化字典)**、**Task 3 (后端业务逻辑与遗传算法)**、**Task 5 (AI 医学通俗化推理与报告翻译 Agent)**。
- **DeepSeek v4 Flash**: 负责 **Task 2 (数据 API 管道)**、**Task 4 (交互前端、比喻卡片与就医清单 UI)**、**Task 6 (谣言粉碎机数据与自动化测试)**。

---

## 📋 模块化任务拆解与 Prompt 清单

### 📌 Task 1: 基础工程与大众化数据模型 (Pydantic Schema)
**推荐模型**: `DeepSeek v4 Pro`

```markdown
### Prompt for Task 1:

你是生物医学与 Python 后端专家。请为面向大众的开源项目 DecodeGene 初始化基础架构。

【需求】:
1. 在 `backend/` 目录下创建 `requirements.txt`:
   - fastapi, uvicorn, pydantic>=2.0, duckdb, httpx, aiohttp, rich, python-dotenv, pytest
2. 创建 `backend/app/core/config.py`:
   - 读取 DEEPSEEK_API_KEY, DATA_DIR, LOG_LEVEL 等配置。
3. 创建 `backend/app/models/schema.py`，定义支持【通俗模式】与【专业模式】的 Pydantic 模型：
   - `GeneEntity`: (symbol, name, chinese_name, chromosome, metaphor_title, metaphor_story, plain_summary, academic_summary)
   - `DiseaseEntity`: (id, name, chinese_name, category, severity_level, common_symptoms)
   - `GeneticReportQuery`: (raw_text, detected_gene, detected_variant, zygosity)
   - `DoctorChecklist`: (gene_symbol, disease_name, recommended_specialty, key_questions, screening_tests)
   - `FamilyInheritanceQuery`: (pattern, father_status, mother_status)
   - `FamilyInheritanceResult`: (child_disease_risk_pct, child_carrier_risk_pct, plain_explanation)
   - `GeneDiseaseAssociation`: 包含双模数据（专业评分 vs 通俗星级与生活建议）。
4. 在 `backend/app/models/__init__.py` 导出以上模型。

请直接输出所有文件的完整高质量 Python 代码。
```

---

### 📌 Task 2: 数据摄取管道与中英通俗化字典映射
**推荐模型**: `DeepSeek v4 Flash`

```markdown
### Prompt for Task 2:

请为 DecodeGene 编写数据摄取与通俗化标注管道。

【需求】:
1. 在 `pipeline/apis/opentargets.py`:
   - 异步从 Open Targets GraphQL 拉取靶点-疾病关联分。
2. 在 `pipeline/apis/clinvar.py`:
   - 从 ClinVar E-utilities 查询变异致病性，并将 Pathogenic 自动映射为中文通俗标签：`⚠️ 明确风险变异 (需关注)`，Benign 映射为 `✅ 良性变异 (无需担心)`，VUS 映射为 `❓ 意义未明变异 (持续研究中)`。
3. 在 `pipeline/parsers/metaphors.py`:
   - 内置常见高频基因的生动生活比喻库（如 BRCA1: 细胞里的 DNA 汽车维修工；TP53: 紧急制动刹车片；APOE: 大脑垃圾清运车；CFTR: 细胞黏液水龙头调节器）。
4. 在 `pipeline/run_pipeline.py`:
   - 一键生成包含通俗解释与科研证据的 `data/processed/sample_associations.json`。

请输出完整 Python 代码。
```

---

### 📌 Task 3: 后端核心业务、遗传概率计算器与 REST 接口
**推荐模型**: `DeepSeek v4 Pro`

```markdown
### Prompt for Task 3:

请为 DecodeGene 实现支持大众科普与就医辅导的 FastAPI 后端。

【需求】:
1. 在 `backend/app/services/inheritance.py` 实现 `InheritanceCalculator`:
   - 支持常染色体显性 (AD)、隐性 (AR)、X连锁隐性 (XR) 遗传概率计算，输出子女患病/携带百分比及白话文解析。
2. 在 `backend/app/services/checklist.py` 实现 `ChecklistService`:
   - 根据基因与疾病，自动生成面向临床医生的《门诊就医提问清单》与筛查建议。
3. 在 `backend/app/core/database.py` 实现 DuckDB/SQLite 检索，支持中文疾病名、基因别名、拼音首字母模糊匹配。
4. 在 `backend/app/api/v1/` 实现路由：
   - `GET /api/v1/genes/{symbol}` (支持 ?view=simple 或 ?view=pro)
   - `GET /api/v1/search?q={query}` (即时联想，返回通俗中文标签)
   - `POST /api/v1/calculate/inheritance` (计算家族遗传概率)
   - `GET /api/v1/checklist/{gene_symbol}` (生成就医清单)
   - `GET /api/v1/myths` (返回热门基因谣言与科学辟谣清单)
5. 在 `backend/app/main.py` 整合并配置 CORS。

请输出完整代码。
```

---

### 📌 Task 4: React + Vite 大众友好型前端与可视化组件
**推荐模型**: `DeepSeek v4 Flash`

```markdown
### Prompt for Task 4:

请为 DecodeGene 搭建普通大众一目了然的现代化 Web 前端。

【页面与组件规范】:
1. 顶部模式切换开关：`【🌱 小白通俗模式】 ⇄ 【🔬 专业科研模式】`。
2. `frontend/src/components/MetaphorCard.jsx`:
   - 用生动插画/图标展示基因的生活化比喻（如“汽车维修工”故事）。
3. `frontend/src/components/ReportDecoder.jsx`:
   - 基因检测报告粘贴框，输入后立即展示客观解读、安抚提示、风险对比柱状图与行动指南。
4. `frontend/src/components/DoctorChecklistModal.jsx`:
   - 弹出精美可打印/一键复制到微信的《门诊提问清单》。
5. `frontend/src/components/FamilySimulator.jsx`:
   - 图形化交互家族树，拖拽或勾选父母状态，动态显示下一代患病概率动画。
6. `frontend/src/components/MythBusterSection.jsx`:
   - 辟谣卡片网格（“天赋基因是真的吗？”等）。
7. `frontend/src/App.jsx` 与 `frontend/src/index.css`:
   - 医疗薄荷绿与深海蓝配色，大字体，高对比度，防焦虑温情提示。

请输出完整的前端代码。
```

---

### 📌 Task 5: DeepSeek 原生驱动的“报告白话文翻译”与“问医生”AI 智能体
**推荐模型**: `DeepSeek v4 Pro`

```markdown
### Prompt for Task 5:

请为 DecodeGene 实现基于 DeepSeek 的大众基因科普与心理安抚 AI Agent。

【核心要求】:
1. 在 `backend/app/services/ai_reasoning.py` 实现 `DeepSeekPublicAgent`:
   - 支持 DeepSeek API (`deepseek-chat` / `deepseek-reasoner`)。
   - 系统级 Prompt 设定：你是一名资深临床遗传咨询师与顶级科普专家。你的语气应当**温和、客观、极其通俗，严禁使用未加解释的晦涩术语，坚决避免引发用户的基因焦虑**。
2. 核心功能 1: 基因检测报告自然语言翻译 (`explain_report`)：
   - 结构化输出：① 到底测出了什么？ ② 会对我造成什么实际影响？ ③ 接下来我该去医院做什么？ ④ 日常生活该怎么吃、怎么动？
3. 核心功能 2: 患者答疑聊天机器人 (`chat_qa`)：
   - 支持流式输出 (SSE)。
4. 严格强制附加医疗免责声明与医院就诊指引。

请输出完整代码。
```

---

### 📌 Task 6: 自动化测试与一键启动脚本
**推荐模型**: `DeepSeek v4 Flash`

```markdown
### Prompt for Task 6:

请为 DecodeGene 编写测试用例与启动脚本。

【需求】:
1. 编写 pytest 自动化测试：
   - 测试家族遗传概率计算器的显性/隐性算式正确性。
   - 测试就诊提问清单生成逻辑。
   - 测试搜索模糊匹配与拼音检索。
2. 编写根目录 `run_dev.py` 或启动脚本，一键拉起后端与前端。

请输出完整代码。
```
