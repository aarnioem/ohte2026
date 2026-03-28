import random

TOTAL_TILES = 136
DEAD_WALL_SIZE = 14
RED_FIVE_IDS = {16, 52, 88}

def generate_wall_tiles():
    """
    Returns a list of 136 tile IDs and shuffles it.
    """
    wall = list(range(TOTAL_TILES))
    random.shuffle(wall)
    return wall

class Wall:
    """
    Representation for the 136 tile wall.
    """
    def __init__(self) -> None:
        self.tiles = generate_wall_tiles()
        self.draw_pointer = 0

    def draw_tile(self):
        """Draws one tile from the wall.
        Returns the tile ID and increments the draw pointer"""
        tile = self.tiles[self.draw_pointer] # add some error checking here
        self.draw_pointer += 1
        return tile
