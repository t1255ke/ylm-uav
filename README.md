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


---

## 🧠 模型與技術細節

本專案整合以下開源模型以提升影片處理與 3D 建構品質：

### 🔷 [Mast3r](https://github.com/naver/mast3r) - 多視角幾何重建

- 由 NAVER 開發的多視角深度估計與相機姿態恢復模型
- 應用於影片轉 3D 模型的幾何一致性重建階段
- 特別適用於低視差、非對稱移動的 UAV 視角

### 🔷 [LaMa](https://github.com/advimman/lama) - 高品質影像修復

- 基於大感受野卷積與深度學習的影像修補模型
- 用於去除遮擋、填補物件缺失區域，提升 3D 建模準確性
- 支援大區域修補，適用於 UAV 影像中的雜訊修復與細節補全
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
- 後端預設 API port 為 `8000`
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

---

## 📚 參考資料與引用（References）

本專案整合以下開源模型技術，特此致謝並引用原作者：

- 🔷 **Mast3r** – Multi-view Geometry Aware Canonical Matching  
  GitHub: [https://github.com/naver/mast3r](https://github.com/naver/mast3r)  
  請參考原論文：  
  > Hyeonwoo Yu, Wonjune Cho, Junsik Kim, Taekyun Jeon, In So Kweon.  
  > "Mast3r: Multiple View Geometry-Aware Self-supervised 3D Reconstruction."  
  > In ECCV 2022. [arXiv:2204.00636](https://arxiv.org/abs/2204.00636)

- 🔷 **LaMa** – Resolution-robust Large Mask Inpainting with Fourier Convolutions  
  GitHub: [https://github.com/advimman/lama](https://github.com/advimman/lama)  
  請參考原論文：  
  > Andrey Vasiliev, Egor Zakharov, Dmitry Ulyanov, Victor Lempitsky.  
  > "LaMa: Resolution-robust Large Mask Inpainting with Fourier Convolutions."  
  > In CVPR 2022. [arXiv:2109.07161](https://arxiv.org/abs/2109.07161)
