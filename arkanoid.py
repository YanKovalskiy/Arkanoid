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


class Ball:
    def __init__(self, start_x, start_y):
        self.radius = 7
        self.x = start_x
        self.y = start_y - self.radius


    def move(self):
        pass


class Platform:
    def __init__(self):
        self.width = 64
        self.height = 16
        self.x = SCREEN_WIDTH // 2 - self.width
        self.y = SCREEN_HEIGHT - self.height - 1
        self.dx = 5
        self.direction = 'stop'

    def get_height(self):
        return self.height

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
        self.balls.append(Ball(self.platform.x + self.platform.width // 2, self.platform.y))

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

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.platform.direction = 'stop'

    def platform_handler(self):
        self.platform.move()
        self.graphic_processor.draw_platform(self.platform)

    def ball_handler(self, ball):
        ball.move()
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

            for ball in self.balls:
                self.ball_handler(ball)

            self.platform_handler()
            
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
