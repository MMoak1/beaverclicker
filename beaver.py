import pygame
import random
import json
import os
import math
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Game window dimensions
WIDTH, HEIGHT = 1024, 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beaver Empire: The Ultimate Clicker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (156, 127, 84)
BUTTON_HOVER_COLOR = (176, 147, 104)
BUTTON_TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (219, 239, 255)
WATER_COLOR = (64, 164, 223)
LAND_COLOR = (76, 153, 0)

# Fonts
title_font = pygame.font.SysFont("comicsans", 60)
font = pygame.font.SysFont("comicsans", 30)
small_font = pygame.font.SysFont("comicsans", 24)

# Game state
class GameState:
    def __init__(self):
        self.wood = 0
        self.total_wood_collected = 0
        self.beavers = 0
        self.dams = 0
        self.lodges = 0
        self.saplings = 0
        self.forests = 0
        self.clicks = 0
        self.auto_click_power = 0
        self.click_power = 1
        self.wood_per_second = 0
        
        # Prices and multipliers
        self.beaver_price = 10
        self.dam_price = 100
        self.lodge_price = 500
        self.sapling_price = 2000
        self.forest_price = 10000
        self.click_upgrade_price = 50
        
        # Production rates
        self.beaver_production = 0.1  # Wood per second per beaver
        self.dam_production = 1      # Wood per second per dam
        self.lodge_production = 5     # Wood per second per lodge
        self.sapling_production = 20  # Wood per second per sapling
        self.forest_production = 100  # Wood per second per forest
        
        # Achievements
        self.achievements = {
            "first_beaver": False,
            "first_dam": False,
            "first_lodge": False,
            "first_sapling": False,
            "first_forest": False,
            "wood_100": False,
            "wood_1000": False,
            "wood_10000": False,
            "wood_100000": False,
            "wood_1000000": False,
            "clicks_100": False,
            "clicks_1000": False,
        }
        
        # Updates time tracking
        self.last_time = pygame.time.get_ticks()
        self.last_save_time = pygame.time.get_ticks()
        
        # Notifications
        self.notifications = []
        self.animation_items = []

    def calculate_wood_per_second(self):
        self.wood_per_second = (
            self.beavers * self.beaver_production +
            self.dams * self.dam_production +
            self.lodges * self.lodge_production +
            self.saplings * self.sapling_production +
            self.forests * self.forest_production
        )
        return self.wood_per_second
    
    def add_notification(self, text, color=(255, 255, 0)):
        self.notifications.append({"text": text, "time": pygame.time.get_ticks(), "color": color})
    
    def add_animation(self, text, x, y, color=(255, 255, 0)):
        self.animation_items.append({
            "text": text, 
            "x": x, 
            "y": y, 
            "time": pygame.time.get_ticks(), 
            "color": color,
            "velocity": random.uniform(-1, 1)
        })
    
    def check_achievements(self):
        # Check beaver-related achievements
        if not self.achievements["first_beaver"] and self.beavers >= 1:
            self.achievements["first_beaver"] = True
            self.add_notification("Achievement: First Beaver!")
            
        if not self.achievements["first_dam"] and self.dams >= 1:
            self.achievements["first_dam"] = True
            self.add_notification("Achievement: First Dam!")
            
        if not self.achievements["first_lodge"] and self.lodges >= 1:
            self.achievements["first_lodge"] = True
            self.add_notification("Achievement: First Lodge!")
            
        if not self.achievements["first_sapling"] and self.saplings >= 1:
            self.achievements["first_sapling"] = True
            self.add_notification("Achievement: First Sapling!")
            
        if not self.achievements["first_forest"] and self.forests >= 1:
            self.achievements["first_forest"] = True
            self.add_notification("Achievement: First Forest!")
        
        # Check wood-related achievements
        if not self.achievements["wood_100"] and self.total_wood_collected >= 100:
            self.achievements["wood_100"] = True
            self.add_notification("Achievement: 100 Wood Collected!")
            
        if not self.achievements["wood_1000"] and self.total_wood_collected >= 1000:
            self.achievements["wood_1000"] = True
            self.add_notification("Achievement: 1,000 Wood Collected!")
            
        if not self.achievements["wood_10000"] and self.total_wood_collected >= 10000:
            self.achievements["wood_10000"] = True
            self.add_notification("Achievement: 10,000 Wood Collected!")
            
        if not self.achievements["wood_100000"] and self.total_wood_collected >= 100000:
            self.achievements["wood_100000"] = True
            self.add_notification("Achievement: 100,000 Wood Collected!")
            
        if not self.achievements["wood_1000000"] and self.total_wood_collected >= 1000000:
            self.achievements["wood_1000000"] = True
            self.add_notification("Achievement: 1,000,000 Wood Collected!")
            
        # Check click-related achievements
        if not self.achievements["clicks_100"] and self.clicks >= 100:
            self.achievements["clicks_100"] = True
            self.add_notification("Achievement: 100 Clicks!")
            
        if not self.achievements["clicks_1000"] and self.clicks >= 1000:
            self.achievements["clicks_1000"] = True
            self.add_notification("Achievement: 1,000 Clicks!")
    
    def save_game(self):
        save_data = {
            "wood": self.wood,
            "total_wood_collected": self.total_wood_collected,
            "beavers": self.beavers,
            "dams": self.dams,
            "lodges": self.lodges,
            "saplings": self.saplings,
            "forests": self.forests,
            "clicks": self.clicks,
            "click_power": self.click_power,
            "beaver_price": self.beaver_price,
            "dam_price": self.dam_price,
            "lodge_price": self.lodge_price,
            "sapling_price": self.sapling_price,
            "forest_price": self.forest_price,
            "click_upgrade_price": self.click_upgrade_price,
            "achievements": self.achievements
        }
        
        with open("beaver_save.json", "w") as f:
            json.dump(save_data, f)
        
        self.add_notification("Game Saved!", (0, 255, 0))
    
    def load_game(self):
        if os.path.exists("beaver_save.json"):
            try:
                with open("beaver_save.json", "r") as f:
                    save_data = json.load(f)
                
                self.wood = save_data.get("wood", 0)
                self.total_wood_collected = save_data.get("total_wood_collected", 0)
                self.beavers = save_data.get("beavers", 0)
                self.dams = save_data.get("dams", 0)
                self.lodges = save_data.get("lodges", 0)
                self.saplings = save_data.get("saplings", 0)
                self.forests = save_data.get("forests", 0)
                self.clicks = save_data.get("clicks", 0)
                self.click_power = save_data.get("click_power", 1)
                self.beaver_price = save_data.get("beaver_price", 10)
                self.dam_price = save_data.get("dam_price", 100)
                self.lodge_price = save_data.get("lodge_price", 500)
                self.sapling_price = save_data.get("sapling_price", 2000)
                self.forest_price = save_data.get("forest_price", 10000)
                self.click_upgrade_price = save_data.get("click_upgrade_price", 50)
                self.achievements = save_data.get("achievements", self.achievements)
                
                self.add_notification("Game Loaded!", (0, 255, 0))
                return True
            except Exception as e:
                print(f"Error loading save: {e}")
                return False
        return False

