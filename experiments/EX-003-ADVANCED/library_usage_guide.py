import cv2
from core.web.web_utils import WebAppSDK
from core.models.qwen_vl import QwenVLProcessor
from core.utils.logger import get_logger

logger = get_logger("LibraryGuide")

def main():
    """
    [라이브러리 사용 가이드] 시각화 기능 활용 예시
    
    1. 라이브러리 불러오기:
       from core.web.web_utils import WebAppSDK
    
    2. 주요 함수:
       WebAppSDK.draw_analysis_overlay(이미지, 분석결과_리스트)
    """
    
    # 1. 초기화 (모델 및 SDK)
    logger.info("Initializing library components...")
    context = WebAppSDK.bootstrap_vision_app(model_types=["qwen-vl"])
    qwen = context["models"]["qwen_vl"]
    
    # 2. 이미지 로드
    img_path = "experiments/EX-002-QWEN-VL/sample.jpg"
    frame = cv2.imread(img_path)
    
    if frame is None:
        logger.error("Sample image not found.")
        return

    # 3. 인공지능 분석 수행
    # 리턴 값 구조: [{'id': 1, 'bbox': [...], 'gender': 'Female', 'age': '20s', ...}, ...]
    logger.info("Running AI analysis...")
    results = qwen.detect_and_analyze_persons(frame)

    # 4. 라이브러리 함수를 사용한 시각화 (남/여 표시 기능 포함)
    # core/web/web_utils.py 내의 draw_analysis_overlay를 호출합니다.
    logger.info("Visualizing results using WebAppSDK...")
    vis_frame = WebAppSDK.draw_analysis_overlay(frame, results)

    # 5. 결과 저장 및 확인
    output_path = "results/library_vis_test.jpg"
    cv2.imwrite(output_path, vis_frame)
    logger.info(f"✅ 결과물이 저장되었습니다: {output_path}")

if __name__ == "__main__":
    main()
