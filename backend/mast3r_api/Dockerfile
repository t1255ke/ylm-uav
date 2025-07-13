FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.11
ENV PYTHON_BIN=/usr/bin/python3.11

# 安裝系統套件
RUN apt update && apt install -y \
    python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python3-pip \
    git wget curl unzip ffmpeg \
    libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 設定 Python 預設版本並升級 pip
RUN ln -s ${PYTHON_BIN} /usr/bin/python && python -m pip install --upgrade pip

# Clone MASt3R 原始碼
RUN git clone --recursive https://github.com/naver/mast3r.git /app/mast3r
WORKDIR /app/mast3r

# 安裝 MASt3R 相依套件
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
RUN pip install -r requirements.txt
RUN pip install -r dust3r/requirements.txt
RUN pip install -r dust3r/requirements_optional.txt || true
RUN pip install faiss-cpu

# 安裝 ASMK 模組
RUN pip install cython
RUN git clone https://github.com/jenicek/asmk /app/asmk
WORKDIR /app/asmk/cython
RUN cythonize *.pyx
WORKDIR /app/asmk
RUN pip install .

# 下載 MASt3R 模型
WORKDIR /app/checkpoints
RUN wget https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth
RUN wget https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric_retrieval_trainingfree.pth
RUN wget https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric_retrieval_codebook.pkl

# 建立掛載資料夾（影像放在 /app/temp）
WORKDIR /app
VOLUME ["/app/temp"]

# 複製 FastAPI 接口檔案
COPY mast3r_api/mast3r_api.py /app/mast3r_api.py
COPY app/utils/file_utils.py /app/file_utils.py
COPY mast3r_api/demo.py /app/mast3r/mast3r/demo.py
# COPY mast3r_api.py /app/mast3r_api.py
# COPY demo.py /app/mast3r/mast3r/demo.py
# COPY app/utils/file_utils.py /app/file_utils.py

# 安裝 FastAPI 與 Uvicorn
RUN pip install fastapi uvicorn

# 預設啟動 FastAPI 應用
CMD ["uvicorn", "mast3r_api:app", "--host", "0.0.0.0", "--port", "8000"]
