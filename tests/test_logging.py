import os
import time

def test_unified_logging():
    print("🚀 [Test] Verifying unified logging system")
    
    # 1. Delete log file before testing (Clean test)
    log_dir = "logs"
    log_file = os.path.join(log_dir, "vision_ai.log")
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
        except PermissionError:
            print("⚠️ Log file is in use by another process. Appending to existing file.")
    
    # 2. Call each module (Verify error logs are generated)
    print("\n--- Starting module-specific logging events ---")
    
    try:
        from core.processing.face_utils import FaceUtils
        face = FaceUtils(models_path="core/models/invalid") # Induce error logging
    except Exception as e:
        print(f"FaceUtils test skipped or error: {e}")

    try:
        from core.processing.market_utils import MarketUtils
        market = MarketUtils()
        market.record_visit(101, "Male", "25-32", {"color": "red"})
    except Exception as e:
        print(f"MarketUtils test failed: {e}")

    try:
        from core.processing.reid_utils import FeatureBank
        reid = FeatureBank()
        reid.clear_old_features(300)
    except Exception as e:
        print(f"ReID test failed: {e}")

    try:
        from core.models.qwen_vl import QwenVLProcessor
        qwen = QwenVLProcessor()
    except Exception as e:
        print(f"QwenVL test skipped (torch not installed, etc.): {e}")
    
    # 3. Verify log file
    print("\n--- Verifying log file records ---")
    time.sleep(0.5) # Wait for file write
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"Log file line count: {len(lines)}")
            print("Log history details:")
            for line in lines:
                print(f"  > {line.strip()}")
    else:
        print("❌ Log file was not created!")

if __name__ == "__main__":
    test_unified_logging()
