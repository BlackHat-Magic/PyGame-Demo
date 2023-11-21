def render_dungeon(floor, camera, screen, wall_char, floor_char):
    for x in range(floor.grid.shape[0]):
        for y in range(floor.grid.shape[1]):
            tile = floor.grid[x, y]
            coordinates = (x * 16, y * 16)
            if(tile == "w"):
                camera.render(screen, wall_char, coordinates)
                continue
            if(tile == "f"):
                camera.render(screen, floor_char, coordinates)
