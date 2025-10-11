import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Снежинка Коха")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 255)
LIGHT_BLUE = (135, 206, 250)

def get_color(depth, max_depth):
    """Возвращает цвет в зависимости от глубины"""
    if max_depth == 0:
        return BLUE
    t = depth / max_depth
    color = (
        int(BLUE[0] + (LIGHT_BLUE[0] - BLUE[0]) * t),
        int(BLUE[1] + (LIGHT_BLUE[1] - BLUE[1]) * t),
        int(BLUE[2] + (LIGHT_BLUE[2] - BLUE[2]) * t)
    )
    return color

def koch_curve(surface, x1, y1, x2, y2, depth, max_depth):
    """
    Рекурсивно рисует кривую Коха
    x1, y1 - начальная точка отрезка
    x2, y2 - конечная точка отрезка
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        # Базовый случай: рисуем прямую линию
        color = get_color(depth, max_depth)
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)
        return
    
    # Вычисляем длину и угол отрезка
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    angle = math.atan2(dy, dx)
    
    # Делим отрезок на три части и находим точки
    # Первая точка: 1/3 от начала
    x3 = x1 + dx / 3
    y3 = y1 + dy / 3
    
    # Вторая точка: 2/3 от начала
    x5 = x1 + 2 * dx / 3
    y5 = y1 + 2 * dy / 3
    
    # Вершина треугольника (средняя точка)
    # Берем вектор от x3 к x5 и поворачиваем его на -60 градусов (влево)
    vec_x = x5 - x3
    vec_y = y5 - y3
    # Поворот на -60 градусов
    angle_60 = -math.pi / 3
    x4 = x3 + vec_x * math.cos(angle_60) - vec_y * math.sin(angle_60)
    y4 = y3 + vec_x * math.sin(angle_60) + vec_y * math.cos(angle_60)
    
    # Рекурсивно рисуем четыре сегмента
    koch_curve(surface, x1, y1, x3, y3, depth - 1, max_depth)
    koch_curve(surface, x3, y3, x4, y4, depth - 1, max_depth)
    koch_curve(surface, x4, y4, x5, y5, depth - 1, max_depth)
    koch_curve(surface, x5, y5, x2, y2, depth - 1, max_depth)

def koch_snowflake(surface, center_x, center_y, size, depth):
    """
    Рисует снежинку Коха (три кривых Коха, образующих треугольник)
    center_x, center_y - центр снежинки
    size - размер (радиус описанной окружности)
    depth - глубина рекурсии
    """
    # Вычисляем три вершины равностороннего треугольника
    # Вершины расположены под углами 90°, 210°, 330° (треугольник вершиной вверх)
    points = []
    for i in range(3):
        angle = math.pi / 2 + i * 2 * math.pi / 3
        x = center_x + size * math.cos(angle)
        y = center_y + size * math.sin(angle)
        points.append((x, y))
    
    # Рисуем три кривых Коха, образующих снежинку
    for i in range(3):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % 3]
        koch_curve(surface, x1, y1, x2, y2, depth, depth)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для снежинки
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    size = 250
    depth = 4
    
    # Рисуем снежинку
    koch_snowflake(screen, center_x, center_y, size, depth)
    
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

