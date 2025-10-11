import pygame
import math

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кривая Гильберта")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

def get_color(progress):
    """
    Возвращает цвет в зависимости от прогресса по кривой (0.0 - 1.0)
    Создает радужный градиент
    """
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    
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

class HilbertCurve:
    def __init__(self, surface, start_x, start_y, size, order):
        """
        Инициализация кривой Гильберта
        surface - поверхность для рисования
        start_x, start_y - начальная позиция
        size - размер области
        order - порядок кривой (глубина рекурсии)
        """
        self.surface = surface
        self.size = size
        self.order = order
        
        # Вычисляем длину одного сегмента
        total_segments = (2 ** order) ** 2 - 1
        self.segment_length = size / (2 ** order)
        
        # Текущая позиция и направление
        self.x = start_x + self.segment_length / 2
        self.y = start_y + self.segment_length / 2
        self.angle = 0  # 0=право, 90=вверх, 180=лево, 270=вниз
        
        # Список точек для рисования
        self.points = [(self.x, self.y)]
        self.segment_count = 0
        self.total_segments = total_segments
    
    def forward(self):
        """Двигаемся вперед на один сегмент"""
        angle_rad = math.radians(self.angle)
        new_x = self.x + self.segment_length * math.cos(angle_rad)
        new_y = self.y - self.segment_length * math.sin(angle_rad)
        
        # Рисуем линию с цветом в зависимости от прогресса
        progress = self.segment_count / self.total_segments
        color = get_color(progress)
        pygame.draw.line(self.surface, color, (self.x, self.y), (new_x, new_y), 3)
        
        self.x = new_x
        self.y = new_y
        self.points.append((self.x, self.y))
        self.segment_count += 1
    
    def left(self):
        """Поворот налево на 90 градусов"""
        self.angle = (self.angle + 90) % 360
    
    def right(self):
        """Поворот направо на 90 градусов"""
        self.angle = (self.angle - 90) % 360
    
    def hilbert(self, order, direction=1):
        """
        Рекурсивно рисует кривую Гильберта
        order - порядок кривой
        direction - направление (1 или -1 для зеркального отражения)
        """
        if order == 0:
            return
        
        if direction > 0:
            self.right()
            self.hilbert(order - 1, -direction)
            self.forward()
            self.left()
            self.hilbert(order - 1, direction)
            self.forward()
            self.hilbert(order - 1, direction)
            self.left()
            self.forward()
            self.hilbert(order - 1, -direction)
            self.right()
        else:
            self.left()
            self.hilbert(order - 1, -direction)
            self.forward()
            self.right()
            self.hilbert(order - 1, direction)
            self.forward()
            self.hilbert(order - 1, direction)
            self.right()
            self.forward()
            self.hilbert(order - 1, -direction)
            self.left()

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры для кривой Гильберта
    size = 700
    start_x = (WIDTH - size) // 2
    start_y = (HEIGHT - size) // 2
    order = 6  # Порядок кривой (1-7 рекомендуется)
    
    # Рисуем рамку
    pygame.draw.rect(screen, BLACK, (start_x, start_y, size, size), 2)
    
    # Создаем и рисуем кривую Гильберта
    hilbert = HilbertCurve(screen, start_x, start_y, size, order)
    hilbert.hilbert(order)
    
    # Обновляем экран
    pygame.display.flip()
    
    print(f"Нарисовано сегментов: {hilbert.segment_count}")
    
    # Основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

