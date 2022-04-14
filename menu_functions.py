import pygame
from button import Button


def draw_start_screen(ai_game):
    """Отрисовывает стартовый экран"""
    if not ai_game.settings.record_screen and not ai_game.settings.settings_screen:
        # Прорисовка заднего фона и кнопок
        screen = ai_game.screen
        screen.blit(ai_game.settings.bg_color, [0, 0])
        ai_game.play_button.draw_button()
        ai_game.record_button.draw_button()
        ai_game.settings_button.draw_button()

        # Принт лого.
        logo = ai_game.settings.logo
        rect = logo.get_rect()
        rect.center = ai_game.screen_rect.center
        rect.y -= ai_game.settings.offset * 2
        screen.blit(logo, rect)


def check_play_button(ai_game, mouse_pos, play_button):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_pos)
    if (button_clicked and not ai_game.stats.game_active and not ai_game.settings.record_screen
            and not ai_game.settings.settings_screen):
        ai_game.stats.game_active = True
        reset_game(ai_game)
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)


def reset_game(ai_game):
    # Сброс игровых настроек.
    ai_game.settings._initialize_dynamic_settings()

    # Сброс игровой статистики.
    ai_game.stats.reset_stats()
    ai_game.sb.prep_score()
    ai_game.sb.prep_level()
    ai_game.sb.prep_ships()

    # Очистка списков пришельцев и снарядов.
    ai_game.aliens.empty()
    ai_game.bullets.empty()

    # Создание нового флота и размещение корабля в центре.
    ai_game.create_fleet()
    ai_game.starship.center_ship()


def check_record_button(ai_game, mouse_pos, player_button):
    """Меняет флаг на True для отрисовки экрана рекодов"""
    button_clicked = player_button.rect.collidepoint(mouse_pos)
    if button_clicked and not ai_game.settings.settings_screen:
        ai_game.settings.record_screen = True


def draw_record_screen(ai_game):
    """Отрисовывает экран рекордов"""
    if ai_game.settings.record_screen:
        ai_game.back_button.draw_button()
        draw_records(ai_game)


def draw_records(ai_game):
    """Отрисовывает картунку кубка и рекордный счет"""
    # Назначение координат кубка
    award_board = ai_game.settings.award_board_image
    award_board_rect = award_board.get_rect()
    award_board_rect.center = ai_game.screen_rect.center

    # Назначение координат рек. счета
    high_score_str = "Score: {}".format(ai_game.stats.high_score)
    high_score = ai_game.settings.myfont.render(high_score_str, True, (255, 255, 255))
    score_rect = high_score.get_rect()
    score_rect.center = award_board_rect.center

    # Назначение координат рек. уровня
    high_level_str = "Level: {}".format(ai_game.stats.high_level)
    high_level = ai_game.settings.myfont.render(high_level_str, True, (255, 255, 255))
    level_rect = high_level.get_rect()
    level_rect.center = score_rect.center
    level_rect.y += ai_game.settings.offset

    # Вывод на экран
    ai_game.screen.blit(award_board, award_board_rect)
    ai_game.screen.blit(high_score, score_rect)
    ai_game.screen.blit(high_level, level_rect)


def check_back_button(ai_game, mouse_pos, back_button):
    """Возвращает стартовый экран при нажатии кнопки back"""
    button_clicked = back_button.rect.collidepoint(mouse_pos)
    if button_clicked:
        ai_game.settings.record_screen = False
        ai_game.settings.settings_screen = False


def check_sett_button(ai_game, mouse_pos, settings_button):
    """При нажатии на кнопку настроек разрешает отрисовывать экран настроек"""
    button_clicked = settings_button.rect.collidepoint(mouse_pos)
    if button_clicked and not ai_game.settings.record_screen:
        ai_game.settings.settings_screen = True


def draw_sett_screen(ai_game):
    """Отрисовывает экран настроек"""
    if ai_game.settings.settings_screen:
        ai_game.back_button.draw_button()
        ai_game.settings.update_parametrs()
        ai_game.settings.adaptation_parametrs()
        draw_settings(ai_game)
        draw_top_down_buttons(ai_game)


def draw_settings(ai_game):
    """Отрисовывает настройки"""
    settings_name_dict, settings_value_dict = ai_game.settings.settings_name_dict, ai_game.settings.settings_value_dict
    for name in settings_name_dict.values():
        ai_game.screen.blit(name[0], name[-1])
    for value in settings_value_dict.values():
        ai_game.screen.blit(value[0], value[-1])


def add_top_down_buttons(ai_game):
    """Добавлят для каждого поля настроек кнопки top и down"""
    top_down_buttons = {}
    for key in ai_game.settings.settings_parametrs:
        top_down_buttons[key] = (Button(ai_game, 'top'), Button(ai_game, 'down'))
    return top_down_buttons


def draw_top_down_buttons(ai_game):
    """Рисует кнопки top и bot"""
    for button in ai_game.top_down_buttons.values():
        button[0].draw_button()
        button[-1].draw_button()


def check_top_down_buttons(ai_game, mouse_pos):
    button_clicked, key, index = enumeration_buttons(ai_game, mouse_pos)
    if button_clicked:
        functions_top_down_buttons(ai_game, key, index)


def functions_top_down_buttons(ai_game, key, index):
    if key == 'Aliens speed':
        if index == 0:
            ai_game.settings.alien_speed += 0.1
        else:
            ai_game.settings.alien_speed -= 0.1
    elif key == 'Ship speed':
        if index == 0:
            ai_game.settings.ship_speed += 0.1
        else:
            ai_game.settings.ship_speed -= 0.1
    elif key == 'Bullet speed':
        if index == 0:
            ai_game.settings.bullet_speed += 0.1
        else:
            ai_game.settings.bullet_speed -= 0.1
    elif key == 'Fleet drop speed':
        if index == 0:
            ai_game.settings.fleet_drop_speed += 1
        else:
            ai_game.settings.fleet_drop_speed -= 1
    elif key == 'Speedup scale':
        if index == 0:
            ai_game.settings.speedup_scale += 0.1
        else:
            ai_game.settings.speedup_scale -= 0.1
    elif key == 'Music':
        if index == 0:
            ai_game.settings.game_music.set_volume(True)
            ai_game.settings.game_music_volume = True
        else:
            ai_game.settings.game_music.set_volume(False)
            ai_game.settings.game_music_volume = False


def enumeration_buttons(ai_game, mouse_pos):
    for key in ai_game.top_down_buttons:
        for index, button in enumerate(ai_game.top_down_buttons[key]):
            button_clicked = button.rect.collidepoint(mouse_pos)
            if button_clicked:
                return button_clicked, key, index
    return False, 0, 0
