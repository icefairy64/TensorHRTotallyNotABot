# import telegram_botapi
import storage

def handle_incoming_message(text, is_keyboard, sender_id): 
    print("TODO")

print(storage.fetch_questions()[0].answer["type"])
storage.store_user("11", "Breezy", 27, None, None, "A lot of")
print(storage.fetch_user_by_telegramid("11").learn_exp)
print(storage.fetch_user_by_telegramid("11").uid)