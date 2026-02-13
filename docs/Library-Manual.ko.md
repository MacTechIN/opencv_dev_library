# VisionAI-Platform Library Function Manual (한글)

이 문서는 VisionAI-Platform 라이브러리에 포함된 주요 함수와 클래스의 상세 사용법을 설명하는 공식 매뉴얼입니다.

---

## 0. 개발 환경 구성 (Virtual Environments)

본 플랫폼은 시스템의 안정성과 대용량 AI 모델의 효율적인 관리를 위해 가상환경을 이원화하여 운영합니다.

### 🔹 [루트 가상환경](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/.venv) (`.venv`)


- **용도**: 핵심 라이브러리(`core/`) 개발, 유틸리티 유지보수, 웹 서버 운영 및 범용 OpenCV 이미지 처리.

- **주요 패키지**: `opencv-python`, `numpy`, `requests` 등 표준 라이브러리.
- **사용법**: 일반적인 개발 및 `core` 모듈 수정 시 활성화합니다.


### 🔹 [실험 전용 가상환경](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/experiments/EX-002-QWEN-VL/venv) (`experiments/EX-002-QWEN-VL/venv`)


- **용도**: Qwen-VL 기반 Vision-Language 모델 추론, GPU 가석 실험 및 대용량 AI 의존성 테스트.

- **주요 패키지**: `torch`, `transformers`, `accelerate`, `pillow` 등 Deep Learning 특화 라이브러리.
- **특징**: 루트 환경과의 라이브러리 충돌(특히 PyTorch 버전 관리)을 방지하기 위해 독립적으로 구축되었습니다.
- **사용법**: Qwen-VL 엔진을 직접 실행하거나 관련 실험을 수행할 때 해당 디렉토리의 가상환경을 활성화해야 합니다.

---

## 1. Vision Processing (`core/processing/`)

### 🔹 [FaceUtils](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_utils.py)
얼굴 인식, 성별 및 연령 추론을 담당하는 유틸리티 클래스입니다.

#### **Initialize**
```python
from core.processing.face_utils import FaceUtils
utils = FaceUtils(models_path="assets/weights/face_models", use_opencl=True)
```
- `models_path`: Caffe 및 Torch 모델 파일(`face_net.caffemodel` 등)이 위치한 경로입니다.
- `use_opencl`: OpenCL 하드웨어 가속을 활성화하여 성능을 향상시킵니다.

#### **Example: 얼굴 탐지 및 성별 분석**
```python
import cv2
frame = cv2.imread("image.jpg")
face_boxes = utils.detect_faces(frame, conf_threshold=0.8)

for (x1, y1, x2, y2) in face_boxes:
    face_roi = frame[y1:y2, x1:x2]
    gender = utils.classify_gender(face_roi)
    age = utils.classify_age(face_roi)
    print(f"Detected: {gender}, Age: {age}")
```

---

### 🔹 [CentroidTracker](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/centroid_tracker.py)
탐지된 객체의 중심점을 계산하여 프레임 간 고유 ID를 유지하는 추적기입니다.

#### **Initialize**
```python
from core.processing.centroid_tracker import CentroidTracker
tracker = CentroidTracker(max_disappeared=30)
```
- `max_disappeared`: 객체가 화면에서 사라진 후 ID를 유지할 최대 프레임 수입니다.

#### **Example: 객체 추적 업데이트**
```python
# rects: 탐지된 얼굴들의 (x1, y1, x2, y2) 리스트
objects = tracker.update(rects)

for (objectID, centroid) in objects.items():
    # ID와 중심 좌표(x, y)를 사용하여 로직 수행
    cv2.putText(frame, f"ID {objectID}", (centroid[0]-10, centroid[1]-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
```

---

### 🔹 [FaceReID](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/reid_utils.py)
128차원 얼굴 특징 벡터(Embedding)를 추출하고 클라우드 데이터베이스와 대조하여 인물을 재식별합니다.

#### **Methods & Examples**
- `get_embedding(face_img: np.ndarray)`: 얼굴 이미지에서 특징 벡터를 추출합니다.
- `find_match(embedding: np.ndarray, threshold: float = 0.6)`: 기존 등록된 인물 중 일치하는 ID를 찾습니다.

```python
from core.processing.reid_utils import FaceReID
reid = FaceReID()

# 임베딩 추출 및 매칭
embedding = reid.get_embedding(face_roi)
matched_id = reid.find_match(embedding, threshold=0.5)

if matched_id:
    print(f"Welcome back, {matched_id}")
else:
    # 새 인물로 등록
    reid.register_face("User_ID:001", embedding)
```

---

### 🔹 [FaceProcessor](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_processor.py)
탐지, 추적, Re-ID 기능을 하나로 통합하여 실시간 영상 스트림 처리에 최적화된 클래스입니다.

#### **Example: 실시간 파이프라인 구현**
```python
from core.processing.face_processor import FaceProcessor
processor = FaceProcessor()

while True:
    ret, frame = cap.read()
    # process_frame 하나로 탐지+추적+인식 완료
    people = processor.process_frame(frame)
    
    for p in people:
        # p.id: 고유 ID (기존 인물 시 User_ID:xxx, 미등록 시 TRK_xxx)
        # p.rect: (x1, y1, x2, y2)
        cv2.rectangle(frame, (p.rect[0], p.rect[1]), (p.rect[2], p.rect[3]), (0, 255, 0), 2)
```

