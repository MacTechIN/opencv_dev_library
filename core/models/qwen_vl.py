import os
import re
import json
import cv2
import torch
import requests
import numpy as np
from PIL import Image
from typing import Optional, List, Dict, Any
from core.utils.logger import get_logger

logger = get_logger("QwenVL")

class QwenVLProcessor:
    """
    Hybrid object detection and analysis processor using the Qwen-2.5-VL model.
    Supports:
    - Automatic Hybrid Loading: Local weights (assets/weights) vs Online (Hugging Face)
    - Comprehensive Person Analysis: Detection + Gender + Age in one pass
    - Precision Parsing: Regex-based coordinate extraction
    """
    def __init__(self, model_path: Optional[str] = None, device: Optional[str] = None):
        # Set default local path
        if model_path is None:
            model_path = os.path.join(os.getcwd(), "assets/weights/Qwen2.5-VL-3B-Instruct")
        
        self.model_path = model_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.repo_id = "Qwen/Qwen2.5-VL-3B-Instruct"
        self.model = None
        self.processor = None
        
        self._initialize_model()

    def _check_internet(self, timeout: int = 3) -> bool:
        """Checks for internet connectivity."""
        try:
            requests.get("https://huggingface.co", timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def _initialize_model(self):
        """Initializes the model in an environment-optimized manner."""
        # 1. Check local weights
        has_local = os.path.exists(self.model_path)
        
        # 2. Check internet for repo fallback
        is_online = self._check_internet()
        
        if has_local:
            os.environ["TRANSFORMERS_OFFLINE"] = "1"
            os.environ["HF_DATASETS_OFFLINE"] = "1"
            load_path = self.model_path
            logger.info(f"🏠 Offline Mode: Prioritizing local weights at '{self.model_path}'")
        elif is_online:
            load_path = self.repo_id
            logger.info(f"🌐 Online Mode: Local weights not found. Loading '{self.repo_id}' from HF...")
        else:
            logger.error("❌ Critical: No local weights found AND no internet connection.")
            return

        try:
            from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
            
            # Load Processor
            self.processor = AutoProcessor.from_pretrained(
                load_path, 
                local_files_only=has_local
            )
            
            # Load Model
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                load_path,
                torch_dtype="auto",
                device_map={"": self.device},
                local_files_only=has_local
            )
            
            logger.info(f"✅ Qwen-2.5-VL loaded successfully on {self.device}")
            
        except ImportError as e:
            logger.error(f"❌ ImportError during model initialization: {e}")
            logger.info("💡 Hint: Try 'pip install --upgrade transformers accelerate'")
        except Exception as e:
            logger.error(f"❌ Error during model initialization: {e}")
            if not has_local:
                logger.info("💡 Hint: Run 'core/utils/download_model.py' to download weights for offline use.")

    def detect_and_analyze_persons(self, image_input: Any) -> List[Dict[str, Any]]:
        """
        Detects all persons in the image and analyzes their gender and age group.
        Returns a list of dictionaries containing 'bbox', 'gender', and 'age'.
        """
        if not self.model or not self.processor:
            return []

        try:
            # 1. Load image and ensure resolution is optimized for Qwen-VL
            image = Image.open(image_input).convert("RGB") if isinstance(image_input, str) else Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))
            
            # 2. Prepare Prompt (Strict High-Precision Detection)
            prompt = (
                "<|image_pad|>Analyze the image and detect every single person.\n"
                "Return the results in exactly this format for each person:\n"
                "[ymin, xmin, ymax, xmax] Gender, AgeGroup\n"
                "Example output: [150, 200, 400, 300] Male, 20s\n"
                "Focus: Ensure every person is caught. No talking. Just the list."
            )

            # Performance optimization: Scale resolution to fit model limits efficiently
            min_pixels = 256 * 28 * 28
            max_pixels = 1280 * 28 * 28
            
            logger.info("📡 Analyzing image with Qwen-VL (Inference starting...)")
            max_side = 1200
            if max(image.size) > max_side:
                scale = max_side / max(image.size)
                new_size = (int(image.size[0] * scale), int(image.size[1] * scale))
                image = image.resize(new_size, Image.LANCZOS)
                logger.info(f"📏 Image resized to {new_size} for model stability.")

            # Optimized pixel limitations (Multiple of 28 is best for Qwen2-VL)
            min_pixels = 224 * 224
            max_pixels = 1024 * 1024
            
            inputs = self.processor(
                text=[prompt], 
                images=[image], 
                padding=True,
                return_tensors="pt",
                min_pixels=min_pixels,
                max_pixels=max_pixels
            ).to(self.device)
            
            logger.info(f"🚀 Starting token generation (Ready with input shape constraint)...")
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs, 
                    max_new_tokens=256,
                    repetition_penalty=1.2,
                    temperature=0.1,
                    top_p=0.9
                )
            
            res_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            logger.info(f"--- [Qwen-VL Raw Output Content] ---\n{res_text}\n-----------------------------------")

            # Regex for parsing bounding boxes: [ymin, xmin, ymax, xmax] or (ymin, xmin, ymax, xmax)
            results = []
            
            # Enhanced Regex for parsing bounding boxes and attributes
            # Matches: [ymin, xmin, ymax, xmax] Gender, Age
            # Also handles variations with/without comma and parentheses
            pattern = re.compile(r"[\[\(](\d+),\s*(\d+),\s*(\d+),\s*(\d+)[\]\)]\s*(\w+)[,\s]*(\d+s)")
            matches = pattern.findall(res_text)

            if not matches:
                # Fallback: Try just finding boxes first
                logger.warning("⚠️ No structured attribute matches found. Falling back to box-only search.")
                box_matches = re.findall(r"[\[\(](\d+),\s*(\d+),\s*(\d+),\s*(\d+)[\]\)]", res_text)
                if not box_matches:
                    logger.warning("❌ Totally no bounding boxes found in model output.")
                    return []
                # If only boxes found, assign default attributes
                for box in box_matches:
                    matches.append((*box, "Unknown", "Unknown"))

            for i, match in enumerate(matches):
                ymin, xmin, ymax, xmax, gender, age = match
                ymin, xmin, ymax, xmax = int(ymin), int(xmin), int(ymax), int(xmax)

                # Skip if it's the example from the prompt
                if [ymin, xmin, ymax, xmax] == [120, 250, 480, 510]:
                    continue

                # [NEW] Distance and Location Estimation
                distance = self.estimate_distance([ymin, xmin, ymax, xmax])
                location = self.calculate_location([ymin, xmin, ymax, xmax], distance)
                
                # [NEW] Vectorize attributes for downstream analysis
                feature_vector = self.vectorize_attributes(i + 1, gender, age, [ymin, xmin, ymax, xmax])

                results.append({
                    "id": len(results) + 1,
                    "bbox": [ymin, xmin, ymax, xmax],
                    "gender": gender,
                    "age": age,
                    "distance": round(float(distance), 2),
                    "location": location,
                    "feature_vector": feature_vector.tolist() if isinstance(feature_vector, np.ndarray) else feature_vector,
                    "raw_info": f"{gender}, {age}"
                })

            return results

        except Exception as e:
            logger.error(f"❌ Error during comprehensive person analysis: {e}")
            return []

    def vectorize_attributes(self, obj_id: int, gender: str, age: str, bbox: List[int]) -> np.ndarray:
        """
        Converts person attributes into a standardized 1D feature vector.
        Vector format: [Gender_Bit, Age_Group_Val, Norm_X, Norm_Y, Norm_Width, Norm_Height]
        """
        # Gender: Male=1, Female=1, Unknown=0 (Simplified)
        gender_bit = 1.0 if gender == "Male" else -1.0 if gender == "Female" else 0.0
        
        # Age Mapping
        age_map = {"10s": 0.1, "20s": 0.2, "30s": 0.3, "40s": 0.4, "50s": 0.5, "60s": 0.6, "70s+": 0.7}
        age_val = age_map.get(age, 0.0)
        
        # BBox Normalization (Assuming 1000-scale coordinates from Qwen-VL)
        ymin, xmin, ymax, xmax = bbox
        nx = xmin / 1000.0
        ny = ymin / 1000.0
        nw = (xmax - xmin) / 1000.0
        nh = (ymax - ymin) / 1000.0
        
        vector = np.array([gender_bit, age_val, nx, ny, nw, nh], dtype=np.float32)
        return vector

    def estimate_distance(self, bbox: List[int], focal_length_px: float = 800.0, avg_height_m: float = 1.7) -> float:
        """
        Estimates relative distance (Z-axis) based on BBox height.
        Formula: Distance = (Real Height * Focal Length) / Pixel Height
        """
        ymin, xmin, ymax, xmax = bbox
        pixel_height = max(1, ymax - ymin)
        
        # Normalize pixel height if it's in 1000-scale
        if pixel_height > 0:
             distance = (avg_height_m * focal_length_px) / (pixel_height * (640 / 1000.0)) # Scale heuristic
             return max(0.5, distance) # Minimum 0.5m
        return 0.0

    def calculate_location(self, bbox: List[int], distance: float) -> Dict[str, float]:
        """Maps 2D screen coordinates to estimated 3D space coordinates."""
        ymin, xmin, ymax, xmax = bbox
        cx = (xmin + xmax) / 2.0
        
        # Horizontal shift from center (normalized -1.0 to 1.0)
        h_shift = (cx - 500) / 500.0
        
        # Heuristic 3D mapping
        x_3d = h_shift * distance * 0.5 # Approx FOV spread
        z_3d = distance
        
        return {"x": round(x_3d, 2), "y": 0.0, "z": round(z_3d, 2)}

    def detect_objects(self, image_input: Any, prompt: str = "Detect all items and describe them.") -> str:
        """
        Generic object detection and description using an arbitrary prompt.
        Returns the raw text response from the model.
        """
        if not self.model or not self.processor:
            return "Error: Model not initialized."

        try:
            image = Image.open(image_input).convert("RGB") if isinstance(image_input, str) else Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))
            
            # Use the provided prompt or default
            inputs = self.processor(
                text=[prompt], 
                images=[image], 
                padding=True,
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(**inputs, max_new_tokens=256)
            
            res_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            logger.info(f"🔍 [detect_objects] Output: {res_text[:100]}...")
            return res_text

        except Exception as e:
            logger.error(f"❌ Error during generic detection: {e}")
            return f"Error: {e}"

    def process(self, frame):
        """Backward compatibility: legacy process method."""
        return self.detect_and_analyze_persons(frame)

import datetime

def generate_markdown_report(results, output_path):
    """Generates a markdown report (detect_person_list.md)."""
    headers = ["ID", "Gender", "Age Group", "Distance (m)", "Coordinates", "Vector (Gender, Age, BBox...)","Raw Output"]
    
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
                res.get('raw_info', '').replace("|", "\\|")
            ]
            f.write("| " + " | ".join(row) + " |\n")
            
    logger.info(f"💾 Report saved to {output_path}")
