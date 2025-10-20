import pygame
import socket
import json

import encryptAES.manageAES
import udp_service.udp_service
direction = ""
playerId = ""

class CombatScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        self.background = pygame.image.load(
            "/home/sac/Downloads/clientCN2/pygame-stick-game/src/sprites/enviroment/nature_5/orig.png"
        ).convert()

        self.player_image = pygame.image.load(
            "/home/sac/Downloads/clientCN2/pygame-stick-game/src/sprites/sprite_player/sprite_07.png"
        ).convert_alpha()

        self.player1_pos = pygame.Vector2(200, 300)
        self.player2_pos = pygame.Vector2(600, 300)

        self.player2_image = pygame.transform.flip(self.player_image, True, False)

    def handle_event(self, event):
        global direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_screen("login")

            elif event.key == pygame.K_UP:
                self.player1_pos.y -= 10
            elif event.key == pygame.K_LEFT:
                self.player1_pos.x -= 10
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.player1_pos.x += 10
                direction = "right"

    def handled_player2(self):
        positions = udp_service.udp_service.return_value()
        self.player2_pos.x = positions["positionX"]
        self.player2_pos.y = positions["positionY"]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.player_image, self.player1_pos)

        screen.blit(self.player2_image, self.player2_pos)

        # Texto
        text = self.font.render("Juego de combate (ESC para salir)", True, (255,255,255))
        screen.blit(text, (100, 100))

    def send_position(self):
        global playerId
        data_transfer = {
            "IdPlayer": playerId,
            "eventType": "PLAYER_MOVE",
            "payload": {
                "x": self.player1_pos.x,
                "y": self.player1_pos.y,
                "direction": direction
            }
        }
        


