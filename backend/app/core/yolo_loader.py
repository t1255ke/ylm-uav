from ultralytics import YOLO

def load_yolo_model(path="models/yolo11.pt"):
    return YOLO(path)
