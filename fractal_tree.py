import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фрактальное дерево")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (101, 67, 33)
DARK_GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)

def get_color(depth, max_depth):
    """Возвращает цвет в зависимости от глубины"""
    if max_depth == 0:
        return BROWN
    t = (max_depth - depth) / max_depth
    
    # Переход от коричневого к темно-зеленому и светло-зеленому
    if t < 0.5:
        # От коричневого к темно-зеленому
        t2 = t * 2
        color = (
            int(BROWN[0] + (DARK_GREEN[0] - BROWN[0]) * t2),
            int(BROWN[1] + (DARK_GREEN[1] - BROWN[1]) * t2),
            int(BROWN[2] + (DARK_GREEN[2] - BROWN[2]) * t2)
        )
    else:
        # От темно-зеленого к светло-зеленому
        t2 = (t - 0.5) * 2
        color = (
            int(DARK_GREEN[0] + (LIGHT_GREEN[0] - DARK_GREEN[0]) * t2),
            int(DARK_GREEN[1] + (LIGHT_GREEN[1] - DARK_GREEN[1]) * t2),
            int(DARK_GREEN[2] + (LIGHT_GREEN[2] - DARK_GREEN[2]) * t2)
        )
    return color

def get_thickness(depth, max_depth):
    """Возвращает толщину ветки в зависимости от глубины"""
    if max_depth == 0:
        return 1
    # Толщина уменьшается экспоненциально
    return max(1, int(10 * (depth / max_depth) ** 1.5))

def draw_branch(surface, x, y, length, angle, depth, max_depth):
    """
    Рекурсивно рисует ветку дерева
    x, y - начальная точка ветки
    length - длина ветки
    angle - угол направления ветки (в радианах, 0 = вправо, π/2 = вверх)
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        return
    
    # Вычисляем конечную точку ветки
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    
    # Определяем цвет и толщину
    color = get_color(depth, max_depth)
    thickness = get_thickness(depth, max_depth)
    
    # Рисуем ветку
    pygame.draw.line(surface, color, (x, y), (end_x, end_y), thickness)
    
    # Параметры для дочерних веток
    new_length = length * 0.7  # Уменьшаем длину на 30%
    angle_delta = math.pi / 6  # 30 градусов
    
    # Рисуем левую ветку (поворот влево)
    draw_branch(surface, end_x, end_y, new_length, angle - angle_delta, depth - 1, max_depth)
    
    # Рисуем правую ветку (поворот вправо)
    draw_branch(surface, end_x, end_y, new_length, angle + angle_delta, depth - 1, max_depth)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для дерева
    start_x = WIDTH // 2
    start_y = HEIGHT - 50
    trunk_length = 150
    initial_angle = -math.pi / 2  # Направление вверх
    depth = 10
    
    # Рисуем дерево
    draw_branch(screen, start_x, start_y, trunk_length, initial_angle, depth, depth)
    
    # Обновляем экран
    pygame.display.flip()
    
    # Основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

