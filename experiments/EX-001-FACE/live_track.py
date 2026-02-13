import cv2
import os
import sys
import time
import datetime
import numpy as np
import json
from typing import Dict

# Ensure core package is in path
sys.path.append(os.getcwd())

from core.processing.face_utils import FaceUtils
from core.processing.centroid_tracker import CentroidTracker
from core.processing.reid_utils import FaceReID
from core.utils.logger import get_logger

# Configure experiment logger
logger = get_logger("EX_001_FACE_PERSISTENT")

def update_dashboard_log(log_path: str, active_objects: Dict[int, Dict]):
    """
    Overwrites the dashboard log file with the current state of tracked faces.
    """
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"=== PERSISTENT FACE TRACKING DASHBOARD ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
            f.write(f"Total Active IDs: {len(active_objects)}\n")
            f.write("-" * 80 + "\n")
            
            for face_id, info in sorted(active_objects.items()):
                timestamp = info['time'].strftime('%H:%M:%S.%f')[:-3]
                pos = info['centroid']
                size = info['size']
                status = info['status']
                
                log_line = f"[{face_id}] {timestamp} | Pos: ({pos[0]:4d},{pos[1]:4d}) Size: {size[0]:3d}x{size[1]:3d} | {status}\n"
                f.write(log_line)
            
            f.write("-" * 80 + "\n")
    except Exception as e:
        logger.error(f"Failed to update dashboard log: {e}")

def run_persistent_tracking():
    # Paths
    results_dir = "experiments/EX-001-FACE/results"
    log_path = os.path.join(results_dir, "persistent_tracking_log.txt")
    os.makedirs(results_dir, exist_ok=True)
    
    # Initialize components
    face_utils = FaceUtils()
    reid = FaceReID()
    ct = CentroidTracker(max_disappeared=40)
    
    if not face_utils.is_ready or not reid.is_ready:
        logger.error("FaceUtils or ReID model not ready.")
        return

    logger.info("🎥 Initializing Webcam for Persistent Tracking...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Could not open webcam.")
        return

    logger.info("🚀 Persistent Face Tracking Started. Press 'q' to exit.")
    
    # Track ID mapping: CentroidID -> FaceID_XXX
    id_map = {}
    active_tracking_data = {}

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1) # Mirror
            rects = face_utils.detect_faces(frame, conf_threshold=0.5)
            objects = ct.update(rects)
            
            current_time = datetime.datetime.now()
            
            # 1. Clean up stale mappings
            active_centroid_ids = set(objects.keys())
            id_map = {k: v for k, v in id_map.items() if k in active_centroid_ids}
            active_tracking_data = {k: v for k, v in active_tracking_data.items() if k in [id_map.get(cid) for cid in active_centroid_ids]}

            # 2. Process each tracked object
            for (centroid_id, centroid) in objects.items():
                face_id = id_map.get(centroid_id)
                
                # Find matching rect for image extraction
                matched_rect = None
                for r in rects:
                    if r[0] <= centroid[0] <= r[2] and r[1] <= centroid[1] <= r[3]:
                        matched_rect = r
                        break
                
                if matched_rect:
                    w = matched_rect[2] - matched_rect[0]
                    h = matched_rect[3] - matched_rect[1]
                    
                    # If this centroid is new (no FaceID yet), perform Re-ID
                    if face_id is None:
                        # Extract Face ROI
                        face_roi = frame[matched_rect[1]:matched_rect[3], matched_rect[0]:matched_rect[2]]
                        embedding = reid.get_embedding(face_roi)
                        
                        if embedding is not None:
                            # Try to find match in gallery
                            matched_fid = reid.find_match(embedding, threshold=0.6)
                            
                            if matched_fid:
                                logger.info(f"🔄 Re-identified existing person: {matched_fid}")
                                face_id = matched_fid
                            else:
                                # New Identity
                                next_num = len(reid.gallery) + 1
                                face_id = f"FaceID_{next_num:03d}"
                                logger.info(f"✨ New Identity detected: {face_id}")
                                
                                # Save ROI Image
                                roi_path = os.path.join(results_dir, f"tracking_vision_result_{face_id}.jpg")
                                cv2.imwrite(roi_path, face_roi)
                                reid.register_face(face_id, embedding)
                            
                            id_map[centroid_id] = face_id

                    if face_id:
                        active_tracking_data[face_id] = {
                            "centroid": centroid,
                            "size": (w, h),
                            "time": current_time,
                            "status": "ACTIVE"
                        }
                        
                        # Drawing
                        cv2.rectangle(frame, (matched_rect[0], matched_rect[1]), 
                                      (matched_rect[2], matched_rect[3]), (0, 255, 0), 2)
                        cv2.putText(frame, face_id, (matched_rect[0], matched_rect[1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Draw centroid
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)

            # 3. Periodic Cleanup (Every 30 seconds for testing)
            # Set max_age_seconds to 60s for demo purposes
            reid.cleanup_stale_entries(max_age_seconds=60)

            # 4. Update Dashboard
            update_dashboard_log(log_path, active_tracking_data)

            # 5. Interface
            cv2.imshow("Persistent Face Tracking (Cross-Session)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info(f"🛑 Session Closed. Gallery Size: {len(reid.gallery)}")

if __name__ == "__main__":
    run_persistent_tracking()
