from abc import ABC, abstractmethod
import cv2

class Processor(ABC):
    """
    Common base class for all image processing modules.
    """
    @abstractmethod
    def process(self, frame):
        """
        Receives an image and returns the processed image.
        :param frame: Input image (numpy array)
        :return: Processed image (numpy array)
        """
        pass

    def get_info(self):
        """
        Returns information about the processor.
        """
        return {"type": self.__class__.__name__}
