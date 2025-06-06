import pygame



class Cell:
    def __init__(self, row,col):
        self.row = row
        self.col = col
        self.alive = False

    def toggle(self):
        self.alive = not self.alive

    
    def draw(self, surface, cell_size, top_margin, side_margin, alive_colour, dead_colour, border_colour):
        x= side_margin + self.col * cell_size
        y= top_margin + self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        fill_colour = alive_colour if self.alive else dead_colour
        pygame.draw.rect(surface, fill_colour, rect)
        pygame.draw.rect(surface, border_colour, rect, 1) # Border
