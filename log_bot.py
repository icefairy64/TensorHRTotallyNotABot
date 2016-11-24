#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import subprocess as sp
from zipfile import ZipFile

from io import *
import pathlib

def create_new_user(id,name,surname):
    print("Creating new user", id)
    y=os.getcwd() + '/info_candidats'
    create_new(y)
    new_user(id,name,surname)

def get_info_user(idd):
    id = str(idd)
    folder = 'info_candidats/' + id + "/"

    file_info = open(folder + 'perepiska.html','a')
    st="</BODY></HTML>\n"
    file_info.write("<br/>" + st)
    file_info.close()

    if pathlib.Path(folder + id + '.txt').exists():
        file_name = open(folder + id + '.txt', 'r')
        for line in file_name:
            print(line)

    command_1 = "athenapdf/athenapdf " + folder + 'perepiska.html ' + folder + id + '_info.pdf'
    print(command_1 )

    subprocess.call(command_1, shell=True)

    command_2 ="athenapdf/athenapdf " + folder +  'cv.html ' + folder + id + '_charect.pdf'
    print(command_2)

    subprocess.call(command_2, shell=True)

    filename = __file__

    # Создание архива
    zip_archive = folder + id + '.zip'
    z = ZipFile(zip_archive, 'w')
    # Добавление файла в архив
    z.write(folder + id + '_info.pdf', id + '_info.pdf')
    z.write(folder + id + '_charect.pdf', id + '_charect.pdf')
    z.close()

    return zip_archive

def write_characteristic(idd,cv):
    id = str(idd)
    folder = 'info_candidats/' + id + "/"
    create_new(folder)
    file_charect = open(folder + 'cv.html', 'w')
    file_charect.write(cv)
    file_charect.close()

def write_message(idd,message):
    id = str(idd)
    y = os.getcwd() + '/info_candidats/'
    create_new(y + id + "/")
    file_info = open(y + id + "/" + 'perepiska.html','a')
    file_info.write('<br/>\n')
    file_info.write(message)
    file_info.close()

def write_answer(idd,message):
    id = str(idd)
    y = os.getcwd() + '/info_candidats/'
    create_new(y + id + "/")
    file_info = open(y + id + "/" + 'perepiska.html','a')
    file_info.write('<br/>\n')
    file_info.write(message)
    file_info.close()

def create_new(y):
    print("Creating dir", y)
    if not os.path.exists(y):
        os.mkdir(y)

def new_user(idd,name,surname):
    print("Creating folder for user", idd)
    id = str(idd)

    #Создаем папку для нового пользователя
    folder = os.getcwd() + '/info_candidats/' + id + "/"
    create_new(folder)

    #Сохраняем имя и фамилию по идентификатору для дальнейшей работы
    id_file = open( folder + id + ".txt", 'w' )
    id_file.write( "{}_{}".format(name, surname) )
    id_file.close()

    #Создаем html с перепиской пользователя
    file_info = open(folder + 'perepiska' + '.html', 'w')
    st = u'<HTML><head><TITLE>{}_{}</TITLE><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>\n'.format(name, surname)
    file_info.write(st)
    file_info.close()

    # Создаем html с характеристикой на пользователя
    file_charect = open(folder + 'cv.html', 'w')
    file_charect.close()
