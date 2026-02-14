import cv2
import numpy as np
from typing import List, Dict, Any
from core.utils.logger import get_logger
from core.processing.face_processor import FaceProcessor

class RefinementEngine:
    """
    VLM(Qwen-VL)의 탐지 결과를 기하학적 분석 및 고전적 CV 엔진으로 정제하는 클래스.
    """
    def __init__(self, face_processor: FaceProcessor = None):
        self.logger = get_logger("RefinementEngine")
        self.face_processor = face_processor or FaceProcessor()
        self.logger.info("🛡️ RefinementEngine initialized for high-precision validation.")

    def refine_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        탐지된 리스트를 정제하여 신뢰도가 높은 결과만 반환.
        """
        refined_results = []
        
        for det in detections:
            bbox = det.get('bbox') # [ymin, xmin, ymax, xmax]
            if not bbox: continue
            
            # 1. Geometric Verification (기하학적 검증)
            geo_score = self._verify_geometry(bbox, frame.shape)
            
            # 2. CV-based Verification (Face/Keypoint 검증 - 우선 Face 위주)
            cv_score = self._verify_with_face(frame, bbox)
            
            # 3. Final Integration (가중치 기반 결정)
            # VLM 결과가 압도적이거나, CV 증거가 보완될 때 생존
            final_confidence = (geo_score * 0.4) + (cv_score * 0.6)
            
            self.logger.info(f"🔍 Refinement [ID:{det.get('id')}]: Geo:{geo_score:.2f}, CV:{cv_score:.2f} -> Final:{final_confidence:.2f}")
            
            if final_confidence > 0.4: # 임계값 (상황에 따라 조정 가능)
                det['confidence_score'] = round(final_confidence, 2)
                refined_results.append(det)
            else:
                self.logger.warning(f"🚫 Removing False Positive [ID:{det.get('id')}]: Semantic mismatch or geometry error.")

        return refined_results

    def _verify_geometry(self, bbox: List[int], img_shape: tuple) -> float:
        """
        바운딩 박스의 종횡비와 크기를 분석하여 인체 가능성 점수 산출.
        """
        ymin, xmin, ymax, xmax = bbox
        h = ymax - ymin
        w = xmax - xmin
        
        if h <= 0 or w <= 0: return 0.0
        
        aspect_ratio = h / w
        
        # 일반적인 서 있거나 앉은 사람의 종횡비 (0.5 ~ 5.0 사이)
        if 0.5 < aspect_ratio < 5.0:
            score = 1.0
        elif 0.3 < aspect_ratio < 7.0:
            score = 0.5
        else:
            score = 0.1
            
        return score

    def _verify_with_face(self, frame: np.ndarray, bbox: List[int]) -> float:
        """
        탐지 영역 내부에 얼굴이 존재하는지 확인 (강력한 증거).
        """
        ymin, xmin, ymax, xmax = bbox
        img_h, img_w = frame.shape[:2]
        
        # 안전한 좌표 클리핑
        ymin, xmin = max(0, ymin), max(0, xmin)
        ymax, xmax = min(img_h, ymax), min(img_w, xmax)
        
        roi = frame[ymin:ymax, xmin:xmax]
        if roi.size == 0: return 0.0
        
        try:
            # FaceProcessor를 사용해 ROI 내 얼굴 탐지 시도
            persons = self.face_processor.process_frame(roi)
            
            if persons and len(persons) > 0:
                self.logger.info(f"✅ Face confirmed inside VLM bbox.")
                return 1.0
            
            # 얼굴이 안 보일 수도 있음 (뒷모습 등)
            return 0.3
            
        except Exception as e:
            self.logger.error(f"❌ Error during CV verification: {e}")
            return 0.0
