import pygame
import os
import socket
import math
import json

class LoginScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.username = ""
        self.password = ""
        self.active_field = None
        self.orange = (250, 140, 0)
        self.light_green = (180, 238, 144)
        self.button_sound = pygame.mixer.Sound("static/button.wav")
        self.t = 0 # contador de animaciones del borde

        bg_path = os.path.join("static", "DR06vu.png")
        self.background = pygame.image.load(bg_path).convert()

        # titulo
        title_path = os.path.join("static", "title.png")
        self.title_img = pygame.image.load(title_path).convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (300, 150))

        # Ajustar al tamaño de la ventana
        self.background = pygame.transform.scale(self.background, (800, 500))

        # reproducir musica
        #music_path = os.path.join("static", "login.mp3")
        # pygame.mixer.music.load(music_path)
        # pygame.mixer.music.set_volume(0.7)
        # pygame.mixer.music.play(-1)

        # sonido del boton
        self.button_sound.set_volume(1.0)

        # text field position
        self.input_box_user = pygame.Rect(330, 200, 200, 32)
        self.input_box_pass = pygame.Rect(330, 250, 200, 32)

        # buttons position
        self.login_button = pygame.Rect(300, 320, 100, 40)
        self.register_button = pygame.Rect(410, 320, 100, 40)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box_user.collidepoint(event.pos):
                self.active_field = "user"
            elif self.input_box_pass.collidepoint(event.pos):
                self.active_field = "pass"
            elif self.login_button.collidepoint(event.pos):
                self.login()
            elif self.register_button.collidepoint(event.pos):
                self.button_sound.play()
                self.game.set_screen("register")
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
        pass  # lógica extra si necesitas

    def draw(self, screen):
        self.t += 1

        screen.fill((30, 30, 30))

        border_thickness = 8
        w, h = screen.get_size()

        # Generar color animado tipo arcoiris
        r = int(128 + 127 * math.sin(self.t * 0.05))
        g = int(128 + 127 * math.sin(self.t * 0.05 + 2))
        b = int(128 + 127 * math.sin(self.t * 0.05 + 4))
        color = (r, g, b)

        # background
        screen.blit(self.background, (0, 0))

        #Title image
        screen.blit(self.title_img, (250, 20))

        # Dibujar rectángulos de borde
        pygame.draw.rect(screen, color, (0, 0, w, border_thickness))          # arriba
        pygame.draw.rect(screen, color, (0, h-border_thickness, w, border_thickness)) # abajo
        pygame.draw.rect(screen, color, (0, 0, border_thickness, h))          # izquierda
        pygame.draw.rect(screen, color, (w-border_thickness, 0, border_thickness, h)) # derecha

        # calculando el color para las letras
        if (self.t // 30) % 2 == 0:
            text_color = self.orange
        else:
            text_color = self.light_green

        # Labels
        screen.blit(self.font.render("Usuario :", True, text_color), (220, 200))
        screen.blit(self.font.render("Contraseña:", True, text_color), (180, 250))

        # Cajas
        pygame.draw.rect(screen, text_color, self.input_box_user)
        pygame.draw.rect(screen, text_color, self.input_box_pass)

        # Botones
        pygame.draw.rect(screen, (100,100,200), self.login_button)
        pygame.draw.rect(screen, (100,100,200), self.register_button)

        # Creadores
        screen.blit(self.font.render("By Said, Cristian and Leonardo ", True, text_color), (220, 430))

        # Texto en cajas
        screen.blit(self.font.render(self.username, True, (255,255,255)), (self.input_box_user.x+5, self.input_box_user.y+5))
        screen.blit(self.font.render("*"*len(self.password), True, (255,255,255)), (self.input_box_pass.x+5, self.input_box_pass.y+5))

        # Botones
        screen.blit(self.font.render("Login", True, (0,0,0)), (self.login_button.x+20, self.login_button.y+10))
        screen.blit(self.font.render("Register", True, (0,0,0)), (self.register_button.x+10, self.register_button.y+10))


    def login(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", 5000))

            # Payload
            request = {
                "type": "login",
                "payload": {"username": self.username, "password": self.password}
            }

            # Serializar
            message = json.dumps(request) + "\n"
            client.sendall(message.encode())

            # Recibir respuesta completa (hasta \n)
            data = b""
            while not data.endswith(b"\n"):
                chunk = client.recv(1024)
                if not chunk:
                    break
                data += chunk

            response_data = data.decode().strip()
            print("Respuesta del server (raw):", response_data)

            client.close()

            # Parsear JSON
            try:
                response_json = json.loads(response_data)
                if response_json.get("success"):
                    print(" Login exitoso:", response_json.get("message"))
                    self.game.set_screen("combat")
                else:
                    print(" Error de login:", response_json.get("message"))
            except Exception as e:
                print(" Error parseando JSON:", e)

        except Exception as e:
            print(" Error en conexión:", e)