# Initialize game state
game_state = GameState()

# Try to load saved game
game_state.load_game()

# Load images
try:
    beaver_image = pygame.image.load("beaver_guy.png")
    beaver_image = pygame.transform.scale(beaver_image, (200, 200))
except:
    # Create a placeholder beaver if image isn't found
    beaver_image = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.ellipse(beaver_image, (139, 69, 19), (50, 50, 100, 150))
    pygame.draw.ellipse(beaver_image, (165, 113, 78), (60, 60, 80, 130))
    pygame.draw.ellipse(beaver_image, (139, 69, 19), (70, 30, 60, 40))
    pygame.draw.ellipse(beaver_image, (0, 0, 0), (80, 40, 10, 10))
    pygame.draw.ellipse(beaver_image, (0, 0, 0), (110, 40, 10, 10))

try:
    dam_image = pygame.image.load("dam.png")
    dam_image = pygame.transform.scale(dam_image, (100, 100))
except:
    # Create a placeholder dam if image isn't found
    dam_image = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(dam_image, (139, 69, 19), (10, 30, 80, 60))
    for i in range(4):
        pygame.draw.rect(dam_image, (101, 67, 33), (15 + i*20, 35, 15, 50))

try:
    lodge_image = pygame.image.load("lodge.png")
    lodge_image = pygame.transform.scale(lodge_image, (120, 120))
