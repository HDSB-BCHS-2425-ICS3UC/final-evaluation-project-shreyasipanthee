```
START

# Introduction
PRINT "Welcome to Blob Life"
PRINT "A fun, colorful version of Conway's Game of Life!"

# Initialize
IMPORT pygame and other modules
SETUP screen, clock, constants (width, height, grid size, etc.)
LOAD fonts, images, sounds

# Define Cell class
CLASS Cell:
    INIT(row, col, size)
        SET alive = False
    METHOD toggle()
        SWITCH alive/dead state
    METHOD draw(screen)
        DRAW filled blob if alive, outline if dead

# Create Grid
MAKE 2D list of Cell objects

# Game State
SET screen_state = "start_page"
SET simulation_running = False
SET generation = 0

# Main Loop
WHILE game is running:
    HANDLE events:
        IF quit event:
            EXIT
        IF mouse click:
            IF on start button:
                screen_state = "start_menu"
            IF in grid and simulation not running:
                TOGGLE cell at click
        IF key press:
            IF SPACE:
                TOGGLE simulation_running
            IF R and not running:
                RANDOMIZE grid
            IF LEFT ARROW and not running:
                CLEAR grid
            IF RIGHT ARROW and not running:
                STEP one generation

    IF simulation_running:
        UPDATE grid using next_generation()

    DRAW screen based on screen_state:
        IF start_page:
            SHOW animated blobs and title
        IF start_menu:
            SHOW buttons for Play and Tutorial
        IF tutorial:
            DISPLAY next tutorial message each click
        IF simulation:
            DRAW grid and instructions

    UPDATE screen
    DELAY for frame rate

# next_generation()
COPY grid to temp_grid
FOR each cell in grid:
    COUNT alive neighbours
    APPLY rules:
        - Alive + <2 or >3 neighbours → die
        - Alive + 2 or 3 neighbours → live
        - Dead + exactly 3 neighbours → become alive
RETURN updated grid

# count_alive_neighbours(cell)
CHECK 8 surrounding cells
COUNT how many are alive
RETURN count

END
```
