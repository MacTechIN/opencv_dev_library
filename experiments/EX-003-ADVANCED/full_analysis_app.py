import cv2
import time
import numpy as np
from typing import Dict, List, Any
from core.web.web_utils import WebAppSDK
from core.processing.feature_tracker import FeatureMatchTracker
from core.utils.logger import get_logger

logger = get_logger("AdvancedApp")

def run_advanced_analysis(image_path: str):
    """
    Simulates a real-time advanced analysis pipeline using a static image or sequence.
    """
    # 1. Bootstrap Environment & Models
    context = WebAppSDK.bootstrap_vision_app(model_types=["qwen-vl"])
    qwen = context["models"].get("qwen_vl")
    tracker = FeatureMatchTracker(max_disappeared=50, feature_weight=0.8)
    
    if not qwen:
        logger.error("❌ Qwen-VL model not loaded. Aborting.")
        return

    # 2. Load Image
    frame = cv2.imread(image_path)
    if frame is None:
        logger.error(f"❌ Image not found: {image_path}")
        return

    # 3. Deep Analysis (Periodical / Keyframe)
    logger.info("🧠 Performing Deep Analysis with Qwen-VL...")
    analysis_results = qwen.detect_and_analyze_persons(frame)
    
    # 4. Integrate with Tracker
    # Convert Qwen-VL results to tracker format
    rects = []
    features = []
    metadata = {} # ID -> {gender, age, distance}

    height, width = frame.shape[:2]
    for res in analysis_results:
        ymin, xmin, ymax, xmax = res['bbox']
        # Convert 1000-scale to absolute pixels for tracker
        rect = [
            int(xmin * width / 1000), 
            int(ymin * height / 1000), 
            int(xmax * width / 1000), 
            int(ymax * height / 1000)
        ]
        rects.append(rect)
        features.append(np.array(res['feature_vector']))

    # Tracker Update
    tracked_objects = tracker.update(rects, features)
    
    # Map Tracker IDs to Metadata
    # Since this is a single frame demo, we map directly. 
    # In live video, metadata would persist across updates.
    for obj_id, centroid in tracked_objects.items():
        # Find closest match from analysis_results
        # (Simplified logic for single frame)
        metadata[obj_id] = analysis_results[0] if analysis_results else {}

    # 5. Visualization
    # Create a history for trajectory (simulation)
    history = {}
    for obj_id, centroid in tracked_objects.items():
        # Fake a trajectory for visualization
        history[obj_id] = [
            (centroid[0] - 50, centroid[1] - 50),
            (centroid[0] - 25, centroid[1] - 25),
            (int(centroid[0]), int(centroid[1]))
        ]

    # Draw Overlays
    vis_frame = WebAppSDK.draw_analysis_overlay(frame, analysis_results)
    vis_frame = WebAppSDK.draw_trajectories(vis_frame, history)

    # 6. Save Result
    output_path = "results/advanced_integrated_analysis.jpg"
    cv2.imwrite(output_path, vis_frame)
    logger.info(f"✅ Integrated analysis saved to {output_path}")

    # Generate Report
    from core.models.qwen_vl import generate_markdown_report
    report_path = "results/advanced_detect_report.md"
    generate_markdown_report(analysis_results, report_path)
    logger.info(f"📄 Advanced report saved to {report_path}")

if __name__ == "__main__":
    # Test with the sample image from the previous experiment
    sample_img = "experiments/EX-002-QWEN-VL/sample.jpg"
    run_advanced_analysis(sample_img)
