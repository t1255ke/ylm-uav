from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import torch
import glob
import logging
from contextlib import nullcontext
import tempfile
import shutil

# 導入 MASt3R 核心功能
import sys
sys.path.append("/app/mast3r")
from mast3r.demo import get_reconstructed_scene, get_3D_model_from_scene
from mast3r.model import AsymmetricMASt3R
from mast3r.utils.misc import hash_md5
from file_utils import get_session_dir

app = FastAPI()
router = APIRouter()

CHECKPOINT_NAME = "MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric"
CHECKPOINT_PATH = f"/app/checkpoints/{CHECKPOINT_NAME}.pth"

@router.post("/reconstruct/")
def reconstruct(session_id: str = Query(...)):
    session_dir = Path(get_session_dir(session_id))
    input_dir = Path("temp") / session_id / "inpainted"
    print(f"input_dir = {input_dir}, exists = {input_dir.exists()}")

    image_files = sorted(list(input_dir.glob("*.jpg")))
    image_paths = [str(p) for p in image_files]  
    print(f"找到圖片數量: {len(image_files)}, 檔案列表: {[str(p) for p in image_files]}")
    if len(image_files) < 2:
        return JSONResponse({"error": "至少需要兩張圖片來進行重建"}, status_code=400)

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = AsymmetricMASt3R.from_pretrained(CHECKPOINT_PATH).to(device)
        chkpt_tag = hash_md5(CHECKPOINT_PATH)

        with tempfile.TemporaryDirectory(suffix="_mast3r") as tmpdir:
            cache_path = os.path.join(tmpdir, chkpt_tag)
            os.makedirs(cache_path, exist_ok=True)

            # 執行重建
            scene_state, _ = get_reconstructed_scene(
                outdir=cache_path,
                model=model,
                retrieval_model=None,
                device=device,
                image_size=512,
                filelist=image_paths,
                optim_level="refine+depth",
                lr1=0.07,
                niter1=300,
                lr2=0.01,
                niter2=300,
                min_conf_thr=1.5,
                matching_conf_thr=0.0,
                as_pointcloud=False,
                mask_sky=False,
                clean_depth=False,
                transparent_cams=False,
                cam_size=0.2,
                scenegraph_type="complete",
                winsize=1,
                win_cyclic=False,
                refid=0,
                TSDF_thresh=0.0,
                shared_intrinsics=False,
                silent=True,
                gradio_delete_cache=True,
                current_scene_state=None
            )

            # 儲存 3D 模型
            outfile = get_3D_model_from_scene(
                scene_state=scene_state,
                min_conf_thr=1.5,
                as_pointcloud=False,
                mask_sky=False,
                clean_depth=False,
                transparent_cams=False,
                cam_size=0.2,
                TSDF_thresh=0.0,
                silent=True,
            )
            output_dir =Path("temp") / session_id  / "models"
            output_dir.mkdir(parents=True, exist_ok=True)
            final_output_path = output_dir / f"model.glb"
            if outfile and os.path.exists(outfile):
                shutil.move(outfile, final_output_path)
                return {
                    "status": "success",
                    "message": "Reconstruction completed",
                    "output": str(final_output_path)
                }
            else:
                return JSONResponse(status_code=500, content={"error": "模型輸出失敗"})

    except Exception as e:
        logging.exception("重建失敗")
        return JSONResponse(status_code=500, content={"error": str(e)})

app.include_router(router)
