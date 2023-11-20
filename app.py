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
clock = pygame.time.Clock()

# define font
font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 16)

# background
background = pygame.Surface((1280, 960))
background.fill("Black")

# character class

# character and enemy
character = Character(surface=font.render("@", False, "White"), name="It's You!", font=font, screen=screen)
enemy = Character(surface=font.render("X", False, "Red"), name="Enemy Dude", pos_x=320, pos_y=240, font=font, screen=screen)

# initialize camera
camera = Camera()

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

floor_char = font.render(".", False, "Gray")
wall_char = font.render("#", False, "Gray")

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
        target_x, target_y = mouse_pos
        target_x = target_x // 16 * 16 + 8 - camera.x
        target_y = target_y // 16 * 16 + 8 - camera.y
        character.target_pos = (target_x, target_y)
    character.moveToTarget()

    camera.move()
    
    # render background
    screen.blit(background, (0, 0))
    
    # render the map
    for x in range(floor.grid.shape[0]):
        for y in range(floor.grid.shape[1]):
            room = floor.grid[x, y]
            big_x = x * 15
            big_y = y * 15
            for small_x in range(room.grid.shape[0]):
                for small_y in range(room.grid.shape[1]):
                    tile = room.grid[small_x, small_y]
                    coordinates = ((big_x + small_x) * 16, (big_y + small_y) * 16)
                    if(tile == "w"):
                        camera.render(screen, wall_char, coordinates)
                        continue
                    if(tile == "f"):
                        camera.render(screen, floor_char, coordinates)

    # render character
    camera.render(screen, character.surface, (character.pos_x, character.pos_y))
    # camera.render(screen, character.)
    character.renderBillboard(camera)
    camera.render(screen, enemy.surface, (enemy.pos_x, enemy.pos_y))
    enemy.renderBillboard(camera)

    # check if player collided with enemy
    if(enemy.rectangle().colliderect(character.rectangle())):
        print("Collided")

    # render to window & handle clock stuff
    pygame.display.update()