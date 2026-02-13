import os
import sys
import cv2
import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core.models.qwen_vl import QwenVLProcessor
from core.web.web_utils import WebAppSDK
from core.utils.logger import get_logger

logger = get_logger("Integrator")

def generate_markdown_report(results, output_path):
    """Generates a markdown report (detect_person_list.md)."""
    headers = ["ID", "Gender", "Age Group", "Distance (m)", "Coordinates", "Vector (Gender, Age, BBox...)", "Raw Output"]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Person Detection & Analysis Report\n\n")
        f.write(f"- **Generated At**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Total Detected**: {len(results)}\n\n")
        
        # Table Header
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        
        # Table Rows
        for res in results:
            # Format vector to be more readable
            vec_short = ", ".join([f"{v:.2f}" for v in res.get('feature_vector', [])])
            
            row = [
                str(res['id']),
                res['gender'],
                res['age'],
                f"{res.get('distance', 0.0)}m",
                str(res['bbox']),
                f"[{vec_short}]",
                res['raw_info'].replace("|", "\\|")
            ]
            f.write("| " + " | ".join(row) + " |\n")
            
    logger.info(f"💾 Report saved to {output_path}")

def run_integration(image_path):
    """Main integration pipeline."""
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return

    # 1. Initialize Hybrid Qwen-VL Processor
    processor = QwenVLProcessor()
    
    # 2. Run Comprehensive Analysis
    logger.info(f"📸 Analyzing image: {image_path}")
    results = processor.detect_and_analyze_persons(image_path)
    
    # 3. Visualization using WebAppSDK
    frame = cv2.imread(image_path)
    visualized_frame = WebAppSDK.draw_analysis_overlay(frame, results)
    
    output_img_path = "results/output_analysis.jpg"
    os.makedirs("results", exist_ok=True)
    cv2.imwrite(output_img_path, visualized_frame)
    logger.info(f"🖼️ Visualized image saved to {output_img_path}")
    
    # 4. Generate Markdown Report
    report_path = "detect_person_list.md"
    generate_markdown_report(results, report_path)
    
    print("\n" + "="*50)
    print(f"✅ Integration Completed!")
    print(f"📊 Persons Detected: {len(results)}")
    print(f"📄 Report: {report_path}")
    print(f"🖼️ Visualization: {output_img_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Test with verification image if available, else sample.jpg
    target = "final_verification.jpg"
    if not os.path.exists(target):
        target = "sample.jpg"
        
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    run_integration(target)
