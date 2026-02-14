import numpy as np
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

class FeatureMatchTracker:
    """
    Advanced tracker combine Centroid (Spatial) and Feature Vector (Appearance).
    Uses weighted matching to maintain ID consistency even with occlusion.
    """
    def __init__(self, max_disappeared: int = 40, feature_weight: float = 0.7):
        self.next_id = 0
        self.objects = OrderedDict()        # ID -> Centroid
        self.features = OrderedDict()       # ID -> Feature Vector
        self.disappeared = OrderedDict()     # ID -> Disappeared Frames Count
        self.max_disappeared = max_disappeared
        self.feature_weight = feature_weight # Weight for feature similarity (0.0 to 1.0)

    def register(self, centroid, feature=None):
        self.objects[self.next_id] = centroid
        self.features[self.next_id] = feature
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.features[object_id]
        del self.disappeared[object_id]

    def _cosine_similarity(self, v1, v2):
        if v1 is None or v2 is None:
            return 0.0
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return dot_product / (norm_v1 * norm_v2)

    def update(self, rects, features=None):
        """
        Args:
            rects: List of [startX, startY, endX, endY]
            features: List of feature vectors (optional)
        """
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            input_centroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                feat = features[i] if features is not None else None
                self.register(input_centroids[i], feat)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            object_features = list(self.features.values())

            # Combined Distance Matrix
            num_obj = len(object_centroids)
            num_in = len(input_centroids)
            D = np.zeros((num_obj, num_in))

            for i in range(num_obj):
                for j in range(num_in):
                    # 1. Spatial Distance (Normalized)
                    spatial_dist = np.linalg.norm(object_centroids[i] - input_centroids[j])
                    # Simple normalization: distance over 500px is "far"
                    spatial_score = min(1.0, spatial_dist / 500.0) 

                    # 2. Appearance Distance (1 - Cosine Similarity)
                    appearance_score = 1.0
                    if features is not None and object_features[i] is not None:
                        sim = self._cosine_similarity(object_features[i], features[j])
                        appearance_score = 1.0 - sim
                    
                    # Combined Score (Lower is better match)
                    D[i, j] = (1 - self.feature_weight) * spatial_score + self.feature_weight * appearance_score

            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                # Threshold check: If match score is too high, it might be a different object
                if D[row, col] > 0.8: 
                    continue

                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                # Update features with a small momentum to handle appearance changes
                if features is not None:
                    new_feat = features[col]
                    if self.features[object_id] is not None:
                        self.features[object_id] = 0.8 * self.features[object_id] + 0.2 * new_feat
                    else:
                        self.features[object_id] = new_feat
                
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    feat = features[col] if features is not None else None
                    self.register(input_centroids[col], feat)

        return self.objects

    def get_feature(self, object_id):
        return self.features.get(object_id)
