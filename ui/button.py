# ui/button.py - Button class for the UI
import pygame

# Colors
BUTTON_COLOR = (156, 127, 84)
BUTTON_HOVER_COLOR = (176, 147, 104)
BUTTON_TEXT_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text, action, hover_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover_text = hover_text
        self.is_hovered = False
    
    def draw(self, window, font, enabled=True):
        color = BUTTON_COLOR
        if not enabled:
            color = (100, 100, 100)  # Disabled button color
        elif self.is_hovered:
            color = BUTTON_HOVER_COLOR
            
        pygame.draw.rect(window, color, self.rect, border_radius=10)
        pygame.draw.rect(window, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def click(self):
        return self.action()
    
