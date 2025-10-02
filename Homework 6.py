import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Исходные вершины куба в локальной системе координат
vertices = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
])

# Ребра куба
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # нижняя грань
    [4, 5], [5, 6], [6, 7], [7, 4],  # верхняя грань
    [0, 4], [1, 5], [2, 6], [3, 7]  # боковые ребра
]

# Параметры преобразований
t = np.array([2, 3, 1])  # Вектор переноса
s = 0.5  # Коэффициент масштабирования
angle = math.radians(45)  # Угол поворота в радианах

# Масштабирование: P' = S · P
def apply_scale(vertices, scale_factor):
    return vertices * scale_factor

# Поворот вокруг оси Z
def apply_rotation_z(vertices, angle_rad):
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)

    # Матрица поворота вокруг оси Z
    rotation_matrix = np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])

    # Применение поворота к каждой вершине
    rotated_vertices = np.zeros_like(vertices)
    for i, vertex in enumerate(vertices):
        rotated_vertices[i] = rotation_matrix @ vertex

    return rotated_vertices

# Перенос P' = P + T
def apply_translation(vertices, translation_vector):
    return vertices + translation_vector

# Применение преобразований в порядке, указанном в задании
scaled_vertices = apply_scale(vertices, s)
rotated_vertices = apply_rotation_z(scaled_vertices, angle)
transformed_vertices = apply_translation(rotated_vertices, t)


# Создание анимации
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Настройка осей
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-3, 4)
ax.set_ylim(-3, 4)
ax.set_zlim(-3, 4)

# Добавление координатных осей
ax.quiver(0, 0, 0, 1.5, 0, 0, color='r', arrow_length_ratio=0.1, linewidth=2)
ax.quiver(0, 0, 0, 0, 1.5, 0, color='g', arrow_length_ratio=0.1, linewidth=2)
ax.quiver(0, 0, 0, 0, 0, 1.5, color='b', arrow_length_ratio=0.1, linewidth=2)
ax.text(1.5, 0, 0, "X", color='r')
ax.text(0, 1.5, 0, "Y", color='g')
ax.text(0, 0, 1.5, "Z", color='b')

# Список для хранения линий куба
lines = []

# Функция для вычисления промежуточных преобразований
def interpolate_transform(progress):
    # Интерполяция параметров преобразования
    s_interp = 1 + (s - 1) * progress  # от 1 до s
    angle_interp = angle * progress  # от 0 до angle
    t_interp = t * progress  # от [0,0,0] до t

    # Применение преобразований в порядке: масштабирование → поворот → перенос
    scaled = apply_scale(vertices, s_interp)
    rotated = apply_rotation_z(scaled, angle_interp)
    translated = apply_translation(rotated, t_interp)

    return translated


# Функция инициализации анимации
def init():
    for line in lines:
        line.remove()
    lines.clear()
    return []

# Функция обновления кадра анимации
def update(frame):
    # Очистка предыдущих линий
    for line in lines:
        line.remove()
    lines.clear()

    # Вычисление прогресса анимации
    progress = (1 - math.cos(frame / 100 * math.pi)) / 2

    # Получение промежуточных вершин
    intermediate_vertices = interpolate_transform(progress)

    # Отрисовка промежуточного куба
    for edge in edges:
        line = ax.plot3D(*zip(intermediate_vertices[edge[0]], intermediate_vertices[edge[1]]),'red', linewidth=2)[0]
        lines.append(line)

    return lines


# Создание анимации
ani = animation.FuncAnimation(fig, update, frames=100, init_func=init, blit=False, repeat=True, interval=50)

plt.tight_layout()
plt.show()