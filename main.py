import configparser
import random
import pygame
import sys

pygame.init()

frame_size_x = 1000
frame_size_y = 720

main_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

now_screen = 'menu'

config = configparser.ConfigParser()
config.read('config/main.ini')

records_mass = [int(config['DEFAULT'][f'm{i}']) for i in range(1, 11)]

menu_buttons = [
    {
        'center_pos': [500, 200], 
        'img': pygame.image.load('images/Start_game.png'), 
        'img1': pygame.image.load('images/Start_game1.png'), 
        'click': False, 
    },
    {
        'center_pos': [500, 360],
        'img': pygame.image.load('images/Check_records.png'),
        'img1': pygame.image.load('images/Check_records1.png'),
        'click': False,
    },
    {
        'center_pos': [500, 520],
        'img': pygame.image.load('images/Exit.png'),
        'img1': pygame.image.load('images/Exit1.png'),
        'click': False,
    },
]


choice_buttons = [
    {
        'center_pos': [300, 350],
        'img': pygame.image.load('images/1player.png'),
        'img1': pygame.image.load('images/1player1.png'),
        'click': False,
    },
    {
        'center_pos': [700, 350],
        'img': pygame.image.load('images/2player.png'),
        'img1': pygame.image.load('images/2player1.png'),
        'click': False,
    },
]

game_buttons = [
    {
        'center_pos': [35, 35],
        'img': pygame.image.load('images/menu.png'),
        'img1': pygame.image.load('images/menu1.png'),
        'click': False,
    }
]

