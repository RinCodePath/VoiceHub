import os
import json
from src.strings import STRINGS, CURRENT_LANG

# Базовые команды по умолчанию
COMMANDS = {
    'browser': {
        'names': ['браузер', 'интернет', 'открой браузер', 'browser', 'open browser', 'google', 'гугл'],
        'message': 'Открываю браузер...',
        'action': 'browser'
    },
    'editor': {
        'names': ['редактор', 'блокнот', 'текст', 'открой блокнот', 'editor', 'notepad'],
        'message': 'Запускаю текстовый редактор...',
        'action': 'editor'
    },
    'game': {
        'names': ['стим', 'игра', 'игру', 'запусти стим', 'steam', 'game'],
        'message': 'Запускаю Steam / Игру...',
        'action': 'game'
    },
    'help': {
        'names': ['помощь', 'справка', 'команды', 'что ты умеешь', 'help'],
        'message': 'Открываю окно справки...',
        'action': 'help'
    },
    'change_lang': {
        'names': ['смени язык', 'поменяй язык', 'change language', 'switch language'],
        'message': 'Смена языка / Changing language...',
        'action': 'change_lang'
    },
    'shutdown': {
        'names': ['выключи компьютер', 'выключить комп', 'выключение', 'shutdown'],
        'message': 'Выключаю систему...',
        'action': 'shutdown'
    }
}

def find_command(text):
    text = text.lower().strip()
    for cmd_id, cmd_data in COMMANDS.items():
        for name in cmd_data['names']:
            if name in text:  # Проверка на вхождение слова
                return cmd_data
    return None
