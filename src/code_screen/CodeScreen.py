import pygame
import os
import math
import socket
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ============================================
# CONSTANTES Y UTILIDADES DE CLAVE AES
# ============================================

KEY_FILE = "aes_keys.json"

# -------------------------------
#  Guardar y cargar claves AES
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
#  Encriptar / Desencriptar
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
#  Enviar y recibir mensajes
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
# CLASE CodeScreen
# ============================================
class CodeScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.code = ""
        self.active_field = None
        self.t = 0 # contador de colores

        # Titulo
        title_path = os.path.join("static", "title.png")
        self.title_img = pygame.image.load(title_path).convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (200, 150))

        # text field position
        self.input_box_code = pygame.Rect(260, 250, 300, 32)

        # Botones
        self.code_button = pygame.Rect(340, 340, 130, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box_code.collidepoint(event.pos):
                self.active_field = "code"
            elif self.code_button.collidepoint(event.pos):
                self.verify_code()
            else:
                self.active_field = None

        elif event.type == pygame.KEYDOWN:
            if self.active_field == "code":
                if event.key == pygame.K_BACKSPACE:
                    self.code = self.code[:-1]
                else:
                    self.code += event.unicode

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen("register")

    def update(self):
        pass

    def draw(self, screen):
        self.t += 1;

        screen.fill((50, 50, 80))

        #Title image
        screen.blit(self.title_img, (300, 20))

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

         # Labels
        screen.blit(self.font.render("Ingresar Codigo", True, (200,200,200)), (320, 210))

        # Cajas
        pygame.draw.rect(screen, (200,200,200), self.input_box_code)

        # Boton
        pygame.draw.rect(screen, (100,100,200), self.code_button)

        # Texto en cajas
        screen.blit(self.font.render(self.code, True, (255,255,255)), (self.input_box_code.x+5, self.input_box_code.y+5))

        # Botones
        screen.blit(self.font.render("send code", True, (255,255,122)), (self.code_button.x+10, self.code_button.y+10))

        # Regresar a registro
        screen.blit(self.font.render("Pantalla de validacion de codigo (ESC para volver)", True, color), (50, 440))

    def verify_code(self):

        client, key, iv = connect_to_server()

        request = {
            "type": "verify_code",
            "payload": {"code": self.code, "email": self.game.game_user_email}
        }

        # Enviar la solicitud cifrada
        send_encrypted_request(client, request, key, iv)

        # Recibir y descifrar la respuesta
        response = receive_encrypted_response(client, key, iv)
        print("Respuesta del servidor:", response)

