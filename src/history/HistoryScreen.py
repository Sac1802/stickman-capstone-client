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
       # self.code_button = pygame.Rect(50, 120, 150, 40)
        #self.history_button = pygame.Rect(230, 120, 170, 40)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("wq")
         #   if self.code_button.collidepoint(event.pos):
         #       print("weqe")
         #   elif self.history_button.collidepoint(event.pos):
         #       print("wwww")
         #   else:
         #       self.active_field = None

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen("menu")

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

        screen.blit(self.font.render("History", True, color), (50, 60))

        # Boton
        # pygame.draw.rect(screen, (100,100,200), self.code_button)
        # pygame.draw.rect(screen, (100,100,200), self.history_button)

        # Botones
        #    screen.blit(self.font.render("Create Room", True, (255,255,122)), (self.code_button.x+10, self.code_button.y+10))
        #  screen.blit(self.font.render("match history", True, (255,255,122)), (self.history_button.x+10, self.history_button.y+10))
