import random, numpy
from collections import deque

class Biome():
    def __init__(self, name, allowed_neighbors: list = [], required_neighbors: list = []):
        self.name = name
        self.allowed_neighbors = allowed_neighbors
        self.required_neighbors = required_neighbors

class Tile():
    def __init__(self):
        self.biome = None
        self.possibilities = biomes
    def entropy(self):
        return(len(self.possibilities))
    def collapse(self, collapse_to: tile = None):
        if(not collapse_to):
            self.collapse(random.choice(self.possibilities))
            return(self.biome)
        if(not collapse_to in self.possibilities):
            return(None)
        self.biome = collapse_to
        self.possibilities = [self.biome]
        return(self.biome)

forest = Biome("Forest")
mountains = Biome("Mountains")
plains = Biome("Plains")
desert = Biome("Desert")
swamp = Biome("Swamp")
coastal = Biome("Forest")
ocean = Biome("Ocean")
taiga = Biome("Taiga")
ice = Biome("Ice")
death_ice = Biome("Death Ice")
volcano = Biome("Volcano")

forest.allowed_neighbors = [forest, mountains, plains, swamp, coastal, taiga]
mountains.allowed_neighbors = [forest, mountains, plains, desert, taiga, ice, volcano]
plains.allowed_neighbors = [forest, mountains, plains, desert, swamp, coastal, taiga]
desert.allowed_neighbors = [mountains, plains, desert]
swamp.allowed_neighbors = [forest, plains, swamp, coastal, taiga]
coastal.allowed_neighbors = [forest, plains, swamp, coastal, ocean]
coastal.required_neighbors = [ocean]
ocean.allowed_neighbors = [coastal, ocean]
taiga.allowed_neighbors = [forest, mountains, plains, swamp, ice]
ice.allowed_neighbors = [taiga, ice, death_ice]
death_ice.allowed_neighbors = [ice, death_ice]
volcano.allowed_neighbors = [mountains]

biomes = [forest, mountains, plains, desert, swamp, coastal, ocean, taiga, ice, death_ice]

grid_size = (25, 25)
grid = numpy.empty(grid_size, dtype=object)
for x in range(grid_size[0]):
    for y in range(grid_size[1]):
        grid[x, y] = Tile()