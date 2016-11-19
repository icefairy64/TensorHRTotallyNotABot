# import telegram_botapi
import storage

def handle_incoming_message(text, is_keyboard, sender_id): 
    print("TODO")

# Some examples of Storage API usage
print(storage.fetch_questions()[0].answer["type"])

print(storage.fetch_next_question(1))
print(storage.fetch_next_question_onlevel(1))