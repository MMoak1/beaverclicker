import pygame
import random

# Initialize pygame
pygame.init()

# Set up game window
WIDTH = 400
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.5
bird_movement = 0
bird_position = [100, 300]
bird_velocity = 0
bird_jump = -10
bird_rect = pygame.Rect(bird_position[0], bird_position[1], 30, 30)

pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipes = []

score = 0
font = pygame.font.Font(None, 36)

# Load bird image
bird_image = pygame.Surface((30, 30))
bird_image.fill(BLUE)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)

    def move(self):
        self.x -= pipe_velocity
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(window, GREEN, self.top_rect)
        pygame.draw.rect(window, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x < -pipe_width

    def collision(self, bird):
        return bird.colliderect(self.top_rect) or bird.colliderect(self.bottom_rect)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = bird_jump

    # Bird physics
    bird_velocity += gravity
    bird_position[1] += bird_velocity
    bird_rect.y = bird_position[1]

    if bird_position[1] >= HEIGHT - 30:
        bird_position[1] = HEIGHT - 30
        bird_velocity = 0

    # Generate pipes
    if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
        pipes.append(Pipe())

    # Move pipes and check for collisions
    for pipe in pipes[:]:
        pipe.move()
        if pipe.off_screen():
            pipes.remove(pipe)
            score += 1
        if pipe.collision(bird_rect):
            running = False

    # Draw everything
    window.fill(WHITE)
    for pipe in pipes:
        pipe.draw()
    window.blit(bird_image, bird_rect)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    window.blit(score_text, (10, 10))

    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(60)

# Game Over
pygame.quit()
