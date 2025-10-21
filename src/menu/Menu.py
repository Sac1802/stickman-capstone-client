import pygame
import os
import math

class Menu:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.code = ""
        self.active_field = None
        self.t = 0 # contador de colores

        # Botones
        self.code_button = pygame.Rect(340, 340, 130, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.code_button.collidepoint(event.pos):
                self.game.set_screen("dashboard")
            else:
                self.active_field = None

        elif event.type == pygame.KEYDOWN:
            if self.active_field == "code":
                if event.key == pygame.K_BACKSPACE:
                    self.code = self.code[:-1]
                else:
                    self.code += event.unicode

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen("login")

    def update(self):
        pass

    def draw(self, screen):
        self.t += 1;
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

        screen.blit(self.font.render("MENU", True, color), (50, 60))

        # Boton
        pygame.draw.rect(screen, (100,100,200), self.code_button)

        # Botones
        screen.blit(self.font.render("send code", True, (255,255,122)), (self.code_button.x+10, self.code_button.y+10))
