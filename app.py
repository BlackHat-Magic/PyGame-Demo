import pygame, sys

sys.path.insert(1, "./generator")
from wfc_utils import Biome, Tile, World
from dungeon_layout_generator import rooms
from dungeon_room_generator import Floor
from menus import render_main_menu, render_pause_menu

sys.path.insert(1, "./controller")
from camera import Camera
from character import Character

sys.path.insert(1, "./")
from menus import render_main_menu
from dungeon_crawler import render_dungeon

# Initialize pygame, window
pygame.init()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Pygame Demo")
width, height = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()

# define visuals
background = pygame.Surface((width, height))
background.fill("Black")
font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 16)
floor_char = font.render(".", False, "Gray")
wall_char = font.render("#", False, "Gray")

# generate dungeon
def create_dungeon(sizes):
    worlds = [World(f"floor_{i}", rooms, size) for i, size in enumerate(sizes)]
    for world in worlds:
        world.generate()
    floors = [Floor(world) for world in worlds]
    return(floors)
dungeon = create_dungeon([
    (5, 5),     # floor 1
    (9, 9),     # floor secret 1
    (7, 7),     # floor 2
    (12, 12),   # floor secret 2
    (9, 9),     # floor 3
    (15, 15),   # floor secret 3
    (12, 12),   # floor 4
    (17, 17),   # floor 5
    (20, 20)
])
floor = dungeon[0]

# character and enemy
character = Character(
    surface=font.render("@", False, "White"), 
    name="It's You!", 
    screen=screen, 
    font=font
)

# initialize camera
camera = Camera()

# move character to starter room
character.pos_x, character.pos_y = floor.start_coordinates
character.pos_x *= 16
character.pos_y *= 16
character.target_pos = (character.pos_x, character.pos_y)
camera.x = character.pos_x - width // 2
camera.y = character.pos_y - height // 2

paused = False
main_menu = False

# game loop
while True:
    dt = clock.tick(120)
    
    # check for events
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
            continue
        if(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            paused = not paused
    
    # get mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()

    # point-and-click movement
    if(mouse[0] and not paused):
        target_x, target_y = camera.get_mouse_world_position()
        target_x = (target_x + 8) // 16 * 16
        target_y = (target_y + 8) // 16 * 16
        character.target_pos = (target_x, target_y)
    

    # get keys
    keys = pygame.key.get_pressed()

    if(not paused):
        # player controlled stuff
        character.move_to_target()
        camera.move()

        # enemy stuff
    
    # render background
    screen.blit(background, (0, 0))
    
    # render the map
    render_dungeon(floor, camera, screen, wall_char, floor_char)

    # render character
    camera.render(screen, character.surface, (character.pos_x, character.pos_y))
    character.render_billboard(camera)

    # render pause menu
    if(paused):
        render_pause_menu(screen, font)
    
    # render main menu
    if(main_menu):
        render_main_menu(screen, font)

    # render to window & handle clock stuff
    pygame.display.update()