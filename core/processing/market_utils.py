import time
from collections import defaultdict
from typing import Dict, List, Any
import datetime

class MarketUtils:
    """
    상권 분석 및 유동 인구 통계를 위한 전문 분석 라이브러리.
    객체의 특징과 시간 데이터를 결합하여 비즈니스 통계를 산출합니다.
    """

    def __init__(self):
        # 데이터 저장소 (메모리 내 보관, 실제 운영시 DB 연동 추천)
        self.visit_log = [] # List of {timestamp, id, gender, age, features}
        self.active_objects = {} # ID별 활성 객체 정보

    def record_visit(self, obj_id: int, gender: str, age: str, features: Dict[str, Any]):
        """
        방문자의 특징과 시간을 기록합니다.
        
        Args:
            obj_id: 고유 객체 ID
            gender: 성별
            age: 연령대
            features: 기타 특징 (의상 색상, 가방 유무 등)
        """
        timestamp = datetime.datetime.now()
        log_entry = {
            "timestamp": timestamp,
            "id": obj_id,
            "gender": gender,
            "age": age,
            "features": features
        }
        self.visit_log.append(log_entry)

    def aggregate_demographics_by_time(self) -> Dict[str, Dict[str, int]]:
        """
        시간대별 성별/연령대 인구 분포 통계를 집계합니다.
        
        Returns:
            { "14:00": {"Male_25-32": 5, "Female_15-20": 2}, ... }
        """
        stats = defaultdict(lambda: defaultdict(int))
        for entry in self.visit_log:
            hour = entry["timestamp"].strftime("%H:00")
            key = f"{entry['gender']}_{entry['age']}"
            stats[hour][key] += 1
        return dict(stats)

    def analyze_visitor_flow(self, interval_minutes: int = 60) -> Dict[str, Any]:
        """
        특정 간격(분) 동안의 유입 인구 흐름을 분석합니다.
        
        Returns:
            { "inflow": 120, "outflow": 105, "net_change": 15 }
        """
        # 실제 운영 환경에서는 진입/진출 구역(ROI) 통과 여부로 판단합니다.
        # 여기서는 로그 데이터를 기반으로 단순 집계 예시를 제공합니다.
        total_visits = len(self.visit_log)
        print(f"📈 [LOG] Flow analysis triggered: {total_visits} records found.")
        return {
            "inflow": total_visits,  # 단순화된 예시
            "outflow": int(total_visits * 0.8),
            "net_change": int(total_visits * 0.2)
        }

    def detect_visit_frequency(self, reid_features: List[np.ndarray]) -> Dict[str, Any]:
        """
        Re-ID 특징 벡터를 대조하여 단골 손님(재방문자) 비중을 분석합니다.
        """
        # FeatureBank와 연동하여 신규 vs 기존 ID 구분 로직 필요
        total = len(self.visit_log)
        unique_ids = len(set(entry["id"] for entry in self.visit_log))
        retention = (1 - (unique_ids / total)) * 100 if total > 0 else 0
        
        print(f"📊 [LOG] Retention Analysis: {retention:.1f}% repeat visitors.")
        return {
            "total_visitors": total,
            "unique_visitors": unique_ids,
            "retention_rate": retention
        }
