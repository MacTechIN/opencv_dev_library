import cv2
import os
import sys
import time
import datetime
import numpy as np
import logging
from typing import Dict

# Ensure core package is in path
sys.path.append(os.getcwd())

from core.processing.face_utils import FaceUtils
from core.processing.centroid_tracker import CentroidTracker
from core.utils.logger import get_logger

# Configure experiment logger
logger = get_logger("EX_001_FACE_MAIN")

def update_dashboard_log(log_path: str, active_objects: Dict[int, Dict]):
    """
    Overwrites the dashboard log file with the current state of all active IDs.
    Format: [ID XX] HH:MM:SS.mmm | Pos: (x,y) Size: WxH | Conf: 0.XX | STATUS
    """
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"=== FACE TRACKNG DASHBOARD ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
            f.write(f"Total Active IDs: {len(active_objects)}\n")
            f.write("-" * 80 + "\n")
            
            for obj_id, info in sorted(active_objects.items()):
                timestamp = info['time'].strftime('%H:%M:%S.%f')[:-3]
                pos = info['centroid']
                size = info['size']
                conf = info['conf']
                status = info['status']
                
                log_line = f"[ID {obj_id:02d}] {timestamp} | Pos: ({pos[0]:4d},{pos[1]:4d}) Size: {size[0]:3d}x{size[1]:3d} | Conf: {conf:.2f} | {status}\n"
                f.write(log_line)
            
            f.write("-" * 80 + "\n")
    except Exception as e:
        logger.error(f"Failed to update dashboard log: {e}")

def run_experiment():
    # Paths
    input_image = "data/test_images/face_sample.jpg"
    results_dir = "experiments/EX-001-FACE/results"
    log_path = os.path.join(results_dir, "tracking_log.txt")
    output_image = os.path.join(results_dir, "tracking_vision_result.jpg")
    
    os.makedirs(results_dir, exist_ok=True)
    
    # Initialize components
    face_utils = FaceUtils()
    ct = CentroidTracker(max_disappeared=20)
    
    if not face_utils.is_ready:
        logger.error("FaceUtils not ready. Please run download_face_models.py first.")
        return

    # Load test image
    frame = cv2.imread(input_image)
    if frame is None:
        logger.error(f"Test image not found at {input_image}")
        return

    logger.info("🚀 Starting Face Tracking & Dashboard Logging Experiment")

    # In a real scenario, this would loop over video frames.
    # We simulate 5 frames to see ID persistence and log updates.
    active_tracking_data = {}
    
    # Simulate first detection frame
    rects = face_utils.detect_faces(frame, conf_threshold=0.5)
    objects = ct.update(rects)

    # Note: CentroidTracker works with centroids. We need to map back to rects for metadata.
    # For simulation, we assume detection is stable.
    for i in range(5): # Simulating 5 frames
        logger.info(f"--- Processing Frame {i+1} ---")
        
        # In a real video, rects would change slightly.
        # Here we just re-run detection (on same image) or simulate slight centroid movement.
        rects = face_utils.detect_faces(frame, conf_threshold=0.5)
        objects = ct.update(rects)
        
        # Update our metadata for dashboard
        current_time = datetime.datetime.now()
        
        # Filter active tracking data to remove objects that disappeared
        active_ids = set(objects.keys())
        active_tracking_data = {k: v for k, v in active_tracking_data.items() if k in active_ids}
        
        for (objectID, centroid) in objects.items():
            # Find the closest rect for metadata (conf, size)
            # In a real sequence, we'd have better mapping logic.
            # For this experiment, we take the first matching rect or a dummy if multiple.
            matched_conf = 0.95 # Simulated
            matched_size = (100, 100) # Simulated
            
            if len(rects) > 0:
                # Basic mapping: take first rect for simplicity in this demo
                r = rects[0]
                matched_size = (r[2] - r[0], r[3] - r[1])
            
            active_tracking_data[objectID] = {
                "centroid": centroid,
                "size": matched_size,
                "conf": matched_conf,
                "time": current_time,
                "status": "TRACKING"
            }
            
            # Draw on frame (only for last frame result)
            if i == 4:
                text = f"ID {objectID}"
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Update real-time "Dashboard" log
        update_dashboard_log(log_path, active_tracking_data)
        time.sleep(0.1) # Brief pause to simulate processing time

    # Save visual result
    cv2.imwrite(output_image, frame)
    logger.info(f"✅ Experiment Completed. Dashboard: {log_path}, Visual: {output_image}")

    # Display final dashboard content to terminal
    print("\n--- FINAL TRACKING DASHBOARD ---")
    with open(log_path, "r") as f:
        print(f.read())
    print("-" * 30)

if __name__ == "__main__":
    run_experiment()
