import os
import json
import sys
import threading
import tkinter as tk
from tkinter import ttk

for env_var in ['PYTHONPATH', 'PYTHONHOME']:
    os.environ.pop(env_var, None)

from src.config import CONFIG
from src.strings import STRINGS, CURRENT_LANG
from src.utils import get_os_type
from src.commands import find_command
from src.recognizer import init_vosk
from src.executor import execute_browser, execute_editor, execute_game, execute_shutdown

def show_fatal_error_gui(error_text):
    """Окно критической ошибки при старте Vosk (если нет папки модели)"""
    root = tk.Tk()
    root.title("VoiceHub - Ошибка Запуска")
    root.geometry("460x360")
    root.configure(bg="#1e1e2e")
    root.resizable(False, False)

    title_label = tk.Label(
        root, text="⚠️ КРИТИЧЕСКАЯ ОШИБКА",
        fg="#f38ba8", bg="#1e1e2e", font=("Arial", 14, "bold")
    )
    title_label.pack(pady=15)

    msg_frame = tk.Frame(root, bg="#252538", bd=1, relief="solid")
    msg_frame.pack(fill="both", expand=True, padx=20, pady=5)

    error_details = tk.Label(
        msg_frame, text=error_text,
        fg="#cdd6f4", bg="#252538", font=("Arial", 10),
        wraplength=380, justify="left"
    )
    error_details.pack(padx=15, pady=15, anchor="w")

    close_btn = ttk.Button(root, text="Закрыть / Exit", command=root.destroy)
    close_btn.pack(pady=15)
    root.mainloop()


