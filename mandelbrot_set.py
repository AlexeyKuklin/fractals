import pygame
import numpy as np

# Инициализация pygame
pygame.init()

# Параметры окна
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Множество Мандельброта")

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
    
    # Создаем цветной градиент - от темно-синего через фиолетовый к желто-белому
    if t < 0.16:
        # Темно-синий -> синий
        ratio = t / 0.16
        return (int(10 * ratio), int(10 * ratio), int(50 + 100 * ratio))
    elif t < 0.33:
        # Синий -> фиолетовый
        ratio = (t - 0.16) / 0.17
        return (int(0 + 100 * ratio), int(10 + 40 * ratio), int(150 + 55 * ratio))
    elif t < 0.5:
        # Фиолетовый -> розовый
        ratio = (t - 0.33) / 0.17
        return (int(100 + 100 * ratio), int(50 + 100 * ratio), int(205 - 55 * ratio))
    elif t < 0.67:
        # Розовый -> оранжевый
        ratio = (t - 0.5) / 0.17
        return (int(200 + 55 * ratio), int(150 + 55 * ratio), int(150 - 100 * ratio))
    elif t < 0.83:
        # Оранжевый -> желтый
        ratio = (t - 0.67) / 0.16
        return (255, int(205 + 50 * ratio), int(50 + 100 * ratio))
    else:
        # Желтый -> белый
        ratio = (t - 0.83) / 0.17
        return (255, 255, int(150 + 105 * ratio))

def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iterations=100):
    """
    Вычисляет множество Мандельброта
    
    width, height - размеры изображения
    x_min, x_max, y_min, y_max - область комплексной плоскости для отображения
    max_iterations - максимальное количество итераций
    
    Возвращает массив с количеством итераций для каждого пикселя
    """
    # Создаем массивы координат
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    
    # Создаем сетку
    X, Y = np.meshgrid(x, y)
    
    # Комплексная плоскость - это константа C для каждой точки
    C = X + 1j * Y
    
    # Начальное значение Z = 0 для всех точек
    Z = np.zeros_like(C)
    
    # Массив для хранения результатов
    result = np.zeros(C.shape, dtype=int)
    
    # Маска для точек, которые еще не вышли за пределы
    mask = np.ones(C.shape, dtype=bool)
    
    print("Вычисление множества Мандельброта...")
    
    # Итерационный процесс: Z = Z^2 + C
    for i in range(max_iterations):
        if i % 10 == 0:
            print(f"Итерация {i}/{max_iterations}")
        
        # Z = Z^2 + C для всех точек
        Z[mask] = Z[mask] ** 2 + C[mask]
        
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

def draw_mandelbrot(surface, data, max_iterations):
    """Рисует множество Мандельброта"""
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
    
    # Параметры множества Мандельброта
    # Раскомментируйте нужный вариант для экспериментов:
    
    # 1. Полный вид (классическая форма "жука")
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.25, 1.25
    max_iterations = 100
    
    # 2. Увеличение на "антенну" (детальная спираль сверху)
    # x_min, x_max = -0.8, -0.4
    # y_min, y_max = 0.0, 0.4
    # max_iterations = 150
    
    # 3. Долина морских коньков (очень детальная область)
    # x_min, x_max = -0.75, -0.73
    # y_min, y_max = 0.09, 0.11
    # max_iterations = 200
    
    # 4. Минибро (маленькая копия множества)
    # x_min, x_max = -0.16, -0.14
    # y_min, y_max = 1.025, 1.045
    # max_iterations = 200
    
    # 5. Слоновая долина (детальные филаменты справа)
    # x_min, x_max = 0.25, 0.35
    # y_min, y_max = 0.0, 0.1
    # max_iterations = 200
    
    # 6. Тройная спираль (красивые завитки)
    # x_min, x_max = -0.77, -0.74
    # y_min, y_max = 0.08, 0.11
    # max_iterations = 250
    
    print("Генерация множества Мандельброта")
    print(f"Область: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    
    # Вычисляем множество Мандельброта
    mandelbrot_data = mandelbrot_set(WIDTH, HEIGHT, x_min, x_max, y_min, y_max, max_iterations)
    
    # Рисуем
    draw_mandelbrot(screen, mandelbrot_data, max_iterations)
    
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

