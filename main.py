# main.py

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
from quotes import quotes

history = []

def load_history():
    global history
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

def save_history():
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(quote):
    history.append(quote)
    save_history()
    update_history_display()

def update_history_display(filtered=None):
    history_listbox.delete(0, tk.END)
    source = filtered if filtered is not None else history
    for q in source:
        history_listbox.insert(tk.END, f'"{q["text"]}" — {q["author"]}')

def generate_quote():
    if not quotes:
        messagebox.showwarning("Ошибка", "Список цитат пуст!")
        return
    quote = random.choice(quotes)
    quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
    add_to_history(quote)

def filter_quotes():
    author = author_entry.get().strip()
    topic = topic_entry.get().strip()
    filtered = [q for q in quotes if (not author or q["author"].lower() == author.lower()) and (not topic or q["topic"].lower() == topic.lower())]
    update_history_display(filtered)

def add_new_quote():
    text = new_quote_text.get("1.0", tk.END).strip()
    author = new_quote_author.get().strip()
    topic = new_quote_topic.get().strip()
    if not text or not author or not topic:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
        return
    quotes.append({"text": text, "author": author, "topic": topic})
    messagebox.showinfo("Успех", "Цитата добавлена!")
    new_quote_text.delete("1.0", tk.END)
    new_quote_author.delete(0, tk.END)
    new_quote_topic.delete(0, tk.END)

# --- Интерфейс ---
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x600")

# Цитата
quote_label = tk.Label(root, text="", wraplength=500, justify="center", font=("Arial", 12))
quote_label.pack(pady=20)
generate_button = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_button.pack()

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)
tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
author_entry = tk.Entry(filter_frame)
author_entry.grid(row=0, column=1)
tk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0)
topic_entry = tk.Entry(filter_frame)
topic_entry.grid(row=1, column=1)
filter_button = tk.Button(filter_frame, text="Фильтровать историю", command=filter_quotes)
filter_button.grid(row=2, columnspan=2, pady=5)

# История
history_label = tk.Label(root, text="История сгенерированных цитат:")
history_label.pack()
history_listbox = tk.Listbox(root, width=70, height=15)
history_listbox.pack(pady=10)
load_history()
update_history_display()

# Добавление новой цитаты
add_frame = tk.Frame(root)
add_frame.pack(pady=20)
tk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0)
new_quote_text = tk.Text(add_frame, height=3, width=50)
new_quote_text.grid(row=0, column=1)
tk.Label(add_frame, text="Автор:").grid(row=1, column=0)
new_quote_author = tk.Entry(add_frame)
new_quote_author.grid(row=1, column=1)
tk.Label(add_frame, text="Тема:").grid(row=2, column=0)
new_quote_topic = tk.Entry(add_frame)
new_quote_topic.grid(row=2, column=1)
add_button = tk.Button(add_frame, text="Добавить цитату", command=add_new_quote)
add_button.grid(row=3, columnspan=2, pady=5)

root.mainloop()