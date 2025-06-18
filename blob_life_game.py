# blob_life_game.py
# Author: Shreyasi Panthee
# Date Modified: 2025-06-18
# Description: A fun version of Conway's Game of Life using blobs, animations, music, templates, and a colorful Pygame interface.

# === IMPORTS ===
import pygame
import random
from cell import Cell # Cell class handles each grid cell's state and image

# === INITIALIZATION ===
pygame.init()
screen_width = 1100
screen_height = 630
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blob Life")
clock = pygame.time.Clock()

# === GRID AND CELL SETTINGS ===
grid_width = 10
grid_height = 10
cell_size = 50
grid_pixel_width = grid_width * cell_size
grid_pixel_height = grid_height * cell_size
side_margin = (screen_width - grid_pixel_width) // 2
top_margin = 120

# === COLORS ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230) 
PASTEL_PINK = (255, 204, 229)
HONEY_YELLOW = (246,190,0)
PASTEL_GREEN = (204, 255, 204)
PASTEL_PURPLE = (229, 204, 255)

# === THEMES ===
themes = {
    "Ocean": LIGHT_BLUE,
    "Candy": PASTEL_PINK,
    "Honey": HONEY_YELLOW,
    "Meadow": PASTEL_GREEN,
    "Fairy": PASTEL_PURPLE,
    "None": BLACK
}
current_theme = "None"

# === FONTS ===
font = pygame.font.Font(None, 50)
font_1 = pygame.font.Font(None, 36)
font_2 = pygame.font.Font(None, 28)

# === STORYLINE TEXT ===
story_lines = [
    "The Blob Life Story",
    "",
    "Once upon a time, a genius named Conway made",
    "a grid where life grew using rules, not magic!",
    "",
    "Now blobs have taken over in this playful version!",
    "They pop in, disappear, or stay—based on how",
    "many blob buddies are around.",
    "",
    "It's Conway's Game of Life... blobified!"
]

# === ASSETS ===
# Load blob images and scale them to cell size
blob_images = [
    pygame.transform.scale(pygame.image.load("assets/blob1.png"), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load("assets/blob2.png"), (cell_size, cell_size))
]
blobbo_img = pygame.transform.scale(pygame.image.load("assets/blobbo.png"), (80, 80))

# === MUSIC AND SOUND ===
pygame.mixer.music.load("assets/game-music.mp3")
pygame.mixer.music.play(-1)
blob_pop_sound = pygame.mixer.Sound("assets/button-click.mp3")

# === TEMPLATES ===
# Predefined templates for user convenience
templates = {
    "Letter A": [(1,3), (1,4), (1,5), (1,6), (2,3), (2,6), (3,3), (3,4), (3,5), (3,6), (4,3), (4,6), (5,3), (5,6)],
    "Smiley": [(7,4), (6,3), (7,5), (6,6), (5,2), (5,7), (2,3), (2,6), (3,3), (3,6), (1,3), (1,6)],
    "Heart": [(6,4), (5,3), (5,5), (4,2), (4,6), (3,2), (3,6), (2,3), (3,4), (2,5)]
}

# === GAME STATE ===
screen_state = "start_page" # Current screen state
grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
simulation_running = False # Controls whether the simulation is running
generation = 0             # Current generation number
tutorial_step = 0          # Current tutorial step
just_paused = False        # Checks if the simulation was just paused
is_muted = False           # Checks if the music is muted

