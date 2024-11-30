from customtkinter import *
from CTkMessagebox import CTkMessagebox
from cryptography.fernet import Fernet
import os

# Файл для хранения ключа
KEY_FILE = "key.key"

# Файл для хранения зашифрованного кода
CODE_FILE = "code.txt"

# Генерация ключа, если он отсутствует
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

# Создание объекта для шифрования
cipher = Fernet(key)

# Функция для создания и шифрования кода
def create_code():
    code = entry.get()  # Получение кода из поля ввода
    if code:
        encrypted_code = cipher.encrypt(code.encode())  # Шифрование кода
        with open(CODE_FILE, "wb") as code_file:
            code_file.write(encrypted_code)  # Сохранение зашифрованного кода
        CTkMessagebox(title="Успех!", message="Код успешно сохранён!", icon="info")
    else:
        CTkMessagebox(title="Ошибка!", message="Введите код!", icon="warning")

# Функция для проверки (взлома) кода
def guess_code():
    try:
        # Чтение зашифрованного кода из файла
        with open(CODE_FILE, "rb") as code_file:
            encrypted_code = code_file.read()
        # Расшифровка кода
        decrypted_code = cipher.decrypt(encrypted_code).decode()
        
        # Сравнение введённого кода с расшифрованным
        user_code = entry.get()
        if user_code == decrypted_code:
            CTkMessagebox(title="Успех!", message="Вы угадали код!", icon="info")
        else:
            CTkMessagebox(title="Ошибка!", message="Вы не угадали код!", icon="error")
    except FileNotFoundError:
        CTkMessagebox(title="Ошибка!", message="Файл с кодом не найден!", icon="error")
    except Exception as e:
        print(f"Ошибка: {e}")
        CTkMessagebox(title="Ошибка!", message="Не удалось проверить код!", icon="error")

# Настройка окна
root = CTk()
root.title("Взломай код!")
root.geometry("400x300")
root._set_appearance_mode("dark")

# Метка
label = CTkLabel(root, text="Введите код:")
label.pack(pady=10)

# Поле ввода
entry = CTkEntry(root, show="*", width=200, placeholder_text="Введите ваш код здесь")
entry.pack(pady=10)

# Кнопка для создания кода
create_button = CTkButton(root, text="Задать код!", command=create_code)
create_button.pack(pady=10)

# Кнопка для проверки кода
guess_button = CTkButton(root, text="Взломать код!", command=guess_code)
guess_button.pack(pady=10)

# Запуск приложения
root.mainloop()
