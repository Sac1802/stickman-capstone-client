import pygame
import socket
import json
import os
from encryptAES import manageAES
from udp_service import udp_service
from game_over_screen.game_over_screen import Game_over_screen


class CombatScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)

        request = {
            "eventType": "PLAYER_JOIN_UDP",
            "IdPlayer": self.game.game_user_id
        }
        udp_service.send_message(request)
        print("Send udp services")
        nature_5_path = os.path.join("static/sprites/enviroment/nature_5", "orig.png")
        self.background = pygame.image.load(nature_5_path).convert()
        self.background = pygame.transform.scale(self.background, (800, 500))

        player_skin = os.path.join("static/sprites/sprite_player/", "sprite_07.png")
        self.player_image = pygame.image.load(player_skin).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (40, 100))

        self.attack_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("static/sprites/sprite_player/", "sprite_02.png")).convert_alpha(),
                (50, 100)),
            pygame.transform.scale(
                pygame.image.load(os.path.join("static/sprites/sprite_player/", "sprite_03.png")).convert_alpha(),
                (50, 100)),
            pygame.transform.scale(
                pygame.image.load(os.path.join("static/sprites/sprite_player/", "sprite_04.png")).convert_alpha(),
                (50, 100))
        ]

        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.2
        self.remotePlayerId = None

        self.player1_pos = pygame.Vector2(200, 380)
        self.player2_pos = pygame.Vector2(600, 380)

        self.player1_image = self.player_image
        self.player2_image = pygame.transform.flip(self.player_image, True, False)

        jump_skin = os.path.join("static/sprites/sprite_player/", "sprite_08.png")
        self.jump_image = pygame.image.load(jump_skin).convert_alpha()
        self.jump_image = pygame.transform.scale(self.jump_image, (50, 100))

        self.direction = ""
        self.playerId = self.game.game_user_id
        self.player1_health = 100
        self.player2_health = 100

        self.player1_velocity_y = 0
        self.player1_on_ground = True
        self.ground_level = 380
        self.gravity = 0.8
        self.jump_strength = -20

        self.moving_left = False
        self.moving_right = False

        self.player2_direction = 'left'

        self.send_udp_registration()

    def send_udp_registration(self):
        try:
            registration_data = {
                "eventType": "PLAYER_REGISTER",
                "idGame": self.game.current_game_id,
                "idPlayer": self.game.game_user_id
            }
            udp_service.send_message(registration_data)
            print(f"[CombatScreen] Sent UDP registration for game {self.game.current_game_id} and user {self.game.game_user_id}")
        except Exception as e:
            print(f"[CombatScreen] Error sending UDP registration: {e}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_screen("login")
            elif event.key == pygame.K_UP:
                if self.player1_on_ground:
                    self.player1_velocity_y = self.jump_strength
                    self.player1_on_ground = False

            elif event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
            elif event.key == pygame.K_SPACE:
                if not self.is_attacking:
                    self.is_attacking = True
                    self.attack_frame_index = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False

    def process_server_messages(self):
        server_data = udp_service.get_message()
        if not server_data:
            return

        event_type = server_data.get("eventType")

        if event_type == "PLAYER_MOVE":
            payload = server_data.get("payload", {})
            if server_data.get("IdPlayer") != self.playerId:
                self.remotePlayerId = server_data.get("IdPlayer")
                self.player2_pos.x = payload.get("x")
                self.player2_pos.y = payload.get("y")
                self.player2_direction = payload.get("direction")
                if self.player2_direction == "left":
                    self.player2_image = pygame.transform.flip(self.player_image, True, False)
                else:
                    self.player2_image = self.player_image

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
                winner = "You won!" if self.player1_health > 0 else "You Loss!"
                winnerId = self.playerId if self.player1_health > 0 else self.remotePlayerId
                print(f"Winner {winnerId}")
                if self.playerId == winnerId:
                    self.update_user_victories(winnerId)
                self.game.current_screen = Game_over_screen(self.game, winner)

    def update(self):
        self.process_server_messages()
        self.check_collisions()

        if self.is_attacking:
            self.attack_frame_index += self.attack_animation_speed
            if self.attack_frame_index >= len(self.attack_frames):
                self.is_attacking = False
                self.attack_frame_index = 0

        if self.moving_left:
            self.player1_pos.x -= 10
            self.direction = "left"
            self.player1_image = pygame.transform.flip(self.player_image, True, False)
            self.send_position(self.player1_pos.x, self.player1_pos.y)
        if self.moving_right:
            self.player1_pos.x += 10
            self.direction = "right"
            self.player1_image = self.player_image
            self.send_position(self.player1_pos.x, self.player1_pos.y)

        if not self.player1_on_ground:
            self.player1_velocity_y += self.gravity
            self.player1_pos.y += self.player1_velocity_y

        if self.player1_pos.y >= self.ground_level:
            self.player1_pos.y = self.ground_level
            self.player1_velocity_y = 0
            self.player1_on_ground = True

    def check_collisions(self):
        player1_rect = self.player1_image.get_rect(topleft=self.player1_pos)
        player2_rect = self.player2_image.get_rect(topleft=self.player2_pos)
        if player1_rect.colliderect(player2_rect) and self.is_attacking:
            self.send_attack()
            print("Collision detected!")

    def draw_health_bars(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.player1_pos.x - 25, self.player1_pos.y - 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.player1_pos.x - 25, self.player1_pos.y - 20, self.player1_health, 10))

        pygame.draw.rect(screen, (255, 0, 0), (self.player2_pos.x - 25, self.player2_pos.y - 20, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.player2_pos.x - 25, self.player2_pos.y - 20, self.player2_health, 10))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        if self.is_attacking:
            current_frame = self.attack_frames[int(self.attack_frame_index)]
            if self.direction == 'left':
                current_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(current_frame, self.player1_pos)
        else:
            screen.blit(self.player1_image, self.player1_pos)

        if self.player2_pos.y < self.ground_level:
            if self.player2_direction == 'left':
                flipped_jump = pygame.transform.flip(self.jump_image, True, False)
                screen.blit(flipped_jump, self.player2_pos)
            else:
                screen.blit(self.jump_image, self.player2_pos)
        else:
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

    def update_user_victories(self, winnerId):
        data_transfer = {
            "IdPlayer": self.playerId,
            "eventType": "UPDATE_USER_VIC",
            "payload": {
                "idWinn": winnerId
            }
        }
        print(data_transfer)
        udp_service.send_message(data_transfer)

