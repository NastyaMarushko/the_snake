import sys
from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (93, 216, 228)
BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = BLUE
WHITE = (255, 255, 255)

SNAKE_COLOR = GREEN
APPLE_COLOR = RED

START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс: позиция и цвет."""

    def __init__(self, position=START_POSITION, body_color=WHITE):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод."""
        error_msg = (
            f'Метод draw не реализован в классе {self.__class__.__name__}'
        )
        raise NotImplementedError(error_msg)

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку."""
        rect_color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, rect_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока. Наследуется от GameObject."""

    def __init__(self, occupied_positions=None, color=APPLE_COLOR):
        """Создает яблоко в случайной позиции."""
        super().__init__(body_color=color)
        positions_to_use = occupied_positions or []
        self.randomize_position(positions_to_use)

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в случайную свободную клетку."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки. Наследуется от GameObject."""

    def __init__(self, color=SNAKE_COLOR):
        """Змейка в центре поля с начальным размером 1"""
        super().__init__(body_color=color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет текущее направление движения."""
        if self.next_direction is not None:
            opposite_direction = (-self.direction[0], -self.direction[1])
            if opposite_direction != self.next_direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку, добавляя голову и удаляя хвост."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к изначальной."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def draw(self):
        """Отрисовывает все части тела змейки."""
        for position in self.positions:
            self.draw_cell(position)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш игроком."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        sys.exit()
    if keys[pg.K_UP] and snake.direction != DOWN:
        snake.next_direction = UP
    elif keys[pg.K_DOWN] and snake.direction != UP:
        snake.next_direction = DOWN
    elif keys[pg.K_LEFT] and snake.direction != RIGHT:
        snake.next_direction = LEFT
    elif keys[pg.K_RIGHT] and snake.direction != LEFT:
        snake.next_direction = RIGHT


def main():
    """Запускает игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
