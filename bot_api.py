#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import ssl
import datetime
import log_bot
import telebot
#import business_logic
import config_bot 
from config_bot import bot

id_list = [] #список зарегистрированных пользователей
buttonFact = True #изначально True, изменяется при получении текстового сообщения

# WebhookHandler, process webhook calls
class WebhookHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "WebhookHandler/1.0"

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == config_bot.WEBHOOK_URL_PATH and \
           'content-type' in self.headers and \
           'content-length' in self.headers and \
           self.headers['content-type'] == 'application/json':
            json_string = self.rfile.read(int(self.headers['content-length']))

            self.send_response(200)
            self.end_headers()

            update = telebot.types.Update.de_json(json_string)
            bot.process_new_messages([update.message])
        else:
            self.send_error(403)
            self.end_headers()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
    log_bot.write_message(message.char.id,message.text)
    business_logic.handle_incoming_message(message.char.id,message.text,False)
    

#@bot.message_handler(content_types=["inline_keyboard"])
 
#def CreateNewUser(message.chat.id, message.chat.first_name, message.chat.last_name): 
    #id_list.append(message.chat.id)

#@bot.message_handler(content_types=["text"]) #вызывает следующий метод, когда боту приходит сообщение типа text		
#def List(message):  #Поиск ID в листе
    #if message.chat.id in id_list == False
    #   CreateNewUser(message.chat.id, message.chat.first_name, message.chat.last_name)
#   buttonFact = False
    #Message(message,buttonFact) 
    #bot.send_message( message.chat.id, "Эхо канал" )

#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
 #   bot.reply_to(message, message.text)



# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook( url = config_bot.WEBHOOK_URL_BASE + config_bot.WEBHOOK_URL_PATH, certificate = open( config_bot.WEBHOOK_SSL_CERT, 'r' ) )

# Start server
httpd = BaseHTTPServer.HTTPServer((config_bot.WEBHOOK_LISTEN, config_bot.WEBHOOK_PORT),
                                  WebhookHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               certfile=config_bot.WEBHOOK_SSL_CERT,
                               keyfile=config_bot.WEBHOOK_SSL_PRIV,
                               server_side=True)

httpd.serve_forever()


