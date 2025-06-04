START

# Introduction
PRINT "Welcome to Conway's Game of Life"
PRINT "A simulation of cellular life and death based on mathematical rules."

# Setup Grid
CREATE 10x10 grid → STORE as grid
For each cell in grid 
    INITIALIZE state as DEAD
    STORE coordinates and size