from core.processing.market_utils import MarketUtils
import datetime

def test_market_utils_logic():
    print("🧪 [Test] Verifying MarketUtils analysis logic")
    market = MarketUtils()
    
    # 1. Record sample visits
    print("[Step 1] Recording sample visits")
    market.record_visit(101, "Male", "25-32", {"confidence": 0.98})
    market.record_visit(102, "Female", "18-24", {"confidence": 0.95})
    market.record_visit(101, "Male", "25-32", {"confidence": 0.99}) # Return visitor
    
    # 2. Test demographics aggregation
    print("[Step 2] Verifying demographics aggregation")
    stats = market.aggregate_demographics_by_time()
    current_hour = datetime.datetime.now().strftime("%H:00")
    assert current_hour in stats, "Current hour should be in stats"
    assert stats[current_hour]["Male_25-32"] == 2
    assert stats[current_hour]["Female_18-24"] == 1
    print(f"Stats: {stats[current_hour]}")
    
    # 3. Test visitor frequency
    print("[Step 3] Verifying visitor frequency analysis")
    freq = market.detect_visit_frequency()
    assert freq["total_unique"] == 2
    assert freq["return_visitors"] == 1
    assert freq["retention_rate"] == 50.0
    print(f"Frequency: {freq}")
    
    print("✅ MarketUtils verification successful")

if __name__ == "__main__":
    test_market_utils_logic()
