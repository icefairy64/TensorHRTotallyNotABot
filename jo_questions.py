# -*- encoding: utf-8 -*-

import json
import io
import codecs
import storage

class JOAnswer:
    def __init__(self, dct):
        self.keywords = dct["kw"]
        self.next_question = dct["next"]

class JOQuestion:
    def __init__(self, name, dct):
        self.name = name
        self.text = dct["text"]
        self.answers = [JOAnswer(x) for x in dct["answers"]]
        self.save_to = dct.get("save_to")

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

def handle_answer(user, question, answer_text):
    if question.save_to == "name":
        user.name = answer_text
    elif question.save_to == "age":
        user.age = answer_text
    elif question.save_to == "learn_exp":
        user.learn_exp = answer_text
    elif question.save_to == "work_exp":
        user.work_exp = answer_text
    elif question.save_to == "skills":
        user.skills = answer_text
    elif question.save_to == "desired_job":
        user.desired_job = answer_text
    if question.save_to is not None:
        storage.update_user(user)
