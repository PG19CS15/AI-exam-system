import numpy as np
import cv2
import dlib

cap = cv2.VideoCapture(0)
ret, img = cap.read()
thresh = img.copy()
cv2.namedWindow('Live')
kernel = np.ones((9, 9), np.uint8)


def nothing(x):
    pass


detector = dlib.get_frontal_face_detector()

while (True):
    img = cv2.imread('image.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    rects = detector(gray, 1)  # rects contains all the faces detected
    ret, img = cap.read()
    cv2.imshow('Live', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
