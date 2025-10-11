import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кривая Дракона")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

def get_color(progress):
    """
    Возвращает цвет в зависимости от прогресса по кривой (0.0 - 1.0)
    Создает радужный градиент
    """
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]
    
    if progress >= 1.0:
        return colors[-1]
    
    # Определяем между какими цветами интерполировать
    segment = progress * (len(colors) - 1)
    index = int(segment)
    t = segment - index
    
    if index >= len(colors) - 1:
        return colors[-1]
    
    # Интерполяция между двумя цветами
    color1 = colors[index]
    color2 = colors[index + 1]
    
    color = (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )
    return color

class Turtle:
    """Черепашья графика для рисования кривой"""
    def __init__(self, x, y, angle, step):
        self.x = x
        self.y = y
        self.angle = angle
        self.step = step
        self.points = [(x, y)]
    
    def forward(self):
        """Движение вперед"""
        self.x += self.step * math.cos(math.radians(self.angle))
        self.y += self.step * math.sin(math.radians(self.angle))
        self.points.append((self.x, self.y))
    
    def left(self):
        """Поворот налево на 90 градусов"""
        self.angle += 90
    
    def right(self):
        """Поворот направо на 90 градусов"""
        self.angle -= 90

def dragon_curve_sequence(order):
    """
    Генерирует последовательность поворотов для кривой Дракона
    R - поворот направо, L - поворот налево
    """
    if order == 0:
        return ""
    
    # Алгоритм: каждый новый порядок = предыдущий + R + зеркальное_отражение(предыдущий)
    sequence = "R"
    
    for i in range(1, order):
        # Зеркальное отражение: L <-> R
        reversed_seq = ""
        for char in reversed(sequence):
            if char == 'R':
                reversed_seq += 'L'
            else:
                reversed_seq += 'R'
        
        # Добавляем R между последовательностями
        sequence = sequence + "R" + reversed_seq
    
    return sequence

def draw_dragon_curve(surface, center_x, center_y, step, order):
    """Рисует кривую Дракона с центрированием"""
    print(f"Генерация последовательности для порядка {order}...")
    sequence = dragon_curve_sequence(order)
    
    print(f"Длина последовательности: {len(sequence)}")
    print("Построение кривой...")
    
    # Создаем черепаху с временными координатами
    turtle = Turtle(0, 0, 0, step)
    
    # Первый шаг вперед
    turtle.forward()
    
    # Выполняем последовательность поворотов
    for turn in sequence:
        if turn == 'R':
            turtle.right()
        else:
            turtle.left()
        turtle.forward()
    
    # Находим границы кривой
    points = turtle.points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Вычисляем смещение для центрирования
    offset_x = center_x - (min_x + max_x) / 2
    offset_y = center_y - (min_y + max_y) / 2
    
    print(f"Границы: x[{min_x:.0f}, {max_x:.0f}], y[{min_y:.0f}, {max_y:.0f}]")
    
    # Рисуем кривую с градиентом и смещением
    print("Рисование...")
    total = len(points) - 1
    
    for i in range(len(points) - 1):
        progress = i / total
        color = get_color(progress)
        p1 = (points[i][0] + offset_x, points[i][1] + offset_y)
        p2 = (points[i + 1][0] + offset_x, points[i + 1][1] + offset_y)
        pygame.draw.line(surface, color, p1, p2, 2)
    
    print(f"Нарисовано сегментов: {len(points) - 1}")

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для кривой Дракона
    order = 13  # Порядок кривой (10-15 рекомендуется)
    
    # Вычисляем размер шага
    # Для order=13: 2^13 = 8192 сегмента
    total_segments = 2 ** order
    step = 4  # Длина одного сегмента
    
    # Центр экрана
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    print(f"Кривая Дракона порядка {order}")
    print(f"Количество сегментов: {total_segments}")
    
    # Рисуем кривую Дракона (функция сама отцентрирует)
    draw_dragon_curve(screen, center_x, center_y, step, order)
    
    # Обновляем экран
    pygame.display.flip()
    
    print("Готово!")
    
    # Основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

