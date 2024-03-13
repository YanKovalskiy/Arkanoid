import random
import time
from random import choice

import pygame
from pygame.locals import Rect

from arkanoid_settings import *


class SoundProcessor:
    def __init__(self):
        self.hit_platform = pygame.mixer.Sound('sounds/hit_platform.ogg')
        self.hit_platform.set_volume(0.2)
        self.ball_out_of_screen = pygame.mixer.Sound('sounds/ball_out.ogg')
        self.ball_out_of_screen.set_volume(0.3)
        self.expand_platform = pygame.mixer.Sound('sounds/extend_panel.ogg')
        self.expand_platform.set_volume(0.5)
        self.hit_brick_hardness_1 = pygame.mixer.Sound('sounds/hit_brick_1.ogg')
        self.hit_brick_hardness_1.set_volume(0.1)
        self.hit_brick_hardness_2 = pygame.mixer.Sound('sounds/hit_brick_2.ogg')
        self.hit_brick_hardness_2.set_volume(0.1)
        self.hit_brick_hardness_3 = pygame.mixer.Sound('sounds/hit_brick_3.ogg')
        self.hit_brick_hardness_3.set_volume(0.1)
        self.get_bonus_point = pygame.mixer.Sound('sounds/get_bonus_point.ogg')
        self.get_bonus_point.set_volume(0.1)
        self.laser_shot = pygame.mixer.Sound('sounds/laser-shot.ogg')
        self.laser_shot.set_volume(0.1)
        self.game_over = pygame.mixer.Sound('sounds/game_over.ogg')
        self.laser_shot.set_volume(0.1)

    def play_hit_platform(self):
        self.hit_platform.play()

    def play_ball_out(self):
        self.ball_out_of_screen.play()

    def play_expand_platform(self):
        self.expand_platform.play()

    def play_get_bonus_point(self):
        self.get_bonus_point.play()

    def play_laser_shot(self, extra_repetition=0):
        self.laser_shot.play(loops=extra_repetition)

    def play_game_over(self):
        self.game_over.play()

    def play_hit_brick(self, hardness):
        if hardness == 1:
            self.hit_brick_hardness_1.play()
        elif hardness == 2:
            self.hit_brick_hardness_2.play()
        elif hardness == 3:
            self.hit_brick_hardness_3.play()


class GraphicProcessor:
    def __init__(self, work_screen):
        self.screen = work_screen

    def prepare_work_screen(self, color):
        self.screen.fill(color)
        pygame.draw.rect(self.screen, SILVER, (0, 0, SCREEN_WIDTH, INFO_PANEL_HEIGHT))

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
        if platform.laser:
            pygame.draw.line(self.screen,
                             SILVER,
                             (platform.x+radius, platform.y),
                             (platform.x+radius, platform.y - 3),
                             2)

            pygame.draw.line(self.screen,
                             SILVER,
                             (platform.x + platform.width - radius - 2, platform.y),
                             (platform.x + platform.width - radius - 2, platform.y - 3),
                             2)

    def draw_power_bonus(self, bonus):
        pygame.draw.rect(self.screen, LIME_GREEN, (bonus.x, bonus.y, bonus.width, bonus.height), border_radius=4)
        pygame.draw.rect(self.screen, GREEN_YELLOW, (bonus.x + 2, bonus.y + 3, bonus.width - 4, 3), border_radius=60)
        font = pygame.font.SysFont('System', bold=True, size=18)
        symbol_type = font.render(bonus.power_type, 1, RED)
        self.screen.blit(symbol_type, (bonus.x + bonus.width // 2 - 4, bonus.y + 2))

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

    def draw_laser_ray(self, laser_ray):
        pygame.draw.line(self.screen, WHITE, [laser_ray.x, laser_ray.y], [laser_ray.x, laser_ray.y + 3], 2)

    def draw_info_panel(self, score, player_lives):
        font = pygame.font.SysFont('Courier New', bold=True, size=20)
        score_text = font.render('SCORE : ' + str(score), 1, BLACK)
        self.screen.blit(score_text, (10, 4))
        lives_text = font.render('LIVE : ' + str(player_lives), 1, BLACK)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 110, 4))

    def show_screensaver(self, info_text):
        screensaver = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screensaver.fill(BLACK)
        screensaver.set_alpha(200)
        self.screen.blit(screensaver, (0, 0))
        font = pygame.font.SysFont('System', bold=False, size=72)
        text = font.render(info_text, 1, RED)
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.update()


