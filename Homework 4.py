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

def func_1():
    alpha = np.linspace(0, 2 * np.pi, 1000)
    r = 4 * np.cos(alpha)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    ax.plot(alpha, r, 'r-', linewidth=2, label='Функция 1')

    plt.show()

def func_2():
    alpha = np.array([np.pi / 3, 4 * np.pi / 3])
    r = np.linspace(0, 10, 100)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
    for t in alpha:
        ax.plot([t] * len(r), r, 'r', label='Функция 2')
    plt.show()

def func_3():
    x = np.arange(-100, 2, 0.01)
    y = np.sqrt(16 - 8 * x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'r-', linewidth=2, label='Функция 3')

    ax.set_xlabel('Ось X')
    ax.set_ylabel('Ось Y')
    ax.legend()
    ax.grid(True)

    plt.show()

root = Tk()
root.title('Homework 4')
center_window(root, 300, 160)

btn_func1 = Button(root, text='Функция 1', command=func_1, width=15, height=2)
btn_func1.pack(pady=5)

btn_func2 = Button(root, text='Функция 2', command=func_2, width=15, height=2)
btn_func2.pack(pady=5)

btn_func3 = Button(root, text='Функция 3', command=func_3, width=15, height=2)
btn_func3.pack(pady=5)

root.mainloop()