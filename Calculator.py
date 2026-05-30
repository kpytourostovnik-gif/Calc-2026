import tkinter as tk
from tkinter import font as tkfont
import math

# 🌑 Окно — как OLED-экран
root = tk.Tk()
root.title("🔮 Calc 2026+")
root.geometry("360x680")  # Увеличили для истории
root.resizable(False, False)
root.configure(bg="#000000")

# Отключаем лишние эффекты
root.option_add("*Button*highlightBackground", "#000000")
root.option_add("*Button*highlightColor", "#000000")
root.option_add("*Button*highlightThickness", "0")

# 🔠 Шрифты — кроссплатформенные
try:
    display_font = tkfont.Font(family="Segoe UI", size=36, weight="bold")
    button_font = tkfont.Font(family="Segoe UI", size=18, weight="normal")
except:
    display_font = tkfont.Font(family="Arial", size=36, weight="bold")
    button_font = tkfont.Font(family="Arial", size=18, weight="bold")

# 🎨 Цвета: тёмная и светлая тема
THEMES = {
    "dark": {
        "bg": "#000000",
        "entry_bg": "#000000",
        "entry_fg": "#FFFFFF",
        "num_color": "#1C1C1E",
        "spec_color": "#3A3A3C",
        "op_color": "#FF2D55",
        "text_color": "#FFFFFF",
        "glow_color": "#444444",
        "press_color": "#0A0A0A",
        "history_fg": "#555555",
        "theme_btn": "☀️"
    },
    "light": {
        "bg": "#F2F2F7",
        "entry_bg": "#F2F2F7",
        "entry_fg": "#000000",
        "num_color": "#E5E5EA",
        "spec_color": "#C7C7CC",
        "op_color": "#FF3B30",
        "text_color": "#000000",
        "glow_color": "#BBBBBB",
        "press_color": "#D1D1D6",
        "history_fg": "#8E8E93",
        "theme_btn": "🌙"
    }
}
current_theme = "dark"

# 🖥️ Фрейм для дисплея и истории
top_frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
top_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=(40, 5), sticky="e")

# 📜 История
history_label = tk.Label(
    top_frame,
    text="",
    font=("Helvetica", 12),
    bg=THEMES[current_theme]["bg"],
    fg=THEMES[current_theme]["history_fg"],
    anchor="e"
)
history_label.pack(fill="x")

# 🖥️ Дисплей
entry = tk.Entry(
    top_frame,
    font=display_font,
    border=0,
    justify="right",
    bg=THEMES[current_theme]["entry_bg"],
    fg=THEMES[current_theme]["entry_fg"],
    insertbackground=THEMES[current_theme]["entry_fg"],
    relief="flat",
    width=12
)
entry.pack()

# ⚙️ Функции
def on_click(value):
    current = entry.get()
    if value == 'C':
        entry.delete(0, tk.END)
        play_click()
    elif value == '±':
        if current and current != '0':
            if current[0] == '-':
                entry.delete(0)
            else:
                entry.insert(0, '-')
        play_click()
    elif value == '=':
        try:
            result = eval(current.replace('×', '*').replace('÷', '/').replace('%', '/100'))
            history_label.config(text=f"{current} =")
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
            play_click()
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(0, "Error")
            play_click()
    else:
        if current == '0' and value in '0123456789':
            entry.delete(0)
        entry.insert(tk.END, value)
        play_click()

# 🔊 Звук клика (без внешних файлов)
def play_click():
    try:
        root.bell()  # Системный звук (работает везде)
    except:
        pass

# 🌓 Переключение темы
def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

def apply_theme():
    theme = THEMES[current_theme]
    root.configure(bg=theme["bg"])
    top_frame.configure(bg=theme["bg"])
    entry.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])
    history_label.configure(bg=theme["bg"], fg=theme["history_fg"])
    theme_button.configure(text=theme["theme_btn"])

    # Обновляем цвета всех кнопок
    for btn_data in buttons:
        text = btn_data[0]
        btn = button_refs[text]
        if text in ['+', '-', '×', '÷', '=']:
            btn.configure(bg=theme["op_color"], fg=theme["text_color"])
        elif text in ['C', '±', '%']:
            btn.configure(bg=theme["spec_color"], fg=theme["text_color"])
        else:
            btn.configure(bg=theme["num_color"], fg=theme["text_color"])

# 🎯 Анимация появления кнопок
def animate_button(btn):
    btn.configure(bg=THEMES[current_theme]["glow_color"])
    root.after(80, lambda: btn.configure(bg=btn.cget("fg") if btn.cget("text") in ['+', '-', '×', '÷', '='] else None))

# 📱 Кнопки: (текст, строка, колонка, тип, colspan)
buttons = [
    ('C',     1, 0, 'spec'), ('±',    1, 1, 'spec'), ('%',    1, 2, 'spec'), ('÷',   1, 3, 'op'),
    ('7',     2, 0, 'num'),  ('8',    2, 1, 'num'),  ('9',    2, 2, 'num'),  ('×',   2, 3, 'op'),
    ('4',     3, 0, 'num'),  ('5',    3, 1, 'num'),  ('6',    3, 2, 'num'),  ('-',   3, 3, 'op'),
    ('1',     4, 0, 'num'),  ('2',    4, 1, 'num'),  ('3',    4, 2, 'num'),  ('+',   4, 3, 'op'),
    ('0',     5, 0, 'num', 2), ('.', 5, 2, 'num'),  ('=',   5, 3, 'op')
]

