```
START

## Introduction
PRINT "Welcome to Conway's Game of Life"
PRINT "A simulation of cellular life and death based on mathematical rules."

## Setup Grid
CREATE 10x10 grid → STORE as grid
For each cell in grid 
    INITIALIZE state as DEAD
    STORE coordinates and size
    DRAW cell on screen using pygame functions

## Define Cell Class
DEFINE class Cell:
    INIT with x, y, size, and alive state
    METHOD draw() → Draw cell (alive = filled, dead = empty)
    METHOD toggle() → Switch alive/dead state

#Main Game Loop
SET simulation_running = FALSE
WHILE game is running 
    LISTEN for pygame events:
        If event is QUIT
            END program
        IF event is MOUSE CLICK
            GET cell at clicked position → CALL toggle() function
        IF event KEY PRESS:
            IF key is SPACE
                TOGGLE simulation_running
            IF key is C
                SET all cells to DEAD
            IF key is R
                RANDOMIZE cell states
            IF key is ESC
                END program

    IF simulation_running is TRUE
        CALL update_grid(grid) → APPLY Game of Life Rules

    CALL draw_grid(grid) → DISPLAY updated grid 
    UPDATE display 
    DELAY to control simulation speed

### Define update_grid(grid)
COPY current grid to a temporary grid temp_grid
FOR each cell in grid:
    CALL count_alive_neighbours(cell)
    APPLY rules:
        IF cell is ALIVE and (neighbors < 2 or neighbors > 3):
            SET cell to DEAD
        IF cell is ALIVE and (neighbors == 2 or 3):
            KEEP cell ALIVE
        IF cell is DEAD and (neighbors == 3):
            SET cell to ALIVE
RETURN updated grid

### Define count_alive_neighbours(cell)
SET alive_count = 0
FOR each of the 8 surrounding positions:
    IF neighbour is within bounds and is ALIVE
        INCREMENT count
RETURN count

### Define draw_grid(grid)
FOR each cell in grid:
    CALL cell.draw(screen)

END
```