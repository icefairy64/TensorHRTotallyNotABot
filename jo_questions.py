# -*- encoding: utf-8 -*-

import json
import io
import codecs
import storage
import parsing


class JOAnswer:

    def __init__(self, dct):
        self.keywords = dct["kw"]
        self.next_question = dct["next"]
        self.quiz_id = dct.get("quiz")


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
            answ.next_question = questions[
                answ.next_question] if answ.next_question in questions else None


def handle_answer(user, question, answer_text):
    """
    Попробовать записать ответ в анкету.
    Вернёт True, если получилось записать в анкету.
    Если это неанкетный вопрос - возвращается False.
    """
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
        return True
    else:
        return False


def get_best_answer(text, question):
    """
    Выбрать answer, который лучше всего подходит под ответ пользователя
    """

    if len(question.answers) == 1:
        return question.answers[0]

    def consider_kw(user_kw, answer_kw):
        if answer_kw == []:
            return 0

        kws = [a for a in user_kw if a in answer_kw]
        return len(kws) / float(len(answer_kw))

    user_answer = parsing.split_string(text)
    coefs = [consider_kw(user_answer, a.keywords) for a in question.answers]

    max_coef = max(coefs)

    if max_coef == 0:
        return question.answers[-1]

    return question.answers[coefs.index(max_coef)]
