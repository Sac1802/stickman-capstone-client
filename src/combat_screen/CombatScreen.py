import os

import pygame
import socket
import json

class CombatScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        nature_5_path = os.path.join("static/sprites/enviroment/nature_5", "orig.png")
        self.background = pygame.image.load(nature_5_path).convert()

        player_skin = os.path.join("static/sprites/sprite_player/", "sprite_07.png")
        self.player_image = pygame.image.load(player_skin).convert()

        self.player_pos = pygame.Vector2(300, 300)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_screen("login")
            elif event.key == pygame.K_UP:
                self.player_pos.y -= 10
            elif event.key == pygame.K_LEFT:
                self.player_pos.x -= 10
            elif event.key == pygame.K_RIGHT:
                self.player_pos.x += 10

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        screen.blit(self.player_image, self.player_pos)
        screen.blit(self.player_image, self.player_pos)
        screen.blit(self.font.render("Juego de combate (ESC para salir)", True, (255,255,255)), (100, 100))
