import cv2
import numpy as np
from PIL import Image
import os

class trainAll:
    def __init__(self):
        self.state=1
        try:
            path = 'dataset'
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            detector = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img,'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1]) 
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            recognizer.train(faceSamples, np.array(ids))
            recognizer.write('trainer/trainer.yml')
            self.state = len(np.unique(ids))
        except:
            self.state=0
            
    def stateReturn(self):
        return self.state
if __name__=="__main__":
    obj = trainAll()