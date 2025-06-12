# blob_life_game.py
# Author: Shreyasi Panthee (updated with child-friendly blob features and animated start page)
# Date Modified: 2025-06-11

import pygame
import random
from cell import Cell

# --- Initialization ---
pygame.init()
screen_width = 1100
screen_height = 630
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
    "Fairy": PASTEL_PURPLE,
    "None": BLACK
}
current_theme = "None"

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
pygame.mixer.music.load("assets/game-music.mp3")
pygame.mixer.music.play(-1)
blob_pop_sound = pygame.mixer.Sound("assets/button-click.mp3")

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
just_paused = False
is_muted = False # mute state

# Mute button dimensions
mute_button_rect = pygame.Rect(screen_width - 120, 20, 100, 40)

# Tutorial messages
tutorial_messages = [
    "Hi! I'm Blobbo. Let me teach you blob life!",
    "Click to place a blob!",
    "Press spacebar to watch your blobs grow!",
    "Nice job! You're ready to play!"
]

# Animated blobs for intro screen
animated_blobs = []
for _ in range(30):
    x = random.randint(0, 300)
    y = random.randint(0, screen_height)
    speed = random.choice([1, 2])
    direction = random.choice([-1, 1])
    img = random.choice(blob_images)
    animated_blobs.append({"x": x, "y": y, "speed": speed, "dir": direction, "img": img})

# Timing variables for generation updates
generation_interval = 500  # milliseconds between generations
last_update_time = pygame.time.get_ticks()

# --- Helper Functions ---
def draw_text_centered(text, y, font_obj, color=WHITE):
    rendered = font_obj.render(text, True, color)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)

def draw_text_left(text, x, y, font_obj, color=WHITE):
    rendered = font_obj.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_text_right(text, x, y, font_obj, color=WHITE):
    rendered = font_obj.render(text, True, color)
    rect = rendered.get_rect(right=x, centery=y)
    screen.blit(rendered, rect)

def draw_cells():
    for row in grid:
        for cell in row:
            if cell.alive and cell.image:
                screen.blit(cell.image, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size))
            pygame.draw.rect(screen, WHITE, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size, cell_size, cell_size), 1)

def draw_mute_button():
    color = (200, 0, 0) if is_muted else (0, 200, 0)
    pygame.draw.rect(screen, color, mute_button_rect)
    label = "Unmute" if is_muted else "Mute"
    text = font_2.render(label, True, WHITE)
    screen.blit(text, (mute_button_rect.x + 10, mute_button_rect.y + 10))

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
                new_grid[r][c].image = random.choice(blob_images)
            else:
                new_grid[r][c].image = None

            # Play sound only if a new cell is born
            if new_grid[r][c].alive and not grid[r][c].alive:
                if not is_muted:
                    blob_pop_sound.play()


    # Update the global grid
    grid[:] = new_grid
    generation += 1

def apply_template(name):
    global grid, generation
    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
    if name != "None":
        for r, c in templates[name]:
            grid[r][c].alive = True
            grid[r][c].image = random.choice(blob_images)
    generation = 0

def animate_blobs():
    for blob in animated_blobs:
        screen.blit(blob["img"], (blob["x"], blob["y"]))
        blob["x"] += blob["speed"] * blob["dir"]
        if 300 <= blob["x"] <= 800 or blob["x"] < 0 or blob["x"] > screen_width:
            # Keep blobs away from the center area (300–600)
            left_range = range(0, 300)
            right_range = range(801, screen_width)
            selected_range = random.choice([left_range, right_range])
            
            blob["x"] = random.randint(selected_range.start, selected_range.stop - 1)
            blob["y"] = random.randint(0, screen_height)

def draw_back_button():
    draw_text_left("<- Back", 20, 20, font_2)


