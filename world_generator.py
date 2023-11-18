from wfc_utils import Biome, Tile, World

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