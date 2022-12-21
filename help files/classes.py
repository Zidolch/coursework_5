from dataclasses import dataclass


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(name='Abc', max_health=100, max_stamina=100, attack=10, stamina=10, armor=10, skill=)
ThiefClass = ... # TODO действуем так же как и с войном

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}