import numpy as np
import time
from typing import Dict, Optional, Tuple, List, Any
from core.utils.logger import get_logger

logger = get_logger("ReID")

class FeatureBank:
    """
    Re-identification (Re-ID) engine that stores and compares object feature vectors
    to determine if they belong to the same individual.
    """

    def __init__(self, threshold: float = 0.6):
        self.bank: Dict[int, np.ndarray] = {}  # {obj_id: feature_vector}
        self.threshold = threshold
        self.next_id = 1

    def get_unique_id(self, current_feature: np.ndarray) -> int:
        """
        Compares the input feature vector with the existing bank to return the most 
        similar ID or assign a new ID.
        
        Args:
            current_feature: Feature vector of the currently detected object (1D numpy array)
            
        Returns:
            The matched or newly assigned unique ID
        """
        best_match_id = -1
        max_similarity = -1.0

        for obj_id, stored_feature in self.bank.items():
            # Cosine similarity calculation
            similarity = np.dot(current_feature, stored_feature) / (
                np.linalg.norm(current_feature) * np.linalg.norm(stored_feature)
            )
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_id = obj_id

        # If a similar object exceeding the threshold exists, return that ID
        if max_similarity > self.threshold:
            # Update the feature vector (Reflecting latest appearance - could apply moving average)
            self.bank[best_match_id] = 0.8 * self.bank[best_match_id] + 0.2 * current_feature
            return best_match_id
        
        # If no match found, assign a new ID
        new_id = self.next_id
        self.bank[new_id] = current_feature
        self.next_id += 1
        return new_id

    def clear_old_features(self, max_idle_seconds: int = 300):
        """
        Manages memory by deleting features of objects that haven't appeared for a long time.
        
        Args:
            max_idle_seconds: Idle time (seconds) threshold for deletion
        """
        current_time = time.time()
        # Note: Actual implementation would require tracking the last detection time per ID.
        # This is a conceptual implementation placeholder.
        logger.info(f"🧹 FeatureBank cleanup: Removing features idle for more than {max_idle_seconds} seconds...")
        pass
