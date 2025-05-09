import pygame
import sys
from game_manager import GameManager
from ui import Menu, GameOver, VictoryScreen, draw_ui

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гра з юнітами")

def main():
    clock = pygame.time.Clock()
    running = True
    state = "menu"
    menu = Menu()
    game = None
    game_over = None
    victory_screen = None
    while running:
        mouse_click = False
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
        if state == "menu":
            if menu.update(mouse_pos, mouse_click):
                game = GameManager(menu.selected_class, menu.selected_weapon)
                state = "game"
            screen.fill((255, 255, 255))
            menu.draw(screen)
        elif state == "game":
            game.update(keys, mouse_pos, mouse_click, events)
            if game.game_over:
                if game.victory:
                    victory_screen = VictoryScreen()
                    state = "victory"
                else:
                    game_over = GameOver(game.message)
                    state = "game_over"
            screen.fill((255, 255, 255))
            game.draw(screen)
            draw_ui(screen, game)
        elif state == "game_over":
            result = game_over.update(mouse_pos, mouse_click)
            if result == "exit":
                running = False
            screen.fill((255, 255, 255))
            game_over.draw(screen)
        elif state == "victory":
            result = victory_screen.update(mouse_pos, mouse_click)
            if result == "exit":
                running = False
            screen.fill((255, 255, 255))
            victory_screen.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()