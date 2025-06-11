import pygame
import random

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.alive = False
        self.image = None  # Holds a consistent image while alive

    def toggle(self, blob_images):
        self.alive = not self.alive
        if self.alive:
            self.image = random.choice(blob_images)
        else:
            self.image = None

    def update_state(self, neighbors, blob_images, current_image):
        """
        Update the cell's state based on neighbor count.
        Keeps current_image if remaining alive.
        Assigns new image if reborn.
        """
        if self.alive:
            if neighbors in [2, 3]:
                self.alive = True
                self.image = current_image  # Keep the same blob
            else:
                self.alive = False
                self.image = None
        else:
            if neighbors == 3:
                self.alive = True
                self.image = random.choice(blob_images)
            else:
                self.alive = False
                self.image = None

    def draw(self, surface, cell_size, top_margin, side_margin, alive_colour, dead_colour, border_colour):
        x = side_margin + self.col * cell_size
        y = top_margin + self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        fill_colour = alive_colour if self.alive else dead_colour
        pygame.draw.rect(surface, fill_colour, rect)
        pygame.draw.rect(surface, border_colour, rect, 1)  # Border
