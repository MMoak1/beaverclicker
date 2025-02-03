import pygame

# Initialize pygame
pygame.init()

# Game window dimensions (800x800)
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beaver Clicker Game")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BUTTON_COLOR = (100, 100, 255)
TEXT_COLOR = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 40)

# Initial game variables
wood_count = 0
beaver_count = 0
beaver_price = 10

# Button dimensions
button_width, button_height = 200, 80
get_wood_button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 3, button_width, button_height)
add_beaver_button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2 + 100, button_width, button_height)

# Initial time tracking variable
last_time = pygame.time.get_ticks()

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

    # Draw the wood counter
    wood_text = font.render(f"Wood: {wood_count}", True, TEXT_COLOR)
    window.blit(wood_text, (10, 10))

    # Draw the beaver counter
    beaver_text = font.render(f"Beavers: {beaver_count}", True, TEXT_COLOR)
    window.blit(beaver_text, (10, 50))

    beaver_price_text = font.render(f"Beaver Price: {beaver_price}", True, TEXT_COLOR)
    window.blit(beaver_price_text, (WIDTH - 250, 10))  # Display price in top-right corner

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

    # Update wood count based on beavers
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= 1000:
        wood_count += beaver_count
        last_time = current_time 

    # Update the window
    draw_window()

    # Frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()

