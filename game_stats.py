import json


class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.filename = 'records.json'

        # Игра запускается в активном состоянии.
        self.game_active = False

        # Рекорд не должен сбрасываться.

        self.high_score = 0
        self.high_level = 0

        self.load_records()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_records(self):
        """Сохраняет json файл с рекордами"""
        myrecords = {
            'score': self.high_score,
            'level': self.high_level
        }
        json_string = json.dumps(myrecords)
        with open(self.filename, 'w') as f:
            f.write(json_string)

    def load_records(self):
        """Восстанавливает рекорды из json"""
        with open(self.filename) as json_file:
            myrecords = json.load(json_file)
            self.high_score = myrecords.get('score', 0)
            self.high_level = myrecords.get('level', 0)
