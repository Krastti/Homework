# Библиотеки
from turtle import *
from tkinter import *
import matplotlib.pyplot as plt

# Алгоритм Бразенхаума для линии
def bresenham_algorithm(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx > dy:
        error = 2 * dy - dx
        y = y0

        for x in range(x0, x1 + sx, sx):
            points.append([x, y])

            if error >= 0:
                y += sy
                error -= 2 * dx
            error += 2 * dy
    else:
        error = 2 * dx - dy
        x = x0

        for y in range(y0, y1 + sy, sy):
            points.append([x, y])

            if error >= 0:
                x += sx
                error -= 2 * dy
            error += 2 * dx
    return points

# Функция для центрирования окна
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

# Инициализация черепашки
def turtle():
    turtle_window = Toplevel(root)
    turtle_window.title("Черепашка")
    center_window(turtle_window, 500, 500)

    canvas = Canvas(turtle_window, width=500, height=500)
    canvas.pack()

    screen = TurtleScreen(canvas)
    screen.setworldcoordinates(0, 500, 500, 0)
    screen.tracer(0)
    t = RawTurtle(screen)
    t.setpos(0, 0)

    # Создание контекстного меню для черепашки
    turtle_menu = Menu(turtle_window, tearoff=0)
    turtle_menu.add_command(label="Задать координаты", command=lambda: turtle_coordinates(t))

    canvas.bind("<Button-1>", lambda event: turtle_menu.post(event.x_root, event.y_root))

# Создание диалогового окна для ввода координат
def turtle_coordinates(t):
    coord_window = Toplevel(root)
    coord_window.title("Ввод координат")
    center_window(coord_window, 300, 200)

    # Создание меток и полей ввода
    Label(coord_window, text="Начало X:").grid(row=0, column=0, padx=5, pady=5)
    start_x_entry = Entry(coord_window)
    start_x_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(coord_window, text="Начало Y:").grid(row=1, column=0, padx=5, pady=5)
    start_y_entry = Entry(coord_window)
    start_y_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(coord_window, text="Конец X:").grid(row=2, column=0, padx=5, pady=5)
    end_x_entry = Entry(coord_window)
    end_x_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(coord_window, text="Конец Y:").grid(row=3, column=0, padx=5, pady=5)
    end_y_entry = Entry(coord_window)
    end_y_entry.grid(row=3, column=1, padx=5, pady=5)

    # Функция применения координат
    def apply_coordinates():
        start_x = int(start_x_entry.get())
        start_y = int(start_y_entry.get())
        end_x = int(end_x_entry.get())
        end_y = int(end_y_entry.get())

        points = bresenham_algorithm(start_x, start_y, end_x, end_y)
        t.penup()
        t.goto(start_x, start_y)
        t.pendown()
        for i in range(len(points)):
            t.speed(1000)
            t.goto(points[i][0], points[i][1])
            t.dot(5, 'red')

        coord_window.destroy()

    # Кнопка для применения координат
    Button(coord_window, text="Применить", command=apply_coordinates).grid(row=4, column=0, columnspan=2, pady=10)

# Функция для визуализации результатов на графике
def plot_line(points, start_x, start_y, end_x, end_y):
    x_values = [p[0] for p in points]
    y_values = [p[1] for p in points]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, color='red', s=100, zorder=3)

    for i, (x, y) in enumerate(points):
        plt.text(x + 0.05, y + 0.05, f'({x},{y})', fontsize=9)
    plt.plot([start_x, end_x], [start_y, end_y], 'b--', alpha=0.7, label='Идеальная прямая')

    plt.title('Алгоритм Брезенхема для построения отрезка')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.show()


# Создание диалогового окна для ввода координат
def plot_coordinates():
    coord_window = Toplevel(root)
    coord_window.title("Ввод координат графика")
    center_window(coord_window, 300, 180)

    # Создание меток и полей ввода
    Label(coord_window, text="Начало X:").grid(row=0, column=0, padx=5, pady=5)
    start_x_entry = Entry(coord_window)
    start_x_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(coord_window, text="Начало Y:").grid(row=1, column=0, padx=5, pady=5)
    start_y_entry = Entry(coord_window)
    start_y_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(coord_window, text="Конец X:").grid(row=2, column=0, padx=5, pady=5)
    end_x_entry = Entry(coord_window)
    end_x_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(coord_window, text="Конец Y:").grid(row=3, column=0, padx=5, pady=5)
    end_y_entry = Entry(coord_window)
    end_y_entry.grid(row=3, column=1, padx=5, pady=5)

    # Функция применения координат
    def apply_coordinates():
        start_x = int(start_x_entry.get())
        start_y = int(start_y_entry.get())
        end_x = int(end_x_entry.get())
        end_y = int(end_y_entry.get())

        points = bresenham_algorithm(start_x, start_y, end_x, end_y)

        coord_window.destroy()
        plot_line(points, start_x, start_y, end_x, end_y)
    Button(coord_window, text='Применить', command=apply_coordinates).grid(row=4, column=0, columnspan=2, pady=10)

# Создание меню выбора метода
root = Tk()
root.title('Домашняя работа')
center_window(root, 300, 150)

# Создание кнопок
btn_turtle = Button(root, text="Черепашка", command=turtle, width=15, height=2)
btn_turtle.pack(pady=5)

btn_graph = Button(root, text="График", command=plot_coordinates, width=15, height=2)
btn_graph.pack(pady=5)

root.mainloop()