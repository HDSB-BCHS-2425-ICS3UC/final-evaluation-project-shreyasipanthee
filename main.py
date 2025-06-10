# Author: Shreyasi Panthee
# Date Modified: 2025-6-5
# Description:
#Implement better toggle function
# Create menu for preexisting patterns
# make new cells green, dead ones black, and alive since the previous generation or longer white and but it in a legend
# for restart, start stop etc. buttons make them look like pause play fast forward etc. using both keys and mousclicks
# move grid to center and make screen fuulscreen

import pygame
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

# === Constants ===
grid_width, grid_height = 10, 10
cell_size = 50
top_margin = 70
side_margin = 50

# === Screen ===
grid_pixel_width = grid_width * cell_size
grid_pixel_height = grid_height * cell_size
screen_width = grid_pixel_width * 2 + side_margin * 2
screen_height = grid_pixel_height + top_margin + 70

# === Colors ===
black = (0, 0, 15)
white = (255, 255, 255)
dark_blue = (50, 0, 50)
green = (0, 255, 0)

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.Font(None, 40)
font_1 = pygame.font.Font(None, 30)
font_2 = pygame.font.Font(None, 25)
clock = pygame.time.Clock()

# === Grid State ===
grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
simulation_running = False
generation = 0
grid_history = []
click_handled = False

# === Drawing ===
def draw_grid(surface):
    for col in range(grid_width + 1):
        x = side_margin + col * cell_size
        pygame.draw.line(surface, white, (x, top_margin), (x, top_margin + grid_height * cell_size))    
    for row in range(grid_height + 1):
        y = top_margin + row * cell_size
        pygame.draw.line(surface, white, (side_margin, y), (side_margin + grid_width * cell_size, y))

def draw_cells(surface):
    for row in grid:
        for cell in row:
            cell.draw(surface, cell_size, top_margin, side_margin, white, black, green)

def draw_legend(surface):
    legend_x = side_margin
    legend_y = top_margin + grid_pixel_height + 80
    pygame.draw.rect(surface, white, (legend_x, legend_y, 200, 100))
    pygame.draw.rect(surface, black, (legend_x, legend_y, 200, 100), 2)
    pygame.draw.rect(surface, green, (legend_x + 10, legend_y + 10, 20, 20))
    pygame.draw.rect(surface, black, (legend_x + 10, legend_y + 40, 20, 20))
    pygame.draw.rect(surface, white, (legend_x + 10, legend_y + 70, 20, 20))
    surface.blit(font_2.render("New Cell", True, black), (legend_x + 40, legend_y + 10))
    surface.blit(font_2.render("Dead Cell", True, black), (legend_x + 40, legend_y + 40))
    surface.blit(font_2.render("Alive Cell", True, black), (legend_x + 40, legend_y + 70))

def draw_button(surface, text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, white, rect)
    pygame.draw.rect(surface, black, rect, 2)
    label = font_2.render(text, True, black)
    surface.blit(label, label.get_rect(center=rect.center))
    return rect

# === Game Logic ===
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
                new_grid[r][c].alive = alive_neighbors in [2, 3]
            else:
                new_grid[r][c].alive = alive_neighbors == 3
    return new_grid

# Main loop
                
running = True
while running:
    screen.fill(dark_blue)
    screen.blit(font.render("Conway's Game of Life", True, white), (screen_width - 460, 10))
    screen.blit(font_1.render(f"Generation: {generation}", True, white), (side_margin, top_margin - 25))

    draw_grid(screen)
    draw_cells(screen)
    draw_legend(screen)

    start_button = draw_button(screen, "▶" if not simulation_running else "||", side_margin, top_margin + grid_pixel_height + 20, 60, 40)
    next_button = draw_button(screen, "⏭", side_margin + 70, top_margin + grid_pixel_height + 20, 60, 40)
    reset_button = draw_button(screen, "🔄", side_margin + 140, top_margin + grid_pixel_height + 20, 60, 40)
    prev_button = draw_button(screen, "⏮", side_margin + 210, top_margin + grid_pixel_height + 20, 60, 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_running = not simulation_running
            elif event.key == pygame.K_RIGHT:
                grid = next_generation()
                generation += 1
            elif event.key == pygame.K_UP:
                grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                generation = 0
            elif event.key == pygame.K_LEFT and generation > 0:
                generation -= 1
                # Future: grid = grid_history[generation]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if top_margin < mouse_y < top_margin + grid_pixel_height:
                col = (mouse_x - side_margin) // cell_size
                row = (mouse_y - top_margin) // cell_size
                if 0 <= col < grid_width and 0 <= row < grid_height:
                    grid[row][col].toggle()
                    click_handled = True

        if event.type == pygame.MOUSEBUTTONUP:
            click_handled = False

    if simulation_running:
        grid = next_generation()
        generation += 1
        clock.tick(10)

    pygame.display.flip()

pygame.quit()
