# 🧠 Backend - FastAPI for UAV 影片處理與 3D 重建

本後端系統基於 FastAPI 架構，整合 YOLOv8、LaMa 與 MASt3R 等模型，實現影片上傳、物件偵測、人車移除及 3D 模型重建等功能。所有服務均容器化，支援跨平台部署。

---

## 🔧 功能模組總覽

| 模組 | 路由 | 說明 |
|------|------|------|
| `detect_api.py` | `/detect` | 上傳影片、擷取影格並以 YOLO 執行物件偵測與遮罩建立 |
| `lama_api.py` | `/inpaint` | 使用 LaMa 修復遮罩區域，並觸發 MASt3R 進行 3D 重建 |
| `viewer_api.py` | `/get_model/{session_id}` | 依照 session ID 提供對應的 glb 模型下載 |
| `mast3r_api.py` | `/reconstruct` | MASt3R 重建 API，接收處理過的影格並產生 3D 模型 |
| `file_utils.py` | 工具模組 | 處理資料夾建立、檔案儲存與清除暫存資料等共用邏輯 |
| `main.py` | 主應用 | 整合路由並設定 CORS 與靜態資源服務 |

---

## 🌐 API 測試入口

本系統啟動兩個 FastAPI 實例，分別服務不同處理流程：

- 📍 `http://localhost:8001/docs`[http://localhost:8000/docs] 
  - `/detect`：影片解析與物件遮罩
  - `/inpaint`：LaMa 修復與觸發重建
  - `/get_model/{session_id}`：回傳 `.glb` 模型檔案

- 📍 `http://localhost:8000/docs`[http://localhost:8000/docs]
  - `/reconstruct`：單獨提供 MASt3R 模組進行 3D 重建任務

使用 Swagger UI 可直接測試各項 API。

---

## ▶️ 啟動方式

### ✅ 使用 `.bat`（推薦，限 Windows）

```bash
start_backend.bat
```

將自動啟動兩個容器服務並對應至上述 port。

---

## 📁 資料夾結構簡述

```
backend/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── detect_api.py
│   │   ├── lama_api.py
│   │   └── viewer_api.py
│   ├── core/
│   │   └── yolo_loader.py
│   └── utils/
│       └── file_utils.py
├── mast3r_api/
│   ├── mast3r_api.py
│   ├── file_utils.py
│   ├── demo.py
│   └── Dockerfile
├── models/                  # YOLOv8 權重檔案（yolo8.pt, yolo10.pt...）
├── temp/                    # 暫存上傳與處理資料（依 session 分類）
├── requirements.txt
├── docker-compose.yaml
└── start_backend.bat
```

---


## 🧪 測試方式

可使用 Swagger UI 或 CLI 工具（如 curl）進行三步驟測試：

### 1️⃣ 上傳影片並產生 Session
```bash
curl -X POST http://localhost:8001/detect/ \
  -F "video=@your_video.mp4"
```

成功會回傳：
```json
{ "session_id": "your-session-id" }
```

### 2️⃣ 修補與建模（需傳入 session_id）
```bash
curl -X POST http://localhost:8001/inpaint/ \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"your-session-id\"}"
```

### 3️⃣ 下載生成的 glb 模型
```bash
curl -O http://localhost:8001/get_model/your-session-id
```
