# Библиотеки
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

# Функция для центрирования окна
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

# Отрисовка кардиоиды
def cardioid():
    alpha = np.linspace(0, 2 * np.pi, 1000)
    r = 2 * (1 + np.cos(alpha))

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    ax.plot(alpha, r, 'r-', linewidth=2, label='Кардиоида')
    ax.fill(alpha, r, 'r', alpha=0.3)

    plt.show()

# Отрисовка графика лемнискаты Бернулли в полярной системе координат
def lemniscate():
    alpha1 = np.linspace(0, 2 * np.pi, 15000)
    r1 = np.sqrt(2 * np.sin(alpha1 * 2))

    alpha2 = np.linspace(0, 2 * np.pi, 15000)
    r2 = np.sqrt(2 * np.cos(alpha2 * 2))

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    ax.plot(alpha1, r1, 'b--', linewidth=2, label='Лемниската 1', alpha=0.5)
    ax.plot(alpha2, r2, 'r-', linewidth=2, label='Лемниската 2', alpha=0.7)

    plt.show()

# Инициализация контекстного меню
root = Tk()
root.title('Homework 3')
center_window(root, 300, 115)

btn_cardioid = Button(root, text='Кардиоида ', command=cardioid, width=15, height=2)
btn_cardioid.pack(pady=5)

btn_lemniscate = Button(root, text='Лемниската', command=lemniscate, width=15, height=2)
btn_lemniscate.pack(pady=5)

root.mainloop()