# === BUTTON LOCATIONS ===
mute_button_rect = pygame.Rect(screen_width - 120, 20, 100, 40)
start_button_rect = pygame.Rect(screen_width//2 - 150, screen_height//2 +60 , 300, 50)
back_button_rect = pygame.Rect(20, 20, 100, 30)  # Back button in the top left corner

# === TUTORIAL MESSAGES ===
tutorial_messages = [
    "Hi! I'm Blobbo. Let me teach you blob life!",
    "Click to place a blob!",
    "Press spacebar to watch your blobs grow!",
    "Nice job! You're ready to play!"
]

# === ANIMATED BLOBS ===
# Creates animated blobs that move across the screen
animated_blobs = []
for _ in range(30):
    x = random.randint(0, 300)
    y = random.randint(0, screen_height)
    speed = random.choice([1, 2])
    direction = random.choice([-1, 1])
    img = random.choice(blob_images)
    animated_blobs.append({"x": x, "y": y, "speed": speed, "dir": direction, "img": img})

# === TIMING FOR GENERATIONS ===
generation_interval = 500  # Default time between generations in milliseconds
default_interval = 500
fast_interval = 100
last_update_time = pygame.time.get_ticks()

# === FUNCTION DEFINITIONS ===

# --- UI Drawing Functions ---

def draw_text_centered(text, y, font_obj, color=WHITE):
    """
    Draw text centered horizontally at the given y position.
    
    Parameters:
        text (str): The text to display.
        y (int): The vertical position to center the text (y-coordinate).
        font_obj (pygame.font.Font): The font object to use for rendering the text.
        color (tuple): The RGB color of the text (default is WHITE).
    """
    rendered = font_obj.render(text, True, color)
    rect = rendered.get_rect(center=(screen_width // 2, y))
    screen.blit(rendered, rect)

def draw_text(text, x, y, font_obj, color=WHITE):
    """
    Draw text at a specific (x, y) coordinate.
    
    Parameters:
        text (str): The text to display.
        x (int): Horizontal position.
        y (int): Vertical position.
        font_obj (pygame.font.Font): The font object to use for rendering the text.
        color (tuple): The RGB color of the text (default is WHITE)."""
    rendered = font_obj.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_cells():
    """Draw all cells on the grid. Alive cells are drawn with their images; grid lines are white."""
    for row in grid:
        for cell in row:
            if cell.alive and cell.image:
                screen.blit(cell.image, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size))
            pygame.draw.rect(screen, WHITE, (side_margin + cell.col * cell_size, top_margin + cell.row * cell_size, cell_size, cell_size), 1)

def draw_mute_button():
    """Draw the mute/unmute button based on the current mute state."""
    color = (200, 0, 0) if is_muted else (0, 200, 0) # Color changes based on mute state
    pygame.draw.rect(screen, color, mute_button_rect, border_radius=15)
    label = "Unmute" if is_muted else "Mute"
    text = font_2.render(label, True, WHITE)
    screen.blit(text, (mute_button_rect.x + 10, mute_button_rect.y + 10))

def draw_start_page():
    """Draw the start page with animated blobs, a welcome message, and a start button."""
    animate_blobs()
    draw_text_centered ("Welcome to Blob Life!", 120, font)
    draw_text_centered("A fun interactive game where blobs come to life!", 180, font_2)
    draw_button("Start", start_button_rect)

def draw_button(text,rect, color = WHITE):
    """
    Draw a button with the given text and rectangle.
    
    Parameters:
        text (str): The text to display on the button.
        rect (pygame.Rect): The rectangle defining the button's position and size.
        color (tuple): The RGB color of the button background (default is WHITE).
    """
    pygame.draw.rect(screen, color, rect,border_radius=15)
    label = font_2.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_template_button(text, rect, color):
    """
    Draw a template button with the given text, rectangle, and color.
    
    Parameters:
        text (str): The text to display on the button.
        rect (pygame.Rect): The rectangle defining the button's position and size.
        color (tuple): The RGB color of the button background."""
    pygame.draw.rect(screen, color, rect)
    label = font_2.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_back_button():
    """Draw the back button in the top-left corner of the screen."""
    rect = pygame.Rect(20, 20, 100, 30)  # x, y, width, height
    color = (255, 255, 255)  # White background
    pygame.draw.rect(screen, color, rect, border_radius=15)
    label = font_2.render("Back", True, (0, 0, 0))  # Black text
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# === GAME LOGIC ===

def count_neighbors(r, c):
    """
    Count the number of alive neighbors for a cell at (r, c).
    
    Parameters:
        r (int): Row index of the cell.
        c (int): Column index of the cell.
    
    Returns:
        int: Number of alive neighboring cells.
    """
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
    """
    Calcuklates the next generation of cells based on the current grid state.
    Applies Conway's Game of Life rules to determine which cells live, die, or are born.
    Updates the global grid and plays a sound when a new cell is born.
    """
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

def randomize_grid():
    """
    Randomizes the grid by setting each cell to a random alive or dead state.
    Resets the generation count to 0.
    """
    global grid, generation
    for row in grid:
        for cell in row:
            cell.alive = random.choice([True, False])
            cell.image = random.choice(blob_images) if cell.alive else None
    generation = 0

def apply_template(name):
    """
    Applies a predefined template to the grid based on the given name.
    
    Parameters:
        name (str): The name of the template to apply.
    """
    global grid, generation
    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
    if name != "None":
        for r, c in templates[name]:
            grid[r][c].alive = True
            grid[r][c].image = random.choice(blob_images)
    generation = 0

def all_blobs_dead():
    """ 
    Checks if all cells in the grid are dead (not alive).
    Returns:
        bool: True if all cells are dead, False otherwise.
    """
    return all(not cell.alive for row in grid for cell in row)

# === ANIMATION ===

def animate_blobs():
    """
    Animate blobs by moving them horizontalle, keeping them away from the center area (300-800).
    If a blob goes out of bounds or enters the center area, it is repositioned randomly.
    """
    for blob in animated_blobs:
        screen.blit(blob["img"], (blob["x"], blob["y"]))
        blob["x"] += blob["speed"] * blob["dir"]
        if 300 <= blob["x"] <= 800 or blob["x"] < 0 or blob["x"] > screen_width:
            # Keep blobs away from the center area (300–800)
            left_range = range(0, 300)
            right_range = range(801, screen_width)
            selected_range = random.choice([left_range, right_range])
            
            blob["x"] = random.randint(selected_range.start, selected_range.stop - 1)
            blob["y"] = random.randint(0, screen_height)

def animate_storyline_blobs():
    """
    Animate blobs for the storyline screen, moving them horizontally and keeping them away from the center area (250-800).
    If a blob goes out of bounds or enters the center area, it is repositioned randomly."""
    for blob in animated_blobs:
        screen.blit(blob["img"], (blob["x"], blob["y"]))
        blob["x"] += blob["speed"] * blob["dir"]
        if 250 <= blob["x"] <= 800 or blob["x"] < 0 or blob["x"] > screen_width:
            # Keep blobs away from the center area (250–800)
            left_range = range(0, 250)
            right_range = range(801, screen_width)
            selected_range = random.choice([left_range, right_range])
            
            blob["x"] = random.randint(selected_range.start, selected_range.stop - 1)
            blob["y"] = random.randint(0, screen_height)

# === STORYLINE SCREEN ===

def draw_storyline_screen():
    """
    Draws the storyline screen with a background box and storyline text.
    Fills the screen with the current theme color and draws the storyline text inside a box.
    """
    screen.fill(themes[current_theme])

    # --- Settings ---
    box_x = 300  # Distance from left side of screen
    box_y = 100  # Distance from top (Top margin)
    box_width = screen_width - 10 * 60  # Width of the box
    box_height = 450  # Height of the box

    # --- Draw the background box with rounded corners ---
    pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_width, box_height), border_radius=15)

    # --- Draw the storyline text inside the box ---
    y = box_y + 50  # Starting a bit below top of box
    x_offset = 0   
    for i, line in enumerate(story_lines):
        font_used = font if i == 0 else font_2
        rendered = font_used.render(line, True, WHITE)
        rect = rendered.get_rect(center=(screen_width // 2 + x_offset, y))
        screen.blit(rendered, rect)
        y += 40

# === MESSAGE HANDLING ===

def show_message_and_wait(message):
    """
    Displays a message in the center of the screen and waits for a mouse click to continue.
    Also handles quitting the game if the window is closed.
    
    Parameters:
        message (str): The message to display.
    """
    waiting = True
    while waiting:
        screen.fill(themes[current_theme])
        draw_text_centered(message, screen_height // 2 - 30, font_1)
        draw_text_centered("Click anywhere to reset", screen_height // 2 + 30, font_2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


# --- Main Game Loop ---
running = True
while running:
    # Fill the screen with the current theme color
    screen.fill(themes[current_theme])
    
    # Handle all incoming events (like mouse clicks and key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exits the game loop if window is closed

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos() # Gets current mouse click position

            # Checks if the mute button is clicked
            if mute_button_rect.collidepoint(mx, my):
                is_muted = not is_muted # Toggle mute state
                pygame.mixer.music.set_volume ((0 if is_muted else 1))  # Mute or unmute music

            # Back button returns to start menu from certain screens
            elif back_button_rect.collidepoint(mx, my):
                if screen_state in ["tutorial", "storyline", "simulation"]:
                    screen_state = "start_menu"

            # Handles clicks on the start page's start button and sends to theme selection
            elif screen_state == "start_page":
                if start_button_rect.collidepoint(mx,my):
                    screen_state = "theme_select"

            # Handles the theme selection screen
            elif screen_state == "theme_select":
                y_offset = 180
                for i, theme in enumerate(themes):
                    # Checks if the mouse is over a theme button
                    if y_offset + i * 40 <= my <= y_offset + (i+1) * 40:
                        current_theme = theme # Change theme
                        screen_state = "start_menu" # Go to the main menu

            # Main menu buttons
            elif screen_state == "start_menu":
                if tutorial_button_rect.collidepoint(mx, my):
                    screen_state = "tutorial"
                    tutorial_step = 0 # Reset tutorial step
                elif storyline_button_rect.collidepoint(mx, my):
                    screen_state = "storyline"
                elif play_button_rect.collidepoint(mx, my):
                    screen_state = "simulation"
                    # Initialize new grid when entering simulation
                    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                    generation = 0
                    simulation_running = False
                elif theme_button_rect.collidepoint(mx, my):
                    screen_state = "theme_select"

            # Tutorial steps advance on click
            elif screen_state == "tutorial":
                if tutorial_step < len(tutorial_messages) - 1:
                    tutorial_step += 1
                else:
                    screen_state = "simulation"
                    # Initialize new grid when entering simulation
                    grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                    generation = 0
                    simulation_running = False

            # Simulation blob toggling on click
            elif screen_state == "simulation":
                mx, my = event.pos
                col = (mx - side_margin) // cell_size
                row = (my - top_margin) // cell_size
                if 0 <= row < grid_height and 0 <= col < grid_width:
                    grid[row][col].toggle(blob_images)

        elif event.type == pygame.KEYDOWN:
            if screen_state == "simulation":
                # Spacebar toggles simulation play/pause
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                    just_paused = not simulation_running  # Tracks if just paused
                
                if not simulation_running:
                    # R randomizes the grid cells
                    if event.key == pygame.K_r:
                        randomize_grid()
                    # Left arrow resets the grid to all dead blobs
                    elif event.key == pygame.K_LEFT:
                        grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                        generation = 0
                        simulation_running = False
                    # Right arrow advances to the next generation
                    elif event.key == pygame.K_RIGHT:
                        if not simulation_running:
                            next_generation()
                    # Applies predefined templates based on key presses
                    elif event.key == pygame.K_1:
                        apply_template("Heart")
                    elif event.key == pygame.K_2:
                        apply_template("Smiley")
                    elif event.key == pygame.K_3:
                        apply_template("Letter A")

    # --- Drawing UI and game elements based on current state ---
    
    # Start page
    if screen_state == "start_page":
        draw_start_page()
        animate_blobs()
        draw_mute_button()

    # Theme selection screen
    elif screen_state == "theme_select":
        animate_blobs()
        draw_text_centered("Choose Your Theme!", 100, font)
        for i, theme in enumerate(themes):
            # Draws button with contrasting text color if theme is black
            if themes[theme] == BLACK:
                draw_template_button(theme, pygame.Rect(400, 180 + i * 40, 300, 40), (255,255,255))
            else:
                draw_template_button(theme, pygame.Rect(400, 180 + i * 40, 300, 40), themes[theme])
        draw_mute_button()

    # Main menu
    elif screen_state == "start_menu":
        animate_blobs()
        draw_text_centered("Welcome to Blob Life!", 100, font)
        draw_text_centered("Game of Life with a Blob Twist!", 160, font_1)
        # Defines button rectangles for each menu option
        tutorial_button_rect = pygame.Rect(400, 200, 300, 40)
        storyline_button_rect = pygame.Rect(400, 270, 300, 40)
        play_button_rect = pygame.Rect(400, 340, 300, 40)
        theme_button_rect = pygame.Rect(400, 410, 300, 40)
        # Draws buttons for each option
        draw_button("Tutorial", tutorial_button_rect)
        draw_button("Storyline", storyline_button_rect)
        draw_button("Play", play_button_rect)
        draw_button("Theme Select", theme_button_rect)
        draw_mute_button()

    # Tutorial screen
    elif screen_state == "tutorial":
        draw_text_centered("Blobbo Tutorial", 100, font)
        draw_text_centered(tutorial_messages[tutorial_step], 200, font_2)
        screen.blit(blobbo_img, (screen_width // 2 - 40, 300))
        draw_text_centered("Click to continue tutorial", 450, font_2)
        draw_back_button()
        draw_mute_button()
    
    # Storyline screen
    elif screen_state == "storyline":
        draw_storyline_screen()
        animate_storyline_blobs()
        draw_back_button()
        draw_mute_button()

    # Simulation screen
    elif screen_state == "simulation":
        # Display generation number and progress bar
        draw_text_centered(f"Generation: {generation}", 40, font_1)
        
        # Draw progress bar
        bar_x = side_margin
        bar_y = 70
        bar_width = screen_width - 2 * side_margin
        bar_height = 10
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))

        # Compute progress: 1–20 fills the bar fully
        # So gen 1 = 1/20 filled, gen 2 = 2/20 filled, ..., gen 20 = full bar
        progress_position = generation % 20
        if progress_position == 0 and generation != 0:
            progress_position = 20  # Full bar at generation 20, 40, etc.

        filled_width = int((progress_position / 20) * bar_width)
        pygame.draw.rect(screen, (255, 105, 180), (bar_x, bar_y, filled_width, bar_height))

        # Draw all cells (blobs) on the grid
        draw_cells()
        draw_back_button()
        draw_mute_button()
        
        # Display control instructions on the right side of the screen
        draw_text("Controls:", screen_width - 280, 120, font_2)
        draw_text("Space: Pause/Resume", screen_width - 280, 150, font_2)
        draw_text("R: Randomize", screen_width - 280, 170, font_2)
        draw_text("Left Arrow: Reset Grid", screen_width - 280, 190, font_2)
        draw_text("1: Heart Template", screen_width - 280, 210, font_2)
        draw_text("2: Smiley Template", screen_width - 280, 230, font_2)
        draw_text("3: Letter A Template", screen_width - 280, 250, font_2)
        draw_text("Click to toggle blobs", screen_width - 280, 270, font_2)
        draw_text("Right Arrow: Next Generation", screen_width - 280, 290, font_2)
        draw_text("S: Speed Up Generations", screen_width - 280, 310, font_2)
        draw_text("Mute/Unmute Music", screen_width - 280, 330, font_2)
        draw_text("Click to place blobs", screen_width - 280, 360, font_2)
        
        # Display the rules for Blob Life on the left side of the screen
        draw_text("Blob Life Rules:", 10, 120, font)
        draw_text("Lonely blob? It poofs!", 10, 180, font_2)
        draw_text("(0-1 friends)", 10, 200, font_2)
        draw_text("Happy blob? It stays!", 10, 225, font_2)
        draw_text("(2-3 friends)", 10, 245, font_2)
        draw_text("Crowded blob? It poofs!", 10, 270, font_2)
        draw_text("(4+ friends)", 10, 290, font_2)
        draw_text("New blob? 3 nearby friends!", 10, 315, font_2)

        # Check if 'S' key pressed to speed up generations
        keys = pygame.key.get_pressed()
        generation_interval = fast_interval if keys[pygame.K_s] else default_interval

        # Update generations if running and interval time has passed
        current_time = pygame.time.get_ticks()
        if simulation_running and (current_time - last_update_time >= generation_interval):
            next_generation()

            # Stop simulation if all blobs are dead
            if all_blobs_dead():
                simulation_running = False
                show_message_and_wait("Oh no! All the blobs have vanished!")
                # Reset grid and generation
                grid = [[Cell(r, c) for c in range(grid_width)] for r in range(grid_height)]
                generation = 0

            last_update_time = current_time

    # Refresh the display to show the updated screen with everything drawn
    pygame.display.flip()
    clock.tick(60) # Limit to 60 frames per second

pygame.quit() # Cleanly exits pygame
