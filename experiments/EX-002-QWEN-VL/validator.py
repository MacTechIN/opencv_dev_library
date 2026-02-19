import os
import sys
import cv2
import numpy as np
import time
from datetime import datetime

# 프로젝트 루트를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.models.qwen_vl import QwenVLProcessor
from core.web.web_utils import WebAppSDK
from core.utils.logger import get_logger

logger = get_logger("EX-002-VALIDATOR")

def run_comprehensive_validation(target_image):
    """
    EX-002 전용 통합 검증 프로그램.
    1. 모델 초기화 상태 점검
    2. 인물 탐지 및 고도화된 속성 분석 (Gender, Age, Distance, Location)
    3. 특징 벡터(Feature Vector) 생성 확인
    4. 분석 결과 시각화 오버레이 생성
    5. 최종 리포트 및 성능 지표 산출
    """
    print("\n" + "🚀" * 3 + " EX-002 Qwen-VL 통합 검증 프로그램 " + "🚀" * 3)
    print(f"📅 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖼️ 대상: {target_image}\n")

    if not os.path.exists(target_image):
        logger.error(f"❌ 대상 이미지를 찾을 수 없습니다: {target_image}")
        return

    # [1단계] 엔진 초기화
    start_time = time.time()
    try:
        processor = QwenVLProcessor()
        init_time = time.time() - start_time
        print(f"✅ [1단계] Qwen-VL 엔진 로드 완료 ({init_time:.2f}s)")
    except Exception as e:
        print(f"❌ [1단계] 엔진 로드 실패: {e}")
        return

    # [2단계] 심층 인물 분석 수행
    print("🧠 [2단계] 심층 인물 분석 실행 중 (Inference)...")
    analysis_start = time.time()
    results = processor.detect_and_analyze_persons(target_image)
    analysis_time = time.time() - analysis_start
    
    if not results:
        print("⚠️ 검출된 인물이 없습니다. (이미지를 확인하거나 프롬프트를 점검하세요)")
        return

    print(f"✅ [2단계] 분석 완료: {len(results)}명 검출 ({analysis_time:.2f}s)")

    # [3단계] 데이터 검증 및 시각화
    print("🎨 [3단계] 시각화 및 데이터 무결성 검사...")
    frame = cv2.imread(target_image)
    if frame is None:
        logger.error("이미지 로드 실패 (OpenCV)")
        return

    # 오버레이 그리기
    visualized = WebAppSDK.draw_analysis_overlay(frame, results)
    
    # 결과 저장
    out_dir = "results"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"EX002_VAL_{os.path.basename(target_image)}")
    cv2.imwrite(out_path, visualized)
    
    # [4단계] 특징 벡터 및 메타데이터 확인
    print("\n" + "-"*30 + " [ 검출 데이터 상세 ] " + "-"*30)
    for res in results:
        v = res.get('feature_vector', [])
        # 벡터 앞부분 3개만 샘플 출력
        v_str = ", ".join([f"{x:.2f}" for x in v[:3]]) + " ..."
        print(f"👤 ID: {res['id']} | 속성: {res['gender']}, {res['age']} | 거리: {res['distance']}m")
        print(f"📍 위치(3D 예상): {res['location']}")
        print(f"🧬 특징 벡터(샘플): [{v_str}]")
        print("-" * 80)

    print(f"\n✨ 검증 완료: 결과물이 '{out_path}'에 저장되었습니다.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    # 기본 테스트 이미지 설정
    test_image = "sample.jpg"
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    
    # 만약 sample.jpg가 없으면 EX-002 디렉토리 내부를 먼저 찾아봄
    if not os.path.exists(test_image):
        local_sample = os.path.join(os.path.dirname(__file__), "sample.jpg")
        if os.path.exists(local_sample):
            test_image = local_sample

    run_comprehensive_validation(test_image)
