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
operator_id = 245898202
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


def send_message(id,text,list):
    if list.count == 0:
        bot.send_message(id, text)
        bot.send_message(operator_id, text)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for it in list:
           print(it)
           keyboard.add(types.InlineKeyboardButton(text=it, callback_data=it))
        bot.send_message(id, text, reply_markup=keyboard)
        bot.send_message(operator_id, text)

def scan_database(message):
    if log_bot.scan_directory(message.chat.id) == False:
          log_bot.create_new_user(message.chat.id,message.chat.first_name,message.chat.last_name)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    # list = ["pret","pok", "text"]
    # send_message(message.chat.id,message.text,list)
    print("text")
    scan_database(message)
    print("text")
    business_logic.handle_incoming_message(message.chat.id,message.text,False,send_message)
    print("text")
    print(message.chat.id)
    print(message.text)
    #log_bot.write_message(message.chat.id,message.text)
    print(message.chat.id)
    bot.send_message(operator_id,"bolvanka")
    print("sent")



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        print("keyb")
        bot.send_message(operator_id, call.message.text)
        business_logic.handle_incoming_message(call.message.chat.id, call.message.text, True, send_message)
        log_bot.write_message(call.message.chat.id, call.message.text)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        # Уведомление в верхней части экрана
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пыщь!")



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
