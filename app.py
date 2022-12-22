from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    """
    Представление для главной страницы
    """
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """
    Представление для начала боя
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    Представление для удара игрока
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Представление для использования умения игрока
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Представление для пропуска хода игрока
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    Представление для окончания боя
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    Представление для выбора героя
    """
    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            'header': 'Выберите героя:',
            'weapons': weapons,
            'armors': armors,
            'classes': classes
        }

        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        player.equip_weapon(equipment.get_weapon(weapon_name))
        player.equip_armor(equipment.get_armor(armor_name))
        heroes['player'] = player

        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    Представлиние для выбора противника
    """
    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            'header': 'Выберите героя:',
            'weapons': weapons,
            'armors': armors,
            'classes': classes
        }

        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        enemy.equip_armor(equipment.get_armor(armor_name))
        heroes['enemy'] = enemy

        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
