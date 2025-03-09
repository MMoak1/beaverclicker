# utils/assets.py - Manages game assets
import pygame
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.load_images()
        
    def load_images(self):
        # Beaver image
        try:
            self.images['beaver'] = pygame.image.load("assets/images/beaver_guy.png")
            self.images['beaver'] = pygame.transform.scale(self.images['beaver'], (200, 200))
        except:
            # Create a placeholder beaver if image isn't found
            self.images['beaver'] = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.ellipse(self.images['beaver'], (139, 69, 19), (50, 50, 100, 150))
            pygame.draw.ellipse(self.images['beaver'], (165, 113, 78), (60, 60, 80, 130))
            pygame.draw.ellipse(self.images['beaver'], (139, 69, 19), (70, 30, 60, 40))
            pygame.draw.ellipse(self.images['beaver'], (0, 0, 0), (80, 40, 10, 10))
            pygame.draw.ellipse(self.images['beaver'], (0, 0, 0), (110, 40, 10, 10))

        # Dam image
        try:
            self.images['dam'] = pygame.image.load("assets/images/dam.png")
            self.images['dam'] = pygame.transform.scale(self.images['dam'], (100, 100))
        except:
            # Create a placeholder dam if image isn't found
            self.images['dam'] = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.rect(self.images['dam'], (139, 69, 19), (10, 30, 80, 60))
            for i in range(4):
                pygame.draw.rect(self.images['dam'], (101, 67, 33), (15 + i*20, 35, 15, 50))

        # Lodge image
        try:
            self.images['lodge'] = pygame.image.load("assets/images/lodge.png")
            self.images['lodge'] = pygame.transform.scale(self.images['lodge'], (120, 120))
        except:
            # Create a placeholder lodge if image isn't found
            self.images['lodge'] = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.ellipse(self.images['lodge'], (139, 69, 19), (20, 40, 80, 60))
            pygame.draw.rect(self.images['lodge'], (101, 67, 33), (50, 20, 20, 20))

        # Sapling image
        try:
            self.images['sapling'] = pygame.image.load("assets/images/sapling.png")
            self.images['sapling'] = pygame.transform.scale(self.images['sapling'], (80, 120))
        except:
            # Create a placeholder sapling if image isn't found
            self.images['sapling'] = pygame.Surface((80, 120), pygame.SRCALPHA)
            pygame.draw.rect(self.images['sapling'], (101, 67, 33), (35, 40, 10, 70))
            pygame.draw.ellipse(self.images['sapling'], (34, 139, 34), (10, 10, 60, 50))

        # Forest image
        try:
            self.images['forest'] = pygame.image.load("assets/images/forest.png")
            self.images['forest'] = pygame.transform.scale(self.images['forest'], (150, 150))
        except:
            # Create a placeholder forest if image isn't found
            self.images['forest'] = pygame.Surface((150, 150), pygame.SRCALPHA)
            for i in range(3):
                for j in range(2):
                    x, y = 20 + i*40, 20 + j*60
                    pygame.draw.rect(self.images['forest'], (101, 67, 33), (x+15, y+20, 10, 40))
                    pygame.draw.ellipse(self.images['forest'], (34, 139, 34), (x, y, 40, 30))
    
    def get_image(self, name):
        return self.images.get(name)

# Create a global instance for import
assets = AssetManager()