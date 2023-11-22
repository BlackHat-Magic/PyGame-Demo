import random, numpy
from collections import deque

# Biome class
class Biome():
    def __init__(self, name, allowed_neighbors: list = [], required_neighbors: list = [], minimum: int = 0, maximum: int = 0, empty: bool = False):
        self.name = name
        self.allowed_neighbors = allowed_neighbors
        self.required_neighbors = required_neighbors
        self.minimum = minimum
        self.maximum = maximum
        self.empty = empty # i forgot why I added this attribute

# tile class
class Tile():
    def __init__(self, coordinates: tuple, world: object, biome: Biome = None, possibilities: list = []):
        self.coordinates = coordinates
        self.world = world
        self.biome = biome
        if(self.biome):
            self.possibilities = [biome]
        else:
            self.possibilities = possibilities
    
    # cell entropy
    def entropy(self) -> int:
        # easier if this is a method instead of an attribute
        if(self.biome):
            return(0)
        return(len(self.possibilities))

    # collapse the cell
    def collapse(self, collapse_to: Biome = None) -> Biome:
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

    # get cell neighbors
    def get_neighbors(self) -> list:
        # allows diagonals
        offsets = [(0, 1), (-1, 0), (1, 0), (0, -1)]
        neighbors = []

        # loop through possible offsets
        for x_offset, y_offset in offsets:
            adj_x, adj_y = self.coordinates[0] + x_offset, self.coordinates[1] + y_offset
            # if attempting to check a cell out of bounds, skip
            if((not 0 <= adj_x < self.world.grid.shape[0]) or (not 0 <= adj_y < self.world.grid.shape[1])):
                continue
            neighbors.append(self.world.grid[adj_x, adj_y])
        return(neighbors)
    
    # update state upon propagation
    def update_state(self, origin_cell: tuple) -> bool:
        # store original states
        origin_cell = self.world.grid[origin_cell]

        original_possibilities = self.possibilities

        # if this cell has already collapsed, we can skip it.
        if(self.biome):
            return(False)

        new_possibilities = set()
        # if the origin cell collapsed...
        if(origin_cell.biome):
            # remove all possibilities that are not allqwowed by the cell who 
            # triggered the function
            new_possibilities = set(self.possibilities)
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
        new_possibilities = set(self.possibilities).intersection(new_possibilities)
        self.possibilities = list(new_possibilities)
        
        return(self.possibilities in original_possibilities)
    
    def requirements_met(self) -> bool:
        # if the cell hasn't collapsed yet and not all of the possibilities have requirements, the
        # requirements of the cell are met by default, since it's possible that the cell won't have a
        # requirement at all
        if((not self.biome) and (not all([possibility.required_neighbors for possibility in self.possibilities]))):
            return(True)
        # if the cell has collapsed but has no requirements, the requiremetns are met by default
        if(self.biome and not self.biome.required_neighbors):
            return(True)

        # essentially, get a collection all allowed neighbors
        # allowed states are based on requirements, not literal allowed_neighbors
        allowed_states = set()
        for possibility in self.possibilities:
            for requirement in possibility.required_neighbors:
                allowed_states.add(requirement)

        # get all the neighbors
        neighbors = []
        for neighbor in self.get_neighbors():
            if(not neighbor.biome):
                continue
            neighbors.append(neighbor)
        
        # loop through all neighbors, if possibilities for a given tile are not all contained in
        # allowed_states, return false
        for neighbor in neighbors:
            possibilities = neighbor.possibilities
            if(not all([possibility in allowed_states for possibility in possibilities])):
                return(False)
        
        neighbor_biomes = [tile.biome for tile in self.get_neighbors()]
        for biome in self.biome.required_neighbors:
            if(biome not in neighbor_biomes):
                return(False)

        return(True)

