
from login_screen.LoginScreen import LoginScreen
from register_screen.RegisterScreen import RegisterScreen

import pygame
import socket
import json

pygame.init()

class CombatScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen("login")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.font.render("Juego de combate (ESC para salir)", True, (255,255,255)), (100, 100))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Juego con pantallas")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screens = {
            "login": LoginScreen(self),
            "register": RegisterScreen(self),
            "combat": CombatScreen(self)
        }
        self.current_screen = self.screens["login"]

    def set_screen(self, name):
        self.current_screen = self.screens[name]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)

            self.current_screen.update()
            self.current_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
