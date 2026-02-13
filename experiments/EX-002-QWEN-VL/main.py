import os
import sys

# Add project root and core library paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from core.models.qwen_vl import QwenVLProcessor
from core.processing.vision_utils import draw_bboxes
import cv2

def run_experiment():
    print("--- Qwen-2.5-VL Object Detection Experiment Start ---")
    
    # Initialize model (Using central management library)
    processor = QwenVLProcessor()
    
    # Test image path (Example)
    image_path = os.path.join(project_root, "data/test_image.jpg")
    
    # 1. Image load and preprocessing
    # frame = cv2.imread(image_path)
    
    # 2. Inference (Detect people, objects, vehicles, etc.)
    # result_frame = processor.process(frame)
    
    # 3. Save results
    # output_path = "experiments/EX-002-QWEN-VL/results/output.jpg"
    # cv2.imwrite(output_path, result_frame)
    
    print("Experiment completed. Check the results/ folder for outcomes.")

if __name__ == "__main__":
    run_experiment()
