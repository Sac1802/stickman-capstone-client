import pygame
import os
import socket
import math
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ============================================
# CONSTANTES Y UTILIDADES DE CLAVE AES
# ============================================

KEY_FILE = "aes_keys.json"

# -------------------------------
# 🔒 Guardar y cargar claves AES
# -------------------------------

def save_aes_keys(key_b64, iv_b64, path=KEY_FILE):
    """
    Guarda las claves AES directamente en formato Base64,
    tal como las envía el servidor.
    """
    data = {
        "key": key_b64,
        "iv": iv_b64
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f" Claves guardadas en {path}")

def load_aes_keys(path=KEY_FILE):
    """
    Carga las claves AES (en Base64) del archivo.
    No las decodifica, simplemente las devuelve tal cual.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("⚠️ No existe el archivo de claves AES.")
    with open(path, "r") as f:
        data = json.load(f)
    return data["key"], data["iv"]


# -------------------------------
#  Conexión con servidor
# -------------------------------

def connect_to_server(host="127.0.0.1", port=5000, save_keys=True):
    import base64
    import socket

    def fix_base64_padding(b64_str: str) -> str:
        """Corrige el padding base64 si falta (= o ==)."""
        b64_str = b64_str.strip()
        missing = len(b64_str) % 4
        if missing:
            b64_str += "=" * (4 - missing)
        return b64_str

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Conectado al servidor TCP.")

    # Recibir mensaje inicial "key:iv"
    raw_data = client.recv(4096).decode().strip()
    print(f" Datos recibidos del servidor: {raw_data}")

    # Limpiar escapes si vienen de JSON (\u003d)
    clean_data = raw_data.replace("\\u003d", "=").replace('"', "")
    key_b64, iv_b64 = [x.strip() for x in clean_data.split(":")]

    # Corregir padding si falta
    key_b64 = fix_base64_padding(key_b64)
    iv_b64 = fix_base64_padding(iv_b64)

    # Decodificar desde base64
    key_bytes = base64.b64decode(key_b64)
    iv_bytes = base64.b64decode(iv_b64)

    print(f"Clave AES (bytes): {len(key_bytes)} bytes")
    print(f"IV (bytes): {len(iv_bytes)} bytes")

    if save_keys:
        save_aes_keys(key_b64, iv_b64)
        print(f" Claves guardadas en aes_keys.json")

    return client, key_bytes, iv_bytes

# -------------------------------
# 🔐 Encriptar / Desencriptar
# -------------------------------

def encrypt_aes(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt_aes(encrypted_b64, key, iv):
    ciphertext = base64.b64decode(encrypted_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# -------------------------------
# 🚀 Enviar y recibir mensajes
# -------------------------------

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

    print(f"Respuesta cifrada recibida (raw): '{encrypted_b64}'")

    decrypted_json = decrypt_aes(encrypted_b64, key, iv)
    return json.loads(decrypted_json)

# ============================================
# CLASE LoginScreen
# ============================================

class LoginScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.username = ""
        self.password = ""
        self.active_field = None
        self.orange = (250, 140, 0)
        self.light_green = (180, 238, 144)
        self.t = 0  # contador para animación del borde

        # Background
        bg_path = os.path.join("static", "DR06vu.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (800, 500))

        # Título
        title_path = os.path.join("static", "title.png")
        self.title_img = pygame.image.load(title_path).convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (300, 150))

        # Sonido de boton
        sound_path = os.path.join("static", "button.wav")
        if os.path.exists(sound_path):
            self.button_sound = pygame.mixer.Sound(sound_path)
            self.button_sound.set_volume(1.0)
        else:
            self.button_sound = None

        # Cajas de texto
        self.input_box_user = pygame.Rect(330, 200, 200, 32)
        self.input_box_pass = pygame.Rect(330, 250, 200, 32)

        # Botones
        self.login_button = pygame.Rect(300, 320, 100, 40)
        self.register_button = pygame.Rect(410, 320, 100, 40)
        self.combat_button = pygame.Rect(410, 370, 100, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box_user.collidepoint(event.pos):
                self.active_field = "user"
            elif self.input_box_pass.collidepoint(event.pos):
                self.active_field = "pass"
            elif self.login_button.collidepoint(event.pos):
                self.login()
            elif self.register_button.collidepoint(event.pos):
                if self.button_sound:
                    self.button_sound.play()
                    self.game.set_screen("register")
            elif self.combat_button.collidepoint(event.pos):
                self.game.set_screen("combat")

            else:
                self.active_field = None

        elif event.type == pygame.KEYDOWN:
            if self.active_field == "user":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_field == "pass":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        self.t += 1
        screen.fill((30, 30, 30))

        w, h = screen.get_size()
        border_thickness = 8

        # Animación arcoíris del borde
        r = max(0, min(255, int(128 + 127 * math.sin(self.t * 0.05))))
        g = max(0, min(255, int(128 + 127 * math.sin(self.t * 0.05 + 2))))
        b = max(0, min(255, int(128 + 127 * math.sin(self.t * 0.05 + 4))))
        color = (r, g, b)

        screen.blit(self.background, (0, 0))
        screen.blit(self.title_img, (250, 20))

        pygame.draw.rect(screen, color, (0, 0, w, border_thickness))
        pygame.draw.rect(screen, color, (0, h - border_thickness, w, border_thickness))
        pygame.draw.rect(screen, color, (0, 0, border_thickness, h))
        pygame.draw.rect(screen, color, (w - border_thickness, 0, border_thickness, h))

        text_color = self.orange if (self.t // 30) % 2 == 0 else self.light_green

        screen.blit(self.font.render("Usuario:", True, text_color), (220, 200))
        screen.blit(self.font.render("Contraseña:", True, text_color), (180, 250))

        pygame.draw.rect(screen, text_color, self.input_box_user)
        pygame.draw.rect(screen, text_color, self.input_box_pass)
        pygame.draw.rect(screen, (100, 100, 200), self.login_button)
        pygame.draw.rect(screen, (100, 100, 200), self.register_button)
        pygame.draw.rect(screen, (100, 100, 200), self.combat_button)

        screen.blit(self.font.render("By Said, Cristian and Leonardo", True, text_color), (220, 430))
        screen.blit(self.font.render(self.username, True, (255, 255, 255)),
                    (self.input_box_user.x + 5, self.input_box_user.y + 5))
        screen.blit(self.font.render("*" * len(self.password), True, (255, 255, 255)),
                    (self.input_box_pass.x + 5, self.input_box_pass.y + 5))

        screen.blit(self.font.render("Login", True, (0, 0, 0)),
                    (self.login_button.x + 20, self.login_button.y + 10))
        screen.blit(self.font.render("Register", True, (0, 0, 0)),
                    (self.register_button.x + 10, self.register_button.y + 10))

        # boton de prueba para said
        screen.blit(self.font.render("saidfi", True, (0, 0, 0)),
                    (self.combat_button.x + 20, self.combat_button.y + 10))

    def login(self):
        try:
            # Conectarse y obtener claves YA decodificadas (bytes)
            client, key, iv = connect_to_server()

            # Crear el request de login
            request = {
                "type": "login",
                "payload": {"username": self.username, "password": self.password}
            }

            # Enviar la solicitud cifrada
            send_encrypted_request(client, request, key, iv)

            # Recibir y descifrar la respuesta
            response = receive_encrypted_response(client, key, iv)

            print("Respuesta del servidor:", response)
            self.game.game_user_id = response.get("userId")

            print(f"USERID: {self.game.game_user_id}")

            self.game.set_screen("dashboard")

            client.close()

        except Exception as e:
            print(f"Error en login: {e}")
