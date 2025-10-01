import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Характеристики частицы
class Particle:
    def __init__(self, pos, vel, lifetime):
        self.pos = np.array(pos, dtype=float) # Позиция
        self.vel = np.array(vel, dtype=float) # Скорость
        self.lifetime = lifetime # Время жизни
        self.age = 0.0 # Возраст

# Характеристики системы частиц
class ParticleSystem:
    # Инициализация
    def __init__(self, bounds=(0, 10, 0, 10), gravity=(0, -0.1)):
        self.particles = []
        self.bounds = bounds
        self.gravity = np.array(gravity, dtype=float)

    # Добавление частицы
    def add_particle(self, pos, vel, lifetime):
        self.particles.append(Particle(pos, vel, lifetime))

    # Создание рандомный частицы
    def create_random_particle(self):
        pos = [random.uniform(0, 10), random.uniform(0, 10)] # Позиция генерируется рандомно в пределах от 0 до 10
        vel = [random.uniform(-1, 1), random.uniform(-1, 1)] # А скорость по X и Y изменяется от -1 до 1
        lifetime = random.uniform(5, 15) # Жизнь частицы от 5ти до 15 секунд
        self.add_particle(pos, vel, lifetime)

    # Обновляем состояние всех частиц
    def update(self, time_step):
        for particle in self.particles:
            ''' 
            В данном случае реализована функция, о которой говорится в условии задачи, где нам сказано
            new_position = position + velocity * time_step
            Однако, поскольку в системе присутствует гравитация, то для начала нужно просчитать скорость относительно гравитации
            А после этого посчитать новую позицию.
            '''
            particle.vel += self.gravity * time_step # Применяем гравитацию к скорости
            new_pos = particle.pos + particle.vel * time_step # Обновляем позицию

            x_min, x_max, y_min, y_max = self.bounds # Обработка столкновений с границей
            # Проверка границ по X
            if new_pos[0] < x_min:
                new_pos[0] = x_min
                particle.vel[0] = -particle.vel[0]
            elif new_pos[0] > x_max:
                new_pos[0] = x_max
                particle.vel[0] = -particle.vel[0]

            # Проверка границ по Y
            if new_pos[1] < y_min:
                new_pos[1] = y_min
                particle.vel[1] = -particle.vel[1]
            elif new_pos[1] > y_max:
                new_pos[1] = y_max
                particle.vel[1] = -particle.vel[1]

            # Обновление позиции и увеличение жизни частицы
            particle.pos = new_pos
            particle.age += time_step

        # Удаляем "мертвые" частицы
        dead_particles = [p for p in self.particles if p.age >= p.lifetime]
        self.particles = [p for p in self.particles if p.age < p.lifetime]

        return len(dead_particles) # Возвращаем количество умерших частиц для статистики

    # Массив позиций всех частиц
    def get_positions(self):
        return np.array([p.pos for p in self.particles])

    # Массив возраста всех частиц
    def get_ages(self):
        return np.array([p.age for p in self.particles])

    # Массив оставшегося время жизни всех частиц
    def get_remaining_lifetimes(self):
        return np.array([p.lifetime - p.age for p in self.particles])

# Параметры системы
NUM_PARTICLES = 10
TIME_STEP = 0.1

# Создаем систему частиц
system = ParticleSystem(gravity=(0, -0.1))

# Создаем начальные частицы
for i in range(NUM_PARTICLES):
    system.create_random_particle()

# Настройка графики
fig, ax = plt.subplots(figsize=(6, 6))

# Настраиваем область отображения
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Создаем scatter с начальными данными
initial_positions = system.get_positions() # Получаем начальные позиции всех частиц из системы
initial_lifetimes = system.get_remaining_lifetimes() # Получаем оставшееся время жизни для каждой частицы
scat = ax.scatter(initial_positions[:, 0], initial_positions[:, 1], c=initial_lifetimes, s=50, alpha=0.8, cmap='viridis')

# Текст для информации
info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

# Счетчик для статистики
total_died = 0

def init():
    # Инициализируем с текущими позициями
    positions = system.get_positions()
    lifetimes = system.get_remaining_lifetimes()
    scat.set_offsets(positions)
    scat.set_array(lifetimes)

    info_text.set_text(f'Кадр: 0\nУмерло: {total_died}')

    return [scat, info_text]


def animate(frame):
    global total_died

    # Обновляем систему и получаем количество умерших частиц
    died_count = system.update(TIME_STEP)
    total_died += died_count

    # Создаем новые частицы взамен умерших
    for i in range(died_count):
        system.create_random_particle()

    # Получаем позиции частиц
    positions = system.get_positions()
    lifetimes = system.get_remaining_lifetimes()

    # Обновляем scatter plot
    if len(positions) > 0:
        scat.set_offsets(positions)
        scat.set_array(lifetimes)

    # Обновляем информацию
    info_text.set_text(
        f'Кадр: {frame}\nУмерло: {total_died}')

    return [scat, info_text]

# Создаем анимацию
ani = FuncAnimation(fig, animate, frames=60, init_func=init, interval=50, blit=True, repeat=True)

plt.tight_layout()
plt.show()