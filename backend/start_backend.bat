@echo off
echo 啟動 FastAPI API（uvicorn）...
start cmd /k "uvicorn app.main:app --reload --port 8001"

echo 啟動 mast3r_api（Docker Compose）...
start cmd /k "docker-compose up --build"

