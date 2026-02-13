import time
from collections import defaultdict
from typing import Dict, List, Any
import datetime
from core.utils.logger import get_logger

# Logger initialization
logger = get_logger("MarketUtils")

class MarketUtils:
    """
    Expert analysis library for commercial district analysis and floating population statistics.
    Combines object features and temporal data to calculate business statistics.
    """

    def __init__(self):
        # Data storage (In-memory for now, DB integration recommended for production)
        self.visit_log = [] # List of {timestamp, id, gender, age, features}
        self.active_objects = {} # Active object info by ID

    def record_visit(self, obj_id: int, gender: str, age: str, features: Dict[str, Any]):
        """Records the visitor's characteristics and entry time."""
        timestamp = datetime.datetime.now()
        log_entry = {
            "timestamp": timestamp,
            "id": obj_id,
            "gender": gender,
            "age": age,
            "features": features
        }
        self.visit_log.append(log_entry)
        logger.info(f"✅ Visitor recorded: ID={obj_id}, Gender={gender}, Age={age}")

    def aggregate_demographics_by_time(self) -> Dict[str, Dict[str, int]]:
        """
        Aggregates demographic distribution (gender/age) by time slot.
        
        Returns:
            Dictionary with time slots as keys and counts as values.
            Example: { "14:00": {"Male_25-32": 5, "Female_15-20": 2}, ... }
        """
        stats = defaultdict(lambda: defaultdict(int))
        for entry in self.visit_log:
            hour = entry["timestamp"].strftime("%H:00")
            key = f"{entry['gender']}_{entry['age']}"
            stats[hour][key] += 1
        return dict(stats)

    def analyze_visitor_flow(self, interval_minutes: int = 60) -> Dict[str, Any]:
        """
        Analyzes the inflow and outflow of visitors during a specific interval (minutes).
        
        Returns:
            Dictionary containing inflow, outflow, net change, and peak hour.
        """
        current_time = datetime.datetime.now()
        start_time = current_time - datetime.timedelta(minutes=interval_minutes)
        
        # Filter visitors within the specified time interval
        recent_visits = [e for e in self.visit_log if e["timestamp"] > start_time]
        
        inflow = len(recent_visits)
        # In actual environments, exit camera logs are managed separately; 
        # Here, we apply a random ratio for demonstration.
        outflow = int(inflow * 0.85) 
        
        # Calculate peak time
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
        Analyzes the ratio between return visitors and new visitors.
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
