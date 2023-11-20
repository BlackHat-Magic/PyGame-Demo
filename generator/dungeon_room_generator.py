from wfc_utils import Biome, Tile, World
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
        self.grid = numpy.empty(world.grid.shape, dtype=object)
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                self.grid[x, y] = Room(sizes[world.grid[x, y].biome.name], world.grid[x, y])