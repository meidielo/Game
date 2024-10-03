import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Drag and Drop Example')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Symbols (you can use images or text)
symbols = ['5', '+', '7']
symbol_rects = []  # Rectangles to define where each symbol is
empty_spot = pygame.Rect(500, 250, 100, 50)  # A rect for the drop zone

# Set positions for symbols
for i, symbol in enumerate(symbols):
    symbol_rect = pygame.Rect(100 + i * 150, 100, 50, 50)
    symbol_rects.append(symbol_rect)

# Dragging state
dragging = False
dragged_symbol_index = None

def draw_screen():
    screen.fill(WHITE)
    
    # Draw symbols
    for i, symbol in enumerate(symbols):
        pygame.draw.rect(screen, BLACK, symbol_rects[i], 2)
        text_surface = font.render(symbol, True, BLACK)
        screen.blit(text_surface, (symbol_rects[i].x + 10, symbol_rects[i].y + 10))

    # Draw empty spot (drop zone)
    pygame.draw.rect(screen, BLACK, empty_spot, 2)
    screen.blit(font.render('Drop Here', True, BLACK), (empty_spot.x + 10, empty_spot.y + 10))
    
    pygame.display.update()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse clicked on any symbol
            mouse_pos = event.pos
            for i, rect in enumerate(symbol_rects):
                if rect.collidepoint(mouse_pos):
                    dragging = True
                    dragged_symbol_index = i
                    offset_x = rect.x - mouse_pos[0]
                    offset_y = rect.y - mouse_pos[1]
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                # Check if the symbol was dropped on the empty spot
                if empty_spot.colliderect(symbol_rects[dragged_symbol_index]):
                    print(f"Symbol '{symbols[dragged_symbol_index]}' dropped in the spot!")
                
                dragging = False
                dragged_symbol_index = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Move the symbol with the mouse
                mouse_pos = event.pos
                symbol_rects[dragged_symbol_index].x = mouse_pos[0] + offset_x
                symbol_rects[dragged_symbol_index].y = mouse_pos[1] + offset_y

    draw_screen()

pygame.quit()