class World():
    # init function
    def __init__(self, name: str = "world", biomes: list = [], size: tuple = (1, 1), pickle: any = None):
        self.name = name
        self.biomes = biomes
        self.grid = numpy.empty(size, dtype=object)
        for x in range(size[0]):
            for y in range(size[1]):
                self.grid[x, y] = Tile((x, y), self, None, biomes)
        # miscellaneous data
        self.pickle = pickle

    # observe the grid
    def observe(self, collapse_to: Biome = None) -> tuple:
        min_entropy = len(self.biomes)
        lowest_tiles = []
        all_tiles = []
        for x, column in enumerate(self.grid):
            for y, tile in enumerate(column):
                if(tile.biome):
                    all_tiles.append(tile.biome)
        
        need_to_generate = []

        for biome in self.biomes:
            if(biome.minimum > all_tiles.count(biome)):
                need_to_generate.append(biome)
        if(need_to_generate and not collapse_to):
            collapse_to = random.choice(need_to_generate)

        # loop through cells
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                entropy = cell.entropy()
                if(entropy == 0):
                    continue
                if(collapse_to and not collapse_to in self.grid[x, y].possibilities):
                    continue
                # if new lowest entropy, set lowest entropy
                if(entropy < min_entropy):
                    min_entropy = entropy
                    lowest_tiles = [(x, y)]
                    continue

                # else if == lowest entropy, add to lowest tiles
                if(entropy == min_entropy):
                    lowest_tiles.append((x, y))
                continue

        # if no tiles can be collapsed, return
        if(not lowest_tiles):
            return

        # else, randomly select a cell to collapse
        x, y = random.choice(lowest_tiles)
        if(not collapse_to):
            self.grid[x, y].collapse()
        else:
            self.grid[x, y].collapse(collapse_to)
        return(x, y)
    
    # propagate changes
    def propagate(self, start_cell: tuple) -> None:
        # queue of cells whose states have changed and therefore need their neighbors'
        # states changed
        queue = deque([start_cell])

        # while the queue isn't empty
        while(queue):
            x, y = queue.popleft()
            target_tile = self.grid[x, y]
            neighbors = target_tile.get_neighbors()

            # loop through adjacent cells (including diagonals)
            for neighbor in neighbors:
                # update possible states
                updated = neighbor.update_state((x, y))

                # if we updated, then the updated cell gets added to the queue of cells that need to
                # propagate
                if(updated and (not neighbor.coordinates in queue)):
                    queue.append(neighbor.coordinates)
            
            # if the cell we're propagating hasn't collapsed or doesn't have a required neighbor or meets
            # its requirements, we're done with it
            if(target_tile.requirements_met()):
                continue
            
            # 
            required_neighbors = []
            for possibility in target_tile.possibilities:
                for requirement in possibility.required_neighbors:
                    required_neighbors.append(requirement)


            # sort neighbors by entropy
            neighbors = sorted(neighbors, key=lambda neighbor: neighbor.entropy())

            # loop through neighbors and collapse as required
            for neighbor in neighbors:
                for requirement in required_neighbors:
                    if(not requirement in neighbor.possibilities):
                        continue
                    result = neighbor.collapse(requirement)
                    if(neighbor.coordinates not in queue):
                        queue.append(neighbor.coordinates)
                if(target_tile.requirements_met):
                    break
        
        # get biomes who have reached their max
        flattened = self.grid.flatten()
        biomes_in_grid = [tile.biome for tile in flattened if tile.biome]
        maxed = []
        for biome in self.biomes:
            if(biome.maximum != 0 and biome.maximum <= biomes_in_grid.count(biome)):
                maxed.append(biome)
        for tile in flattened:
            for biome in maxed:
                if(not tile.biome and biome in tile.possibilities):
                    tile.possibilities.remove(biome)
    
    def max_entropy(self) -> int:
        maximum_entropy = -1
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                entropy = self.grid[x, y].entropy()
                if(entropy > maximum_entropy):
                    maximum_entropy = entropy
        return(maximum_entropy)
    
    def min_entropy(self) -> int:
        minimum_entropy = float("inf")
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                entropy = self.grid[x, y].entropy()
                if(entropy < minimum_entropy):
                    minimum_entropy = entropy
        return(minimum_entropy)
    
    def all_collapsed(self) -> bool:
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if(not self.grid[x, y].biome):
                    return(False)
        return(True)
    
    def generate(self) -> None:
        while not self.all_collapsed():
            observed = self.observe()
            if(not observed):
                continue
            self.propagate(observed)