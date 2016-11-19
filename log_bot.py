#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import subprocess as sp
from zipfile import ZipFile

def create_new_user(id,name,surname):
    y=os.getcwd() + '/info_candidats'
    create_new(y)
    new_user(id,name,surname)

def get_info_user(id):
    folder = 'info_candidats/' + id + "/"

    file_info = file(folder + 'perepiska.html','a')
    str="</BODY></HTML>"
    file_info.write("<b>" + str + "</br>")
    file_info.close()

    file_name = open(folder + id + '.txt', 'r')
    for line in file_name:
         print(line)

    command_1 = "athenapdf/athenapdf " + folder + 'perepiska.html ' + folder + line + '_info.pdf'
    print(command_1 )

    subprocess.call(command_1, shell=True)

    command_2 ="athenapdf/athenapdf " + folder +  'cv.html ' + folder + line + '_charect.pdf'
    print(command_2)

    subprocess.call(command_2, shell=True)

    filename = __file__

    # Создание архива
    z = ZipFile(folder +line+ '.zip', 'w')
    # Добавление файла в архив
    z.write(filename, line + '_info.pdf')
    z.write(filename, line + '_charect.pdf')
    z.close()

def write_characteristic(id,cv):
    folder = 'info_candidats/' + id + "/"
    file_charect = file(folder + 'cv.html', 'wb')
    file_charect.write(cv)
    file_charect.close()

def write_message(id,message):
    y = os.getcwd() + '/info_candidats/'
    file_info = file(y + id + "/" + 'perepiska.html','a')
    file_info.write("<b>" + message + "=>" + "</b>")
    file_info.close()

def write_answer(id,message):
    y = os.getcwd() + '/info_candidats/'
    file_info = file(y + id + "/" + 'perepiska.html','a')
    file_info.write("<b>" + message + "</br>")
    file_info.close()

def create_new(y):
    print(y)
    if not os.path.exists(y):
        os.mkdir(y)

def new_user(id,name,surname):
    #Создаем папку для нового пользователя
    folder = os.getcwd() + '/info_candidats/' + id + "/"
    create_new(folder)

    #Сохраняем имя и фамилию по идентификатору для дальнейшей работы
    id_file = file( folder + id + ".txt", 'wb' )
    id_file.write( name + "_" + surname )
    id_file.close()

    #Создаем html с перепиской пользователя
    file_info = file(folder + 'perepiska' + '.html', 'a')
    str = "<HTML><BODY><TITLE>" + name + "_" + surname + "<br><\TITlE>"
    file_info.write(str)
    file_info.close()

    # Создаем html с характеристикой на пользователя
    file_charect = file(folder + 'cv.html', 'a')
    file_charect.close()