import json

def get_lang_content():
    with open('app/I18n/th.json', 'r', encoding='utf-8') as th_file:
        th_data = json.load(th_file)
    return th_data