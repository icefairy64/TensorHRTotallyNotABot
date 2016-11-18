import sqlite3
import json

conn = sqlite3.connect("storage.db")

class QuestionCategory:
    def __init__(self, id, disp_name):
        self.id = id
        self.disp_name = disp_name

class Question:
    def __init__(self, category, level, num, text, answer, id):
        self.category = category
        self.level = level
        self.id = id
        self.text = text
        self.answer = answer

class User:
    def __init__(self, id, telegram_id, name, age, learn_exp, work_exp, skills):
        self.id = id
        self.telegram_id = telegram_id
        self.name = name
        self.age = age
        self.learn_exp = learn_exp
        self.work_exp = work_exp
        self.skills = skills

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
    for row in conn.execute("select * from users"):
        return user_fromdb(row)
    raise Exception("Could not find user with Telegram ID '" + telegram_id + "'")

def store_user(telegram_id, name, age, learn_exp, work_exp, skills):
    exists = False
    uid = -1
    for row in conn.execute("select * from users"):
        uid = row[0]
        exists = True
        break
    # TODO Implement the rest
    