except:
    # Create a placeholder lodge if image isn't found
    lodge_image = pygame.Surface((120, 120), pygame.SRCALPHA)
    pygame.draw.ellipse(lodge_image, (139, 69, 19), (20, 40, 80, 60))
    pygame.draw.rect(lodge_image, (101, 67, 33), (50, 20, 20, 20))

try:
    sapling_image = pygame.image.load("sapling.png")
    sapling_image = pygame.transform.scale(sapling_image, (80, 120))
except:
    # Create a placeholder sapling if image isn't found
    sapling_image = pygame.Surface((80, 120), pygame.SRCALPHA)
    pygame.draw.rect(sapling_image, (101, 67, 33), (35, 40, 10, 70))
    pygame.draw.ellipse(sapling_image, (34, 139, 34), (10, 10, 60, 50))

try:
    forest_image = pygame.image.load("forest.png")
    forest_image = pygame.transform.scale(forest_image, (150, 150))
except:
    # Create a placeholder forest if image isn't found
    forest_image = pygame.Surface((150, 150), pygame.SRCALPHA)
    for i in range(3):
        for j in range(2):
            x, y = 20 + i*40, 20 + j*60
            pygame.draw.rect(forest_image, (101, 67, 33), (x+15, y+20, 10, 40))
            pygame.draw.ellipse(forest_image, (34, 139, 34), (x, y, 40, 30))

# Try to load sounds
try:
    click_sound = mixer.Sound("click.wav")
    buy_sound = mixer.Sound("buy.wav")
    achievement_sound = mixer.Sound("achievement.wav")
except:
    # Create placeholder sounds if not found
    click_sound = None
    buy_sound = None
    achievement_sound = None

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action, hover_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover_text = hover_text
        self.is_hovered = False
    
    def draw(self, enabled=True):
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

# Define button actions
def get_wood_action():
    amount = game_state.click_power
    game_state.wood += amount
    game_state.total_wood_collected += amount
    game_state.clicks += 1
    game_state.add_animation(f"+{amount}", 200, 200)
    game_state.check_achievements()
    if click_sound:
        click_sound.play()
    return True

def buy_beaver_action():
    if game_state.wood >= game_state.beaver_price:
        game_state.wood -= game_state.beaver_price
        game_state.beavers += 1
        old_price = game_state.beaver_price
        game_state.beaver_price = int(game_state.beaver_price * 1.1)
        game_state.calculate_wood_per_second()
        game_state.check_achievements()
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Bought 1 beaver for {old_price} wood!")
        return True
    return False

def buy_dam_action():
    if game_state.wood >= game_state.dam_price:
        game_state.wood -= game_state.dam_price
        game_state.dams += 1
        old_price = game_state.dam_price
        game_state.dam_price = int(game_state.dam_price * 1.15)
        game_state.calculate_wood_per_second()
        game_state.check_achievements()
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Bought 1 dam for {old_price} wood!")
        return True
    return False

def buy_lodge_action():
    if game_state.wood >= game_state.lodge_price:
        game_state.wood -= game_state.lodge_price
        game_state.lodges += 1
        old_price = game_state.lodge_price
        game_state.lodge_price = int(game_state.lodge_price * 1.2)
        game_state.calculate_wood_per_second()
        game_state.check_achievements()
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Bought 1 lodge for {old_price} wood!")
        return True
    return False

def buy_sapling_action():
    if game_state.wood >= game_state.sapling_price:
        game_state.wood -= game_state.sapling_price
        game_state.saplings += 1
        old_price = game_state.sapling_price
        game_state.sapling_price = int(game_state.sapling_price * 1.25)
        game_state.calculate_wood_per_second()
        game_state.check_achievements()
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Bought 1 sapling for {old_price} wood!")
        return True
    return False

def buy_forest_action():
    if game_state.wood >= game_state.forest_price:
        game_state.wood -= game_state.forest_price
        game_state.forests += 1
        old_price = game_state.forest_price
        game_state.forest_price = int(game_state.forest_price * 1.3)
        game_state.calculate_wood_per_second()
        game_state.check_achievements()
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Bought 1 forest for {old_price} wood!")
        return True
    return False

