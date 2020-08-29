import pygame
import random


game_state = 'game'

with open('best_result.txt', 'r') as filik:
    best_result = int(filik.read())

pygame.init()

width = 600
height = 600

height_of_info_panel = 50

window = pygame.display.set_mode((width, height + height_of_info_panel))
SIDE = 30

col_fruit = random.randint(0, width // SIDE - 1)
row_fruit = random.randint(0, height // SIDE - 1)

background_color = (10, 10, 0)
color = {
    'fruit': (255, 0, 100),
    'snake': (100, 200, 0),
    'head': (100, 255, 50),
    'text': (255, 255, 255),
    'info_panel': (0, 0, 0),
}

snake = [(0, 0), (1, 0), (2, 0)] # (row, col)
delta_row = 0
delta_col = 1
last_direction = (delta_row, delta_col)

count_of_skipped_frames = 0

cur_lvl = 1 # от 1 до количества элементов в dict_len_to_frames

# в словаре ключ текущая длинна змеи, а значение количество фремов, которые будем пропускать
dict_len_to_frames = {
    0: 15, # начальное количество пропускаемых фреймов
    5: 12, 
    10: 10, 
    15: 5, 
    20: 3, 
}
max_count_of_skipped_frames = dict_len_to_frames[0]

clock = pygame.time.Clock()
FPS = 60

sounds = {
    'eat': pygame.mixer.Sound('eat.wav'),
    'death': pygame.mixer.Sound('death.wav'),
}

font_type = 'Anonymous Pro B.ttf'
my_font = pygame.font.Font(font_type, 26)
info_panel_font = pygame.font.Font(font_type, 14)
restart_button_x = 50
restart_button_y = 250
restart_button_width = 200
restart_button_hight = 50

while True:
    pygame.draw.rect(window, background_color, (0, 0, width, height))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == 'death':
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (restart_button_x <= mouse_x <= restart_button_x + restart_button_width
                     and restart_button_y <= mouse_y <= restart_button_y + restart_button_hight):
                game_state = 'game'
                snake = [(0, 0), (1, 0), (2, 0)] # (row, col)
                delta_row = 0
                delta_col = 1
                last_direction = (delta_row, delta_col)
        if event.type == pygame.KEYDOWN and game_state == 'game':
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and last_direction[1] != -1:
                delta_col = 1
                delta_row = 0 
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and last_direction[1] != 1:
                delta_col = -1
                delta_row = 0 
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and last_direction[0] != -1:
                delta_col = 0
                delta_row = 1 
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and last_direction[0] != 1:
                delta_col = 0
                delta_row = -1
    if game_state == 'game': 
        count_of_skipped_frames += 1
        if count_of_skipped_frames == max_count_of_skipped_frames:
            count_of_skipped_frames = 0        
            snake.insert(0, (snake[0][0] + delta_row, snake[0][1] + delta_col))
            last_direction = (delta_row, delta_col)
            if snake[0] == (row_fruit, col_fruit):
                sounds['eat'].play()
                if len(snake) in dict_len_to_frames.keys():
                    max_count_of_skipped_frames = dict_len_to_frames[len(snake)]
                    cur_lvl += 1
                # возможно стоит переписать генерацию фрукта вне змеи
                while (row_fruit, col_fruit) in snake: 
                    col_fruit = random.randint(0, width // SIDE - 1)
                    row_fruit = random.randint(0, height // SIDE - 1)
            else:
                del(snake[-1])
        if snake[0][0] in (-1, height // SIDE) or snake[0][1] in (-1, width // SIDE):
            game_state = 'death_now'
            text_death_1 = my_font.render('Ты впечатался в стенку', 1, color['text'])
        elif snake[0] in snake[1:]:
            game_state = 'death_now'
            text_death_1 = my_font.render('Ты впечатался в себя', 1, color['text'])
        else:     
            for row, col in snake:
                pygame.draw.rect(window, color['snake'], (col * SIDE, row * SIDE, SIDE, SIDE))
            pygame.draw.rect(window, color['head'], (snake[0][1] * SIDE, snake[0][0] * SIDE, SIDE, SIDE))
            pygame.draw.rect(window, color['fruit'], (col_fruit * SIDE, row_fruit * SIDE, SIDE, SIDE))
    if game_state == 'death_now':
        sounds['death'].play()
        max_count_of_skipped_frames = dict_len_to_frames[0]
        cur_lvl = 1
        text_death_2 = my_font.render(f'Текущая длинна змеи: {len(snake)}', 1, color['text'])
        if len(snake) >= best_result:
            best_result = len(snake)
            with open('best_result.txt', 'w') as filik:
                filik.write(str(best_result))
            text_best = my_font.render(f'Это лучший результат!', 1, color['text'])
        else:
            text_best = my_font.render(f'Лучший результат: {best_result}', 1, color['text'])
        text_restart = my_font.render('ЗАНОВО!', 1, color['text'])
        game_state = 'death'
    if game_state == 'death':
        window.blit(text_death_1, (50, 50))
        window.blit(text_death_2, (50, 100))
        window.blit(text_best, (50, 150))
        pygame.draw.rect(window, color['head'], (
                restart_button_x, restart_button_y, restart_button_width, restart_button_hight)
            )
        window.blit(text_restart, (restart_button_x + 45, restart_button_y + 15))
    elif game_state == 'pause':
        pass
    pygame.draw.rect(window, color['info_panel'], (0, height, width, height_of_info_panel))
    info_str = f'Длина змея: {len(snake):3}  Лучший результат: {best_result:3}  Текущий уровень: {cur_lvl:2}'
    info_panel_text = info_panel_font.render(info_str, 1, color['text'])
    window.blit(info_panel_text, (50, height + height_of_info_panel // 3))
    pygame.display.update()
    clock.tick(FPS)


# нужно добавить возможноcть менять количество фруктов
# нужна кнопка паузы игры
# таблица лидеров (имена? даты?)
# разобраться с запозданием звука?