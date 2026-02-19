import os
import sys
import cv2
import numpy as np

# 프로젝트 루트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.engines.qwen_sam_engine import QwenSAMEngine
from core.utils.logger import get_logger

logger = get_logger("EX-005-TESTER")

def main():
    print("\n" + "🌟" * 3 + " EX-005 Qwon-SAM 통합 테스트 " + "🌟" * 3)
    
    # 1. 엔진 초기화 - MPS 오류 발생 시 CPU 강제 사용
    engine = QwenSAMEngine(device="cpu")
    
    # 2. 테스트 이미지 경로 설정
    test_img = "experiments/EX-002-QWEN-VL/sample.jpg"
    if len(sys.argv) > 1:
        test_img = sys.argv[1]
        
    if not os.path.exists(test_img):
        logger.error(f"파일을 찾을 수 없습니다: {test_img}")
        return

    # 3. 브레인(Qwen) + 메스(SAM2) 하이브리드 세그멘테이션 실행
    print(f"🧐 분석 대상: {test_img}")
    print("🚀 Qwen-VL 탐지 및 SAM2 정밀 분할 시작...")
    
    results = engine.segment_with_qwen_guide(test_img, "Segment everyone in this image.")
    
    if not results:
        print("검출 결과가 없습니다.")
        return

    # 4. 결과 시각화 및 저장
    frame = cv2.imread(test_img)
    visualized = engine.draw_segmentation_results(frame, results)
    
    out_dir = "experiments/EX-005-QWEN-SAM/results"
    os.makedirs(out_dir, exist_ok=True)
    out_filename = f"seg_{os.path.basename(test_img)}"
    out_path = os.path.join(out_dir, out_filename)
    
    cv2.imwrite(out_path, visualized)
    print(f"✅ 테스트 완료! 결과 이미지 저장됨: {out_path}")
    print(f"📊 총 {len(results)}개의 객체가 정밀 분할되었습니다.")

if __name__ == "__main__":
    main()
