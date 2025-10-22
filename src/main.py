
from login_screen.LoginScreen import LoginScreen
from register_screen.RegisterScreen import RegisterScreen
from combat_screen.CombatScreen import CombatScreen
from code_screen.CodeScreen import CodeScreen
from dashboard.dashboardScreen import DashboardScreen
from menu.Menu import Menu
from tcp_listener import TcpListener

import pygame
import socket
import json
import threading
import base64
import queue # Import the queue module

pygame.init()
pygame.mixer.init()

def fix_base64_padding(b64_str: str) -> str:
    """Corrige el padding base64 si falta (= o ==)."""
    b64_str = b64_str.strip()
    missing = len(b64_str) % 4
    if missing:
        b64_str += "=" * (4 - missing)
    return b64_str

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Juego con pantallas")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_user_id = 0
        self.game_username = None
        self.client_socket = None
        self.aes_key = None
        self.aes_iv = None
        self.tcp_listener_thread = None
        self.message_queue = queue.Queue() # Initialize the message queue

        # Establish persistent TCP connection and receive AES keys
        try:
            host = "127.0.0.1"
            port = 5000
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            print("Conectado al servidor TCP.")

            raw_data = self.client_socket.recv(4096).decode().strip()
            print(f" Datos recibidos del servidor: {raw_data}")

            clean_data = raw_data.replace("\\u003d", "=").replace('"', "")
            key_b64, iv_b64 = [x.strip() for x in clean_data.split(":")]

            key_b64 = fix_base64_padding(key_b64)
            iv_b64 = fix_base64_padding(iv_b64)

            self.aes_key = base64.b64decode(key_b64)
            self.aes_iv = base64.b64decode(iv_b64)

            print(f"Clave AES (bytes): {len(self.aes_key)} bytes")
            print(f"IV (bytes): {len(self.aes_iv)} bytes")

        except Exception as e:
            print(f"Error establishing initial connection or receiving keys: {e}")
            self.running = False # Stop game if connection fails

        self.screens = {
            "login": LoginScreen(self),
            "register": RegisterScreen(self),
            "code": CodeScreen(self),
            "combat": CombatScreen(self),
            "dashboard": DashboardScreen(self),
            "menu" : Menu(self)
        }
        self.current_screen = self.screens["login"]

    def set_screen(self, name):
        if name == "dashboard" and self.tcp_listener_thread is None:
            self.tcp_listener_thread = TcpListener(self, self.client_socket, self.aes_key, self.aes_iv, self.message_queue)
            self.tcp_listener_thread.start()
            # Send initial GET_CONNECTED_USERS request after listener starts
            self.screens["dashboard"].send_get_connected_users_request()
        self.current_screen = self.screens[name]

    def run(self):
        while self.running:
            # Process messages from the queue in the main thread
            while not self.message_queue.empty():
                message = self.message_queue.get()
                if self.current_screen and hasattr(self.current_screen, 'handle_server_message'):
                    self.current_screen.handle_server_message(message)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)

            self.current_screen.update()
            self.current_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

        if self.tcp_listener_thread:
            self.tcp_listener_thread.stop()
            self.tcp_listener_thread.join()

        # Close the client socket
        if self.client_socket:
            self.client_socket.close()
            print("[Game] Client socket closed.")


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
