# actions.py - Functions for game actions
from pygame import mixer

# Try to load sounds
try:
    click_sound = mixer.Sound("assets/sounds/click.wav")
    buy_sound = mixer.Sound("assets/sounds/buy.wav")
    achievement_sound = mixer.Sound("assets/sounds/achievement.wav")
except:
    # Create placeholder sounds if not found
    click_sound = None
    buy_sound = None
    achievement_sound = None

def get_wood_action(game):
    amount = game.click_power
    game.wood += amount
    game.total_wood_collected += amount
    game.clicks += 1
    game.add_animation(f"+{amount}", 200, 200)
    game.check_achievements()
    if click_sound:
        click_sound.play()
    return True

def buy_beaver_action(game):
    if game.wood >= game.beaver_price:
        game.wood -= game.beaver_price
        game.beavers += 1
        old_price = game.beaver_price
        game.beaver_price = int(game.beaver_price * 1.1)
        game.calculate_wood_per_second()
        game.check_achievements()
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Bought 1 beaver for {old_price} wood!")
        return True
    return False

def buy_dam_action(game):
    if game.wood >= game.dam_price:
        game.wood -= game.dam_price
        game.dams += 1
        old_price = game.dam_price
        game.dam_price = int(game.dam_price * 1.15)
        game.calculate_wood_per_second()
        game.check_achievements()
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Bought 1 dam for {old_price} wood!")
        return True
    return False

def buy_lodge_action(game):
    if game.wood >= game.lodge_price:
        game.wood -= game.lodge_price
        game.lodges += 1
        old_price = game.lodge_price
        game.lodge_price = int(game.lodge_price * 1.2)
        game.calculate_wood_per_second()
        game.check_achievements()
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Bought 1 lodge for {old_price} wood!")
        return True
    return False

def buy_sapling_action(game):
    if game.wood >= game.sapling_price:
        game.wood -= game.sapling_price
        game.saplings += 1
        old_price = game.sapling_price
        game.sapling_price = int(game.sapling_price * 1.25)
        game.calculate_wood_per_second()
        game.check_achievements()
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Bought 1 sapling for {old_price} wood!")
        return True
    return False

def buy_forest_action(game):
    if game.wood >= game.forest_price:
        game.wood -= game.forest_price
        game.forests += 1
        old_price = game.forest_price
        game.forest_price = int(game.forest_price * 1.3)
        game.calculate_wood_per_second()
        game.check_achievements()
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Bought 1 forest for {old_price} wood!")
        return True
    return False

def upgrade_click_action(game):
    if game.wood >= game.click_upgrade_price:
        game.wood -= game.click_upgrade_price
        old_power = game.click_power
        game.click_power += 1
        old_price = game.click_upgrade_price
        game.click_upgrade_price = int(game.click_upgrade_price * 1.5)
        if buy_sound:
            buy_sound.play()
        game.add_notification(f"Upgraded click power from {old_power} to {game.click_power} for {old_price} wood!")
        return True
    return False

def save_game_action(game):
    game.save_game()
    return True