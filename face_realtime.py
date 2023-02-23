import cv2
import numpy as np
from deepface import DeepFace
cap = cv2.VideoCapture(0)

while (True):
    cv2.imshow('Live', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
