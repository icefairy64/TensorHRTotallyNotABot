#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with CherryPy
# It echoes any incoming text messages and does not use the polling method.

import cherrypy
import telebot
import logging
import config_bot
from config_bot import bot
from telebot import types
import business_logic
import log_bot

from traceback import *

operator_id = 244811534
send_msg_operator_f = True
intercept_communication = False
current_id_user = ""

# WebhookServer, process webhook calls
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


def send_message(id,text,list,url):
    try:
        global send_msg_operator_f
        if not len( url ) == 0:
            bot.send_message( operator_id, u"Отчет: http://itrial.tech/git-master/TensorHRTotallyNotABot/" + url )
            bot.send_message(id, text)
        else:
            if list.count == 0:
                bot.send_message(id, text)
                if send_msg_operator_f == True:
                    send_msg_operator('БОТ: ' + text)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for it in list:
                    print(it)
                    keyboard.add(types.InlineKeyboardButton(text=it, callback_data=it))
                bot.send_message(id, text, reply_markup=keyboard)
                if send_msg_operator_f == True:
                    send_msg_operator('БОТ: ' + text)
            log_bot.write_answer(id, text)
    except Exception as e:
        print_exc()
        raise e
    

def scan_database(message):
    try:
        if log_bot.scan_directory(message.chat.id) == False:
            log_bot.create_new_user(message.chat.id,message.chat.first_name,message.chat.last_name)
    except Exception as e:
        print_exc()
        raise e

def send_msg_operator( msg ):
    print('To operator:', msg)
    try:
        # Создаем клавиатуру и каждую из кнопок (по 2 в ряд)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        pause_button = types.InlineKeyboardButton(text=u"Приостановить общение бота", callback_data="pause_send_msg_oper")
        start_button = types.InlineKeyboardButton(text=u"Возобновить общение бота", callback_data="start_send_msg_oper")
        disable_button = types.InlineKeyboardButton(text=u"Отключить сообщения оператору", callback_data="disable_msg_operator")
        enable_button = types.InlineKeyboardButton(text=u"Возобновить сообщения оператору", callback_data="enable_msg_operator")
        keyboard.add(pause_button, start_button, disable_button, enable_button)
        bot.send_message(operator_id, msg, reply_markup=keyboard)
    except Exception as e:
        print_exc()
        raise e

@bot.message_handler(commands=['start'])
def handle_text(message):
    try:
        business_logic.handle_start( message.chat.id, send_message )
        log_bot.create_new_user( message.chat.id, message.chat.first_name, message.chat.last_name )
    except Exception as e:
        print_exc()
        raise e

@bot.message_handler(content_types=["text"])
def any_msg(message):
    try:
        global current_id_user
        global send_msg_operator_f
        print('Incoming message', message.chat.id, message.text)
        if intercept_communication == True:
            print('Intercept')
            if message.chat.id == operator_id:
                print('Operator -> User')
                bot.send_message( current_id_user, message.text )
                log_bot.write_message(message.chat.id, message.text)
                #log_bot.write_answer(message.chat.id, message.text)
            else:#if message.chat.id == current_id_user:
                print('User -> Operator') 
                bot.send_message( operator_id, message.text )
                log_bot.write_answer(message.chat.id, message.text)
                #log_bot.write_message(message.chat.id, message.text)
        else:
            print('No intercept')
            
            if send_msg_operator_f:
                print('Sending to operator')
                send_msg_operator(message.text)
                log_bot.write_message(message.chat.id, message.text)

            if not message.chat.id == operator_id:
                print('User')
                current_id_user = message.chat.id
                business_logic.handle_incoming_message(message.chat.id,message.text,False,send_message)

    except Exception as e:
        print_exc()
        raise e


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        global send_msg_operator_f
        global intercept_communication
        # Если сообщение из чата с ботом
        if call.message:
            if call.data == "disable_msg_operator":
                print("disable_msg_operator")
                send_msg_operator_f = False
            if call.data == "enable_msg_operator":
                send_msg_operator_f = True
                print("enable_msg_operator")
            if call.data == "pause_send_msg_oper":
                business_logic.pause()
                intercept_communication=True
                print("pause_send_msg_oper")
            if call.data == "start_send_msg_oper":
                business_logic.restore()
                intercept_communication=False
                print("start_send_msg_oper")

            print("keyb")
            bot.send_message(operator_id, call.message.text)
            business_logic.handle_incoming_message(call.message.chat.id, call.message.text, True, send_message)
            log_bot.write_message(call.message.chat.id, call.message.text)
    except Exception as e:
        print_exc()
        raise e

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=config_bot.WEBHOOK_URL_BASE + config_bot.WEBHOOK_URL_PATH,
                certificate=open( config_bot.WEBHOOK_SSL_CERT, 'r' ) )

# Start cherrypy server
cherrypy.config.update({
    'server.socket_host': config_bot.WEBHOOK_LISTEN,
    'server.socket_port': config_bot.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config_bot.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config_bot.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), config_bot.WEBHOOK_URL_PATH, {'/': {}})
