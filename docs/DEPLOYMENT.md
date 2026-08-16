# 🚀 部署指南 · Deployment Guide

> 中文 | English

DecodeGene 打包成**單一容器**（nginx 服務前端 + 反向代理到後端 uvicorn），可一鍵部署到任何 Docker 主機或 Render。The app ships as a single container (nginx serving the frontend + reverse-proxying to the backend), deployable to any Docker host or Render.

---

## 方式 A：Docker（本機或任何主機）

```bash
# 建置並啟動（前端 + 後端 + 資料全部打包）
docker compose up -d --build

# 開啟
# http://localhost:5173
```

### 啟用 AI（可選）
```bash
DEEPSEEK_API_KEY=sk-xxx docker compose up -d
# 或建立 .env 檔案：
#   DEEPSEEK_API_KEY=sk-xxx
#   DEEPSEEK_MODEL=deepseek-chat
```

---

## 方式 B：Render（免費層，一鍵部署）

1. 把專案推到 GitHub（已完成）。
2. 到 [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**。
3. 選擇 `tkarnatar/DecodeGene` 倉庫，Render 會自動讀取根目錄的 `render.yaml`。
4. 在 Environment 裡填 `DEEPSEEK_API_KEY`（可選，留空則用離線降級）。
5. 點 **Deploy**，完成後會得到 `https://decodegene.onrender.com` 網址。

> ⚠️ Render 免費層的 web service **閒置 15 分鐘會休眠**，首次喚醒約需 30-60 秒。

### 健康檢查
- `GET /api/v1/health` → `{"status":"ok", ...}`

---

## 方式 C：本機開發（不需 Docker）

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload

cd frontend && npm install && npm run dev
# 或一鍵：python run_dev.py
```

---

## 架構說明 Architecture

```
Browser
   │
   ▼
nginx (port 80 / $PORT)
   ├── /            → 前端靜態檔 (React build)
   └── /api/*       → uvicorn (backend, port 8000)
```

- 前端 `api.js` 使用相對路徑 `/api/v1`，若前後端分離部署，可用建置環境變數
  `VITE_API_BASE_URL` 指定後端位址（例如部署到 GitHub Pages + 獨立後端時）。

---

## 環境變數 Env Vars

| 變數 | 預設 | 說明 |
| :--- | :--- | :--- |
| `DEEPSEEK_API_KEY` | 空 | DeepSeek API Key（啟用 AI，留空則離線降級） |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | DeepSeek API 位址 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | 模型名稱 |
| `PORT` | `80` | nginx 監聽埠（Render 自動注入） |
