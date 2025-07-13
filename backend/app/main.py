from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import detect_api, lama_api, viewer_api

app = FastAPI()

# ✅ 允許指定前端來源
origins = [
    "http://localhost:5173",  # Vue 開發伺服器
]

# ✅ CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # 只允許 localhost:5173
    allow_credentials=True,               # 允許攜帶 Cookie / 授權
    allow_methods=["*"],                  # 允許所有請求方法（POST, GET, OPTIONS, DELETE...）
    allow_headers=["*"],                  # 允許所有 headers（例如 Content-Type）
)

# # ✅ 掛載 static，供前端載入 GLB 模型
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

# ✅ 掛載 detect API
app.include_router(detect_api.router, prefix="/detect")
app.include_router(lama_api.router, prefix="/inpaint")
app.include_router(viewer_api.router)
# ✅ 可選：啟動時清除 temp 資料夾內容
# import shutil
# import os

# @app.on_event("startup")
# def clear_temp_folder():
#     temp_dir = "temp"
#     if os.path.exists(temp_dir):
#         for name in os.listdir(temp_dir):
#             path = os.path.join(temp_dir, name)
#             try:
#                 if os.path.isfile(path) or os.path.islink(path):
#                     os.unlink(path)
#                 elif os.path.isdir(path):
#                     shutil.rmtree(path)
#             except Exception as e:
#                 print(f"無法刪除 {path}: {e}")

