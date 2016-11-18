import sqlite3
import json

conn = sqlite3.connect("storage.db")

class QuestionCategory:
    def __init__(self, id, disp_name):
        self.id = id
        self.disp_name = disp_name

class Question:
    def __init__(self, category, level, id, text, answer):
        self.category = category
        self.level = level
        self.id = id
        self.text = text
        self.answer = answer

def fetch_categories():
    res = {}
    for row in conn.execute("select * from question_categories"):
        res[row[0]] = (QuestionCategory(row[0], row[1]))
    return res

def fetch_questions():
    res = []
    cats = fetch_categories()
    for row in conn.execute("select * from quizzes"):
        res.append(Question(cats[row[0]], row[1], row[2], row[3], json.loads(row[4])))
    return res