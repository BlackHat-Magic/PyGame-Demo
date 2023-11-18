import random, numpy
from collections import deque

# Biome class
class Biome():
    def __init__(self, name, allowed_neighbors: list = [], required_neighbors: list = []):
        self.name = name
        self.allowed_neighbors = allowed_neighbors
        self.required_neighbors = required_neighbors

# tile class
class Tile():
    def __init__(self, biome: Biome = None, possibilities: list = []):
        self.biome = biome
        if(self.biome):
            self.possibilities = [biome]
        else:
            self.possibilities = possibilities
    def entropy(self):
        # easier if this is a method instead of an attribute
        return(len(self.possibilities))
    def collapse(self, collapse_to: Biome = None):
        # if no possibilities are left, we can't collapse
        if(not self.possibilities):
            return(None)
        # if not forcing collapse on specific biome, pick one at random
        if(not collapse_to):
            collapse_to = random.choice(self.possibilities)
        # if we're trying to collapse to a disallowed tile, return
        if(not collapse_to in self.possibilities):
            return(None)
        # collapse on chosen possibility
        self.biome = collapse_to
        self.possibilities = [self.biome]
        return(self.biome)

# define biomes
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

# add allowed neighbors. There has to be a better way to do this
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

# list of biomes
biomes = [forest, mountains, plains, desert, swamp, coastal, ocean, taiga, ice, death_ice]

grid_size = (25, 25)
grid = numpy.empty(grid_size, dtype=object)
for x in range(grid_size[0]):
    for y in range(grid_size[1]):
        grid[x, y] = Tile()

def observe(grid):
    min_entropy = len(biomes)
    lowest_tiles = []

    # loop through cells
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            entropy = item.entropy()
            # if new lowest entropy, set lowest entropy
            if(entropy < min_entropy):
                min_entropy = entropy
                lowest_tiles = [(x, y)]
                continue
            # else if == lowest entropy, add to lowest tiles
            if(entropy == min_entropy):
                lowest_tiles.append((x, y))
    
    # if no tiles can be collapsed, return
    if(not lowest_tiles):
        return
    
    # else, randomly select a cell to collapse
    chosen_tile = random.choice(lowest_tiles)
    grid[chosen_tile].collapse()
    return(chosen_tile)