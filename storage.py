# -*- encoding: utf-8 -*-

import sqlite3
import json
import random
import time
import jo_questions
import codecs

class QuestionCategory:
    def __init__(self, cid, disp_name):
        self.cid = cid
        self.disp_name = disp_name

class Question:
    def __init__(self, category, level, num, text, answer, qid):
        self.category = category
        self.level = level
        self.num = num
        self.qid = qid
        self.text = text
        self.answer = answer

    def get_params(self):
        if self.answer["type"] == 0:
            return self.answer["right_answer"]
        elif self.answer["type"] == 1:
            return self.answer["right_answer"]
        elif self.answer["type"] == 2:
            return self.answer["keywords"]

class User:
    def __init__(self, uid, telegram_id, name, age, learn_exp, work_exp, skills, desired_job):
        self.uid = uid
        self.telegram_id = telegram_id
        self.name = name
        self.age = age
        self.learn_exp = learn_exp
        self.work_exp = work_exp
        self.skills = skills
        self.desired_job = desired_job

    def get_answers(self):
        return fetch_answers_for_user(self)

class UsersAnswer:
    def __init__(self, user, question, text, grade, timestamp):
        self.user = user
        self.question = question
        self.text = text
        self.grade = grade
        self.timestamp = timestamp

def nf(data):
    if isinstance(data, str):
        return "'" + data + "'"
    elif data is None:
        return "NULL"
    else:
        return data

def user_fromdb(row):
    return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

def fetch_categories():
    res = {}
    for row in sqlite3.connect("storage.db").execute(u"select * from question_categories"):
        res[row[0]] = (QuestionCategory(row[0], row[1]))
    return res

def fetch_questions():
    res = []
    cats = fetch_categories()
    for row in sqlite3.connect("storage.db").execute(u"select * from quizzes"):
        print("Debug info: ", row[0])
        res.append(Question(cats[row[1]], row[2], row[3], row[4], json.loads(row[5]), row[0]))
    return res

g_categories = fetch_categories()
g_questions = fetch_questions()

rnda = codecs.open("universal_answer.txt", "r", encoding="utf-8")
random_answers = rnda.readlines()

class Session:

    STATE_JO = "JO"
    STATE_QUIZ = "QUIZ"
    STATE_FIN = "FIN"

    def __init__(self, user, state=None, jo_question=None, quiz_question=None, quiz_id=None):
        self.user = user

        if state is None:
            self.state = Session.STATE_JO
        else:
            self.state = state

        if jo_question is None:
            self.jo_question = jo_questions.questions[u"Начало"] #Начало
        else:
            self.jo_question = jo_question

        if quiz_question is None:
            self.quiz_question = g_questions[1]
        else:
            self.quiz_question = quiz_question

        self.quiz_id = quiz_id

def question_order(question):
    return question.level * 65535 + question.num

def fetch_next_question(question_id):
    """Returns next question relative to given one (with possible level change) or None if there is no more questions within that category"""
    tq = next(x for x in g_questions if x.qid == question_id)
    samecat = [x for x in g_questions if x.category.cid == tq.category.cid and question_order(x) > question_order(tq)]
    samecat.sort(key=question_order)
    if len(samecat) == 0:
        return None
    return samecat[0]

def fetch_next_question_onlevel(question_id):
    """Returns next question within one level with given one or None if there is no more questions on that level"""
    tq = next(x for x in g_questions if x.qid == question_id)
    samelvl = [x for x in g_questions if x.category.cid == tq.category.cid and x.level == tq.level and x.num > tq.num]
    samelvl.sort(key=question_order)
    if len(samelvl) == 0:
        return None
    return samelvl[0]

def fetch_user_by_telegramid(telegram_id):
    for row in sqlite3.connect("storage.db").execute(u"select * from users where telegram_id=?", [telegram_id]):
        return user_fromdb(row)
    raise Exception("Could not find user with Telegram ID '{}'".format(telegram_id))

