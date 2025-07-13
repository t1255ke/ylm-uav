import os
import shutil
import uuid

def create_session_dir():
    clear_temp_dir()  # 可選：每次清空舊資料
    session_id = str(uuid.uuid4())[:8]
    base_dir = os.path.join("temp", session_id)
    os.makedirs(os.path.join(base_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "masks"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "inpainted"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "models"), exist_ok=True)
    return session_id, base_dir

def get_session_dir(session_id):
    base_dir = os.path.join("temp", session_id)
    return base_dir

def save_upload_file(file, destination):
    with open(destination, "wb") as buffer:
        buffer.write(file.file.read())

def clear_temp_dir():
    if os.path.exists("temp"):
        shutil.rmtree("temp")
    os.makedirs("temp", exist_ok=True)
