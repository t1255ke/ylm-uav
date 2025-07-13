from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import cv2
import os
import uuid
import tempfile
import requests

from app.utils.file_utils import create_session_dir
from app.core.yolo_loader import load_yolo_model

router = APIRouter()
model = load_yolo_model("models/yolo11.pt")

TARGET_CLASSES = ['pedestrian', 'person', 'bicycle', 'car', 'van', 'tricycle', 'awning-tricycle', 'bus', 'motor']
KERNEL_SIZE = (15, 15)

@router.post("/")
async def detect(video: UploadFile = File(...)):
    session_id, session_dir = create_session_dir()
    image_dir = os.path.join(session_dir, "images")
    mask_dir = os.path.join(session_dir, "masks")

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)

    tmp_video_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp4")
    with open(tmp_video_path, "wb") as f:
        f.write(await video.read())

    cap = cv2.VideoCapture(tmp_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * 0.5) if fps > 0 else 0.5
    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval_frames == 0:
            img_path = os.path.join(image_dir, f"frame_{saved:03d}.jpg")
            cv2.imwrite(img_path, frame)
            saved += 1
        count += 1

    cap.release()
    os.remove(tmp_video_path)

    # 偵測與生成遮罩
    for img_file in sorted(os.listdir(image_dir)):
        img_path = os.path.join(image_dir, img_file)
        img = Image.open(img_path).convert("RGB")
        width, height = img.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)

        results = model.predict(img_path, conf=0.3)[0]

        for box, cls_id in zip(results.boxes.xyxy, results.boxes.cls):
            label = model.names[int(cls_id)]
            if label in TARGET_CLASSES:
                x1, y1, x2, y2 = map(int, box)
                draw.rectangle([x1, y1, x2, y2], fill=255)

        mask_np = np.array(mask)
        kernel = np.ones(KERNEL_SIZE, np.uint8)
        dilated = cv2.dilate(mask_np, kernel, iterations=1)
        dilated_mask = Image.fromarray(dilated)

        mask_output_path = os.path.join(mask_dir, f"{Path(img_file).stem}_mask.png")
        dilated_mask.save(mask_output_path)

    return JSONResponse({"status": "success", "session_id": session_id})
