from time import sleep
from twx.botapi import TelegramBot, ReplyKeyboardHide, ReplyKeyboardMarkup

from business_logic import *

class Bot:

    def __init__(self, token):
        self.bot = TelegramBot(token)
        self.offset = 0

    def start(self):
        while True:
            updates = self.bot.get_updates(self.offset).wait()

            for update in updates:
                print(update.message.text)
                if update.message.text == '/start':
                    handle_start(update.message.sender.id, self.send)
                else:
                    handle_incoming_message(update.message.sender.id, update.message.text, False, self.send)
                    
                self.offset = update.update_id + 1

            sleep(1)

    def send(self, user_id, text, keyboard_list):
        rm = ReplyKeyboardMarkup.create(keyboard=[[x] for x in keyboard_list],one_time_keyboard=True) if keyboard_list != [] else None
        return self.bot.send_message(user_id, text, reply_markup=rm).wait()

bot = Bot('223961538:AAEqWbRFTbUfJuWJOLaWM16znnIDVgR962A')
print("Starting Bot...")
bot.start()