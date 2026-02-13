import numpy as np
import time
import datetime
from core.processing.face_utils import FaceUtils
from core.processing.reid_utils import FeatureBank
from core.processing.market_utils import MarketUtils

def run_actual_working_demo():
    print("🚀 [VisionAI] 통합 실무 라이브러리 작동 데모 시작")
    
    # 1. 초기화
    reid_bank = FeatureBank(threshold=0.7)
    market_stats = MarketUtils()
    
    # 가상의 특징 벡터 생성 (정규화된 128차원 벡터 예시)
    def create_mock_feature():
        # 양수만 있는 rand 대신 normal을 사용하여 벡터 간 변별력 확보
        f = np.random.normal(0, 1, 128)
        return f / np.linalg.norm(f)

    # 2. 시나리오: 3명의 인물이 화면에 등장 (인물 A, B, C)
    person_a_feature = create_mock_feature()
    person_b_feature = create_mock_feature()
    person_c_feature = create_mock_feature()
    
    print("\n[STEP 1] 불특정 객체 탐지 및 ID 부여")
    for i, feat in enumerate([person_a_feature, person_b_feature, person_c_feature]):
        uid = reid_bank.get_unique_id(feat)
        # 성별/연령은 모델 출력값으로 가정
        gender = "Male" if i % 2 == 0 else "Female"
        age = "(25-32)"
        
        # 방문 기록
        market_stats.record_visit(uid, gender, age, {"cloth_color": "Blue"})
        print(f"✅ 객체 탐지: ID-{uid} | 성별: {gender} | 연령: {age}")

    # 3. 인물 A가 화면에서 사라졌다가 다시 등장 (Re-ID 작동 확인)
    print("\n[STEP 2] 객체 재식별 (Re-ID) 테스트")
    # 인물 A의 특징 벡터에 약간의 노이즈 추가
    person_a_reentry = person_a_feature + np.random.normal(0, 0.05, 128)
    uid_reentry = reid_bank.get_unique_id(person_a_reentry)
    
    if uid_reentry == 1: # 인물 A의 기존 ID가 1임
        print(f"🎯 재식별 성공! ID-1 객체가 다시 등장했습니다. (동일인 판명)")
        market_stats.record_visit(uid_reentry, "Male", "(25-32)", {"status": "revisited"})

    # 4. 상권 분석 통계 산출
    print("\n[STEP 3] 상권 분석 데이터 변환 (통계)")
    
    # 시간대별 분포
    demo_stats = market_stats.aggregate_demographics_by_time()
    print(f"📊 시간대별 방문객: {demo_stats}")
    
    # 유동 인구 분석
    flow = market_stats.analyze_visitor_flow()
    print(f"📈 유입 인구 흐름: {flow}")
    
    # 재방문율 분석
    frequency = market_stats.detect_visit_frequency()
    print(f"♻️ 고객 유지율(Retention): {frequency['retention_rate']}%")

if __name__ == "__main__":
    # 라이브러리 경로 인식을 위해 상위 디렉토리에서 실행 권장
    run_actual_working_demo()
