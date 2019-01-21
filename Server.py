import sqlite3
import numpy as np
import face_recognition
import time
import cv2
from PIL import Image
import os
import pika

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

face_bytes = 0
width_int = 0
hight_int = 0
face = 0
width = 0
hight = 0
c4et = 0


def callback(ch, method, properties, body):
    text = str(body.decode())
    print(text)
    if c4et == 0:
        face = body
    elif c4et == 1:
        width = int(body.decode())
    elif c4et == 2:
        hight = int(body.decode())
    elif c4et == 3:
        b = Image.frombytes(mode='RGB', size=(hight, width), data=face)
        # Переводим фото в формат для работы с библиотекой face_recognition
        unknown_face = np.array(b)
        # Для примера берем последнее лицо.
        Unknown = face_recognition.face_encodings(unknown_face)
        q = face_recognition.compare_faces(baza_lic, Unknown, tolerance=0.4)
        imya_output = "unknown"
        if q == True:
            index_lica = q.index(True)
            name = imena[index_lica]
            print(name)
        else:
            print(imya_output)
        width = 0
        face = 0
        hight = 0
        c4et = 0


channel.basic_consume(callback,
                      queue='face',
                      no_ack=True)
channel.basic_consume(callback,
                      queue='width',
                      no_ack=True)

channel.basic_consume(callback,
                      queue='hight',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')


conn.commit()
channel.start_consuming()
