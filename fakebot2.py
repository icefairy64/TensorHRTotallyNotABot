#-*-encoding:utf-8-*-
from time import sleep
from twx.botapi import TelegramBot, ReplyKeyboardHide, ReplyKeyboardMarkup, InputFileInfo, InputFile

from business_logic import *

class Bot:

    def __init__(self, token):
        self.bot = TelegramBot(token)
        self.offset = 0
        self.admin_id = 244811534

    def start(self):        
        while True:
            updates = self.bot.get_updates(self.offset).wait()

            for update in updates:
                if update.message.sender.id == self.admin_id:
                    continue

                if update.message.text == '/start':
                    handle_start(update.message.sender.id, self.send)

                    self.send(self.admin_id, u'Началось собеседование c ' + update.message.sender.first_name + ' ' + update.message.sender.last_name)
                else:
                    handle_incoming_message(update.message.sender.id, update.message.text, False, self.send)
                    
                self.offset = update.update_id + 1

            sleep(2)

    def send(self, user_id=None, text=None, keyboard_list=[], report=None):
        if report is not None:
            self.send(self.admin_id, report)
            # fp = open(report, 'rb')
            # file_info = InputFileInfo(report, fp, 'text/html')
            # report_file = InputFile('photo', file_info)
            # result = self.bot.send_document(self.admin_id, report_file).wait()
            return

        rm = ReplyKeyboardMarkup.create(keyboard=[[x] for x in keyboard_list],one_time_keyboard=True) if keyboard_list != [] else None
        return self.bot.send_message(user_id, text, reply_markup=rm).wait()

bot = Bot('223961538:AAEqWbRFTbUfJuWJOLaWM16znnIDVgR962A')
print("Starting Bot...")
#bot.send(report=u'report.html')
bot.start()