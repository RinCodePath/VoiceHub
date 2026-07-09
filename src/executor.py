import subprocess
import json
import os
import shutil
from src.config import CONFIG

def get_config_value(key, default):
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, default)
    except:
        return default

def execute_browser(os_type):
    browser_cfg = get_config_value('browser', 'default').strip().lower()
    url = "https://google.com"
    
    try:
        if os_type == 'windows':
            if browser_cfg == 'default':
                subprocess.Popen(['cmd', '/c', 'start', url])
            else:
                subprocess.Popen(['cmd', '/c', 'start', browser_cfg, url])
        elif os_type == 'mac':
            if browser_cfg == 'default':
                subprocess.Popen(['open', url])
            else:
                subprocess.Popen(['open', '-a', browser_cfg, url])
        else:  # Linux
            if browser_cfg == 'default':
                if shutil.which('xdg-open'):
                    subprocess.Popen(['xdg-open', url])
                elif shutil.which('firefox'):
                    subprocess.Popen(['firefox', url])
                else:
                    raise RuntimeError("Не найдены xdg-open или firefox")
            else:
                subprocess.Popen([browser_cfg, url])
    except Exception as e:
        display_name = "Системный (default)" if browser_cfg == 'default' else browser_cfg
        raise RuntimeError(f"Не удалось открыть браузер '{display_name}'.\nОшибка: {e}")

def execute_editor(os_type):
    editor = get_config_value('editor', 'pycharm').strip().lower()
    
    try:
        if editor == 'pycharm':
            if os_type == 'windows':
                # Пытаемся вызвать pycharm через команду из PATH или стандартный лаунчер
                subprocess.Popen(['pycharm'])
            elif os_type == 'mac':
                subprocess.Popen(['open', '-a', 'PyCharm'])
            else:  # Linux (Arch Linux)
                # На Arch Linux имя бинарника зависит от типа пакета в pacman/AUR/snap/flatpak:
                # 1. pycharm-community (самый частый вариант из официальных репозиториев Arch)
                # 2. pycharm-professional
                # 3. pycharm (просто pycharm)
                if shutil.which('pycharm-community'):
                    subprocess.Popen(['pycharm-community'])
                elif shutil.which('pycharm-professional'):
                    subprocess.Popen(['pycharm-professional'])
                elif shutil.which('pycharm'):
                    subprocess.Popen(['pycharm'])
                else:
                    raise RuntimeError("Команда pycharm не найдена в вашей системе. Проверьте, установлен ли он.")
        else:
            # Если в конфиге указано что-то другое вручную
            if os_type == 'windows':
                subprocess.Popen([editor])
            elif os_type == 'mac':
                subprocess.Popen(['open', '-a', editor])
            else:
                subprocess.Popen([editor])
    except Exception as e:
        raise RuntimeError(f"Не удалось открыть редактор '{editor}'.\nОшибка: {e}")

def execute_game(os_type):
    game = get_config_value('game', '')
    if not game:
        raise RuntimeError("Путь к игре не указан в файле config.json (поле 'game')")
    try:
        subprocess.Popen([game])
    except Exception as e:
        raise RuntimeError(f"Не удалось запустить игру по пути '{game}'.\nОшибка: {e}")

def execute_shutdown(os_type):
    try:
        if os_type == 'windows':
            subprocess.Popen(['shutdown', '/s', '/t', '60'])
        elif os_type == 'mac':
            subprocess.Popen(['osascript', '-e', 'tell app "System Events" to shut down'])
        else:
            subprocess.Popen(['shutdown', '+1'])
        return True
    except Exception as e:
        raise RuntimeError(f"Не удалось выполнить команду выключения.\nОшибка: {e}")
