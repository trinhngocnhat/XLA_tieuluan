# from ultralytics import YOLO
#
# # Load YOLOv8 pre-trained weights
# model = YOLO("yolo11n.pt")  # Options: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8x.pt
#
# # Train the model
# model.train(data="C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/dataset/data.yaml",  # Path to data.yaml from Roboflow
#             epochs=50,                             # Number of training epochs
#             batch=16,                              # Batch size
#             imgsz=640)                             # Image size
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-cls.pt")  # Load a pretrained YOLO model

# Train the model and save the results to a specific directory
results = model.train(
    data="mnist",          # Path to dataset configuration or dataset directory
    epochs=100,            # Number of training epochs
    imgsz=32,              # Image size
    project="C:/Users/ASUS/Documents/GitHub/XLA_tieuluan/runs", # Custom project directory for saving results
    name="mnist_training", # Custom name for this specific training run
    save=True              # Ensure the weights and results are saved
)

# The model weights (best.pt and last.pt) will be saved in:
# my_yolo_runs/mnist_training/weights/
