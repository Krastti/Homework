import pygame
import sys
import random
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ПВО")

# Загрузка изображений
try:
    background_image = pygame.image.load("фон.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Произошла ошибка загрузки фона: {e}")
try:
    player_image = pygame.image.load("пво.jpg").convert_alpha()
    player_width = 100
    player_height = 80
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
except Exception as e:
    print(f"Произошла ошибка загрузки пво: {e}")
try:
    plane_left_image = pygame.image.load("самолет влево.jpg").convert_alpha()
    plane_width = 60
    plane_height = 30
    plane_left_image = pygame.transform.scale(plane_left_image, (plane_width, plane_height))
except Exception as e:
    print(f"Произошла ошибка загрузки самолета: {e}")
try:
    plane_right_image = pygame.image.load("самолет вправо.jpg").convert_alpha()
    plane_right_image = pygame.transform.scale(plane_right_image, (plane_width, plane_height))
except Exception as e:
    print(f"Произошла ошибка загрузки самолета: {e}")
try:
    bullet_image = pygame.image.load("ракета.jpg").convert_alpha()
    bullet_width = 20
    bullet_height = 40
    bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
except Exception as e:
    print(f"Произошла ошибка загрузки ракета: {e}")

# Цвета
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (231, 76, 60)

# Параметры игры
PLAYER_X = WIDTH // 2
PLAYER_Y = HEIGHT - 40
PLANE_SPEED = 2
BULLET_SPEED = 10
PLANE_SPAWN_RATE = 60
MAX_PLANES = 10
RELOAD_TIME = 30

def create_plane():
    plane = {
        'width': 60,
        'height': 30,
        'y': random.randint(50, HEIGHT - 150),
        'direction': random.choice([-1, 1]),
        'speed': PLANE_SPEED * random.uniform(0.8, 1.4),
        'x': -60 if random.choice([-1, 1]) == -1 else WIDTH + 60
    }
    if plane['direction'] == 1:
        plane['x'] = -plane['width']
    else:
        plane['x'] = WIDTH + plane['width']
    return plane

def update_plane(plane):
    plane['x'] += plane['speed'] * plane['direction']
    return plane

def draw_plane(plane, surface):
    if plane['direction'] == 1 and plane_right_image:
        surface.blit(plane_right_image, (plane['x'] - plane['width'] // 2, plane['y'] - plane['height'] // 2))
    elif plane['direction'] == -1 and plane_left_image:
        surface.blit(plane_left_image, (plane['x'] - plane['width'] // 2, plane['y'] - plane['height'] // 2))

def is_plane_off_screen(plane):
    return plane['x'] < -plane['width'] - 50 or plane['x'] > WIDTH + plane['width'] + 50

def create_bullet(start_x, start_y, target_x, target_y):
    dx = target_x - start_x
    dy = target_y - start_y
    distance = max(1, math.sqrt(dx * dx + dy * dy))
    vx = (dx / distance) * BULLET_SPEED
    vy = (dy / distance) * BULLET_SPEED
    angle = math.degrees(math.atan2(dy, dx))
    return {
        'x': start_x,
        'y': start_y,
        'radius': 4,
        'vx': vx,
        'vy': vy,
        'angle': angle
    }

def update_bullet(bullet):
    bullet['x'] += bullet['vx']
    bullet['y'] += bullet['vy']
    return bullet

def draw_bullet(bullet, surface):
    if bullet_image:
        rotated_bullet = pygame.transform.rotate(bullet_image, -bullet['angle'])
        rect = rotated_bullet.get_rect(center=(int(bullet['x']), int(bullet['y'])))
        surface.blit(rotated_bullet, rect)

def is_bullet_off_screen(bullet):
    return (bullet['x'] < 0 or bullet['x'] > WIDTH or
            bullet['y'] < 0 or bullet['y'] > HEIGHT)

def draw_player(surface, mouse_x, mouse_y):
    if player_image:
        dx = mouse_x - PLAYER_X
        dy = mouse_y - (PLAYER_Y - 10)
        angle = math.degrees(math.atan2(dy, dx))
        rotated_player = pygame.transform.rotate(player_image, -angle)
        rect = rotated_player.get_rect(center=(PLAYER_X, PLAYER_Y))
        surface.blit(rotated_player, rect)

# Игровые переменные
planes = []
bullets = []
reload_counter = 0
game_active = True
clock = pygame.time.Clock()
frame_count = 0
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                if game_active and reload_counter <= 0:
                    bullets.append(create_bullet(PLAYER_X, PLAYER_Y - 10, event.pos[0], event.pos[1]))
                    reload_counter = RELOAD_TIME

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Спавн самолетов
    if frame_count % PLANE_SPAWN_RATE == 0 and len(planes) < MAX_PLANES and game_active:
        planes.append(create_plane())

    # Обновление самолетов
    for i in range(len(planes) - 1, -1, -1):
        planes[i] = update_plane(planes[i])
        if is_plane_off_screen(planes[i]):
            del planes[i]

    # Обновление пуль
    for i in range(len(bullets) - 1, -1, -1):
        bullets[i] = update_bullet(bullets[i])
        if is_bullet_off_screen(bullets[i]):
            del bullets[i]

    # Проверка столкновений
    for i in range(len(bullets) - 1, -1, -1):
        bullet = bullets[i]
        bullet_rect = pygame.Rect(bullet['x'] - bullet['radius'], bullet['y'] - bullet['radius'],
                                  bullet['radius'] * 2, bullet['radius'] * 2)
        for j in range(len(planes) - 1, -1, -1):
            plane = planes[j]
            plane_rect = pygame.Rect(plane['x'] - plane['width'] // 2, plane['y'] - plane['height'] // 2,
                                     plane['width'], plane['height'])
            if bullet_rect.colliderect(plane_rect):
                score += 10
                del planes[j]
                del bullets[i]
                break

    # Уменьшение таймера перезарядки
    if reload_counter > 0:
        reload_counter -= 1

    # Фон
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(SKY_BLUE)

    # Отрисовка объектов
    for plane in planes:
        draw_plane(plane, screen)
    for bullet in bullets:
        draw_bullet(bullet, screen)

    draw_player(screen, mouse_x, mouse_y)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()