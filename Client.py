import sqlite3
import numpy as np
import face_recognition
import time
import os


# Сегодня мы будем искать лучшую фотографию человека и пихать её в бд
# Подключаемся к базе и создаем курсор
conn = sqlite3.connect('new2.db')
cur = conn.cursor()

# name = input('Введите имя (например Vin Dizzel)')

#Вводим папку с фотографиями, имеющими название 1.jpeg,2.jpeg ... :) и считаем количество файлов в папке
path = input('Введите папку с изображениями (например Putin)')
list = os.listdir(path)
number_files = len(list)

# Начинаем искать максимальную, по совпадениям) фотку
maximum = 0
count = 0
count_index = 0
faces = []
faces_result = []
# загружаем фотографии и производим кодировку в вектора
for i in range(number_files):
    faces.append(
        face_recognition.face_encodings(face_recognition.load_image_file(path+'/' + str(i + 1) + '.jpeg')))
# это действие можно и оставить в цикле сверху, но так круче выглядит (так как есть ограничение на длинну строки в питоне)
for i in range(len(faces)):
    faces[i] = faces[i][0]
# идет поиск лучшей фотографии (поиск максимума по совпадениям)
for i in range(len(faces)):
    a = face_recognition.compare_faces(faces, faces[i], tolerance=0.40)
    for true in a:
        if true == True:
            maximum += 1
    if maximum > count:
        count = maximum
        count_index = i
    maximum = 0

print('Лучшая фотка под номером:',str(count_index+1)+'.jpeg',"имеет",count,"совпадений")

# Добавляем фото в базу данных, jitter увеличивает точность
best_face = face_recognition.face_encodings(face_recognition.load_image_file(path+'/' + str(count_index + 1) + '.jpeg'), num_jitters=100)
#тестим новую фотку на имеющихся лицах
print(face_recognition.compare_faces(faces,best_face[0],tolerance=0.4))

# x = best_face[0].tolist()
# x = str(x)
# cur.execute('''insert into face values (?,?)''', (name, x))
# print('запрос выполнен')
# conn.commit()

