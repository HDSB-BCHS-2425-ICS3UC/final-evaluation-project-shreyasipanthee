# Author: Shreyasi Panthee
# Date Modified: 2025-6-5
# Description:

import pygame

# Introduction
print("Welcome to Conway's Game of Life!")
print("A simulation of cellular life and death based on mathematical rules.")

# Rules of the Game
print("Rules:")
print("1. Any live cell with fewer than two live neighbors dies (underpopulation).")
print("2. Any live cell with two or three live neighbors lives on to the next generation.")
print("3. Any live cell with more than three live neighbors dies (overpopulation).")
print("4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).")

pygame.init()

# Screen Size
# The screen size is 1800x1000 pixels
screen_width, screen_height = 1250, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("10x10 Grid")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Grid cell size
cell_size = 60

# Grid Size
# The grid size is 10x10
grid_size = 10


runnning = True
while runnning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False
    
    screen.fill(black) # Fill the screen with black
    # Draw grid lines
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, white, (x, y, cell_size, cell_size), 1)
        
    pygame.display.flip()  # Update the display

pygame.quit()  # Quit the game