# -*- encoding: utf-8 -*-

import json
import io
import codecs

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

dct = None
with codecs.open("jo-questions.json", "r", encoding="utf-8") as q:
    dct = json.load(q)

if dct is not None:
    for name, sdct in dct.items():
        questions[name] = JOQuestion(name, sdct)
    for name, q in questions.items():
        for answ in q.answers:
            answ.next_question = questions[answ.next_question]
