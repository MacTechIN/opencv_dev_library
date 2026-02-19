import cv2
import numpy as np
import torch
from typing import List, Dict, Any, Optional
from PIL import Image

# Core components
from core.models.qwen_vl import QwenVLProcessor
from core.utils.logger import get_logger

# SAM2 imports (Assuming Meta SAM2 is installed)
try:
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor
    SAM2_AVAILABLE = True
except ImportError:
    SAM2_AVAILABLE = False

logger = get_logger("QwenSAMEngine")

class QwenSAMEngine:
    """
    Hybrid engine combining Qwen2-VL for semantic detection 
    and SAM2 for precise pixel-level segmentation.
    """
    def __init__(self, 
                 qwen_processor: Optional[QwenVLProcessor] = None,
                 sam2_checkpoint: str = "sam2_hiera_tiny.pt",
                 sam2_config: str = "sam2_hiera_t.yaml",
                 device: str = "mps" if torch.backends.mps.is_available() else "cpu"):
        
        self.device = device
        self.qwen = qwen_processor or QwenVLProcessor(device=self.device)
        self.predictor = None
        
        if SAM2_AVAILABLE:
            try:
                # Note: Checkpoints should be downloaded separately if not present
                self.sam2_model = build_sam2(sam2_config, sam2_checkpoint, device=self.device)
                self.predictor = SAM2ImagePredictor(self.sam2_model)
                logger.info("✅ SAM2 Engine initialized successfully.")
            except Exception as e:
                logger.error(f"❌ Failed to initialize SAM2: {e}")
        else:
            logger.warning("⚠️ SAM2 library not found. Falling back to Detection-only mode.")

    def segment_with_qwen_guide(self, image_path: str, prompt: str) -> List[Dict[str, Any]]:
        """
        1. Detect objects using Qwen-VL (Visual Grounding)
        2. Refine boundaries using SAM2 (Segmentation)
        """
        # Step 1: VLM Detection
        # Qwen-VL usually returns normalized bounding boxes [ymin, xmin, ymax, xmax]
        detections = self.qwen.detect_and_analyze_persons(image_path)
        
        if not detections:
            logger.info("No objects detected by Qwen-VL.")
            return []

        # Load image for SAM2 and scaling
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        
        if self.predictor:
            self.predictor.set_image(image_rgb)

        refined_results = []
        
        for i, det in enumerate(detections):
            # Step 2: Scale coordinates to image pixels
            # Expected format from detection: [ymin, xmin, ymax, xmax] (normalized 0-1000)
            # Actually, check QwenVLProcessor.detect_and_analyze_persons implementation
            # It returns results with 'bbox' and 'id' etc.
            
            bbox = det.get('bbox') # Expected [y1, x1, y2, x2]
            if not bbox: continue
            
            # Convert to [x1, y1, x2, y2] for SAM2
            x1, y1, x2, y2 = bbox[1], bbox[0], bbox[3], bbox[2]
            
            # Scaling if normalized (Qwen-VL defaults to 1000-based)
            # We assume bbox is normalized 0-1000 as per common Qwen-VL output
            real_bbox = np.array([
                x1 * w / 1000, 
                y1 * h / 1000, 
                x2 * w / 1000, 
                y2 * h / 1000
            ])
            
            mask_data = None
            if self.predictor:
                # Step 3: SAM2 Segmentation
                masks, scores, _ = self.predictor.predict(
                    box=real_bbox,
                    multimask_output=False
                )
                mask_data = masks[0] # Boolean mask
            
            refined_results.append({
                "id": det.get("id", i),
                "label": det.get("label", "object"),
                "bbox": real_bbox.tolist(),
                "mask": mask_data,
                "confidence": det.get("confidence", 0.0),
                "attributes": det.get("attributes", {})
            })
            
        logger.info(f"Successfully segmented {len(refined_results)} objects.")
        return refined_results

    def draw_segmentation_results(self, frame: np.ndarray, results: List[Dict[str, Any]]) -> np.ndarray:
        """
        Overlays masks and boxes on the frame.
        """
        overlay = frame.copy()
        for res in results:
            mask = res.get("mask")
            bbox = res.get("bbox")
            
            if mask is not None:
                # Draw colorful mask
                color = np.random.randint(0, 255, (3,), dtype=np.uint8).tolist()
                mask_overlay = np.zeros_like(frame)
                mask_overlay[mask] = color
                overlay = cv2.addWeighted(overlay, 1.0, mask_overlay, 0.5, 0)
            
            if bbox:
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(overlay, f"ID:{res['id']} {res['label']}", (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        return overlay
