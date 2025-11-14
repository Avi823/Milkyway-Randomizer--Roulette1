import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IsoPush")
clock = pygame.time.Clock()
FPS = 60

TILE_WIDTH, TILE_HEIGHT = 64, 32
GRID_ROWS, GRID_COLS = 10, 10

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

player_x, player_y = 5, 5
player_color = blue
player_size = 20

box_start_x, box_start_y = 7, 5
box_x, box_y = box_start_x, box_start_y

goal_x, goal_y = 2, 2
level_complete = False

move_delay = 200
last_move_time = 0

def grid_to_iso(x, y):
    iso_x = (x - y) * (TILE_WIDTH // 2) + WIDTH // 2
    iso_y = (x + y) * (TILE_HEIGHT // 2) + HEIGHT // 2 - 144
    return iso_x, iso_y

def draw_tile(x, y):
    iso_x, iso_y = grid_to_iso(x, y)
    pygame.draw.polygon(screen, white, [
        (iso_x, iso_y),
        (iso_x + TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2),
        (iso_x, iso_y + TILE_HEIGHT),
        (iso_x - TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2)
    ], 1)

def draw_goal(x, y):
    iso_x, iso_y = grid_to_iso(x, y)
    pygame.draw.polygon(screen, (0, 255, 0), [
        (iso_x, iso_y),
        (iso_x + TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2),
        (iso_x, iso_y + TILE_HEIGHT),
        (iso_x - TILE_WIDTH // 2, iso_y + TILE_HEIGHT // 2)
    ])

def draw_cube(x, y, size=TILE_WIDTH, height=TILE_HEIGHT, color=red):
    iso_x, iso_y = grid_to_iso(x, y)
    # Draw a simple diamond shape on the tile to represent the cube
    points = [
        (iso_x, iso_y - 15),
        (iso_x + 25, iso_y),
        (iso_x, iso_y + 15),
        (iso_x - 25, iso_y)
    ]
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, white, points, 2)

def draw_player(x, y):
    iso_x, iso_y = grid_to_iso(x, y)
    pygame.draw.circle(screen, player_color, (iso_x, iso_y), player_size)
def is_inside_grid(x, y):
    return 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS
running = True
while running:
    dt = clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if current_time - last_move_time > move_delay:
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        if dx != 0 or dy != 0:
            new_px = player_x + dx
            new_py = player_y + dy

        
            if 0 <= new_px < GRID_COLS and 0 <= new_py < GRID_ROWS:
                if (new_px, new_py) == (box_x, box_y):
                    new_bx = box_x + dx
                    new_by = box_y + dy
                    if 0 <= new_bx < GRID_COLS and 0 <= new_by < GRID_ROWS:
                        box_x, box_y = new_bx, new_by
                        if (box_x, box_y) == (goal_x, goal_y):
                            level_complete = True
                        player_x, player_y = new_px, new_py
                    else:
                        box_x, box_y = box_start_x, box_start_y
                    last_move_time = current_time
                else:
                    player_x, player_y = new_px, new_py
                    last_move_time = current_time


    screen.fill(black)


    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            draw_tile(col, row)

    draw_goal(goal_x, goal_y)
    draw_objects = [("cube", box_x, box_y), ("player", player_x, player_y)]
    draw_objects.sort(key=lambda item: item[1] + item[2])

    for item in draw_objects:
        kind, x, y = item
        if kind == "cube":
            draw_cube(x, y)
        elif kind == "player":
            draw_player(x, y)

    pygame.display.flip()
    if level_complete:
        font = pygame.font.SysFont(None, 72)
        text = font.render("Level Complete!", True, (255, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))
        pygame.time.delay(2000)
        running = False
pygame.quit()

sys.exit()
