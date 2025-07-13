# 🌐 Frontend 使用說明（Vue 3 + Vite）

本前端專案位於 `glb-viewer-app/` 資料夾，使用 Vue 3 搭配 Vite 開發，並整合 Three.js 以呈現 glb 3D 模型視覺化介面。

---

### 🚀 啟動方式

請先確認已安裝 [Node.js](https://nodejs.org/)（建議版本：v18 以上）。

```bash
cd glb-viewer-app
npm install      # 第一次使用需安裝依賴
npm run dev      # 啟動本地開發伺服器
```

---

### 🌍 使用說明

啟動後，瀏覽器開啟：

👉 [http://localhost:5173](http://localhost:5173)

即可進入使用者介面，上傳影片並預覽自動重建的 3D 模型。

---

### 🧰 技術簡介

- **Vue 3 (Options API)**：負責前端畫面邏輯與狀態管理
- **Three.js**：用於渲染 `.glb` 格式 3D 模型
- **Vite**：輕量快速的開發伺服器與打包工具

---

