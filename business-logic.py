# import telegram_botapi
import storage
import pymorphy2
import re

def handle_incoming_message(text, is_keyboard, sender_id): 
    print("TODO")

def split_string(string):
	words = re.split('\W+', string)
	words.remove('')
	return_list = []
	morph = pymorphy2.MorphAnalyzer()
	for i in range(0, len(words)):
		return_list.append(morph.parse(words[i])[0].normal_form)
	return return_list

# Some examples of Storage API usage
print(storage.fetch_questions()[0].answer["type"])

print(storage.fetch_next_question(1))
print(storage.fetch_next_question_onlevel(1))