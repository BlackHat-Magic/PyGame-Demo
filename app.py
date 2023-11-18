import pygame, sys

# Initialize pygame, window
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Demo")
clock = pygame.time.Clock()

# define font
font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 16)
text_font = pygame.font.Font("./graphics/font/GGBotNet_Public-Pixel-Font.ttf", 8)

# background
background = pygame.Surface((640, 480))
background.fill("Black")

# player
class Character():
    def __init__(self, surface: pygame.Surface, name: str, pos_x: int = 0, pos_y: int = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.surface = surface
        self.target_pos = (self.pos_x, self.pos_y)
        self.health = 100
        self.name_tag = text_font.render(name, False, "Black")
        self.health_tag = text_font.render("H: 100/100", False, "Black")

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
            self.pos_x = int(self.pos_x) // 2 * 2
            self.pos_y = int(self.pos_y) // 2 * 2
            self.target_pos = self.pos_x, self.pos_y
        unit_vector = self.dirToPoint(self.target_pos)
        x_comp, y_comp = unit_vector
        self.pos_x += x_comp
        self.pos_y += y_comp
    
    # render billboard
    def renderBillboard(self, mouse_pos):
        if(self.rectangle().collidepoint(mouse_pos)):
            # draw name tag
            pygame.draw.rect(screen, "Gray", self.name_tag.get_rect(center=(self.pos_x, self.pos_y - 20)))
            screen.blit(self.name_tag, self.name_tag.get_rect(center=(self.pos_x, self.pos_y - 20)))

            # draw health tag
            pygame.draw.rect(screen, "Gray", self.health_tag.get_rect(center=(self.pos_x, self.pos_y - 12)))
            screen.blit(self.health_tag, self.health_tag.get_rect(center=(self.pos_x, self.pos_y - 12)))

character = Character(surface=font.render("@", False, "White"), name="It's You!")

enemy = Character(surface=font.render("X", False, "Red"), name="Enemy Dude", pos_x=320, pos_y=240)

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
        character.target_pos = mouse_pos
    character.moveToTarget()

    # get keys
    keys = pygame.key.get_pressed()
    
    # render background
    screen.blit(background, (0, 0))

    # render character
    screen.blit(character.surface, character.rectangle())
    character.renderBillboard(mouse_pos)
    screen.blit(enemy.surface, enemy.rectangle())
    enemy.renderBillboard(mouse_pos)

    # check if player collided with enemy
    if(enemy.rectangle().colliderect(character.rectangle())):
        print("Collided")

    # render to window
    pygame.display.update()
    clock.tick(120)