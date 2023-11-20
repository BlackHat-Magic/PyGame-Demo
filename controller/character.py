import pygame
from camera import Camera

class Character():
    def __init__(self, surface: pygame.Surface, name: str, screen: pygame.display, font: pygame.font, pos_x: int = 0, pos_y: int = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.surface = surface
        self.target_pos = (self.pos_x, self.pos_y)
        self.health = 100
        self.screen = screen
        self.font = font
        self.name_tag = self.font.render(name, False, "Black")
        self.health_tag = self.font.render("H: 100/100", False, "Black")
    
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
    def renderBillboard(self, camera: Camera) -> None:
        x, y = camera.get_mouse_world_position()
        if(self.rectangle().collidepoint((x, y))):
            # draw name tag
            relative_pos = camera.get_relative_pos((self.pos_x, self.pos_y - 32))
            pygame.draw.rect(self.screen, "Gray", self.name_tag.get_rect(center=relative_pos))
            self.screen.blit(self.name_tag, self.name_tag.get_rect(center=relative_pos))

            # draw health tag
            relative_pos = camera.get_relative_pos((self.pos_x, self.pos_y - 16))
            pygame.draw.rect(self.screen, "Gray", self.health_tag.get_rect(center=relative_pos))
            self.screen.blit(self.health_tag, self.health_tag.get_rect(center=relative_pos))