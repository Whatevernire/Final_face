# Final_facerecognition
Библиотеки:
For Detection device:
from PIL import Image;
import face_recognition;
import os;
import cv2;
import sqlite3;
import pika;
For Server:
import sqlite3;
import numpy as np;
import face_recognition;
import time;
import cv2;
from PIL import Image;
import os;
import pika;
Как это работает: 
1) Добавляем лица:
   Создаем (или ложим) несколько фотографий человека в какую-либо папку, затем запускаем Client.py и вписываем имя человека и местоположение его фото (Например "faces/"), все фотографии должны иметь названия 1.jpeg,2.jpeg и т.д.
2) Включаем Detection.py на устройстве с камерой, скрипт подключается к Rabbitmq и начинает кидать туда данные.
3) Включаем Server.py на сервере и ловим данные с очереди и делаем выводы.

В плане:
Собрать докер контейнер (или сделать комбо из двух контейнеров: один ловит данные с очереди, второй сравнивает).
