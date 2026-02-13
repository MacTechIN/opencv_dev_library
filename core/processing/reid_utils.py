import numpy as np
from typing import Dict, Optional, Tuple

class FeatureBank:
    """
    객체의 특징 벡터(Feature Vector)를 보관하고 비교하여
    동일인 여부를 판별하는 재식별(Re-ID) 엔진.
    """

    def __init__(self, threshold: float = 0.6):
        self.bank: Dict[int, np.ndarray] = {}  # {obj_id: feature_vector}
        self.threshold = threshold
        self.next_id = 1

    def get_unique_id(self, current_feature: np.ndarray) -> int:
        """
        입력된 특징 벡터를 기존 저장소와 비교하여 가장 유사한 ID를 반환하거나
        새로운 ID를 부여합니다.
        
        Args:
            current_feature: 현재 검출된 객체의 특징 벡터 (1D numpy array)
            
        Returns:
            매칭된 또는 새로 부여된 고유 ID
        """
        best_match_id = -1
        max_similarity = -1.0

        for obj_id, stored_feature in self.bank.items():
            # 코사인 유사도 계산
            similarity = np.dot(current_feature, stored_feature) / (
                np.linalg.norm(current_feature) * np.linalg.norm(stored_feature)
            )
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_id = obj_id

        # 임계값을 넘는 가장 유사한 객체가 있으면 해당 ID 반환
        if max_similarity > self.threshold:
            # 특징 벡터 업데이트 (최신 모습 반영 - 이동 평균 등 적용 가능)
            self.bank[best_match_id] = 0.8 * self.bank[best_match_id] + 0.2 * current_feature
            return best_match_id
        
        # 일치하는 것이 없으면 새로운 ID 부여
        new_id = self.next_id
        self.bank[new_id] = current_feature
        self.next_id += 1
        return new_id

    def clear_old_features(self):
        """오랫동안 나타나지 않은 객체의 특징을 삭제하여 메모리를 관리합니다."""
        pass
