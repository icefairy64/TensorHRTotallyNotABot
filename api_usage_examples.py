# -*- encoding: utf-8 -*-

import storage
import jo_questions

# Some examples of Storage API usage

print(storage.fetch_questions()[0].answer["type"])

user = storage.fetch_user_by_telegramid("11")

if user == None:
    print("No user found")
else:
    print("{}'s answers:".format(user.name))

    for answer in user.get_answers():
        print("Question: '{}'; answer: '{}'; grade: {}".format(answer.question.text, answer.text, answer.grade))
    
    print(storage.fetch_next_question_for_user(user, 1))
    print(storage.fetch_next_question_for_user(user, 2))

# JO Questions example

question = jo_questions.questions["КакаяВакансия"]
if not (question is None):
    print("JO Question: {}".format(question.text))
    for answer in question.answers:
        print("\tAnswer -- keywords: {}, next question: {}".format(answer.keywords, answer.next_question.text))