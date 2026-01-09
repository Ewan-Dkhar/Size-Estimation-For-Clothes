from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid

from app.video_pipeline import estimate_clothing_size

import tensorflow as tf
from pathlib import Path

app = FastAPI(title="Clothing Size Estimation API")

# Add CORS middleware
origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MOVENET_MODEL_PATH = BASE_DIR.parent / "models" / "3.tflite"
interpreter = tf.lite.Interpreter(model_path=str(MOVENET_MODEL_PATH))
interpreter.allocate_tensors()

TEMP_DIR = BASE_DIR.parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/estimate-size")
async def estimate_size(
    video: UploadFile = File(...),
    height_cm: float = Form(...)
):
    # Validate input
    if video.content_type not in ["video/mp4"]:
        raise HTTPException(status_code=400, detail="Invalid video format")

    if height_cm < 100 or height_cm > 250:
        raise HTTPException(status_code=400, detail="Invalid height")

    # Generate unique filename
    temp_filename = f"{uuid.uuid4().hex}_{video.filename}"
    temp_path = TEMP_DIR / temp_filename

    # Save image temporarily
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        # Run your existing model pipeline
        result = estimate_clothing_size(
            video_path=str(temp_path),
            person_height=height_cm
        )

    finally:
        # Always clean up
        if temp_path.exists():
            temp_path.unlink()

    return result



