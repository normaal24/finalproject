import pygame
import os

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.image = image
        self.font = pygame.font.SysFont(None, 30)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(centerx=self.rect.left + 70, centery=self.rect.centery)
        if self.image:
            self.image_rect = self.image.get_rect(centerx=self.rect.right - 40, centery=self.rect.centery)

    def update(self, mouse_pos):
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        surface.blit(self.text_surface, self.text_rect)
        if self.image:
            surface.blit(self.image, self.image_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class Menu:
    def __init__(self):
        print("Initializing Menu")
        try:
            self.background = pygame.image.load(os.path.join('images', 'background1.jpg'))
            self.background = pygame.transform.scale(self.background, (800, 600)).convert()
        except FileNotFoundError:
            self.background = pygame.Surface((800, 600))
            self.background.fill((0, 100, 0))
        try:
            hero_images = {
                "Ogre": pygame.transform.scale(pygame.image.load(os.path.join('images', 'ogre.png')).convert_alpha(), (50, 50)),
                "Paladin": pygame.transform.scale(pygame.image.load(os.path.join('images', 'paladin.jpg')).convert_alpha(), (50, 50)),
                "Druid": pygame.transform.scale(pygame.image.load(os.path.join('images', 'druid.png')).convert_alpha(), (50, 50))
            }
            for img in hero_images.values():
                img.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            hero_images = {
                "Ogre": pygame.Surface((50, 50)).convert_alpha(),
                "Paladin": pygame.Surface((50, 50)).convert_alpha(),
                "Druid": pygame.Surface((50, 50)).convert_alpha()
            }
            hero_images["Ogre"].fill((100, 100, 100))
            hero_images["Paladin"].fill((150, 150, 150))
            hero_images["Druid"].fill((200, 200, 200))
        try:
            weapon_images = {
                "Sword": pygame.transform.scale(pygame.image.load(os.path.join('images', 'sword.jpg')).convert_alpha(), (50, 30)),
                "Double Axe": pygame.transform.scale(pygame.image.load(os.path.join('images', 'doublehandedaxe.jpg')).convert_alpha(), (50, 30)),
                "One Axe": pygame.transform.scale(pygame.image.load(os.path.join('images', 'onehandedaxe.jpg')).convert_alpha(), (50, 30)),
                "Bow": pygame.transform.scale(pygame.image.load(os.path.join('images', 'bow.png')).convert_alpha(), (50, 30))
            }
            for img in weapon_images.values():
                img.set_colorkey((255, 255, 255))
        except FileNotFoundError:
            weapon_images = {
                "Sword": pygame.Surface((50, 30)).convert_alpha(),
                "Double Axe": pygame.Surface((50, 30)).convert_alpha(),
                "One Axe": pygame.Surface((50, 30)).convert_alpha(),
                "Bow": pygame.Surface((50, 30)).convert_alpha()
            }
            weapon_images["Sword"].fill((255, 50, 50))
            weapon_images["Double Axe"].fill((255, 100, 100))
            weapon_images["One Axe"].fill((255, 150, 150))
            weapon_images["Bow"].fill((255, 200, 200))
        self.class_buttons = [
            Button(150, 100, 200, 60, "Ogre", (0, 0, 255), (100, 100, 255), hero_images["Ogre"]),
            Button(150, 170, 200, 60, "Paladin", (0, 0, 255), (100, 100, 255), hero_images["Paladin"]),
            Button(150, 240, 200, 60, "Druid", (0, 0, 255), (100, 100, 255), hero_images["Druid"])
        ]
        self.weapon_buttons = [
            Button(450, 100, 200, 50, "Sword", (255, 0, 0), (255, 100, 100), weapon_images["Sword"]),
            Button(450, 160, 200, 50, "Double Axe", (255, 0, 0), (255, 100, 100), weapon_images["Double Axe"]),
            Button(450, 220, 200, 50, "One Axe", (255, 0, 0), (255, 100, 100), weapon_images["One Axe"]),
            Button(450, 280, 200, 50, "Bow", (255, 0, 0), (255, 100, 100), weapon_images["Bow"])
        ]
        self.start_button = Button(325, 450, 150, 50, "Start Game", (0, 255, 0), (100, 255, 100))
        self.selected_class = None
        self.selected_weapon = None
        self.text_bg = pygame.Surface((200, 30)).convert_alpha()
        self.text_bg.fill((128, 128, 128))
        self.text_bg.set_alpha(128)

    def update(self, mouse_pos, mouse_click):
        for button in self.class_buttons:
            button.update(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                self.selected_class = button.text
        for button in self.weapon_buttons:
            button.update(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                self.selected_weapon = button.text
        self.start_button.update(mouse_pos)
        return self.start_button.is_clicked(mouse_pos, mouse_click) and self.selected_class and self.selected_weapon

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for button in self.class_buttons:
            button.draw(surface)
        for button in self.weapon_buttons:
            button.draw(surface)
        self.start_button.draw(surface)
        if self.selected_class:
            text = pygame.font.SysFont(None, 30).render(f"Selected Class: {self.selected_class}", True, (0, 0, 0))
            surface.blit(self.text_bg, (150, 400))
            surface.blit(text, (150, 400))
        if self.selected_weapon:
            text = pygame.font.SysFont(None, 30).render(f"Selected Weapon: {self.selected_weapon}", True, (0, 0, 0))
            surface.blit(self.text_bg, (450, 400))
            surface.blit(text, (450, 400))

class GameOver:
    def __init__(self, message):
        try:
            self.background = pygame.image.load(os.path.join('images', 'background1.jpg'))
            self.background = pygame.transform.scale(self.background, (800, 600)).convert()
        except FileNotFoundError:
            self.background = pygame.Surface((800, 600))
            self.background.fill((0, 100, 0))
        self.message = message
        self.exit_button = Button(800 // 2 - 75, 600 // 2, 150, 50, "Exit", (255, 0, 0), (255, 100, 100))

    def update(self, mouse_pos, mouse_click):
        self.exit_button.update(mouse_pos)
        if self.exit_button.is_clicked(mouse_pos, mouse_click):
            return "exit"
        return None

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        text = pygame.font.SysFont(None, 48).render(self.message, True, (0, 0, 0))
        surface.blit(text, (800 // 2 - text.get_width() // 2, 600 // 2 - 100))
        self.exit_button.draw(surface)

class VictoryScreen:
    def __init__(self):
        try:
            self.background = pygame.image.load(os.path.join('images', 'background1.jpg'))
            self.background = pygame.transform.scale(self.background, (800, 600)).convert()
        except FileNotFoundError:
            self.background = pygame.Surface((800, 600))
            self.background.fill((0, 100, 0))
        self.message = "Вітаємо! Ви перемогли!"
        self.exit_button = Button(800 // 2 - 75, 600 // 2, 150, 50, "Exit", (0, 255, 0), (100, 255, 100))

    def update(self, mouse_pos, mouse_click):
        self.exit_button.update(mouse_pos)
        if self.exit_button.is_clicked(mouse_pos, mouse_click):
            return "exit"
        return None

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        text = pygame.font.SysFont(None, 48).render(self.message, True, (0, 0, 0))
        surface.blit(text, (800 // 2 - text.get_width() // 2, 600 // 2 - 100))
        self.exit_button.draw(surface)

def draw_minimap(surface, game_manager):
    minimap_surface = pygame.Surface((100, 100))
    minimap_surface.fill((50, 50, 50))
    scale_x = 100 / 4000
    scale_y = 100 / 4000
    for unit in game_manager.units:
        if unit.dead:
            continue
        minimap_x = int(unit.x * scale_x)
        minimap_y = int(unit.y * scale_y)
        color = (0, 255, 0) if unit == game_manager.units[0] else (255, 0, 0)
        pygame.draw.circle(minimap_surface, color, (minimap_x, minimap_y), 2)
    for item in game_manager.items:
        minimap_x = int(item.x * scale_x)
        minimap_y = int(item.y * scale_y)
        pygame.draw.circle(minimap_surface, (255, 255, 0), (minimap_x, minimap_y), 1)
    for interactable in game_manager.interactables:
        if not interactable.used:
            minimap_x = int(interactable.x * scale_x)
            minimap_y = int(interactable.y * scale_y)
            pygame.draw.circle(minimap_surface, (255, 215, 0), (minimap_x, minimap_y), 1)
    surface.blit(minimap_surface, (800 - 110, 600 - 110))
    pygame.draw.rect(surface, (0, 0, 0), (800 - 110, 600 - 110, 100, 100), 2)

def draw_ui(surface, game_manager):
    if game_manager.selected_unit:
        info_text = [
            f"Тип: {game_manager.selected_unit.type}",
            f"Рівень: {game_manager.player_level}",
            f"HP: {game_manager.selected_unit.hp}/{game_manager.selected_unit.max_hp}",
            f"Шкода: {game_manager.selected_unit.damage}",
            f"Броня: {game_manager.selected_unit.armor}",
            f"Зброя: {game_manager.selected_unit.weapon.type if game_manager.selected_unit.weapon.type else 'Немає'}"
        ]
        info_y = 20
        for text in info_text:
            text_surface = pygame.font.SysFont(None, 24).render(text, True, (0, 0, 0))
            surface.blit(text_surface, (20, info_y))
            info_y += 25
    quest_text = []
    for quest in game_manager.mandatory_quests:
        progress = game_manager.quest_progress[quest["target_type"]]
        quest_text.append(f"Квест (обов’язковий): {quest['description']} ({progress}/{quest['target_count']})")
    for quest in game_manager.random_quests:
        progress = game_manager.quest_progress[quest.target_type]
        quest_text.append(f"Квест: {quest.description} ({progress}/{quest.target_count})")
    quest_y = 600 - 30 - 25 * len(quest_text)
    for text in quest_text:
        text_surface = pygame.font.SysFont(None, 24).render(text, True, (0, 0, 0))
        surface.blit(text_surface, (20, quest_y))
        quest_y += 25
    if game_manager.target_unit:
        target_info = [
            f"Ворог: {game_manager.target_unit.type}",
            f"HP: {game_manager.target_unit.hp}/{game_manager.target_unit.max_hp}",
            f"Шкода: {game_manager.target_unit.damage}",
            f"Броня: {game_manager.target_unit.armor}",
            f"Зброя: {game_manager.target_unit.weapon.type if game_manager.target_unit.weapon.type else 'Немає'}"
        ]
        info_y = 20
        for text in target_info:
            text_surface = pygame.font.SysFont(None, 24).render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topright=(800 - 50, info_y))
            surface.blit(text_surface, text_rect)
            info_y += 25
    turn_text = "Ваш хід" if game_manager.player_turn else "Хід противника"
    turn_surface = pygame.font.SysFont(None, 36).render(turn_text, True, (0, 0, 255) if game_manager.player_turn else (255, 0, 0))
    surface.blit(turn_surface, (800 // 2 - turn_surface.get_width() // 2, 20))
    if game_manager.message and not game_manager.game_over:
        message_surface = pygame.font.SysFont(None, 24).render(game_manager.message, True, (0, 0, 0))
        surface.blit(message_surface, (800 // 2 - message_surface.get_width() // 2, 600 - 30))
    draw_minimap(surface, game_manager)