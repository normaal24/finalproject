import pygame
import random
import math

def paladin_shield(user, game_manager):
    user.armor += 50

def druid_slow(user, game_manager):
    for unit in game_manager.units:
        if unit != user and not unit.dead:
            unit.speed *= 0.5

class Ability:
    def __init__(self, name, cooldown, effect):
        self.name = name
        self.cooldown = cooldown
        self.effect = effect
        self.last_used = 0

    def use(self, user, game_manager, current_time):
        if current_time - self.last_used >= self.cooldown:
            self.effect(user, game_manager)
            self.last_used = current_time
            return True
        return False

class Weapon:
    def __init__(self, type):
        self.type = type
        if type == "Sword":
            self.damage = 15
            self.attack_range = 150
        elif type == "Double handed axe":
            self.damage = 20
            self.attack_range = 100
        elif type == "One handed axe":
            self.damage = 18
            self.attack_range = 120
        elif type == "Bow":
            self.damage = 10
            self.attack_range = 300
        else:
            self.damage = 0
            self.attack_range = 100

class Armor:
    def __init__(self, type, armor):
        self.type = type
        self.armor = armor

class Item:
    def __init__(self, type, x, y, effect):
        self.type = type
        self.x = x
        self.y = y
        self.effect = effect
        self.width = 20
        self.height = 20

def health_potion_effect(unit):
    unit.heal(20)

def damage_boost_effect(unit):
    unit.damage += 5

class InteractableObject:
    def __init__(self, type, x, y, effect):
        self.type = type
        self.x = x
        self.y = y
        self.effect = effect
        self.width = 30
        self.height = 30
        self.used = False

def chest_effect(unit, game_manager):
    heal_amount = random.randint(30, 50)
    unit.heal(heal_amount)
    game_manager.show_message(f"Скриня: {unit.type} відновив {heal_amount} здоров'я!")

class Unit:
    def __init__(self, hp, damage, armor, type, weapon, damage_multiplier, bodykit, ability=None):
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.armor = armor
        self.type = type
        self.weapon = weapon
        self.damage_multiplier = damage_multiplier
        self.bodykit = bodykit
        self.ability = ability
        self.speed = 20
        self.width = 64
        self.height = 64
        self.x = 0
        self.y = 0
        self.is_selected = False
        self.target = None
        self.dead = False
        self.facing_left = False
        self.is_moving = False
        self.is_attacking = False
        self.animation_timer = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.facing_left = dx < 0

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def attack(self, target):
        self.is_attacking = True
        distance = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
        if distance <= self.weapon.attack_range:
            damage = self.damage + self.weapon.damage
            damage *= self.damage_multiplier
            damage = max(1, damage - target.armor)
            target.hp -= damage
            if target.hp <= 0:
                target.dead = True
            return damage
        return 0

    def update_animation(self, current_time):
        self.animation_timer += 1
        if self.animation_timer >= 100:
            self.animation_timer = 0

class Healer(Unit):
    def __init__(self, hp, damage, armor, type, weapon, damage_multiplier, bodykit, heal_amount, heal_cooldown, ability=None):
        super().__init__(hp, damage, armor, type, weapon, damage_multiplier, bodykit, ability)
        self.heal_amount = heal_amount
        self.heal_cooldown = heal_cooldown
        self.last_heal = 0

    def heal(self, amount):
        super().heal(amount)

noarmor = Armor("No Armor", 0)
armornhelmet = Armor("Armor and Helmet", 10)
fullarmor = Armor("Full Armor", 20)
noweapon = Weapon("No Weapon")
sword = Weapon("Sword")
dhandedaxe = Weapon("Double handed axe")
ohandedaxe = Weapon("One handed axe")
bow = Weapon("Bow")
health_potion = Item("Health Potion", 0, 0, health_potion_effect)
damage_boost = Item("Damage Boost", 0, 0, damage_boost_effect)
Ogre = Unit(270, 15, 8, "Ogre", noweapon, 1.0, noarmor)
Paladin = Unit(200, 15, 15, "Paladin", noweapon, 1.0, noarmor, Ability("Holy Shield", 15000, paladin_shield))
Druid = Healer(185, 15, 10, "Druid", noweapon, 1.0, noarmor, 5, 20, Ability("Nature’s Call", 12000, druid_slow))
WeakEnemy = Unit(80, 15, 1, "Weak Enemy", noweapon, 1.0, noarmor)
Boss = Unit(300, 30, 15, "Boss", noweapon, 1.0, noarmor)
Player = Unit(300, 70, 30, "Player", noweapon, 1.0, noarmor)