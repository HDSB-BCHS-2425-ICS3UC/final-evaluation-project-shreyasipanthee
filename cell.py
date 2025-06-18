# --- Imports ---
import pygame
import random

class Cell:
    """
    Represents a single in the grid for Blob Life Game.
    Each cell can be alive or dead, and it can toggle its state.
    """

    def __init__(self, row, col):
        """
        Initialize a cell at a specific row and column.
        Parameters:
            row (int): The row index of the cell in the grid.
            col (int): The column index of the cell in the grid.
        """
        self.row = row
        self.col = col
        self.alive = False
        self.image = None  # Blob image shown when alive

    def toggle(self, blob_images):
        """
        Toggle the cell's alive state. Assigns a blob image if turned alive.
        
        Parameters:
            blob_images (list): List of images to choose from when the cell is alive.
        """
        self.alive = not self.alive
        if self.alive:
            self.image = random.choice(blob_images)
        else:
            self.image = None

    def update_state(self, neighbors, blob_images, current_image):
        """
        Updates the cell's state based on the number of alive neighbor using Conway's Game of Life rules.
        
        Parameters:
            neighbors (int): The number of alive neighbors surrounding this cell.
            blob_images (list): List of images to choose from when the cell becomes alive.
            current_image: The current image of the cell if it is alive.
        """
        if self.alive:
            # Stays alive with 2 or 3 neighbors, dies otherwise
            if neighbors in [2, 3]:
                self.alive = True
                self.image = current_image  # Keep the same blob
            else:
                self.alive = False
                self.image = None
        else:
            # Becomes alive with exactly 3 neighbors
            if neighbors == 3:
                self.alive = True
                self.image = random.choice(blob_images)
            else:
                self.alive = False
                self.image = None

