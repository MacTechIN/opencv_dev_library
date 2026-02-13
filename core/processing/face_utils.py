import cv2
import numpy as np
import os
import time
from typing import List, Tuple, Dict, Optional
from core.utils.logger import get_logger

# Unified logger initialization
logger = get_logger("FaceUtils")

class FaceUtils:
    """
    Utility class for face recognition and analysis (gender, age).
    Performs inference based on Caffe models using the OpenCV DNN module.
    """
    
    # Constant definitions
    AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    GENDER_LIST = ['Male', 'Female']
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def __init__(self, models_path: str = "assets/weights/face_models", use_opencl: bool = True):
        self.models_path = models_path
        self.use_opencl = use_opencl
        self.is_ready = False
        
        # Initialize model attributes
        self.face_net = None
        self.age_net = None
        self.gender_net = None
        self.reid_net = None
        
        self._load_models()

    def _load_models(self):
        """Loads model weights and prototxt files, and configures the backend."""
        try:
            paths = {
                "face": (os.path.join(self.models_path, "face_net.caffemodel"), os.path.join(self.models_path, "face_deploy.prototxt")),
                "age": (os.path.join(self.models_path, "age_net.caffemodel"), os.path.join(self.models_path, "age_deploy.prototxt")),
                "gender": (os.path.join(self.models_path, "gender_net.caffemodel"), os.path.join(self.models_path, "gender_deploy.prototxt")),
                "reid": (os.path.join(self.models_path, "openface.nn4.small2.v1.t7"), None)
            }

            for key, (model, proto) in paths.items():
                if not os.path.exists(model) or (proto and not os.path.exists(proto)):
                    raise FileNotFoundError(f"Model files not found: {model} or {proto}")

            self.face_net = cv2.dnn.readNet(paths["face"][0], paths["face"][1])
            self.age_net = cv2.dnn.readNet(paths["age"][0], paths["age"][1])
            self.gender_net = cv2.dnn.readNet(paths["gender"][0], paths["gender"][1])
            self.reid_net = cv2.dnn.readNetFromTorch(paths["reid"][0])

            # Hardware acceleration settings
            if self.use_opencl:
                self.face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
                self.face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
                logger.info("🚀 FaceUtils: OpenCL acceleration mode enabled")

            self.is_ready = True
            logger.info("✅ FaceUtils: All models loaded successfully")

        except Exception as e:
            logger.error(f"❌ Model load process failed: {e}")
            self.is_ready = False

    def detect_faces(self, frame: np.ndarray, conf_threshold: float = 0.7) -> List[Tuple[int, int, int, int]]:
        """
        Detects faces in the frame and returns their coordinates.
        
        Args:
            frame: Input image (BGR)
            conf_threshold: Confidence threshold for detection
            
        Returns:
            List of (x1, y1, x2, y2) tuples
        """
        if not self.is_ready or frame is None or frame.size == 0:
            return []

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        face_boxes = []
        # Optimization: Reference fixed shape value outside the loop
        num_detections = detections.shape[2]
        
        for i in range(num_detections):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                # Coordinate normalization and boundary handling
                x1 = max(0, int(detections[0, 0, i, 3] * w))
                y1 = max(0, int(detections[0, 0, i, 4] * h))
                x2 = min(w - 1, int(detections[0, 0, i, 5] * w))
                y2 = min(h - 1, int(detections[0, 0, i, 6] * h))
                
                # Check if the box has valid dimensions
                if x2 > x1 and y2 > y1:
                    face_boxes.append((x1, y1, x2, y2))
        return face_boxes

    def _classify_common(self, net: cv2.dnn.Net, face_img: np.ndarray, labels: List[str]) -> str:
        """Common classification logic (deduplication and stability)"""
        if not self.is_ready or net is None or face_img is None or face_img.size == 0:
            return "Unknown"
            
        try:
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
            net.setInput(blob)
            preds = net.forward()
            return labels[preds[0].argmax()]
        except Exception as e:
            logger.warning(f"Error during classification: {e}")
            return "Unknown"

    def classify_gender(self, face_img: np.ndarray) -> str:
        """Categorize gender (Male/Female) from a face image snippet"""
        return self._classify_common(self.gender_net, face_img, self.GENDER_LIST)

    def classify_age(self, face_img: np.ndarray) -> str:
        """Estimate age range from a face image snippet"""
        return self._classify_common(self.age_net, face_img, self.AGE_LIST)

    def get_face_embedding(self, face_img: np.ndarray) -> Optional[np.ndarray]:
        """Extracts a 128-dimensional embedding vector from a face image."""
        if not self.is_ready or self.reid_net is None or face_img is None or face_img.size == 0:
            return None
        
        try:
            # Preprocess for OpenFace (96x96 RGB)
            face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            blob = cv2.dnn.blobFromImage(face_rgb, 1.0/255, (96, 96), (0, 0, 0), swapRB=False, crop=False)
            self.reid_net.setInput(blob)
            return self.reid_net.forward().flatten()
        except Exception as e:
            logger.warning(f"Embedding extraction failed: {e}")
            return None
