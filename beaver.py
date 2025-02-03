import pygame

# Initialize pygame
pygame.init()

# Game window dimensions (800x800)
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beaver Clicker Game")

# Colors
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 255)
TEXT_COLOR = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 40)

# Initial game variables
wood_count = 0
beaver_count = 0
beaver_price = 10
beaver_dam_price = 100  # Example price for Beaver Dam

# Load the beaver image
beaver_image = pygame.image.load(r"C:\ai-fun\beaver_guy.png")
beaver_image = pygame.transform.scale(beaver_image, (200, 200))  # Resize it to fit in the window

# Button dimensions
button_width, button_height = 200, 80
get_wood_button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 3, button_width, button_height)
add_beaver_button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2 + 100, button_width, button_height)
buy_beaver_dam_button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2 + 200, button_width, button_height)  # New "Buy Beaver Dam" button

# Initial time tracking variable
last_time = pygame.time.get_ticks()

# Beaver's position relative to the "Get Wood" button
beaver_x = get_wood_button_rect.x + (get_wood_button_rect.width // 2) - 300  # Adjust x to center next to the button
beaver_y = get_wood_button_rect.y - 100  # Adjust y to position above the button

# Function to draw everything
def draw_window():
    window.fill(WHITE)

    # Draw the "Get Wood" button
    pygame.draw.rect(window, BUTTON_COLOR, get_wood_button_rect)
    get_wood_button_text = font.render("Get Wood", True, TEXT_COLOR)
    window.blit(get_wood_button_text, (get_wood_button_rect.x + 30, get_wood_button_rect.y + 25))

    # Draw the "Add Beaver" button
    pygame.draw.rect(window, BUTTON_COLOR, add_beaver_button_rect)
    add_beaver_button_text = font.render("Add Beaver", True, TEXT_COLOR)
    window.blit(add_beaver_button_text, (add_beaver_button_rect.x + 20, add_beaver_button_rect.y + 25))

    # Draw the "Buy Beaver Dam" button
    pygame.draw.rect(window, BUTTON_COLOR, buy_beaver_dam_button_rect)
    buy_beaver_dam_button_text = font.render("Buy Beaver Dam", True, TEXT_COLOR)
    window.blit(buy_beaver_dam_button_text, (buy_beaver_dam_button_rect.x + 20, buy_beaver_dam_button_rect.y + 25))

    # Draw the wood counter
    wood_text = font.render(f"Wood: {wood_count}", True, TEXT_COLOR)
    window.blit(wood_text, (10, 10))

    # Draw the beaver counter
    beaver_text = font.render(f"Beavers: {beaver_count}", True, TEXT_COLOR)
    window.blit(beaver_text, (10, 50))

    # Draw the beaver price with two lines ("Beaver" on the first line and "Price" on the second)
    beaver_price_text1 = font.render("Beaver", True, TEXT_COLOR)
    window.blit(beaver_price_text1, (add_beaver_button_rect.x + 200, add_beaver_button_rect.y))  # "Beaver" text

    beaver_price_text2 = font.render(f"Price: {beaver_price} wood", True, TEXT_COLOR)
    window.blit(beaver_price_text2, (add_beaver_button_rect.x + 200, add_beaver_button_rect.y + 30))  # "Price" text

    # Draw the beaver dam price with two lines ("Beaver Dam" on the first line and "Price" on the second)
    beaver_dam_price_text1 = font.render("Beaver Dam", True, TEXT_COLOR)
    window.blit(beaver_dam_price_text1, (buy_beaver_dam_button_rect.x + 200, buy_beaver_dam_button_rect.y))  # "Beaver Dam" text

    beaver_dam_price_text2 = font.render(f"Price: {beaver_dam_price} wood", True, TEXT_COLOR)
    window.blit(beaver_dam_price_text2, (buy_beaver_dam_button_rect.x + 200, buy_beaver_dam_button_rect.y + 30))  # "Price" text

    # Draw the beaver image near the "Get Wood" button
    window.blit(beaver_image, (beaver_x, beaver_y))

    pygame.display.update()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if get_wood_button_rect.collidepoint(event.pos):
                wood_count += 1  # Increase wood count when "Get Wood" button is clicked
            elif add_beaver_button_rect.collidepoint(event.pos):
                if wood_count >= beaver_price:
                    wood_count -= beaver_price  # Deduct the current price of a beaver
                    beaver_count += 1  # Add a beaver
                    beaver_price = int(beaver_price * 1.1)  # Increase the price by 10%
            elif buy_beaver_dam_button_rect.collidepoint(event.pos):
                if wood_count >= beaver_dam_price:
                    wood_count -= beaver_dam_price  # Deduct the current price of a Beaver Dam
                    # You can add a Beaver Dam functionality here later if needed
                    print("Bought a Beaver Dam!")

    # Update the window
    draw_window()

    # Frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
