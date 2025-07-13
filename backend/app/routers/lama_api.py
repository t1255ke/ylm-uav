from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from PIL import Image
from pathlib import Path
import os
import requests

from simple_lama_inpainting import SimpleLama
from app.utils.file_utils import get_session_dir

router = APIRouter()
lama_model = SimpleLama()

@router.post("/")
async def inpaint(session_id: str = Form(...)):
    session_dir = get_session_dir(session_id) 
    print("inpaint 被呼叫！session_id =", session_id)
    image_dir = os.path.join(session_dir, "images")
    mask_dir = os.path.join(session_dir, "masks")
    output_dir = os.path.join(session_dir, "inpainted")
    os.makedirs(output_dir, exist_ok=True)

    inpainted_count = 0

    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(image_dir, filename)
            mask_path = os.path.join(mask_dir, f"{Path(filename).stem}_mask.png")
            out_path = os.path.join(output_dir, filename)

            if not os.path.exists(mask_path):
                print(f"⚠️ 無 mask，略過 {filename}")
                continue

            image = Image.open(img_path).convert("RGB")
            mask = Image.open(mask_path).convert("L")
            result = lama_model(image, mask)
            result.save(out_path)
            inpainted_count += 1
    print(f"移除人車儲存至：{output_dir}")

    if inpainted_count == 0:
        return JSONResponse({"error": "沒有成功修復的影像，inpainted 資料夾為空"}, status_code=400)

    # 呼叫 MASt3R
    response = requests.post("http://localhost:8000/reconstruct/", params={"session_id": session_id})
    if response.status_code != 200:
        print("MASt3R 重建失敗:", response.text)
    else:
        print("MASt3R 重建成功！")

    return FileResponse(out_path, media_type="image/png")

