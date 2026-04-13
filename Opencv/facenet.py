import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

mtcnn = MTCNN(image_size=160, margin=20)
model = InceptionResnetV1(pretrained='vggface2').eval()

def get_embedding(image_path):
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    face = mtcnn(img)
    if face is None:
        return None
    with torch.no_grad():
        return model(face.unsqueeze(0))

def are_same_person(path1, path2, threshold=1.0):
    emb1 = get_embedding(path1)
    emb2 = get_embedding(path2)
    if emb1 is None or emb2 is None:
        return "Face not detected"
    distance = torch.dist(emb1, emb2).item()
    return {"distance": round(distance, 4), "same_person": distance < threshold}

print(are_same_person("person1.jpg", "person2.jpg"))