import sqlite3

conn = sqlite3.connect("storage.db")

class QuestionCategory:
    def __init__(self, id, disp_name):
        self.id = id
        self.disp_name = disp_name

def fetch_categories():
    res = []
    for row in conn.execute("select * from question_categories"):
        res.append(QuestionCategory(row[0], row[1]))
