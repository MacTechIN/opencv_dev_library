# VisionAI-Platform Library Function Manual (한글)

이 문서는 VisionAI-Platform 라이브러리에 포함된 주요 함수와 클래스의 상세 사용법을 설명하는 공식 매뉴얼입니다.

---

## 1. Vision Processing (`core/processing/`)

### 🔹 [FaceUtils](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_utils.py)
얼굴 인식, 성별 및 연령 추론을 담당하는 유틸리티 클래스입니다.

#### **Initialize**
```python
from core.processing.face_utils import FaceUtils
utils = FaceUtils(models_path="assets/weights/face_models", use_opencl=True)
```
- `models_path`: Caffe 및 Torch 모델 파일이 위치한 경로.
- `use_opencl`: OpenCL 하드웨어 가속 사용 여부.

#### **Methods**
- `detect_faces(frame: np.ndarray, conf_threshold: float = 0.7) -> List[Tuple[int, int, int, int]]`
    - 이미지에서 얼굴을 탐지하여 `(x1, y1, x2, y2)` 사각형 리스트를 반환합니다.
- `classify_gender(face_img: np.ndarray) -> str`
    - 잘려진 얼굴 이미지에서 성별(`Male`, `Female`)을 추론합니다.
- `classify_age(face_img: np.ndarray) -> str`
    - 잘려진 얼굴 이미지에서 연령대(`(0-2)`, `(4-6)` 등 8단계)를 추론합니다.
- `get_face_embedding(face_img: np.ndarray) -> Optional[np.ndarray]`
    - 얼굴 이미지에서 128차원의 특징 벡터(Embedding)를 추출합니다.

---

### 🔹 [CentroidTracker](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/centroid_tracker.py)
탐지된 객체에 고유 ID를 부여하고 프레임 간에 추적을 유지합니다.

#### **Initialize**
```python
from core.processing.centroid_tracker import CentroidTracker
tracker = CentroidTracker(max_disappeared=20)
```
- `max_disappeared`: 객체가 화면에서 사라진 후 ID를 삭제하기 전까지 대기하는 최대 프레임 수.

#### **Methods**
- `update(rects: List[Tuple[int, int, int, int]]) -> OrderedDict`
    - 탐지된 박스 좌표들을 입력받아 현재 활성화된 `ID -> 중심점(x, y)` 매핑을 반환합니다.

---

### 🔹 [FaceProcessor](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_processor.py)
탐지, 추적, Re-ID를 통합하여 사용자가 한 프레임씩 처리할 수 있게 돕는 상위 클래스입니다.

#### **Initialize**
```python
from core.processing.face_processor import FaceProcessor
processor = FaceProcessor(max_disappeared=40, match_threshold=0.6)
```

#### **Methods**
- `process_frame(frame: np.ndarray) -> List[Person]`
    - 한 프레임을 처리하여 `Person` 객체(ID, 좌표, 성별, 나이 등 포함) 리스트를 반환합니다.

---

### 🔹 [MarketUtils](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/market_utils.py)
상권 분석 및 유동 인구 분석을 위한 통계 도구입니다.

#### **Methods**
- `record_visit(obj_id: int, gender: str, age: str, features: Dict[str, Any])`
    - 방문자의 속성을 ID와 함께 기록합니다.
- `aggregate_demographics_by_time() -> Dict`
    - 시간대별 방문자 분포 통계를 반환합니다.
- `analyze_visitor_flow(interval_minutes: int = 60) -> Dict`
    - 최근 N분간의 유입량, 유출량, 피크 시간대를 분석합니다.

---

## 2. Support Utilities (`core/utils/`)

### 🔹 [VisionLogger](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/logger.py)
전역 싱글톤 로깅 인스턴스를 제공합니다.

#### **Usage**
```python
from core.utils.logger import get_logger
logger = get_logger("MyModule")
logger.info("작업 시작")
```
- 로그 파일은 `logs/vision_ai.log`에 저장되며, 5MB 단위로 최대 5개까지 백업(Rotate)됩니다.

---

## 3. 통합 사용 예제 (Example)

```python
import cv2
from core.processing.face_processor import FaceProcessor
from core.utils.logger import get_logger

logger = get_logger("Main")
processor = FaceProcessor()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # 통합 프로세싱 실행
    people = processor.process_frame(frame)
    
    for p in people:
        x1, y1, x2, y2 = p.rect
        # 화면에 결과 가시화
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{p.id} {p.gender} {p.age}", (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("VisionAI Real-time Pipeline", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
```

---
> [!IMPORTANT]
> 본 매뉴얼은 최신 소스 코드를 기준으로 작성되었습니다. 
> 함수 인터페이스나 파라미터가 변경될 경우 반드시 문서를 동기화해 주세요.
