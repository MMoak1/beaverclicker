# main.py - Main entry point for the Beaver Clicker Game
import pygame
from pygame import mixer
import game_state
from ui.button import Button
from ui.renderer import GameRenderer
from actions import *

# Initialize pygame
pygame.init()
mixer.init()

# Game window dimensions
WIDTH, HEIGHT = 1024, 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beaver Empire: The Ultimate Clicker")

# Initialize game state
game = game_state.GameState()

# Try to load saved game
game.load_game()

# Create renderer
renderer = GameRenderer(window, game)

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
    lambda: get_wood_action(game),
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
    lambda: upgrade_click_action(game),
    "Increases wood per click"
)

buy_beaver_button = Button(
    building_x,
    buildings_start_y + button_height + padding,
    button_width,
    button_height,
    "Buy Beaver",
    lambda: buy_beaver_action(game),
    "Produces 0.1 wood per second"
)

buy_dam_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 2,
    button_width,
    button_height,
    "Buy Dam",
    lambda: buy_dam_action(game),
    "Produces 1 wood per second"
)

buy_lodge_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 3,
    button_width,
    button_height,
    "Buy Lodge",
    lambda: buy_lodge_action(game),
    "Produces 5 wood per second"
)

buy_sapling_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 4,
    button_width,
    button_height,
    "Buy Sapling",
    lambda: buy_sapling_action(game),
    "Produces 20 wood per second"
)

buy_forest_button = Button(
    building_x,
    buildings_start_y + (button_height + padding) * 5,
    button_width,
    button_height,
    "Buy Forest",
    lambda: buy_forest_action(game),
    "Produces 100 wood per second"
)

save_button = Button(
    WIDTH - button_width - padding,
    HEIGHT - button_height - padding,
    button_width,
    button_height,
    "Save Game",
    lambda: save_game_action(game),
    "Save your progress"
)

# Group all buttons
all_buttons = [get_wood_button, upgrade_click_button, buy_beaver_button, buy_dam_button, 
              buy_lodge_button, buy_sapling_button, buy_forest_button, save_button]

def main_game_loop():
    running = True
    clock = pygame.time.Clock()
    current_time = pygame.time.get_ticks()
    
    # Animation values
    beaver_offset = 0
    beaver_direction = 1
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
                game.save_game()
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for button in all_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.click()
                            
                    # Clicking beaver image also gives wood
                    beaver_rect = pygame.Rect(50, 250, 200, 200)
                    if beaver_rect.collidepoint(event.pos):
                        get_wood_action(game)
        
        # Auto production from buildings
        time_delta = current_time - game.last_time
        if time_delta >= 1000:  # Every second
            wood_to_add = game.calculate_wood_per_second() * (time_delta / 1000)
            game.wood += wood_to_add
            game.total_wood_collected += wood_to_add
            game.last_time = current_time
        
        # Auto-save every 2 minutes
        if current_time - game.last_save_time >= 120000:
            game.save_game()
            game.last_save_time = current_time
        
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
        renderer.draw_game_screen(
            all_buttons, 
            beaver_offset, 
            water_offset, 
            tooltip_text,
            padding,
            button_width
        )
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()

# Start the game
if __name__ == "__main__":
    main_game_loop()