def fetch_next_question_for_user(user, cat, level):
    answered = user.get_answers()

    qs = [x for x in g_questions if x.level == level and x.category.cid == cat and len([z for z in answered if z.question.qid == x.qid]) == 0]

    if len(qs) == 0:
        return None
    return random.choice(qs)
    

def store_user(telegram_id, name=None, age=None, learn_exp=None, work_exp=None, skills=None, desired_job=None):
    exists = False
    uid = -1
    for row in sqlite3.connect("storage.db").execute("select id from users where telegram_id=?", [telegram_id]):
        uid = row[0]
        exists = True
        break
    if exists:
        query = u"update users set telegram_id=?, name=?, age=?, learn_exp=?, work_exp=?, skills=?, desired_job=? where id=?"
        conn = sqlite3.connect("storage.db")
        conn.execute(query, [telegram_id, name, age, learn_exp, work_exp, skills, desired_job, uid])
        conn.commit()
        conn.close()
    else:
        query = u"insert into users (telegram_id, name, age, learn_exp, work_exp, skills, desired_job) values (?, ?, ?, ?, ?, ?, ?)"
        conn = sqlite3.connect("storage.db")
        conn.execute(query, [telegram_id, name, age, learn_exp, work_exp, skills, desired_job])
        conn.commit()
        conn.close()

def update_user(user):
    store_user(user.telegram_id, user.name, user.age, user.learn_exp, user.work_exp, user.skills, user.desired_job)

def fetch_answers_for_user(user):
    res = []
    for row in sqlite3.connect("storage.db").execute(u"select question_id, raw_answer, answer_grade, answer_time from users_answers where user_id={} order by answer_time".format(user.uid)):
        res.append(UsersAnswer(user, next(x for x in g_questions if x.qid == row[0]), row[1], row[2], row[3]))
    return res

def store_users_answer(user, question, answer_text, grade):
    exists = False
    for row in sqlite3.connect("storage.db").execute(u"select user_id from users_answers where user_id={} and question_id={}".format(user.uid, question.qid)):
        exists = True
        break
    if exists:
        return

    conn = sqlite3.connect("storage.db")
    conn.execute(u"insert into users_answers (user_id, question_id, raw_answer, answer_grade, answer_time) values (?, ?, ?, ?, ?)",
                 (user.uid, question.qid, answer_text, grade, int(time.time())))
    conn.commit()
    conn.close()

def fetch_session(session_id):
    for row in sqlite3.connect("storage.db").execute(u"select state, jo_question, quiz_question from sessions where session_id={}".format(session_id)):
        return Session(fetch_user_by_telegramid(session_id), row[0], jo_questions.questions[row[1]], g_questions[row[2]])
    return None

def store_session(session, session_id):
    exists = False
    sid = -1
    for row in sqlite3.connect("storage.db").execute(u"select session_id from sessions where session_id={}".format(session_id)):
        exists = True
        sid = row[0]
    if exists:
        conn = sqlite3.connect("storage.db")
        conn.execute(u"update sessions set state={}, jo_question={}, quiz_question={} where session_id={}".format(nf(session.state), nf(session.jo_question.name), nf(session.quiz_question.qid), sid))
        conn.commit()
    else:
        conn = sqlite3.connect("storage.db")
        conn.execute(u"insert into sessions (session_id, state, jo_question, quiz_question) values ({}, {}, {}, {})".format(nf(session_id), nf(session.state), nf(session.jo_question.name), nf(session.quiz_question.qid)))
        conn.commit()

def delete_session(session_id):
    conn = sqlite3.connect("storage.db")
    conn.execute(u"delete from sessions where session_id = {}".format(nf(session_id)))
    conn.commit()
    conn.close()

def clear_quiz_history(user_id):
    conn = sqlite3.connect("storage.db")
    conn.execute(u"delete from users_answers where user_id = {}".format(user_id))
    conn.commit()
    conn.close()

def get_random_answer():
    return random.choice(random_answers)
