import pygame
import math
import random

pygame.init()
pygame.display.set_caption("2048")
HEIGHT = 800    # Originally, height and width were set to 600 but I realized
WIDTH = 800     # the velocity was skipping over some cols and rows when playing
HEIGHT_RECT = HEIGHT // 4
WIDTH_RECT = WIDTH // 4
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
FONT = pygame.font.SysFont('comicsans', 50, bold = True)
BG_COLOUR = (187, 173, 160)
GRID_COLOUR = (163, 148, 137)
FONT_COLOUR = (121,108,100)
VEL = 20

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
        self.x = col * WIDTH_RECT
        self.y = row * HEIGHT_RECT
    
    def find_colour(self):
        colour_i = int(math.log2(self.value)) - 1
        colour = self.COLOURS[colour_i]
        return colour
    
    def draw(self, window):
        colour = self.find_colour()
        pygame.draw.rect(window, colour, (self.x, self.y,WIDTH_RECT, HEIGHT_RECT))
        text = FONT.render(str(self.value), 1, FONT_COLOUR)
        # To find the coordinates of the text, find the size of the text.
        # Then go to the middle of the tile and subtract half the text size.
        text_width, text_height = text.get_width(), text.get_height()
        mid_tile_x = self.x + WIDTH_RECT / 2    # Middle of given tile in x
        mid_tile_y = self.y + HEIGHT_RECT / 2   # Middle of given tile in y
        text_coords = ((mid_tile_x - text_width/2), (mid_tile_y - text_height/2))
        window.blit(text, text_coords)

    def set_pos(self, ceil=False):
        if ceil:
            self.col, self.row = math.ceil(self.x / (WIDTH_RECT)), math.ceil(self.y / (HEIGHT_RECT))
        else:
            self.col, self.row = math.floor(self.x / (WIDTH_RECT)), math.floor(self.y / (HEIGHT_RECT))
    
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def get_random_pos(tiles):
    while True:
        row = random.randrange(0, 4)
        col = random.randrange(0, 4)
        if f"{row}{col}" not in tiles:
            break
    return row, col

def move_tiles(window, tiles, clock, direction):
    changed = True
    merged = set()     # We don't want multiple tiles merging in one move, prevented by adding merged tiles to the set.

    if direction == "left":
        sort_func = lambda x: x.col                                                   # Order tiles by column
        reverse = False
        delta = (-VEL, 0)                                                             # Change of tile x and y per clock tick
        boundary_check = lambda tile: tile.col == 0                                   # Check if the tile is at the edge 
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")           # Produce next tile
        check_merge = lambda tile, next_tile: tile.x > next_tile.x + VEL              # Check if tile merges with next_tile in the next clock tick
        check_move = lambda tile, next_tile: tile.x > next_tile.x + VEL + WIDTH_RECT  # Check if the tile moves into the square beside next_tile
        ceil = True                                                                   # Should coord value be rounded up or down when finding col or row
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (VEL, 0)
        boundary_check = lambda tile: tile.col == 3
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        check_merge = lambda tile, next_tile: tile.x < next_tile.x - VEL
        check_move = lambda tile, next_tile: tile.x < next_tile.x - VEL - WIDTH_RECT
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        check_merge = lambda tile, next_tile: tile.y > next_tile.y + VEL
        check_move = lambda tile, next_tile: tile.y > next_tile.y + VEL + HEIGHT_RECT
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, VEL)
        boundary_check = lambda tile: tile.row == 3
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        check_merge = lambda tile, next_tile: tile.y < next_tile.y - VEL
        check_move = lambda tile, next_tile: tile.y < next_tile.y - VEL - HEIGHT_RECT
        ceil = False

    while changed:                         # If a change occured in the previous iteration, we will keep trying until no changes occur.
        clock.tick(FPS)
        changed = False
        tiles_sorted = sorted(tiles.values(), key = sort_func, reverse = reverse)

        for i, tile in enumerate(tiles_sorted):
            if boundary_check(tile):
                continue                           # If the tile is at the boundary, skip it.

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)                   # If there isn't a next_tile, move the tile.
            
            elif (tile.value == next_tile.value    # If the next_tile == tile and neither is in merged
                  and tile not in merged           # then we want to add them up.
                  and next_tile not in merged):
                if check_merge(tile, next_tile):   # We need the tiles to merge into one another before changing tile values.
                    tile.move(delta)
                else:
                    next_tile.value *= 2           # Once the tile is on next_tile, double next_tile and add it to the merged set.
                    tiles_sorted.pop(i)
                    merged.add(next_tile)
            elif check_move(tile, next_tile):
                tile.move(delta)
            else: 
                continue                           # If nothing changes, keep changed as False to break to loop

            tile.set_pos(ceil)
            changed = True
        update_tiles(window, tiles, tiles_sorted)  # Need to reassign tiles within the dictionary
    return end_move(tiles)

def update_tiles(window, tiles, tiles_sorted):
    tiles.clear()
    for tile in tiles_sorted:
        tiles[f"{tile.row}{tile.col}"] = tile 
    draw(window, tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "GAME OVER"
    row,col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2,4]), row, col)
    return "GAME ONGOING"

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
        y = HEIGHT_RECT * line_num
        pygame.draw.line(window, GRID_COLOUR, (0, y), (WIDTH, y), 10)

        # Vertical Grid Lines
        x = WIDTH_RECT * line_num
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)