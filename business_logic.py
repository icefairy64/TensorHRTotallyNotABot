# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions
import random

from log_bot import *

from parsing import *
from quiz.answer_evaluation import *

from user_report_generator import *

active_sessions = {}

is_active = True

def pause():
    global is_active
    is_active = False
    return True

def restore():
    global is_active
    is_active = True

def eval_answer_rate(answers):
    if len(answers) >= 5:
        res = answers[-5:]  # Last 5 answers

        is_same = True
        lv = res[0].question.level
        sm = 0.0

        for r in res:
            sm += r.grade
            if r.question.level != lv:
                is_same = False
                break

        if is_same and sm >= 3.5:
            return 1
        elif is_same and sm <= 2:
            return -1

    return 0

def send_quiz_question(target, question, callback):
    if question.answer["type"] == 0:
        lst = question.answer["all_answers"]
    else:
        lst = []
    callback(target, question.text, lst, "")

def send_jo_question(target, question, callback):
    if isinstance(question.text, str):
        text = question.text
    else:
        text = random.choice(question.text)
    callback(target, text, [], "")

def get_overall_grade(user):
    answers = storage.fetch_answers_for_user(user)
    sm = 0.0
    for x in answers:
        sm += x.grade
    return sm

def handle_start(sender_id, send_callback):
    if not is_active:
        return

    session = active_sessions.get(sender_id)

    if session is not None:
        del active_sessions[sender_id]
        storage.delete_session(sender_id)

    handle_incoming_message(sender_id, '', False, send_callback)


def handle_incoming_message(sender_id, text, is_keyboard, send_callback):
    if not is_active:
        return

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
        send_jo_question(sender_id, session.jo_question, send_callback)
        storage.store_session(session, sender_id)
        return

    # Делаем выбор в зависимости от состояния сессии

    if session.state == storage.Session.STATE_JO:
        # Сначала берём первый попавшийся ответ
        #answer = session.jo_question.answers[0]

        # Заменяем C++
        if u'C++' in text:
            text = text.replace(u'C++', u'cpp')
        elif u'с++' in text:
            text = text.replace(u'C++', u'cpp')
        elif u'си++' in text:
            text = text.replace(u'си++', u'cpp')

        jo_questions.handle_answer(session.user, session.jo_question, text)
            # Если ответ не был записан в анкету, значит надо проанализировать его
        answer = jo_questions.get_best_answer(text, session.jo_question)

        if answer.quiz_id is not None:
            session.quiz_id = answer.quiz_id

        n_jo_quest = answer.next_question

        if n_jo_quest is not None:
            send_jo_question(sender_id, n_jo_quest, send_callback)
            session.jo_question = n_jo_quest
        else:
            # Переходим на тестирование
            session.state = storage.Session.STATE_QUIZ
            storage.clear_quiz_history(session.user.uid)
            session.quiz_question = storage.fetch_next_question_for_user(
                session.user, session.quiz_id or 1, 1)
            send_quiz_question(sender_id, session.quiz_question, send_callback)

    elif session.state == storage.Session.STATE_QUIZ:
        quest = session.quiz_question

        # if quest.answer["type"] == 0 and not is_keyboard:
        #     send_callback(sender_id, u"Пожалуйста, выберите ответ из перечисленных выше.", [])
        #     return

        mark = AnswerEvaluation.factory(quest.answer["type"]).estimate(
            text if quest.answer["type"] == AnswerEvaluation.SINGLE_CHOICE else list(
                split_string(text)),
            quest.get_params())

        storage.store_users_answer(session.user, quest, text, mark)

        answs = storage.fetch_answers_for_user(session.user)

        answer_rate = eval_answer_rate(answs)

        # Adjusting question level
        if answer_rate >= 1:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level + 1)
        elif answer_rate <= -1:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level - 1)
        else:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level)

        # Some weird case
        if n_quest is None and len(answs) < 1:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level + 1)

        if n_quest is None and quest.level < 4:
            n_quest = storage.fetch_next_question_for_user(
                session.user, quest.category.cid, quest.level + 1)

        if len(answs) >= 5:
           n_quest = None

        # No more questions. For real now.
        if n_quest is None:
            session.state = storage.Session.STATE_FIN
            generate_report_for_user(storage.fetch_user_by_telegramid(sender_id), "info_candidats/{}/cv.html".format(sender_id))
            send_callback(sender_id, u"Спасибо за ответы, мы с вами свяжемся.\nУдачного дня!", [], get_info_user(sender_id))
            score = int(100*get_overall_grade(session.user) / len(answs))
            #report = u'{} прошёл тест по {}, набрал {} баллов из 100'.format(session.user.name, 
            #                                                                 ['Python', 'Java', 'C++'][session.quiz_id or 1],
            #                                                                 score)
            #send_callback(sender_id, report, [], "")

        else:
            send_quiz_question(sender_id, n_quest, send_callback)
            session.quiz_question = n_quest

    elif session.state == storage.Session.STATE_FIN:
        send_callback(sender_id, storage.get_random_answer(), [], "")

    storage.store_session(session, sender_id)
