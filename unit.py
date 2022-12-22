from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        """
        Возвращает аттрибут hp
        """
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        """
        Возвращает аттрибут stamina
        """
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        """
        Присваивает герою новое оружие
        """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        """
        Присваивает герою новое броню
        """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        """
        Расчет урона от удара
        """
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        target_stamina = target.stamina * target.armor.stamina_per_turn
        if target.stamina > target_stamina:
            damage -= target.armor.defence * target.unit_class.armor
            target.stamina -= target_stamina

        damage = round(damage, 1)
        target.get_damage(damage=damage)

        return damage

    def get_damage(self, damage: int) -> Optional[float]:
        """
        Получение урона
        """
        if damage > 0:
            self.hp -= damage
        return round(self.hp, 1)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Использование умения
        """
        if self._is_skill_used:
            return 'Навык использован'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        """
        damage = self._count_damage(target)

        if self.stamina_points < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        elif damage <= 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        damage = self._count_damage(target)

        if self.stamina_points < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        elif damage <= 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        else:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
