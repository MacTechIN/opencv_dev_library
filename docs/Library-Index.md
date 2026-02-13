# VisionAI-Platform Library Index (Master)

이 문서는 플랫폼에 구현된 모든 코어 라이브러리와 주요 기능들을 한눈에 파악할 수 있는 통합 색인입니다.

## 📂 Core Libraries

### 1. Vision Processing (`core/processing/`)
이미지 및 영상 처리의 핵심 엔진 루틴입니다.

#### 🔹 [vision_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/vision_utils.py)
- **설명**: 이미지 리사이징, 색상 변환, ROI 추출 등 범용 비전 유틸리티.
- **원리**: OpenCV의 최적화된 C++ 백엔드 함수들을 활용한 효율적 행렬 연산.
- **예제**: `img = VisionUtils.resize_with_padding(frame, (640, 640))`

#### 🔹 [face_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_utils.py)
- **설명**: 얼굴 인식 및 성별/연령 분석 기능 제공.
- **원리**: Caffe DNN 모델을 사용하여 얼굴의 특징점(Feature)을 추출하고 사전 학습된 분류기를 통해 추론.
- **예제**: `gender = FaceUtils.classify_gender(face_img)`

#### 🔹 [reid_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/reid_utils.py) [NEW]
- **설명**: 객체 재식별(Re-ID) 및 고유 ID 관리.
- **원리**: 특징 벡터 간의 코사인 유사도를 계산하여 화면에서 사라졌다 나타난 객체를 동일인으로 식별.
- **예제**: `unique_id = feature_bank.get_unique_id(current_vector)`

#### 🔹 [market_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/market_utils.py) [NEW]
- **설명**: 상권 분석 및 유동 인구 분석 통계 엔진.
- **원리**: 시간대별 인구 분포 집계 및 누적 방문자 수 계산.
- **예제**: `stats = market_utils.aggregate_demographics_by_time()`

### 2. AI Model Wrappers (`core/models/`)

#### 🔹 [qwen_vl.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/models/qwen_vl.py)
- **설명**: Qwen-2.5-VL 기반 고성능 멀티모달 객체 탐지 인터페이스.
- **원리**: Transformer 기반 Vision-Language 모델로, 텍스트 쿼리와 이미지를 동시 임베딩하여 연관성 추론.
- **예제**: `results = qwen.detect(image, query="Find all people")`

### 3. Support Utilities (`core/utils/`)
시스템 운영 및 개발 지원 도구입니다.
- **[download_model.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/download_model.py)**: Hugging Face 고속 모델 다운로더.

## 🧪 Experiments Traceability
성공한 실험들이 라이브러리화된 이력입니다.
- **EX-001-FACE**: 얼굴 분석 기술 (성별/연령) -> `face_utils.py` 승급 완료.
- **EX-002-QWEN-VL**: 물체 탐지 기술 -> `qwen_vl.py` 이관 완료.

---
> [!NOTE]
> 새로운 라이브러리를 추가할 때는 반드시 이 Index 문서에 등록하여 가독성을 유지해 주세요.
