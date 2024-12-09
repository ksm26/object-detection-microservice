from fastapi import FastAPI, File, UploadFile
from PIL import Image
from ultralytics import YOLO
import json
import os
import shutil

# Initialize the app and YOLOv8 model
app = FastAPI()

# Load YOLOv8 model
model_path = "models/yolov8s.pt"
device = "cpu"
model = YOLO(model_path).to(device)

# Define output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Load and save the uploaded image temporarily
        input_path = os.path.join(OUTPUT_DIR, f"input_{file.filename}")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Perform object detection
        results = model.predict(source=input_path, save=False)

        # Define output paths
        output_image_path = os.path.join(OUTPUT_DIR, f"predict_{file.filename}")
        json_output_path = os.path.join(OUTPUT_DIR, f"{file.filename.split('.')[0]}_detections.json")

        # Save the image with bounding boxes
        for result in results:
            # Get the NumPy array with bounding boxes
            image_with_boxes = result.plot()
            # Convert to PIL Image and save
            Image.fromarray(image_with_boxes).save(output_image_path)

        # Parse detections and save JSON file
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    "bbox": box.xyxy.tolist(),
                    "confidence": float(box.conf),
                    "class": int(box.cls),
                    "label": result.names[int(box.cls)]
                })
        with open(json_output_path, "w") as f:
            json.dump(detections, f)

        # Clean up the temporary input file
        os.remove(input_path)

        # Return results
        return {
            "detections": detections,
            "output_image": output_image_path,
            "json_file": json_output_path,
        }
    except Exception as e:
        return {"error": f"Model inference failed: {str(e)}"}
