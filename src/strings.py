from src.config import CONFIG

LANGUAGES = {
    'ru': {
        'browser': {'names': ['браузер откройся', 'открой браузер', 'веб браузер'], 'action': 'browser', 'message': 'Запускаю браузер...'},
        'editor': {'names': ['текстовый редактор откройся', 'открой редактор', 'редактор'], 'action': 'editor', 'message': 'Запускаю редактор...'},
        'game': {'names': ['игра откройся', 'открой стим', 'стим', 'steam'], 'action': 'game', 'message': 'Запускаю Steam...'},
        'shutdown': {'names': ['выключись', 'выключи компьютер', 'пока', 'спи'], 'action': 'shutdown', 'message': 'Выключение системы...'},
        'help': {'names': ['помощь', 'команды', 'что ты умеешь', 'справка'], 'action': 'help', 'message': 'Вот доступные команды:'},
        # НОВАЯ КОМАНДА:
        'change_lang': {'names': ['смени язык', 'поменяй язык', 'english', 'инглиш', 'switch language'], 'action': 'change_lang', 'message': 'Переключаю язык на английский...'},
        
        'startup_msg': 'Голосовой ассистент запущен и слушает...',
        'unknown_cmd': 'Команда не распознана. Напишите "помощь".',
        'recognized': 'Распознано:',
        'press_help': 'Напишите "помощь" для списка команд. Ctrl+C для выхода.\n',
        'available_commands': 'ДОСТУПНЫЕ КОМАНДЫ:',
        'shutdown_confirm': 'Выключение через {timeout} секунд. Отмена: Ctrl+C',
        'error_browser': 'ERROR: Ошибка запуска браузера:',
        'error_editor': 'ERROR: Ошибка запуска редактора:',
        'error_steam': 'ERROR: Ошибка запуска Steam:',
        'steam_not_found': 'ERROR: Steam не найден. Установите Steam.',
        'error_shutdown': 'ERROR: Ошибка выключения:',
        'error_init': 'ERROR: Ошибка инициализации:',
        'model_not_found': 'ERROR: Папка с моделью не найдена:',
        'download_model': 'INFO: Скачайте модель Vosk с https://alphacephei.com/vosk/models',
        'check_setup': 'INFO: Проверьте наличие папки "model" и установку pyaudio',
        'keyboard_interrupt': 'Завершение работы по команде с клавиатуры...',
        'unexpected_error': 'ERROR: Непредвиденная ошибка:',
        'finished': 'OK: Работа завершена.',
        'os_type': 'Операционная система:',
        'editor_config': 'Текстовый редактор из config.json:',
        'lang_info': 'Язык:',
    },
    'en': {
        'browser': {'names': ['browser', 'open browser', 'web browser'], 'action': 'browser', 'message': 'Launching browser...'},
        'editor': {'names': ['text editor', 'open editor', 'editor'], 'action': 'editor', 'message': 'Launching text editor...'},
        'game': {'names': ['game', 'open steam', 'steam'], 'action': 'game', 'message': 'Launching Steam...'},
        'shutdown': {'names': ['shutdown', 'turn off', 'bye', 'goodbye'], 'action': 'shutdown', 'message': 'System shutdown...'},
        'help': {'names': ['help', 'commands', 'what can you do', 'info'], 'action': 'help', 'message': 'Available commands:'},
        # NEW COMMAND:
        'change_lang': {'names': ['change language', 'switch language', 'russian', 'русский'], 'action': 'change_lang', 'message': 'Switching language to Russian...'},
        
        'startup_msg': 'Voice assistant is running and listening...',
        'unknown_cmd': 'Command not recognized. Type "help".',
        'recognized': 'Recognized:',
        'press_help': 'Type "help" for command list. Ctrl+C to exit.\n',
        'available_commands': 'AVAILABLE COMMANDS:',
        'shutdown_confirm': 'Shutdown in {timeout} seconds. Cancel: Ctrl+C',
        'error_browser': 'ERROR: Error launching browser:',
        'error_editor': 'ERROR: Error launching editor:',
        'error_steam': 'ERROR: Error launching Steam:',
        'steam_not_found': 'ERROR: Steam not found. Please install Steam.',
        'error_shutdown': 'ERROR: Shutdown error:',
        'error_init': 'ERROR: Initialization error:',
        'model_not_found': 'ERROR: Model folder not found:',
        'download_model': 'INFO: Download Vosk model from https://alphacephei.com/vosk/models',
        'check_setup': 'INFO: Check "model" folder exists and pyaudio is installed',
        'keyboard_interrupt': 'Interrupted by user...',
        'unexpected_error': 'ERROR: Unexpected error:',
        'finished': 'OK: Work completed.',
        'os_type': 'Operating System:',
        'editor_config': 'Text editor from config.json:',
        'lang_info': 'Language:',
    }
}

CURRENT_LANG = CONFIG.get('language', 'ru')
if CURRENT_LANG not in LANGUAGES:
    print(f"WARN: Неизвестный язык '{CURRENT_LANG}'. Используется русский.")
    CURRENT_LANG = 'ru'

STRINGS = LANGUAGES[CURRENT_LANG]
