import cv2
import os
import sys
import numpy as np
import logging
from core.processing.face_utils import FaceUtils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FaceIntegrationTest")

def run_face_integration_test():
    image_path = "data/test_images/face_sample.jpg"
    result_dir = "tests/results"
    result_path = os.path.join(result_dir, "face_test_result.jpg")
    
    os.makedirs(result_dir, exist_ok=True)
    
    if not os.path.exists(image_path):
        logger.error(f"❌ Test image not found at {image_path}")
        return

    # Initialize FaceUtils
    face_utils = FaceUtils()
    if not face_utils.is_ready:
        logger.error("❌ FaceUtils initialization failed. Check model paths.")
        return

    # Load image
    frame = cv2.imread(image_path)
    if frame is None:
        logger.error(f"❌ Failed to load image from {image_path}")
        return

    logger.info(f"🚀 Processing image: {image_path} ({frame.shape[1]}x{frame.shape[0]})")
    
    # Detect faces
    faces = face_utils.detect_faces(frame, conf_threshold=0.5)
    logger.info(f"🔍 Detected {len(faces)} face(s)")

    for (x1, y1, x2, y2) in faces:
        # Extract face snippet for classification
        padding = 20
        face_img = frame[max(0, y1-padding):min(frame.shape[0], y2+padding),
                         max(0, x1-padding):min(frame.shape[1], x2+padding)]
        
        # Classify Gender and Age
        gender = face_utils.classify_gender(face_img)
        age = face_utils.classify_age(face_img)
        
        logger.info(f"✨ Face found at ({x1}, {y1}) -> Gender: {gender}, Age: {age}")
        
        # Draw on frame
        color = (0, 255, 0) # Green
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{gender}, {age}"
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Save result
    cv2.imwrite(result_path, frame)
    logger.info(f"✅ Result saved to: {result_path}")
    print(f"\n--- FACE TEST COMPLETED ---\nResult: {result_path}")

if __name__ == "__main__":
    run_face_integration_test()