class VoiceAssistantApp:
    def __init__(self, root, model, rec, p, stream):
        self.root = root
        self.os_type = get_os_type()
        
        self.model = model
        self.rec = rec
        self.p = p
        self.stream = stream
        self.running = True
        
        # Настройка главного окна
        self.root.title("VoiceHub")
        self.root.geometry("450x320")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "TButton", font=("Arial", 10, "bold"),
            background="#313244", foreground="#cdd6f4", borderwidth=0, focuscolor="none"
        )
        self.style.map("TButton", background=[("active", "#45475a")])
        
        # Основной статус приложения
        self.status_label = tk.Label(
            root, text=STRINGS['startup_msg'], 
            fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 10, "bold"),
            wraplength=410, justify="center"
        )
        self.status_label.pack(pady=20, padx=15)
        
        self.info_frame = tk.Frame(root, bg="#252538", bd=0)
        self.info_frame.pack(fill="x", padx=20, pady=5)
        
        self.lang_label = tk.Label(
            self.info_frame, text=f"{STRINGS['lang_info']} {CURRENT_LANG.upper()}", 
            fg="#a6e3a1", bg="#252538", font=("Arial", 10, "bold")
        )
        self.lang_label.pack(side="left", padx=15, pady=8)
        
        self.os_label = tk.Label(
            self.info_frame, text=f"OS: {self.os_type}", 
            fg="#89b4fa", bg="#252538", font=("Arial", 10, "bold")
        )
        self.os_label.pack(side="right", padx=15, pady=8)
        
        self.help_button = ttk.Button(
            root, text=STRINGS['press_help'].strip(), style="TButton", command=self.show_gui_help
        )
        self.help_button.pack(pady=15, padx=15)
        
        # Поле распознанного текста / Подсказок
        self.text_label = tk.Label(
            root, text="...", 
            fg="#b4befe", bg="#1e1e2e", font=("Arial", 11, "italic"),
            wraplength=400, justify="center"
        )
        self.text_label.pack(pady=15, padx=15)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.listen_thread = threading.Thread(target=self.voice_listening_loop, daemon=True)
        self.listen_thread.start()

    def show_gui_help(self):
        from src.commands import COMMANDS
        help_window = tk.Toplevel(self.root)
        help_window.title(STRINGS['available_commands'])
        help_window.geometry("420x450")
        help_window.configure(bg="#181825")
        help_window.resizable(False, False)
        
        title = tk.Label(help_window, text=STRINGS['available_commands'], fg="#f5c2e7", bg="#181825", font=("Arial", 12, "bold"))
        title.pack(pady=15)
        
        container = tk.Frame(help_window, bg="#181825")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container, bg="#181825", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#181825")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))
        
        def _on_mousewheel(event):
            if event.delta:
                if sys.platform == 'darwin': canvas.yview_scroll(int(-1 * (event.delta)), "units")
                else: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        if sys.platform.startswith('linux'):
            help_window.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            help_window.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        else:
            help_window.bind("<MouseWheel>", _on_mousewheel)

        for cmd_key, cmd_data in COMMANDS.items():
            cmd_frame = tk.Frame(scrollable_frame, bg="#1e1e2e", bd=1, relief="flat")
            cmd_frame.pack(fill="x", padx=5, pady=6, ipady=6)
            lbl_action = tk.Label(cmd_frame, text=f"• {cmd_key.upper()}", fg="#89b4fa", bg="#1e1e2e", font=("Arial", 10, "bold"))
            lbl_action.pack(anchor="w", padx=15, pady=2)
            phrases = ", ".join([f"«{name}»" for name in cmd_data['names']])
            lbl_phrases = tk.Label(cmd_frame, text=phrases, fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 10), wraplength=340, justify="left")
            lbl_phrases.pack(anchor="w", padx=15, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_status(self, text, fg_color="#cdd6f4"):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=fg_color))

    def update_recognized_text(self, text, fg_color="#b4befe", font_style=("Arial", 11, "italic")):
        self.root.after(0, lambda: self.text_label.config(text=text, fg=fg_color, font=font_style))

    def change_language_logic(self):
        new_lang = 'en' if CURRENT_LANG == 'ru' else 'ru'

        if new_lang == 'en' and not os.path.exists('model/en'):
            self.update_status("Ошибка: папка 'model/en' не найдена!", "#f38ba8")
            self.update_recognized_text("Скачайте английскую модель Vosk", fg_color="#f5a97f",
                                        font_style=("Arial", 10, "bold"))
            return

        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except Exception:
            config_data = CONFIG

        config_data['language'] = new_lang
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

        self.update_status("Перезапуск / Restarting...", "#fab387")
        self.root.after(1000, self.hard_restart)

    def hard_restart(self):
        self.cleanup_audio()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def cleanup_audio(self):
        self.running = False
        try:
            if self.stream: self.stream.stop_stream(); self.stream.close()
            if self.p: self.p.terminate()
        except: pass

    def on_closing(self):
        self.cleanup_audio()
        self.root.destroy()

    def voice_listening_loop(self):
        while self.running:
            try:
                data = self.stream.read(CONFIG['buffer_size'], exception_on_overflow=False)
                if self.rec.AcceptWaveform(data):
                    result_dict = json.loads(self.rec.Result())
                    text = result_dict.get("text", "").strip().lower()

                    if text:
                        # Показываем, что ассистент услышал команду
                        self.update_recognized_text(f"«{text}»", fg_color="#b4befe", font_style=("Arial", 11, "italic"))
                        cmd_data = find_command(text)

                        if cmd_data:
                            action = cmd_data['action']
                            
                            if action == 'help':
                                self.root.after(0, self.show_gui_help)
                            elif action == 'shutdown':
                                if execute_shutdown(self.os_type):
                                    self.root.after(0, self.on_closing); break
                            elif action == 'change_lang':
                                self.change_language_logic(); break
                            else:
                                try:
                                    if action == 'browser': execute_browser(self.os_type)
                                    elif action == 'editor': execute_editor(self.os_type)
                                    elif action == 'game': execute_game(self.os_type)
                                    
                                    # Если всё запустилось — пишем зелёным цветом статус
                                    self.update_status(cmd_data['message'], "#a6e3a1")
                                except Exception as cmd_error:
                                    # Извлекаем чистую строку ошибки без лишних скобок
                                    clean_err = str(cmd_error).split('\n')[0]
                                    
                                    # Пишем ошибку КРАСНЫМ прямо в основное окно
                                    self.update_status(f"❌ {clean_err}", "#f38ba8")
                                    # В нижнее поле выводим подсказку
                                    self.update_recognized_text("Пожалуйста, исправьте config.json", fg_color="#f5a97f", font_style=("Arial", 10, "bold"))
                        else:
                            self.update_status(STRINGS['unknown_cmd'], "#f38ba8")
            except Exception as e:
                if not self.running: break
                continue

def main():
    model, rec, p, result = init_vosk()
    if model is None:
        show_fatal_error_gui(result)
        sys.exit(1)
    root = tk.Tk()
    app = VoiceAssistantApp(root, model, rec, p, result)
    root.mainloop()

if __name__ == "__main__":
    main()
