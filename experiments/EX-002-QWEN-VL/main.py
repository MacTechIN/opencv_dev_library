import os
import sys

# 프로젝트 루트 및 코어 라이브러리 경로 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from core.models.qwen_vl import QwenVLProcessor
from core.processing.vision_utils import draw_bboxes
import cv2

def run_experiment():
    print("--- Qwen-2.5-VL Object Detection Experiment Start ---")
    
    # 모델 초기화 (중앙 관리 라이브러리 사용)
    processor = QwenVLProcessor()
    
    # 테스트 이미지 경로 (예시)
    image_path = os.path.join(project_root, "data/test_image.jpg")
    
    # 1. 이미지 로드 및 전처리
    # frame = cv2.imread(image_path)
    
    # 2. 추론 (사람, 사물, 차량 등 탐지)
    # result_frame = processor.process(frame)
    
    # 3. 결과 저장
    # output_path = "experiments/EX-002-QWEN-VL/results/output.jpg"
    # cv2.imwrite(output_path, result_frame)
    
    print("실험 완료. 결과는 results/ 폴더를 확인하세요.")

if __name__ == "__main__":
    run_experiment()
