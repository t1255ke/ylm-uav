# 📦 UAV 影片上傳與 3D 模型顯示系統

本專案為前後端分離架構，前端採用 Vue 3（Options API）與 Three.js 建構使用者介面與 3D 模型顯示，後端則使用 FastAPI 處理影片上傳與模型生成，並以 Docker 封裝後端服務，支援跨平台快速部署與開發。

---

## 🚀 快速啟動教學

### ✅ 前置需求

- ✅ 已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- ✅ 已安裝 [Node.js](https://nodejs.org/)（建議 v18+）
- ✅ Windows 用戶可直接使用 `start_backend.bat` 啟動後端

---

### 🔧 1. 啟動後端（FastAPI + Docker）

#### 方法一（推薦）：使用 `.bat` 一鍵啟動（限 Windows）

```bash
cd backend
start_backend.bat
```

執行後將自動進入 `mast3r_api/`、建構 Docker 容器並啟動 FastAPI 應用。

打開瀏覽器前往：
👉 http://localhost:8000/docs  
可查看並測試後端 API（影片上傳、模型處理等）

---

#### 方法二：使用 `docker-compose`（跨平台）

```bash
cd backend
docker-compose up --build
```

此方式適合 macOS / Linux 使用者或 CI/CD 部署場景。

---

### 🌐 2. 啟動前端（Vue 3 + Vite）

前端專案位於 `glb-viewer-app/`，使用 Vue 3 建構介面並搭配 Three.js 顯示 3D 模型。

```bash
cd glb-viewer-app
npm install      # 第一次使用需安裝依賴
npm run dev      # 啟動本地開發伺服器
```

瀏覽器開啟：

👉 http://localhost:5173  
即可使用影片上傳介面與 3D 模型瀏覽功能。

---

## 🧪 系統功能簡述

| 功能 | 描述 |
|------|------|
| 🎞️ 影片上傳 | 使用者可上傳 MP4 影片至後端進行處理 |
| 🧠 模型生成 | 後端進行影片解析，處理影像資訊並轉換為 3D 模型資料 |
| 🌐 前端渲染 | Vue 3 + Three.js 於瀏覽器載入並顯示 `.glb` 模型檔 |
| 🔁 多次上傳 | 支援多次上傳影片，自動更新模型畫面 |

---

## 📁 專案結構簡介

```
ylm-uav/
├── backend/              # FastAPI 後端
│   ├── mast3r_api/       # FastAPI 應用與 Dockerfile
│   ├── start_backend.bat # Windows 啟動腳本
│   └── docker-compose.yaml
├── glb-viewer-app/       # Vue 3 前端專案（Vite + Three.js）
│   ├── src/
│   └── public/
├── README.md             # 本文件
```

---

## 🧠 注意事項

- 後端與前端請分別啟動
- 須確認 Docker Desktop 已執行
- 前端開發伺服器預設 port 為 `5173`
- 後端預設 API port 為 `8001`
- 若需跨機測試，請開放對應 port 或使用內網 IP
- 模型需為 `.glb` 格式，影片為 `.mp4` 格式

---

## 👥 開發團隊

NTUT UAV 團隊  
- [your-name](https://github.com/your-name)
- [your-collaborator](https://github.com/your-collaborator)

---

## 📜 授權 License

本專案依據 MIT License 授權，詳見 `LICENSE` 檔案。
