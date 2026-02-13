import cv2
import numpy as np

def draw_bboxes(image, bboxes, labels):
    """
    Draws bounding boxes and labels on the image.
    """
    for bbox, label in zip(bboxes, labels):
        x1, y1, x2, y2 = bbox
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return image

def resize_image(image, target_size=(640, 640)):
    """
    Resizes the image to the target size.
    """
    return cv2.resize(image, target_size)
