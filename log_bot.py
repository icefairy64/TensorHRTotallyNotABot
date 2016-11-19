#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def create_new_user(id,name,surname):
    y=os.getcwd() + '/info_candidats'
    create_new(y)
    new_user(id,name,surname)

def get_info_user(id):
    file_info = file(id + "/" + id + '_perepiska.html')
    str="</BODY></HTML>"
    file_info.write("<b>" + str + "</br>")
    file_info.close()

def write_characteristic(id,message):
    file_charect = file(id + name + surname + '_characteristic' + '.html', 'a')
    file_charect.write("<b>" + message +"</br>")
    file_charect.close()

def write_message(id,message):
    y = os.getcwd() + '/info_candidats/'
    file_info = file(y + id + "/" + id + '_perepiska.html','a')
    file_info.write("<b>" + message + "=>" + "</b>")
    file_info.close()

def write_answer(id,message):
    y = os.getcwd() + '/info_candidats/'
    file_info = file(y + id + "/" + id + '_perepiska.html','a')
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
    id_file.write( name + " " + surname )
    id_file.close()

    #Создаем html с перепиской пользователя
    file_info = file(folder + id + '_perepiska' + '.html', 'a')
    str = "<HTML><BODY><TITLE>" + name + "_" + surname + "<br><\TITlE>"
    file_info.write(str)
    file_info.close()

    # Создаем html с характеристикой на пользователя
    file_charect = file(folder + id + '_characteristic' + '.html', 'a')
    str = "<HTML><BODY><TITLE>" + name + "_" + surname + "<br><\TITlE>"
    file_charect.write(str)
    file_charect.close()