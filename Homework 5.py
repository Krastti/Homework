import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры системы
NUM_PARTICLES = 30
TIME_STEP = 0.1
GRAVITY = np.array([0, -0.1], dtype=float)
particles = []

total_died = 0

# Функция создания характеристик частицы
def create_particle(pos, vel, lifetime):
    particle = {
        'pos': np.array(pos, dtype=float),
        'vel': np.array(vel, dtype=float),
        'lifetime': lifetime,
        'age': 0.0
    }
    return particle

# Функция создания рандомный частицы
def create_random_particle():
    pos = [random.uniform(0, 10), random.uniform(0, 10)]
    vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
    lifetime = random.uniform(5, 15)

    particles.append(create_particle(pos, vel, lifetime))

# Функция обновления системы
def update_system(time_step):
    global particles, total_died
    dead_count = 0

    for particle in particles:
        ''' 
        В данном случае реализована функция, о которой говорится в условии задачи, где нам сказано
        
        new_position = position + velocity * time_step
                    
        Однако, поскольку в системе присутствует гравитация, то для начала нужно просчитать скорость относительно гравитации
        А после этого посчитать новую позицию.
        '''
        particle['vel'] += GRAVITY * time_step
        new_pos = particle['pos'] + particle['vel'] * time_step

        x_min, x_max, y_min, y_max = 0, 10, 0, 10
        if new_pos[0] < x_min:
            new_pos[0] = x_min
            particle['vel'][0] = -particle['vel'][0]
        elif new_pos[0] > x_max:
            new_pos[0] = x_max
            particle['vel'][0] = -particle['vel'][0]

        if new_pos[1] < y_min:
            new_pos[1] = y_min
            particle['vel'][1] = -particle['vel'][1]
        elif new_pos[1] > y_max:
            new_pos[1] = y_max
            particle['vel'][1] = -particle['vel'][1]

        particle['pos'] = new_pos
        particle['age'] += time_step

        if particle['age'] >= particle['lifetime']:
            dead_count += 1
    particles = [p for p in particles if p['age'] < p['lifetime']]
    total_died += dead_count

    for _ in range(dead_count):
        create_random_particle()
    return dead_count

# Функция позиции частицы
def get_pos(particles_list):
    return np.array([p['pos'] for p in particles_list])

# Функция для вычисления времени жизни частицы
def get_remaining_lifetimes(particles_list):
    return np.array([p['lifetime'] - p['age'] for p in particles_list])

for _ in range(NUM_PARTICLES):
    create_random_particle()

# Настройка графики
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')

initial_pos = get_pos(particles)
initial_lifetimes = get_remaining_lifetimes(particles)
scat = ax.scatter(
    initial_pos[:, 0],
    initial_pos[:, 1],
    c=initial_lifetimes,
    s=50,
    alpha=0.8,
    cmap='inferno',
)

info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

def init():
    positions = get_pos(particles)
    lifetimes = get_remaining_lifetimes(particles)
    scat.set_offsets(positions)
    scat.set_array(lifetimes)
    info_text.set_text(f'Кадр: 0\nУмерло: {total_died}')
    return [scat, info_text]

def animate(frame):
    update_system(TIME_STEP)

    positions = get_pos(particles)
    lifetimes = get_remaining_lifetimes(particles)

    if len(positions) > 0:
        scat.set_offsets(positions)
        scat.set_array(lifetimes)

    info_text.set_text(f'Кадр: {frame}\nУмерло: {total_died}')
    return [scat, info_text]

anim = FuncAnimation(fig, animate, frames=60, init_func=init, interval=50, blit=False, repeat=True)

plt.tight_layout()
plt.show()