class PowerBonus:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 16
        self.dy = 2
        self.power_type = power_type

    def move(self):
        if self.y + self.height <= SCREEN_HEIGHT + self.height:
            self.y += self.dy


class Brick:
    @staticmethod
    def get_x(column_pos):
        return BRICK_WIDTH * column_pos

    @staticmethod
    def get_y(line_pos):
        return INFO_PANEL_HEIGHT + TOP_INDENT + BRICK_HEIGHT * line_pos

    def __init__(self, column_pos, line_pos, hardness):
        self.x = self.get_x(column_pos)
        self.y = self.get_y(line_pos)
        self.hardness = hardness
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT


class LaserRay:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 2
        self.height = 3
        self.dy = 10

    def move(self):
        self.y -= self.dy


class Ball:
    @staticmethod
    def get_y(y, radius, on_platform):
        if on_platform:
            y = y - radius
        return y

    def __init__(self, x, y, on_platform):
        self.on_platform = on_platform
        self.radius = 7
        self.x = x
        self.y = self.get_y(y, self.radius, self.on_platform)
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


class Platform:
    @staticmethod
    def get_x(width):
        return SCREEN_WIDTH // 2 - width

    @staticmethod
    def get_y(height):
        return SCREEN_HEIGHT - height - 1

    def __init__(self):
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.x = self.get_x(self.width)
        self.y = self.get_y(self.height)
        self.dx = 7
        self.direction = 'stop'
        self.laser = False
        self.laser_fire = False
        self.fire_delay = LASER_FIRE_DELAY
        self.power_bonuses = set()

    def move(self):
        if self.direction == 'left' and self.x >= self.dx:
            self.x -= self.dx
        elif self.direction == 'right' and self.x + self.width <= SCREEN_WIDTH - self.dx:
            self.x += self.dx

    def fire_from_laser(self, laser_rays, sound):
        if self.laser_fire:
            if self.fire_delay == 0:
                y = self.y + 3
                #  Left laser fire
                x = self.x + self.height // 2
                laser_rays.append(LaserRay(x, y))
                #  Right laser fire
                x = self.x + self.width - self.height // 2
                laser_rays.append(LaserRay(x, y))
                sound.play_laser_shot()
                self.fire_delay = LASER_FIRE_DELAY
            else:
                self.fire_delay -= 1

    def handler(self, laser_rays, graphic_processor, sound):
        self.move()
        self.fire_from_laser(laser_rays, sound)
        graphic_processor.draw_platform(self)


class InfoPanel:
    def __init__(self):
        self._score = 0
        self._player_lives = NUMBER_PLAYER_LIVES

    def set_score(self, score):
        self._score += score
        pass

    def get_score(self):
        return self._score

    def set_player_lives(self, lives):
        self._player_lives = lives

    def get_player_lives(self):
        return self._player_lives


