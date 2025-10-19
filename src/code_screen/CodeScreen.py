import pygame
import os
import math

class CodeScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.username = ""
        self.active_field = None
        self.t = 0 # contador de colores

        # Titulo
        title_path = os.path.join("static", "title.png")
        self.title_img = pygame.image.load(title_path).convert_alpha()
        self.title_img = pygame.transform.scale(self.title_img, (200, 150))

        # text field position
        self.input_box_user = pygame.Rect(260, 250, 300, 32)

        # Botones
        self.register_button = pygame.Rect(340, 340, 130, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box_user.collidepoint(event.pos):
                self.active_field = "user"
            elif self.input_box_pass.collidepoint(event.pos):
                self.active_field = "pass"
            elif self.input_box_cuser.collidepoint(event.pos):
                self.active_field = "email"
            elif self.register_button.collidepoint(event.pos):
                self.game.set_screen("code")
            else:
                self.active_field = None

        elif event.type == pygame.KEYDOWN:
            if self.active_field == "user":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_field == "email":
                if event.key == pygame.K_BACKSPACE:
                      self.email = self.email[:-1]
                else:
                      self.email += event.unicode
            elif self.active_field == "pass":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

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
        pygame.draw.rect(screen, (200,200,200), self.input_box_user)

        # Boton
        pygame.draw.rect(screen, (100,100,200), self.register_button)

        # Texto en cajas
        screen.blit(self.font.render(self.username, True, (255,255,255)), (self.input_box_user.x+5, self.input_box_user.y+5))

        # Botones
        screen.blit(self.font.render("send code", True, (255,255,122)), (self.register_button.x+10, self.register_button.y+10))

        # Regresar a registro
        screen.blit(self.font.render("Pantalla de validacion de codigo (ESC para volver)", True, color), (50, 440))
