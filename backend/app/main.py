from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import shutil
import uuid

from app.measurement import extract_features_from_keypoints
from app.classifier import get_estimated_size

import tensorflow as tf
from pathlib import Path
import cv2
import numpy as np

app = FastAPI(title="Clothing Size Estimation API")

BASE_DIR = Path(__file__).resolve().parent
MOVENET_MODEL_PATH = BASE_DIR.parent / "models" / "3.tflite"
interpreter = tf.lite.Interpreter(model_path=str(MOVENET_MODEL_PATH))
interpreter.allocate_tensors()

TEMP_DIR = BASE_DIR.parent / "temp_images"
TEMP_DIR.mkdir(exist_ok=True)

@app.post("/estimate-size")
async def estimate_size(
    image: UploadFile = File(...),
    height_cm: float = Form(...)
):
    # Validate input
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")

    if height_cm < 100 or height_cm > 250:
        raise HTTPException(status_code=400, detail="Invalid height")

    # Generate unique filename
    temp_filename = f"{uuid.uuid4().hex}_{image.filename}"
    temp_path = TEMP_DIR / temp_filename

    # Save image temporarily
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        # Run your existing model pipeline
        result = estimate_clothing_size(
            image_path=str(temp_path),
            person_height=height_cm
        )

    finally:
        # Always clean up
        if temp_path.exists():
            temp_path.unlink()

    return result


def estimate_clothing_size(image_path, person_height):
    # Load image
    frame = cv2.imread(image_path)

    if frame is None:
        raise ValueError("Could not read image")

    # Reshape image
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192, 192)
    input_image = tf.cast(img, dtype=tf.float32)

    # Setup input and output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Make predictions
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

    h, w, _ = frame.shape 

    df_features = extract_features_from_keypoints(keypoints_with_scores, h, w, person_height)
    print(df_features)

    if df_features is not None:
        predicted_size = get_estimated_size(df_features)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return predicted_size
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return "Please take a proper picture."
