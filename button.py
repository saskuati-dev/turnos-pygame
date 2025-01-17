import pygame

class Button:
    def __init__(self, x, y, width, height, color, text, text_color, mana_cost):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.mana_cost = mana_cost
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        mana_font = pygame.font.Font(None, 20)
        mana_surface = mana_font.render(f"Cost: {self.mana_cost}", True, self.text_color)
        mana_rect = mana_surface.get_rect(midtop=(text_rect.centerx, text_rect.bottom + 5))

        
        surface.blit(text_surface, text_rect)
        surface.blit(mana_surface, mana_rect)
        

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return self.text
            