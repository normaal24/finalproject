import pygame
import math
import random
import copy
import os
from units import *
from quests import get_random_quests

class GameManager:
    def __init__(self, player_class, player_weapon):
        print(f"Initializing GameManager with class: {player_class}, weapon: {player_weapon}")
        self.units = []
        self.items = []
        self.interactables = []
        self.selected_unit = None
        self.target_unit = None
        self.current_turn = 0
        self.player_turn = True
        self.message = ""
        self.message_time = 0
        self.ai_turn_counter = 0
        self.game_over = False
        self.victory = False
        self.player_level = 1
        self.attack_combo = 0
        self.quest_progress = {
            "Boss": 0,
            "Enemy": 0
        }
        self.mandatory_quests = [
            {"description": "Убити 3 Босів", "target_type": "Boss", "target_count": 3},
            {"description": "Убити 10 ворогів", "target_type": "Enemy", "target_count": 10}
        ]
        self.random_quests = get_random_quests(2)
        for quest in self.random_quests:
            self.quest_progress[quest.target_type] = 0
        try:
            self.ogre_image = pygame.image.load(os.path.join('images', 'ogre.png')).convert_alpha()
            self.ogre_image = pygame.transform.scale(self.ogre_image, (64, 64))  
            self.ogre_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: ogre.png not found, using placeholder")
            self.ogre_image = pygame.Surface((64, 64))
            self.ogre_image.fill((100, 100, 100))
        self.flipped_ogre = pygame.transform.flip(self.ogre_image, True, False)
        self.flipped_ogre.set_colorkey((255, 255, 255))
        try:
            self.paladin_image = pygame.image.load(os.path.join('images', 'paladin.jpg')).convert_alpha()
            self.paladin_image = pygame.transform.scale(self.paladin_image, (64, 64))  
            self.paladin_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: paladin.jpg not found, using placeholder")
            self.paladin_image = pygame.Surface((64, 64))
            self.paladin_image.fill((150, 150, 150))
        self.flipped_paladin = pygame.transform.flip(self.paladin_image, True, False)
        self.flipped_paladin.set_colorkey((255, 255, 255))
        try:
            self.druid_image = pygame.image.load(os.path.join('images', 'druid.png')).convert_alpha()
            self.druid_image = pygame.transform.scale(self.druid_image, (64, 64))  
            self.druid_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: druid.png not found, using placeholder")
            self.druid_image = pygame.Surface((64, 64))
            self.druid_image.fill((200, 200, 200))
        self.flipped_druid = pygame.transform.flip(self.druid_image, True, False)
        self.flipped_druid.set_colorkey((255, 255, 255))
        try:
            self.weak_enemy_image = pygame.image.load(os.path.join('images', 'hero.jpg')).convert_alpha()
            self.weak_enemy_image = pygame.transform.scale(self.weak_enemy_image, (64, 64))  
            self.weak_enemy_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: hero.jpg not found, using placeholder")
            self.weak_enemy_image = pygame.Surface((64, 92))
            self.weak_enemy_image.fill((50, 50, 50))
        self.flipped_weak_enemy = pygame.transform.flip(self.weak_enemy_image, True, False)
        self.flipped_weak_enemy.set_colorkey((255, 255, 255))
        try:
            self.boss_image = pygame.image.load(os.path.join('images', 'hero.jpg')).convert_alpha()
            self.boss_image = pygame.transform.scale(self.boss_image, (96, 96))  
            self.boss_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: hero.jpg not found, using placeholder")
            self.boss_image = pygame.Surface((96, 96))
            self.boss_image.fill((75, 75, 75))
        self.flipped_boss = pygame.transform.flip(self.boss_image, True, False)
        self.flipped_boss.set_colorkey((255, 255, 255))
        try:
            self.double_axe_image = pygame.image.load(os.path.join('images', 'doublehandedaxe.jpg')).convert_alpha()
            self.double_axe_image = pygame.transform.scale(self.double_axe_image, (72, 72))  
            self.double_axe_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: doublehandedaxe.jpg not found, using placeholder")
            self.double_axe_image = pygame.Surface((96, 48))
            self.double_axe_image.fill((255, 100, 100))
        self.flipped_double_axe = pygame.transform.flip(self.double_axe_image, True, False)
        self.flipped_double_axe.set_colorkey((255, 255, 255))
        try:
            self.one_axe_image = pygame.image.load(os.path.join('images', 'onehandedaxe.jpg')).convert_alpha()
            self.one_axe_image = pygame.transform.scale(self.one_axe_image, (72, 72))  
            self.one_axe_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: onehandedaxe.jpg not found, using placeholder")
            self.one_axe_image = pygame.Surface((72, 36))
            self.one_axe_image.fill((255, 150, 150))
        self.flipped_one_axe = pygame.transform.flip(self.one_axe_image, True, False)
        self.flipped_one_axe.set_colorkey((255, 255, 255))
        try:
            self.bow_image = pygame.image.load(os.path.join('images', 'bow.png')).convert_alpha()
            self.bow_image = pygame.transform.scale(self.bow_image, (48, 72))  
            self.bow_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: bow.png not found, using placeholder")
            self.bow_image = pygame.Surface((48, 96))
            self.bow_image.fill((255, 200, 200))
        self.flipped_bow = pygame.transform.flip(self.bow_image, True, False)
        self.flipped_bow.set_colorkey((255, 255, 255))
        try:
            self.sword_image = pygame.image.load(os.path.join('images', 'sword.jpg')).convert_alpha()
            self.sword_image = pygame.transform.scale(self.sword_image, (72, 72))  
            self.sword_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: sword.jpg not found, using placeholder")
            self.sword_image = pygame.Surface((96, 48))
            self.sword_image.fill((255, 50, 50))
        self.flipped_sword = pygame.transform.flip(self.sword_image, True, False)
        self.flipped_sword.set_colorkey((255, 255, 255))
        try:
            self.background = pygame.image.load(os.path.join('images', 'background.jpg')).convert()
            self.background = pygame.transform.scale(self.background, (800, 600))  
        except FileNotFoundError:
            print("Error: background.jpg not found, using placeholder")
            self.background = pygame.Surface((800, 600))
            self.background.fill((0, 100, 0))
        try:
            self.health_potion_image = pygame.image.load(os.path.join('images', 'health_potion.png')).convert_alpha()
            self.health_potion_image = pygame.transform.scale(self.health_potion_image, (20, 20))  
            self.health_potion_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: health_potion.png not found, using placeholder")
            self.health_potion_image = pygame.Surface((20, 20))
            self.health_potion_image.fill((255, 0, 0))
        try:
            self.damage_boost_image = pygame.image.load(os.path.join('images', 'damage_boost.png')).convert_alpha()
            self.damage_boost_image = pygame.transform.scale(self.damage_boost_image, (20, 20))  
            self.damage_boost_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: damage_boost.png not found, using placeholder")
            self.damage_boost_image = pygame.Surface((20, 20))
            self.damage_boost_image.fill((0, 0, 255))
        try:
            self.chest_image = pygame.image.load(os.path.join('images', 'chest.png')).convert_alpha()
            self.chest_image = pygame.transform.scale(self.chest_image, (30, 30))  
            self.chest_image.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            print("Error: chest.png not found, using placeholder")
            self.chest_image = pygame.Surface((30, 30))
            self.chest_image.fill((255, 215, 0))
        self.camera_x = 0
        self.camera_y = 0
        self.last_spawn_time = 0
        self.spawn_interval = 3000
        self.last_boss_spawn_time = 0
        self.boss_spawn_interval = 10000
        self.player_class = player_class
        self.player_weapon = player_weapon
        self.action_cooldown = 500
        self.last_heal_time = 0
        self.last_attack_time = 0
        self.last_ability_time = 0
        self.attack_animation_timer = 0
        self.attack_animation_duration = 300
        self.setup_units()
        self.setup_interactables()

    def setup_units(self):
        weapon_map = {
            "Sword": sword,
            "Double Axe": dhandedaxe,
            "One Axe": ohandedaxe,
            "Bow": bow
        }
        player = copy.deepcopy(Player)
        player.type = self.player_class
        player.weapon = weapon_map[self.player_weapon]
        player.bodykit = armornhelmet if self.player_class == "Ogre" else fullarmor
        player.x = 2000
        player.y = 2000
        print(f"Player {player.type}: HP={player.hp}, Max HP={player.max_hp}, Damage={player.damage}, Weapon Damage={player.weapon.damage}, Armor={player.armor}, Speed={player.speed}, Attack Range={player.weapon.attack_range}")
        self.units.append(player)
        num_enemies = random.randint(5, 7)
        for i in range(num_enemies):
            enemy_classes = [Ogre, Paladin, Druid, WeakEnemy]
            enemy_class = copy.deepcopy(random.choice(enemy_classes))
            enemy_weapons = [sword, dhandedaxe, ohandedaxe, bow]
            enemy_class.weapon = random.choice(enemy_weapons)
            enemy_class.bodykit = armornhelmet
            while True:
                enemy_class.x = random.randint(1000, 3000)
                enemy_class.y = random.randint(1000, 3000)
                if not self.check_collision(enemy_class, 0, 0):
                    break
            enemy_class.speed = 16
            print(f"Enemy {i+1} ({enemy_class.type}): HP={enemy_class.hp}, Max HP={enemy_class.max_hp}, Damage={enemy_class.damage}, Weapon Damage={enemy_class.weapon.damage}, Speed={enemy_class.speed}, Pos=({enemy_class.x}, {enemy_class.y}), Weapon={enemy_class.weapon.type}, Attack Range={enemy_class.weapon.attack_range}")
            self.units.append(enemy_class)
        self.current_turn = 0
        self.player_turn = True
        self.selected_unit = self.units[self.current_turn]
        self.selected_unit.is_selected = True

    def setup_interactables(self):
        for _ in range(3):
            chest = InteractableObject("Chest", random.randint(1000, 3000), random.randint(1000, 3000), chest_effect)
            self.interactables.append(chest)

    def spawn_enemy(self, is_boss=False):
        if is_boss:
            enemy = copy.deepcopy(Boss)
            enemy.type = f"{enemy.type}"
        else:
            enemy_classes = [Ogre, Paladin, Druid, WeakEnemy]
            enemy = copy.deepcopy(random.choice(enemy_classes))
        enemy_weapons = [sword, dhandedaxe, ohandedaxe, bow]
        enemy.weapon = random.choice(enemy_weapons)
        enemy.bodykit = armornhelmet
        spawn_distance = 1000
        spawn_side = random.randint(0, 3)
        if spawn_side == 0:
            enemy.x = random.randint(self.camera_x, self.camera_x + 800)
            enemy.y = self.camera_y - spawn_distance
        elif spawn_side == 1:
            enemy.x = self.camera_x + 800 + spawn_distance
            enemy.y = random.randint(self.camera_y, self.camera_y + 600)
        elif spawn_side == 2:
            enemy.x = random.randint(self.camera_x, self.camera_x + 800)
            enemy.y = self.camera_y + 600 + spawn_distance
        else:
            enemy.x = self.camera_x - spawn_distance
            enemy.y = random.randint(self.camera_y, self.camera_y + 600)
        enemy.speed = 16
        if is_boss:
            enemy.width = 96
            enemy.height = 96
            print(f"Spawned boss ({enemy.type}) at ({enemy.x}, {enemy.y}) with weapon {enemy.weapon.type}, Damage={enemy.weapon.damage}, Attack Range={enemy.weapon.attack_range}")
        else:
            print(f"Spawned enemy ({enemy.type}) at ({enemy.x}, {enemy.y}) with weapon {enemy.weapon.type}, Damage={enemy.weapon.damage}, Attack Range={enemy.weapon.attack_range}")
        self.units.append(enemy)

    def drop_item(self, unit):
        if random.random() < 0.2 and unit != self.units[0]:
            item_type = random.choice([health_potion, damage_boost])
            new_item = copy.deepcopy(item_type)
            new_item.x = unit.x
            new_item.y = unit.y
            self.items.append(new_item)
            print(f"Dropped {new_item.type} at ({new_item.x}, {new_item.y})")

    def check_collision(self, unit, dx, dy):
        new_rect = pygame.Rect(unit.x + dx, unit.y + dy, unit.width, unit.height)
        for other_unit in self.units:
            if other_unit != unit and not other_unit.dead:
                other_rect = pygame.Rect(other_unit.x, other_unit.y, other_unit.width, other_unit.height)
                if new_rect.colliderect(other_rect):
                    return True
        return False

    def get_distance(self, unit1, unit2):
        center1 = (unit1.x + unit1.width // 2, unit1.y + unit1.height // 2)
        center2 = (unit2.x + unit2.width // 2, unit2.y + unit2.height // 2)
        return math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

    def check_player_death(self):
        try:
            if self.units[0].hp <= 0 or self.units[0].dead:
                print("Player died, game over triggered")
                self.message = "Гру завершено: Ви програли!"
                self.game_over = True
                self.victory = False
                return True
        except AttributeError as e:
            print(f"Error in check_player_death: {e}")
            self.message = "Гру завершено: Помилка!"
            self.game_over = True
            self.victory = False
            return True
        return False

    def check_quests_completed(self):
        if self.quest_progress["Boss"] >= 3 and self.quest_progress["Enemy"] >= 10:
            self.game_over = True
            self.victory = True
            self.message = "Вітаємо! Ви перемогли, виконавши всі квести!"
            return True
        return False

    def next_turn(self):
        for unit in self.units:
            if unit.ability:
                if unit.type == "Paladin" and unit.ability.name == "Holy Shield" and unit.ability.last_used > 0:
                    if pygame.time.get_ticks() - unit.ability.last_used > 3000:
                        unit.armor -= 50
                if unit.type == "Druid" and unit.ability.name == "Nature’s Call" and unit.ability.last_used > 0:
                    if pygame.time.get_ticks() - unit.ability.last_used > 5000:
                        for u in self.units:
                            if u != unit and not u.dead:
                                u.speed /= 0.5
        dead_units = []
        for unit in self.units:
            if unit.hp <= 0 or unit.dead:
                print(f"Unit {unit.type} is dead: hp={unit.hp}, dead={unit.dead}")
                dead_units.append(unit)
        for unit in dead_units:
            if unit != self.units[0]:
                if not unit.type.startswith("Boss"):
                    self.quest_progress["Enemy"] += 1
                    print(f"Enemy killed! Total: {self.quest_progress['Enemy']}/10")
                if unit.type.startswith("Boss"):
                    self.quest_progress["Boss"] += 1
                    print(f"Boss killed! Total: {self.quest_progress['Boss']}/3")
                if unit.type in self.quest_progress:
                    self.quest_progress[unit.type] += 1
                    quest_target = next((q.target_count for q in self.random_quests if q.target_type == unit.type), None)
                    if quest_target is not None:
                        print(f"{unit.type} killed! Total: {self.quest_progress[unit.type]}/{quest_target}")
                    else:
                        print(f"{unit.type} killed! No quest associated.")
                if unit.weapon.type == "Sword" and "Sword Enemy" in self.quest_progress:
                    self.quest_progress["Sword Enemy"] += 1
                    sword_quest_target = next((q.target_count for q in self.random_quests if q.target_type == "Sword Enemy"), None)
                    if sword_quest_target is not None:
                        print(f"Sword enemy killed! Total: {self.quest_progress['Sword Enemy']}/{sword_quest_target}")
                    else:
                        print(f"Sword enemy killed! No quest associated.")
                if (unit.weapon.type == "Double handed axe" or unit.weapon.type == "One handed axe") and "Axe Enemy" in self.quest_progress:
                    self.quest_progress["Axe Enemy"] += 1
                    axe_quest_target = next((q.target_count for q in self.random_quests if q.target_type == "Axe Enemy"), None)
                    if axe_quest_target is not None:
                        print(f"Axe enemy killed! Total: {self.quest_progress['Axe Enemy']}/{axe_quest_target}")
                    else:
                        print(f"Axe enemy killed! No quest associated.")
            print(f"Calling drop_item for {unit.type}")
            self.drop_item(unit)
        self.units = [unit for unit in self.units if not unit.dead]
        self.items = [item for item in self.items if item not in self.items[:]]
        if self.check_quests_completed():
            return
        if not any(unit != self.units[0] for unit in self.units):
            self.message = "Ви перемогли всіх ворогів, але квести не завершені!"
            self.game_over = True
            self.victory = False
            return
        if self.check_player_death():
            return
        self.current_turn = (self.current_turn + 1) % len(self.units)
        self.player_turn = self.current_turn == 0
        for unit in self.units:
            unit.is_selected = False
        self.selected_unit = self.units[self.current_turn]
        self.selected_unit.is_selected = True
        self.target_unit = None
        if not self.player_turn:
            self.ai_turn_counter += 1
            self.ai_turn()
        else:
            self.attack_combo = 0

    def ai_turn(self):
        player_unit = self.units[0]
        for ai_unit in self.units[1:]:
            if ai_unit.dead:
                continue
            distance = self.get_distance(ai_unit, player_unit)
            health_percentage = ai_unit.hp / ai_unit.max_hp
            print(f"AI {ai_unit.type}: Distance={distance}, Weapon={ai_unit.weapon.type}, Range={ai_unit.weapon.attack_range}, Base Damage={ai_unit.damage}, Weapon Damage={ai_unit.weapon.damage}")
            if health_percentage < 0.3 and self.ai_turn_counter % 5 == 0:
                heal_amount = 10
                ai_unit.heal(heal_amount)
                self.show_message(f"{ai_unit.type} відновив {heal_amount} здоров'я!")
            else:
                if distance <= ai_unit.weapon.attack_range:
                    damage = ai_unit.attack(player_unit)
                    print(f"AI {ai_unit.type} attacks: Damage={damage}, Player HP={player_unit.hp}/{player_unit.max_hp}")
                    if damage > 0:
                        self.show_message(f"{ai_unit.type} атакував {player_unit.type} і наніс {int(damage)} шкоди!")
                    else:
                        self.show_message(f"{ai_unit.type} атакував, але не завдав шкоди!")
                    if self.check_player_death():
                        return
                else:
                    dx = player_unit.x - ai_unit.x
                    dy = player_unit.y - ai_unit.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance > 0:
                        move_x = int(dx / distance * ai_unit.speed * 2)
                        move_y = int(dy / distance * ai_unit.speed * 2)
                        if not self.check_collision(ai_unit, move_x, move_y):
                            ai_unit.move(move_x, move_y)
                            self.show_message(f"{ai_unit.type} рухається до {player_unit.type}!")
        self.next_turn()

    def show_message(self, text):
        self.message = text
        self.message_time = pygame.time.get_ticks()

    def level_up(self):
        self.player_level += 1
        player = self.units[0]
        player.max_hp += 10
        player.hp += 10
        player.damage += 2
        player.armor += 1
        self.show_message(f"Рівень підвищено до {self.player_level}! HP +10, Шкода +2, Броня +1")
        print(f"Player leveled up to {self.player_level}: HP={player.hp}/{player.max_hp}, Damage={player.damage}, Armor={player.armor}")

    def update(self, keys, mouse_pos, mouse_click, events):
        if self.game_over:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.message_time > 2000:
            self.message = ""
        if self.attack_animation_timer > 0:
            elapsed = current_time - self.last_attack_time
            self.attack_animation_timer -= elapsed
            if self.attack_animation_timer < 0:
                self.attack_animation_timer = 0
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_enemy(is_boss=False)
            self.last_spawn_time = current_time
        if current_time - self.last_boss_spawn_time > self.boss_spawn_interval:
            self.spawn_enemy(is_boss=True)
            self.last_boss_spawn_time = current_time
        for unit in self.units:
            unit.update_animation(current_time)
        if self.player_turn and self.selected_unit:
            dx, dy = 0, 0
            if keys[pygame.K_a]:
                dx = -self.selected_unit.speed
            if keys[pygame.K_d]:
                dx = self.selected_unit.speed
            if keys[pygame.K_w]:
                dy = -self.selected_unit.speed
            if keys[pygame.K_s]:
                dy = self.selected_unit.speed
            if dx != 0 or dy != 0:
                print(f"Movement: dx={dx}, dy={dy}, Pos=({self.selected_unit.x}, {self.selected_unit.y})")
                if not self.check_collision(self.selected_unit, dx, dy):
                    self.selected_unit.move(dx, dy)
                    self.selected_unit.is_moving = True
                else:
                    print("Move rejected: collision")
            else:
                self.selected_unit.is_moving = False
            self.camera_x = self.selected_unit.x - 800 // 2
            self.camera_y = self.selected_unit.y - 600 // 2
            player_rect = pygame.Rect(self.selected_unit.x, self.selected_unit.y, self.selected_unit.width, self.selected_unit.height)
            for item in self.items[:]:
                item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
                if player_rect.colliderect(item_rect):
                    item.effect(self.selected_unit)
                    self.show_message(f"Гравець підібрав {item.type}!")
                    self.items.remove(item)
            for interactable in self.interactables:
                if interactable.used:
                    continue
                interactable_rect = pygame.Rect(interactable.x, interactable.y, interactable.width, interactable.height)
                if player_rect.colliderect(interactable_rect):
                    interactable.effect(self.selected_unit, self)
                    interactable.used = True
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self.target_unit:
                        distance = self.get_distance(self.selected_unit, self.target_unit)
                        if distance <= self.selected_unit.weapon.attack_range:
                            if current_time - self.last_attack_time >= self.action_cooldown:
                                self.attack_combo += 1
                                damage = self.selected_unit.attack(self.target_unit)
                                if self.attack_combo >= 3:
                                    damage *= 2
                                    self.show_message(f"Комбо-атака! Подвійний урон: {int(damage)}!")
                                    self.attack_combo = 0
                                else:
                                    self.show_message(f"{self.selected_unit.type} атакував {self.target_unit.type} і наніс {int(damage)} шкоди! Комбо: {self.attack_combo}/3")
                                self.attack_animation_timer = self.attack_animation_duration
                                if self.target_unit.hp <= 0 or self.target_unit.dead:
                                    self.level_up()
                                if distance <= self.target_unit.weapon.attack_range and not self.target_unit.dead:
                                    counter_damage = self.target_unit.attack(self.selected_unit)
                                    self.show_message(f"{self.target_unit.type} контратакував і наніс {int(counter_damage)} шкоди!")
                                    if self.check_player_death():
                                        return
                                self.last_attack_time = current_time
                                self.next_turn()
                        else:
                            self.show_message(f"Ціль занадто далеко для атаки! Максимальна відстань: {self.selected_unit.weapon.attack_range}")
                    elif event.key == pygame.K_q:
                        if current_time - self.last_heal_time >= self.action_cooldown:
                            heal_amount = 60 if self.selected_unit.type == "Druid" else 40
                            self.selected_unit.heal(heal_amount)
                            self.show_message(f"{self.selected_unit.type} відновив {heal_amount} здоров'я!")
                            self.last_heal_time = current_time
                            self.next_turn()
                    elif event.key == pygame.K_r and self.selected_unit.ability:
                        if self.selected_unit.ability.use(self.selected_unit, self, current_time):
                            self.last_ability_time = current_time
                            self.next_turn()
        if mouse_click and self.player_turn:
            for unit in self.units:
                if unit.dead:
                    continue
                unit_rect = pygame.Rect(unit.x - self.camera_x, unit.y - self.camera_y, unit.width, unit.height)
                if unit_rect.collidepoint(mouse_pos):
                    if self.selected_unit and self.selected_unit != unit:
                        self.target_unit = unit
                    else:
                        self.selected_unit = unit
                        self.target_unit = None
                        for u in self.units:
                            u.is_selected = (u == unit)

    def draw(self, surface):
        bg_width, bg_height = self.background.get_size()
        for x in range(int(self.camera_x // bg_width - 1), int((self.camera_x + 800) // bg_width + 1)):
            for y in range(int(self.camera_y // bg_height - 1), int((self.camera_y + 600) // bg_height + 1)):
                surface.blit(self.background, (x * bg_width - self.camera_x, y * bg_height - self.camera_y))
        for item in self.items:
            if item.type == "Health Potion":
                surface.blit(self.health_potion_image, (item.x - self.camera_x, item.y - self.camera_y))
            elif item.type == "Damage Boost":
                surface.blit(self.damage_boost_image, (item.x - self.camera_x, item.y - self.camera_y))
        for interactable in self.interactables:
            if not interactable.used:
                surface.blit(self.chest_image, (interactable.x - self.camera_x, interactable.y - self.camera_y))
        for i, unit in enumerate(self.units):
            if unit.dead:
                continue
            if unit.type == "Boss":
                image = self.flipped_boss if unit.facing_left else self.boss_image
            elif unit.type == "Ogre":
                image = self.flipped_ogre if unit.facing_left else self.ogre_image
            elif unit.type == "Paladin":
                image = self.flipped_paladin if unit.facing_left else self.paladin_image
            elif unit.type == "Druid":
                image = self.flipped_druid if unit.facing_left else self.druid_image
            else:
                image = self.flipped_weak_enemy if unit.facing_left else self.weak_enemy_image
            y_offset = 0
            if unit.is_moving and unit.animation_timer > 0:
                y_offset = math.sin(unit.animation_timer * 0.01) * 5
            screen_x = unit.x - self.camera_x
            screen_y = unit.y - self.camera_y
            surface.blit(image, (screen_x, screen_y + y_offset))
            weapon_image = None
            flipped_weapon = None
            weapon_x_offset = 0
            weapon_y_offset = unit.height // 2 + y_offset
            weapon_scale = (96, 48)
            if unit.weapon.type == "Double handed axe":
                weapon_image = self.double_axe_image
                flipped_weapon = self.flipped_double_axe
                weapon_x_offset = (unit.width - weapon_image.get_width()) // 2
                weapon_y_offset = (unit.height - weapon_image.get_height()) // 2 + y_offset
            elif unit.weapon.type == "One handed axe":
                weapon_image = self.one_axe_image
                flipped_weapon = self.flipped_one_axe
                weapon_x_offset = (unit.width - weapon_image.get_width()) // 2
                weapon_y_offset = (unit.height - weapon_image.get_height()) // 2 + y_offset
                weapon_scale = (72, 36)
            elif unit.weapon.type == "Bow":
                weapon_image = self.bow_image
                flipped_weapon = self.flipped_bow
                weapon_x_offset = (unit.width - weapon_image.get_width()) // 2
                weapon_y_offset = (unit.height - weapon_image.get_height()) // 2 + y_offset
                weapon_scale = (48, 96)
            elif unit.weapon.type == "Sword":
                weapon_image = self.sword_image
                flipped_weapon = self.flipped_sword
                weapon_x_offset = (unit.width - weapon_image.get_width()) // 2
                weapon_y_offset = (unit.height - weapon_image.get_height()) // 2 + y_offset
            if weapon_image:
                weapon_to_draw = flipped_weapon if unit.facing_left else weapon_image
                weapon_x = screen_x + weapon_x_offset
                weapon_y = screen_y + weapon_y_offset
                if unit.is_attacking and self.attack_animation_timer > 0:
                    if unit.weapon.type == "Bow":
                        scale_factor = 1 + math.sin(self.attack_animation_timer / self.attack_animation_duration * math.pi) * 0.2
                        new_width = int(weapon_scale[0] * scale_factor)
                        new_height = weapon_scale[1]
                        rotated_weapon = pygame.transform.scale(weapon_to_draw, (new_width, new_height))
                    else:
                        angle = math.sin(self.attack_animation_timer / self.attack_animation_duration * math.pi) * 45
                        rotated_weapon = pygame.transform.rotate(weapon_to_draw, angle if not unit.facing_left else -angle)
                    rotated_rect = rotated_weapon.get_rect(center=(weapon_x + weapon_image.get_width() // 2, weapon_y + weapon_image.get_height() // 2))
                    surface.blit(rotated_weapon, rotated_rect.topleft)
                    unit.is_attacking = False
                else:
                    surface.blit(weapon_to_draw, (weapon_x, weapon_y))
            try:
                hp_width = int((unit.hp / unit.max_hp) * unit.width) if unit.max_hp > 0 else 0
                if hp_width < 0:
                    print(f"Warning: Negative hp_width for {unit.type}, hp={unit.hp}, max_hp={unit.max_hp}")
                    hp_width = 0
            except (AttributeError, ZeroDivisionError) as e:
                print(f"Error drawing health bar for {unit.type}: {e}")
                hp_width = 0
            pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y - 10 + y_offset, unit.width, 5))
            pygame.draw.rect(surface, (0, 255, 0), (screen_x, screen_y - 10 + y_offset, hp_width, 5))
            text_color = (0, 255, 0) if i == 0 else (255, 0, 0)
            text = pygame.font.SysFont(None, 24).render(unit.type, True, text_color)
            text_x = screen_x + (unit.width - text.get_width()) // 2
            surface.blit(text, (text_x, screen_y - 25 + y_offset))
            if unit.is_selected:
                pygame.draw.rect(surface, (0, 0, 255), (screen_x - 2, screen_y - 2 + y_offset, unit.width + 4, unit.height + 4), 2)
                if self.player_turn:
                    pygame.draw.circle(surface, (0, 0, 255),
                                      (screen_x + unit.width // 2, screen_y + unit.height // 2 + y_offset),
                                      unit.weapon.attack_range, 1)
            if unit == self.target_unit:
                pygame.draw.rect(surface, (255, 0, 0), (screen_x - 2, screen_y - 2 + y_offset, unit.width + 4, unit.height + 4), 2)