import base64
import cv2
import numpy as np
from typing import Dict, Any, List
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
    def draw_analysis_overlay(frame: np.ndarray, analysis_results: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draws boxes and labels from Qwen-VL analysis results onto the frame.
        Handles ID, Gender, and Age.
        """
        output_frame = frame.copy()
        height, width = frame.shape[:2]

        for obj in analysis_results:
            # Qwen-VL normalized coordinates [ymin, xmin, ymax, xmax] usually in 1000-scale
            # or absolute if pre-processed. Here we assume 1000-scale normalization based on Qwen-VL defaults.
            ymin, xmin, ymax, xmax = obj['bbox']
            
            # Convert normalized to absolute
            left = int(xmin * width / 1000)
            top = int(ymin * height / 1000)
            right = int(xmax * width / 1000)
            bottom = int(ymax * height / 1000)

            # Draw Box
            color = (0, 255, 0) # Green
            cv2.rectangle(output_frame, (left, top), (right, bottom), color, 2)

            # Label text
            label = f"ID:{obj['id']} | {obj['gender']} | {obj['age']}"
            if 'distance' in obj:
                label += f" | {obj['distance']}m"
            
            # Draw Label Background
            (l_w, l_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
            cv2.rectangle(output_frame, (left, top - 20), (left + l_w, top), color, -1)
            cv2.putText(output_frame, label, (left, top - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

        return output_frame

def get_webapp_sdk():
    """Returns a singleton instance of WebAppSDK or provides static methods."""
    return WebAppSDK()
