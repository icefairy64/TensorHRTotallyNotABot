# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot

TOKEN = '265796484:AAF0Z9OowrO7mImQuuDSVXoWh3dE6f_Xfok'

WEBHOOK_HOST   = 'itrial.tech'
WEBHOOK_PORT   = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = 'itrial.tech'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

#WEBHOOK_SSL_CERT = '/etc/letsencrypt/live/itrial.tech/cert.pem'     # Путь к сертификату
#WEBHOOK_SSL_PRIV = '/etc/letsencrypt/live/itrial.tech/privkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % ( WEBHOOK_HOST, WEBHOOK_PORT )
WEBHOOK_URL_PATH = "/hr-bot-test/%s/" % ( TOKEN )

bot = telebot.TeleBot( TOKEN )
