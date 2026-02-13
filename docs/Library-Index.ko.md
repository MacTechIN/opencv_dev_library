# VisionAI-Platform Library Index (Master) (한글)

이 문서는 플랫폼에 구현된 모든 코어 라이브러리와 주요 기능들을 한눈에 파악할 수 있는 통합 색인입니다.
상세한 함수 사용법은 [라이브러리 함수 사용 매뉴얼](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/docs/Library-Manual.ko.md)을 참조하세요.

## 📂 Core Libraries

### 1. Vision Processing (`core/processing/`)
이미지 및 영상 처리의 핵심 엔진 루틴입니다.

#### 🔹 [vision_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/vision_utils.py) [Official]
- **설명**: 이미지 리사이징, 색상 변환, ROI 추출 등 범용 비전 유틸리티.
- **원리**: OpenCV의 최적화된 C++ 백엔드 함수들을 활용한 효율적 행렬 연산.

| 함수 | 설명 |
| :--- | :--- |
| `draw_bboxes(image, bboxes, labels)` | 이미지에 바운딩 박스와 라벨을 그립니다. |
| `resize_image(image, target_size)` | 이미지를 지정된 크기로 리사이징합니다. |

#### 🔹 [face_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_utils.py) [Official]
- **설명**: 얼굴 인식 및 성별/연령 분석 기능 제공.
- **원리**: Caffe DNN 모델을 사용하여 얼굴의 특징점(Feature)을 추출하고 사전 학습된 분류기를 통해 추론.

| 함수 | 설명 |
| :--- | :--- |
| `detect_faces(frame, conf_threshold)` | 프레임에서 얼굴을 탐지하고 좌표 리스트를 반환합니다. |
| `classify_gender(face_img)` | 얼굴 이미지에서 성별(Male/Female)을 분류합니다. |
| `classify_age(face_img)` | 얼굴 이미지에서 연령대(8단계)를 추정합니다. |
| `get_face_embedding(face_img)` | 얼굴 이미지에서 128차원 특징 벡터를 추출합니다. |

#### 🔹 [reid_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/reid_utils.py) [Official]
- **설명**: 객체 재식별(Re-ID) 및 고유 ID 관리.
- **원리**: 특징 벡터 간의 코사인 유사도를 계산하여 화면에서 사라졌다 나타난 객체를 동일인으로 식별.

| 클래스 / 함수 | 설명 |
| :--- | :--- |
| `FaceReID(model_path)` | 사전 학습된 모델을 사용하여 Re-ID 시스템을 초기화합니다. |
| `get_embedding(face_img)` | 얼굴 이미지에서 128차원 특징 벡터를 추출합니다. |
| `find_match(embedding, threshold)` | 갤러리에서 가장 유사한 아이덴티티를 찾습니다. |
| `register_face(face_id, embedding)` | 새로운 아이덴티티를 클라우드/로컬 갤러리에 등록하거나 업데이트합니다. |

#### 🔹 [centroid_tracker.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/centroid_tracker.py) [Official]
- **설명**: 중심점(Centroid) 기반 객체 추적 알고리즘.
- **원리**: 연속된 프레임 간의 유클리드 거리를 계산하여 객체의 ID를 유지하고 사라진 객체를 관리합니다.

| 클래스 / 함 수 | 설명 |
| :--- | :--- |
| `CentroidTracker(max_disappeared)` | 추적기를 초기화합니다. (부재 유지 프레임 설정) |
| `update(rects)` | 탐지된 사각형 좌표들을 입력받아 업데이트된 ID와 중심점 맵을 반환합니다. |

#### 🔹 [face_processor.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_processor.py) [New]
- **설명**: 얼굴 탐지, 추적 및 재식별을 통합 관리하는 상위 레벨 모듈.
- **원리**: `FaceUtils`, `CentroidTracker`, `FaceReID`를 조정하여 아이덴티티를 관리.

| 클래스 / 함수 | 설명 |
| :--- | :--- |
| `FaceProcessor(...)` | 탐지, 추적 및 Re-ID 모듈을 초기화합니다. |
| `process_frame(frame)` | ID, 좌표, 속성을 포함한 `Person` 객체 리스트를 반환합니다. |
| `cleanup(max_age_seconds)` | 갤러리에서 오래된 아이덴티티를 제거합니다. |

#### 🔹 [market_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/market_utils.py) [Official]
- **설명**: 상권 분석 및 유동 인구 분석 통계 엔진.
- **원리**: 시간대별 인구 분포 집계 및 누적 방문자 수 계산.

| 클래스 / 함수 | 설명 |
| :--- | :--- |
| `record_visit(id, gender, age, features)` | 방문자의 특성과 입장 시간을 기록합니다. |
| `aggregate_demographics_by_time()` | 시간대별 성별/연령 분포를 집계합니다. |
| `analyze_visitor_flow(interval)` | 지정된 시간 동안의 유입/유출 및 피크 타임을 분석합니다. |
| `detect_visit_frequency()` | 재방문자 비율 및 신규 방문자 통계를 분석합니다. |

### 2. AI Model Wrappers (`core/models/`)

#### 🔹 [AI Models](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/models/)
- **설명**: Qwen-2.5-VL 기반 고성능 멀티모달 객체 탐지 인터페이스.
- **원리**: 인터넷 연결 상태에 따른 하이브리드 자동 스위칭 로직.

| 함수 | 설명 |
| :--- | :--- |
| `detect_and_analyze_persons(image)` | 인물 탐지, 성별, 나이 분석 및 거리/벡터화를 통합 수행합니다. |
| `vectorize_attributes(id, g, a, b)` | 인물 속성을 표준화된 1D 특징 벡터로 변환합니다. |
| `estimate_distance(bbox)` | 신체 크기를 기반으로 카메라와의 물리적 거리를 추정합니다. |
| `calculate_location(bbox, dist)` | 2D 좌표와 거리를 결합하여 3D 공간 상의 위치를 산출합니다. |

### 3. Support Utilities (`core/utils/`)

#### 🔹 [logger.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/logger.py) [Official]
- **설명**: 시스템 전역 통합 로깅 시스템.
- **원리**: 싱글톤 패턴으로 구현되어 콘솔 출력과 파일 회전(Rotation)을 동시에 처리.

| 함수 | 설명 |
| :--- | :--- |
| `get_logger(name)` | 모듈별 이름을 가진 로거 인스턴스를 반환합니다. |

#### 🔹 [download_model.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/download_model.py) [Support]
- **설명**: Hugging Face 고속 모델 다운로더.

## 🧪 Experiments Traceability
성공한 실험들이 라이브러리화된 이력입니다.
- **EX-001-FACE**: 얼굴 분석 기술 (성별/연령) -> `face_utils.py` 승급 완료.
- **EX-002-QWEN-VL**: 물체 탐지 기술 -> `qwen_vl.py` 이관 완료.

---
> [!NOTE]
> 새로운 라이브러리를 추가할 때는 반드시 이 Index 문서에 등록하여 가독성을 유지해 주세요.
