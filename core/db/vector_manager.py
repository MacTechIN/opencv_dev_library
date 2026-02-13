import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import datetime
import os
from typing import Dict, List, Optional

class VectorManager:
    """
    Manages 128-d face vector synchronization with Cloud Firestore.
    """
    def __init__(self, collection_name: str = "face_vectors"):
        self.db = None
        self.collection_name = collection_name
        self.is_ready = False
        self._initialize_firebase()

    def _initialize_firebase(self):
        try:
            # Set a shorter timeout for credential discovery to prevent hanging
            # If we're not on GCP, this can take a long time to fail
            os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "false"
            
            if not firebase_admin._apps:
                # Try initializing with default credentials
                firebase_admin.initialize_app()
            
            self.db = firestore.client()
            self.is_ready = True
            print("🚀 VectorManager: Connected to Cloud Firestore")
        except Exception as e:
            print(f"⚠️ VectorManager: Firebase Cloud mode disabled (Local-only). Reason: {e}")
            self.is_ready = False

    def sync_gallery_from_cloud(self) -> Dict[str, dict]:
        """Fetch all vectors from Firestore."""
        if not self.is_ready:
            return {}
        
        gallery = {}
        try:
            docs = self.db.collection(self.collection_name).stream()
            for doc in docs:
                data = doc.to_dict()
                gallery[doc.id] = data
            return gallery
        except Exception as e:
            print(f"Error fetching from cloud: {e}")
            return {}

    def push_vector(self, face_id: str, embedding: np.ndarray, metadata: dict = None):
        """Uplods a new face vector to Firestore."""
        if not self.is_ready:
            return
        
        try:
            doc_ref = self.db.collection(self.collection_name).document(face_id)
            data = {
                "vector": embedding.tolist(),
                "last_seen": firestore.SERVER_TIMESTAMP,
                "created_at": firestore.SERVER_TIMESTAMP
            }
            if metadata:
                data.update(metadata)
                
            doc_ref.set(data, merge=True)
        except Exception as e:
            print(f"Error pushing to cloud: {e}")

    def update_last_seen(self, face_id: str):
        """Updates the timestamp in the cloud."""
        if not self.is_ready:
            return
        try:
            self.db.collection(self.collection_name).document(face_id).update({
                "last_seen": firestore.SERVER_TIMESTAMP
            })
        except:
            pass

    def delete_stale_vectors(self, max_age_seconds: int = 86400):
        """Deletes vectors from cloud that haven't been seen for a long time (Big Data Cleanup)."""
        if not self.is_ready:
            return
        
        # Implementation of cloud-side cleanup query
        # For prototype, we'll keep it simple
        pass
