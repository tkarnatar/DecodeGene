# 💻 换机执行指南 (Instructions for Other Computer)

当你将本压缩包下载并在另一台电脑上解压后，请按照以下简明步骤操作：

---

## 🛠️ 第一步：用 OpenCode Go 打开工作区
1. 在另一台电脑上，打开 **OpenCode Go**（或 VS Code / Cursor / 终端）。
2. 点击 **File -> Open Folder**（打开文件夹），选择解压后的 `DecodeGene` 根目录。

---

## 🤖 第二步：启动 DeepSeek v4 Pro / Flash 执行代码生成
1. 在编辑器中打开文件：[`docs/AI_EXECUTION_BLUEPRINT.md`](docs/AI_EXECUTION_BLUEPRINT.md)。
2. 在 OpenCode Go 的 AI 对话窗口中，切换模型为 **DeepSeek v4 Pro** 或 **DeepSeek v4 Flash**。
3. 按照蓝图指引，**依次将 Task 1 至 Task 6 的 Prompt 复制并发送给 AI**：
   - **Task 1 (DeepSeek v4 Pro)**: 初始化基础架构、配置与 Pydantic 双模数据结构。
   - **Task 2 (DeepSeek v4 Flash)**: 生成 Open Targets/ClinVar API 客户端与数据抓取管道。
   - **Task 3 (DeepSeek v4 Pro)**: 生成 DuckDB 存储引擎、遗传概率计算器与 FastAPI 接口。
   - **Task 4 (DeepSeek v4 Flash)**: 构建 React + Vite 前端、生活比喻卡片、报告翻译机与就医清单 UI。
   - **Task 5 (DeepSeek v4 Pro)**: 构建 DeepSeek RAG 机制解读与心理安抚 Agent。
   - **Task 6 (DeepSeek v4 Flash)**: 编写自动化单元测试与一键启动脚本。

---

## 🚀 第三步：本地测试与运行
代码生成完毕后：
```bash
# 1. 安装后端依赖并运行
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload

# 2. 启动前端界面
cd frontend
npm install
npm run dev
```

---

## 📦 项目核心文件导航
- 📄 `README.md`: 开源项目主页与功能介绍。
- 📋 `docs/PROJECT_PLAN.md`: 完整大众化产品规划与架构设计书。
- 🤖 `docs/AI_EXECUTION_BLUEPRINT.md`: **（最核心）AI 自动化执行指令集**。
- 📊 `docs/data_sources.md`: 全球公开基因数据源与 API 手册。
- 💾 `data/sample/demo_associations.json`: 离线精选示例数据集（含 BRCA1, APOE, EGFR）。
