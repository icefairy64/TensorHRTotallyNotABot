# -*- encoding: utf-8 -*-

import json
import io

class JOAnswer:
    def __init__(self, dct):
        self.keywords = dct["kw"]
        self.next_question = dct["next"]

class JOQuestion:
    def __init__(self, name, dct):
        self.name = name
        self.text = dct["text"]
        self.answers = [JOAnswer(x) for x in dct["answers"]]

questions = {}

dct = json.load(open("jo-questions.json", "r", encoding="utf-8"))
for name, sdct in dct.items():
    questions[name] = JOQuestion(name, sdct)
for name, q in questions.items():
    for answ in q.answers:
        answ.next_question = questions[answ.next_question]