import cv2
import numpy as np
from core.web.web_utils import WebAppSDK
from core.processing.feature_tracker import FeatureMatchTracker
from core.utils.logger import get_logger

logger = get_logger("PhotoTest")

def run_photo_test(image_path: str):
    # 1. 환경 초기화
    context = WebAppSDK.bootstrap_vision_app(model_types=["qwen-vl"])
    qwen = context["models"].get("qwen_vl")
    tracker = FeatureMatchTracker(max_disappeared=50, feature_weight=0.8)
    
    if not qwen:
        logger.error("❌ Qwen-VL 모델 로드 실패")
        return

    # 2. 이미지 로드
    frame = cv2.imread(image_path)
    if frame is None:
        logger.error(f"❌ 이미지를 찾을 수 없음: {image_path}")
        return

    # 3. 인공지능 정밀 분석 (Qwen-VL)
    logger.info(f"🧠 {image_path} 분석 시작...")
    analysis_results = qwen.detect_and_analyze_persons(frame)
    
    # 4. 트래커와 연동
    rects = []
    features = []
    height, width = frame.shape[:2]
    
    for res in analysis_results:
        ymin, xmin, ymax, xmax = res['bbox']
        # 1000-scale 좌표를 실제 픽셀 좌표로 변환
        rect = [
            int(xmin * width / 1000), 
            int(ymin * height / 1000), 
            int(xmax * width / 1000), 
            int(ymax * height / 1000)
        ]
        rects.append(rect)
        features.append(np.array(res['feature_vector']))

    # 트래커 업데이트 (ID 할당)
    tracked_objects = tracker.update(rects, features)
    
    # 시각화를 위한 가상 궤적 데이터 생성 (포토 테스트용)
    history = {}
    for obj_id, centroid in tracked_objects.items():
        # 과거 3개 지점이 있었던 것처럼 시뮬레이션
        history[obj_id] = [
            (int(centroid[0] - 30), int(centroid[1] - 30)),
            (int(centroid[0] - 15), int(centroid[1] - 15)),
            (int(centroid[0]), int(centroid[1]))
        ]

    # 5. 결과 시각화
    # 분석 오버레이 (박스, 성별, 나이, 거리)
    vis_frame = WebAppSDK.draw_analysis_overlay(frame, analysis_results)
    # 궤적 오버레이 (이동 경로)
    vis_frame = WebAppSDK.draw_trajectories(vis_frame, history)

    # 6. 저장
    output_path = "results/photo_test_result.jpg"
    cv2.imwrite(output_path, vis_frame)
    logger.info(f"✅ 테스트 결과 저장 완료: {output_path}")
    
    # 결과 요약 출력
    print("\n" + "="*50)
    print(f"📊 분석 결과 (총 {len(analysis_results)}명 탐지)")
    for res in analysis_results:
        print(f"- ID {res['id']}: {res['gender']}, {res['age']}, 거리 {res['distance']}m")
    print("="*50 + "\n")

if __name__ == "__main__":
    sample_img = "experiments/EX-002-QWEN-VL/sample.jpg"
    run_photo_test(sample_img)
