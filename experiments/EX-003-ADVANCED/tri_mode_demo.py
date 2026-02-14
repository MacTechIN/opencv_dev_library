import cv2
import os
import numpy as np
from core.vision_hub import VisionHub
from core.web.web_utils import WebAppSDK
from core.utils.logger import get_logger

logger = get_logger("TriModeDemo")

def run_tri_mode_analysis():
    # 1. Initialize Vision Hub (Body, Face, Object)
    hub = VisionHub()
    
    # 2. Load Image
    project_root = "/Users/sl/Workspace/12.Antigravity/opencv_dev"
    img_path = os.path.join(project_root, "experiments/EX-002-QWEN-VL/sample.jpg")
    frame = cv2.imread(img_path)
    
    if frame is None:
        logger.error(f"Failed to load image at {img_path}")
        return

    # 3. Triple Engine Analysis
    logger.info("🎬 Starting Tri-Mode Analysis (Body, Face, Object)...")
    results = hub.analyze_scene(frame, modes=["body", "face", "object"])
    
    logger.info(f"📊 Analysis Summary: Body({len(results['body'])}), Face({len(results['face'])}), Object({len(results['object'])})")

    # 4. Visualization with Type-specific Colors
    vis_frame = WebAppSDK.draw_analysis_overlay(frame, results)
    
    # 5. Save and Finish
    output_path = "results/tri_mode_analysis_test.jpg"
    cv2.imwrite(output_path, vis_frame)
    logger.info(f"✅ Tri-Mode analysis result saved to {output_path}")

if __name__ == "__main__":
    run_tri_mode_analysis()
