# Qwen-2.5-VL Usage Guide (한글)

본 문서는 VisionAI-Platform에서 Qwen-2.5-VL 모델을 사용하여 물체 탐지를 수행하는 방법을 설명합니다.

## 1. 환경 설정 (Virtual Environment)
각 실험은 독립적인 가상환경에서 실행되어 라이브러리 충돌을 방지합니다.

```bash
cd experiments/EX-002-QWEN-VL
# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
# 필수 라이브러리 설치
pip install -r requirements.txt
```

## 2. 오프라인 사용 (Offline Support)
인터넷 연결 없이 로컬에서 모델을 실행하려면 가중치를 미리 다운로드해야 합니다.

### 권장 다운로드 방법 (Snapshot Download)
프로젝트 루트에서 다음 스크립트를 실행하여 `assets/weights/`에 모델을 저장합니다.

```python
from huggingface_hub import snapshot_download

# Qwen-2.5-VL-3B-Instruct 모델 다운로드
snapshot_download(
    repo_id="Qwen/Qwen2.5-VL-3B-Instruct",
    local_dir="assets/weights/Qwen2.5-VL-3B-Instruct",
    local_dir_use_symlinks=False
)
```

## 3. 라이브러리 활용 (Library Centralization)
본 플랫폼은 핵심 기능을 `core/` 디렉토리에서 중앙 관리합니다.

### 모델 호출 (`core/models`)
`QwenVLProcessor` 클래스를 통해 모델을 로드하고 이미지 처리를 수행합니다.
```python
from core.models.qwen_vl import QwenVLProcessor
processor = QwenVLProcessor()
```

### 이미지 유틸리티 (`core/processing`)
공통된 이미지 드로잉 및 전처리는 `vision_utils.py`를 사용합니다.
```python
from core.processing.vision_utils import draw_bboxes
```

## 3. 예제 코드 (Example)
`experiments/EX-002-QWEN-VL/main.py`를 참고하여 실험을 확장할 수 있습니다.

## 4. 라이브러리 정보
- **transformers**: 모델 로드 및 추론용
- **opencv-python**: 영상 처리 및 시각화용
- **torch**: 딥러닝 백엔드
