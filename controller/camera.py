import pygame

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 500
    
    def vec_to_point(self, point) -> tuple:
        target_x, target_y = point
        dist_x, dist_y = target_x - self.x, target_y - self.y
        return(dist_x, dist_y)
    def dist_to_point(self, point) -> float:
        dist_x, dist_y = self.vec_to_point(point)
        distance = (dist_x**2 + dist_y**2)**0.5
        return(distance)
    def dir_to_point(self, point) -> tuple:
        dir_x, dir_y = self.vec_to_point(point)
        distance = self.dist_to_point(point)
        if(distance == 0):
            return(0, 0)
        unit_vector = (dir_x / distance, dir_y / distance)
        return(unit_vector)
    
    # wasd movement
    def move(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if(not any([keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]])):
            self.move_to_target((round((self.x + 8) / 16) * 16 - 8, round((self.y + 8) / 16) * 16 - 8), dt)
            return

        x = 0.0
        y = 0.0

        if(keys[pygame.K_w]):
            y -= 1.0
        if(keys[pygame.K_s]):
            y += 1.0
        if(keys[pygame.K_a]):
            if(y != 0):
                y *= 0.7
                x -= 0.7
            else:
                x -= 1.0
        if(keys[pygame.K_d]):
            if(y != 0):
                y *= 0.7
                x += 0.7
            else:
                x += 1.0
            
        self.x += x * self.speed * dt / 1000
        self.y += y * self.speed * dt / 1000
    
    def move_to_target(self, target: tuple, dt: float) -> None:
        distance = self.dist_to_point(target)
        if(distance < 4):
            self.x, self.y = target
            return
        unit_vector = self.dir_to_point(target)
        x_comp, y_comp = unit_vector
        self.x += x_comp * self.speed * dt / 1000
        self.y += y_comp * self.speed * dt / 1000

    
    # render something to the screen
    def render(self, screen: pygame.display, surface: pygame.surface, world_pos: tuple) -> None:
        x, y = world_pos
        rectangle = surface.get_rect(center=(x - self.x, y - self.y))
        if(not rectangle.colliderect(pygame.display.get_surface().get_rect())):
            return
        screen.blit(surface, rectangle)
    
    # get relative position of something
    def get_relative_pos(self, relative_pos: tuple) -> tuple:
        x, y = relative_pos
        return(x - self.x, y - self.y)
    
    def get_mouse_world_position(self) -> tuple:
        x, y = pygame.mouse.get_pos()
        x += self.x
        y += self.y
        return(x, y)