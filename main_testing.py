# blob_life_game.py
# Author: Shreyasi Panthee (updated with child-friendly blob features)
# Date Modified: 2025-06-11

import pygame
import random
from cell import Cell

# --- Initialization ---
pygame.init()
screen_width = 1100
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blob Life")

# Constants
grid_width = 10
grid_height = 10
cell_size = 50

grid_pixel_width = grid_width * cell_size
grid_pixel_height = grid_height * cell_size
side_margin = (screen_width - grid_pixel_width) // 2
top_margin = 120

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (10, 10, 50)
PASTEL_PINK = (255, 204, 229)
PASTEL_YELLOW = (255, 255, 204)
PASTEL_GREEN = (204, 255, 204)
PASTEL_PURPLE = (229, 204, 255)

# Themes
themes = {
    "Ocean": DARK_BLUE,
    "Candy": PASTEL_PINK,
    "Lemonade": PASTEL_YELLOW,
    "Meadow": PASTEL_GREEN,
    "Fairy": PASTEL_PURPLE
}
current_theme = "Ocean"

# Fonts
font = pygame.font.Font(None, 50)
font_1 = pygame.font.Font(None, 36)
font_2 = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Load assets
blob_images = [
    pygame.transform.scale(pygame.image.load("assets/blob1.png"), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load("assets/blob2.png"), (cell_size, cell_size))
]
blobbo_img = pygame.transform.scale(pygame.image.load("assets/blobbo.png"), (80, 80))
play_img = pygame.image.load("assets/play.png")
pause_img = pygame.image.load("assets/pause.png")
fast_forward_img = pygame.image.load("assets/fast_forward.png")
reset_img = pygame.image.load("assets/reset.png")
prev_img = pygame.image.load("assets/prev.png")

# Music and Sound
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
blob_pop_sound = pygame.mixer.Sound("assets/pop.mp3")

# Templates
templates = {
    "Letter A": [(4,5), (5,4), (5,6), (6,3), (6,7), (7,3), (7,7), (8,4), (7,5), (8,6)],
    "Smiley": [(4,3), (4,7), (6,4), (6,5), (6,6), (6,7)],
    "Heart": [(6,4), (5,3), (5,5), (4,2), (4,6), (3,2), (3,6), (2,3), (3,4), (2,5)]
}

# State
screen_state = "theme_select"
grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
simulation_running = False
generation = 0
tutorial_step = 0

# Tutorial messages
tutorial_messages = [
    "Hi! I'm Blobbo. Let me teach you blob life!",
    "Click to place a blob!",
    "Press spacebar to watch your blobs grow!",
    "Nice job! You're ready to play!"
]

# --- Helper Functions ---
def draw_text_centered(text, y, font_obj, color=WHITE):
    rendered = font_obj.render(text, True, color)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)

def draw_text_left(text, x, y, font_obj, color=WHITE):
    rendered = font_obj.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_cells(surface):
    for row in grid:
        for cell in row:
            if cell.alive and cell.image:
                    surface.blit(cell.image, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size))
            pygame.draw.rect(surface, WHITE, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size, cell_size, cell_size), 1)
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
    global generation
    new_grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
    for r in range(grid_height):
        for c in range(grid_width):
            neighbors = count_neighbors(r, c)
            if grid[r][c].alive:
                alive_next = neighbors in [2, 3]
            else:
                alive_next = neighbors == 3

            new_grid[r][c].alive = alive_next

            # Set image for alive cells, None for dead
            if alive_next:
                new_grid[r][c].image = random.choice(blob_images)  # Optional: random blob image for fun
            else:
                new_grid[r][c].image = None

            # Play sound only if a new cell is born
            if new_grid[r][c].alive and not grid[r][c].alive:
                blob_pop_sound.play()

    # Update the global grid
    grid[:] = new_grid
    generation += 1


def apply_template(name):
    global grid, generation
    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
    for r, c in templates[name]:
        grid[r][c].alive = True
        grid[r][c].image = random.choice(blob_images)  # Assign blob image here!
    generation = 0

# --- Main Game Loop ---
running = True
while running:
    screen.fill(themes[current_theme])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if screen_state == "theme_select":
                if my > 180:
                    theme_names = list(themes.keys())
                    index = (my - 180) // 40
                    if 0 <= index < len(theme_names):
                        current_theme = theme_names[index]
                        screen_state = "start_menu"
            elif screen_state == "start_menu":
                screen_state = "tutorial"
            elif screen_state == "tutorial":
                tutorial_step += 1
                if tutorial_step >= len(tutorial_messages):
                    screen_state = "simulation"
            elif screen_state == "simulation":
                col = (mx - side_margin) // cell_size
                row = (my - top_margin) // cell_size
                if 0 <= row < grid_height and 0 <= col < grid_width:
                    grid[row][col].toggle(blob_images)
                    blob_pop_sound.play()
        elif event.type == pygame.KEYDOWN:
            if screen_state == "simulation":
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_r:
                    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                    generation = 0
                    simulation_running = False
                elif event.key == pygame.K_1:
                    apply_template("Heart")
                elif event.key == pygame.K_2:
                    apply_template("Smiley")
                elif event.key == pygame.K_3:
                    apply_template("Letter A")

    if screen_state == "theme_select":
        draw_text_centered("Choose Your Theme!", 100, font)
        for i, theme in enumerate(themes):
            draw_text_centered(f"{i + 1}. {theme}", 180 + i * 40, font_2)
    elif screen_state == "start_menu":
        draw_text_centered("Welcome to Blob Life!", 150, font)
        draw_text_centered("Click anywhere to begin", 220, font_1)
    elif screen_state == "tutorial":
        draw_text_centered("Blobbo Tutorial", 100, font)
        draw_text_centered(tutorial_messages[tutorial_step], 200, font_2)
        screen.blit((blobbo_img) , (screen_width // 2 - 40, 300))
    elif screen_state == "simulation":
        draw_text_centered(f"Blob World: Generation {generation}", 40, font_1)
        progress = (generation % 20) * (screen_width // 20)
        pygame.draw.rect(screen, WHITE, (side_margin, 70, screen_width - 2 * side_margin, 10))
        pygame.draw.rect(screen, (255, 105, 180), (side_margin, 70, progress, 10))
        draw_cells(screen)

        # Rules on the left
        draw_text_left("Blob Life Rules:", 2, 120, font)
        draw_text_left("Lonely blob? It poofs! (0–1 friends)", 2, 180, font_2)
        draw_text_left("Happy blob? It stays! (2–3 friends)", 2, 220, font_2)
        draw_text_left("Crowded blob? It poofs! (4+ friends)", 2, 260, font_2)
        draw_text_left("New blob? 3 nearby friends!", 2, 300, font_2)

        if simulation_running:
            next_generation()
            clock.tick(2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
