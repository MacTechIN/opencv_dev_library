import numpy as np
import time
import datetime
from core.processing.face_utils import FaceUtils
from core.processing.reid_utils import FeatureBank
from core.processing.market_utils import MarketUtils

def run_actual_working_demo():
    print("🚀 [VisionAI] Integrated Business Library Operation Demo Started")
    
    # 1. Initialization
    reid_bank = FeatureBank(threshold=0.7)
    market_stats = MarketUtils()
    
    # Create mock feature vector (Example of normalized 128D vector)
    def create_mock_feature():
        # Use normal distribution instead of rand for better discrimination
        f = np.random.normal(0, 1, 128)
        return f / np.linalg.norm(f)

    # 2. Scenario: 3 individuals appear on screen (Person A, B, C)
    person_a_feature = create_mock_feature()
    person_b_feature = create_mock_feature()
    person_c_feature = create_mock_feature()
    
    print("\n[STEP 1] Unidentified Object Detection and ID Assignment")
    for i, feat in enumerate([person_a_feature, person_b_feature, person_c_feature]):
        uid = reid_bank.get_unique_id(feat)
        # Gender/Age assumed as model outputs
        gender = "Male" if i % 2 == 0 else "Female"
        age = "(25-32)"
        
        # Record visit
        market_stats.record_visit(uid, gender, age, {"cloth_color": "Blue"})
        print(f"✅ Object Detected: ID-{uid} | Gender: {gender} | Age: {age}")

    # 3. Person A disappears and reappears (Verify Re-ID)
    print("\n[STEP 2] Object Re-identification (Re-ID) Test")
    # Add slight noise to Person A's feature vector
    person_a_reentry = person_a_feature + np.random.normal(0, 0.05, 128)
    uid_reentry = reid_bank.get_unique_id(person_a_reentry)
    
    if uid_reentry == 1: # Person A's original ID is 1
        print(f"🎯 Re-identification Success! ID-1 object has reappeared. (Verified as same person)")
        market_stats.record_visit(uid_reentry, "Male", "(25-32)", {"status": "revisited"})

    # 4. Calculate commercial analysis statistics
    print("\n[STEP 3] Commercial Analysis Data Transformation (Statistics)")
    
    # Hourly distribution
    demo_stats = market_stats.aggregate_demographics_by_time()
    print(f"📊 Hourly Visitors: {demo_stats}")
    
    # Visitor flow analysis
    flow = market_stats.analyze_visitor_flow()
    print(f"📈 Visitor Inflow Flow: {flow}")
    
    # Retention rate analysis
    frequency = market_stats.detect_visit_frequency()
    print(f"♻️ Customer Retention Rate: {frequency['retention_rate']}%")

if __name__ == "__main__":
    # Recommended to run from the parent directory for library path recognition
    run_actual_working_demo()
