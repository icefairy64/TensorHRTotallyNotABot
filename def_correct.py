import requests



def correct(text):
    cor_words = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params={'text' : text})
    print(cor_words.json())
    dic_cor_words={info['word']: info['s'] for info in cor_words.json() if len(info['s']) > 0}
    return dic_cor_words
    
