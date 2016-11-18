import sqlite3
import json
import types

conn = sqlite3.connect("storage.db")

class QuestionCategory:
    def __init__(self, cid, disp_name):
        self.cid = cid
        self.disp_name = disp_name

class Question:
    def __init__(self, category, level, num, text, answer, qid):
        self.category = category
        self.level = level
        self.qid = qid
        self.text = text
        self.answer = answer

class User:
    def __init__(self, uid, telegram_id, name, age, learn_exp, work_exp, skills):
        self.uid = uid
        self.telegram_id = telegram_id
        self.name = name
        self.age = age
        self.learn_exp = learn_exp
        self.work_exp = work_exp
        self.skills = skills

def nf(data):
    if type(data) == types.StringType:
        return "'" + data + "'"
    elif type(data) == types.NoneType:
        return "NULL"
    else:
        return data

def user_fromdb(row):
    return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

def fetch_categories():
    res = {}
    for row in conn.execute("select * from question_categories"):
        res[row[0]] = (QuestionCategory(row[0], row[1]))
    return res

def fetch_questions():
    res = []
    cats = fetch_categories()
    for row in conn.execute("select * from quizzes"):
        res.append(Question(cats[row[1]], row[2], row[3], row[4], json.loads(row[5]), row[0]))
    return res

def fetch_user_by_telegramid(telegram_id):
    for row in conn.execute("select * from users where telegram_id={}".format(telegram_id)):
        return user_fromdb(row)
    raise Exception("Could not find user with Telegram ID '{}'".format(telegram_id))

def store_user(telegram_id, name, age, learn_exp, work_exp, skills):
    exists = False
    uid = -1
    for row in conn.execute("select * from users"):
        uid = row[0]
        exists = True
        break
    if exists:
        query = "update users set telegram_id={}, name={}, age={}, learn_exp={}, work_exp={}, skills={} where id={}".format(nf(telegram_id), nf(name), nf(age), nf(learn_exp), nf(work_exp), nf(skills), nf(uid))
    else:
        query = "insert into users (telegram_id, name, age, learn_exp, work_exp, skills) values ({}, {}, {}, {}, {}, {})".format(nf(telegram_id), nf(name), nf(age), nf(learn_exp), nf(work_exp), nf(skills))
    conn.execute(query)
    conn.commit()
    