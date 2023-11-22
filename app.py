import pygame, sys, copy

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
    floors = []
    for i, size in enumerate(sizes):
        world = World(f"floor_{i}", copy.deepcopy(rooms), size)
        world.generate()
        floor = Floor(world)
        floors.append(floor)
    return(floors)
dungeon = create_dungeon([
    (5, 5),     # floor 1
    (7, 7),     # floor secret 1
    (6, 6),     # floor 2
    (8, 8),     # floor secret 2
    (7, 7),     # floor 3
    (9, 9),     # floor secret 3
    (8, 8),     # floor 4
    (10, 10),   # floor secret 4
    (9, 9)      # floor 5
])
floor = dungeon[0]
centers, tree = floor.generate_hallways()

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
        if(event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            floor = create_dungeon([(15, 15)])[0]
            centers, tree = floor.generate_hallways()
            character.pos_x, character.pos_y = floor.start_coordinates
            character.pos_x *= 16
            character.pos_y *= 16
            character.target_pos = (character.pos_x, character.pos_y)
            camera.x = character.pos_x - width // 2
            camera.y = character.pos_y - height // 2
    
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
        character.move_to_target(dt)
        camera.move(dt)

        # enemy stuff
    
    # render background
    screen.blit(background, (0, 0))
    
    # render the map
    render_dungeon(floor, camera, screen, wall_char, floor_char)

    # debug: render the connections
    for edge in tree.edges:
        x1, y1 = centers[edge[0]]
        x1 *= 16
        y1 *= 16
        room1_center = (int(x1 - camera.x), int(y1 - camera.y))

        x2, y2 = centers[edge[1]]
        x2 *= 16
        y2 *= 16
        room2_center = (int(x2 - camera.x), int(y2 - camera.y))

        pygame.draw.line(screen, (0, 0, 255), room1_center, room2_center)

    # render character
    camera.render(screen, character.surface, (character.pos_x, character.pos_y))
    character.render_billboard(camera)

    # render pause menu
    if(paused):
        render_pause_menu(screen, font)
    
    # render main menu
    if(main_menu):
        render_main_menu(screen, font)
    
    # render fps counter
    fps = 1 // (dt / 1000)
    # fps_surface = font.render(f"{fps} FPS", False, "Gray")
    # screen.blit(fps_surface, (0, 0))

    # render to window & handle clock stuff
    pygame.display.update()