class GameLevelHandler:
    def __init__(self, graphic: GraphicProcessor, sound: SoundProcessor, info_panel: InfoPanel, level_drawing):
        self.EXPAND_PLATFORM = 'E'
        self.ADD_BALLS = 'B'
        self.ADD_LASERS = 'L'
        self.end_game = False
        self.type_end_game = ''
        self.clock = pygame.time.Clock()
        self.graphic_processor = graphic
        self.sound = sound
        self.platform = Platform()
        self.info_panel = info_panel
        self.laser_rays = []
        self.balls = []
        self.balls.append(Ball(self.platform.x + self.platform.width // 2, self.platform.y, on_platform=True))
        self.level = level_drawing
        self.power_bonuses = []

        self.bricks = []
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
                self.type_end_game = EXIT
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.platform.direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.platform.direction = 'right'
                elif event.key == pygame.K_ESCAPE:
                    self.end_game = True
                    self.type_end_game = EXIT
                    break
                elif event.key == pygame.K_SPACE:
                    for ball in self.balls:
                        ball.on_platform = False
                    if self.platform.laser:
                        self.platform.laser_fire = True

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.platform.direction = 'stop'
                elif event.key == pygame.K_SPACE:
                    self.platform.laser_fire = False



    def power_bonus_handler(self, power_bonus):
        power_bonus.move()

        if object_collision(self.platform, power_bonus):
            if power_bonus.power_type not in self.platform.power_bonuses:
                self.platform.power_bonuses.add(power_bonus.power_type)

                if power_bonus.power_type == self.EXPAND_PLATFORM:
                    self.sound.play_expand_platform()
                    self.platform.width = self.platform.width * 2

                if power_bonus.power_type == self.ADD_BALLS:
                    if self.balls:
                        ball = self.balls[0]
                        add_ball = Ball(ball.x, ball.y, on_platform=False)
                        add_ball.dx = -ball.dx
                        self.balls.append(add_ball)
                        add_ball = Ball(ball.x, ball.y, on_platform=False)
                        add_ball.dy = -ball.dy
                        self.balls.append(add_ball)
                    else:
                        self.balls.append(Ball(self.platform.x + self.platform.width // 2,
                                               self.platform.y, on_platform=True))
                        self.balls.append(Ball(self.platform.x + self.platform.width // 2,
                                               self.platform.y, on_platform=True))

                if power_bonus.power_type == self.ADD_LASERS:
                    self.sound.play_laser_shot()
                    self.platform.laser = True
            else:
                self.sound.play_get_bonus_point()
                self.info_panel.set_score(100)
            self.power_bonuses.remove(power_bonus)
        else:
            if power_bonus.x > SCREEN_HEIGHT:
                self.power_bonuses.remove(power_bonus)
            else:
                self.graphic_processor.draw_power_bonus(power_bonus)

    def create_bonus(self, bonus_x, bonus_y):
        if random.randint(1, 100) <= 10:  # 10%
            power_type = choice([self.EXPAND_PLATFORM, self.ADD_BALLS, self.ADD_LASERS])
            self.power_bonuses.append(PowerBonus(bonus_x, bonus_y, power_type))

    def ball_handler(self, ball):
        if ball.on_platform:
            ball.move_with_platform(self.platform)
        else:
            if ball.move():
                self.sound.play_ball_out()
                self.balls.remove(ball)
                if self.balls:
                    if len(self.balls) == 1 and self.ADD_BALLS in self.platform.power_bonuses:
                        self.platform.power_bonuses.remove(self.ADD_BALLS)
                else:
                    self.balls.append(Ball(self.platform.x + self.platform.width // 2,
                                           self.platform.y, on_platform=True))
                    self.info_panel.set_player_lives(self.info_panel.get_player_lives() - 1)

                    if self.EXPAND_PLATFORM in self.platform.power_bonuses:
                        self.platform.width = self.platform.width / 2

                    if self.ADD_LASERS in self.platform.power_bonuses:
                        self.platform.laser = False
                        self.platform.laser_fire = False

                    self.platform.power_bonuses.clear()
            else:
                if object_collision(ball, self.platform):
                    self.sound.play_hit_platform()
                    ball.dy = -ball.dy
                    if (self.platform.x <= ball.x <= self.platform.x + self.platform.width // 5 or
                            self.platform.x + (self.platform.width // 5) * 4 <= ball.x <= self.platform.x +
                            self.platform.width):
                        ball.dx = -ball.dx

                for brick in reversed(self.bricks):
                    if object_collision(ball, brick):
                        self.sound.play_hit_brick(brick.hardness)
                        self.info_panel.set_score(10)
                        self.create_bonus(brick.x, brick.y)

                        if brick.hardness > 0:
                            ball.dy = -ball.dy
                        brick.hardness -= 1

                        if brick.hardness == 0:
                            self.bricks.remove(brick)
                            if not self.bricks:
                                self.end_game = True
                                self.type_end_game = PASSED

        self.graphic_processor.draw_ball(ball)

    def laser_ray_handler(self, laser_ray):
        laser_ray.move()
        if laser_ray.y > INFO_PANEL_HEIGHT:
            for brick in reversed(self.bricks):
                if object_collision(laser_ray, brick):
                    self.sound.play_hit_brick(brick.hardness)
                    self.info_panel.set_score(10)
                    self.create_bonus(brick.x, brick.y)
                    brick.hardness -= 1
                    if brick.hardness == 0:
                        self.bricks.remove(brick)
                        if not self.bricks:
                            self.end_game = True
                            self.type_end_game = PASSED
                    self.laser_rays.remove(laser_ray)
                    break
            self.graphic_processor.draw_laser_ray(laser_ray)
        else:
            self.laser_rays.remove(laser_ray)

    def main_loop(self):
        """

        :rtype: bool
        """
        while not self.end_game:
            #  Frame rate to fps
            self.clock.tick(FPS)

            #  Test game over
            if self.info_panel.get_player_lives() == 0:
                self.end_game = True
                self.type_end_game = GAME_OVER

            #  Event handling
            self.event_handler()
            self.graphic_processor.prepare_work_screen(BLACK)

            self.platform.handler(self.laser_rays, self.graphic_processor, self.sound)

            for ball in self.balls:
                self.ball_handler(ball)

            for laser_ray in reversed(self.laser_rays):
                self.laser_ray_handler(laser_ray)

            for brick in self.bricks:
                self.graphic_processor.draw_brick(brick)

            for power_bonus in reversed(self.power_bonuses):
                self.power_bonus_handler(power_bonus)

            self.graphic_processor.draw_info_panel(self.info_panel.get_score(), self.info_panel.get_player_lives())

            pygame.display.flip()

        return self.type_end_game


def object_collision(game_object, test_game_object):
    if isinstance(game_object, Ball):
        game_object_width = game_object_height = game_object.radius
    else:
        game_object_width = game_object.width
        game_object_height = game_object.height

    game_object_rect = Rect(game_object.x,
                            game_object.y,
                            game_object_width,
                            game_object_height)

    test_game_object_rect = Rect(test_game_object.x,
                                 test_game_object.y,
                                 test_game_object.width,
                                 test_game_object.height)

    if pygame.Rect.colliderect(test_game_object_rect, game_object_rect):
        return True
    return False


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption(SCREEN_TITLE)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    sound = SoundProcessor()
    info = InfoPanel()
    graph = GraphicProcessor(screen)

    game_over = False
    type_ending = EXIT
    levels = (LEVEL_01, LEVEL_02, LEVEL_03)
    level_counter = 1
    while not game_over:
        level = GameLevelHandler(graph, sound, info, levels[level_counter - 1])
        type_ending = level.main_loop()
        if type_ending == EXIT:
            game_over = True
        elif type_ending == GAME_OVER:
            graph.show_screensaver('GAME OVER')
            sound.play_game_over()
            time.sleep(4)
            game_over = True
        elif type_ending == PASSED:
            info.set_player_lives(info.get_player_lives() + 1)
            info.set_score(1000)
            level_counter += 1
            if level_counter > len(levels):
                graph.show_screensaver('GAME COMPLETE')
                game_over = True
                type_ending = EXIT
            else:
                graph.show_screensaver('LEVEL IS COMPLETE')
            sound.play_get_bonus_point()
            time.sleep(3)

    if type_ending == GAME_OVER:
        main()

    pygame.quit()


if __name__ == '__main__':
    main()
