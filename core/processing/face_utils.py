import cv2
import numpy as np
import os
from typing import List, Tuple, Dict, Optional

class FaceUtils:
    """
    얼굴 인식 및 분석(성별, 연령)을 담당하는 유틸리티 클래스.
    OpenCV DNN 모듈을 사용하여 Caffe 모델 기반 추론을 수행합니다.
    """
    
    # 상수 정의
    AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    GENDER_LIST = ['Male', 'Female']
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def __init__(self, models_path: str = "assets/weights/face_models"):
        self.models_path = models_path
        self._load_models()

    def _load_models(self):
        """모델 가중치와 프로토텍스트를 로드합니다."""
        try:
            self.face_net = cv2.dnn.readNet(
                os.path.join(self.models_path, "face_net.caffemodel"),
                os.path.join(self.models_path, "face_deploy.prototxt")
            )
            self.age_net = cv2.dnn.readNet(
                os.path.join(self.models_path, "age_net.caffemodel"),
                os.path.join(self.models_path, "age_deploy.prototxt")
            )
            self.gender_net = cv2.dnn.readNet(
                os.path.join(self.models_path, "gender_net.caffemodel"),
                os.path.join(self.models_path, "gender_deploy.prototxt")
            )
        except Exception as e:
            print(f"모델 로드 실패: {e}. 'download_face_models.py'를 먼저 실행하세요.")

    def detect_faces(self, frame: np.ndarray, conf_threshold: float = 0.7) -> List[Tuple[int, int, int, int]]:
        """
        영상에서 얼굴을 탐지하고 좌표를 반환합니다.
        
        Args:
            frame: 입력 이미지 (BGR)
            conf_threshold: 신뢰도 임계값
            
        Returns:
            List of (x1, y1, x2, y2)
        """
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        face_boxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                h, w = frame.shape[:2]
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                face_boxes.append((x1, y1, x2, y2))
        return face_boxes

    def classify_gender(self, face_img: np.ndarray) -> str:
        """
        얼굴 이미지에서 성별을 분류합니다.
        
        Args:
            face_img: 잘려진 얼굴 이미지
            
        Returns:
            'Male' 또는 'Female'
        """
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.gender_net.setInput(blob)
        preds = self.gender_net.forward()
        return self.GENDER_LIST[preds[0].argmax()]

    def classify_age(self, face_img: np.ndarray) -> str:
        """
        얼굴 이미지에서 연령대를 추정합니다.
        
        Args:
            face_img: 잘려진 얼굴 이미지
            
        Returns:
            연령대 문자열 (예: '(25-32)')
        """
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
        self.age_net.setInput(blob)
        preds = self.age_net.forward()
        return self.AGE_LIST[preds[0].argmax()]
