import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ковер Серпинского")

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
    
    # Переход от синего через фиолетовый к розовому
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

def draw_sierpinski_carpet(surface, x, y, size, depth, max_depth):
    """
    Рекурсивно рисует ковер Серпинского
    x, y - левый верхний угол квадрата
    size - размер стороны квадрата
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        # Базовый случай: рисуем закрашенный квадрат
        color = get_color(0, max_depth)
        pygame.draw.rect(surface, color, (x, y, size, size))
        pygame.draw.rect(surface, BLACK, (x, y, size, size), 1)
        return
    
    # Делим квадрат на 9 частей (3x3)
    new_size = size / 3
    
    # Рисуем 8 квадратов (пропускаем центральный)
    positions = [
        (0, 0), (1, 0), (2, 0),  # верхний ряд
        (0, 1),         (2, 1),  # средний ряд (без центра)
        (0, 2), (1, 2), (2, 2)   # нижний ряд
    ]
    
    for i, j in positions:
        new_x = x + i * new_size
        new_y = y + j * new_size
        draw_sierpinski_carpet(surface, new_x, new_y, new_size, depth - 1, max_depth)
    
    # Рисуем центральный квадрат (дырку) с цветом текущей глубины
    center_x = x + new_size
    center_y = y + new_size
    center_color = get_color(depth, max_depth)
    pygame.draw.rect(surface, center_color, (center_x, center_y, new_size, new_size))
    pygame.draw.rect(surface, BLACK, (center_x, center_y, new_size, new_size), 1)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для ковра
    size = 729  # 3^6 для ровного деления
    start_x = (WIDTH - size) // 2
    start_y = (HEIGHT - size) // 2
    depth = 5
    
    # Рисуем ковер Серпинского
    draw_sierpinski_carpet(screen, start_x, start_y, size, depth, depth)
    
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

