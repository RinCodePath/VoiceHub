import os
import json
import subprocess
import pyaudio
from vosk import Model, KaldiRecognizer
from difflib import SequenceMatcher
import platform
import sys

# Очистка переменных окружения
for env_var in ['PYTHONPATH', 'PYTHONHOME']:
    os.environ.pop(env_var, None)

# ===== КОНФИГУРАЦИЯ =====
CONFIG = {
    'SAMPLE_RATE': 16000,
    'BUFFER_SIZE': 4096,
    'FRAMES_PER_BUFFER': 8192,
    'SIMILARITY_THRESHOLD': 0.8,
}

# Команды и их обработчики
COMMANDS = {
    'браузер': {
        'names': ['браузер откройся', 'открой браузер'],
        'action': 'browser',
        'message': 'Запускаю браузер...'
    },
    'редактор': {
        'names': ['текстовый редактор откройся', 'открой редактор'],
        'action': 'editor',
        'message': 'Запускаю редактор...'
    },
    'игра': {
        'names': ['игра откройся', 'открой стим', 'стим'],
        'action': 'game',
        'message': 'Запускаю Steam...'
    },
    'выключение': {
        'names': ['выключись', 'выключи компьютер', 'пока'],
        'action': 'shutdown',
        'message': 'Выключение системы...'
    },
    'помощь': {
        'names': ['помощь', 'команды', 'что ты умеешь'],
        'action': 'help',
        'message': 'Вот доступные команды:'
    }
}


# ===== ФУНКЦИИ =====

def get_os_type():
    """Определение операционной системы"""
    return platform.system()


def recognize_cmd(user_text, command_template):
    """Гибкое сравнение текста с порогом 80%"""
    return SequenceMatcher(None, user_text, command_template).ratio() > CONFIG['SIMILARITY_THRESHOLD']


def find_command(text):
    """Поиск команды по тексту"""
    for cmd_key, cmd_data in COMMANDS.items():
        for cmd_name in cmd_data['names']:
            if recognize_cmd(text, cmd_name) or cmd_name in text:
                return cmd_data
    return None


def execute_browser(os_type):
    """Запуск браузера"""
    try:
        if os_type == 'Windows':
            subprocess.Popen('explorer "https://google.com"', shell=True)
        elif os_type == 'Darwin':  # macOS
            subprocess.Popen(['open', '-a', 'Safari'])
        else:  # Linux
            subprocess.Popen(['firefox'])
        return True
    except Exception as e:
        print(f"❌ Ошибка запуска браузера: {e}")
        return False


def execute_editor(os_type):
    """Запуск текстового редактора"""
    try:
        if os_type == 'Windows':
            subprocess.Popen('notepad.exe')
        elif os_type == 'Darwin':  # macOS
            subprocess.Popen(['open', '-a', 'TextEdit'])
        else:  # Linux
            subprocess.Popen(['gedit'])
        return True
    except Exception as e:
        print(f"❌ Ошибка запуска редактора: {e}")
        return False


def execute_game(os_type):
    """Запуск Steam"""
    try:
        if os_type == 'Windows':
            steam_paths = [
                r'C:\Program Files (x86)\Steam\Steam.exe',
                r'C:\Program Files\Steam\Steam.exe',
            ]
            for path in steam_paths:
                if os.path.exists(path):
                    subprocess.Popen(path)
                    return True
            print("Steam не найден. Установите Steam.")
            return False
        elif os_type == 'Darwin':  # macOS
            subprocess.Popen(['open', '-a', 'Steam'])
        else:  # Linux
            subprocess.Popen(['steam'])
        return True
    except Exception as e:
        print(f"Ошибка запуска Steam: {e}")
        return False


def execute_shutdown(os_type):
    """Выключение системы"""
    try:
        if os_type == 'Windows':
            os.system('shutdown /s /t 10 /c "Выключение через голосового ассистента"')
        elif os_type == 'Darwin':  # macOS
            os.system('osascript -e "tell application \\"System Events\\" to shut down"')
        else:  # Linux
            os.system('systemctl poweroff')
        return True
    except Exception as e:
        print(f"Ошибка выключения: {e}")
        return False


def show_help():
    """Показать справку по командам"""
    print("\n" + "=" * 50)
    print("ДОСТУПНЫЕ КОМАНДЫ:")
    print("=" * 50)
    for cmd_key, cmd_data in COMMANDS.items():
        print(f"\n🔹 {cmd_data['message'].split('...')[0]}")
        for name in cmd_data['names']:
            print(f"   - '{name}'")
    print("\n" + "=" * 50 + "\n")


def init_vosk():
    """Инициализация Vosk и аудио"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "model")

    if not os.path.exists(model_path):
        print(f"❌ Ошибка: Папка с моделью не найдена: {model_path}")
        print("Скачайте модель Vosk с https://alphacephei.com/vosk/models")
        sys.exit(1)

    try:
        model = Model(model_path)
        rec = KaldiRecognizer(model, CONFIG['SAMPLE_RATE'])

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=CONFIG['SAMPLE_RATE'],
            input=True,
            frames_per_buffer=CONFIG['FRAMES_PER_BUFFER']
        )
        stream.start_stream()

        return model, rec, p, stream
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        print("Подсказка: Проверьте наличие папки 'model' и установку pyaudio")
        sys.exit(1)


def main():
    """Главная функция"""
    os_type = get_os_type()
    print(f"Операционная система: {os_type}")
    print("Голосовой ассистент запущен и слушает...")
    print("Напишите 'помощь' для списка команд. Ctrl+C для выхода.\n")

    model, rec, p, stream = init_vosk()
    show_help()

    action_map = {
        'browser': execute_browser,
        'editor': execute_editor,
        'game': execute_game,
        'shutdown': execute_shutdown,
    }

    try:
        while True:
            try:
                data = stream.read(CONFIG['BUFFER_SIZE'], exception_on_overflow=False)

                if rec.AcceptWaveform(data):
                    result_dict = json.loads(rec.Result())
                    text = result_dict.get("text", "").strip().lower()

                    if text:
                        print(f"\nРаспознано: '{text}'")

                        cmd_data = find_command(text)

                        if cmd_data:
                            print(cmd_data['message'])

                            if cmd_data['action'] == 'help':
                                show_help()
                            elif cmd_data['action'] == 'shutdown':
                                if execute_shutdown(os_type):
                                    break
                            else:
                                action = cmd_data['action']
                                if action in action_map:
                                    action_map[action](os_type)
                        else:
                            print("Команда не распознана. Напишите 'помощь'.")

            except json.JSONDecodeError:
                continue

    except KeyboardInterrupt:
        print("\nЗавершение работы по команде с клавиатуры...")
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Работа завершена.")


if __name__ == "__main__":
    main()
