import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фрактал Пифагора")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 90, 43)
GREEN = (50, 205, 50)

def get_color(depth, max_depth):
    """Возвращает цвет в зависимости от глубины"""
    if max_depth == 0:
        return BROWN
    t = (max_depth - depth) / max_depth
    color = (
        int(BROWN[0] + (GREEN[0] - BROWN[0]) * t),
        int(BROWN[1] + (GREEN[1] - BROWN[1]) * t),
        int(BROWN[2] + (GREEN[2] - BROWN[2]) * t)
    )
    return color

def pythagoras_tree(surface, x, y, width, height, depth, max_depth):
    """
    Рекурсивно рисует дерево Пифагора
    x, y - левый нижний угол квадрата
    width - ширина квадрата (вектор вправо)
    height - высота квадрата (вектор вверх)
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        return
    
    # Вычисляем четыре угла квадрата
    x1, y1 = x, y  # левый нижний
    x2, y2 = x + width, y + height  # правый нижний
    x3, y3 = x2 + height, y2 - width  # правый верхний
    x4, y4 = x + height, y - width  # левый верхний
    
    # Рисуем квадрат
    points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    color = get_color(depth, max_depth)
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, 1)
    
    if depth > 1:
        # Вычисляем вершину треугольника над квадратом
        # Центр верхней стороны
        mid_x = (x4 + x3) / 2
        mid_y = (y4 + y3) / 2
        
        # Длина стороны квадрата
        side_length = math.sqrt(width * width + height * height)
        
        # Высота равнобедренного прямоугольного треугольника = половина основания
        triangle_height = side_length / 2
        
        # Направление перпендикулярно верхней стороне (наружу от квадрата)
        perp_x = height / side_length * triangle_height
        perp_y = -width / side_length * triangle_height
        
        # Вершина треугольника
        apex_x = mid_x + perp_x
        apex_y = mid_y + perp_y
        
        # Векторы для левого катета треугольника (от левого верхнего угла к вершине)
        left_vec_x = apex_x - x4
        left_vec_y = apex_y - y4
        
        # Векторы для правого катета (от вершины к правому верхнему углу)
        right_vec_x = x3 - apex_x
        right_vec_y = y3 - apex_y
        
        # Строим левый квадрат на левом катете
        pythagoras_tree(surface, x4, y4, left_vec_x, left_vec_y, depth - 1, max_depth)
        
        # Строим правый квадрат на правом катете
        pythagoras_tree(surface, apex_x, apex_y, right_vec_x, right_vec_y, depth - 1, max_depth)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для фрактала
    base_size = 120
    start_x = WIDTH // 2 - base_size // 2
    start_y = HEIGHT - 150
    depth = 4
    
    # Рисуем фрактал
    # Базовый квадрат: горизонтальная база, растет вверх
    pythagoras_tree(screen, start_x, start_y, base_size, 0, depth, depth)
    
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
