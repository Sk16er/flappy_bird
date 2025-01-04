import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (40, 40))
background_image = pygame.image.load("background.png")
pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (70, 500))

# Colors (only used for text now)
WHITE = (255, 255, 255)

# Game variables
PIPE_GAP = 150
PIPE_SPEED = 5
BIRD_SPEED = 5
GRAVITY = 0.5

# Bird class
class Bird:
    def __init__(self):
        self.image = bird_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self, direction):
        if direction == "UP":
            self.rect.y -= BIRD_SPEED
        elif direction == "DOWN":
            self.rect.y += BIRD_SPEED
        else:
            self.velocity += GRAVITY
            self.rect.y += self.velocity

    def flap(self):
        self.velocity = -BIRD_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top_rect = pipe_image.get_rect(midbottom=(x, self.height))
        self.bottom_rect = pipe_image.get_rect(midtop=(x, self.height + PIPE_GAP))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.midbottom = (self.x, self.height)
        self.bottom_rect.midtop = (self.x, self.height + PIPE_GAP)

    def draw(self, screen):
        screen.blit(pipe_image, self.top_rect)
        screen.blit(pygame.transform.flip(pipe_image, False, True), self.bottom_rect)

# Function to draw text
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Home screen
def show_home_screen():
    screen.blit(background_image, (0, 0))
    draw_text(screen, "Flappy Bird", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, "Press SPACE to Start", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    wait_for_space()

# End screen
def show_end_screen(score):
    screen.blit(background_image, (0, 0))
    draw_text(screen, "Game Over", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, f"Score: {score}", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press SPACE to Restart", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()
    wait_for_space()

# Wait for space key
def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Main game loop
def main():
    clock = pygame.time.Clock()

    while True:
        show_home_screen()
        run_game()
        show_end_screen(score)

# Run game
def run_game():
    global score
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    direction = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = "UP"
                elif event.key == pygame.K_s:
                    direction = "DOWN"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    direction = None

        bird.update(direction)

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe_image.get_width() < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH + 200))
                score += 1

        # Check for collisions
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                running = False
        if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
            running = False

        # Draw everything
        screen.blit(background_image, (0, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Display score
        draw_text(screen, f"Score: {score}", 36, WHITE, 10, 10)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
