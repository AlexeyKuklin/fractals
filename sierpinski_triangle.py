import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Треугольник Серпинского")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
PURPLE = (138, 43, 226)
PINK = (255, 105, 180)

def get_color(depth, max_depth):
    """Возвращает цвет в зависимости от глубины"""
    if max_depth == 0:
        return BLUE
    t = depth / max_depth
    
    # Градиент от синего через фиолетовый к розовому
    if t < 0.5:
        t2 = t * 2
        color = (
            int(BLUE[0] + (PURPLE[0] - BLUE[0]) * t2),
            int(BLUE[1] + (PURPLE[1] - BLUE[1]) * t2),
            int(BLUE[2] + (PURPLE[2] - BLUE[2]) * t2)
        )
    else:
        t2 = (t - 0.5) * 2
        color = (
            int(PURPLE[0] + (PINK[0] - PURPLE[0]) * t2),
            int(PURPLE[1] + (PINK[1] - PURPLE[1]) * t2),
            int(PURPLE[2] + (PINK[2] - PURPLE[2]) * t2)
        )
    return color

def draw_sierpinski_triangle(surface, x1, y1, x2, y2, x3, y3, depth, max_depth):
    """
    Рекурсивно рисует треугольник Серпинского
    (x1, y1), (x2, y2), (x3, y3) - координаты вершин треугольника
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        # Рисуем закрашенный треугольник
        color = get_color(0, max_depth)
        points = [(x1, y1), (x2, y2), (x3, y3)]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, BLACK, points, 1)
        return
    
    # Вычисляем середины сторон
    mid_x1 = (x1 + x2) / 2
    mid_y1 = (y1 + y2) / 2
    
    mid_x2 = (x2 + x3) / 2
    mid_y2 = (y2 + y3) / 2
    
    mid_x3 = (x3 + x1) / 2
    mid_y3 = (y3 + y1) / 2
    
    # Рисуем центральный треугольник (вырезаемый)
    color = get_color(depth, max_depth)
    center_points = [(mid_x1, mid_y1), (mid_x2, mid_y2), (mid_x3, mid_y3)]
    pygame.draw.polygon(surface, color, center_points)
    pygame.draw.polygon(surface, BLACK, center_points, 1)
    
    # Рекурсивно рисуем три угловых треугольника
    # Верхний треугольник
    draw_sierpinski_triangle(surface, x1, y1, mid_x1, mid_y1, mid_x3, mid_y3, depth - 1, max_depth)
    
    # Левый нижний треугольник
    draw_sierpinski_triangle(surface, mid_x1, mid_y1, x2, y2, mid_x2, mid_y2, depth - 1, max_depth)
    
    # Правый нижний треугольник
    draw_sierpinski_triangle(surface, mid_x3, mid_y3, mid_x2, mid_y2, x3, y3, depth - 1, max_depth)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для треугольника Серпинского
    margin = 80
    size = min(WIDTH, HEIGHT) - 2 * margin
    
    # Вычисляем координаты вершин равностороннего треугольника
    # Верхняя вершина
    top_x = WIDTH / 2
    top_y = margin
    
    # Левая нижняя вершина
    left_x = (WIDTH - size) / 2
    left_y = margin + size * math.sqrt(3) / 2
    
    # Правая нижняя вершина
    right_x = (WIDTH + size) / 2
    right_y = margin + size * math.sqrt(3) / 2
    
    depth = 7
    
    # Рисуем треугольник Серпинского
    draw_sierpinski_triangle(screen, top_x, top_y, left_x, left_y, right_x, right_y, depth, depth)
    
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

