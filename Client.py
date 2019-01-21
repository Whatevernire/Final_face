import sqlite3
import numpy as np
import face_recognition
import time
# Подключаемся к базе и создаем курсор
conn = sqlite3.connect('new2.db')
cur = conn.cursor()
known_image = face_recognition.load_image_file("new.png")
fuck_encode = face_recognition.face_encodings(known_image)

x = fuck_encode[0].tolist()
x = str(x)
while True:
    name = input('Введите имя (например Вин Дизель) или слово-выход')
    puti = input('Введите путь к файлу (Например dizzel.jpeg)')
    if name.lower() == 'выход':
        break
    known_image = face_recognition.load_image_file(puti)
    fuck_encode = face_recognition.face_encodings(known_image)

    x = fuck_encode[0].tolist()
    x = str(x)
    cur.execute('''insert into face values (?,?)''', (name, x))
    print('запрос выполнен')
    conn.commit()
