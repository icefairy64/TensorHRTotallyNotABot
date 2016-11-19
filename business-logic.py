# -*- encoding: utf-8 -*-

# import telegram_botapi
import storage
import jo_questions

class Session:
    def __init__(self, user):
        self.user = user
        self.state = "Beginning"

active_sessions = {}

def handle_incoming_message(sender_id, text, is_keyboard):
    session = active_sessions[sender_id]

    if (session is None):
        storage.store_user(telegram_id=sender_id)
        user = storage.fetch_user_by_telegramid(sender_id)
        session = Session(user)
        active_sessions[sender_id] = session

    # Do something based on session.state

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