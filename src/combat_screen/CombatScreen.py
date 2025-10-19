import pygame
import socket
import json

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
