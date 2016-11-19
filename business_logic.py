# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions

from parsing import *
from quiz.answer_evaluation import *

active_sessions = {}


def eval_answer_rate(answers):
    if len(answers) >= 5:
        res = answers[-5:]  # Last 5 answers

        is_same = True
        lv = res[0].question.level
        sum = 0.0

        for r in res:
            sum += r.grade
            if r.question.level != lv:
                is_same = False
                break

        if is_same and sum >= 3.5:
            return 1
        elif is_same and sum <= 2:
            return -1

    return 0

def send_quiz_question(target, question, callback):
    if question.answer["type"] == 0:
        lst = question.answer["right_answer"]
    else:
        lst = []
    callback(target, question.text, lst)

def handle_incoming_message(sender_id, text, is_keyboard, send_callback):
    session = active_sessions.get(sender_id)

    # Если сессия не найдена - создаем новую

    if session is None:
        session = storage.fetch_session(sender_id)
        active_sessions[sender_id] = session

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
        # Сначала берём первый попавшийся ответ
        answer = session.jo_question.answers[0]

        if not jo_questions.handle_answer(session.user, session.jo_question, text):
            # Если ответ не был записан в анкету, значит надо проанализировать его
            answer = jo_questions.get_best_answer(text, session.jo_question)

        n_jo_quest = answer.next_question

        if n_jo_quest is not None:
            send_callback(sender_id, session.jo_question.text, [])
            session.jo_question = n_jo_quest
        else:
             # Переходим на тестирование
            session.state = storage.Session.STATE_QUIZ
            # TODO Использовать не-захадкоженную категорию
            session.quiz_question = storage.fetch_next_question_for_user(
                session.user, 1, 1)
            send_quiz_question(sender_id, session.quiz_question, send_callback)

    elif session.state == storage.Session.STATE_QUIZ:
        quest = session.quiz_question

        mark = AnswerEvaluation.factory(quest.answer["type"]).estimate(
            text if quest.answer["type"] == AnswerEvaluation.SINGLE_CHOICE else list(
                split_string(text)),
            quest.get_params())

        storage.store_users_answer(session.user, quest, text, mark)

        answer_rate = eval_answer_rate(
            storage.fetch_answers_for_user(session.user))

        if answer_rate >= 1:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level + 1)
        elif answer_rate <= -1:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level - 1)
        else:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level)

        if n_quest is None:
            session.state = "FIN"
            send_callback(sender_id, u"Конец", [])
        else:
            send_quiz_question(sender_id, n_quest, send_callback)
            session.quiz_question = n_quest

    elif session.state == storage.Session.STATE_FIN:
        # TODO Fetch random text
        send_callback(sender_id, u"Конец", [])

    storage.store_session(session, sender_id)