# --- Main Game Loop ---
running = True
while running:
    screen.fill(themes[current_theme])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Back button detection (top left corner)
            if 20 <= mx <= 20 + 100 and 20 <= my <= 20 + 30:
                if screen_state in ["tutorial", "storyline", "simulation"]:
                    screen_state = "start_menu"
            if screen_state == "theme_select":
                y_offset = 180
                for i, theme in enumerate(themes):
                    if y_offset + i * 40 <= event.pos[1] <= y_offset + (i+1) * 40:
                        current_theme = theme
                        screen_state = "start_menu"
            elif screen_state == "start_menu":
                if 200 <= event.pos[1] <= 240:
                    screen_state = "tutorial"
                elif 260 <= event.pos[1] <= 300:
                    screen_state = "storyline"
                elif 320 <= event.pos[1] <= 360:
                    screen_state = "simulation"
                    # Reset grid when entering simulation
                    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                    generation = 0
                    simulation_running = False

                elif 500 <= event.pos[1] <= 540:
                    screen_state = "theme_select"
            elif screen_state == "tutorial":
                if tutorial_step < len(tutorial_messages) - 1:
                    tutorial_step += 1
                else:
                    screen_state = "simulation"
            elif screen_state == "simulation":
                mx, my = event.pos
                col = (mx - side_margin) // cell_size
                row = (my - top_margin) // cell_size
                if 0 <= row < grid_height and 0 <= col < grid_width:
                    grid[row][col].toggle(blob_images)
                    if not is_muted:
                        blob_pop_sound.play()

                # Mute button click detection
                if mute_button_rect.collidepoint(mx, my):
                    is_muted = not is_muted
                    if is_muted:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(1)

        elif event.type == pygame.KEYDOWN:
            if screen_state == "simulation":
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                    just_paused = not simulation_running  # Set to True only when you pause
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
        animate_blobs()
        draw_text_centered("Welcome to Blob Life!", 100, font)
        draw_text_centered("Game of Life with a Blob Twist!", 160, font_1)
        draw_text_centered("[Play]", 200, font_2)
        draw_text_centered("[Storyline]", 260, font_2)
        draw_text_centered("[Skip Tutorial - Jump to Game]", 320, font_2)
        draw_text_centered("<- Back to Themes", 500, font_2)

    elif screen_state == "tutorial":
        draw_text_centered("Blobbo Tutorial", 100, font)
        draw_text_centered(tutorial_messages[tutorial_step], 200, font_2)
        screen.blit(blobbo_img, (screen_width // 2 - 40, 300))
        draw_text_centered("Click to continue tutorial", 450, font_2)
        draw_back_button()

    elif screen_state == "simulation":
        draw_text_centered(f"Generation: {generation}", 40, font_1)
        pygame.draw.rect(screen, WHITE, (side_margin, 70, screen_width - 2 * side_margin, 10))
        progress = (generation % 20) * (screen_width // 20)
        pygame.draw.rect(screen, (255, 105, 180), (side_margin, 70, progress, 10))
        draw_cells()
        draw_back_button()
        draw_mute_button()
        draw_text_right("Controls:", screen_width - 150, 20, font_2)
        draw_text_right("Space: Pause/Resume", screen_width - 150, 50, font_2)
        draw_text_right("R: Reset", screen_width - 150, 70, font_2)
        draw_text_right("1: Heart Template", screen_width - 150, 90, font_2)
        draw_text_right("2: Smiley Template", screen_width - 150, 110, font_2)
        draw_text_right("3: Letter A Template", screen_width - 150, 130, font_2)
        draw_text_right("Click to toggle blobs", screen_width - 150, 150, font_2)
        draw_text_right("Mute/Unmute Music", screen_width - 150, 170, font_2)
        draw_text_right("Click to place blobs", screen_width - 150, 190, font_2)
        # Rules on the left
        draw_text_left("Blob Life Rules:", 2, 120, font)
        draw_text_left("Lonely blob? It poofs!", 2, 180, font_2)
        draw_text_left("(0–1 friends)", 2, 200, font_2)
        draw_text_left("Happy blob? It stays!", 2, 225, font_2)
        draw_text_left("(2–3 friends)", 2, 245, font_2)
        draw_text_left("Crowded blob? It poofs!", 2, 270, font_2)
        draw_text_left("(4+ friends)", 2, 290, font_2)
        draw_text_left("New blob? 3 nearby friends!", 2, 315, font_2)

         # Update generations on interval only when simulation_running is True
        current_time = pygame.time.get_ticks()
        if simulation_running and (current_time - last_update_time >= generation_interval):
            next_generation()
            last_update_time = current_time

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
