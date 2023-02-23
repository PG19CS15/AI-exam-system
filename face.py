from deepface import DeepFace
obj=DeepFace.verify(img1_path="database/2.jpg",img2_path="database/1.jpg")
print(obj['verified'])