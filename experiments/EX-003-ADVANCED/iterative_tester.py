import cv2
import os
import sys
import numpy as np
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from core.vision_hub import VisionHub
from core.web.web_utils import WebAppSDK
from core.utils.logger import get_logger

logger = get_logger("IterativeTester")

def run_test_iteration(version: int):
    """
    Runs a single test iteration and saves versioned output.
    """
    logger.info(f"🚀 Starting Iteration v{version}...")
    
    # 1. Initialize Hub
    try:
        hub = VisionHub()
    except Exception as e:
        logger.error(f"❌ Hub Init Fail: {str(e)}")
        return False, str(e)

    # 2. Load Image
    img_path = "deco_scene.jpg"
    frame = cv2.imread(img_path)
    if frame is None:
        logger.error(f"❌ Image Load Fail: {img_path}")
        return False, "Image not found"

    # 3. Analyze
    try:
        results = hub.analyze_scene(frame, modes=["body", "face", "object"])
        
        body_count = len(results.get('body', []))
        face_count = len(results.get('face', []))
        obj_count = len(results.get('object', []))
        
        logger.info(f"📊 v{version} Result: Body({body_count}), Face({face_count}), Object({obj_count})")
        
        # 4. Visualize
        vis_frame = WebAppSDK.draw_analysis_overlay(frame, results)
        
        # 5. Versioned Save
        output_dir = "results/iterations"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%H%M%S")
        output_file = f"{output_dir}/tri_mode_v{version}_{timestamp}.jpg"
        cv2.imwrite(output_file, vis_frame)
        
        logger.info(f"✅ v{version} Saved -> {output_file}")
        
        # Success criteria: At least one person detected
        is_success = body_count > 0
        status_msg = f"Detected {body_count} persons" if is_success else "No persons detected"
        
        return is_success, status_msg

    except Exception as e:
        logger.error(f"❌ Analysis Fail: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, str(e)

if __name__ == "__main__":
    # Determine next version
    output_dir = "results/iterations"
    os.makedirs(output_dir, exist_ok=True)
    existing_files = [f for f in os.listdir(output_dir) if f.startswith("tri_mode_v")]
    next_v = 1
    if existing_files:
        # Expected: tri_mode_vN_timestamp.jpg
        try:
            v_nums = [int(f.split("_")[2].replace("v", "")) for f in existing_files if "v" in f]
            if v_nums:
                next_v = max(v_nums) + 1
        except Exception:
            next_v = len(existing_files) + 1
    
    success, msg = run_test_iteration(next_v)
    if success:
        print(f"\n✨ SUCCESS: {msg}")
    else:
        print(f"\n⚠️ REVISION NEEDED: {msg}")
