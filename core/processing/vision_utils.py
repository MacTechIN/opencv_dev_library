import cv2
import numpy as np

def draw_bboxes(image, bboxes, labels):
    """
    이미지에 바운딩 박스와 라벨을 그림.
    """
    for bbox, label in zip(bboxes, labels):
        x1, y1, x2, y2 = bbox
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return image

def resize_image(image, target_size=(640, 640)):
    """
    이미지 크기를 조정함.
    """
    return cv2.resize(image, target_size)
