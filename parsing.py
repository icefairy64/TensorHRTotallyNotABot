import pymorphy2
import re
import requests


def split_string(string):
    return_list = []
 
    def add_item_list(parsing_string): # добавляет слово в список
        pos_list = ['PREP', 'CONJ', 'PRCL', 'INTJ'] # список ненужных частей речи
        if parsing_string.tag.POS not in pos_list: # Проверка части речи
            return_list.append(parsing_string.normal_form) 

    # Отправка на обработку опечаток
    dic_typos = correct(string)

    # Cоздание списка из слов строки, без знаков пунктуации
    words = re.split('\W+', string)

    # Формируем выходной список
    
    # Добавляем исправленные опечатки
    for word in words:
        if word in dic_typos: # Если слово есть в списке опечаток
            for typo in (typo.split(' ') for typo in dic_typos[word]): # То записываем исправленные
                if type(typo) == type(str):

                    parsing_word = morph.parse(typo) # Парсим слова
                else: # список, разделили по пробелам
                    for typ in typo:
                        parsing_word = morph.parse(typ) # Парсим слова  
                        add_item_list(parsing_word[0])

                add_item_list(parsing_word[0])
        elif word != '':
            parsing_word = morph.parse(word) # Парсим слово
            add_item_list(parsing_word[0])

    return set(return_list)


def correct(text):
    cor_words = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params={'text' : text})
    dic_cor_words={info['word']: info['s'] for info in cor_words.json() if len(info['s']) > 0}
    return dic_cor_words
    

morph = pymorphy2.MorphAnalyzer()
