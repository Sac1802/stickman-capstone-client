import pygame
import os
import math

class DashboardScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.username = ""
        self.email = ""
        self.password = ""
        self.active_field = None
        self.t = 0 # contador de colores

        # Titulo
        # title_path = os.path.join("static", "title.png")
        #self.title_img = pygame.image.load(title_path).convert_alpha()
        #self.title_img = pygame.transform.scale(self.title_img, (100, 80))

        # text field position
        self.input_box_user = pygame.Rect(180, 220, 200, 32)
        self.input_box_cuser = pygame.Rect(530, 220, 200, 32)
        self.input_box_pass = pygame.Rect(180, 265, 200, 32)

        # Botones
        self.register_button = pygame.Rect(350, 340, 100, 40)

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
            self.game.set_screen("login")

    def update(self):
        pass

    def draw(self, screen):
        self.t += 1;

        screen.fill((50, 50, 80))

        #Title image
        # screen.blit(self.title_img, (100, 20))

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
        screen.blit(self.font.render("Usuario :", True, (200,200,200)), (70, 220))
        screen.blit(self.font.render("Email :", True, (200,200,200)), (445, 222))
        screen.blit(self.font.render("Contraseña:", True, (200,200,200)), (42, 270))

        # Cajas
        pygame.draw.rect(screen, (200,200,200), self.input_box_user)
        pygame.draw.rect(screen, (200,200,200), self.input_box_cuser)
        pygame.draw.rect(screen, (200,200,200), self.input_box_pass)

        # Boton
        pygame.draw.rect(screen, (100,100,200), self.register_button)

        # Texto en cajas
        screen.blit(self.font.render(self.username, True, (255,255,255)), (self.input_box_user.x+5, self.input_box_user.y+5))
        screen.blit(self.font.render(self.email, True, (255,255,255)), (self.input_box_cuser.x+5, self.input_box_cuser.y+5))
        screen.blit(self.font.render("*"*len(self.password), True, (255,255,255)), (self.input_box_pass.x+5, self.input_box_pass.y+5))

        # Botones
        screen.blit(self.font.render("Register", True, (200,200,122)), (self.register_button.x+10, self.register_button.y+10))

        screen.blit(self.font.render("Pantalla de Registro (ESC para volver)", True, color), (50, 440))
