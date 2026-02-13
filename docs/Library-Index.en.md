# VisionAI-Platform Library Index (Master)

This document is a unified index that provides an at-a-glance overview of all core libraries and key features implemented in the platform.

## 📂 Core Libraries

### 1. Vision Processing (`core/processing/`)
Key engine routines for image and video processing.

#### 🔹 [vision_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/vision_utils.py) [Official]
- **Description**: General-purpose vision utilities for image resizing, color conversion, ROI extraction, etc.
- **Principle**: Efficient matrix operations utilizing OpenCV's optimized C++ backend functions.
- **Example**: `img = VisionUtils.resize_with_padding(frame, (640, 640))`

#### 🔹 [face_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/face_utils.py) [Official]
- **Description**: Provides face recognition and gender/age analysis features.
- **Principle**: Extracts face features using the Caffe DNN model and infers using pre-trained classifiers.
- **Example**: `gender = FaceUtils.classify_gender(face_img)`

#### 🔹 [reid_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/reid_utils.py) [Official]
- **Description**: Object Re-Identification (Re-ID) and unique ID management.
- **Principle**: Identifies objects that disappear and reappear as the same person by calculating cosine similarity between feature vectors.
- **Example**: `unique_id = feature_bank.get_unique_id(current_vector)`

#### 🔹 [market_utils.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/processing/market_utils.py) [Official]
- **Description**: Commercial analysis and floating population analysis statistics engine.
- **Principle**: Aggregates population distribution by time and calculates cumulative visitor counts.
- **Example**: `stats = market_utils.aggregate_demographics_by_time()`

### 2. AI Model Wrappers (`core/models/`)

#### 🔹 [qwen_vl.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/models/qwen_vl.py) [Official]
- **Description**: High-performance multimodal object detection interface based on Qwen-2.5-VL (Hybrid Online/Offline).
- **Principle**: Real-time internet connectivity detection and automatic local/remote model switching logic.
- **Example**: `results = qwen.process(frame)`

### 3. Support Utilities (`core/utils/`)
Support tools for system operation and development.
- **[download_model.py](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/core/utils/download_model.py)**: High-speed model downloader for Hugging Face.

## 🧪 Experiments Traceability
History of successful experiments promoted to libraries.
- **EX-001-FACE**: Face analysis technology (gender/age) -> Promotion to `face_utils.py` complete.
- **EX-002-QWEN-VL**: Object detection technology -> Transfer to `qwen_vl.py` complete.

---
> [!NOTE]
> When adding a new library, be sure to register it in this Index document to maintain readability.
> This document is maintained in both [English](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/docs/Library-Index.en.md) and [Korean](file:///Users/sl/Workspace/12.Antigravity/opencv_dev/docs/Library-Index.ko.md).
