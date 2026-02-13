import cv2
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from core.processing.face_processor import FaceProcessor
from core.utils.logger import get_logger

logger = get_logger("LIB_DEMO")

def run_library_demo():
    """
    Demonstrates the simplicity of using the formalized FaceProcessor library.
    """
    # Just ONE line to initialize the entire pipeline
    processor = FaceProcessor()
    
    cap = cv2.VideoCapture(0)
    logger.info("🎬 Library Demo Started. High-speed vector Re-ID enabled.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        # ONE line to process detection, tracking, and cloud Re-ID
        people = processor.process_frame(frame)
        
        for p in people:
            # Draw results
            x1, y1, x2, y2 = p.rect
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{p.id}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Log identity detection
            # logger.info(f"Detected: {p.id} at {p.centroid}")

        cv2.imshow("Core Library: FaceProcessor Demo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("👋 Demo closed.")

if __name__ == "__main__":
    run_library_demo()