pause_buttons = [
    {
        'center_pos': [frame_size_x // 2 - 10, frame_size_y // 2 + 130],
        'img': pygame.image.load('images/menuV2.png'),
        'img1': pygame.image.load('images/menuV2-1.png'),
        'click': False,
    }
]

check_buttons = [
    {
        'center_pos': [750, frame_size_y // 2],
        'img': pygame.image.load('images/menuV2.png'),
        'img1': pygame.image.load('images/menuV2-1.png'),
        'click': False,
    }
]

records_font = pygame.font.Font('font/PixelifySans.ttf', 32)


cloud_img = pygame.image.load('images/cloud.png')
front_img = pygame.image.load('images/front.png')
pause_img = pygame.image.load('images/pause.png')
block_img = pygame.image.load('images/block.png')
lose_img = pygame.image.load('images/lose.png')

player1win_img = pygame.image.load('images/player1win.png')
player2win_img = pygame.image.load('images/player2win.png')

player1_img = pygame.image.load('images/red_ball.png')
player2_img = pygame.image.load('images/blue_ball.png')

blue_spike_img = pygame.image.load('images/blue_spike.png')


player1_pos = [250, frame_size_y - 100]
player2_pos = [700, frame_size_y - 100]

player1_jump = False
player2_jump = False

player_step_y1 = 0
player_step_y2 = 0

player_step_x = 5

spikes_in_line = 1

clouds_mass = []

objects_mass = [[block_img, [x, frame_size_y - 50]] for x in range(250, 750, 50)]

control_1pl = {
    'W': False,
    'A': False,
    'S': False,
    'D': False,
}

control_2pl = {
    'W': False,
    'A': False,
    'S': False,
    'D': False,
}

camera_y = - player1_pos[1]

game_pause = False
game_lose = False
game_lose1 = False
game_lose2 = False

for i in range(0, frame_size_x, 100):
    clouds_mass.append([i, random.randrange(frame_size_y - 100), random.randrange(1, 5)])


def add_record(record):
  
    global records_mass

    records_mass.append(int(record)) 
    records_mass.sort(reverse=True) 

    del records_mass[-1] 


def write_config():
    '''Записывает конфигурацию в файл.
    Эта функция обновляет настройки в конфигурационном файле, записывая значения из массива рекордов в секцию 'DEFAULT' файла конфигурации.

    :raises IOError: если возникает ошибка при открытии или записи в файл конфигурации.
    :raises KeyError: если ключи в массиве рекордов отсутствуют или неправильно заданы.
    :returns: None
    '''
    for i in range(1, 11):
        config['DEFAULT'][f'm{i}'] = str(records_mass[i - 1]) 

    with open('config/main.ini', 'w') as configfile:
        config.write(configfile)


def draw_background(screen):
    '''Записывает текущие записи в конфигурационный файл.
    Эта функция обновляет конфигурационный файл main.ini, записывая в него
    значения из глобального списка records_mass. Записи сохраняются в секции
    DEFAULT под ключами m1, m2, ..., m10.

    :returns: None
    :raises FileNotFoundError: если директория config не существует.
    :raises IOError: если произошла ошибка при записи в файл.'''
    screen.fill((0, 143, 223)) 

    for cloud_ind in range(len(clouds_mass)):
        clouds_mass[cloud_ind][0] += clouds_mass[cloud_ind][2] 

        if clouds_mass[cloud_ind][0] > frame_size_x: 
            clouds_mass[cloud_ind][0] = -100 

            clouds_mass[cloud_ind][1:] = [random.randrange(frame_size_y - 100), random.randrange(2, 7)] 

        screen.blit(cloud_img, clouds_mass[cloud_ind][:2]) 


def draw_menu_interface(screen):
    '''Отображает интерфейс меню на экране.
    Эта функция проходит по всем кнопкам меню и отображает их на переданном
    экране. Если кнопка была нажата, отображается её активное изображение, в
    противном случае — обычное изображение.

    :param screen: Экран, на который будут отрисованы кнопки.
    :type screen: pygame.Surface
    :returns: None
    :raises TypeError: если параметр screen не является объектом pygame.Surface.'''
    for button in menu_buttons: 
        if button['click']: 
            button_rect = button['img1'].get_rect() 
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect() 
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def check_menu_events(click_pos, have_click):
    '''Проверяет события меню на основе позиции клика и состояния клика.
    Эта функция обрабатывает события клика по кнопкам меню. Если клик произошел
    внутри границ кнопки, устанавливается состояние нажатия для соответствующей
    кнопки. В зависимости от нажатой кнопки изменяется текущий экран или
    завершается программа.

    :param click_pos: Позиция клика мыши в формате (x, y).
    :type click_pos: tuple
    :param have_click: Состояние клика (True, если клик был произведен).
    :type have_click: bool
    :returns: None
    :raises TypeError: если click_pos не является кортежем или have_click не является булевым значением.
    '''
    global menu_buttons, now_screen

    for button in menu_buttons: 
        if button['center_pos'][0] - 150 <= click_pos[0] <= button['center_pos'][0] + 150 and button['center_pos'][1] - 75 <= click_pos[1] <= button['center_pos'][1] + 75 and have_click: 
            button['click'] = True 

            if button == menu_buttons[0]:
                now_screen = 'choice'

            elif button == menu_buttons[1]:
                now_screen = 'records'

            else: 
                write_config() 

                pygame.quit()
                sys.exit()

        else:
            button['click'] = False 



def menu_screen(screen):
    '''Отображает экран меню и обрабатывает события.
    Эта функция отвечает за отображение экрана меню и обработку событий,
    таких как клики мышью. Она управляет состоянием экрана и обновляет
    интерфейс в зависимости от взаимодействия пользователя.

    :param screen: Объект экрана для отображения графики.
    :type screen: pygame.Surface
    :returns: None
    :raises SystemExit: если происходит выход из программы.'''
    global now_screen, menu_buttons

    fps_controller = pygame.time.Clock() 

    click = False 

    while now_screen == 'menu': 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                write_config() 

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                click = True 

            elif event.type == pygame.MOUSEBUTTONUP: 
                click = False 

        screen.fill((0, 143, 223)) 

        check_menu_events(pygame.mouse.get_pos(), click) 

        draw_background(screen) 
        draw_menu_interface(screen) 

        pygame.display.update()
        fps_controller.tick(90) 


def check_choice_events(click_pos, have_click):
    '''Обрабатывает события выбора кнопок (кол-ва игроков).
    Эта функция проверяет, были ли нажаты кнопки выбора на экране. 
    Если кнопка была нажата, она обновляет текущее состояние экрана 
    в зависимости от выбранной кнопки.

    :param click_pos: Позиция клика мыши в координатах (x, y).
    :type click_pos: tuple
    :param have_click: Флаг, указывающий, был ли клик.
    :type have_click: bool
    :raises ValueError: если переданы некорректные параметры.'''
    global choice_buttons, now_screen

    for button in choice_buttons:
        if button['center_pos'][0] - 150 <= click_pos[0] <= button['center_pos'][0] + 150 and button['center_pos'][1] - 75 <= click_pos[1] <= button['center_pos'][1] + 75 and have_click:
            button['click'] = True

            if button == choice_buttons[0]:
                now_screen = 'game1'

            else:
                now_screen = 'game2'


def draw_choice_interface(screen):
    '''Отрисовывает интерфейс выбора клавиш кол-ва игроков на экране.

    :param screen: Экран, на который будут рисоваться кнопки.
    :type screen: pygame.Surface
    :raises ValueError: если передан некорректный объект экрана.
    :returns: None'''
    for button in choice_buttons:
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def choice_screen(screen):
    '''Отображает экран выбора и обрабатывает события.
    Этот метод отвечает за отображение экрана выбора в игре. Он обрабатывает события мыши и обновляет экран, пока текущий экран равен 'choice'.

    :param screen: объект экрана Pygame, на котором будет отображаться интерфейс выбора.
    :type screen: pygame.Surface
    :raises SystemExit: если пользователь закрывает окно игры, вызывается выход из программы.
    :raises Exception: может возникнуть при неправильной инициализации Pygame или других непредвиденных обстоятельствах.
    :returns: None
    '''

    global now_screen

    fps_controller = pygame.time.Clock()

    click = False

    while now_screen == 'choice':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_config()

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            elif event.type == pygame.MOUSEBUTTONUP:
                click = False

        screen.fill((0, 143, 223))

        check_menu_events(pygame.mouse.get_pos(), click)
        check_choice_events(pygame.mouse.get_pos(), click)

        draw_background(screen)
        draw_choice_interface(screen)

        pygame.display.update()
        fps_controller.tick(90)


def create_lines(y):
    '''Создает линии и шипы на заданной высоте.
    Эта функция генерирует случайное количество линий и шипов 
    на заданной высоте y. Линии создаются с использованием 
    случайных координат по оси x, а шипы располагаются 
    в определенных позициях на той же высоте.

    :param y: Высота, на которой будут размещены линии и шипы.
    :type y: int
    :returns: None
    :raises Exception: может вызвать исключения, если объекты не могут быть добавлены в массив'''
    rnd_x = random.randrange(0, 10) 

    for cnt in range(rnd_x, rnd_x + random.randrange(3 , 6)): 
        objects_mass.append([block_img, [250 + (rnd_x * 50 + cnt * 50) % 500, y]]) 

    rnd_spikes = [random.randrange(250, 750, 50) for i in range(spikes_in_line)] 

    for rnd_x in rnd_spikes:
        objects_mass.append([blue_spike_img, [rnd_x, y - 50]]) 


def draw_game_1pl(screen):
    '''Отображает игру для одного игрока на заданном экране.
    Эта функция отвечает за отрисовку всех игровых объектов, 
    включая фон, игрока и элементы управления. Она обновляет 
    экран в зависимости от положения камеры и состояния игровых объектов.

    :param screen: Экран, на котором будут отрисованы объекты.
    :type screen: Surface
    :returns: None
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    while objects_mass[0][1][1] + camera_y > frame_size_y: 
        del objects_mass[0]

    ind = 0

    while objects_mass[ind][1][1] + camera_y > 0: 
        screen.blit(objects_mass[ind][0], [objects_mass[ind][1][0], objects_mass[ind][1][1] + camera_y])

        ind += 1

    screen.blit(player1_img, [player1_pos[0], player1_pos[1] + camera_y]) 

    screen.blit(front_img, [0, 0]) 

    for button in game_buttons: 
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def control_1():
    '''Обрабатывает управление игроком 1.
    Эта функция отвечает за управление движением игрока 1, включая 
    прыжки и перемещение влево и вправо. Она проверяет столкновения 
    с игровыми объектами и обновляет положение игрока в зависимости 
    от состояния управления.

    :returns: None
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    global player1_jump, player1_pos, player_step_y1

    if player1_jump: 
        player_step_y1 += 0.1 

    else: 
        player1_points = [[player1_pos[0] + 6, player1_pos[1] + 50 + player_step_y1], [player1_pos[0] + 44, player1_pos[1] + 50 + player_step_y1]] 

        flag = 0

        for point in player1_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50: 
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50: 
                    flag += 1 
                    break

        if flag == 0: 
            player1_jump = True

    if control_1pl['W']: 
        if not player1_jump: 
            player_step_y1 += -8

        player1_jump = True 

    if control_1pl['A']:
        player1_points = [[player1_pos[0] - player_step_x, player1_pos[1] + 6], [player1_pos[0] - player_step_x, player1_pos[1] + 44]] 
        flag = False 
        x_block = 0

        for point in player1_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50: 
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50: 
                    flag = True 
                    x_block = elem[1][0] + 50 
                    break

        if flag: 
            player1_pos[0] = x_block 

        else:
            player1_pos[0] -= player_step_x 

    if control_1pl['D']: 
        player1_points = [[player1_pos[0] + 50 + player_step_x, player1_pos[1] + 6], [player1_pos[0] + 50 + player_step_x, player1_pos[1] + 44]] 
        flag = False 
        x_block = 0

        for point in player1_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50: 
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50: 
                    flag = True 
                    x_block = elem[1][0] - 50 
                    break

        if flag:  
            player1_pos[0] = x_block 

        else:
            player1_pos[0] += player_step_x 

    if player_step_y1 >= 0: 
        player1_points = [[player1_pos[0] + 6, player1_pos[1] + 50 + player_step_y1], [player1_pos[0] + 44, player1_pos[1] + 50 + player_step_y1]] 

        for point in player1_points: 
            flag = False 
            y_block = 0

            for elem in objects_mass:
                if elem[1][1] + camera_y < 50: 
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50: 
                    flag = True 
                    y_block = elem[1][1] - 50 
                    break

            if flag: 
                player1_jump = False 
                player_step_y1 = 0
                player1_pos[1] = y_block 

    else: 
        player1_points = [[player1_pos[0] + 6, player1_pos[1] + player_step_y1],
                          [player1_pos[0] + 44, player1_pos[1] + player_step_y1]] 

        for point in player1_points: 
            flag = False 

            for elem in objects_mass:
                if elem[1][1] + camera_y < 50: 
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50: 
                    flag = True 
                    break

            if flag: 
                player_step_y1 = 0 

    player1_pos[1] += player_step_y1 



def control_2():
    '''Обрабатывает управление игроком 2.
    Эта функция отвечает за управление движением игрока 2, включая 
    прыжки и перемещение влево и вправо. Она проверяет столкновения 
    с игровыми объектами и обновляет положение игрока в зависимости 
    от состояния управления.

    :returns: None
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    global player2_jump, player2_pos, player_step_y2

    if player2_jump:
        player_step_y2 += 0.1

    else:
        player2_points = [[player2_pos[0] + 6, player2_pos[1] + 50 + player_step_y2], [player2_pos[0] + 44, player2_pos[1] + 50 + player_step_y2]]

        flag = 0

        for point in player2_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50:
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50:
                    flag += 1
                    break

        if flag == 0:
            player2_jump = True

    if control_2pl['W']:
        if not player2_jump:
            player_step_y2 += -8

        player2_jump = True

    if control_2pl['A']:
        player2_points = [[player2_pos[0] - player_step_x, player2_pos[1] + 6], [player2_pos[0] - player_step_x, player2_pos[1] + 44]]
        flag = False
        x_block = 0

        for point in player2_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50:
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50:
                    flag = True
                    x_block = elem[1][0] + 50
                    break

        if flag:
            player2_pos[0] = x_block

        else:
            player2_pos[0] -= player_step_x

    if control_2pl['D']:
        player2_points = [[player2_pos[0] + 50 + player_step_x, player2_pos[1] + 6], [player2_pos[0] + 50 + player_step_x, player2_pos[1] + 44]]
        flag = False
        x_block = 0

        for point in player2_points:
            for elem in objects_mass:
                if elem[1][1] + camera_y < 50:
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50:
                    flag = True
                    x_block = elem[1][0] - 50
                    break

        if flag:
            player2_pos[0] = x_block
            pass

        else:
            player2_pos[0] += player_step_x

    if player_step_y2 >= 0:
        player2_points = [[player2_pos[0] + 6, player2_pos[1] + 50 + player_step_y2], [player2_pos[0] + 44, player2_pos[1] + 50 + player_step_y2]]

        for point in player2_points:
            flag = False
            y_block = 0

            for elem in objects_mass:
                if elem[1][1] + camera_y < 50:
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50:
                    flag = True
                    y_block = elem[1][1] - 50
                    break

            if flag:
                player2_jump = False
                player_step_y2 = 0
                player2_pos[1] = y_block

    else:
        player2_points = [[player2_pos[0] + 6, player2_pos[1] + player_step_y2],
                          [player2_pos[0] + 44, player2_pos[1] + player_step_y2]]

        for point in player2_points:
            flag = False

            for elem in objects_mass:
                if elem[1][1] + camera_y < 50:
                    break

                if elem[0] == block_img and elem[1][0] <= point[0] <= elem[1][0] + 50 and elem[1][1] <= point[1] <= elem[1][1] + 50:
                    flag = True
                    break

            if flag:
                player_step_y2 = 0

    player2_pos[1] += player_step_y2



def check_lose():
    '''Проверяет, проиграл ли игрок.
    Эта функция проверяет, столкнулся ли игрок с шипами или вышел за пределы игрового поля.
    Если одно из условий выполняется, устанавливает глобальную переменную game_lose в True.

    :returns: None
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    global game_lose

    player1_points = [[player1_pos[0] + 1, player1_pos[1] + 1], [player1_pos[0] + 49, player1_pos[1] + 1], [player1_pos[0] + 1, player1_pos[1] + 49], [player1_pos[0] + 49, player1_pos[1] + 1]] 

    for point in player1_points: 
        for elem in objects_mass: 
            if elem[1][1] + camera_y < 50: 
                break

            if elem[0] == blue_spike_img and elem[1][0] < point[0] < elem[1][0] + 50 and elem[1][1] < point[1] < elem[1][1] + 50: 
                game_lose = True 

    if player1_pos[1] + camera_y > frame_size_y: 
        game_lose = True 


def check_lose1():
    '''Проверяет, проиграл ли игрок 1 в режиме 2-х игроков.
    Эта функция проверяет, столкнулся ли игрок с шипами или вышел за пределы игрового поля.
    Если одно из условий выполняется, устанавливает глобальную переменную game_lose1 в True.

    :returns: None
    :rtype: NoneType
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    global game_lose1

    player1_points = [[player1_pos[0] + 1, player1_pos[1] + 1], [player1_pos[0] + 49, player1_pos[1] + 1], [player1_pos[0] + 1, player1_pos[1] + 49], [player1_pos[0] + 49, player1_pos[1] + 1]]

    for point in player1_points:
        for elem in objects_mass:
            if elem[1][1] + camera_y < 50:
                break

            if elem[0] == blue_spike_img and elem[1][0] < point[0] < elem[1][0] + 50 and elem[1][1] < point[1] < elem[1][1] + 50:
                game_lose1 = True

    if player1_pos[1] + camera_y > frame_size_y:
        game_lose1 = True


def check_lose2():
    '''Проверяет, проиграл ли игрок 2 в режиме 2-х игроков.
    Эта функция проверяет, столкнулся ли игрок с шипами или вышел за пределы игрового поля.
    Если одно из условий выполняется, устанавливает глобальную переменную game_lose1 в True.

    :returns: None
    :rtype: NoneType
    :raises IndexError: если объекты в массиве не существуют или индекс выходит за пределы.'''
    global game_lose2

    player2_points = [[player2_pos[0] + 1, player2_pos[1] + 1], [player2_pos[0] + 49, player2_pos[1] + 1], [player2_pos[0] + 1, player2_pos[1] + 49], [player2_pos[0] + 49, player2_pos[1] + 1]]

    for point in player2_points:
        for elem in objects_mass:
            if elem[1][1] + camera_y < 50:
                break

            if elem[0] == blue_spike_img and elem[1][0] < point[0] < elem[1][0] + 50 and elem[1][1] < point[1] < elem[1][1] + 50:
                game_lose2 = True

    if player2_pos[1] + camera_y > frame_size_y:
        game_lose2 = True



def check_game_events(click_pos, have_click):
    '''Обрабатывает события клика в игре.
    Эта функция проверяет, были ли нажаты кнопки на экране игры, и в зависимости от этого 
    изменяет состояние паузы игры. Если кнопка была нажата, её состояние устанавливается в True,
    и игра приостанавливается или возобновляется.

    :param click_pos: Позиция клика в формате (x, y)
    :type click_pos: tuple
    :param have_click: Флаг, указывающий, был ли клик
    :type have_click: bool
    :returns: None
    :rtype: NoneType'''
    global game_pause

    for ind in range(len(game_buttons)):
        if game_buttons[ind]['center_pos'][0] - 35 <= click_pos[0] <= game_buttons[ind]['center_pos'][0] + 35 and game_buttons[ind]['center_pos'][1] - 35 <= click_pos[1] <= game_buttons[ind]['center_pos'][1] + 35 and have_click: 
            game_buttons[ind]['click'] = True 

        else:
            if game_buttons[ind]['click']: 
                game_pause = not game_pause 

            game_buttons[ind]['click'] = False 



def draw_pause(screen):
    '''Отображает экран паузы игры.
    Эта функция рисует изображение паузы на переданном экране и отображает кнопки 
    паузы в зависимости от их состояния (нажата или нет).

    :param screen: Экран, на который будет нарисовано изображение паузы и кнопки
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises AttributeError: Может возникнуть, если объект button не содержит ожидаемых ключей'''
    pause_rect = pause_img.get_rect()
    pause_rect.center = [frame_size_x // 2, frame_size_y // 2] 

    screen.blit(pause_img, pause_rect) 

    for button in pause_buttons: 
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)



def check_event_pause(click_pos, have_click):
    '''Проверяет события на экране паузы.
    Эта функция обрабатывает клики по кнопке на экране паузы. Если клик был 
    произведен по кнопкек, она отмечается как нажатая. Если кнопка была 
    ранее нажата, то переключает экран на меню.

    :param click_pos: Позиция клика мыши (x, y)
    :type click_pos: tuple
    :param have_click: Флаг, указывающий был ли клик
    :type have_click: bool
    :returns: None
    :rtype: NoneType'''
    global now_screen

    for ind in range(len(pause_buttons)): 
        if pause_buttons[ind]['center_pos'][0] - 150 <= click_pos[0] <= pause_buttons[ind]['center_pos'][0] + 150 and pause_buttons[ind]['center_pos'][1] - 75 <= click_pos[1] <= pause_buttons[ind]['center_pos'][1] + 75 and have_click:
            pause_buttons[ind]['click'] = True

        else:
            if pause_buttons[ind]['click']:
                now_screen = 'menu'

            pause_buttons[ind]['click'] = False



def draw_lose(screen):
    '''Отображает экран поражения.
    Эта функция выводит изображение экрана поражения и кнопки на него. 
    Если кнопка была нажата, отображается соответствующее изображение.

    :param screen: Объект экрана, на который будет отрисовано изображение
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises AttributeError: Может возникнуть, если объект button не содержит ожидаемых ключей '''
    lose_rect = lose_img.get_rect()
    lose_rect.center = [frame_size_x // 2, frame_size_y // 2] 

    screen.blit(lose_img, lose_rect) 

    for button in pause_buttons: 
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)



def draw_record(screen):
    '''Отображает текущий рекорд на экране.

    :param screen: Объект экрана, на который будет выводиться текст рекорда.
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises pygame.error: Если происходит ошибка при работе с библиотекой Pygame, например, если шрифт не загружен.'''
    record_text = records_font.render(str(int(camera_y)), False, (0, 0, 0)) 

    screen.blit(record_text, [frame_size_x - 250, 3]) 


def restart():
    '''Сбрасывает состояние игры и возвращает игроков в начальные позиции.
    Эта функция инициализирует глобальные переменные, связанные с состоянием игры, 
    такими как позиции игроков, состояние прыжков, шаги, количество шипов на линии 
    и управление игроками.

    :returns: None
    :rtype: NoneType
    :raises Exception: Если происходит ошибка при записи конфигурации.'''
    global player1_pos, player2_pos, player1_jump, player2_jump, player_step_x, player_step_y1, player_step_y2, spikes_in_line, objects_mass, control_1pl, control_2pl, camera_y, game_pause, game_lose, game_lose1, game_lose2

    player1_pos = [250, frame_size_y - 100]
    player2_pos = [700, frame_size_y - 100]

    player1_jump = False
    player2_jump = False

    player_step_y1 = 0
    player_step_y2 = 0

    player_step_x = 5

    spikes_in_line = 1

    objects_mass = [[block_img, [x, frame_size_y - 50]] for x in range(250, 750, 50)]

    control_1pl = {
        'W': False,
        'A': False,
        'S': False,
        'D': False,
    }

    control_2pl = {
        'W': False,
        'A': False,
        'S': False,
        'D': False,
    }

    camera_y = 0

    game_pause = False
    game_lose = False
    game_lose1 = False
    game_lose2 = False

    write_config()


def game_screen_1pl(screen):
    '''Отображает игровой экран для одного игрока.
    Эта функция инициализирует игровой экран, обрабатывает события 
    управления и обновляет состояние игры. Она также управляет 
    паузами и состоянием проигрыша.

    :param screen: Экран, на котором будет отображаться игра.
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises SystemExit: Если пользователь закрывает окно игры.
    :raises Exception: Если возникает ошибка при записи конфигурации.'''
    global now_screen, control_1pl, camera_y, game_pause

    restart() 

    fps_controller = pygame.time.Clock() 

    click = False 

    for i in range(frame_size_y - 200, -1000000, -150): 
        create_lines(i)

    while now_screen == 'game1': 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                write_config() 

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN: 
                check_mass = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]: 
                        control_1pl[wasd[i]] = True 

            elif event.type == pygame.KEYUP: 
                check_mass = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]: 
                        control_1pl[wasd[i]] = False 

            if event.type == pygame.MOUSEBUTTONDOWN:  
                click = True  

            elif event.type == pygame.MOUSEBUTTONUP:  
                click = False  

        if not game_pause and not game_lose: 
            control_1() 
            check_lose() 

            check_game_events(pygame.mouse.get_pos(), click) 

            if camera_y < -player1_pos[1] + frame_size_y - 400: 
                camera_y = -player1_pos[1] + frame_size_y - 400

            draw_background(screen) 
            draw_game_1pl(screen) 

            draw_record(screen) 

        elif game_pause: 
            check_event_pause(pygame.mouse.get_pos(), click) 

            draw_background(screen) 
            draw_game_1pl(screen) 

            draw_record(screen)

            draw_pause(screen) 

            check_game_events(pygame.mouse.get_pos(), click) 

        elif game_lose:
            check_event_pause(pygame.mouse.get_pos(), click) 

            draw_background(screen) 
            draw_game_1pl(screen) 

            draw_record(screen) 

            draw_lose(screen) 

        pygame.display.update()
        fps_controller.tick(90) 

    add_record(camera_y) 



def check_record_events(click_pos, have_click):
    '''Обрабатывает события кликов для записи.
    Эта функция проверяет, были ли нажаты кнопки на экране 
    записи, и изменяет состояние кнопок в зависимости от 
    позиции клика и состояния нажатия.

    :param click_pos: Позиция клика мыши (x, y).
    :type click_pos: tuple
    :param have_click: Флаг, указывающий, был ли клик.
    :type have_click: bool
    :returns: None
    :rtype: NoneType
    :raises Exception: Если возникают ошибки при обработке событий.'''
    global check_buttons, now_screen

    for ind in range(len(check_buttons)):
        if check_buttons[ind]['center_pos'][0] - 150 <= click_pos[0] <= check_buttons[ind]['center_pos'][0] + 150 and check_buttons[ind]['center_pos'][1] - 75 <= click_pos[1] <= check_buttons[ind]['center_pos'][1] + 75 and have_click:
            check_buttons[ind]['click'] = True

        else:
            if check_buttons[ind]['click']:
                now_screen = 'menu'

            check_buttons[ind]['click'] = False


def draw_check_records(screen):
    '''Отображает кнопки и записи на экране.
    Эта функция рисует кнопки на экране в зависимости от их состояния 
    (нажата или нет) и отображает записи из массива records_mass.

    :param screen: Объект экрана, на который будут выводиться кнопки и текст.
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises Exception: Если возникают ошибки при отрисовке элементов на экране.
    '''
    for button in check_buttons: 
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)

    for i in range(10): 
        text = records_font.render(str(records_mass[i]), False, (0, 0, 0)) 

        screen.blit(text, [200, i * 35 + 100]) 



def check_record_screen(screen):
    '''Обрабатывает экран записей и события пользователя.
    Эта функция отвечает за отображение экрана записей и обработку событий,
    таких как нажатия мыши. Она работает в цикле до тех пор, пока активен экран
    записей. При выходе из программы сохраняет конфигурацию и завершает работу.

    :param screen: Объект экрана, на который будет выводиться информация.
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises SystemExit: Если пользователь закрывает окно, вызывается выход из программы.'''
    global now_screen

    fps_controller = pygame.time.Clock() 

    click = False

    while now_screen == 'records': 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                write_config() 

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  
                click = True  

            elif event.type == pygame.MOUSEBUTTONUP:  
                click = False  

        check_record_events(pygame.mouse.get_pos(), click) 

        draw_background(screen) 
        draw_check_records(screen) 

        pygame.display.update()
        fps_controller.tick(90) 


def draw_game_2pl(screen):
    '''Отображает элементы игры для режима 2 игроков
    Эта функция отвечает за отрисовку игровых объектов, игроков и кнопок на
    экране. Она удаляет объекты, находящиеся ниже нижней границы экрана, 
    а затем рисует оставшиеся объекты, игроков и кнопки.

    :param screen: Объект экрана, на который будет производиться отрисовка.
    :type screen: pygame.Surface
    :returns: None
    :rtype: NoneType
    :raises IndexError: Если список объектов пуст или индекс выходит за пределы.'''
    while objects_mass[0][1][1] + camera_y > frame_size_y:
        del objects_mass[0]

    ind = 0

    while objects_mass[ind][1][1] + camera_y > 0:
        screen.blit(objects_mass[ind][0], [objects_mass[ind][1][0], objects_mass[ind][1][1] + camera_y])

        ind += 1

    screen.blit(player1_img, [player1_pos[0], player1_pos[1] + camera_y])
    screen.blit(player2_img, [player2_pos[0], player2_pos[1] + camera_y])

    screen.blit(front_img, [0, 0])

    for button in game_buttons:
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def draw_lose1(screen):
    '''Отображает экран проигрыша для первого игрока.
    Эта функция отвечает за отрисовку изображения, указывающего на победу 
    второго игрока, и отображение кнопок паузы на экране.

    :param screen: Объект экрана, на который будет производиться отрисовка.
    :type screen: pygame.Surface
    :raises AttributeError: Если объект screen не поддерживает метод blit.'''
    lose_rect = player2win_img.get_rect()
    lose_rect.center = [frame_size_x // 2, frame_size_y // 2]

    screen.blit(player2win_img, lose_rect)

    for button in pause_buttons:
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def draw_lose2(screen):
    '''Отображает экран проигрыша для второго игрока.
    Эта функция отвечает за отрисовку изображения, указывающего на победу 
    первого игрока, и отображение кнопок паузы на экране.

    :param screen: Объект экрана, на который будет производиться отрисовка.
    :type screen: pygame.Surface
    :raises AttributeError: Если объект screen не поддерживает метод blit.'''
    lose_rect = player1win_img.get_rect()
    lose_rect.center = [frame_size_x // 2, frame_size_y // 2]

    screen.blit(player1win_img, lose_rect)

    for button in pause_buttons:
        if button['click']:
            button_rect = button['img1'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img1'], button_rect)
        else:
            button_rect = button['img'].get_rect()
            button_rect.center = button['center_pos']

            screen.blit(button['img'], button_rect)


def game_screen_2pl(screen):
    '''Основной игровой экран для двух игроков.
    Эта функция управляет игровым процессом для двух игроков, обрабатывает 
    события клавиатуры и мыши, обновляет состояние игры и отрисовывает 
    необходимые элементы на экране.

    :param screen: Объект экрана, на который будет производиться отрисовка.
    :type screen: pygame.Surface
    :raises SystemExit: Если игра закрыта пользователем.
    :raises AttributeError: Если объект screen не поддерживает необходимые методы.'''
    global now_screen, control_1pl, camera_y, game_pause

    restart()

    fps_controller = pygame.time.Clock()

    click = False

    for i in range(frame_size_y - 200, -2000000, -150):
        create_lines(i)

    while now_screen == 'game2':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_config()

                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                check_mass = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]:
                        control_1pl[wasd[i]] = True

                check_mass = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]:
                        control_2pl[wasd[i]] = True

            elif event.type == pygame.KEYUP:
                check_mass = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]:
                        control_1pl[wasd[i]] = False

                check_mass = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
                wasd = 'WASD'

                for i in range(4):
                    if event.key == check_mass[i]:
                        control_2pl[wasd[i]] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            elif event.type == pygame.MOUSEBUTTONUP:
                click = False

        if not game_pause and not (game_lose1 or game_lose2):
            control_1()
            control_2()
            check_lose1()
            check_lose2()

            check_game_events(pygame.mouse.get_pos(), click)

            if camera_y < -player1_pos[1] + frame_size_y - 400:
                camera_y = -player1_pos[1] + frame_size_y - 400

            if camera_y < -player2_pos[1] + frame_size_y - 400:
                camera_y = -player2_pos[1] + frame_size_y - 400

            draw_background(screen)
            draw_game_2pl(screen)

            draw_record(screen)

        elif game_pause:
            check_event_pause(pygame.mouse.get_pos(), click)

            draw_background(screen)
            draw_game_2pl(screen)

            draw_record(screen)

            draw_pause(screen)

            check_game_events(pygame.mouse.get_pos(), click)

        elif game_lose1:
            check_event_pause(pygame.mouse.get_pos(), click)

            draw_background(screen)
            draw_game_2pl(screen)

            draw_record(screen)

            draw_lose1(screen)

        elif game_lose2:
            check_event_pause(pygame.mouse.get_pos(), click)

            draw_background(screen)
            draw_game_2pl(screen)

            draw_record(screen)

            draw_lose2(screen)

        pygame.display.update()
        fps_controller.tick(90)

    add_record(camera_y)


if __name__ == '__main__':
    while True:  
        if now_screen == 'menu':
            menu_screen(main_screen)

        elif now_screen == 'choice':
            choice_screen(main_screen)

        elif now_screen == 'records':
            check_record_screen(main_screen)

        elif now_screen == 'game1':
            game_screen_1pl(main_screen)

        elif now_screen == 'game2':
            game_screen_2pl(main_screen)
