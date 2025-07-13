# 📦 UAV 影片上傳與 3D 模型顯示系統

本專案為前後端分離架構，前端採用 Vue 3（Options API）與 Three.js 負責使用者介面與 3D 顯示，後端採用 FastAPI 並封裝於 Docker 中，負責處理影片上傳與模型生成邏輯。

---

## 🚀 快速啟動教學

### ✅ 前置需求

- ✅ 已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- ✅ 已安裝 [Node.js](https://nodejs.org/)（建議 v18 以上）
- ✅ Windows 用戶可直接使用 `start_backend.bat` 啟動後端

---

### 🔧 1. 啟動後端（FastAPI + Docker）

#### 方法一（推薦）：使用 `.bat` 一鍵啟動（限 Windows）

```bash
cd backend
start_backend.bat


---

### 🌐 2. 啟動前端（Vue 3 + Vite）

前端專案位於 `glb-viewer-app/` 資料夾，使用 Vue 3 建構介面並搭配 Three.js 顯示 3D 模型。

#### 步驟如下：

```bash
cd glb-viewer-app
npm install      # 第一次使用時執行（安裝所有依賴）
npm run dev      # 啟動開發伺服器
