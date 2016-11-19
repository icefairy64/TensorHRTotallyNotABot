# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions

class Session:
    def __init__(self, user):
        self.user = user
        self.state = "Beginning"

active_sessions = {}

def handle_incoming_message(sender_id, text, is_keyboard):
    session = active_sessions[sender_id]

    if (session is None):
        storage.store_user(telegram_id=sender_id)
        user = storage.fetch_user_by_telegramid(sender_id)
        session = Session(user)
        active_sessions[sender_id] = session

    # Do something based on session.state