# ui/renderer.py - Handles game rendering
import pygame
from util.assets import assets  # Note the extra 's' import assets

# Colors
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (219, 239, 255)
WATER_COLOR = (64, 164, 223)
LAND_COLOR = (76, 153, 0)

class GameRenderer:
    def __init__(self, window, game_state):
        self.window = window
        self.game = game_state
        self.width, self.height = window.get_size()
        
        # Fonts
        self.title_font = pygame.font.SysFont("comicsans", 60)
        self.font = pygame.font.SysFont("comicsans", 30)
        self.small_font = pygame.font.SysFont("comicsans", 24)

    def draw_game_screen(self, buttons, beaver_offset, water_offset, tooltip_text, padding, button_width):
        # Draw background scene
        self.window.fill(BACKGROUND_COLOR)
        
        # Draw water with animation
        for x in range(-40, self.width + 40, 40):
            pygame.draw.rect(self.window, WATER_COLOR, (x + water_offset - 40, self.height - 200, 40, 200))
        
        # Draw land
        pygame.draw.rect(self.window, LAND_COLOR, (0, self.height - 220, self.width, 20))
        
        # Draw title
        title_text = self.title_font.render("Beaver Empire", True, BLACK)
        self.window.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 20))
        
        # Draw stats
        stats_y = 80
        wood_text = self.font.render(f"Wood: {int(self.game.wood):,}", True, BLACK)
        self.window.blit(wood_text, (padding, stats_y))
        
        wps_text = self.font.render(f"Wood per Second: {self.game.calculate_wood_per_second():.1f}", True, BLACK)
        self.window.blit(wps_text, (padding, stats_y + 30))
        
        wpc_text = self.font.render(f"Wood per Click: {self.game.click_power}", True, BLACK)
        self.window.blit(wpc_text, (padding, stats_y + 60))
        
        # Draw beaver with animation
        self.window.blit(assets.get_image('beaver'), (50, 250 + beaver_offset))
        
        # Draw owned buildings with icons
        building_stats_x = 50
        building_stats_y = 480
        
        # Beaver stats
        if self.game.beavers > 0:
            beaver_stats = self.small_font.render(f"Beavers: {self.game.beavers} ({self.game.beavers * self.game.beaver_production:.1f}/s)", True, BLACK)
            self.window.blit(beaver_stats, (building_stats_x, building_stats_y))
            self.window.blit(pygame.transform.scale(assets.get_image('beaver'), (30, 30)), (building_stats_x - 40, building_stats_y))
        
        # Dam stats
        if self.game.dams > 0:
            dam_stats = self.small_font.render(f"Dams: {self.game.dams} ({self.game.dams * self.game.dam_production:.1f}/s)", True, BLACK)
            self.window.blit(dam_stats, (building_stats_x, building_stats_y + 30))
            self.window.blit(pygame.transform.scale(assets.get_image('dam'), (30, 30)), (building_stats_x - 40, building_stats_y + 30))
        
        # Lodge stats
        if self.game.lodges > 0:
            lodge_stats = self.small_font.render(f"Lodges: {self.game.lodges} ({self.game.lodges * self.game.lodge_production:.1f}/s)", True, BLACK)
            self.window.blit(lodge_stats, (building_stats_x, building_stats_y + 60))
            self.window.blit(pygame.transform.scale(assets.get_image('lodge'), (30, 30)), (building_stats_x - 40, building_stats_y + 60))
        
        # Sapling stats
        if self.game.saplings > 0:
            sapling_stats = self.small_font.render(f"Saplings: {self.game.saplings} ({self.game.saplings * self.game.sapling_production:.1f}/s)", True, BLACK)
            self.window.blit(sapling_stats, (building_stats_x, building_stats_y + 90))
            self.window.blit(pygame.transform.scale(assets.get_image('sapling'), (30, 30)), (building_stats_x - 40, building_stats_y + 90))
        
        # Forest stats
        if self.game.forests > 0:
            forest_stats = self.small_font.render(f"Forests: {self.game.forests} ({self.game.forests * self.game.forest_production:.1f}/s)", True, BLACK)
            self.window.blit(forest_stats, (building_stats_x, building_stats_y + 120))
            self.window.blit(pygame.transform.scale(assets.get_image('forest'), (30, 30)), (building_stats_x - 40, building_stats_y + 120))
        
        # Draw buttons
        for button in buttons:
            if button == buttons[0]:  # get_wood_button
                button.draw(self.window, self.font)
            elif button == buttons[1]:  # upgrade_click_button
                button.draw(self.window, self.font, self.game.wood >= self.game.click_upgrade_price)
                price_text =self.small_font.render(f"Price: {self.game.click_upgrade_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            elif button == buttons[2]:  # buy_beaver_button
                button.draw(self.window, self.font, self.game.wood >= self.game.beaver_price)
                price_text = self.small_font.render(f"Price: {self.game.beaver_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            elif button == buttons[3]:  # buy_dam_button
                button.draw(self.window, self.font, self.game.wood >= self.game.dam_price)
                price_text = self.small_font.render(f"Price: {self.game.dam_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            elif button == buttons[4]:  # buy_lodge_button
                button.draw(self.window, self.font, self.game.wood >= self.game.lodge_price)
                price_text = self.small_font.render(f"Price: {self.game.lodge_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            elif button == buttons[5]:  # buy_sapling_button
                button.draw(self.window, self.font, self.game.wood >= self.game.sapling_price)
                price_text = self.small_font.render(f"Price: {self.game.sapling_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            elif button == buttons[6]:  # buy_forest_button
                button.draw(self.window, self.font, self.game.wood >= self.game.forest_price)
                price_text = self.small_font.render(f"Price: {self.game.forest_price}", True, BLACK)
                self.window.blit(price_text, (button.rect.x, button.rect.y + button.rect.height + 5))
            else:  # save_button
                button.draw(self.window, self.font)
        
        current_time = pygame.time.get_ticks()
        notification_y = self.height - 150
        for notification in self.game.notifications[:]:
            if current_time - notification["time"] < 3000:  # Show notifications for 3 seconds
                text = self.small_font.render(notification["text"], True, notification["color"])
                self.window.blit(text, (self.width // 2 - text.get_width() // 2, notification_y))
                notification_y -= 30
            else:
                self.game.notifications.remove(notification)

        # Draw animations
        for anim in self.game.animation_items[:]:
            if current_time - anim["time"] < 2000:  # Show animations for 2 seconds
                text = self.small_font.render(anim["text"], True, anim["color"])
                # Move animation upward and fade it
                elapsed = (current_time - anim["time"]) / 1000.0  # seconds
                y_offset = int(elapsed * -50)  # Move up 50 pixels per second
                x_offset = int(anim["velocity"] * elapsed * 20)  # Random horizontal drift
                alpha = 255 - int((elapsed / 2.0) * 255)  # Fade out over 2 seconds
                
                # Create a surface with alpha channel
                text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
                text_surface.fill((0, 0, 0, 0))  # Transparent fill
                text_surface.blit(text, (0, 0))
                # Apply alpha
                text_surface.set_alpha(alpha)
                
                self.window.blit(text_surface, (anim["x"] + x_offset, anim["y"] + y_offset))
            else:
                self.game.animation_items.remove(anim)

        # Draw tooltip
        if tooltip_text:
            tooltip_surface = self.small_font.render(tooltip_text, True, BLACK)
            tooltip_rect = tooltip_surface.get_rect()
            tooltip_rect.topleft = (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10)
            
            # Make sure tooltip stays on screen
            if tooltip_rect.right > self.width:
                tooltip_rect.right = self.width
            if tooltip_rect.bottom > self.height:
                tooltip_rect.bottom = self.height
            
            # Draw tooltip background
            pygame.draw.rect(self.window, (255, 255, 220), tooltip_rect.inflate(10, 10))
            pygame.draw.rect(self.window, BLACK, tooltip_rect.inflate(10, 10), 1)
            self.window.blit(tooltip_surface, tooltip_rect)

        # Update display
        pygame.display.update()


                        