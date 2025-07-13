# 🧠 Backend - FastAPI for UAV 影片處理與 3D 重建
本後端系統基於 FastAPI 建構，負責處理影片上傳、物件偵測、人車移除與 3D 模型重建任務，整合 YOLOv8、LaMa 與 MASt3R 模型。

---

## 🔧 功能模組說明

| 模組 | 路由 | 說明 |
|------|------|------|
| `detect_api.py` | `/detect` | 接收影片並擷取影格，使用 YOLO 偵測並建立遮罩 |
| `lama_api.py` | `/inpaint` | 對遮罩區域執行 LaMa 修復，呼叫 MASt3R 重建模型 |
| `viewer_api.py` | `/get_model/` | 提供前端下載對應 session 的 glb 模型 |
| `file_utils.py` | 工具 | 建立 temp session 資料夾、清除暫存資料等功能 |
| `main.py` | 主應用 | 組合 API、設定 CORS 與掛載 static 資料夾 |

---


---

## 🌐 API 測試入口

本系統包含兩個 FastAPI 服務，分別對應不同處理模組：

### 📍 http://localhost:8001/docs  
提供核心影片處理 API：
- `/detect`：影片影格擷取與 YOLO 物件偵測
- `/inpaint`：影像修復與模型建構
- `/get_model/{session_id}`：回傳對應的 glb 模型檔

### 📍 http://localhost:8000/docs  
提供 MASt3R 模組的重建 API：
- `/reconstruct`：執行多視角 3D 模型重建流程


## ▶️ 啟動方式

### 1️⃣ 使用 bat 檔（限 Windows）

```bash
start_backend.bat
```

會自動啟動 Docker 並執行 FastAPI，後端可在：

📍 http://localhost:8000/docs  
📍 http://localhost:8001/docs  
使用 Swagger UI 測試 API。

---

## 📁 資料夾結構簡述

```
backend/
├── app/
│ ├── main.py # FastAPI 應用主入口
│ ├── routers/
│ │ ├── detect_api.py # 處理影片上傳與 YOLO 偵測
│ │ ├── lama_api.py # 使用 LaMa 修復並觸發 MASt3R
│ │ └── viewer_api.py # 提供 glb 模型下載
│ ├── core/
│ │ └── yolo_loader.py # 載入 YOLO 模型
│ └── utils/
│ └── file_utils.py # 暫存資料夾建立與管理
├── mast3r_api/ # 封裝 MASt3R 重建流程的 FastAPI 服務
│ ├── mast3r_api.py # 提供 /reconstruct API
│ ├── file_utils.py # 處理輸出模型與資料夾管理
│ ├── demo.py # 測試或非 API 模式入口
│ └── Dockerfile # 對應 mast3r_api 的映像檔設定
├── models/ # YOLO 權重檔（yolo8.pt, yolo10.pt, yolo11.pt）
├── temp/ # 用戶上傳與處理過程的暫存資料夾
├── requirements.txt # Python 套件需求列表
├── docker-compose.yaml # 同時啟動主要與重建後端服務
└── start_backend.bat # Windows 用一鍵啟動後端服務
```

---
## 🧪 測試說明

可透過 Swagger UI 或 `curl` 測試：

```bash
curl -X POST http://localhost:8001/detect/ -F "video=@input.mp4"
```

成功後將回傳 `session_id`，可依序呼叫 `/inpaint` → `/get_model/` 取得模型。

---