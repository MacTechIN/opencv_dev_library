# Qwen-2.5-VL Usage Guide (한글)

본 문서는 VisionAI-Platform에서 Qwen-2.5-VL 모델을 사용하여 물체 탐지를 수행하는 방법을 설명합니다.


## 1. 환경 설정 (Virtual Environment)

각 실험은 독립적인 가상환경에서 실행되어 라이브러리 충돌을 방지합니다.

```bash
cd experiments/EX-002-QWEN-VL
# 가상환경 활성화 (Mac/Linux)
# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
# 필수 라이브러리 설치
pip install -r requirements.txt
```


## 2. 오프라인 사용 (Offline Support)

인터넷 연결 없이 로컬에서 모델을 실행하려면 가중치를 미리 다운로드하고 환경을 설정해야 합니다.

export HF_TOKEN="YOUR_HF_TOKEN"
python3 core/utils/download_model.py


### 단계 1: 모델 가중치 사전 다운로드 (온라인 상태에서 1회 수행)
프로젝트에 포함된 전용 유틸리티를 실행하여 `assets/weights/`에 모델을 저장합니다.


```bash
# 프로젝트 루트에서 실행
python3 core/utils/download_model.py
```

또는 Python으로 직접 수행하려면 다음 코드를 사용하세요:

```python
from huggingface_hub import snapshot_download

# Qwen-2.5-VL-3B-Instruct 모델 다운로드
snapshot_download(
    repo_id="Qwen/Qwen2.5-VL-3B-Instruct",
    local_dir="assets/weights/Qwen2.5-VL-3B-Instruct",
    token="YOUR_HF_TOKEN" # (권장) 빠른 다운로드를 위해 토큰 설정
)
```

### 단계 2: 환경 변수 설정 (오프라인 모드)
Python 코드 내에서 라이브러리가 외부 서버에 접속하지 않도록 강제합니다.

```python
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
```

### 단계 3: 로컬 경로를 이용한 모델 로드
`from_pretrained` 호출 시 모델 이름 대신 **로컬 폴더 경로**를 전달합니다.

```python
from transformers import Qwen2_5_VForConditionalGeneration, AutoProcessor

model_path = "./assets/weights/Qwen2.5-VL-3B-Instruct"

model = Qwen2_5_VForConditionalGeneration.from_pretrained(
    model_path, 
    local_files_only=True,
    device_map="auto"
)
processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)
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