def upgrade_click_action():
    if game_state.wood >= game_state.click_upgrade_price:
        game_state.wood -= game_state.click_upgrade_price
        old_power = game_state.click_power
        game_state.click_power += 1
        old_price = game_state.click_upgrade_price
        game_state.click_upgrade_price = int(game_state.click_upgrade_price * 1.5)
        if buy_sound:
            buy_sound.play()
        game_state.add_notification(f"Upgraded click power from {old_power} to {game_state.click_power} for {old_price} wood!")
        return True
    return False

def save_game_action():
    game_state.save_game()
    return True

# Create buttons
button_width, button_height = 200, 50
padding = 20

# Main action button
get_wood_button = Button(
    WIDTH // 2 - button_width // 2,
    150,
    button_width,
    button_height,
    "Get Wood",
    get_wood_action,
    "Click to gather wood"
)

# Building buttons (right side)
building_x = WIDTH - button_width - padding
buildings_start_y = 250

upgrade_click_button = Button(
    building_x,
    buildings_start_y,
    button_width,
    button_height,
    "Upgrade Click",
    upgrade_click_action,
    "Increases wood per click"
)

buy_beaver_button = Button(
    building_x,
    buildings_start_y + button_height + padding,
    button_width,
    button_height,
    "Buy Beaver",
    buy_beaver_action,
    "Produces 0.1 wood per second"
)

buy_dam_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 2,
    button_width,
    button_height,
    "Buy Dam",
    buy_dam_action,
    "Produces 1 wood per second"
)

buy_lodge_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 3,
    button_width,
    button_height,
    "Buy Lodge",
    buy_lodge_action,
    "Produces 5 wood per second"
)

buy_sapling_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 4,
    button_width,
    button_height,
    "Buy Sapling",
    buy_sapling_action,
    "Produces 20 wood per second"
)

buy_forest_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 5,
    button_width,
    button_height,
    "Buy Forest",
    buy_forest_action,
    "Produces 100 wood per second"
)

save_button = Button(
    WIDTH - button_width - padding,
    HEIGHT - button_height - padding,
    button_width,
    button_height,
    "Save Game",
    save_game_action,
    "Save your progress"
)

# Group all buttons
all_buttons = [get_wood_button, upgrade_click_button, buy_beaver_button, buy_dam_button, 
              buy_lodge_button, buy_sapling_button, buy_forest_button, save_button]

# Game loop
def main_game_loop():
    running = True
    clock = pygame.time.Clock()
    current_time = pygame.time.get_ticks()
    
    # Animation for beavers
    beaver_offset = 0
    beaver_direction = 1
    
    # Water animation
    water_offset = 0
    
    # Tooltip text
    tooltip_text = ""
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save game before quitting
                game_state.save_game()
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for button in all_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.click()
                            
                    # Clicking beaver image also gives wood
                    beaver_rect = pygame.Rect(50, 250, 200, 200)
                    if beaver_rect.collidepoint(event.pos):
                        get_wood_action()
        
        # Auto production from buildings
        time_delta = current_time - game_state.last_time
        if time_delta >= 1000:  # Every second
            wood_to_add = game_state.calculate_wood_per_second() * (time_delta / 1000)
            game_state.wood += wood_to_add
            game_state.total_wood_collected += wood_to_add
            game_state.last_time = current_time
        
        # Auto-save every 2 minutes
        if current_time - game_state.last_save_time >= 120000:
            game_state.save_game()
            game_state.last_save_time = current_time
        
        # Update tooltip
        tooltip_text = ""
        for button in all_buttons:
            if button.check_hover(mouse_pos) and button.hover_text:
                tooltip_text = button.hover_text
        
        # Update animation values
        beaver_offset += 0.2 * beaver_direction
        if beaver_offset > 5 or beaver_offset < -5:
            beaver_direction *= -1
            
        water_offset = (water_offset + 0.5) % 40
        
        # Draw the screen
        draw_game_screen(beaver_offset, water_offset, tooltip_text)
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()

