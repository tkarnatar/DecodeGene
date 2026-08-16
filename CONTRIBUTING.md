🌐 [English](CONTRIBUTING.md) · [中文](CONTRIBUTING.zh-CN.md)

# 🤝 Contributing Guide

Thanks for your interest in DecodeGene! Contributions of all kinds are welcome.

## What we need

| Type | Description |
| :--- | :--- |
| 💻 Code | Backend, frontend, pipeline, and test bug fixes and new features. |
| 🧬 Data | New gene entries, metaphors, doctor checklists, and myth-buster cards. |
| 🌐 Translation | Chinese/English content and UI copy. |
| 📖 Docs | Documentation and tutorials. |
| 🐛 Feedback | File issues for bugs and ideas. |

## Getting started

```bash
git clone https://github.com/tkarnatar/DecodeGene.git
cd DecodeGene

# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && cd ..

# Tests
pytest tests -q
```

## Workflow

1. Fork the repo and clone it locally.
2. Create a feature branch off `main`:
   ```bash
   git checkout -b feat/my-awesome-change
   ```
3. Run tests and build before committing:
   ```bash
   pytest tests -q
   cd frontend && npm run build
   ```
4. Write clear commit messages ([Conventional Commits](https://www.conventionalcommits.org/) recommended).
5. Push and open a Pull Request.

## Adding a gene entry

In `pipeline/parsers/metaphors.py`:

1. Add a metaphor in `METAPHORS` (title + story).
2. Add a full association in `EXTRA_ASSOCIATIONS` (`gene` / `disease` / `evidence` / `lifestyle_prevention` / `doctor_checklist` / `myth_buster`).
3. Add the gene's Ensembl ID to `ENSEMBL_IDS` in `pipeline/run_pipeline.py` (for live data).
4. Regenerate the data and run the tests:
   ```bash
   python -m pipeline.run_pipeline
   pytest tests -q
   ```

> Please keep plain-language content accurate, warm, and anxiety-free; academic summaries should be evidence-based.

## Style

- **Python**: follow [PEP 8](https://peps.python.org/pep-0008/), use type hints, avoid meaningless comments.
- **Frontend**: follow the existing component style; prefer function components and Hooks.
- Ensure `pytest` and `npm run build` pass before submitting.

## License

By contributing you agree to license your work under the [MIT License](LICENSE).
