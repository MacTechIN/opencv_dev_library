import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from core.engines.body_engine import BodyEngine
from core.engines.face_engine import FaceEngine
from core.engines.object_engine import ObjectEngine
from core.utils.logger import get_logger

logger = get_logger("VisionHub")

class VisionHub:
    """
    The Orchestrator that manages Body, Face, and Object engines.
    Merges multi-engine results into a unified intelligence map.
    """
    def __init__(self):
        self.body_engine = BodyEngine()
        self.face_engine = FaceEngine()
        self.object_engine = ObjectEngine(processor=self.body_engine.processor)
        logger.info("🚀 VisionHub initialized. All engines online.")

    def analyze_scene(self, frame: np.ndarray, modes: List[str] = ["body", "face", "object"]) -> Dict[str, Any]:
        """
        Runs multiple engines and aggregates results.
        """
        combined_results = {
            "body": [],
            "face": [],
            "object": [],
            "total_count": 0
        }
        
        if "body" in modes:
            combined_results["body"] = self.body_engine.detect_and_analyze(frame)
        
        if "face" in modes:
            combined_results["face"] = self.face_engine.detect_and_analyze(frame)
            
        if "object" in modes:
            combined_results["object"] = self.object_engine.detect_general_objects(frame)
            
        combined_results["total_count"] = len(combined_results["body"]) + len(combined_results["face"]) + len(combined_results["object"])
        
        return combined_results
