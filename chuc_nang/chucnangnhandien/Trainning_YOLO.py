from ultralytics import YOLO

# Load YOLOv8 pre-trained weights
model = YOLO("yolo11n.pt")  # Options: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8x.pt

# Train the model
model.train(data="C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/dataset/data.yaml",  # Path to data.yaml from Roboflow
            epochs=50,                             # Number of training epochs
            batch=16,                              # Batch size
            imgsz=640)                             # Image size