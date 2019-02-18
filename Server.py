import cv2
from PIL import Image
import face_recognition
import time
import numpy as np
import  sqlite3
mport socket 

#ставим сервер на распберри
TCP_IP = '127.0.1.1' 
TCP_PORT = 5002 
BUFFER_SIZE = 1024 # Надо выбрать получше, для быстрого ответа 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((TCP_IP, TCP_PORT)) 
s.listen(1) 

# Подключаемся к базе и создаем курсор
conn = sqlite3.connect('new2.db')
cur = conn.cursor()

# Создаем хранилище всех имеющихся лиц и их
baza_lic = []
imena = []
baza_lic_res = []
c4et4ik = True

# Выгружаем все имена из базы данных

cur.execute('''select count(names) from face''')
kolichestvo_imen = cur.fetchone()
len_imena = kolichestvo_imen[0]
cur.execute('''select names from face''')
for i in range(len_imena):
    imya = cur.fetchone()
    imena.append(imya[0])

# Выгружаем все коды людей из базы

cur.execute('''select count(code) from face''')
kolichestvo_imen = cur.fetchone()
len_imena = kolichestvo_imen[0]
cur.execute('''select code from face''')
for i in range(len_imena):
    # вытаскиваем код лица, в виде строки и затем подгоняем его под сравнялку нейросети
    code_lica = cur.fetchone()
    code_lica = code_lica[0]
    code_lica = code_lica[1:-1]
    code_lica = code_lica.split(',')
    for i in code_lica:
        i = float(i)
        baza_lic_res.append(i)
    asd = np.array(baza_lic_res)
    baza_lic_res = []
    baza_lic.append(asd)

faaace = []
faace_res = []
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)


while True:
    conn, addr = s.accept() 
    print ('Connection address:', addr) 
    while 1: 
        data = conn.recv(BUFFER_SIZE) 
    if not data: break 
        print ("received data:", data) 
    start = time.time()  
    pix = np.array(data)
    encode = face_recognition.face_encodings(pix)
    if len(encode)>0:
        face_recognition_try = face_recognition.compare_faces(baza_lic, encode[0], tolerance=0.4)
        imya_output = 'Unknown'
        print(face_recognition_try)
        if True in face_recognition_try:
            index_lica = face_recognition_try.index(True)
            name = imena[index_lica]
            print(name)
        else:
            print(imya_output)
    print(start - time.time())



cap.release()
cv2.destroyAllWindows()
