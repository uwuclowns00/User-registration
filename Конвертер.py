import tkinter as tk
from tkinter import messagebox
import sqlite3


# Создаем базу данных и таблицу пользователей, если она еще не существует
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Функция для регистрации пользователя
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Регистрация", "Регистрация прошла успешно!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    finally:
        conn.close()


# Функция для авторизации пользователя
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Авторизация", "Авторизация прошла успешно!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")


# Окно регистрации
def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")

    tk.Label(registration_window, text="Логин").grid(row=0, column=0)
    tk.Label(registration_window, text="Пароль").grid(row=1, column=0)

    username_entry = tk.Entry(registration_window)
    password_entry = tk.Entry(registration_window, show='*')

    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    tk.Button(registration_window, text="Зарегистрироваться",
              command=lambda: register_user(username_entry.get(), password_entry.get())).grid(row=2, columnspan=2)


# Основное окно авторизации
root = tk.Tk()
root.title("Авторизация")

tk.Label(root, text="Логин").grid(row=0, column=0)
tk.Label(root, text="Пароль").grid(row=1, column=0)

username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show='*')

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

tk.Button(root, text="Войти",
          command=lambda: login_user(username_entry.get(), password_entry.get())).grid(row=2, columnspan=2)

tk.Button(root, text="Регистрация",
          command=open_registration_window).grid(row=3, columnspan=2)

create_database()  # Создаем базу данных при запуске приложения
root.mainloop()

