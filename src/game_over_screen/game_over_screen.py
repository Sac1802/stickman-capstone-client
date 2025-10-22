import pygame

class Game_over_screen:
    def __init__(self, game, winner):
        self.game = game
        self.winner = winner
        self.font = pygame.font.Font(None, 32)
        self.refresh_button = pygame.Rect(200, 350, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.refresh_button.collidepoint(event.pos):
                self.game.set_screen("menu")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((50, 50, 80))
        pygame.draw.rect(screen, (100, 100, 200), self.refresh_button)
        refresh_text = self.font.render("Return Dashboard", True, (255, 255, 255))
        text_rect = refresh_text.get_rect(center=self.refresh_button.center)
        screen.blit(refresh_text, text_rect)

        winner_text = self.font.render(f"{self.winner}", True, (255, 0, 0))
        winner_rect = winner_text.get_rect(center=(screen.get_width()//2, 200))
        screen.blit(winner_text, winner_rect)
