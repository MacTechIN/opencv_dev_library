import base64
import cv2
import numpy as np
import os
import datetime
from typing import Dict, Any, List, Tuple
from core.utils.logger import get_logger

logger = get_logger("WebUtils")

class WebAppSDK:
    """
    Common library for Web Application Development.
    Provides utility functions for API handling, image streaming, and result visualization.
    """
    
    @staticmethod
    def frame_to_base64(frame: np.ndarray) -> str:
        """Converts an OpenCV frame to a base64 string for web display."""
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            return base64.b64encode(buffer).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding frame: {e}")
            return ""

    @staticmethod
    def format_api_response(status: str, data: Any, message: str = "") -> Dict[str, Any]:
        """Standardizes API response format."""
        return {
            "status": status,
            "data": data,
            "message": message
        }

    @staticmethod
    def draw_analysis_overlay(frame: np.ndarray, analysis_results: Any) -> np.ndarray:
        """
        Draws boxes and labels for multiple types (Body, Face, Object).
        Color Map: Body=Green, Face=Blue, Object=Yellow
        """
        output_frame = frame.copy()
        height, width = frame.shape[:2]

        # Handle both list (v1) and dict (v2 VisionHub) inputs
        results_list = []
        if isinstance(analysis_results, dict):
            for k, v in analysis_results.items():
                if isinstance(v, list): results_list.extend(v)
        else:
            results_list = analysis_results

        for obj in results_list:
            ymin, xmin, ymax, xmax = obj['bbox']
            l, t = int(xmin * width / 1000), int(ymin * height / 1000)
            r, b = int(xmax * width / 1000), int(ymax * height / 1000)

            # Determine color and label by type
            obj_type = obj.get("type", "body")
            if obj_type == "face":
                color = (255, 0, 0) # Blue
                label = f"FACE {obj.get('id', '')}"
            elif obj_type == "object":
                color = (0, 255, 255) # Yellow
                label = f"OBJ: {obj.get('class', 'item')}"
            else:
                color = (0, 255, 0) # Green
                g_raw = obj.get('gender', 'Unknown').lower()
                gender_kr = "남" if "male" in g_raw and "female" not in g_raw else "여" if "female" in g_raw else "?"
                label = f"{gender_kr}/{obj.get('age', '?')}"
                if 'distance' in obj: label += f"({obj['distance']}m)"

            # Draw
            cv2.rectangle(output_frame, (l, t), (r, b), color, 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            f_scale, f_thick = 0.4, 1
            (lw, lh), _ = cv2.getTextSize(label, font, f_scale, f_thick)
            cv2.rectangle(output_frame, (l, t - lh - 10), (l + lw + 5, t), color, -1)
            cv2.putText(output_frame, label, (l + 2, t - 5), font, f_scale, (0, 0, 0), f_thick)

        return output_frame

    @staticmethod
    def draw_trajectories(frame: np.ndarray, history: Dict[int, List[Tuple[int, int]]], max_points: int = 20) -> np.ndarray:
        """
        Draws the movement paths (trajectories) of tracked objects.
        
        Args:
            frame: Base image.
            history: Dictionary mapping ID to list of (x, y) coordinates.
            max_points: Max number of history points to draw per object.
        """
        output_frame = frame.copy()
        
        # Consistent color palette for IDs
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
            (0, 255, 255), (255, 0, 255), (255, 255, 255)
        ]

        for obj_id, points in history.items():
            if len(points) < 2:
                continue
            
            color = colors[obj_id % len(colors)]
            points_to_draw = points[-max_points:]
            
            for i in range(1, len(points_to_draw)):
                pt1 = points_to_draw[i - 1]
                pt2 = points_to_draw[i]
                thickness = int(np.sqrt(max_points / float(i + 1)) * 2)
                cv2.line(output_frame, pt1, pt2, color, thickness)
        
        return output_frame

    @staticmethod
    def bootstrap_vision_app(model_types: List[str] = ["qwen-vl"]) -> Dict[str, Any]:
        """
        One-stop bootstrap for Vision AI applications.
        Creates directories, initializes logging, and loads requested models.
        
        Returns:
            Dict containing initialized models and system context.
        """
        logger.info("🚀 [Bootstrap] Starting Vision AI Application environment setup...")
        
        # 1. Ensure Essential Directories
        essential_dirs = ["results", "logs", "assets/weights"]
        for d in essential_dirs:
            os.makedirs(d, exist_ok=True)
            logger.info(f"📁 [Bootstrap] Directory verified: {d}")

        context = {
            "init_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "models": {},
            "device_info": "Detected automatically by models"
        }

        # 2. Dynamic Model Loading
        if "qwen-vl" in [m.lower() for m in model_types]:
            try:
                from core.models.qwen_vl import QwenVLProcessor
                logger.info("🤖 [Bootstrap] Loading Qwen-VL Processor...")
                context["models"]["qwen_vl"] = QwenVLProcessor()
                logger.info("✅ [Bootstrap] Qwen-VL Engine ready.")
            except Exception as e:
                logger.error(f"❌ [Bootstrap] Failed to load Qwen-VL: {e}")

        logger.info("✨ [Bootstrap] Application environment is now ready.")
        return context

def get_webapp_sdk():
    """Returns a singleton instance of WebAppSDK or provides static methods."""
    return WebAppSDK()
