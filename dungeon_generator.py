from wfc_utils import Biome, Tile, World

empty = Biome("Empty")
vacant = Biome("Vacant")
trap = Biome("Trap", maximum=3)
combat = Biome("Combat")
treasure = Biome("Treasure", minimum=1, maximum=2)
merchant = Biome("Merchant", minimum=1, maximum=1)
starter = Biome("Starter", minimum=1, maximum=1)
pre_boss = Biome("Pre-Boss", minimum=1, maximum=1)
boss = Biome("Boss", minimum=1, maximum=1)
ending = Biome("Ending", minimum=1, maximum=1)

empty.allowed_neighbors = [empty, trap, combat, treasure, merchant, starter, vacant]
vacant.allowed_neighbors = [empty, trap, combat, treasure, merchant, starter, vacant]
trap.allowed_neighbors = [empty, treasure, merchant, starter, vacant]
combat.allowed_neighbors = [empty, treasure, merchant, starter, vacant]
treasure.allowed_neighbors = [empty, trap, combat, merchant, starter, vacant]
merchant.allowed_neighbors = [empty, trap, combat, treasure, starter, vacant]
starter.allowed_neighbors = [empty, trap, combat, treasure, merchant, vacant]
pre_boss.allowed_neighbors = [empty, trap, combat, treasure, merchant, boss, vacant]
boss.allowed_neighbors = [pre_boss, ending, empty]
ending.allowed_neighbors = [boss, empty]

pre_boss.required_neighbors = [boss]
boss.required_neighbors = [pre_boss, ending]
ending.required_neighbors = [boss]

rooms = [empty, empty, empty, trap, combat, treasure, merchant, starter, pre_boss, boss, ending, vacant]