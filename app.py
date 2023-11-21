import pygame, sys

sys.path.insert(1, "./generator")
from wfc_utils import Biome, Tile, World
from dungeon_layout_generator import rooms
from dungeon_room_generator import Floor

sys.path.insert(1, "./controller")
from camera import Camera
from character import Character

# Initialize pygame, window
pygame.init()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Pygame Demo")
width, height = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()

# define visuals
font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 16)
floor_char = font.render(".", False, "Gray")
wall_char = font.render("#", False, "Gray")
floor_char_b = font.render(".", False, "White")
wall_char_b = font.render("#", False, "White")
background = pygame.Surface((width, height))
background.fill("Black")

# generate dungeon
world_floors = []
for i in range(10):
    world_floors.append(World(f"floor_{i}", rooms, (5, 5)))
for floor in world_floors:
    floor.generate()
dungeon = []
for i, floor in enumerate(world_floors):
    dungeon.append(Floor(floor))
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

# print(character.target_pos)

camera.x = character.pos_x - width // 2
camera.y = character.pos_y - height // 2

# game loop
while True:
    dt = clock.tick(120)
    # check for events
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
    
    # get mouse
    mouse_pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()

    if(mouse[0]):
        target_x, target_y = camera.get_mouse_world_position()
        target_x = (target_x + 8) // 16 * 16
        target_y = (target_y + 8) // 16 * 16
        character.target_pos = (target_x, target_y)
    character.move_to_target()

    camera.move()
    
    # render background
    screen.blit(background, (0, 0))
    
    # render the map
    # for big_x in range(floor.grid.shape[0]):
    #     for big_y in range(floor.grid.shape[1]):
    #         room = floor.grid[big_x, big_y]
    #         for small_x in range(room.grid.shape[0]):
    #             for small_y in range(room.grid.shape[1]):
    #                 coordinates = (big_x * 15 * 16 + small_x * 16, big_y * 15 * 16 + small_y * 16)
    #                 tile = room.grid[small_x, small_y]
    #                 if(tile == "w"):
    #                     camera.render(screen, wall_char, coordinates)
    #                     continue
    #                 if(tile == "f"):
    #                     camera.render(screen, floor_char, coordinates)
    for x in range(floor.grid.shape[0]):
        for y in range(floor.grid.shape[1]):
            tile = floor.grid[x, y]
            coordinates = (x * 16, y * 16)
            if(tile == "w"):
                camera.render(screen, wall_char, coordinates)
                continue
            if(tile == "f"):
                camera.render(screen, floor_char, coordinates)

    # render character
    camera.render(screen, character.surface, (character.pos_x, character.pos_y))
    character.render_billboard(camera)

    # render to window & handle clock stuff
    pygame.display.update()