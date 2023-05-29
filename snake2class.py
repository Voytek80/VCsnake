import pygame
import random


class Snejk():
    def __init__(self):
        pygame.init()

        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        self.violet = (129, 29, 195)
        self.grey = (200, 200, 200)

        screen_resolution = pygame.display.Info()
        screen_width = screen_resolution.current_w
        screen_height = screen_resolution.current_h

        self.dis_width = screen_width
        self.dis_height = screen_height
        self.exit_game = False

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Snake')

        self.clock = pygame.time.Clock()
        self.local_direction = 1
        self.global_direction = 1
        self.once_more = False

        self.snake_block = round(self.dis_width / 50)
        self.food_block = 100
        self.snake_speed = 60
        self.font_style = pygame.font.SysFont("Chalkboard", 35)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        self.fruits_img = []
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/greenapple100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/kiwi100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/lemon100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/melon100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/orange100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/paprika100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/pumpkin100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/redapple100.png").convert_alpha())
        self.fruits_img.append(pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/food/tomato100.png").convert_alpha())

        self.background_img = pygame.image.load("/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/background.jpg")
        self.trap_img = pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/trap100.png").convert_alpha()
        self.traps = []
        self.head_top_img = pygame.image.load(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/images/head_top26.png").convert_alpha()
        self.head_rect = self.head_top_img.get_rect()
        self.food_rect = self.fruits_img[0].get_rect()

        self.ran = 7
        self.game_close = False

        self.eat_sound = pygame.mixer.Sound("/Users/Voytek/Desktop/Programming/Python/keras_mfcc/Audio11025/game_sounds/munch.wav")
        self.ouch_sound = pygame.mixer.Sound(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/Audio11025/game_sounds/Ouche.wav")
        self.music = pygame.mixer.Sound(
            "/Users/Voytek/Desktop/Programming/Python/keras_mfcc/Audio11025/game_sounds/music/music1.wav")

        pygame.mouse.set_visible(False)

    def food_position(self):
        self.food_rect.x = round(random.randrange(0, self.dis_width - 100))
        self.food_rect.y = round(random.randrange(0, self.dis_height - 64))
        while self.food_rect.collidelist(self.traps) >= 0:
            self.food_rect.x = round(random.randrange(0, self.dis_width - 100))
            self.food_rect.y = round(random.randrange(0, self.dis_height - 64))

    def food(self):
        self.dis.blit(self.fruits_img[self.ran], self.food_rect)

    def traps_position(self):
        self.traps[-1].x = round(random.randrange(0, self.dis_width - 100))
        self.traps[-1].y = round(random.randrange(0, self.dis_height - 64))
        while self.food_rect.colliderect(self.traps[-1]) or (self.traps[-1].collidelist(self.traps[:-1]) >= 0):
            self.traps[-1].x = round(random.randrange(0, self.dis_width - 100))
            self.traps[-1].y = round(random.randrange(0, self.dis_height - 64))

    def put_traps(self, traps_list):
        for x in traps_list:
            self.dis.blit(self.trap_img, x)

    def head(self, x, y, direction):
        self.head_rect.center = (x, y)
        if direction == 0:
            self.dis.blit(pygame.transform.rotate(self.head_top_img, 180), self.head_rect)
        if direction == 1:
            self.dis.blit(self.head_top_img, self.head_rect)
        if direction == 3:
            self.dis.blit(pygame.transform.rotate(self.head_top_img, 90), self.head_rect)
        if direction == 4:
            self.dis.blit(pygame.transform.rotate(self.head_top_img, 270), self.head_rect)

    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for i, x in enumerate(snake_list):
            if (i % 10) == 0:
                pygame.draw.circle(self.dis, self.grey, (x[0], x[1]), snake_block / 2)
            else:
                pygame.draw.circle(self.dis, self.black, (x[0], x[1]), snake_block/2)


    def message(self, color):
        mesg1 = self.font_style.render("Powiedz: ", True, color)
        mesg2 = self.font_style.render('"Koniec" - aby zakończyć', True, color)
        mesg3 = self.font_style.render('"Jeszcze raz" - aby zagrać', True, color)

        self.dis.blit(mesg1, [self.dis_width / 5 * 2 + 70, self.dis_height / 3])
        self.dis.blit(mesg2, [self.dis_width / 5 * 2 - 60, self.dis_height / 3 + 50])
        self.dis.blit(mesg3, [self.dis_width / 5 * 2 - 60, self.dis_height / 3 + 100])

    def gameLoop(self):
        pygame.mixer.Sound.play(self.music, -1)
        game_over = False
        self.game_close = False
        self.once_more = False

        x1 = round(self.dis_width / 2 / self.snake_block) * self.snake_block
        y1 = round(self.dis_height / 2 / self.snake_block) * self.snake_block

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 50
        score = 0

        self.traps = []
        self.traps.append(self.trap_img.get_rect())

        self.food_rect.x = round(random.randrange(0, self.dis_width - 100))
        self.food_rect.y = round(random.randrange(0, self.dis_height - 100))
        self.traps_position()

        while not game_over:

            while self.game_close == True:

                pygame.mixer.Sound.stop(self.music)

                self.dis.blit(self.background_img, (0, 0))
                self.message(self.red)
                self.Your_score(score)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.exit_game = True
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_p:
                            self.global_direction = 0
                            self.local_direction = 0
                            self.gameLoop()
                if self.exit_game == True:
                    pygame.quit()
                    exit()
                if self.once_more:
                    self.global_direction = 0
                    self.local_direction = 0
                    self.gameLoop()
                pygame.time.wait(100)

            if self.global_direction == 0 and self.local_direction != 1:
                y1_change = 1
                x1_change = 0
                self.local_direction = 0
            elif self.global_direction == 1 and self.local_direction != 0:
                y1_change = -1
                x1_change = 0
                self.local_direction = 1
            elif self.global_direction == 3 and self.local_direction != 4:
                x1_change = -1
                y1_change = 0
                self.local_direction = 3
            elif self.global_direction == 4 and self.local_direction != 3:
                x1_change = 1
                y1_change = 0
                self.local_direction = 4

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                self.game_close = True

            if x1 >= self.dis_width + self.snake_block / 2:
                x1 = -x1_change
            elif x1 < 0 - self.snake_block / 2:
                x1 = self.dis_width
            if y1 >= self.dis_height + self.snake_block / 2:
                y1 = -y1_change
            elif y1 < 0 - self.snake_block / 2:
                y1 = self.dis_height
            x1 += x1_change
            y1 += y1_change

            self.dis.blit(self.background_img, (0, 0))

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    self.game_close = True

            self.our_snake(self.snake_block, snake_List)
            self.Your_score(score)
            self.food()
            self.put_traps(self.traps)
            self.head(snake_List[-1][0], snake_List[-1][1], self.local_direction)
            pygame.display.update()

            if self.food_rect.colliderect(self.head_rect):
                pygame.mixer.Sound.play(self.eat_sound)
                self.ran = random.randrange(0, 8)
                self.food_position()
                self.traps.append(self.trap_img.get_rect())
                self.traps_position()
                Length_of_snake += self.snake_block
                score += 1

            if self.head_rect.collidelist(self.traps) >= 0:
                pygame.mixer.Sound.play(self.ouch_sound)
                self.game_close = True

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()
