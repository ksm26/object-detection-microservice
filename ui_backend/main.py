from fastapi import FastAPI, File, UploadFile
import requests
import shutil
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "UI Backend is running!"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Validate file extension (example: only allow .jpg and .png)
        allowed_extensions = {"jpg", "jpeg", "png"}
        if not file.filename.split(".")[-1].lower() in allowed_extensions:
            return {"error": "Unsupported file type. Please upload a .jpg or .png image."}

        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Send image to AI backend
        with open(temp_file_path, "rb") as f:
            ai_response = requests.post("http://ai-backend:8000/detect/", files={"file": f})

        if ai_response.status_code != 200:
            return {"error": f"AI Backend returned an error: {ai_response.text}"}

        # Return the response to the user
        return ai_response.json()
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Ensure the temporary file is removed
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
