import cv2
import numpy as np
import os
import time
from typing import List, Tuple, Dict, Optional
from core.utils.logger import get_logger

# 통합 로거 초기화
logger = get_logger("FaceUtils")

class FaceUtils:
    """
    얼굴 인식 및 분석(성별, 연령)을 담당하는 유틸리티 클래스.
    OpenCV DNN 모듈을 사용하여 Caffe 모델 기반 추론을 수행합니다.
    """
    
    # 상수 정의
    AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    GENDER_LIST = ['Male', 'Female']
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def __init__(self, models_path: str = "assets/weights/face_models", use_opencl: bool = True):
        self.models_path = models_path
        self.use_opencl = use_opencl
        self.is_ready = False
        
        # 모델 속성 초기화
        self.face_net = None
        self.age_net = None
        self.gender_net = None
        
        self._load_models()

    def _load_models(self):
        """모델 가중치와 프로토텍스트를 로드하고 백엔드 설정을 수행합니다."""
        try:
            paths = {
                "face": (os.path.join(self.models_path, "face_net.caffemodel"), os.path.join(self.models_path, "face_deploy.prototxt")),
                "age": (os.path.join(self.models_path, "age_net.caffemodel"), os.path.join(self.models_path, "age_deploy.prototxt")),
                "gender": (os.path.join(self.models_path, "gender_net.caffemodel"), os.path.join(self.models_path, "gender_deploy.prototxt"))
            }

            for key, (model, proto) in paths.items():
                if not os.path.exists(model) or not os.path.exists(proto):
                    raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model} 또는 {proto}")

            self.face_net = cv2.dnn.readNet(paths["face"][0], paths["face"][1])
            self.age_net = cv2.dnn.readNet(paths["age"][0], paths["age"][1])
            self.gender_net = cv2.dnn.readNet(paths["gender"][0], paths["gender"][1])

            # 가속화 설정
            if self.use_opencl:
                self.face_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
                self.face_net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
                logger.info("🚀 FaceUtils: OpenCL 가속 모드 활성화")

            self.is_ready = True
            logger.info("✅ FaceUtils: 모든 모델 로드 완료")

        except Exception as e:
            logger.error(f"❌ 모델 로드 프로세스 실패: {e}")
            self.is_ready = False

    def detect_faces(self, frame: np.ndarray, conf_threshold: float = 0.7) -> List[Tuple[int, int, int, int]]:
        """
        영상에서 얼굴을 탐지하고 좌표를 반환합니다.
        
        Args:
            frame: 입력 이미지 (BGR)
            conf_threshold: 신뢰도 임계값
            
        Returns:
            List of (x1, y1, x2, y2)
        """
        if not self.is_ready or frame is None or frame.size == 0:
            return []

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        face_boxes = []
        # 최적화: 루프 밖에서 고정된 shape 값 참조
        num_detections = detections.shape[2]
        
        for i in range(num_detections):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                # 좌표 정규화 및 바운딩 처리
                x1 = max(0, int(detections[0, 0, i, 3] * w))
                y1 = max(0, int(detections[0, 0, i, 4] * h))
                x2 = min(w - 1, int(detections[0, 0, i, 5] * w))
                y2 = min(h - 1, int(detections[0, 0, i, 6] * h))
                
                # 유효한 크기의 박스인지 확인
                if x2 > x1 and y2 > y1:
                    face_boxes.append((x1, y1, x2, y2))
        return face_boxes

    def _classify_common(self, net: cv2.dnn.Net, face_img: np.ndarray, labels: List[str]) -> str:
        """분류 공통 로직 (중복 제거 및 안정성 확보)"""
        if not self.is_ready or net is None or face_img is None or face_img.size == 0:
            return "Unknown"
            
        try:
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)
            net.setInput(blob)
            preds = net.forward()
            return labels[preds[0].argmax()]
        except Exception as e:
            logger.warning(f"분류 도중 오류 발생: {e}")
            return "Unknown"

    def classify_gender(self, face_img: np.ndarray) -> str:
        return self._classify_common(self.gender_net, face_img, self.GENDER_LIST)

    def classify_age(self, face_img: np.ndarray) -> str:
        return self._classify_common(self.age_net, face_img, self.AGE_LIST)
