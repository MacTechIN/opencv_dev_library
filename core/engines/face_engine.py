import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from core.processing.face_processor import FaceProcessor
from core.utils.logger import get_logger

logger = get_logger("FaceEngine")

class FaceEngine:
    """
    Engine specialized in detailed face detection, landmarks, and Re-ID.
    """
    def __init__(self, processor: Optional[FaceProcessor] = None):
        # Assuming FaceProcessor is already implemented in core/processing
        self.processor = processor or FaceProcessor()
        logger.info("👤 FaceEngine initialized with FaceProcessor backend.")

    def detect_and_analyze(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detects faces and extracts features.
        """
        logger.info("🔍 [FaceEngine] Analyzing faces...")
        # FaceProcessor has process_frame method returning List[Person]
        people = self.processor.process_frame(frame)
        
        # Standardize results
        formatted_results = []
        for p in people:
            formatted_results.append({
                "id": p.id,
                "bbox": p.rect, # (x1, y1, x2, y2)
                "type": "face",
                "confidence": 0.99, # Placeholder if not in Person
                "landmarks": []
            })
            
        return formatted_results
