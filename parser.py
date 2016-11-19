import pymorphy2
import re


def split_string(string):
    # Отправка на обработку опечаток
    dic_typos = correct(string)

    # Создание списка из слов строки, без знаков пунктуации
    words = re.split('\W+', string)

    # Формируем выходной список
    return_list = []
    
    # Добавляем исправленные опечатки
    for word in words:
        if word in dic_typos:
            for typo in dic_typos[word]:
                return_list.append(morph.parse(typo)[0].normal_form)
        elif word != '':
            return_list.append(morph.parse(word)[0].normal_form)

    return set(return_list)

def correct(string):
    return {'роботать': ['работать'], 'опичатка': ['опечатка', 'печатка']}
    

morph = pymorphy2.MorphAnalyzer()
print(split_string('Здравствуйте! Меня зовут Петя. Я бы хотел роботать в вашей компании программистом. Тут опичатка'))
