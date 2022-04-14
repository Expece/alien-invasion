import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """Инициализирует атрибуты кнопки."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.msg = msg
        # Назначение размеров и свойств кнопок.
        self.rect, self.button_image = self._find_out_rect_and_color()

    def _find_out_rect_and_color(self):
        """Возвращает размер и картинку кнопки"""
        if self.msg == "Play":
            # Построение объекта rect кнопки, выравнивание и загрузка картинки
            self.button_image = pygame.image.load('images/button_play.png')
            self.rect = self.button_image.get_rect()
            self.rect.center = self.screen_rect.center

        elif self.msg == "Record":
            # Построение объекта rect кнопки, выравнивание и загрузка картинки
            self.button_image = pygame.image.load('images/record_button.png')
            self.rect = self.button_image.get_rect()
            self.rect.center = self.screen_rect.center
            self.rect.y += self.settings.offset

        elif self.msg == "Settings":
            # Построение объекта rect кнопки, выравнивание и загрузка картинки
            self.button_image = pygame.image.load('images/button_settings.png')
            self.rect = self.button_image.get_rect()
            self.rect.center = self.screen_rect.center
            self.rect.y += self.settings.offset * 2

        elif self.msg == "back":
            self.button_image = pygame.image.load('images/button_back.png')
            self.rect = self.button_image.get_rect()
            self.rect = pygame.Rect(10, 10, self.rect.width, self.rect.height)

        elif self.msg == "top":
            self.button_image = pygame.image.load('images/top.png')
            self.rect = self.button_image.get_rect()
            self.rect = pygame.Rect(0, -18, self.rect.width, self.rect.height)

        elif self.msg == "down":
            self.button_image = pygame.image.load('images/bottom.png')
            self.rect = self.button_image.get_rect()
            self.rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)

        return self.rect, self.button_image

    def draw_button(self):
        """Отображает кнопку на экране"""
        self.screen.blit(self.button_image, self.rect)

    def set_rect(self, x, y):
        self.rect.x += x
        self.rect.y += y
