import os
import json


def load_config():
    """Загрузка конфигурации из config.json"""
    # config.json лежит в корне проекта (на уровень выше, чем этот файл)
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

    default_config = {
        'language': 'ru',
        'sample_rate': 16000,
        'buffer_size': 4096,
        'frames_per_buffer': 8192,
        'similarity_threshold': 0.8,
        'text_editor': 'notepad',
        'browser': 'default',
        'shutdown_timeout': 10
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
        except Exception as e:
            print(f"WARN: Ошибка при загрузке config.json: {e}")
            print("Использую настройки по умолчанию.\n")
    else:
        print("WARN: config.json не найден. Создаю с настройками по умолчанию...")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print("OK: config.json создан.\n")
        except Exception as e:
            print(f"WARN: Не удалось создать config.json: {e}\n")

    return default_config


CONFIG = load_config()