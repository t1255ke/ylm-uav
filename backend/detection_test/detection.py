from ultralytics import YOLO
import cv2

# 指定要偵測的類別
TARGET_CLASSES = [
    'pedestrian', 'person', 'bicycle', 'car', 'van',
    'tricycle', 'awning-tricycle', 'bus', 'motor'
]

# 載入訓練好的 YOLOv8 模型（可換成 yolov8n.pt, yolov8m.pt, yolov8l.pt 依需求）
model = YOLO('./models/yolo10.pt')

# 載入影像或影片（可換成影片路徑或攝影機編號）
image = cv2.imread('test1.png')

# 執行預測
results = model(image)

# 取得 YOLO 類別名稱
model_classes = model.names

# 處理並繪製偵測結果
for result in results:
    for box in result.boxes:
        cls_id = int(box.cls[0])
        cls_name = model_classes[cls_id]

        # 過濾指定類別
        if cls_name in TARGET_CLASSES:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            # 繪製邊框與標籤
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'{cls_name} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 顯示結果影像
cv2.imshow('Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
