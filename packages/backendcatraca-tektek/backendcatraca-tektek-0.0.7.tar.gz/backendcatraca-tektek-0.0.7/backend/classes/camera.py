import cv2
import uuid
import time
import threading

import os
import json
from decouple import config

current_milli_time = lambda: int(round(time.time() * 1000))
TEMPO_TOLERANCIA_ROSTO = 0.5
PATH_TMP_IMGS = 'tmpimgs/'
IMAGE_NAME = "tmpimg.jpg"
NUM_CAMERA=0

class VideoCamera():
    
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(int(NUM_CAMERA))
        self.possuiFace = False
        self.oldFaces = []
        self.imagemJpeg = None
        self.image = self.video.read()
        self.available = False
        self.mode = "detect"

        self.ultimaRequisicao = time.time()

    def __del__(self):
        self.video.release()
        
    def desenharRosto(self, image, x, y, w, h, blur = False):
        # To draw a rectangle in a face  
        cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,0) ,2)

        if (blur):
            result_image = cv2.blur(image, (7, 7))
            sub_face = image[y:y+h, x:x+w]
            result_image[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
            image = result_image

        return image

    def get_frame(self):
        self.success, self.image = self.video.read()
        self.available = True

        # We are using Motion JPEG,  but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, imagemJpeg = cv2.imencode('.jpg', self.image)

        self.imagemJpeg = imagemJpeg.tobytes()

        return (self.imagemJpeg, self.image)
    
    def capturarFoto(self):
        i = 1

        with os.scandir(PATH_TMP_IMGS) as entries:
            for entry in entries:
                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)

        for (x,y,w,h) in self.oldFaces:
            roi_color = self.image[y:y + h, x:x + w]
            cv2.imwrite(PATH_TMP_IMGS+str(i)+ '_tmpface.jpg', roi_color)
            i=i+1

        cv2.imwrite(IMAGE_NAME, self.image)

    def analisarFace(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        
        # Verifica se alguma face foi detectada
        # Caso não tenha sido, verifica se tem X segundos que nenhuma face eh detectada
        # Caso tenha mais tempo que o tempo de tolerancia, marca como nenhuma face
        # Caso tenha menos tempo que o tempo de tolerancia desenha o ultimo quadrado desenhado
        if(len(faces) > 0):
            # self.ws.enviarMensagem("Possui face.")

            self.possuiFace = True
            self.momentoUltimaFaceDetectada = current_milli_time()
            self.oldFaces = faces
     

            for (x,y,w,h) in faces:                 
                self.image = self.desenharRosto(self.image, x, y, w, h)
        else:
            # self.ws.enviarMensagem("Não possui face.")
            if ((current_milli_time() - self.momentoUltimaFaceDetectada) > TEMPO_TOLERANCIA_ROSTO * 1000):
                self.possuiFace = False    
            else:
                if (len(self.oldFaces) > 0):
                    for (x,y,w,h) in self.oldFaces: 
                        self.image = self.desenharRosto(self.image, x, y, w, h, False)