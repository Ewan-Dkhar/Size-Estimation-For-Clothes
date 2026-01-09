from app.measurement import extract_features_from_keypoints
from app.classifier import get_estimated_size

import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path
from collections import Counter 

BASE_DIR = Path(__file__).resolve().parent
MOVENET_MODEL_PATH = BASE_DIR.parent / "models" / "3.tflite"

interpreter = tf.lite.Interpreter(model_path=str(MOVENET_MODEL_PATH))
interpreter.allocate_tensors()

def estimate_clothing_size(video_path, person_height):
    cap = cv2.VideoCapture(video_path)

    predictions = [] # to store all the predictions

    while cap.isOpened():
        ret, frame = cap.read()

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

        message = ""

        if df_features is not None:
            predicted_size = get_estimated_size(df_features)
            predictions.append(predicted_size)
            # message = f"Estimated Size: {predicted_size}"
        
        if len(predictions) >= 30:
            break
        
        # cv2.imshow('Size Estiamtion', frame)

        # if cv2.waitKey(10) & 0xFF==ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

    if len(predictions) < 10:
        return "unknown"

    # Get the Prediction with the most count
    final_prediction, count = Counter(predictions).most_common(1)[0]
    confidence = count / len(predictions) * 100

    message = f"Estimated Size: {final_prediction} (Confidence = {round(confidence, 2)}%)"

    return {
        "size": final_prediction,
        "confidence": round(confidence, 2)
    }