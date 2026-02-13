import cv2
import os

def test_camera():
    print("📸 Testing Camera Access...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera 0 could not be opened.")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame from Camera 0.")
        return False
    
    save_path = "camera_test.jpg"
    cv2.imwrite(save_path, frame)
    print(f"✅ Camera working! Frame saved to {save_path}")
    cap.release()
    return True

if __name__ == "__main__":
    test_camera()
