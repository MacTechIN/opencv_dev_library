import numpy as np
import logging
from core.processing.face_utils import FaceUtils

def test_face_utils_robustness():
    print("🧪 [Test] FaceUtils 최적화 및 안정성 테스트 시작")
    
    # 1. 모델 부재 시 초기화 테스트 (에러 로그가 출력되어야 함)
    print("\n[Case 1] 잘못된 경로로 초기화 (에러 처리 확인)")
    face_module = FaceUtils(models_path="invalid/path")
    print(f"결과: is_ready = {face_module.is_ready}")
    
    # 2. 유효하지 않은 입력 프레임 테스트
    print("\n[Case 2] None 또는 빈 프레임 입력 테스트")
    boxes = face_module.detect_faces(None)
    print(f"None 입력 결과 (빈 리스트 예상): {boxes}")
    
    empty_frame = np.zeros((0, 0, 3), dtype=np.uint8)
    boxes = face_module.detect_faces(empty_frame)
    print(f"빈 프레임 입력 결과 (빈 리스트 예상): {boxes}")

    # 3. 분류 시 안정성 테스트
    print("\n[Case 3] 분류기 안정성 확인 (Unknown 반환 여부)")
    gender = face_module.classify_gender(None)
    age = face_module.classify_age(None)
    print(f"결과: Gender={gender}, Age={age} (모두 Unknown 예상)")

if __name__ == "__main__":
    test_face_utils_robustness()
