from wfc_utils import Biome, Tile, World
import numpy, random

sizes = {
    "Empty": (0, 0),
    "Vacant": (3, 12),
    "Trap": (3, 5),
    "Combat": (3, 12),
    "Treasure": (3, 3),
    "Merchant": (5, 5),
    "Starter": (3, 3),
    "Pre-Boss": (3, 3),
    "Boss": (12, 12),
    "Ending": (3, 3)
}

class Room():
    def __init__(self, max_size: tuple, tile: Tile, target_size: tuple = None):
        self.max_width, self.max_height = max_size
        self.biome = tile.biome
        self.coordinates = tile.coordinates
        if(target_size):
            self.width, self.height = target_size
        else:
            if(self.max_width == 0):
                self.width = 0
            else:
                self.width = random.randint(1, self.max_width)
            if(self.max_height == 0):
                self.height = 0
            else:
                self.height = random.randint(1, self.max_height)

class Floor():
    def __init__