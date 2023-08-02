import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
import keyboard
import pyperclip



#Словник
COUNTRY_NAMES = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Mordor (ru)",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu",
}
language_names = list(COUNTRY_NAMES.values())


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translator")
        self.root.configure(bg="gray")

        # Neon стиль
        self.neon_style = ttk.Style()
        self.neon_style.theme_use('clam')
        self.neon_style.configure('.', background='gray', foreground='purple')
        self.neon_style.map('.', foreground=[('disabled', 'gray')])

        self.source_language = "English"
        self.target_language = "Ukrainian"

        self.translator = Translator()

        self.create_language_selector()

        self.source_text_label = ttk.Label(root, text="Текст для перекладу:", foreground="purple", background="gray")
        self.source_text_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.source_text_entry = tk.Text(root, width=70, height=8, font=("Arial", 12), wrap=tk.WORD, bg="black", fg="white", insertbackground="purple")
        self.source_text_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.translated_text_label = ttk.Label(root, text="Переклад:", foreground="purple", background="gray")
        self.translated_text_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.translated_text_entry = tk.Text(root, width=70, height=8, font=("Arial", 12), wrap=tk.WORD, state="disabled", bg="black", fg="white")
        self.translated_text_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.last_translation_time = 0
        self.delayed_callback_id = None
        self.source_text_entry.bind("<KeyRelease>", self.on_key_release)

        # Додаємо можливість швидкого друку через комбінації клавіш
        keyboard.add_hotkey("ctrl+a", self.select_all)
        keyboard.add_hotkey("ctrl+c", self.copy_text)
        keyboard.add_hotkey("ctrl+v", self.paste_text)
        keyboard.add_hotkey("ctrl+backspace", self.delete_word)
        keyboard.add_hotkey("ctrl+z", self.undo_delete)
        keyboard.add_hotkey("ctrl+shift+z", self.redo_delete)

        self.text_states = []
        self.undo_states = []  
        self.source_text_entry.bind("<Delete>", self.save_state)
        self.source_text_entry.bind("<BackSpace>", self.save_state)

         # Оголошуємо змінну language_codes тут
        self.language_codes = list(COUNTRY_NAMES.keys())

        self.create_language_selector()


    def create_language_selector(self):
        language_names = list(COUNTRY_NAMES.values())
        language_codes = list(COUNTRY_NAMES.keys())

        self.source_language_var = tk.StringVar(value=self.source_language)
        self.target_language_var = tk.StringVar(value=self.target_language)

        self.source_language_label = ttk.Label(root, text="З мови:", foreground="purple", background="gray")
        self.source_language_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.source_language_selector = ttk.Combobox(root, values=language_names, textvariable=self.source_language_var,  state="readonly")
        self.source_language_selector.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.source_language_selector.bind("<<ComboboxSelected>>", self.set_source_language)

        self.target_language_label = ttk.Label(root, text="На мову:", foreground="purple", background="gray")
        self.target_language_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.target_language_selector = ttk.Combobox(root, values=language_names, textvariable=self.target_language_var, state="readonly")
        self.target_language_selector.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.target_language_selector.bind("<<ComboboxSelected>>", self.set_target_language)

    def set_source_language(self, event):
        selected_language_name = self.source_language_selector.get()
        self.source_language = self.language_codes[language_names.index(selected_language_name)]  # Замінюємо language_codes на self.language_codes

    def set_target_language(self, event):
        selected_language_name = self.target_language_selector.get()
        self.target_language = self.language_codes[language_names.index(selected_language_name)]
        self.translate_text() 

    def on_key_release(self, event):
        if self.delayed_callback_id is not None:
            self.root.after_cancel(self.delayed_callback_id)
        self.delayed_callback_id = self.root.after(1000, self.translate_text)

    def translate_text(self):
        text_to_translate = self.source_text_entry.get("1.0", tk.END).strip()
        if not text_to_translate:
            self.translated_text_entry.config(state="normal")
            self.translated_text_entry.delete("1.0", tk.END)
            self.translated_text_entry.config(state="disabled")
            return

        try:
            translated_text = self.translator.translate(text_to_translate, src=self.source_language, dest=self.target_language)
            self.translated_text_entry.config(state="normal")
            self.translated_text_entry.delete("1.0", tk.END)
            self.translated_text_entry.insert("1.0", translated_text.text)
            self.translated_text_entry.config(state="disabled")
        except Exception as e:
            print("Помилка перекладу:", e)

    def select_all(self):
        self.source_text_entry.tag_add("sel", "1.0", tk.END)
        return False

    def copy_text(self):
        selected_text = self.source_text_entry.selection_get()
        if selected_text:
            self.source_text_entry.clipboard_clear()
            self.source_text_entry.clipboard_append(selected_text)
        return False

    def paste_text(self):
        try:
            text = self.source_text_entry.clipboard_get()
            self.source_text_entry.insert(tk.INSERT, text)
        except tk.TclError:
            pass
        return False

    def delete_word(self):
        text = self.source_text_entry.get("1.0", tk.END)
        words = text.split()
        if len(words) >= 1:
            last_word = words[-1]
            start = text.rfind(last_word)
            end = start + len(last_word)
            self.source_text_entry.delete(f"{1}.{start}", f"{1}.{end}")

    def save_state(self, event):
        text_state = self.source_text_entry.get("1.0", tk.END)
        self.text_states.append(text_state)
        return False

    def undo_delete(self):
        if self.text_states:
            previous_state = self.text_states.pop()
            self.undo_states.append(self.source_text_entry.get("1.0", tk.END))  # Змінюємо redo_states на undo_states
            self.source_text_entry.delete("1.0", tk.END)
            self.source_text_entry.insert("1.0", previous_state)
        return False

    def redo_delete(self):
        if self.undo_states:  # Змінюємо redo_states на undo_states
            next_state = self.undo_states.pop()  # Змінюємо redo_states на undo_states
            self.text_states.append(self.source_text_entry.get("1.0", tk.END))
            self.source_text_entry.delete("1.0", tk.END)
            self.source_text_entry.insert("1.0", next_state)
        return False


if __name__ == "__main__":
    root = tk.Tk()

    # Neon стиль для Entry і Combobox
    root.style = ttk.Style()
    root.style.theme_use('clam')
    root.style.configure("Neon.TEntry", foreground="white", fieldbackground="black", bordercolor="purple")
    root.style.map("Neon.TEntry", foreground=[('disabled', 'black')])

    root.style.configure("Neon.TCombobox", foreground="white", selectbackground="purple", fieldbackground="black", bordercolor="purple")

    app = TranslatorApp(root)
    root.mainloop()
