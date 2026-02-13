import time
from collections import defaultdict
from typing import Dict, List, Any
import datetime
from core.utils.logger import get_logger

logger = get_logger("MarketUtils")

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
        """방문자의 특징과 시간을 기록합니다."""
        timestamp = datetime.datetime.now()
        log_entry = {
            "timestamp": timestamp,
            "id": obj_id,
            "gender": gender,
            "age": age,
            "features": features
        }
        self.visit_log.append(log_entry)
        logger.info(f"✅ 방문객 기록됨: ID={obj_id}, Gender={gender}, Age={age}")

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
            { "inflow": 120, "outflow": 105, "net_change": 15, "peak_hour": "14:00" }
        """
        current_time = datetime.datetime.now()
        start_time = current_time - datetime.timedelta(minutes=interval_minutes)
        
        # 지정된 시간 간격 내의 방문자 필터링
        recent_visits = [e for e in self.visit_log if e["timestamp"] > start_time]
        
        inflow = len(recent_visits)
        # 실제 환경에서는 출구 카메라 로그를 별도로 관리하지만, 예시에선 랜덤 비중 적용
        outflow = int(inflow * 0.85) 
        
        # 피크 타임 계산
        hour_counts = defaultdict(int)
        for e in recent_visits:
            hour_counts[e["timestamp"].strftime("%H:00")] += 1
        peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else "N/A"

        return {
            "inflow": inflow,
            "outflow": outflow,
            "net_change": inflow - outflow,
            "peak_hour": peak_hour
        }

    def detect_visit_frequency(self) -> Dict[str, Any]:
        """
        재방문자(Return Visitor)와 신규 방문자의 비율을 분석합니다.
        """
        if not self.visit_log:
            return {"total": 0, "retention_rate": 0.0}

        id_counts = defaultdict(int)
        for entry in self.visit_log:
            id_counts[entry["id"]] += 1
            
        return_visitors = sum(1 for count in id_counts.values() if count > 1)
        total_unique = len(id_counts)
        retention_rate = (return_visitors / total_unique * 100) if total_unique > 0 else 0.0
        
        return {
            "total_unique": total_unique,
            "return_visitors": return_visitors,
            "retention_rate": round(retention_rate, 2),
            "new_visitors": total_unique - return_visitors
        }
