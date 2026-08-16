🌐 [English](CONTRIBUTING.md) · [中文](CONTRIBUTING.zh-CN.md)

# 🤝 贡献指南

感谢你对 DecodeGene 的关注！我们欢迎任何形式的贡献。

## 我们需要的贡献

| 类型 | 说明 |
| :--- | :--- |
| 💻 代码 | 后端、前端、管道与测试的 Bug 修复和新功能。 |
| 🧬 数据 | 新增基因条目、通俗比喻、就医清单与辟谣卡。 |
| 🌐 翻译 | 中英文内容与 UI 文案。 |
| 📖 文档 | 文档与教程。 |
| 🐛 反馈 | 提交 Issue 报告 Bug 或提出建议。 |

## 快速开始

```bash
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

# 后端
pip install -r backend/requirements.txt

# 前端
cd frontend && npm install && cd ..

# 测试
pytest tests -q
```

## 开发流程

1. Fork 本仓库并克隆到本地。
2. 基于 `main` 创建功能分支：
   ```bash
   git checkout -b feat/my-awesome-change
   ```
3. 提交前运行测试与构建：
   ```bash
   pytest tests -q
   cd frontend && npm run build
   ```
4. 撰写清晰的提交信息（建议遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)）。
5. 推送并提交 Pull Request。

## 新增一个基因条目

在 `pipeline/parsers/metaphors.py` 中：

1. 在 `METAPHORS` 加入生活比喻（标题 + 故事）。
2. 在 `EXTRA_ASSOCIATIONS` 加入完整关联条目（`gene` / `disease` / `evidence` / `lifestyle_prevention` / `doctor_checklist` / `myth_buster`）。
3. 在 `pipeline/run_pipeline.py` 的 `ENSEMBL_IDS` 加入该基因的 Ensembl ID（用于实时数据）。
4. 重新生成数据并运行测试：
   ```bash
   python -m pipeline.run_pipeline
   pytest tests -q
   ```

> 内容要求：通俗解释须**准确、温和、不制造焦虑**；科研摘要须有依据。

## 代码风格

- **Python**：遵循 [PEP 8](https://peps.python.org/pep-0008/)，使用类型注解，避免无意义的注释。
- **前端**：遵循现有组件风格，优先使用函数组件与 Hooks。
- 提交前请确保 `pytest` 与 `npm run build` 均通过。

## 许可证

贡献即表示你同意将你的代码以 [MIT License](LICENSE) 开源。
