import pygame

from arkanoid_settings import *


class GraphicProcessor:
    def __init__(self, work_screen):
        self.screen = work_screen

    def fill_work_screen(self, color):
        self.screen.fill(color)

    def draw_platform(self, platform):
        radius = platform.height // 2

        circle_coord_x = platform.x + radius
        circle_coord_y = platform.y + radius
        pygame.draw.circle(self.screen, FIRE_BRICK, (circle_coord_x, circle_coord_y), radius)

        circle_coord_x = platform.x + platform.width-radius
        pygame.draw.circle(self.screen, FIRE_BRICK, (circle_coord_x, circle_coord_y), radius)

        pygame.draw.rect(self.screen, SILVER, (platform.x+radius,
                                               platform.y,
                                               platform.width - radius*2,
                                               platform.height)
                         )
        pygame.draw.rect(self.screen, WHITE, (platform.x + radius,
                                              platform.y + 2,
                                              platform.width - radius*2,
                                              2)
                         )

    def draw_ball(self, ball):
        x = ball.x
        y = ball.y
        radius = ball.radius
        pygame.draw.circle(self.screen, SILVER, (x, y), radius)
        pygame.draw.circle(self.screen, WHITE, (x - radius // 2, y - radius // 2), radius // 2)

    def draw_brick(self, brick):
        if brick.hardness != 0:
            pygame.draw.rect(self.screen, WHITE, (brick.x, brick.y, BRICK_WIDTH, BRICK_HEIGHT), 1)


class Brick:
    def __init__(self, x, y, hardness):
        self.x = x
        self.y = y
        self.hardness = hardness


class Ball:
    def __init__(self, x, y, on_platform):
        self.on_platform = on_platform
        self.radius = 7
        self.x = x
        if self.on_platform:
            self.y = y - self.radius
        else:
            self.y = y
        self.dx = 5
        self.dy = -5

    def move(self):
        if self.x + self.dx > SCREEN_WIDTH - self.radius or self.x + self.dx < self.radius:
            self.dx = -self.dx
        self.x += self.dx

        if self.y + self.dy > SCREEN_HEIGHT - self.radius or self.y + self.dy < self.radius:
            self.dy = -self.dy
        self.y += self.dy

    def move_with_platform(self, platform):
        self.x = platform.x + platform.width // 2
        self.y = platform.y - self.radius

    def platform_collision(self, platform):
        if not self.on_platform:
            if platform.x <= self.x <= platform.x + platform.width:
                if self.y + self.radius >= platform.y:
                    self.dy = -self.dy


class Platform:
    def __init__(self):
        self.width = 64
        self.height = 16
        self.x = SCREEN_WIDTH // 2 - self.width
        self.y = SCREEN_HEIGHT - self.height - 1
        self.dx = 5
        self.direction = 'stop'

    def move(self):
        if self.direction == 'left' and self.x >= self.dx:
            self.x -= self.dx
        elif self.direction == 'right' and self.x + self.width <= SCREEN_WIDTH - self.dx:
            self.x += self.dx


class GameLevelHandler:
    def __init__(self, work_screen):
        self.end_game = False
        self.clock = pygame.time.Clock()
        self.graphic_processor = GraphicProcessor(work_screen)
        self.platform = Platform()
        self.balls = []
        self.balls.append(Ball(self.platform.x + self.platform.width // 2, self.platform.y, on_platform=True))
        self.level = LEVEL_01
        self.bricks = []

        for k, line in enumerate(self.level):
            for i, hardness in enumerate(self.level[k]):
                self.bricks.append(Brick(BRICK_WIDTH*i, TOP_INDENT + BRICK_HEIGHT*k, hardness))

    def event_handler(self):
        """ Обработка событий окна.
         :return: None
         """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game = True
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.platform.direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.platform.direction = 'right'
                elif event.key == pygame.K_ESCAPE:
                    self.end_game = True
                elif event.key == pygame.K_SPACE:
                    for ball in self.balls:
                        ball.on_platform = False

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.platform.direction = 'stop'

    def platform_handler(self):
        self.platform.move()
        self.graphic_processor.draw_platform(self.platform)

    def ball_handler(self, ball):
        if ball.on_platform:
            ball.move_with_platform(self.platform)
        else:
            ball.move()
            ball.platform_collision(self.platform)
        self.graphic_processor.draw_ball(ball)

    def main_loop(self):
        """

        :rtype: bool
        """
        while not self.end_game:
            # Частота обновления экрана
            self.clock.tick(FPS)
            # Обработка событий
            self.event_handler()
            self.graphic_processor.fill_work_screen(BLACK)

            self.platform_handler()

            for ball in self.balls:
                self.ball_handler(ball)

            for brick in self.bricks:
                self.graphic_processor.draw_brick(brick)

            pygame.display.flip()

        return self.end_game


def main():
    pygame.init()
    pygame.display.set_caption(SCREEN_TITLE)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    game_over = False
    while not game_over:
        level = GameLevelHandler(screen)
        game_over = level.main_loop()

    pygame.quit()


if __name__ == '__main__':
    main()
