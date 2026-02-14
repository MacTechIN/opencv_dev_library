import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from core.models.qwen_vl import QwenVLProcessor
from core.utils.logger import get_logger

from core.engines.refinement_engine import RefinementEngine

logger = get_logger("BodyEngine")

class BodyEngine:
    """
    Engine specialized in full-body detection and attribute analysis.
    Uses Qwen-VL as the core reasoning engine for high-precision metadata.
    And uses RefinementEngine to filter out false positives.
    """
    def __init__(self, processor: Optional[QwenVLProcessor] = None):
        self.processor = processor or QwenVLProcessor()
        self.refiner = RefinementEngine()
        logger.info("🧍 BodyEngine initialized with Qwen-VL backend and Refiner.")

    def detect_and_analyze(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detects persons (full body) and extracts attributes like gender, age, clothing.
        Then refines the results using Hybrid Refinement Algorithm.
        """
        logger.info("🔍 [BodyEngine] Analyzing full body attributes...")
        # 1. Base Detection using Qwen-VL
        raw_results = self.processor.detect_and_analyze_persons(frame)
        
        # 2. Hybrid Refinement (Geometric + CV Verification)
        refined_results = self.refiner.refine_detections(frame, raw_results)
        
        # 3. Final Metadata Tagging
        for res in refined_results:
            res["type"] = "body"
            
        return refined_results
