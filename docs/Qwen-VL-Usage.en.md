# Qwen-2.5-VL Usage Guide

This document explains how to perform object detection using the Qwen-2.5-VL model on the VisionAI-Platform.

## 1. Environment Setup (Virtual Environment)
Each experiment runs in an independent virtual environment to prevent library conflicts.

```bash
cd experiments/EX-002-QWEN-VL
# Activate virtual environment (Mac/Linux)
source venv/bin/activate
# Install required libraries
pip install -r requirements.txt
```

## 2. Offline Support
To run the model locally without an internet connection, you must pre-download the weights.

### Recommended Download Method (Snapshot Download)
Run the following script at the project root to save the model in `assets/weights/`.

```python
from huggingface_hub import snapshot_download

# Download Qwen-2.5-VL-3B-Instruct model
snapshot_download(
    repo_id="Qwen/Qwen2.5-VL-3B-Instruct",
    local_dir="assets/weights/Qwen2.5-VL-3B-Instruct",
    local_dir_use_symlinks=False
)
```

## 3. Library Utilization (Library Centralization)
This platform centrally manages core features in the `core/` directory.

### Model Call (`core/models`)
Load the model and perform image processing via the `QwenVLProcessor` class.
```python
from core.models.qwen_vl import QwenVLProcessor
processor = QwenVLProcessor()
```

### Image Utilities (`core/processing`)
Use `vision_utils.py` for common image drawing and preprocessing.
```python
from core.processing.vision_utils import draw_bboxes
```

## 3. Example Code
Refer to `experiments/EX-002-QWEN-VL/main.py` to extend experiments.

## 4. Library Information
- **transformers**: For model loading and inference
- **opencv-python**: For vision processing and visualization
- **torch**: Deep learning backend
