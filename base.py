from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """
    Класс поля битвы
    """
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """
        Начало игры
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> str:
        """
        Проверка здоровья соперников
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.player.hp = 0
            self.enemy.hp = 0
            self.battle_result = 'Ничья'
        elif self.player.hp <= 0:
            self.player.hp = 0
            self.battle_result = 'Игрок проиграл битву'
        elif self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.battle_result = 'Игрок выиграл битву'

        if self.battle_result is not None:
            return self._end_game()

    def _stamina_regeneration(self):
        """
        Восстановление выносливости
        """
        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> str:
        """
        Переход к следующему ходу
        """
        result = self._check_players_hp()
        if result is not None:
            return result

        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        """
        Конец игры
        """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        """
        Удар игрока
        """
        result = self.player.hit(self.enemy)
        enemy_result = self.next_turn()
        return f'{result} {enemy_result}'

    def player_use_skill(self) -> str:
        """
        Навык игрока
        """
        result = self.player.use_skill(self.enemy)
        enemy_result = self.next_turn()
        return f'{result} {enemy_result}'
