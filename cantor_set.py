import pygame

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Канторово множество")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
DARK_BLUE = (0, 100, 200)

def get_color(depth, max_depth):
    """Возвращает цвет в зависимости от глубины"""
    if max_depth == 0:
        return BLACK
    t = depth / max_depth
    color = (
        int(DARK_BLUE[0] + (BLUE[0] - DARK_BLUE[0]) * t),
        int(DARK_BLUE[1] + (BLUE[1] - DARK_BLUE[1]) * t),
        int(DARK_BLUE[2] + (BLUE[2] - DARK_BLUE[2]) * t)
    )
    return color

def draw_cantor(surface, x, y, length, height, depth, max_depth):
    """
    Рекурсивно рисует Канторово множество
    x, y - левый верхний угол текущего отрезка
    length - длина отрезка
    height - высота отрезка
    depth - текущая глубина рекурсии
    """
    if depth == 0:
        return
    
    # Рисуем текущий отрезок
    color = get_color(depth, max_depth)
    pygame.draw.rect(surface, color, (x, y, length, height))
    pygame.draw.rect(surface, BLACK, (x, y, length, height), 1)
    
    # Вычисляем длину новых отрезков (треть от текущей)
    new_length = length / 3
    
    # Вычисляем позицию следующего уровня
    new_y = y + height * 1.5
    
    # Рисуем левый отрезок (первая треть)
    draw_cantor(surface, x, new_y, new_length, height, depth - 1, max_depth)
    
    # Рисуем правый отрезок (последняя треть, пропускаем среднюю)
    draw_cantor(surface, x + 2 * new_length, new_y, new_length, height, depth - 1, max_depth)

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для Канторова множества
    margin = 50
    start_length = WIDTH - 2 * margin
    start_x = margin
    start_y = 50
    segment_height = 20
    depth = 8
    
    # Рисуем Канторово множество
    draw_cantor(screen, start_x, start_y, start_length, segment_height, depth, depth)
    
    # Добавляем текст
    font = pygame.font.Font(None, 36)
    text = font.render("Канторово множество", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text, text_rect)
    
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

