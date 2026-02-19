# Qwen-VL AI 인물 분석 시스템 구현 상세 (Implementation Details)

이 문서는 `experiments/EX-002-QWEN-VL` 과정에서 구축된 인공지능 분석 시스템의 기술적 상세 내용을 히스토리 기반으로 요약한 보고서입니다.

## 🧠 시스템 아키텍처
Qwen-2.5-VL 3B 모델을 백엔드로 사용하여 이미지 내 인물을 탐지하고 속성을 분석하는 정밀 파이프라인입니다.

### 1. 주요 기능
- **멀티모달 객체 탐지**: 이미지 내 모든 인물의 BBox(Bounding Box) 좌표 추출.
- **정밀 속성 분석**: 성별, 연령대(10s, 20s 등) 자동 분류.
- **3D 공간 좌표 추정**: BBox의 높이를 기반으로 카메라로부터의 거리(Z-axis) 및 3D 위치(X, Y, Z) 계산.
- **속성 벡터화 (Attribute Vectorization)**: [성별, 연령, normalize_x, normalize_y, w, h] 구성의 1D 특징 벡터 생성.

### 2. 기술적 해결 과제 및 최적화
- **Parsing Robustness**: 모델의 출력이 Free-text, JSON 등으로 가변적인 문제를 Regex + JSON 유연 파싱 로직으로 해결.
- **Tensor Dimension Mismatch**: 입력 이미지의 해상도가 모델 입력 한계(1280px)를 넘지 않도록 자동 리사이징 로직 구현.
- **Hybrid Weight Loading**: 로컬 자산(`assets/weights`) 우선 로드 및 HuggingFace 온라인 폴백 시스템 구축.
- **Zero Detection 예외 처리**: 탐지 결과가 없을 시 사용자에게 원인을 알리고 빈 리스트를 반환하는 안정성 확보.

### 3. 주요 핵심 함수 (core.models.qwen_vl)
- `detect_and_analyze_persons(image)`: 전체 분석 수행 엔진.
- `vectorize_attributes(...)`: 하위 ML 작업을 위한 데이터 정규화.
- `estimate_distance(...)`: 광학 수식을 이용한 실제 거리 측정.
- `generate_markdown_report(...)`: 분석 결과를 마크다운 형태의 테이블로 기록.

## 📈 진행 현황 및 히스토리
- **v0.8.0**: Qwen-VL 기본 엔진 탑재 및 3D 거리 추정 기능 추가.
- **v0.8.5**: 웹 UI 트래킹 궤적 시각화 연동 및 리포트 생성기 보완.
- **Next**: 다중 객체 영구 추단(Persistent Tracking) 안정화 및 벡터 DB 연동.
