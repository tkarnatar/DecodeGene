# 🤝 贡献指南 · Contributing Guide

> 中文 | English

感谢你对 **DecodeGene** 的关注！我们欢迎任何形式的贡献。Thank you for your interest in DecodeGene! Contributions of all kinds are welcome.

---

## 🌍 我们需要的贡献 · What we need

| 类型 Type | 说明 Description |
| :--- | :--- |
| 💻 代码 Code | 后端 / 前端 / 管道 / 测试 Bug 修复与新功能。Backend, frontend, pipeline, tests. |
| 🧬 数据 Data | 新增基因-疾病条目、通俗比喻、就医清单、辟谣卡。New gene entries, metaphors, checklists, myths. |
| 🌐 翻译 Translation | 中英双语内容与 UI 翻译。Chinese/English content and UI copy. |
| 📖 文档 Docs | README、教程、数据源手册。Docs and tutorials. |
| 🐛 反馈 Feedback | 提交 Issue 报告 Bug 或提出建议。File issues for bugs and ideas. |

---

## 🚀 快速开始 · Getting Started

```bash
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

# 后端 Backend
pip install -r backend/requirements.txt

# 前端 Frontend
cd frontend && npm install && cd ..

# 测试 Tests
pytest tests -q
```

---

## 🔄 开发流程 · Workflow

1. **Fork** 本仓库 → 克隆到本地。Fork the repo and clone locally.
2. 基于 `main` 创建功能分支。Create a feature branch off `main`:
   ```bash
   git checkout -b feat/my-awesome-change
   ```
3. 提交前运行测试与构建。Run tests and build before committing:
   ```bash
   pytest tests -q
   cd frontend && npm run build
   ```
4. 提交清晰的信息（建议遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)）。Write clear commit messages.
5. 推送到你的 Fork 并提交 **Pull Request**。Push and open a Pull Request.

---

## 🧬 新增一个基因条目 · Adding a gene entry

在 `pipeline/parsers/metaphors.py` 中：

1. 在 `METAPHORS` 字典加入生活比喻（标题 + 故事）。Add a metaphor in `METAPHORS`.
2. 在 `EXTRA_ASSOCIATIONS` 加入完整关联条目（含 `gene` / `disease` / `evidence` / `lifestyle_prevention` / `doctor_checklist` / `myth_buster`）。
3. 在 `pipeline/run_pipeline.py` 的 `ENSEMBL_IDS` 加入该基因的 Ensembl ID（用于实时数据）。
4. 重新生成数据并跑测试：
   ```bash
   python -m pipeline.run_pipeline
   pytest tests -q
   ```

> 内容要求：通俗解释须**准确、温和、不制造焦虑**；科研摘要须有依据。Please keep plain-language content accurate, warm, and anxiety-free.

---

## 🧭 代码风格 · Style

- **Python**: 遵循 [PEP 8](https://peps.python.org/pep-0008/)，使用类型注解，不添加无意义的注释。
- **前端**: 遵循现有组件风格，优先使用函数组件与 Hooks。
- **提交前** 请确保 `pytest` 与 `npm run build` 均通过。

---

## 📄 许可证 · License

贡献即表示你同意将你的代码以 [MIT License](LICENSE) 开源。By contributing you agree to license your work under the [MIT License](LICENSE).
