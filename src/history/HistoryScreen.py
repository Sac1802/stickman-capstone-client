import pygame
import math
import json
import base64
import socket
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ============================================
# AES y conexión
# ============================================

KEY_FILE = "aes_keys.json"


def save_aes_keys(key_b64, iv_b64, path=KEY_FILE):
    data = {"key": key_b64, "iv": iv_b64}
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f" Claves guardadas en {path}")


def load_aes_keys(path=KEY_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError("⚠️ No existe el archivo de claves AES.")
    with open(path, "r") as f:
        data = json.load(f)
    return data["key"], data["iv"]


def connect_to_server(host="127.0.0.1", port=5000, save_keys=True):
    def fix_base64_padding(b64_str: str) -> str:
        b64_str = b64_str.strip()
        missing = len(b64_str) % 4
        if missing:
            b64_str += "=" * (4 - missing)
        return b64_str

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Conectado al servidor TCP.")

    raw_data = client.recv(4096).decode().strip()
    clean_data = raw_data.replace("\\u003d", "=").replace('"', "")
    key_b64, iv_b64 = [x.strip() for x in clean_data.split(":")]

    key_b64 = fix_base64_padding(key_b64)
    iv_b64 = fix_base64_padding(iv_b64)

    key_bytes = base64.b64decode(key_b64)
    iv_bytes = base64.b64decode(iv_b64)

    if save_keys:
        save_aes_keys(key_b64, iv_b64)

    return client, key_bytes, iv_bytes


def encrypt_aes(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()


def decrypt_aes(encrypted_b64, key, iv):
    ciphertext = base64.b64decode(encrypted_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()


def send_encrypted_request(client, request_obj, key, iv):
    json_str = json.dumps(request_obj)
    encrypted = encrypt_aes(json_str, key, iv) + "\n"
    client.sendall(encrypted.encode())


def receive_encrypted_response(client, key, iv):
    data = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        data += chunk
        if b"\n" in data:
            break
    encrypted_b64 = data.decode().strip()
    decrypted_json = decrypt_aes(encrypted_b64, key, iv)
    return json.loads(decrypted_json)


# ============================================
# CLASE HISTORY SCREEN (REDISEÑADA)
# ============================================
class HistoryScreen:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)
        self.t = 0
        self.history_button = pygame.Rect(230, 120, 220, 50)

        self.history_data = []
        self.status_message = "Presiona el botón para cargar el historial."
        self.loading = False

    # ===============================
    # EVENTOS
    # ===============================
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.history_button.collidepoint(event.pos):
                self.request()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen("menu")

    # ===============================
    # ACTUALIZAR
    # ===============================
    def update(self):
        self.t += 1

    # ===============================
    # DIBUJAR
    # ===============================
    def draw(self, screen):
        w, h = screen.get_size()
        screen.fill((30, 30, 50))

        # Color animado arcoíris
        r = int(128 + 127 * math.sin(self.t * 0.05))
        g = int(128 + 127 * math.sin(self.t * 0.05 + 2))
        b = int(128 + 127 * math.sin(self.t * 0.05 + 4))
        neon_color = (r, g, b)

        # Bordes animados
        border = 8
        pygame.draw.rect(screen, neon_color, (0, 0, w, border))
        pygame.draw.rect(screen, neon_color, (0, h-border, w, border))
        pygame.draw.rect(screen, neon_color, (0, 0, border, h))
        pygame.draw.rect(screen, neon_color, (w-border, 0, border, h))

        # Título
        title = self.font_title.render("Match History", True, neon_color)
        screen.blit(title, (50, 50))

        # Botón con hover
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.history_button.collidepoint(mouse_pos)
        btn_color = (130, 130, 255) if hovered else (90, 90, 200)
        pygame.draw.rect(screen, btn_color, self.history_button, border_radius=10)
        text = self.font.render("Cargar historial", True, (255, 255, 255))
        screen.blit(text, (self.history_button.x + 20, self.history_button.y + 10))

        # Cuadro de tabla
        table_rect = pygame.Rect(100, 220, w - 200, h - 300)
        pygame.draw.rect(screen, (40, 40, 70, 180), table_rect, border_radius=12)
        pygame.draw.rect(screen, neon_color, table_rect, 2, border_radius=12)

        # Contenido de tabla
        y = table_rect.y + 30

        if self.loading:
            loading_txt = self.font.render("Cargando...", True, (255, 255, 255))
            screen.blit(loading_txt, (table_rect.x + 30, y))
            return

        if not self.history_data:
            msg = self.font.render(self.status_message, True, (200, 200, 200))
            screen.blit(msg, (table_rect.x + 30, y))
            return

        # Cabecera
        headers = self.font.render("Usuario".ljust(20) + "Victorias", True, neon_color)
        screen.blit(headers, (table_rect.x + 30, y))
        y += 30
        pygame.draw.line(screen, neon_color, (table_rect.x + 20, y), (table_rect.x + table_rect.width - 20, y), 2)
        y += 10

        # Filas
        for item in self.history_data:
            username = item.get("username", "")
            wins = str(item.get("userMatchWinQuantity", 0))
            row = self.small_font.render(f"{username:<18}  {wins}", True, (220, 220, 255))
            screen.blit(row, (table_rect.x + 40, y))
            y += 30

    # ===============================
    # SOLICITAR HISTORIAL
    # ===============================
    def request(self):
        try:
            self.loading = True
            self.status_message = "Solicitando datos..."
            pygame.display.flip()  # Actualiza pantalla mientras carga

            client, key, iv = connect_to_server()

            request = {
                "type": "GET_PLAYER_RANK",
                "payload": {"username": "", "password": ""}
            }

            send_encrypted_request(client, request, key, iv)
            response = receive_encrypted_response(client, key, iv)

            # Guardar datos y mensaje
            self.history_data = response
            self.status_message = "Historial cargado correctamente."
            print("Historial recibido:", response)

        except Exception as e:
            self.status_message = f"Error: {e}"
            print("❌ Error solicitando historial:", e)
        finally:
            self.loading = False
