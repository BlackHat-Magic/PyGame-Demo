from wfc_utils import Biome, Tile, World
from scipy.spatial import Delaunay
import numpy, random

sizes = {
    "Empty": (0, 0, 0, 0),
    "Vacant": (3, 12, 3, 12),
    "Trap": (3, 5, 3, 5),
    "Combat": (3, 12, 3 ,12),
    "Treasure": (3, 3, 3, 3),
    "Merchant": (5, 5, 5, 5),
    "Starter": (3, 3, 3, 3),
    "Pre-Boss": (3, 3, 3, 3),
    "Boss": (12, 12, 12, 12),
    "Ending": (3, 3, 3, 3)
}

class Room():
    def __init__(self, size: tuple, tile: Tile, target_size: tuple = None):
        # extract data from source tile
        self.min_width, self.max_width, self.min_height, self.max_height = size
        self.biome = tile.biome
        self.coordinates = tile.coordinates

        self.connects_to = dict()

        # set self size
        if(target_size):
            self.width, self.height = target_size
        else:
            if(self.max_width < 3):
                self.width = size[0]
            else:
                self.width = random.randint(self.min_width, self.max_width)
            if(self.max_height < 3):
                self.height = size[2]
            else:
                self.height = random.randint(self.min_height, self.max_height)
        
        # generate empty grid
        self.grid = numpy.full((15, 15), "p", dtype=str)
        if(self.width == 0 or self.height == 0):
            self.center = (7, 7)
            return
        
        # self center
        center_x = 7
        center_y = 7

        # find max offset
        max_offset_x = (12 - self.width) // 2
        offset_x = max_offset_x
        max_offset_y = (12 - self.height) // 2
        offset_y = max_offset_y

        # offset center
        if(max_offset_x != 0):
            offset_x = random.randint(max_offset_x * -1, max_offset_x)
        if(max_offset_y != 12):
            offset_y = random.randint(max_offset_y * -1, max_offset_y)
        self.offset = (offset_x, offset_y)

        center_x += offset_x
        center_y += offset_y

        self.center = (center_x, center_y)
        
        # write spaces to grid
        for x in range(self.width + 2):
            for y in range(self.height + 2):
                target_x = center_x - self.width // 2 + x
                target_y = center_y - self.height // 2 + y
                if(x == 0 or y == 0 or x == self.width + 1 or y == self.height + 1):
                    self.grid[target_x, target_y] = "w"
                    continue
                self.grid[target_x, target_y] = "f"

class Floor():
    def __init__(self, world: World):
        self.width, self.height = world.grid.shape
        self.width *= 15
        self.height *= 15
        self.start_coordinates = (0, 0)
        self.grid = numpy.empty((self.width, self.height), dtype=object)
        for big_x in range(world.grid.shape[0]):
            for big_y in range(world.grid.shape[1]):
                tile = world.grid[big_x, big_y]
                room = Room(sizes[tile.biome.name], tile)
                if(room.biome.name == "Starter"):
                    center_x, center_y = room.center
                    start_x = big_x * 15 + center_x + 1
                    start_y = big_y * 15 + center_y + 1
                    self.start_coordinates = (start_x, start_y)
                for small_x in range(room.grid.shape[0]):
                    for small_y in range(room.grid.shape[1]):
                        x, y = big_x * 15 + small_x, big_y * 15 + small_y
                        self.grid[x, y] = room.grid[small_x, small_y]

    def print(self):
        for y in range(self.grid.shape[0]):
            string = ""
            for x in range(self.grid.shape[0]):
                string += self.grid[x, y]
            print(string)

    def triangulate(self):
        centers = numpy.array([tile.coordinates] for tile in self.grid.flatten())
        tri = Delaunay(centers)

        for simplex in tri.simpleces:
            for tile1 in simplex:
                for tile2 in simplex:
                    if(tile1 == tile2):
                        continue
                    tile1.connects_to[tile2.coordinates] = False