import pygame
import screen
import math

CELL_WIDTH =  40 #?
CELL_HEIGHT = 20 #?

ONE_BYTE_RED = pygame.image.load('cell1byte_red.png').convert_alpha()
ONE_BYTE_BLUE = pygame.image.load('cell1byte_blue.png').convert_alpha()
FOUR_BYTES = pygame.image.load('cell4bytes.png').convert_alpha()
FOUR_BYTES_RED = pygame.image.load('cell4bytes_red.png').convert_alpha()
FOUR_BYTES_BLUE = pygame.image.load('cell4bytes_blue.png').convert_alpha()
class Cell:
    def __init__(self, x = 0, y = 0, l = 1, p = 0, value = None):
        self.posx = x
        self.posy = y
        self.length = l
        self.width = CELL_WIDTH
        self.height = CELL_HEIGHT
        self.value = value
        self.static = False
        if l == 1:
            if p == 1:
                self.img = ONE_BYTE_BLUE
            else:
                self.img = ONE_BYTE_RED
        elif l == 4:
            if p == 1:
                self.img = FOUR_BYTES_BLUE
            else:
                self.img = FOUR_BYTES_RED
            self.width = 4*CELL_WIDTH + 3 * screen.DISTNACE_BETWEEN_CARDS #?
            # width of 4 cells plus the spaces inbetween them

    def get_color(self):
        return 1 if self.img == ONE_BYTE_BLUE or self.img == FOUR_BYTES_BLUE else 2

    def color(self, n):
        if n == 1:
            self.img = ONE_BYTE_BLUE if self.length == 1 else FOUR_BYTES_BLUE
        elif n == 2:
            self.img = ONE_BYTE_RED if self.length == 1 else FOUR_BYTES_RED

    def __len__(self):
        return self.length

    def binary_value(self):
        return bin(self.value)

    def render(self, window):
        window.blit(self.img, (self.posx, self.posy))
        if self.value is not None:
            text = screen.FONT.render(str(self.value), 1, (255,255,255))
            window.blit(text, (self.posx + self.width - 8*len(str(self.value)), self.posy + 8))

    def __str__(self):
        return str((self.posx, self.posy)) + '\tlength: ' + str(self.length) + '\tvalue: ' + str(self.value)