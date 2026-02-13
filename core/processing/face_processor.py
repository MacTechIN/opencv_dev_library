import cv2
import numpy as np
import datetime
from typing import List, Dict, Optional, Tuple
from core.processing.face_utils import FaceUtils
from core.processing.centroid_tracker import CentroidTracker
from core.processing.reid_utils import FaceReID
from core.utils.logger import get_logger

logger = get_logger("FaceProcessor")

class Person:
    """Represents a tracked person with identity and spatial metadata."""
    def __init__(self, face_id: str, rect: Tuple[int, int, int, int], centroid: np.ndarray, 
                 age: str = "Unknown", gender: str = "Unknown"):
        self.id = face_id
        self.rect = rect # (x1, y1, x2, y2)
        self.centroid = centroid
        self.age = age
        self.gender = gender
        self.last_seen = datetime.datetime.now()

class FaceProcessor:
    """
    High-level library module for real-time Face Detection, Tracking, and 
    Cloud-synced Identity Re-identification.
    """
    def __init__(self, max_disappeared: int = 40, match_threshold: float = 0.6):
        self.face_utils = FaceUtils()
        self.reid = FaceReID()
        self.ct = CentroidTracker(max_disappeared=max_disappeared)
        self.match_threshold = match_threshold
        
        # CentroidID -> FaceID
        self.id_mapping = {}
        
        if not self.face_utils.is_ready:
            logger.error("Core models failed to load. Ensure 'python core/utils/download_face_models.py' was run.")
        else:
            print("✅ FaceProcessor: Library ready for frame processing.")

    def process_frame(self, frame: np.ndarray) -> List[Person]:
        """
        Processes a single frame: detects faces, tracks motion, and identifies people.
        
        Returns:
            List of Person objects containing ID, coordinates, and attributes.
        """
        if frame is None:
            return []

        # 1. Detection
        rects = self.face_utils.detect_faces(frame)
        if len(rects) > 0:
            print(f"🔍 FaceProcessor: Detected {len(rects)} faces")
        
        # 2. Tracking (Motion-based)
        objects = self.ct.update(rects)
        
        # 3. Identity Identification (Vector-based Re-ID)
        people = []
        active_centroid_ids = set(objects.keys())
        
        # Cleanup stale mappings
        self.id_mapping = {k: v for k, v in self.id_mapping.items() if k in active_centroid_ids}

        for (centroid_id, centroid) in objects.items():
            face_id = self.id_mapping.get(centroid_id)
            
            # Find the detection box corresponding to this tracking centroid
            matching_rect = None
            for r in rects:
                if r[0] <= centroid[0] <= r[2] and r[1] <= centroid[1] <= r[3]:
                    matching_rect = r
                    break
            
            if matching_rect:
                # If we don't have a persistent FaceID for this tracker yet, extract vector
                if face_id is None:
                    face_roi = frame[matching_rect[1]:matching_rect[3], matching_rect[0]:matching_rect[2]]
                    embedding = self.face_utils.get_face_embedding(face_roi)
                    
                    if embedding is not None:
                        # Cloud/Gallery matching
                        matched_fid = self.reid.find_match(embedding, threshold=self.match_threshold)
                        
                        if matched_fid:
                            face_id = matched_fid
                        else:
                            # New Identity Registration
                            new_num = len(self.reid.gallery) + 1
                            face_id = f"FaceID_{new_num:03d}"
                            self.reid.register_face(face_id, embedding)
                        
                        self.id_mapping[centroid_id] = face_id

                if face_id:
                    # Optional: Add Age/Gender if requested (expensive, so only do if needed)
                    # For simplicity in this base version, we keep them optional
                    p = Person(face_id, matching_rect, centroid)
                    people.append(p)

        # Periodic cloud cleanup hint: typically handled outside or as a specific call
        return people

    def cleanup(self, max_age_seconds: int = 86400):
        """Perform cloud/local cleanup for old identities."""
        self.reid.cleanup_stale_entries(max_age_seconds=max_age_seconds)
