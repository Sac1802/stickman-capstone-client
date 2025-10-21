import pygame
import os
import math
import threading
from login_screen.LoginScreen import send_encrypted_request, receive_encrypted_response

# ============================================
# CLASE Dashboard
# ============================================
class DashboardScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.connected_users = []
        self.t = 0 # contador de colores

        # UI Elements for Dashboard
        self.user_list_rect = pygame.Rect(50, 100, 300, 300)
        self.refresh_button = pygame.Rect(50, 420, 170, 40)
        self.invite_button = pygame.Rect(240, 420, 150, 40)
        self.selected_user_index = -1

        # New invitation related variables
        self.pending_invitation = None # Stores {'inviter_username': '...', 'gameId': '...'}
        self.invitation_response_message = None
        self.invitation_timer = 0

        # UI Elements for invitation response
        self.accept_button_rect = pygame.Rect(400, 250, 100, 40)
        self.decline_button_rect = pygame.Rect(520, 250, 100, 40)

        # New feedback variables for invite button
        self.invite_button_feedback_message = None
        self.invite_button_feedback_timer = 0


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
        elif message.get("type") == "GAME_INVITATION":
            payload = message.get("payload", {})
            inviter_username = payload.get("inviterUsername")
            game_id = payload.get("gameId")
            if inviter_username and game_id:
                self.pending_invitation = {'inviter_username': inviter_username, 'gameId': game_id}
                print(f"Received game invitation from {inviter_username} for game {game_id}")
        elif message.get("type") == "INVITATION_ACCEPTED":
            payload = message.get("payload", {})
            accepted_by = payload.get("acceptedBy")
            game_id = payload.get("gameId")
            if accepted_by and game_id:
                self.invitation_response_message = f"Invitation to {accepted_by} for game {game_id} accepted!"
                self.invitation_timer = 180 # Display for 3 seconds (30 FPS * 3 seconds)
                print(self.invitation_response_message)
                # Optionally, transition to game screen or update game state
                self.game.current_game_id = game_id # Set current game ID
                self.game.set_screen("combat") # Example: move to combat screen
        elif message.get("type") == "INVITATION_DENIED":
            payload = message.get("payload", {})
            denied_by = payload.get("deniedBy")
            game_id = payload.get("gameId")
            if denied_by and game_id:
                self.invitation_response_message = f"Invitation to {denied_by} for game {game_id} denied."
                self.invitation_timer = 180 # Display for 3 seconds
                print(self.invitation_response_message)

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
            game_id_to_invite = self.game.current_game_id if hasattr(self.game, 'current_game_id') else 0 # Valor por defecto si no está configurado

            request = {
                "type": "SEND_INVITATION",
                "payload": {
                    "invitedUsername": target_username,
                    "gameId": game_id_to_invite
                }
            }

            print(target_user)
            print(game_id_to_invite)

            send_encrypted_request(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)


            #threading.Thread(target=send_encrypted_request,
            #                 args=(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)).start()
            print(f"[Dashboard] Invitation request for {target_username} queued for sending.")
        else:
            print("[Dashboard] Client not connected or keys missing. Cannot send invitation.")

    def send_accept_invitation_request(self):
        if self.game.client_socket and self.game.aes_key and self.game.aes_iv and self.pending_invitation:
            request = {
                "type": "ACCEPT_INVITATION", # This is the type the client sends to the server
                "payload": {
                    "gameId": self.pending_invitation['gameId'],
                    "inviterUsername": self.pending_invitation['inviter_username']
                }
            }
            threading.Thread(target=send_encrypted_request,
                             args=(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)).start()
            self.pending_invitation = None # Clear the pending invitation after sending response
        else:
            print("[Dashboard] Cannot accept invitation: Client not connected, keys missing, or no pending invitation.")

    def send_deny_invitation_request(self):
        if self.game.client_socket and self.game.aes_key and self.game.aes_iv and self.pending_invitation:
            request = {
                "type": "DENY_INVITATION", # This is the type the client sends to the server
                "payload": {
                    "gameId": self.pending_invitation['gameId'],
                    "inviterUsername": self.pending_invitation['inviter_username']
                }
            }
            threading.Thread(target=send_encrypted_request,
                             args=(self.game.client_socket, request, self.game.aes_key, self.game.aes_iv)).start()
            self.pending_invitation = None # Clear the pending invitation after sending response
        else:
            print("[Dashboard] Cannot deny invitation: Client not connected, keys missing, or no pending invitation.")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pending_invitation: # If there's a pending invitation, handle its buttons
                if self.accept_button_rect.collidepoint(event.pos):
                    self.send_accept_invitation_request()
                elif self.decline_button_rect.collidepoint(event.pos):
                    self.send_deny_invitation_request()
            else: # Otherwise, handle regular dashboard buttons
                if self.refresh_button.collidepoint(event.pos):
                    self.send_get_connected_users_request()
                elif self.invite_button.collidepoint(event.pos):
                    if self.selected_user_index != -1 and self.selected_user_index < len(self.connected_users):
                        target_user = self.connected_users[self.selected_user_index]
                        print(f"[Dashboard] Invite button clicked. Attempting to send invitation to {target_user}.")
                        self.send_invite_request(target_user)
                        self.invite_button_feedback_message = f"Invitation sent to {target_user}!"
                        self.invite_button_feedback_timer = 90 # Display for 1.5 seconds (30 FPS * 1.5)
                    else:
                        print("[Dashboard] Invite button clicked, but no user selected or invalid selection.")
                        self.invite_button_feedback_message = "Please select a user to invite."
                        self.invite_button_feedback_timer = 90
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
        if self.invitation_timer > 0:
            self.invitation_timer -= 1
            if self.invitation_timer == 0:
                self.invitation_response_message = None # Clear message when timer runs out

        if self.invite_button_feedback_timer > 0:
            self.invite_button_feedback_timer -= 1
            if self.invite_button_feedback_timer == 0:
                self.invite_button_feedback_message = None # Clear message when timer runs out

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

        # Draw invite button feedback message
        if self.invite_button_feedback_message:
            feedback_text = self.font.render(self.invite_button_feedback_message, True, (255, 255, 0))
            screen.blit(feedback_text, (self.invite_button.x, self.invite_button.y - 30)) # Above the button

        # Draw pending invitation prompt
        if self.pending_invitation:
            inviter = self.pending_invitation['inviter_username']
            invite_msg = self.font.render(f"Invitation from {inviter}! Game ID: {self.pending_invitation['gameId']}", True, (255, 255, 0))
            screen.blit(invite_msg, (400, 200))

            pygame.draw.rect(screen, (0, 200, 0), self.accept_button_rect)
            accept_text = self.font.render("Accept", True, (255, 255, 255))
            screen.blit(accept_text, (self.accept_button_rect.x + 15, self.accept_button_rect.y + 10))

            pygame.draw.rect(screen, (200, 0, 0), self.decline_button_rect)
            decline_text = self.font.render("Decline", True, (255, 255, 255))
            screen.blit(decline_text, (self.decline_button_rect.x + 15, self.decline_button_rect.y + 10))

        # Draw invitation response message
        if self.invitation_response_message:
            response_msg = self.font.render(self.invitation_response_message, True, (255, 255, 255))
            screen.blit(response_msg, (400, 300))

        screen.blit(self.font.render("Dashboard", True, color), (50, 50))
