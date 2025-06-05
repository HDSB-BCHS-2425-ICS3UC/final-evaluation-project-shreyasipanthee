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

grid_width = 10
grid_height = 10
cell_size = 50
aspect_ratio = grid_width / grid_width

screen_width = grid_width * cell_size
screen_height = grid_height * cell_size

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")

game_surface = pygame.Surface((screen_width, screen_height))

def draw_grid(surface, width, height, cell_size, color):
    # Draw vertical lines
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    
    # Draw horizontal lines
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, color, (0, y), (width, y))

# Grid Size
# The grid size is 10x10
grid_size = 10


runnning = True
while runnning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False
        
        elif event.type == pygame.VIDEORESIZE:
            # Maintain aspect ratio
            new_width = event.w
            new_height = int(new_width / aspect_ratio)
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    screen.fill(black) # Fill the screen with black
    draw_grid(screen, screen_width, screen_height, cell_size, white)    
    pygame.display.flip()  # Update the display

pygame.quit()  # Quit the game