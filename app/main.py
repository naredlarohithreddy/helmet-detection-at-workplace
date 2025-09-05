import io
import cv2
import base64
import numpy as np
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import torch

original_torch_load = torch.load

def patched_torch_load(f, map_location=None, pickle_module=None, weights_only=None, **kwargs):
    return original_torch_load(f, map_location=map_location, pickle_module=pickle_module, weights_only=False, **kwargs)

torch.load = patched_torch_load


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models/best_yolo12s.pt"

app = FastAPI(title="Hard Hat Detection API")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://hardhat-detection.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:

    model = YOLO(MODEL_PATH)
    print(f"Model loaded successfully from: {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.get("/")
def read_root():
    return {"status": "Hard Hat Detection API is running."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not model:
        return {"error": "Model is not loaded."}

    contents = await file.read()

    
    image_array = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    results = model(image)
    annotated_image = image.copy()

    line_thickness = 3
    font_scale = 0.6
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_thickness = 2
    used_positions = []

    for box in results[0].boxes:

        print(box)
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0]
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        
        color = (0, 255, 0) if class_name == 'helmet' else (0, 0, 255)
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, line_thickness)
        label = f"{class_name}: {confidence:.2f}"
        
        (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, text_thickness)

        def find_non_overlapping_position(x1, y1, text_width, text_height, used_positions):
            positions_to_try = [
                (x1, y1 - text_height - 15),
                (x1, y2 + text_height + 5), 
                (x2 + 5, y1),              
                (x1 - text_width - 5, y1), 
                (x1, y1 + text_height + 5),
            ]
            
            for pos_x, pos_y in positions_to_try:
                # Check boundaries
                if pos_x < 0 or pos_y < 0:
                    continue
                if pos_x + text_width > annotated_image.shape[1]:
                    continue
                if pos_y > annotated_image.shape[0]:
                    continue
                
                # Check overlap with existing labels
                new_rect = (pos_x, pos_y, pos_x + text_width, pos_y + text_height)
                
                overlap = False
                for used_rect in used_positions:
                    if (new_rect[0] < used_rect[2] and new_rect[2] > used_rect[0] and
                        new_rect[1] < used_rect[3] and new_rect[3] > used_rect[1]):
                        overlap = True
                        break
                
                if not overlap:
                    return pos_x, pos_y
            
            # If all positions overlap, use default
            return x1, y1 - text_height - 15
        
        # Find best position for label
        label_x, label_y = find_non_overlapping_position(x1, y1, text_width, text_height, used_positions)
        
        # Draw label background
        bg_x1 = label_x
        bg_y1 = label_y
        bg_x2 = label_x + text_width + 10
        bg_y2 = label_y + text_height + 5
        
        cv2.rectangle(annotated_image, (bg_x1, bg_y1), (bg_x2, bg_y2), color, -1)
        
        # Draw white text
        cv2.putText(annotated_image, label, (label_x + 5, label_y + text_height), 
                   font, font_scale, (255, 255, 255), text_thickness)
        
        # Store this label position
        used_positions.append((bg_x1, bg_y1, bg_x2, bg_y2))

    _, buffer = cv2.imencode('.jpg', annotated_image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    return {"annotated_image": f"data:image/jpeg;base64,{image_base64}"}