from models.mtcnn import MTCNN
from models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image
import numpy as np

def cosSimilarity(p1, p2): 
    return np.dot(p1, p2) / (np.linalg.norm(p1) * np.linalg.norm(p2))

def getVec(img, mtcnn, resnet):
    img = mtcnn(img)
    latent_vec = resnet(img.unsqueeze(0))
    latent_vec = latent_vec.squeeze().to('cpu').detach().numpy().copy()

    return latent_vec

def main():
    mtcnn = MTCNN(image_size=160, margin=10)
    resnet = InceptionResnetV1().eval()

    img = Image.open("data/1.jpeg")
    vec = getVec(img, mtcnn, resnet)
    print(vec.shape)

if __name__ == "__main__":
    main()