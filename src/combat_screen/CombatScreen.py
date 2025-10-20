import pygame
import socket
import json
from encryptAES import manageAES
from udp_service import udp_service

class CombatScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        nature_5_path = os.path.join("static/sprites/enviroment/nature_5", "orig.png")
        self.background = pygame.image.load(nature_5_path).convert()

        player_skin = os.path.join("static/sprites/sprite_player/", "sprite_07.png")
        self.player_image = pygame.image.load(player_skin).convert()

        self.player_pos = pygame.Vector2(300, 300)
        self.player1_pos = pygame.Vector2(200, 300)
        self.player2_pos = pygame.Vector2(600, 300)
        self.player2_image = pygame.transform.flip(self.player_image, True, False)

        self.direction = ""
        self.playerId = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_screen("login")

            elif event.key == pygame.K_UP:
                self.player1_pos.y -= 10
            elif event.key == pygame.K_LEFT:
                self.player1_pos.x -= 10
                self.direction = "left"
                self.send_position(self.player1_pos.x, self.player1_pos.y)
            elif event.key == pygame.K_RIGHT:
                self.player1_pos.x += 10
                self.direction = "right"
                self.send_position(self.player1_pos.x, self.player1_pos.y)

    def handled_player2(self):
        positions = udp_service.return_value()
        self.player2_pos.x = positions["positionX"]
        self.player2_pos.y = positions["positionY"]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.player_image, self.player1_pos)
        screen.blit(self.player2_image, self.player2_pos)

        text = self.font.render("Juego de combate (ESC para salir)", True, (255,255,255))
        screen.blit(text, (100, 100))

    def send_position(self, positionX, positionY):
        data_transfer = {
            "IdPlayer": self.playerId,
            "eventType": "PLAYER_MOVE",
            "payload": {
                "x": positionX,
                "y": positionY,
                "direction": self.direction
            }
        }
        value_encrypt = manageAES.encrypt(data_transfer)
        udp_service.send_message(value_encrypt)