---

### 🔹 [MarketUtils](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/market_utils.py)
유동 인구 통계 및 상권 분석 데이터를 생성하는 비즈니스 로직 라이브러리입니다.

#### **Example: 유동 인구 분석 리포트**
```python
from core.processing.market_utils import MarketUtils
mu = MarketUtils()

# 방문 기록 (ID, 성별, 나이, 부가특징)
mu.record_visit(101, "Male", "(25-32)", {"wearing_hat": False})

# 통계 분석
flow_stats = mu.analyze_visitor_flow(interval_minutes=30)
print(f"Inflow: {flow_stats['inflow']}, Peak Hour: {flow_stats['peak_hour']}")

retention = mu.detect_visit_frequency()
print(f"Retention Rate: {retention['retention_rate']}%")
```

---

## 2. AI Model Wrappers (`core/models/`)

### 🔹 [QwenVLProcessor](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/models/qwen_vl.py)
Qwen-2.5-VL 모델을 이용하여 하이브리드 로딩 및 정밀 인물 분석을 수행합니다.

#### **Hybrid Loading**
인터넷 연결 상태와 로컬 가중치(`assets/weights`) 존재 여부에 따라 자동으로 로딩 모드를 전환합니다.

#### **Example: 통합 인물 분석 및 데이터 자산화**
```python
from core.models.qwen_vl import QwenVLProcessor
qwen = QwenVLProcessor()

# 1. 인물 탐지 및 종합 분석 실행
results = qwen.detect_and_analyze_persons("scene.jpg")

for res in results:
    # 2. 개별 인물 데이터 추출
    pid = res['id']
    dist = res['distance']    # 추정 거리 (m)
    loc = res['location']     # 3D 추정 위치 {'x', 'y', 'z'}
    vec = res['feature_vector'] # 표준화된 1D 속성 벡터
    
    print(f"[{pid}] Distance: {dist}m, Gender: {res['gender']}")
    print(f"Location Config: {loc}")

---

### 🔹 [WebAppSDK](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/web/web_utils.py)
웹 애플리케이션 개발 및 비전 결과 시각화를 위한 공용 인터페이스입니다.

#### **Example: 부트스트랩을 이용한 원스톱 초기화**
```python
from core.web.web_utils import WebAppSDK

# 1. 앱 시작에 필요한 모든 리소스(폴더, 모델 등)를 한 번에 초기화
context = WebAppSDK.bootstrap_vision_app(model_types=["qwen-vl"])

# 2. 초기화된 모델 꺼내 쓰기
qwen = context["models"]["qwen_vl"]
logger = context.get("logger") # 기본 로거 포함

print(f"App initialized at: {context['init_time']}")
```

#### **Core Functions**
- `bootstrap_vision_app(model_types=[...])`: 폴더 생성 및 모델 로딩 등 공통 시작 프로세스를 자동 처리합니다.
- `draw_analysis_overlay(frame, results)`: 분석 결과를 화면에 오버레이합니다.
- `frame_to_base64(frame)`: 웹 스트리밍을 위한 이미지 인코딩을 수행합니다.
```

#### **Core Functions**
- `vectorize_attributes(...)`: 성별(Numerical), 연령대(Mapped), 정규화된 BBox 좌표를 결합하여 머신러닝 모델이 이해할 수 있는 벡터를 생성합니다.
- `estimate_distance(...)`: 광학 중심과 객체 크기를 기반으로 물리적 거리를 계산합니다.
- `calculate_location(...)`: 거리 값과 화면 내 위치를 투영하여 공간 상의 좌표를 산출합니다.

---

## 3. App Development (웹개발) (`core/web/`) [NEW]

### 🔹 [WebAppSDK](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/web/web_utils.py)
웹 애플리케이션 개발 생산성을 높이기 위한 공통 라이브러리입니다.

#### **Example: 분석 결과 시각화 및 웹 전송**
```python
from core.web.web_utils import WebAppSDK
import cv2

# 1. 분석 결과 오버레이 그리기 (ID/성별/나이 표시)
visualized_frame = WebAppSDK.draw_analysis_overlay(frame, results)

# 2. 웹 스트리밍용 Base64 인코딩
base64_img = WebAppSDK.frame_to_base64(visualized_frame)

# 3. 표준 API 응답 생성
response = WebAppSDK.format_api_response("success", {"image": base64_img})
```

---

## 4. Support Utilities (`core/utils/`)

### 🔹 [VisionLogger](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/logger.py)
시스템 전역에서 일관된 포맷으로 로그를 기록하며, 파일 회전 기능을 지원합니다.

#### **Example: 로깅 활용**
```python
from core.utils.logger import get_logger
logger = get_logger("AnalysisEngine")

try:
    # 작업 수행
    logger.info("영상 분석을 시작합니다.")
except Exception as e:
    logger.error(f"오류 발생: {str(e)}")
```

---
> [!IMPORTANT]
> 본 매뉴얼의 예제 코드는 `core/` 디렉터리의 라이브러리 구현을 기준으로 하며, 최신 안정 버전을 따릅니다. 
> 새로운 속성이나 메서드가 추가될 경우 반드시 예제를 함께 업데이트해 주세요.
