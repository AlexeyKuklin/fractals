import pygame
import numpy as np

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Множество Жюлиа")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_color(iterations, max_iterations):
    """
    Возвращает цвет на основе количества итераций
    Создает красивый цветной градиент
    """
    if iterations == max_iterations:
        return BLACK
    
    # Нормализуем количество итераций
    t = iterations / max_iterations
    
    # Создаем цветной градиент
    if t < 0.16:
        # Темно-синий -> синий
        ratio = t / 0.16
        return (0, int(50 + 100 * ratio), int(100 + 155 * ratio))
    elif t < 0.33:
        # Синий -> голубой
        ratio = (t - 0.16) / 0.17
        return (0, int(150 + 105 * ratio), 255)
    elif t < 0.5:
        # Голубой -> зеленый
        ratio = (t - 0.33) / 0.17
        return (int(0 + 100 * ratio), 255, int(255 - 155 * ratio))
    elif t < 0.67:
        # Зеленый -> желтый
        ratio = (t - 0.5) / 0.17
        return (int(100 + 155 * ratio), 255, int(100 - 100 * ratio))
    elif t < 0.83:
        # Желтый -> оранжевый
        ratio = (t - 0.67) / 0.16
        return (255, int(255 - 155 * ratio), 0)
    else:
        # Оранжевый -> красный
        ratio = (t - 0.83) / 0.17
        return (255, int(100 - 80 * ratio), 0)

def julia_set(width, height, c_real, c_imag, max_iterations=100):
    """
    Вычисляет множество Жюлиа
    
    width, height - размеры изображения
    c_real, c_imag - параметры комплексного числа c
    max_iterations - максимальное количество итераций
    
    Возвращает массив с количеством итераций для каждого пикселя
    """
    # Определяем область комплексной плоскости
    x_min, x_max = -2.0, 2.0
    y_min, y_max = -1.5, 1.5
    
    # Создаем массивы координат
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    
    # Создаем сетку
    X, Y = np.meshgrid(x, y)
    
    # Комплексная плоскость
    Z = X + 1j * Y
    
    # Константа c
    C = complex(c_real, c_imag)
    
    # Массив для хранения результатов
    result = np.zeros(Z.shape, dtype=int)
    
    # Маска для точек, которые еще не вышли за пределы
    mask = np.ones(Z.shape, dtype=bool)
    
    print("Вычисление множества Жюлиа...")
    
    # Итерационный процесс
    for i in range(max_iterations):
        if i % 10 == 0:
            print(f"Итерация {i}/{max_iterations}")
        
        # Z = Z^2 + C для всех точек
        Z[mask] = Z[mask] ** 2 + C
        
        # Проверяем, какие точки вышли за пределы (|Z| > 2)
        escaped = np.abs(Z) > 2
        newly_escaped = escaped & mask
        
        # Записываем количество итераций для вышедших точек
        result[newly_escaped] = i
        
        # Обновляем маску
        mask = mask & ~escaped
        
        # Если все точки вышли, прерываем
        if not mask.any():
            break
    
    # Для точек, которые не вышли, ставим максимальное значение
    result[mask] = max_iterations
    
    print("Вычисление завершено!")
    return result

def draw_julia(surface, data, max_iterations):
    """Рисует множество Жюлиа"""
    height, width = data.shape
    
    print("Рисование...")
    
    # Создаем массив пикселей
    pixel_array = pygame.surfarray.pixels3d(surface)
    
    for y in range(height):
        for x in range(width):
            iterations = data[y, x]
            color = get_color(iterations, max_iterations)
            pixel_array[x, y] = color
    
    del pixel_array  # Освобождаем блокировку поверхности
    
    print("Рисование завершено!")

def main():
    """Основная функция"""
    clock = pygame.time.Clock()
    running = True
    
    # Очищаем экран
    screen.fill(WHITE)
    
    # Параметры множества Жюлиа
    # Интересные значения c:
    # -0.7 + 0.27015i - классическая форма
    # -0.4 + 0.6i - дендрит
    # 0.285 + 0.01i - спираль
    # -0.8 + 0.156i - кристалл
    # -0.4 - 0.59i - дракон
    
    c_real = -0.7
    c_imag = 0.27015
    max_iterations = 100
    
    print(f"Генерация множества Жюлиа для c = {c_real} + {c_imag}i")
    
    # Вычисляем множество Жюлиа
    julia_data = julia_set(WIDTH, HEIGHT, c_real, c_imag, max_iterations)
    
    # Рисуем
    draw_julia(screen, julia_data, max_iterations)
    
    # Обновляем экран
    pygame.display.flip()
    
    print("Готово! Закройте окно для выхода.")
    
    # Основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

