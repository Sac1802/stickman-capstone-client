import pygame
import os
import math
import threading
from login_screen.LoginScreen import send_encrypted_request, receive_encrypted_response

class DashboardScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.connected_users = []
        self.t = 0 # contador de colores

        # UI Elements for Dashboard
        self.user_list_rect = pygame.Rect(50, 100, 300, 300)
        self.refresh_button = pygame.Rect(50, 420, 150, 40)
        self.invite_button = pygame.Rect(210, 420, 150, 40)
        self.selected_user_index = -1

    def handle_server_message(self, message):
        if "users" in message:
            users = message.get("users", [])
            # Filter out the current user by username
            self.connected_users = [user for user in users if user != self.game.game_username]
        elif message.get("type") == "USER_CONNECTED":
            user = message.get("payload", {}).get("username")
            if user and user != self.game.game_username and user not in self.connected_users:
                self.connected_users.append(user)
        elif message.get("type") == "USER_DISCONNECTED":
            user = message.get("payload", {}).get("username")
            if user and user != self.game.game_username and user in self.connected_users:
                self.connected_users.remove(user)

    def send_get_connected_users_request(self):
        if self.game.client_socket and self.game.aes_key and self.game.aes_iv:
            request = {
                "type": "get_online_users",
                "payload": {}
            }
            # Send in a new thread to avoid blocking the UI
            threading.Thread(target=send_encrypted_request,
                             args=(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)).start()
        else:
            print("[Dashboard] Client not connected or keys missing.")

    def send_invite_request(self, target_username):
        if self.game.client_socket and self.game.aes_key and self.game.aes_iv:
            request = {
                "type": "INVITE",
                "payload": {"target_username": target_username}
            }
            threading.Thread(target=send_encrypted_request,
                             args=(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)).start()
        else:
            print("[Dashboard] Client not connected or keys missing.")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.refresh_button.collidepoint(event.pos):
                self.send_get_connected_users_request()
            elif self.invite_button.collidepoint(event.pos):
                if self.selected_user_index != -1 and self.selected_user_index < len(self.connected_users):
                    target_user = self.connected_users[self.selected_user_index]
                    self.send_invite_request(target_user)
            elif self.user_list_rect.collidepoint(event.pos):
                # Handle user selection from the list
                mouse_y = event.pos[1]
                item_height = 30 # Assuming each user item is 30 pixels high
                relative_y = mouse_y - self.user_list_rect.y
                self.selected_user_index = relative_y // item_height
                if self.selected_user_index >= len(self.connected_users):
                    self.selected_user_index = -1 # Deselect if clicked outside valid user

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Optionally go back to login or exit
            self.game.set_screen("login")

    def update(self):
        pass

    def draw(self, screen):
        self.t += 1

        screen.fill((50, 50, 80))

        border_thickness = 8
        w, h = screen.get_size()

        # Generar color animado tipo arcoiris
        r = int(128 + 127 * math.sin(self.t * 0.05))
        g = int(128 + 127 * math.sin(self.t * 0.05 + 2))
        b = int(128 + 127 * math.sin(self.t * 0.05 + 4))
        color = (r, g, b)

         # Dibujar rectángulos de borde
        pygame.draw.rect(screen, color, (0, 0, w, border_thickness))          # arriba
        pygame.draw.rect(screen, color, (0, h-border_thickness, w, border_thickness)) # abajo
        pygame.draw.rect(screen, color, (0, 0, border_thickness, h))          # izquierda
        pygame.draw.rect(screen, color, (w-border_thickness, 0, border_thickness, h)) # derecha

        # Draw user list background
        pygame.draw.rect(screen, (30, 30, 30), self.user_list_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.user_list_rect, 2) # Border

        # Draw connected users
        y_offset = self.user_list_rect.y + 5
        for i, user in enumerate(self.connected_users):
            text_color = (255, 255, 255)
            if i == self.selected_user_index:
                pygame.draw.rect(screen, (70, 70, 100), (self.user_list_rect.x + 2, y_offset - 2, self.user_list_rect.width - 4, 30))
                text_color = (255, 255, 0) # Highlight selected user
            user_text = self.font.render(user, True, text_color)
            screen.blit(user_text, (self.user_list_rect.x + 10, y_offset))
            y_offset += 30

        # Draw buttons
        pygame.draw.rect(screen, (100, 100, 200), self.refresh_button)
        refresh_text = self.font.render("Refresh Users", True, (255, 255, 255))
        screen.blit(refresh_text, (self.refresh_button.x + 10, self.refresh_button.y + 10))

        pygame.draw.rect(screen, (100, 200, 100), self.invite_button)
        invite_text = self.font.render("Invite", True, (255, 255, 255))
        screen.blit(invite_text, (self.invite_button.x + 40, self.invite_button.y + 10))

        screen.blit(self.font.render("Dashboard", True, color), (50, 50))