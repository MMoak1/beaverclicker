# game_state.py - Manages the game state
import pygame
import json
import os
import random

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