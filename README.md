# 📦 UAV 影片上傳與 3D 模型顯示系統

本專案為前後端分離架構，前端採用 Vue 3（Options API）與 Three.js 建構使用者介面與 3D 模型顯示，後端則使用 FastAPI 處理影片上傳與模型生成，並以 Docker 封裝後端服務，支援跨平台快速部署與開發。

---

## 🚀 快速啟動教學

### ✅ 前置需求

- ✅ 已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- ✅ 已安裝 [Node.js](https://nodejs.org/)（建議 v18+）
- ✅ Windows 用戶可直接使用 `start_backend.bat` 啟動後端

---

## 🧪 系統功能簡述

| 功能 | 描述 |
|------|------|
| 🎞️ 影片上傳 | 使用者可上傳 MP4 影片至後端進行處理 |
| 🧠 模型生成 | 後端進行影片解析，處理影像資訊並轉換為 3D 模型資料 |
| 🌐 前端渲染 | Vue 3 + Three.js 於瀏覽器載入並顯示 `.glb` 模型檔 |
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

---

## 🧠 注意事項

- 後端與前端請分別啟動
- 須確認 Docker Desktop 已啟動
- 前端開發伺服器預設 port 為 `5173`
- 後端預設 API port 為 `8001`與`8000`
- 輸入影片格式不限，模型的輸出格式為 `.glb`

---

## 📚 參考資料與引用（References）

本專案整合以下開源模型技術，特此致謝並引用原作者：

- 🔷 **Mast3r** – Multi-view Geometry Aware Canonical Matching  
  GitHub: [https://github.com/naver/mast3r](https://github.com/naver/mast3r)  
  請參考原論文：  
  > Vincent Leroy, Yohann Cabon, Jérôme Revaud.  
  > "Grounding Image Matching in 3D with MASt3R."  
  > In European Conference on Computer Vision (ECCV), 2024.  
  > [arXiv:2406.09756](https://arxiv.org/abs/2406.09756)  

- 🔷 **LaMa** – Resolution-robust Large Mask Inpainting with Fourier Convolutions  
  GitHub: [https://github.com/advimman/lama](https://github.com/advimman/lama)  
  請參考原論文：  
  > Andrey Vasiliev, Egor Zakharov, Dmitry Ulyanov, Victor Lempitsky.  
  > "LaMa: Resolution-robust Large Mask Inpainting with Fourier Convolutions."  
  > In CVPR 2022. [arXiv:2109.07161](https://arxiv.org/abs/2109.07161)
