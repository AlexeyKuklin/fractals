import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кривая Пеано")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 100, 255)
PURPLE = (138, 43, 226)
MAGENTA = (255, 0, 255)

def get_color(progress):
    """Возвращает цвет в зависимости от прогресса"""
    colors = [CYAN, BLUE, PURPLE, MAGENTA]
    
    if progress >= 1.0:
        return colors[-1]
    
    segment = progress * (len(colors) - 1)
    index = int(segment)
    t = segment - index
    
    if index >= len(colors) - 1:
        return colors[-1]
    
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

def peano_lsystem(order):
    """
    Генерирует L-систему для кривой Пеано
    L: влево
    R: вправо
    F: движение вперед
    """
    axiom = "L"
    rules = {
        'L': "LFRFL-F-RFLFR+F+LFRFL",
        'R': "RFLFR+F+LFRFL-F-RFLFR"
    }
    
    result = axiom
    for _ in range(order):
        new_result = ""
        for char in result:
            if char in rules:
                new_result += rules[char]
            else:
                new_result += char
        result = new_result
    
    return result

def draw_peano(surface, center_x, center_y, size, order):
    """Рисует кривую Пеано"""
    # Генерируем L-систему
    print("Генерация L-системы...")
    lsystem = peano_lsystem(order)
    
    # Вычисляем длину шага - используем временный размер для расчета
    temp_step = 10
    turtle_temp = Turtle(0, 0, 0, temp_step)
    
    # Выполняем команды для определения размеров
    print("Вычисление размеров...")
    for char in lsystem:
        if char == 'F':
            turtle_temp.forward()
        elif char == '+':
            turtle_temp.left()
        elif char == '-':
            turtle_temp.right()
    
    # Находим границы
    points_temp = turtle_temp.points
    xs = [p[0] for p in points_temp]
    ys = [p[1] for p in points_temp]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    width = max_x - min_x
    height = max_y - min_y
    
    # Вычисляем реальный шаг для заданного размера
    if width > height:
        real_step = size / width * temp_step
    else:
        real_step = size / height * temp_step
    
    print(f"Ширина: {width:.0f}, высота: {height:.0f}, шаг: {real_step:.2f}")
    
    # Создаем реальную черепаху
    turtle = Turtle(0, 0, 0, real_step)
    
    # Выполняем команды
    print("Построение кривой...")
    for char in lsystem:
        if char == 'F':
            turtle.forward()
        elif char == '+':
            turtle.left()
        elif char == '-':
            turtle.right()
    
    # Находим границы реальной кривой
    points = turtle.points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Вычисляем смещение для центрирования
    offset_x = center_x - (min_x + max_x) / 2
    offset_y = center_y - (min_y + max_y) / 2
    
    # Применяем смещение и рисуем
    print("Рисование...")
    total = len(points) - 1
    
    for i in range(len(points) - 1):
        progress = i / total
        color = get_color(progress)
        p1 = (points[i][0] + offset_x, points[i][1] + offset_y)
        p2 = (points[i + 1][0] + offset_x, points[i + 1][1] + offset_y)
        pygame.draw.line(surface, color, p1, p2, 3)
    
    print(f"Нарисовано сегментов: {len(points) - 1}")

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для кривой Пеано
    order = 4  # Порядок кривой (1-4 рекомендуется)
    
    # Размер кривой
    margin = 80
    size = min(WIDTH, HEIGHT) - 2 * margin
    
    # Центр экрана
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Рисуем кривую (передаем центр, функция сама отцентрирует)
    draw_peano(screen, center_x, center_y, size, order)
    
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
