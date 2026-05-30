from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс: позиция и цвет."""

    def __init__(self):
        """Инициализирует объект в центре экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (255, 255, 255)

    def draw(self):
        """Метод для рисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока. Наследуется от GameObject."""

    def __init__(self):
        """Яблоко со случайной позицией и красным цветом."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Перемещает яблоко в случайную клетку игрового поля."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Яблоко на экране в виде квадрата с рамкой."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки. Наследуется от GameObject."""

    def __init__(self):
        """Создает змейку в центре поля."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]

        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление, если новое не противоположно текущему."""
        if self.next_direction is not None:
            # Разбиваем длинную строку на две для соответствия PEP 8
            new_x = self.direction[0] * -1
            new_y = self.direction[1] * -1
            opposite_direction = (new_x, new_y)

            if opposite_direction != self.next_direction:
                self.direction = self.next_direction

            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении.
        Реализован проход сквозь границы поля.
        """
        head_x, head_y = self.get_head_position()

        dx, dy = self.direction
        new_x = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH)
        new_y = ((head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            pass

    def reset(self):
        """Сбрасывает змейку к изначальной из-за столкновения с собой."""
        center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center_pos]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def draw(self):
        """Отрисовывает все части змейки и очищает клетку удаленной части."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            pygame.draw.rect(screen, BORDER_COLOR, last_rect, 1)


def handle_keys(snake):
    """Обрабатывает действия игрока: нажатия стрелок и закрытие окна."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры. Запуск игровго процесса."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
