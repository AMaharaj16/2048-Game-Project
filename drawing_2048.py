import pygame

pygame.init()
pygame.display.set_caption("2048")
HEIGHT = 600
WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
FONT = pygame.font.SysFont('comicsans', 80, bold = True)
BG_COLOUR = (187, 173, 160)
GRID_COLOUR = (163, 148, 137)


def draw(window):
    window.fill(BG_COLOUR) # Background color
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

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window)
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)