#!/usr/bin/env python
from PIL import Image
import face_recognition
import os
import cv2
import sqlite3
import pika

video_capture = cv2.VideoCapture(0)
face_locations = []


parameters = pika.URLParameters('amqp://admin2:123@185.185.68.195:5672')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.queue_declare(queue='face')
channel.queue_declare(queue='width')
channel.queue_declare(queue='hight')


i=0
def main():
    while True:

        # Взятие кадра с видео
        ret, frame = video_capture.read()

        # Уменьшение кадра до 1/4 для быстрого распознования лица
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Конвертация изображения из BGR color (which OpenCV uses) в RGB color (с которым работает библиотека)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0)
        if face_locations != 0:
            for face_location in face_locations:
                top, right, bottom, left = face_location
                face_image = rgb_small_frame[top - 10:bottom + 10, left - 10:right + 10]
                #Создаем обрезанные фото и берем с них размеры окна
                pil_image = Image.fromarray(face_image)
                hight = pil_image.size[0]
                weight = pil_image.size[1]
                pil_image = pil_image.tobytes()
                i= i+1
                #Вносим значения в виде: bytes, int, int, самого фото и его размеры.
                channel.basic_publish(exchange='',
                                      routing_key='face',
                                      body=pil_image)
                hight = hight.encode()
                channel.basic_publish(exchange='',
                                      routing_key='width',
                                      body=hight)
                weight = weight.encode()
                channel.basic_publish(exchange='',
                                      routing_key='hight',
                                      body=weight)
                print(" [x] Sent ")
                connection.close()
                # Вырубаем на четвертом круге.
                if i >= 3:
                    i=0
                    break

        print('Is Ok')
