# WebAppSDK 공통 초기화 프로세스(`bootstrap_vision_app`) 구현 계획

웹 애플리케이션이나 실험 스크립트 시작 시 반복되는 초기화 로직을 자동화하여 코드의 간결성과 유지보수성을 확보합니다.

## 제안된 설계: `bootstrap_vision_app`

가장 범용성이 높은 방식은 **컨텍스트 객체 반환(Context-Return) 패턴**입니다. 함수 하나만 호출하면 필요한 모든 객체(모델, 로거, 설정값)가 준비된 상태로 전달됩니다.

### 주요 기능
- **환경 감지**: 현재 장치(MPS, CUDA, CPU) 및 모델 가중치 경로 자동 판별.
- **통합 로딩**: `QwenVLProcessor` 등 주요 엔진의 인스턴스화 및 상태 체크.
- **정적 자원 준비**: 결과 데이터 저장 폴더(`results`, `logs`) 자동 생성.
- **로그 최적화**: 애플리케이션 시작 로그 및 하드웨어 가속 상태 리포트.

## 변경 사항

### 1. `core/web/web_utils.py` [MODIFY]
- `WebAppSDK` 클래스에 `@staticmethod`인 `bootstrap_vision_app` 추가.
- 설정값(dict)을 인자로 받아 유연한 초기화 지원.

### 2. `docs/Library-Manual.ko.md` [MODIFY]
- 새롭게 추가된 부트스트랩 함수의 사용법과 예제 추가.

## 검증 계획
- `experiments/EX-002-QWEN-VL/integrator.py`의 초기화 로직을 이 신규 함수로 교체하여 정상 작동 여부 확인.
