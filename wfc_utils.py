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

# propagate changed tiles
def propagate(grid, start_cell):
    # queue of cells whose states have changed and therefore need their neighbors'
    # states changed
    queue = deque([start_cell])
    
    # while the queue isn't empty
    while(queue):
        x, y = queue.popleft()

        # loop through adjacent cells (including diagonals)
        for x_offset, y_offset in [
            (-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)
        ]:
            adj_x, adj_y = x + x_offset, y + y_offset

            # if attempting to check a cell out of bounds, skip
            if((not 0 <= adj_x < grid.shape[0]) or (not 0 <= adj_y < grid.shape[1])):
                continue

            # else update possible states
            updated = updateStates((x, y), (adj_x, adj_y))

            # if we updated, then the updated cell gets added to the queue of cells that need to
            # propagate
            if(updated and (not (adj_x, adj_y) in queue)):
                queue.append((adj_x, adj_y))
        
        # if the cell we're propagating hasn't collapsed or doesn't have a required neighbor or meets
        # its requirements, we're done with it
        if(grid[x, y].requirementsMet()):
            continue
        
        # grab target tile
        target_tile = grid[x, y]
        required_neighbors = target_tile.biome.required_neighbors

        # get neighbors and sort by entropy
        neighbors = [
            (x + x_offset, y + y_offset) for x_offset, y_offset in [
                (-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)
            ]
        ]
        neighbors = sorted(neighbors, key=lambda coords: grid[coords].entropy() for coords in neighbors)

        # loop through neighbors and collapse as required
        for coords in neighbors:
            neighbor = grid[coords]
            for requirement in target_cell.required_neighbors:
                if(not requirement in grid[coords].possibilities):
                    continue
                result = neighbor.collapse(requirement)
                if(not result):
                    input("We goofed up.")
                    return
                if(coords not in queue):
                    queue.append(coords)

def requirementsMet(x, y):
    # if the cell hasn't collapsed yet and not all of the possibilities have requirements, the
    # requirements of the cell are met by default, since it's possible that the cell won't have a
    # requirement at all
    if((not grid[x, y].biome) and (not all([possibility.requirements for possibility in grid[x, y].possibilities]))):
        return(True)
    # if the cell has collapsed but has no requirements, the requiremetns are met by default
    if(grid[x, y].biome and not grid[x, y].biome.required_neighbors):
        return(True)

    # essentially, get a collection all allowed neighbors
    # if the cell is collapsed, `possibilities` will have length 1
    # allowed states are based on requirements, not literal allowed_neighbors
    allowed_states = set()
    for possibility in grid[x, y].possibilities:
        for requirement in possibility.required_neighbors:
            allowed_states.add(requirement)
    allowed_states = [state for state in allowed_states]

    # get all the neighbors
    offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
    neighbors = []
    for x_offset, y_offset in offsets:
        adj_x = x + x_offset
        adj_y = y + y_offset
        if((not 0 <= adj_x < grid.shape[0]) or (not 0 <= adj_y < grid.shape[1])):
            continue
        neighbor = grid[adj_x, adj_y]
        if(not neighbor.biome):
            continue
        neighbors.append(neighbor.biome)
    
    # loop through all neighbors, if possibilities for a given tile are not all contained in
    # allowed_states, return false
    for neighbor in neighbors:
        possibilities = set(neighbor.possibilities)
        if(intersection(possibilities, allowed_states) != possibilities):
            return(False)
    return(True)

# when a cell is propagated, each neighboring cell 
def updateStates(grid, x, y, adj_x, adj_y):
    # store original states
    target_cell = grid[adj_x, adj_y]
    origin_cell = grid[x, y]

    original_possibilities = target_cell.possibilities

    # if this cell has already collapsed, we can skip it.
    if(target_cell.biome):
        return False

    new_possibilities = set()
    # if the origin cell collapsed...
    if(origin_cell.biome):
        # remove all possibilities that are not allqwowed by the cell who 
        # triggered the function
        new_possibilities = set(target_cell.possibilities)
        new_possibilities.intersection_update(origin_cell.biome.allowed_neighbors)
    
    # if the origin cell hasn't collapsed...
    else:
        # assemble a set of possibilities allowed by the origin cell
        for possibility in origin_cell.possibilities:
            if(not new_possibilities):
                new_possibilities = set(possibility.allowed_neighbors)
                continue
            for neighbor in possibility.allowed_neighbors:
                new_possibilities.add(neighbor)

    # intersect new possibilities with old ones
    new_possibilities = set(target_cell.possibilities).intersection(new_possibilities)
    target_cell.possibilities = list(new_possibilities)
    
    return(target_cell.possibilities != original_possibilities)