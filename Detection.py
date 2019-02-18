import cv2
from PIL import Image
import face_recognition
import time
import numpy as np
import socket 


faaace = []
faace_res = []
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)


TCP_IP = '127.0.0.1' # это ip raspberry
TCP_PORT = 5005 
BUFFER_SIZE = 1024  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((TCP_IP, TCP_PORT))



while True:
    ret, img = cap.read()
    start = time.time()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,

        scaleFactor=1.2,
        minNeighbors=10,
        minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x-10, y-10), (x+10 + w, y+10 + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        box = (x+20,y+20,x+20+w,y+20+h)
        face_image= img
        face_image = Image.fromarray(face_image,'RGB')
        face_image=face_image.crop(box)
        MESSAGE = face_image      
        s.send(MESSAGE) 
        data = s.recv(BUFFER_SIZE) 

        print(start - time.time())



cap.release()
cv2.destroyAllWindows()
