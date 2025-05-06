import pygame
import math
import random

pygame.init()
pygame.display.set_caption("2048")
HEIGHT = 600
WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
FONT = pygame.font.SysFont('comicsans', 50, bold = True)
BG_COLOUR = (187, 173, 160)
GRID_COLOUR = (163, 148, 137)
FONT_COLOUR = (121,108,100)

class Tile:
    COLOURS = [
        (238, 228, 218), # 0 -> 2
        (237, 224, 200), # 1 -> 4
        (242, 177, 121), # 2 -> 8
        (245, 149, 99),  # 3 -> 16
        (246, 124, 95),  # 4 -> 32
        (246, 94, 59),   # 5 -> 64
        (237, 207, 114), # 6 -> 128
        (237, 204, 97),  # 7 -> 256
        (237, 200, 80),  # 8 -> 512
        (237, 197, 63),  # 9 -> 1024
        (237, 194, 46)   # 10 -> 2048
    ]
    # Notice the pattern here:
    # i -> v gives the formula i = log2(v) - 1

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * WIDTH / 4
        self.y = row * HEIGHT / 4
    
    def find_colour(self):
        colour_i = int(math.log2(self.value)) - 1
        colour = self.COLOURS[colour_i]
        return colour
    
    def draw(self, window):
        colour = self.find_colour()
        pygame.draw.rect(window, colour, (self.x, self.y, WIDTH/4, HEIGHT/4))
        text = FONT.render(str(self.value), 1, FONT_COLOUR)
        # To find the coordinates of the text, find the size of the text.
        # Then go to the middle of the tile and subtract half the text size.
        text_width, text_height = text.get_width(), text.get_height()
        mid_tile_x = self.x + WIDTH/8    # Middle of given tile in x
        mid_tile_y = self.y + HEIGHT/8   # Middle of given tile in y
        text_coords = ((mid_tile_x - text_width/2), (mid_tile_y - text_height/2))
        window.blit(text, text_coords)

    def set_pos(self):
        x = self.x
        y = self.x
        return x,y

def get_random_pos(tiles):
    while True:
        row = random.randrange(0, 4)
        col = random.randrange(0, 4)
        if f"{row}{col}" not in tiles:
            break
    return row, col

def create_tiles():
    tiles = {}
    for _ in range(1):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def draw(window, tiles):
    window.fill(BG_COLOUR) # Background color

    for tile in tiles.values():
        tile.draw(window)
    draw_grid(window)
    pygame.display.update()

def draw_grid(window):
    for line_num in range(1, 4):
        # Horizontal Grid Lines
        y = HEIGHT / 4 * line_num
        pygame.draw.line(window, GRID_COLOUR, (0, y), (WIDTH, y), 10)

        # Vertical Grid Lines
        x = WIDTH / 4 * line_num
        pygame.draw.line(window, GRID_COLOUR, (x, 0), (x, HEIGHT), 10)
    
    # Outer Border
    pygame.draw.rect(window, GRID_COLOUR, (0, 0, HEIGHT, WIDTH), 10)

def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = create_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, tiles)
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)