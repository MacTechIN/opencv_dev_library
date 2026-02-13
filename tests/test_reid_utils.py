import numpy as np
from core.processing.reid_utils import FeatureBank

def test_reid_logic():
    print("🧪 [Test] Verifying ReID logic and FeatureBank stability")
    bank = FeatureBank(threshold=0.8)
    
    # 1. Create dummy features
    feat_a1 = np.array([1.0, 0.0, 0.0])
    feat_a2 = np.array([0.9, 0.1, 0.0]) # Similar to A
    feat_b = np.array([0.0, 1.0, 0.0])  # Different from A
    
    # 2. Test ID assignment
    print("[Step 1] Testing ID assignment for new and similar objects")
    id1 = bank.get_unique_id(feat_a1)
    id2 = bank.get_unique_id(feat_a2)
    id3 = bank.get_unique_id(feat_b)
    
    assert id1 == id2, f"ID1({id1}) and ID2({id2}) should match (similarity > 0.8)"
    assert id1 != id3, f"ID1({id1}) and ID3({id3}) should not match"
    print(f"Assigned IDs: A1={id1}, A2={id2}, B={id3}")
    
    # 3. Test feature update
    updated_feat = bank.bank[id1]
    expected_feat = 0.8 * feat_a1 + 0.2 * feat_a2
    assert np.allclose(updated_feat, expected_feat), "Feature vector should be updated with moving average"
    print("✅ Feature bank update verified")
    
    print("✅ ReID logic verification successful")

if __name__ == "__main__":
    test_reid_logic()
