
from login_screen.LoginScreen import LoginScreen
from register_screen.RegisterScreen import RegisterScreen
from combat_screen.CombatScreen import CombatScreen
from code_screen.CodeScreen import CodeScreen
#from dashboard.DashboardScreen import DashboardScreen

import pygame
import socket
import json

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Juego con pantallas")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_user_id = 0
        self.game_user_email = ""

        self.screens = {
            "login": LoginScreen(self),
            "register": RegisterScreen(self),
            "code": CodeScreen(self),
            "combat": CombatScreen(self),
            #"dashboard": DashboardScreen(self)
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