def draw_game_screen(beaver_offset, water_offset, tooltip_text):
    # Draw background scene
    window.fill(BACKGROUND_COLOR)
    
    # Draw water with animation
    for x in range(-40, WIDTH + 40, 40):
        pygame.draw.rect(window, WATER_COLOR, (x + water_offset - 40, HEIGHT - 200, 40, 200))
    
    # Draw land
    pygame.draw.rect(window, LAND_COLOR, (0, HEIGHT - 220, WIDTH, 20))
    
    # Draw title
    title_text = title_font.render("Beaver Empire", True, BLACK)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    # Draw stats
    stats_y = 80
    wood_text = font.render(f"Wood: {int(game_state.wood):,}", True, BLACK)
    window.blit(wood_text, (padding, stats_y))
    
    wps_text = font.render(f"Wood per Second: {game_state.calculate_wood_per_second():.1f}", True, BLACK)
    window.blit(wps_text, (padding, stats_y + 30))
    
    wpc_text = font.render(f"Wood per Click: {game_state.click_power}", True, BLACK)
    window.blit(wpc_text, (padding, stats_y + 60))
    
    # Draw beaver with animation
    window.blit(beaver_image, (50, 250 + beaver_offset))
    
    # Draw owned buildings with icons
    building_stats_x = 50
    building_stats_y = 480
    
    stats_font = small_font
    
    # Beaver stats
    if game_state.beavers > 0:
        beaver_stats = stats_font.render(f"Beavers: {game_state.beavers} ({game_state.beavers * game_state.beaver_production:.1f}/s)", True, BLACK)
        window.blit(beaver_stats, (building_stats_x, building_stats_y))
        window.blit(pygame.transform.scale(beaver_image, (30, 30)), (building_stats_x - 40, building_stats_y))
    
    # Dam stats
    if game_state.dams > 0:
        dam_stats = stats_font.render(f"Dams: {game_state.dams} ({game_state.dams * game_state.dam_production:.1f}/s)", True, BLACK)
        window.blit(dam_stats, (building_stats_x, building_stats_y + 30))
        window.blit(pygame.transform.scale(dam_image, (30, 30)), (building_stats_x - 40, building_stats_y + 30))
    
    # Lodge stats
    if game_state.lodges > 0:
        lodge_stats = stats_font.render(f"Lodges: {game_state.lodges} ({game_state.lodges * game_state.lodge_production:.1f}/s)", True, BLACK)
        window.blit(lodge_stats, (building_stats_x, building_stats_y + 60))
        window.blit(pygame.transform.scale(lodge_image, (30, 30)), (building_stats_x - 40, building_stats_y + 60))
    
    # Sapling stats
    if game_state.saplings > 0:
        sapling_stats = stats_font.render(f"Saplings: {game_state.saplings} ({game_state.saplings * game_state.sapling_production:.1f}/s)", True, BLACK)
        window.blit(sapling_stats, (building_stats_x, building_stats_y + 90))
        window.blit(pygame.transform.scale(sapling_image, (30, 30)), (building_stats_x - 40, building_stats_y + 90))
    
    # Forest stats
    if game_state.forests > 0:
        forest_stats = stats_font.render(f"Forests: {game_state.forests} ({game_state.forests * game_state.forest_production:.1f}/s)", True, BLACK)
        window.blit(forest_stats, (building_stats_x, building_stats_y + 120))
        window.blit(pygame.transform.scale(forest_image, (30, 30)), (building_stats_x - 40, building_stats_y + 120))
    
    # Draw buttons
    get_wood_button.draw()
    
    # Draw building buttons with prices
    upgrade_click_button.draw(game_state.wood >= game_state.click_upgrade_price)
    price_text = small_font.render(f"Price: {game_state.click_upgrade_price:,} wood", True, BLACK)
    window.blit(price_text, (upgrade_click_button.rect.x, upgrade_click_button.rect.y - 25))
    
    buy_beaver_button.draw(game_state.wood >= game_state.beaver_price)
    price_text = small_font.render(f"Price: {game_state.beaver_price:,} wood", True, BLACK)
    window.blit(price_text, (buy_beaver_button.rect.x, buy_beaver_button.rect.y - 25))
    
    buy_dam_button.draw(game_state.wood >= game_state.dam_price)
    price_text = small_font.render(f"Price: {game_state.dam_price:,} wood", True, BLACK)
    window.blit(price_text, (buy_dam_button.rect.x, buy_dam_button.rect.y - 25))
    
    buy_lodge_button.draw(game_state.wood >= game_state.lodge_price)
    price_text = small_font.render(f"Price: {game_state.lodge_price:,} wood", True, BLACK)
    window.blit(price_text, (buy_lodge_button.rect.x, buy_lodge_button.rect.y - 25))
    
    buy_sapling_button.draw(game_state.wood >= game_state.sapling_price)
    price_text = small_font.render(f"Price: {game_state.sapling_price:,} wood", True, BLACK)
    window.blit(price_text, (buy_sapling_button.rect.x, buy_sapling_button.rect.y - 25))
    
    buy_forest_button.draw(game_state.wood >= game_state.forest_price)
    price_text = small_font.render(f"Price: {game_state.forest_price:,} wood", True, BLACK)
    window.blit(price_text, (buy_forest_button.rect.x, buy_forest_button.rect.y - 25))
    
    save_button.draw()
    
    # Draw building images on the left side
    building_display_x = 250
    building_display_y = 480
    
    if game_state.dams > 0:
        window.blit(dam_image, (building_display_x, building_display_y))
    
    if game_state.lodges > 0:
        window.blit(lodge_image, (building_display_x + 120, building_display_y))
    
    if game_state.saplings > 0:
        window.blit(sapling_image, (building_display_x + 250, building_display_y))
    
    if game_state.forests > 0:
        window.blit(forest_image, (building_display_x + 350, building_display_y))
    
    # Draw tooltip
    if tooltip_text:
        tooltip_surface = small_font.render(tooltip_text, True, BLACK, WHITE)
        tooltip_rect = tooltip_surface.get_rect()
        tooltip_rect.topleft = (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10)
        
        # Make sure tooltip stays on screen
        if tooltip_rect.right > WIDTH:
            tooltip_rect.right = WIDTH
        if tooltip_rect.bottom > HEIGHT:
            tooltip_rect.bottom = HEIGHT
            
        pygame.draw.rect(window, WHITE, tooltip_rect)
        pygame.draw.rect(window, BLACK, tooltip_rect, 1)
        window.blit(tooltip_surface, tooltip_rect)
    
    # Process and draw notifications
    current_time = pygame.time.get_ticks()
    notification_y = 150
    
    # Remove old notifications
    game_state.notifications = [n for n in game_state.notifications if current_time - n["time"] < 3000]
    
    # Draw active notifications
    for notification in game_state.notifications:
        alpha = min(255, max(0, 255 - (current_time - notification["time"]) / 3000 * 255))
        notification_surface = small_font.render(notification["text"], True, notification["color"])
        notification_surface.set_alpha(alpha)
        window.blit(notification_surface, (WIDTH // 2 - notification_surface.get_width() // 2, notification_y))
        notification_y += 30
    
    # Process and draw animations
    game_state.animation_items = [a for a in game_state.animation_items if current_time - a["time"] < 2000]
    
    for anim in game_state.animation_items:
        age = (current_time - anim["time"]) / 1000.0
        alpha = min(255, max(0, 255 - age * 255))
        y_offset = -30 * age  # Move upward
        
        anim_surface = small_font.render(anim["text"], True, anim["color"])
        anim_surface.set_alpha(alpha)
        x_pos = anim["x"] + anim["velocity"] * age * 50
        y_pos = anim["y"] + y_offset
        window.blit(anim_surface, (x_pos, y_pos))
    
    # Show some achievement stats
    achieved_count = sum(1 for achieved in game_state.achievements.values() if achieved)
    total_achievements = len(game_state.achievements)
    
    achievements_text = small_font.render(f"Achievements: {achieved_count}/{total_achievements}", True, BLACK)
    window.blit(achievements_text, (WIDTH - achievements_text.get_width() - padding, stats_y))
    
    # Show total wood collected
    total_wood_text = small_font.render(f"Total Wood Collected: {int(game_state.total_wood_collected):,}", True, BLACK)
    window.blit(total_wood_text, (WIDTH - total_wood_text.get_width() - padding, stats_y + 30))
    
    # Show total clicks
    total_clicks_text = small_font.render(f"Total Clicks: {game_state.clicks:,}", True, BLACK)
    window.blit(total_clicks_text, (WIDTH - total_clicks_text.get_width() - padding, stats_y + 60))
    
    pygame.display.update()

# Start the game
if __name__ == "__main__":
    main_game_loop()