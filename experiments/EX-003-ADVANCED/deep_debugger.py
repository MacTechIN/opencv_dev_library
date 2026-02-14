import cv2
import os
import torch
import numpy as np
from core.models.qwen_vl import QwenVLProcessor
from core.web.web_utils import WebAppSDK
import time

def run_deep_debug():
    debug_log = []
    
    def log_step(step, name, inp, outp, status, verify):
        debug_log.append({
            "step": step,
            "name": name,
            "input": inp,
            "output": outp,
            "status": status,
            "verify": verify
        })
        print(f"DEBUG: Step {step} [{name}] -> {status}")

    # 1. Image Load Verification
    project_root = "/Users/sl/Workspace/12.Antigravity/opencv_dev"
    img_path = os.path.join(project_root, "experiments/EX-002-QWEN-VL/sample.jpg")
    
    frame = cv2.imread(img_path)
    if frame is not None:
        log_step(1, "cv2.imread", img_path, f"{frame.shape} Array", "✅ OK", "Image loaded correctly")
    else:
        log_step(1, "cv2.imread", img_path, "None", "❌ FAIL", f"File not found at {img_path}")
        # Try camera_test.jpg as fallback
        img_path = os.path.join(project_root, "camera_test.jpg")
        frame = cv2.imread(img_path)
        if frame is not None:
             log_step(1, "cv2.imread (Fallback)", img_path, f"{frame.shape} Array", "⚠️ FALLBACK", "Loaded camera_test.jpg instead")
        else:
            return

    # 2. Processor Initialization
    try:
        processor = QwenVLProcessor()
        log_step(2, "QwenVLProcessor.__init__", "Default weights", f"Model on {processor.device}", "✅ OK", "Weights loaded")
    except Exception as e:
        log_step(2, "QwenVLProcessor.__init__", "Default weights", str(e), "❌ FAIL", "Model load error")
        return

    # 3. Comprehensive Analysis (Inference Trace)
    try:
        results = processor.detect_and_analyze_persons(frame)
        
        # Raw Output is already logged in QwenVL, we summarize here
        log_step(3, "detect_and_analyze_persons", "Frame Matrix", f"Parsed {len(results)} objects", 
                 "✅ OK" if results else "⚠️ EMPTY", "Check console logs for 'Qwen-VL Raw Output Content'")
        
        for i, res in enumerate(results):
             print(f"   Trace Object {i+1}: ID={res['id']}, BBox={res['bbox']}, Gender={res['gender']}, Age={res['age']}")

    except Exception as e:
        log_step(3, "detect_and_analyze_persons", "Frame Matrix", str(e), "❌ FAIL", "Inference error")
        return

    # 4. Visualization Verification
    try:
        vis_frame = WebAppSDK.draw_analysis_overlay(frame, results)
        
        # Verification: Check if frame actually changed
        diff = np.sum(cv2.absdiff(frame, vis_frame))
        if diff > 0:
            log_step(4, "draw_analysis_overlay", f"{len(results)} items", f"Diff Sum: {diff}", "✅ OK", "Pixels actually modified")
        else:
            log_step(4, "draw_analysis_overlay", f"{len(results)} items", "No Pixel Change", "⚠️ WARNING", "Visualizer returned unchanged frame")
        
        debug_save_path = "results/deep_debug_result.jpg"
        cv2.imwrite(debug_save_path, vis_frame)
        print(f"DEBUG: Saved visualized output to {debug_save_path}")

    except Exception as e:
        log_step(4, "draw_analysis_overlay", "Results List", str(e), "❌ FAIL", "Visualization error")

    # 5. Summary Generation
    with open("results/deep_debug_trace.md", "w", encoding="utf-8") as f:
        f.write("# Deep Debugging Time-series Trace\n\n")
        f.write(f"Generated at: {time.ctime()}\n\n")
        f.write("| Step | Function | Input | Output | Status | Verification |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for log in debug_log:
            f.write(f"| {log['step']} | {log['name']} | {log['input']} | {log['output']} | {log['status']} | {log['verify']} |\n")

if __name__ == "__main__":
    run_deep_debug()
