# -*- encoding: utf-8 -*-

import storage
import jo_questions
import user_report_generator

# Some examples of Storage API usage

print(storage.fetch_questions()[0].answer["type"])

user = storage.fetch_user_by_telegramid("11")

if user == None:
    print("No user found")
else:
    print(u"{}'s answers:".format(user.name))

    for answer in user.get_answers():
        print(u"Question: '{}'; answer: '{}'; grade: {}".format(answer.question.text, answer.text, answer.grade))
    
    print(storage.fetch_next_question_for_user(user, 1))
    print(storage.fetch_next_question_for_user(user, 2))

# JO Questions example

question = jo_questions.questions[u"КакаяВакансия"]
if not (question is None):
    print(u"JO Question: {}".format(question.text))
    for answer in question.answers:
        print(u"\tAnswer -- keywords: {}, next question: {}".format(answer.keywords, answer.next_question.text))

# Report generation

user_report_generator.generate_report_for_user(user, "demo-rep.txt")