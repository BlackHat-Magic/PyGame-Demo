import pygame, sys
from wfc_utils import Biome, Tile, World
from dungeon_layout_generator import rooms
from dungeon_room_generator import Floor

# Initialize pygame, window
pygame.init()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Pygame Demo")
clock = pygame.time.Clock()

# define font
font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 16)
text_font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 8)

# background
background = pygame.Surface((1280, 960))
background.fill("Black")

# character class
class Character():
    def __init__(self, surface: pygame.Surface, name: str, pos_x: int = 0, pos_y: int = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.surface = surface
        self.target_pos = (self.pos_x, self.pos_y)
        self.health = 100
        self.name_tag = font.render(name, False, "Black")
        self.health_tag = font.render("H: 100/100", False, "Black")

    # movement with keys (unused)
    def moveUp(self, amount: int = 1):
        self.pos_y -= amount
    def moveDown(self, amount: int = 1):
        self.pos_y += amount
    def moveLeft(self, amount: int = 1):
        self.pos_x -= amount
    def moveRight(self, amount: int = 1):
        self.pos_x += amount
    
    # distance to point
    def vecToPoint(self, point):
        target_x, target_y = point
        dist_x, dist_y = target_x - self.pos_x, target_y - self.pos_y
        return(dist_x, dist_y)
    def distToPoint(self, point):
        dist_x, dist_y = self.vecToPoint(point)
        distance = (dist_x**2 + dist_y**2)**0.5
        return(distance)
    def dirToPoint(self, point):
        dir_x, dir_y = self.vecToPoint(point)
        distance = self.distToPoint(point)
        if(distance == 0):
            return(0, 0)
        unit_vector = (dir_x / distance, dir_y / distance)
        return(unit_vector)

    # get character rectangle
    def rectangle(self):
        return(self.surface.get_rect(center=(self.pos_x, self.pos_y)))

    # point-and-click movement
    def moveToTarget(self):
        if(self.distToPoint(self.target_pos) < 1):
            self.pos_x, self.pos_y = self.target_pos
            return
        unit_vector = self.dirToPoint(self.target_pos)
        x_comp, y_comp = unit_vector
        self.pos_x += x_comp
        self.pos_y += y_comp
    
    # render billboard
    def renderBillboard(self, mouse_pos):
        if(self.rectangle().collidepoint(mouse_pos)):
            # draw name tag
            pygame.draw.rect(screen, "Gray", self.name_tag.get_rect(center=(self.pos_x, self.pos_y - 32)))
            screen.blit(self.name_tag, self.name_tag.get_rect(center=(self.pos_x, self.pos_y - 32)))

            # draw health tag
            pygame.draw.rect(screen, "Gray", self.health_tag.get_rect(center=(self.pos_x, self.pos_y - 16)))
            screen.blit(self.health_tag, self.health_tag.get_rect(center=(self.pos_x, self.pos_y - 16)))

# camera class
class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 2
    def move_up(self, amt: int = 1):
        self.y -= amt * speed
    def move_down(self, amt: int = 1):
        self.y += amt * speed
    def move_left(self, amt: int = 1):
        self.x -= amt * speed
    def move_right(self, amt: int = 1):
        self.y += amt * speed

camera = Camera

# character and enemy
character = Character(surface=font.render("@", False, "White"), name="It's You!")
enemy = Character(surface=font.render("X", False, "Red"), name="Enemy Dude", pos_x=320, pos_y=240)

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

# time stuff
big_t = 0
dt = 0

floor_char = font.render(".", False, "Gray")
wall_char = font.render("#", False, "Gray")

# game loop
while True:
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
        target_x = target_x // 16 * 16 + 8
        target_y = target_y // 16 * 16 + 8
        character.target_pos = (target_x, target_y)
    character.moveToTarget()

    big_t += dt
    
    # render background
    screen.blit(background, (0, 0))
    
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
                        screen.blit(wall_char, coordinates)
                        continue
                    if(tile == "f"):
                        screen.blit(floor_char, coordinates)

    # render character
    screen.blit(character.surface, character.rectangle())
    character.renderBillboard(mouse_pos)
    screen.blit(enemy.surface, enemy.rectangle())
    enemy.renderBillboard(mouse_pos)

    # check if player collided with enemy
    if(enemy.rectangle().colliderect(character.rectangle())):
        print("Collided")

    # render to window & handle clock stuff
    pygame.display.update()
    dt = clock.tick(120)