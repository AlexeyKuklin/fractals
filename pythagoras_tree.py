import turtle

# Константы окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Константы дерева
TREE_SIZE = 120  # размер основания дерева
TREE_OFFSET_Y = -200  # смещение дерева вниз от центра
TREE_DEPTH = 8  # глубина рекурсии

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Square:
    """Квадрат, определенный четырьмя точками"""
    def __init__(self, a: Point, b: Point, c: Point, d: Point):
        self.a = a  # верхняя левая
        self.b = b  # верхняя правая
        self.c = c  # нижняя правая
        self.d = d  # нижняя левая

    def draw(self, t: turtle.Turtle):
        """Рисует квадрат"""
        points = [self.a, self.b, self.c, self.d, self.a]
        t.penup()
        t.goto(points[0].x, points[0].y)
        t.pendown()
        for point in points[1:]:
            t.goto(point.x, point.y)

    def get_triangle_point(self) -> Point:
        """Находит точку для построения следующих квадратов"""
        x = self.a.x + ((self.b.x - self.a.x) / 2) + ((self.a.x - self.d.x) / 2)
        y = self.a.y + ((self.b.y - self.a.y) / 2) + ((self.a.y - self.d.y) / 2)
        return Point(x, y)

    def get_next_squares(self) -> tuple['Square', 'Square']:
        """Возвращает следующие два квадрата для построения фрактала"""
        t = self.get_triangle_point()
        
        # Создаем левый квадрат
        left = Square(
            Point(self.a.x + (t.x - self.b.x), self.a.y + (t.y - self.b.y)),
            Point(t.x + (t.x - self.b.x), t.y + (t.y - self.b.y)),
            t,
            self.a
        )
        
        # Создаем правый квадрат
        right = Square(
            Point(t.x + (t.x - self.a.x), t.y + (t.y - self.a.y)),
            Point(self.b.x + (t.x - self.a.x), self.b.y + (t.y - self.a.y)),
            self.b,
            t
        )
        
        return left, right

def draw_pythagoras_tree(t: turtle.Turtle, square: Square, depth: int):
    """Рекурсивно рисует дерево Пифагора"""
    square.draw(t)
    
    if depth > 0:
        left, right = square.get_next_squares()
        draw_pythagoras_tree(t, left, depth - 1)
        draw_pythagoras_tree(t, right, depth - 1)

def main():
    # Настройка окна и черепахи
    screen = turtle.Screen()
    screen.title("Фрактал Пифагора")
    screen.bgcolor("white")
    screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.color("green")
    t.pensize(2)
    
    # Создаем начальный квадрат
    initial_square = Square(
        Point(-TREE_SIZE/2, TREE_OFFSET_Y + TREE_SIZE),  # верхняя левая
        Point(TREE_SIZE/2, TREE_OFFSET_Y + TREE_SIZE),   # верхняя правая
        Point(TREE_SIZE/2, TREE_OFFSET_Y),               # нижняя правая
        Point(-TREE_SIZE/2, TREE_OFFSET_Y)               # нижняя левая
    )
    
    # Рисуем фрактал
    draw_pythagoras_tree(t, initial_square, TREE_DEPTH)
    
    screen.mainloop()

if __name__ == "__main__":
    main() 