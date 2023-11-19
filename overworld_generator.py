from wfc_utils import Biome, Tile, World

# define biomes
forest = Biome("Forest")
mountains = Biome("Mountains")
plains = Biome("Plains")
desert = Biome("Desert")
swamp = Biome("Swamp")
# coastal = Biome("Coastal")
# ocean = Biome("Ocean")
taiga = Biome("Taiga")
ice = Biome("Ice")
death_ice = Biome("Death Ice")
volcano = Biome("Volcano")
cherry = Biome("Cherry")
ice_mountain = Biome("Ice Mountain")

# add allowed neighbors. There has to be a better way to do this
forest.allowed_neighbors = [forest, plains, swamp, taiga, cherry]
mountains.allowed_neighbors = [mountains, plains, desert, volcano]
plains.allowed_neighbors = [forest, mountains, plains, desert, swamp, taiga, cherry]
desert.allowed_neighbors = [mountains, plains, desert]
swamp.allowed_neighbors = [forest, plains, swamp, cherry]
# coastal.allowed_neighbors = [forest, plains, swamp, coastal, ocean]
# coastal.required_neighbors = [ocean]
# ocean.allowed_neighbors = [coastal, ocean]
taiga.allowed_neighbors = [forest, plains, ice, ice_mountain]
ice.allowed_neighbors = [taiga, ice, death_ice, ice_mountain]
death_ice.allowed_neighbors = [ice, death_ice, taiga, ice_mountain]
volcano.allowed_neighbors = [mountains, volcano, desert]
cherry.allowed_neighbors = [forest, plains, cherry, swamp]
ice_mountain.allowed_neighbors = [ice, taiga, death_ice, ice_mountain]

# list of biomes
# biomes = [forest, mountains, plains, desert, swamp, coastal, ocean, taiga, ice, death_ice]
biomes = [forest, mountains, plains, desert, swamp, taiga, ice, death_ice, volcano, cherry, ice_mountain]