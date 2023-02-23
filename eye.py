import numpy as np
import cv2
import dlib


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


def eye_on_mask(mask, side):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask



cap = cv2.VideoCapture(0)
ret, img = cap.read()
thresh = img.copy()
cv2.namedWindow('Live')
kernel = np.ones((9, 9), np.uint8)


def nothing(x):
    pass


predictor = dlib.shape_predictor('shape_68.dat')
detector = dlib.get_frontal_face_detector()
left = [36, 37, 38, 39, 40, 41]  # keypoint indices for left eye
right = [42, 43, 44, 45, 46, 47]  # keypoint indices for right eye
mask = np.zeros(img.shape[:2], dtype=np.uint8)
mask = eye_on_mask(mask, left)
mask = eye_on_mask(mask, right)

while (True):
    img = cv2.imread('image.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        for (x, y) in shape:
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

    rects = detector(gray, 1)  # rects contains all the faces detected
    ret, img = cap.read()
    cv2.imshow('Live', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()