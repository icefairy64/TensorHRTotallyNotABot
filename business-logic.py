# import telegram_botapi
import storage

def handle_incoming_message(text, is_keyboard, sender_id): 
    print("TODO")

# Some examples of Storage API usage

print(storage.fetch_questions()[0].answer["type"])

user = storage.fetch_user_by_telegramid("11")

if user == None:
    print("No user found")
else:
    print("{}'s answers:".format(user.name))

    for answer in user.get_answers():
        print("Question: '{}'; answer: '{}'; grade: {}".format(answer.question.text, answer.text, answer.grade))