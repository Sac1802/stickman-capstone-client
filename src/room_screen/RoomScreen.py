import pygame
import os
import math

# ============================================
# CLASE CodeScreen
# ============================================
class RoomScreen:

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.code = ""
        self.active_field = None
        self.t = 0 # contador de colores

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
            print("ESC")

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


        # Regresar a registro
        screen.blit(self.font.render("Crear Sala", True, color), (50, 120))

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


