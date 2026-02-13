import os
import time

def test_unified_logging():
    print("🚀 [Test] 통합 로깅 시스템 작동 확인")
    
    # 1. 로그 파일 존재 여부 확인 전 삭제 (깨끗한 테스트)
    log_dir = "logs"
    log_file = os.path.join(log_dir, "vision_ai.log")
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
        except PermissionError:
            print("⚠️ 로그 파일이 다른 프로세스에서 사용 중입니다. 기존 파일에 이어서 기록합니다.")
    
    # 2. 각 모듈 호출 (실패 시 에러 로그 생성 확인)
    print("\n--- 모듈별 로깅 발생 시작 ---")
    
    try:
        from core.processing.face_utils import FaceUtils
        face = FaceUtils(models_path="core/models/invalid") # 에러 로깅 유도
    except Exception as e:
        print(f"FaceUtils 테스트 스킵 또는 에러: {e}")

    try:
        from core.processing.market_utils import MarketUtils
        market = MarketUtils()
        market.record_visit(101, "Male", "25-32", {"color": "red"})
    except Exception as e:
        print(f"MarketUtils 테스트 실패: {e}")

    try:
        from core.processing.reid_utils import FeatureBank
        reid = FeatureBank()
        reid.clear_old_features(300)
    except Exception as e:
        print(f"ReID 테스트 실패: {e}")

    try:
        from core.models.qwen_vl import QwenVLProcessor
        qwen = QwenVLProcessor()
    except Exception as e:
        print(f"QwenVL 테스트 스킵 (torch 미설치 등): {e}")
    
    # 3. 로그 파일 확인
    print("\n--- 로그 파일 기록 확인 ---")
    time.sleep(0.5) # 파일 쓰기 시간 대기
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"로그 파일 줄 수: {len(lines)}")
            print("로그 기록 내역:")
            for line in lines:
                print(f"  > {line.strip()}")
    else:
        print("❌ 로그 파일이 생성되지 않았습니다!")

if __name__ == "__main__":
    test_unified_logging()
