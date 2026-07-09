import os
import sys
import pyaudio
from vosk import Model, KaldiRecognizer
from src.config import CONFIG
from src.strings import STRINGS, CURRENT_LANG

def init_vosk():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "model", CURRENT_LANG)

    if not os.path.exists(model_path) or not os.listdir(model_path):
        # Возвращаем кортеж с ошибкой вместо жесткого падения
        error_msg = f"{STRINGS['model_not_found']}\n{model_path}\n\nПожалуйста, скачайте модель для {CURRENT_LANG.upper()} и распакуйте её туда."
        return None, None, None, error_msg

    try:
        model = Model(model_path)
        rec = KaldiRecognizer(model, CONFIG['sample_rate'])
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=CONFIG['sample_rate'],
            input=True,
            frames_per_buffer=CONFIG['frames_per_buffer']
        )
        stream.start_stream()
        return model, rec, p, stream
    except Exception as e:
        error_msg = f"Ошибка аудио-подсистемы:\n{e}\n\nПроверьте микрофон или настройки частоты дискретизации."
        return None, None, None, error_msg