# 🧠 Копировать результат по клику
def copy_result(e):
    result = entry.get()
    if result not in ["", "Error"]:
        root.clipboard_clear()
        root.clipboard_append(result)
        root.update()
        # Подсказка
        original_text = history_label.cget("text")
        history_label.configure(text="Скопировано!")
        root.after(800, lambda: history_label.configure(text=original_text))

entry.bind("<Button-1>", copy_result)

# 🌟 Эффекты: hover и press
def on_enter(btn):
    def _on_enter(e):
        current_bg = btn.cget("bg")
        if current_bg == THEMES[current_theme]["op_color"]:
            return
        btn.configure(bg=THEMES[current_theme]["glow_color"])
    return _on_enter

def on_leave(btn):
    def _on_leave(e):
        text = btn.cget("text")
        theme = THEMES[current_theme]
        if text in ['+', '-', '×', '÷', '=']:
            btn.configure(bg=theme["op_color"])
        elif text in ['C', '±', '%']:
            btn.configure(bg=theme["spec_color"])
        else:
            btn.configure(bg=theme["num_color"])
    return _on_leave

def on_press(btn):
    def _on_press(e):
        btn.configure(bg=THEMES[current_theme]["press_color"])
    return _on_press

def on_release(btn):
    def _on_release(e):
        root.after(100, lambda: on_leave(btn)(None))
    return _on_release

# ➕ Создание кнопок
button_refs = {}  # Храним ссылки на кнопки

for (text, row, col, btn_type, *extra) in buttons:
    colspan = extra[0] if extra else 1

    # Цвет
    theme = THEMES[current_theme]
    if btn_type == 'op':
        color = theme["op_color"]
    elif btn_type == 'spec':
        color = theme["spec_color"]
    else:
        color = theme["num_color"]

    # Создаём кнопку
    btn = tk.Button(
        root,
        text=text,
        font=button_font,
        bg=color,
        fg=theme["text_color"],
        bd=0,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=10,
        highlightthickness=0
    )

    # Команда
    btn.configure(command=lambda t=text: on_click(t))

    # Расположение
    btn.grid(
        row=row + 1, column=col,  # Сдвиг из-за top_frame
        columnspan=colspan,
        padx=6, pady=6,
        sticky="nsew",
        ipadx=10, ipady=20
    )

    # Сохраняем ссылку
    button_refs[text] = btn

    # Привязка событий
    btn.bind("<Enter>", on_enter(btn))
    btn.bind("<Leave>", on_leave(btn))
    btn.bind("<Button-1>", on_press(btn))
    btn.bind("<ButtonRelease-1>", on_release(btn))

# 🌓 Кнопка смены темы
theme_button = tk.Button(
    root,
    text="☀️",
    font=("Arial", 16),
    bg="#333333",
    fg="white",
    bd=0,
    relief="flat",
    command=toggle_theme,
    cursor="hand2"
)
theme_button.grid(row=6, column=3, padx=10, pady=10, sticky="se")

# 🔲 Растягивание сетки
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

# ▶️ Запуск
# 🧮 Глобальное состояние
scientific_mode = False
button_refs = {}  # Храним ссылки на кнопки

# 🌀 Переключение научного режима
def toggle_scientific():
    global scientific_mode
    scientific_mode = not scientific_mode
    theme = THEMES[current_theme]

    # Удаляем старые кнопки
    for btn in button_refs.values():
        btn.grid_forget()

    # Обновляем сетку
    if scientific_mode:
        root.geometry("360x820")  # Увеличиваем высоту
        theme_button.grid(row=8, column=3, padx=10, pady=10, sticky="se")
    else:
        root.geometry("360x680")
        theme_button.grid(row=6, column=3, padx=10, pady=10, sticky="se")

    # Новые кнопки
    create_buttons()

    # Анимация появления
    for btn in button_refs.values():
        root.after(50, animate_button, btn)

