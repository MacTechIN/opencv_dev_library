from abc import ABC, abstractmethod
import cv2

class Processor(ABC):
    """
    모든 영상 처리 모듈의 공통 부모 클래스.
    """
    @abstractmethod
    def process(self, frame):
        """
        영상을 입력받아 처리된 영상을 반환함.
        :param frame: 입력 영상 (numpy array)
        :return: 처리된 영상 (numpy array)
        """
        pass

    def get_info(self):
        """
        프로세서의 정보를 반환함.
        """
        return {"type": self.__class__.__name__}
