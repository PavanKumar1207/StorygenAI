import torch
from ultralytics import YOLO


def load_class_names(file_path="coco.names"):
    with open(file_path, "r") as f:
        return f.read().strip().split("\n")

def detect_objects_and_scene(image_path):
    model = YOLO("yolov8n.pt") 
    results = model(image_path)  

    class_names = load_class_names("coco.names")

    
    detected_objects = [
        class_names[int(class_id)]
        for res in results
        for class_id in res.boxes.cls
    ]

    return detected_objects



