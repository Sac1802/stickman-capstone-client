import pygame
import socket
import json
import os
from encryptAES import manageAES
from udp_service import udp_service

class CombatScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        nature_5_path = os.path.join("static/sprites/enviroment/nature_5", "orig.png")
        self.background = pygame.image.load(nature_5_path).convert()

        player_skin = os.path.join("static/sprites/sprite_player/", "sprite_07.png")
        self.player_image = pygame.image.load(player_skin).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (50, 100))

        self.player1_pos = pygame.Vector2(200, 300)
        self.player2_pos = pygame.Vector2(600, 300)
        self.player2_image = pygame.transform.flip(self.player_image, True, False)

        self.direction = ""
        self.playerId = self.game.game_user_id
        self.player1_health = 100
        self.player2_health = 100

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
            elif event.key == pygame.K_SPACE:
                self.send_attack()

    def process_server_messages(self):
        server_data = udp_service.get_message()
        if not server_data:
            return

        event_type = server_data.get("eventType")

        if event_type == "PLAYER_MOVE":
            payload = server_data.get("payload", {})
            if server_data.get("IdPlayer") != self.playerId:
                self.player2_pos.x = payload.get("x")
                self.player2_pos.y = payload.get("y")

        elif event_type == "DAMAGE_DEALT":
            payload = server_data.get("payload", {})
            target_id = payload.get("targetId")
            new_health = payload.get("newHealth")
            is_game_over = payload.get("isGameOver")

            if target_id == self.playerId:
                self.player1_health = new_health
            else:
                self.player2_health = new_health

            if is_game_over:
                print("¡Juego terminado!")
                self.game.set_screen("login")

    def update(self):
        self.process_server_messages()

    def draw_health_bars(self, screen):
        # Barra de vida Jugador 1
        pygame.draw.rect(screen, (255, 0, 0), (self.player1_pos.x - 25, self.player1_pos.y - 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.player1_pos.x - 25, self.player1_pos.y - 20, self.player1_health, 10))

        # Barra de vida Jugador 2
        pygame.draw.rect(screen, (255, 0, 0), (self.player2_pos.x - 25, self.player2_pos.y - 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.player2_pos.x - 25, self.player2_pos.y - 20, self.player2_health, 10))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.player_image, self.player1_pos)
        screen.blit(self.player2_image, self.player2_pos)
        self.draw_health_bars(screen)

        text = self.font.render("Juego de combate (ESC para salir)", True, (255, 255, 255))
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
        udp_service.send_message(data_transfer)

    def send_attack(self):
        data_transfer = {
            "IdPlayer": self.playerId,
            "eventType": "PLAYER_ATTACK",
            "payload": {}
        }
        udp_service.send_message(data_transfer)