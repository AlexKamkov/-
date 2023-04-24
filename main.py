import pygame, random
from os import path


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False


def create_message(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [x, y])


pygame.init()
width = 800
height = 600
music_dir = path.join("C:/Users/admin/PycharmProjects/Змейка 2.0/", "Music")
img_dir = path.join("C:/Users/admin/PycharmProjects/Змейка 2.0/", "img")
green_1 = (50, 205, 50)
green_2 = (34, 139, 34)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
aqua = (0, 255, 255)
magenta = (138, 43, 226)
white = (255, 255, 255)
FPS = 5
snake_block = 30
snake_step = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


def gameloop():
    snake_list = []
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    length = 1
    i = 0
    game_close = False
    run = True
    # Добавление звука
    pygame.mixer.music.load(path.join(music_dir, "Intense.mp3"))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.3)
    yum = pygame.mixer.Sound(path.join(music_dir, "apple_bite.ogg"))
    yum.set_volume(0.4)
    hit = pygame.mixer.Sound(path.join(music_dir, "stop.flac"))
    hit.set_volume(0.4)
    # Добавление фона
    bg = pygame.image.load(path.join(img_dir, "Fon_grass4.jpg")).convert()
    bg = pygame.transform.scale(bg, (width, height))
    bg_rect = bg.get_rect()
    # Добавление еды
    foodx = random.randrange(0, width - snake_block)
    foody = random.randrange(0, height - snake_block)
    food_img = [pygame.image.load(path.join(img_dir, "f_1.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_2.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_4.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_5.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_7.png")).convert()]
    food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
    food.set_colorkey(white)
    # Отрисовка головы змейки
    head_image = [pygame.image.load(path.join(img_dir, "HeadR.png")).convert(),
                  pygame.image.load(path.join(img_dir, "HeadL.png")).convert(),
                  pygame.image.load(path.join(img_dir, "HeadB.png")).convert(),
                  pygame.image.load(path.join(img_dir, "HeadT.png")).convert()]
    while run:
        clock.tick(FPS)
        screen.fill(green_1)
        screen.blit(bg, bg_rect)
        # Счёт
        create_message(f"Score: {length - 1}", aqua, 5, 5, "Architun", 45)
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        # Создание еды
        food_rect = food.get_rect(x=foodx, y=foody)
        screen.blit(food, food_rect)
        # pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])
        if len(snake_list) > length:
            del snake_list[0]

        # Змейка
        for x in snake_list:
            snake_img = pygame.image.load(path.join(img_dir, "block.png")).convert()
            snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
            snake.set_colorkey(white)
            screen.blit(snake, (x[0], x[1]))
        pygame.display.update()
        pygame.display.flip()
        # Управление змейкой
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_step
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_step
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_step
        # Столкновение с границами окна
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            hit.play()
            game_close = True
        x1 += x1_change
        y1 += y1_change
        # Поедание еды
        if eating_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, width - snake_block)
            foody = random.randrange(0, height - snake_block)
            length += 1
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(white)
            yum.play()
        # Столкновение с самим собой
        for x in snake_list[:-1]:
            if x == snake_head:
                hit.play()
                game_close = True
        # Проигрыш
        while game_close:
            screen.fill(green_1)
            create_message("GAME OVER", white, 190, 200, "Architun", 100)
            create_message("Нажмите Q для выхода или C для повторной игры", white, 60, 300, "Arial", 35)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    if event.key == pygame.K_c:
                        gameloop()
            pygame.display.set_caption("Ты проиграл!")
    pygame.quit()


gameloop()
