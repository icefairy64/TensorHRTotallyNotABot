# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions

active_sessions = {}

def handle_incoming_message(sender_id, text, is_keyboard, send_callback):
    session = active_sessions.get(sender_id)

    # Если сессия не найдена - создаем новую

    if session is None:
        session = storage.fetch_session(sender_id)
    
    if session is None:
        storage.store_user(telegram_id=sender_id)
        user = storage.fetch_user_by_telegramid(sender_id)
        session = storage.Session(user)
        active_sessions[sender_id] = session
        send_callback(sender_id, session.jo_question.text, [])
        storage.store_session(session, sender_id)
        return

    # Делаем выбор в зависимости от состояния сессии

    if session.state == storage.Session.STATE_JO:
        # TODO Оцениваем ответ пользователя
        # TODO Отправляем новый вопрос или завершаем ЖО
        for answer in session.jo_question.answers:
            jo_questions.handle_answer(session.user, session.jo_question, text)
            session.jo_question = answer.next_question
            send_callback(sender_id, session.jo_question.text, [])
            break
    elif session.state == storage.Session.STATE_QUIZ:
        # TODO Оцениваем ответ пользователя
        # TODO Отправляем новый вопрос или завершаем тестирование
        pass

    storage.store_session(session, sender_id)
