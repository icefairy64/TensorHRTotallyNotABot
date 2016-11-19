# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions
import quiz.answer_evaluation

class Session:

    STATE_JO = "JO"
    STATE_QUIZ = "QUIZ"

    def __init__(self, user):
        self.user = user
        self.state = Session.STATE_JO
        self.jo_question = jo_questions.questions["КакаяВакансия"]

active_sessions = {}

def handle_incoming_message(sender_id, text, is_keyboard, send_callback):
    session = active_sessions.get(sender_id)

    # Если сессия не найдена - создаем новую

    if session is None:
        storage.store_user(telegram_id=sender_id)
        user = storage.fetch_user_by_telegramid(sender_id)
        session = Session(user)
        active_sessions[sender_id] = session

    # Делаем выбор в зависимости от состояния сессии

    send_callback(sender_id, text, [])

    if session.state == Session.STATE_JO:
        # TODO Оцениваем ответ пользователя
        # TODO Отправляем новый вопрос или завершаем ЖО
        pass
    elif session.state == Session.STATE_QUIZ:
        # TODO Оцениваем ответ пользователя
        # TODO Отправляем новый вопрос или завершаем тестирование
        pass
