import cv2
import numpy as np
from deepface import DeepFace

cap = cv2.VideoCapture(0)

cv2.namedWindow('Live')

while (True):
    ret, img = cap.read()
    cv2.imshow('Live', img)
    obj = DeepFace.verify(
        img1_path=img, img2_path="database/1.jpg", enforce_detection=False)
    print("Face verification : ", obj['verified'])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
