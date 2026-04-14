import random

TOTAL_TILES = 136
DEAD_WALL_SIZE = 14
RED_FIVE_IDS = {16, 52, 88}

def generate_wall_tiles():
    """
    Returns a list of 136 tile IDs.
    """
    tiles = list(range(TOTAL_TILES))
    return tiles

class Wall:
    """
    Representation for the 136 tile wall.
    """
    def __init__(self, tiles=None, shuffle=True, dead_wall_size=14) -> None:
        if tiles is None:
            self.tiles = generate_wall_tiles()
        else:
            self.tiles = list(tiles)

        self.total_tiles = len(self.tiles)
        self.dead_wall_size = dead_wall_size

        if shuffle:
            random.shuffle(self.tiles)

        self.draw_pointer = 0

    def live_tiles(self):
        return self.total_tiles - self.draw_pointer - self.dead_wall_size

    def draw_tile(self):
        """Draws one tile from the wall.
        Returns the tile ID and increments the draw pointer"""

        if self.live_tiles() <= 0:
            raise IndexError("No tiles left in the wall")

        tile = self.tiles[self.draw_pointer] # add some error checking here
        self.draw_pointer += 1
        return tile
