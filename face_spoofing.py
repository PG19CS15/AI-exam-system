import cv2
import numpy as np
import joblib
from face_detector import get_face_detector, find_faces
import torch
from torchvision import transforms
from Model import DeePixBiS

def calc_hist(img):
    histogram = [0] * 3
    for j in range(3):
        histr = cv2.calcHist([img], [j], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[j] = histr
    return np.array(histogram)

face_model = get_face_detector()
clf = joblib.load('models/face_spoofing.pkl')

# Initialize and load the anti-spoofing model
model = DeePixBiS()
model.load_state_dict(torch.load('models/DeePixBiS.pth'))
model.eval()

tfms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

cap = cv2.VideoCapture(0)

sample_number = 10
measures = np.zeros(sample_number, dtype=float)

while True:
    ret, img = cap.read()
    faces = find_faces(img, face_model)

    measures = np.roll(measures, 1)

    height, width = img.shape[:2]
    for x, y, x1, y1 in faces:
        roi = img[y:y1, x:x1]

        if roi.size == 0:
            continue

        img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
        img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

        ycrcb_hist = calc_hist(img_ycrcb)
        luv_hist = calc_hist(img_luv)

        feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
        feature_vector = feature_vector.reshape(1, len(feature_vector))

        prob = clf.predict_proba(feature_vector)[0][1]
        measures[0] = prob

        # Pass the face region through the anti-spoofing model
        faceRegion = tfms(roi)
        faceRegion = faceRegion.unsqueeze(0)
        with torch.no_grad():
            mask, _ = model.forward(faceRegion)
            res = torch.mean(mask).item()

        # Ensemble prediction
        ensemble_prediction = (res + np.mean(measures)) / 2.0

        cv2.rectangle(img, (x, y), (x1, y1), (255, 0, 0), 2)

        if ensemble_prediction < 0.5:
            text = "Fake"
            color = (0, 0, 255)
        else:
            text = "Real"
            color = (0, 255, 0)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img=img, text=text, org=(x, y - 5), fontFace=font, fontScale=0.9,
                    color=color, thickness=2, lineType=cv2.LINE_AA)

    cv2.imshow('img_rgb', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