# ➕ Создание кнопок (динамически)
def create_buttons():
    global button_refs
    button_refs = {}

    # Основные кнопки
    base_buttons = [
        ('C',     1, 0, 'spec'), ('±',    1, 1, 'spec'), ('%',    1, 2, 'spec'), ('÷',   1, 3, 'op'),
        ('7',     2, 0, 'num'),  ('8',    2, 1, 'num'),  ('9',    2, 2, 'num'),  ('×',   2, 3, 'op'),
        ('4',     3, 0, 'num'),  ('5',    3, 1, 'num'),  ('6',    3, 2, 'num'),  ('-',   3, 3, 'op'),
        ('1',     4, 0, 'num'),  ('2',    4, 1, 'num'),  ('3',    4, 2, 'num'),  ('+',   4, 3, 'op'),
        ('0',     5, 0, 'num', 2), ('.', 5, 2, 'num'),  ('=',   5, 3, 'op')
    ]

    # Научные кнопки
    sci_buttons = [
        ('sin',   1, 4, 'spec'), ('cos',  2, 4, 'spec'), ('tan',  3, 4, 'spec'), ('√',   4, 4, 'op'),
        ('x²',    1, 5, 'spec'), ('(',    2, 5, 'spec'), (')',    3, 5, 'spec'), ('^',   5, 4, 'op'),
        ('log',   1, 6, 'spec'), ('ln',   2, 6, 'spec'), ('π',    3, 6, 'num'),  ('e',   4, 6, 'num'),
        ('1/x',   5, 5, 'spec'), ('exp',  4, 5, 'spec')
    ]

    # Выбираем кнопки
    buttons = base_buttons + (sci_buttons if scientific_mode else [])

    for (text, row, col, btn_type, *extra) in buttons:
        colspan = extra[0] if extra else 1
        theme = THEMES[current_theme]

        if btn_type == 'op':
            color = theme["op_color"]
        elif btn_type == 'spec':
            color = theme["spec_color"]
        else:
            color = theme["num_color"]

        btn = tk.Button(
            root,
            text=text,
            font=button_font,
            bg=color,
            fg=theme["text_color"],
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=10,
            highlightthickness=0
        )

        btn.configure(command=lambda t=text: on_click_sci(t))
        btn.grid(row=row + 1, column=col, columnspan=colspan, padx=6, pady=6, sticky="nsew", ipadx=10, ipady=20)
        button_refs[text] = btn

        btn.bind("<Enter>", on_enter(btn))
        btn.bind("<Leave>", on_leave(btn))
        btn.bind("<Button-1>", on_press(btn))
        btn.bind("<ButtonRelease-1>", on_release(btn))

    # Кнопка научного режима
    sci_btn = tk.Button(
        root,
        text="Sci",
        font=("Arial", 12),
        bg=theme["spec_color"],
        fg=theme["text_color"],
        bd=0,
        relief="flat",
        cursor="hand2",
        command=toggle_scientific
    )
    sci_btn.grid(row=6 if not scientific_mode else 5, column=5, padx=6, pady=6, sticky="nsew")
    button_refs["Sci"] = sci_btn
    sci_btn.bind("<Enter>", on_enter(sci_btn))
    sci_btn.bind("<Leave>", on_leave(sci_btn))

# ⚙️ Расширенная функция клика
def on_click_sci(value):
    current = entry.get()
    try:
        if value == 'sin':
            result = math.sin(math.radians(float(current)))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'cos':
            result = math.cos(math.radians(float(current)))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'tan':
            result = math.tan(math.radians(float(current)))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == '√':
            result = math.sqrt(float(current))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'x²':
            result = float(current) ** 2
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == '1/x':
            result = 1 / float(current)
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'log':
            result = math.log10(float(current))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'ln':
            result = math.log(float(current))
            entry.delete(0, tk.END)
            entry.insert(0, f"{result:g}")
        elif value == 'π':
            entry.insert(tk.END, str(round(math.pi, 10)))
        elif value == 'e':
            entry.insert(tk.END, str(round(math.e, 10)))
        elif value == '^':
            entry.insert(tk.END, '**')
        else:
            on_click(value)  # Стандартные операции
        play_click()
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        play_click()

# 🌟 Эффекты остаются те же
def on_enter(btn):
    def _on_enter(e):
        current_bg = btn.cget("bg")
        theme = THEMES[current_theme]
        if current_bg == theme["op_color"]:
            return
        btn.configure(bg=theme["glow_color"])
    return _on_enter

def on_leave(btn):
    def _on_leave(e):
        text = btn.cget("text")
        theme = THEMES[current_theme]
        if text in ['+', '-', '×', '÷', '=', '^']:
            btn.configure(bg=theme["op_color"])
        elif text in ['C', '±', '%', 'Sci', '(', ')', 'exp', '1/x']:
            btn.configure(bg=theme["spec_color"])
        else:
            btn.configure(bg=theme["num_color"])
    return _on_leave

def on_press(btn):
    def _on_press(e):
        btn.configure(bg=THEMES[current_theme]["press_color"])
    return _on_press

def on_release(btn):
    def _on_release(e):
        root.after(100, lambda: on_leave(btn)(None))
    return _on_release

# 🎯 Анимация появления кнопок
def animate_button(btn):
    btn.configure(bg=THEMES[current_theme]["glow_color"])
    root.after(80, lambda: btn.configure(bg=btn.cget("fg") if btn.cget("text") in ['+', '-', '×', '÷', '='] else None))

# 🔲 Растягивание сетки
for i in range(7):  # 7 колонок для научных кнопок
    root.grid_columnconfigure(i, weight=1)
for i in range(10):
    root.grid_rowconfigure(i, weight=1)

# ▶️ Запуск
if __name__ == "__main__":
    create_buttons()  # Создаём кнопки
    root.mainloop()
if __name__ == "__main__":
    # Анимация появления
    for btn in button_refs.values():
        root.after(50, animate_button, btn)
    root.mainloop()