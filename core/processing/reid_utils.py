import cv2
import numpy as np
import os
import json
import logging
from typing import Dict, List, Optional, Tuple

from core.db.vector_manager import VectorManager

class FaceReID:
    def __init__(self, model_path: str = "assets/weights/face_models/openface.nn4.small2.v1.t7"):
        self.model_path = model_path
        self.net = None
        self.gallery = {} # Local cache of Cloud Vectors
        self.vm = VectorManager()
        self.is_ready = False
        
        self._load_model()
        self.sync_with_cloud()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            return
        try:
            self.net = cv2.dnn.readNetFromTorch(self.model_path)
            self.is_ready = True
        except Exception as e:
            print(f"Failed to load ReID model: {e}")

    def sync_with_cloud(self):
        """Sync local gallery cache with Firestore vectors."""
        if self.vm.is_ready:
            cloud_data = self.vm.sync_gallery_from_cloud()
            if cloud_data:
                # Firestore returns "vector" field, local code expects "embedding" for compatibility
                new_gallery = {}
                for fid, data in cloud_data.items():
                    new_gallery[fid] = {
                        "embedding": data.get("vector"),
                        "last_seen": str(data.get("last_seen"))
                    }
                self.gallery = new_gallery
        elif not self.gallery:
             # Fallback to empty if both cloud and local fail
             self.gallery = {}

    def save_gallery(self):
        """No-op for local. Cloud updates happen in register_face."""
        pass

    def get_embedding(self, face_img: np.ndarray) -> Optional[np.ndarray]:
        if not self.is_ready or face_img is None or face_img.size == 0:
            return None
        
        try:
            # OpenFace expects 96x96 RGB images
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            blob = cv2.dnn.blobFromImage(face_img, 1.0/255, (96, 96), (0, 0, 0), swapRB=False, crop=False)
            self.net.setInput(blob)
            vec = self.net.forward()
            return vec.flatten()
        except:
            return None

    def find_match(self, embedding: np.ndarray, threshold: float = 0.6) -> Optional[str]:
        """Compares embedding with gallery and returns best matching FaceID."""
        best_match = None
        min_dist = threshold
        
        for face_id, data in self.gallery.items():
            gal_emb = np.array(data["embedding"])
            dist = np.linalg.norm(embedding - gal_emb)
            if dist < min_dist:
                min_dist = dist
                best_match = face_id
                
        return best_match

    def register_face(self, face_id: str, embedding: np.ndarray):
        """Updates or registers a new identity in the gallery (Cloud + Local Cache)."""
        # Update local cache
        self.gallery[face_id] = {
            "embedding": embedding.tolist(),
            "last_seen": str(np.datetime64('now', 's'))
        }
        
        # Push to Cloud
        if self.vm.is_ready:
            self.vm.push_vector(face_id, embedding)

    def cleanup_stale_entries(self, max_age_seconds: int = 600, protected_ids: List[str] = ["FaceID_001"]):
        """
        Removes gallery entries that haven't been seen for a long time.
        Also deletes the corresponding ROI image from the disk.
        """
        now = np.datetime64('now', 's')
        to_delete = []

        for face_id, data in self.gallery.items():
            if face_id in protected_ids:
                continue
            
            try:
                last_seen = np.datetime64(data["last_seen"], 's')
                age = (now - last_seen).astype(int)
                
                if age > max_age_seconds:
                    to_delete.append(face_id)
            except:
                # If timestamp is corrupted, mark for deletion
                to_delete.append(face_id)

        for fid in to_delete:
            print(f"🧹 Cleaning up stale identity: {fid}")
            # Delete ROI image
            roi_path = os.path.join(os.path.dirname(self.gallery_path), f"tracking_vision_result_{fid}.jpg")
            if os.path.exists(roi_path):
                os.remove(roi_path)
            
            del self.gallery[fid]

        if to_delete:
            self.save_gallery()
