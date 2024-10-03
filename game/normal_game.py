import pygame
import requests

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arithmetic Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size
player_speed = 10

# Font settings
font = pygame.font.SysFont(None, 48)

# Game variables
current_question = ""
correct_answer = 0
player_move = 0
question_answered = False

# Fetch a question from Django API
def fetch_question():
    response = requests.get("http://127.0.0.1:8000/generate_question/")
    data = response.json()
    return data["question"], data["answer"]

# Draw text on screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Main game loop
running = True
current_question, correct_answer = fetch_question()

while running:
    screen.fill(WHITE)
    
    # Display the question
    draw_text(f"Solve: {current_question}", font, BLACK, screen, 50, 50)
    
    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update player position if a question was answered correctly
    if question_answered:
        player_x += player_move
        question_answered = False  # Reset after moving

    # Ensure the player doesn't move out of bounds
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_size:
        player_x = WIDTH - player_size

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
