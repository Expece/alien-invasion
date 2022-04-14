# Imports
import random
import sys
import time

import pygame

import menu_functions as mf

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from starship import StarShip
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings(self)
        self.settings.game_music.play()

        # Для полноэкранного режима
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # Для оконного режима
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.screen_rect = self.screen.get_rect()

        # Создание экземпляров для хранения статистики, базы данных и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.starship = StarShip(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()

        # Создание экземпляров кнопок.
        self.play_button = Button(self, "Play")
        self.record_button = Button(self, "Record")
        self.settings_button = Button(self, "Settings")
        self.back_button = Button(self, "back")
        self.top_down_buttons = mf.add_top_down_buttons(self)

        self.boom_rect = 0

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.starship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mf.check_back_button(self, mouse_pos, self.back_button)
                mf.check_play_button(self, mouse_pos, self.play_button)
                mf.check_record_button(self, mouse_pos, self.record_button)
                mf.check_sett_button(self, mouse_pos, self.settings_button)
                if self.settings.settings_screen:
                    mf.check_top_down_buttons(self, mouse_pos)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.starship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.starship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_records()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.starship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.starship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            values = collisions.values()
            for aliens in values:
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    self.boom_rect = alien.rect
                    self.time_start = time.time()
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()
            self.settings.new_lvl = True
            self.starship.center_ship()

    def create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Определяет количество рядов, помещающихся на экране.
        ship_height = self.starship.rect.height

        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        map = self._create_alien_wave(number_rows, number_aliens_x)

        # Создание первого ряда пришельцев.
        # for row_number in map:
        #     row_num = map.index(row_number)
        #     for index, value in enumerate(row_number):
        #         if value % 2 == 0:
        #             self._create_alien(index, row_num)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien_wave(self, number_rows, number_aliens_x):
        """Генерирует волну пришельцев"""
        map = [[random.randint(0, 10) for j in range(number_aliens_x)] for i in range(number_rows)]
        return map

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.starship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self.create_fleet()
            self.starship.center_ship()

            # Пауза.
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _draw_game_procces(self):
        if self.settings.new_lvl:
            # Отрисовка анимации перехода на новый уровень и остановка игры.
            self.stats.game_active = False
            self.new_lvl_portal = self.settings.portal_image.get_rect()
            self.new_lvl_portal.center = self.screen_rect.center

            self.screen.blit(self.settings.portal_image, self.new_lvl_portal)
            self.starship.go_new_lvl(self)
            self.starship.blitme()
        elif self.stats.game_active:
            # Отрисовка коллизии bullet и alien
            time_end = time.time()
            if self.boom_rect and (time_end - self.time_start) < 0.3:
                self.screen.blit(self.settings.boom_image, self.boom_rect)

            # Отрисовка игровых элементов.
            self.starship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)
            # Вывод информации о счете.
            self.sb.show_score()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.settings.bg_color, [0, 0])
        self._draw_game_procces()

        if not self.stats.game_active and not self.settings.new_lvl:
            mf.draw_start_screen(self)
            mf.draw_record_screen(self)
            mf.draw_sett_screen(self)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
