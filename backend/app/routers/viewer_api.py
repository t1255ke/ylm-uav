from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
import os
from app.utils.file_utils import get_session_dir

router = APIRouter()

@router.get("/get_model/")
async def get_model(session_id: str = Query(...)):
    session_dir = get_session_dir(session_id)
    model_path = os.path.join(session_dir, "models", "model.glb")
    print("完整模型路徑：", os.path.abspath(model_path))

    if os.path.exists(model_path):
        return FileResponse(
            path=model_path,
            media_type="model/gltf-binary",
            filename="model.glb"
        )
    raise HTTPException(status_code=404, detail="GLB model not found.")
