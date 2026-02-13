import numpy as np
import logging
from core.processing.face_utils import FaceUtils

def test_face_utils_robustness():
    print("🧪 [Test] Starting FaceUtils optimization and stability test")
    
    # 1. Initialization test with missing models (Should output error logs)
    print("\n[Case 1] Initialization with invalid path (Verification of error handling)")
    face_module = FaceUtils(models_path="invalid/path")
    print(f"Result: is_ready = {face_module.is_ready}")
    
    # 2. Test with invalid input frames
    print("\n[Case 2] Test with None or empty frame input")
    boxes = face_module.detect_faces(None)
    print(f"Result for None input (Expected empty list): {boxes}")
    
    empty_frame = np.zeros((0, 0, 3), dtype=np.uint8)
    boxes = face_module.detect_faces(empty_frame)
    print(f"Result for empty frame input (Expected empty list): {boxes}")

    # 3. Stability test during classification
    print("\n[Case 3] Verification of classifier stability (Should return 'Unknown')")
    gender = face_module.classify_gender(None)
    age = face_module.classify_age(None)
    print(f"Result: Gender={gender}, Age={age} (Expected 'Unknown' for both)")

if __name__ == "__main__":
    test_face_utils_robustness()
