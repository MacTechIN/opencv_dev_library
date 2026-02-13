# VisionAI-Platform Library Management & Coding Standards

이 문서는 본 플랫폼에서 라이브러리를 체계적으로 운영하고, 재사용 가능한 함수를 작성하는 표준 규칙을 정의합니다.

## 1. 함수 작성 표준 (Coding Standards)

함수는 **"읽기 쉽고, 예측 가능하며, 독립적"**이어야 합니다.

- **명명 규칙 (Naming)**: 
  - `snake_case`를 사용하며, `동사_명사` 형식을 지향합니다. (예: `draw_bboxes`, `preprocess_image`)
  - 의미가 명확하지 않은 약어는 피합니다. (`p_img` (X) -> `preprocess_image` (O))
- **타입 힌팅 (Type Hinting)**: 
  - Python의 type hints를 필수로 사용합니다.
  - 예: `def process(frame: np.ndarray) -> np.ndarray:`
- **문서화 (Docstrings)**: 
  - Google Style을 준수하며 **기능 설명, 매개변수(Args), 반환값(Returns), 예외(Raises)**를 명시합니다.
- **단일 책임 (Single Responsibility)**: 
  - 하나의 함수는 하나의 명확한 작업만 수행해야 합니다.

## 2. 라이브러리 승급 프로세스 (Promotion Process)

모든 코드가 처음부터 `core/`에 저장되지는 않습니다.

1.  **실험 단계 (Experimenting)**: 새로운 기능은 `experiments/EX-XXX/` 내부의 `utils.py`나 `main.py`에서 작성됩니다.
2.  **검증 단계 (Verification)**: 해당 기능이 실험에서 성공적으로 작동하고, **최소 2개 이상의 실험**에서 사용될 가능성이 보일 때 승급 후보가 됩니다.
3.  **코어 승급 (Promotion to Core)**:
    - 코드를 일반화(Generalization)하여 특정 실험에 의존적이지 않게 수정합니다.
    - `core/`의 적절한 하위 디렉토리로 이동합니다.
    - `{directory}+history.md`에 승급 이력을 기록합니다.

## 3. 디렉토리별 역할 분담

- `core/base/`: 모든 프로세서의 부모가 되는 추상 클래스와 인터페이스 정의.
- `core/processing/`: 이미지 필터링, ROI 추출, 색상 변환 등 **입력 -> 출력**이 명확한 순수 함수 위주.
- `core/models/`: AI 모델을 로드하고 추론하는 엔진 래퍼 클래스.
- `core/utils/`: 로깅, 파일 입출력, 시스템 체크 등 비즈니스 로직 외 지원 기능.

## 4. 버전 및 이력 관리 (History Tracking)

- 변경 사항이 발생하면 반드시 해당 디렉토리의 `history.md`에 기록합니다.
- **Breaking Change**(기존 코드를 깨뜨리는 변경)가 발생할 경우 버전을 `vX.0.0` 단위로 올리고, `docs/`에 마이그레이션 가이드를 작성합니다.

---

> [!TIP]
> **최고의 라이브러리는 문서 없이도 코드만 보고 사용법을 알 수 있는 라이브러리입니다.** 명확한 네이밍과 타입 힌팅에 가장 많은 공을 들이세요.
