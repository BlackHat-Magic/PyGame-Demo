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
    def __init__(self, coordinates: tuple, world: object, biome: Biome = None, possibilities: list = []):
        self.coordinates = coordinates
        self.world = world
        self.biome = biome
        if(self.biome):
            self.possibilities = [biome]
        else:
            self.possibilities = possibilities
    
    # cell entropy
    def entropy(self):
        # easier if this is a method instead of an attribute
        if(self.biome):
            return(0)
        return(len(self.possibilities))

    # collapse the cell
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

    # get cell neighbors
    def get_neighbors(self):
        # allows diagonals
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
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
    def update_state(self, origin_cell):
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
        
        return(self.possibilities != original_possibilities)
    
    def requirements_met():
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
            neighbors.append(neighbor.biome)
        
        # loop through all neighbors, if possibilities for a given tile are not all contained in
        # allowed_states, return false
        for neighbor in neighbors:
            possibilities = neighbor.possibilities
            if(not all([possibility in allowed_states for possibility in possibilities])):
                return(False)
        return(True)

class World():
    # init function
    def __init__(self, name: str = "world", biomes: list = [], size: tuple = (1, 1), pickle = None):
        self.name = name
        self.biomes = biomes
        self.grid = numpy.empty(size, dtype=object)
        for x in range(size[0]):
            for y in range(size[1]):
                grid[x, y] = Tile(coordinates=(x, y), world=self)
        # miscellaneous data
        self.pickle = pickle

    # observe the grid
    def observe(self):
        min_entropy = len(self.biomes)
        lowest_tiles = []

        # loop through cells
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                entropy = cell.entropy()

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
        x, y = random.choice(lowest_tiles)
        self.grid[x, y].collapse()
        return(x, y)
    
    # propagate changes
    def propagate(self, start_cell):
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
            
            # grab target tile
            required_neighbors = target_tile.biome.required_neighbors

            # sort neighbors by entropy
            neighbors = sorted(neighbors, key=lambda neighbor: neighbor.entropy())

            # loop through neighbors and collapse as required
            for tile in neighbors:
                corods = neighbor.coordinates
                neighbor = self.grid[coords]
                for requirement in target_cell.required_neighbors:
                    if(not requirement in self.grid[coords].possibilities):
                        continue
                    result = neighbor.collapse(requirement)
                    if(not result):
                        input("We goofed up.")
                        return
                    if(coords not in queue):
                        queue.append(coords)