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
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"⚠️ Warning: Test image not found at {image_path}")
        return

    # 1. Image load and preprocessing
    frame = cv2.imread(image_path)
    
    # 2. Inference (Detect people, objects, vehicles, etc.)
    # The process method in QwenVLProcessor should handle the inference
    result_frame = processor.process(frame)
    
    # 3. Save results
    output_dir = os.path.join(project_root, "experiments/EX-002-QWEN-VL/results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "output.jpg")
    cv2.imwrite(output_path, result_frame)
    
    print(f"Experiment completed. Results saved to: {output_path}")

if __name__ == "__main__":
    run_experiment()
