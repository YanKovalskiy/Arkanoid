import pygame
from pygame.locals import Rect

from arkanoid_settings import *


class GraphicProcessor:
    def __init__(self, work_screen):
        self.screen = work_screen

    def prepare_work_screen(self, color):
        self.screen.fill(color)
        pygame.draw.rect(self.screen, FIRE_BRICK, (0, 0, SCREEN_WIDTH, INFO_PANEL_HEIGHT), 2)

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

    def _brick(self, brick, main_color, dark_color):
        pygame.draw.rect(self.screen, main_color, (brick.x, brick.y, brick.width, brick.height))
        pygame.draw.rect(self.screen, dark_color, (brick.x, brick.y, brick.width, brick.height), 1)

    def draw_brick(self, brick):
        if brick.hardness == 1:
            self._brick(brick, GREEN_YELLOW, DARK_GREEN)
        elif brick.hardness == 2:
            self._brick(brick, RED, DARK_RED)
        elif brick.hardness == 3:
            self._brick(brick, ROYAL_BLUE, DARK_BLUE)

    def draw_score(self, score):
        font = pygame.font.SysFont('Courier New', 36)
        score_text = font.render('SCORE : ' + str(score), 1, WHITE)
        self.screen.blit(score_text, (10, 5))


class Brick:
    def __init__(self, column_pos, line_pos, hardness):
        self.x = BRICK_WIDTH * column_pos
        self.y = INFO_PANEL_HEIGHT + TOP_INDENT + BRICK_HEIGHT * line_pos
        self.hardness = hardness
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT


class Ball:
    def __init__(self, x, y, on_platform):
        self.on_platform = on_platform
        self.radius = 7
        self.x = x
        if self.on_platform:
            self.y = y - self.radius
        else:
            self.y = y
        self.dx = 4
        self.dy = -4

    def move(self):
        """

        :return: bool True - out of screen, False - else
         """
        if self.x + self.dx > SCREEN_WIDTH - self.radius or self.x + self.dx < self.radius:
            self.dx = -self.dx
        self.x += self.dx

        if self.y + self.dy - INFO_PANEL_HEIGHT < self.radius:
            self.dy = -self.dy
        self.y += self.dy

        if self.y + self.dy > SCREEN_HEIGHT:
            return True
        else:
            return False

    def move_with_platform(self, platform):
        self.x = platform.x + platform.width // 2
        self.y = platform.y - self.radius

    def set_ball_initial_position(self, x, y, on_platform):
        self.x = x
        self.y = y
        self.on_platform = on_platform

    def object_collision(self, game_object):
        collision = False
        side_square = 2 * self.radius / 2 ** 0.5
        ball_rect = Rect(self.x, self.y, side_square, side_square)
        game_object_rect = Rect(game_object.x, game_object.y, game_object.width, game_object.height)

        if isinstance(game_object, Platform):
            if pygame.Rect.colliderect(ball_rect, game_object_rect):
                collision = True
                self.dy = -self.dy
                if (game_object.x <= self.x <= game_object.x + game_object.width // 5 or
                        game_object.x + (game_object.width//5) * 4 <= self.x <= game_object.x + game_object.width):
                    self.dx = -self.dx

        if isinstance(game_object, Brick):
            if game_object.hardness > 0:
                if pygame.Rect.colliderect(ball_rect, game_object_rect):
                    collision = True
                    self.dy = -self.dy
                    #self.dx = -self.dx

        return collision


class Platform:
    def __init__(self):
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width
        self.y = SCREEN_HEIGHT - self.height - 1
        self.dx = 7
        self.direction = 'stop'

    def move(self):
        if self.direction == 'left' and self.x >= self.dx:
            self.x -= self.dx
        elif self.direction == 'right' and self.x + self.width <= SCREEN_WIDTH - self.dx:
            self.x += self.dx


class InfoPanel:
    def __init__(self):
        self._score = 0

    def set_score(self, score):
        self._score += score
        pass

    def get_sore(self):
        return self._score


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
        self.info_panel = InfoPanel()

        for k, line in enumerate(self.level):
            for i, hardness in enumerate(self.level[k]):
                if hardness != 0:
                    self.bricks.append(Brick(i, k, hardness))

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
            if ball.move():
                ball.set_ball_initial_position(self.platform.x + self.platform.width // 2,
                                               self.platform.y, on_platform=True)

            ball.object_collision(self.platform)

            destroy_bricks = []
            for brick in self.bricks:
                if ball.object_collision(brick):
                    self.info_panel.set_score(10)
                    brick.hardness -= 1
                    if brick.hardness == 0:
                        destroy_bricks.append(brick)

            for brick in destroy_bricks:
                self.bricks.remove(brick)

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
            self.graphic_processor.prepare_work_screen(BLACK)

            self.platform_handler()

            for ball in self.balls:
                self.ball_handler(ball)

            for brick in self.bricks:
                self.graphic_processor.draw_brick(brick)

            self.graphic_processor.draw_score(self.info_panel.get_sore())

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
