# Author: Shreyasi Panthee
# Date Modified: 2025-6-5
# Description:

import pygame
import sys
from cell import Cell  

# Introduction
print("Welcome to Conway's Game of Life!")
print("A simulation of cellular life and death based on mathematical rules.")

# Rules of the Game
print("Rules:")
print("1. Any live cell with fewer than two live neighbors dies (underpopulation).")
print("2. Any live cell with two or three live neighbors lives on to the next generation.")
print("3. Any live cell with more than three live neighbors dies (overpopulation).")
print("4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).")

# Constants
grid_width = 10
grid_height = 10
cell_size = 50
top_margin = 100 # Space for Grid header and buttons
side_margin = 50

# Calculate screen dimensions
grid_pixel_width = grid_width * cell_size
grid_pixel_height = grid_height * cell_size
screen_width = grid_pixel_width + side_margin * 2
screen_height = grid_pixel_height + top_margin + 50  # Adding space for the header

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

# Grid and State Initialization
grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
simulation_running = False
generation = 0

def draw_grid(surface, cell_size, rows, cols, colour, offset_x, offset_y):
    # Draw vertical lines
    for col in range(cols + 1):
        x= offset_x + col * cell_size
        pygame.draw.line(surface, colour, (x, offset_y), (x, offset_y + rows * cell_size))    
    # Draw horizontal lines
    for row in range(rows + 1):
        y = offset_y + row * cell_size
        pygame.draw.line(surface, colour, (offset_x, y), (offset_x + cols * cell_size, y))

def draw_cells(surface):
    for row in grid:
        for cell in row:
            cell.draw(surface, cell_size, top_margin, side_margin, white, black, white)

def count_neighbors(r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_height and 0 <= nc < grid_width:
                if grid[nr][nc].alive:
                    count += 1
    return count

def next_generation():
    global grid
    new_grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
    for r in range(grid_height):
        for c in range(grid_width):
            alive_neighbors = count_neighbors(r, c)
            if grid[r][c].alive:
                    new_grid[r][c].alive = alive_neighbors in [2, 3]  # Survive if 2 or 3 neighbors
            else:
                new_grid[r][c].alive = alive_neighbors == 3  # Become alive if exactly 3 neighbors
    return new_grid

def draw_button(surface, text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, white, rect)
    pygame.draw.rect(surface, black, rect, 2)
    label = font.render(text, True, black)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)
    return rect
                
running = True
while running:
    screen.fill(black)  # Fill the screen with black

    # Draw title
    title_text = font.render("Conway's Game of Life", True, white)
    screen.blit(title_text, (screen_width - 425, 20))

    # Draw generation count
    generation_text = font.render("Generation: 0", True, white)
    screen.blit(generation_text, (screen_width - 550, 70))

    # Draw grid in center
    draw_grid(screen, cell_size, grid_height, grid_width, white, side_margin, top_margin)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            # Maintain aspect ratio
            new_width = event.w
            new_height = int(new_width / aspect_ratio)
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    pygame.display.flip()  # Update the display

pygame.quit()  # Quit the game