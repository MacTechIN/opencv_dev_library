import os
import sys
import cv2
import numpy as np
import time

# 프로젝트 루트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.engines.qwen_sam_engine import QwenSAMEngine
from core.utils.logger import get_logger

logger = get_logger("EX-005-COMPREHENSIVE-TESTER")

def run_test(engine, image_path, output_name):
    if not os.path.exists(image_path):
        logger.warning(f"Skipping: File not found -> {image_path}")
        return

    print(f"\n--- Testing: {os.path.basename(image_path)} ---")
    start_time = time.time()
    
    # Qwen-VL 탐지 + SAM2 세그멘테이션
    results = engine.segment_with_qwen_guide(image_path, "Detect and segment all people and main objects.")
    
    elapsed = time.time() - start_time
    print(f"⏱️ Elapsed Time: {elapsed:.2f}s | Detected: {len(results)}")

    if not results:
        return

    # 결과 시각화
    frame = cv2.imread(image_path)
    visualized = engine.draw_segmentation_results(frame, results)
    
    out_dir = "experiments/EX-005-QWEN-SAM/results"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, output_name)
    
    cv2.imwrite(out_path, visualized)
    print(f"✅ Saved result to: {out_path}")

def main():
    print("\n" + "🚀" * 3 + " EX-005 Qwon-SAM Comprehensive Multi-Scene Test " + "🚀" * 3)
    
    # 엔진 초기화 (여기서 엔진이 무거우므로 한 번만 초기화)
    engine = QwenSAMEngine()
    
    # 다양한 테스트 시나리오
    test_scenarios = [
        ("experiments/EX-002-QWEN-VL/sample.jpg", "test_01_street.jpg"),
        ("experiments/EX-003-ADVANCED/camera_test.jpg", "test_02_camera.jpg"),
        ("experiments/EX-003-ADVANCED/deco_scene.jpg", "test_03_deco.jpg"),
        ("sample.jpg", "test_04_root_sample.jpg")
    ]

    for img_path, out_name in test_scenarios:
        run_test(engine, img_path, out_name)

    print("\n" + "=" * 70)
    print("✨ All tests completed. Check 'experiments/EX-005-QWEN-SAM/results/' for outputs.")

if __name__ == "__main__":
    main()
