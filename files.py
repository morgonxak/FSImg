#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Модуль для работы к файломи
#Сортировка раскодрованного видео

from PIL import Image
import os

def getDataFolder(path = "image"):
    return os.listdir(path)


def getImage(i):
    pach = "D:\geo\/fotoItog/"
    pachItog = "D:\geo\/fotoItog2/"

    listImage = getDataFolder(pach)

    image = Image.open(pach + '/' + listImage[i])
    image.save(pachItog + listImage[i])


if __name__ == '__main__':  # Program start from here
    try:

        print("Файлы")
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print("stop")