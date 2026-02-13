import os
import sys
import cv2
import torch
import numpy as np
from PIL import Image

# 프로젝트 루트를 경로에 추가 (core 모듈 임포트용)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.models.qwen_vl import QwenVLProcessor
from core.utils.logger import get_logger

logger = get_logger("EX-002-QWEN-VL")

def run_experiment(image_path: str, prompt: str = "Describe this image in detail."):
    """
    Qwen-VL 모델을 사용하여 이미지를 분석하는 실험을 수행합니다.
    """
    logger.info(f"🚀 실험 시작: {image_path}")
    
    if not os.path.exists(image_path):
        logger.error(f"❌ 이미지를 찾을 수 없습니다: {image_path}")
        return

    # 모델 초기화
    try:
        processor = QwenVLProcessor()
        logger.info("✅ 모델 로딩 완료")
    except Exception as e:
        logger.error(f"❌ 모델 로딩 실패: {e}")
        return

    # 분석 수행
    try:
        # detect_objects 메서드를 사용하여 분석 (내부적으로 로깅 수행)
        result_text = processor.detect_objects(image_path, prompt=prompt)
        
        logger.info(f"🔍 분석 결과:\n{result_text}")
        
        # 결과 저장
        os.makedirs("results", exist_ok=True)
        result_file = os.path.join("results", f"result_{os.path.basename(image_path)}.txt")
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Result:\n{result_text}\n")
        logger.info(f"💾 결과가 저장되었습니다: {result_file}")

    except Exception as e:
        logger.error(f"❌ 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    # 테스트용 샘플 이미지 경로 (필요시 수정)
    sample_image = "sample.jpg" # 이 폴더에 이미지를 준비하거나 전체 경로 입력
    
    if len(sys.argv) > 1:
        sample_image = sys.argv[1]
        
    run_experiment(sample_image)
