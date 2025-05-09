import pygame
import random

class Ability:
    def __init__(self, name, cooldown, effect_func):
        self.name = name
        self.cooldown = cooldown
        self.last_used = 0
        self.effect_func = effect_func

    def can_use(self, current_time):
        return current_time - self.last_used >= self.cooldown

    def use(self, user, game_manager, current_time):
        if self.can_use(current_time):
            self.effect_func(user, game_manager)
            self.last_used = current_time
            return True
        return False

class Weapon:
    def __init__(self, type, damage, armor, damage_multiplier, attack_range, crit_chance=0.1):
        self.type = type
        self.damage = damage
        self.armor = armor
        self.damage_multiplier = damage_multiplier
        self.attack_range = attack_range
        self.crit_chance = crit_chance

class Sword(Weapon):
    def __init__(self, type, damage, armor, damage_multiplier, attack_range, crit_chance=0.1):
        super().__init__(type, damage, armor, damage_multiplier, attack_range, crit_chance)

class Axe(Weapon):
    def __init__(self, type, damage, armor, damage_multiplier, attack_range, crit_chance=0.1):
        super().__init__(type, damage, armor, damage_multiplier, attack_range, crit_chance)

class Bow(Weapon):
    def __init__(self, type, damage, armor, damage_multiplier, arrow_speed, attack_range, crit_chance=0.1):
        super().__init__(type, damage, armor, damage_multiplier, attack_range, crit_chance)
        self.arrow_speed = arrow_speed

class Armor:
    def __init__(self, type, armor):
        self.type = type
        self.armor = armor

class Helmet(Armor):
    def __init__(self, type, armor, damage_multiplier):
        super().__init__(type, armor)
        self.damage_multiplier = damage_multiplier

class Armour(Armor):
    def __init__(self, type, armor, damage_multiplier):
        super().__init__(type, armor)
        self.damage_multiplier = damage_multiplier

class Kneepads(Armor):
    def __init__(self, type, armor):
        super().__init__(type, armor)

class Unit:
    def __init__(self, hp, damage, armor, type, weapon, damage_multiplier, bodykit, ability=None):
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.type = type
        self.weapon = weapon
        self.damage_multiplier = damage_multiplier
        self.bodykit = bodykit
        self.x = 0
        self.y = 0
        self.speed = 0
        self.width = 64
        self.height = 64
        self.dead = False
        self.is_selected = False
        self.is_moving = False
        self.is_attacking = False
        self.facing_left = False
        self.animation_timer = 0
        self.ability = ability

    def attack(self, target):
        self.is_attacking = True
        damage = (self.damage + self.weapon.damage) * self.damage_multiplier * self.bodykit.armor
        if random.random() < self.weapon.crit_chance:
            damage *= 2
        final_damage = max(0, int(damage - target.armor))
        target.hp -= final_damage
        if target.hp <= 0:
            target.dead = True
        return final_damage

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.facing_left = dx < 0

    def update_animation(self, current_time):
        self.animation_timer = current_time

class Healer(Unit):
    def __init__(self, hp, damage, armor, type, weapon, damage_multiplier, bodykit, heal_amount, heal_range, ability=None):
        super().__init__(hp, damage, armor, type, weapon, damage_multiplier, bodykit, ability)
        self.heal_amount = heal_amount
        self.heal_range = heal_range

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

class Item:
    def __init__(self, type, effect, x, y):
        self.type = type
        self.effect = effect
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20

class InteractableObject:
    def __init__(self, type, x, y, effect):
        self.type = type
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.effect = effect
        self.used = False