from pygame import image, font, mixer


class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статические настройки игры."""
        # Параметры экрана.
        self.ai_game = ai_game
        self.screen_width = 1000
        self.screen_height, self.bg_color, self.logo = self.adaptation_bg()

        # Картинки.
        self.portal_image = image.load('images/portal.png')
        self.award_board_image = image.load('images/award_board.png')
        self.boom_image = image.load('images/boom.png')
        self.bullet = image.load('images/bullet.png')

        # Музыка
        self.game_music = mixer.Sound('music/game_music.mp3')
        self.game_music_volume = True
        self.game_music.set_volume(True)

        # Фон счета.
        self.some_color = (0, 0, 0)
        # Шрифт
        self.myfont = font.Font(None, 50)

        # Отступ между кнопками.
        self.offset = 70

        # Настройки корабля.
        self.ship_limit = 2

        # Ограничение bullet на экране.
        self.bullets_allowed = 5

        # Настройки пришельцев.
        self.fleet_drop_speed = 30
        self.alien_points = 50

        # Темп ускорения игры.
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев.
        self.score_scale = 1.5

        # Флаги.
        self.record_screen = False
        self.settings_screen = False
        self.new_lvl = False
        self.once = True

        self._initialize_dynamic_settings()

        self.settings_parametrs = {
            'Aliens speed': f'{self.alien_speed}',
            'Ship speed': f'{self.ship_speed}',
            'Bullet speed': f'{self.bullet_speed}',
            'Fleet drop speed': f'{self.fleet_drop_speed}',
            'Speedup scale': f'{self.speedup_scale}',
            'Music': f'{self.game_music_volume}'
        }
        self.settings_name_dict, self.settings_value_dict = {}, {}

    def adaptation_bg(self):
        """Адаптирует задний фон в зависимости от настроек экрана"""
        if self.screen_width == 1000:
            self.bg_color = image.load('images/bg_1000.png')
            self.screen_height = 667
            self.logo = image.load('images/alien_invasion_800.png')
        elif self.screen_width == 1200:
            self.bg_color = image.load('images/bg_1200.png')
            self.screen_height = 800
            self.logo = image.load('images/alien_invasion_1000.png')
        return self.screen_height, self.bg_color, self.logo

    def _initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 2.5
        self.bullet_speed = 2.0
        self.alien_speed = 1.0

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def update_parametrs(self):
        self.settings_parametrs = {
            'Aliens speed': f'{self.alien_speed}',
            'Ship speed': f'{self.ship_speed}',
            'Bullet speed': f'{self.bullet_speed}',
            'Fleet drop speed': f'{self.fleet_drop_speed}',
            'Speedup scale': f'{self.speedup_scale}',
            'Music': f'{self.game_music_volume}'
        }

    def adaptation_parametrs(self):
        """Адаптирует параметры для экрана настроек,
        работает с текстом и назначает rect"""
        coefficient_y = 0
        for key in self.settings_parametrs:
            name_sett_str = f"{key}:"
            name_sett = self.myfont.render(name_sett_str, True, (255, 255, 255))
            name_sett_rect = name_sett.get_rect()
            name_sett_rect.x = 200
            name_sett_rect.y = 100 + self.offset * coefficient_y

            value_sett_str = f"{self.settings_parametrs[key]}"
            value_sett = self.myfont.render(value_sett_str, True, (255, 255, 255))
            value_sett_rect = value_sett.get_rect()
            value_sett_rect.x = 700
            value_sett_rect.y = name_sett_rect.y

            self.settings_name_dict[key] = [name_sett, name_sett_rect]
            self.settings_value_dict[key] = [value_sett, value_sett_rect]
            coefficient_y += 1
            if self.once:
                for button in self.ai_game.top_down_buttons[key]:
                    button.set_rect(value_sett_rect.x + 100, value_sett_rect.y + 15)
        self.once = False
