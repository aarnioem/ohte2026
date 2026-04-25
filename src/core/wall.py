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
        self.kan_counter = 0

        if shuffle:
            random.shuffle(self.tiles)

        self.rinshan_tiles = self._get_rinshan_tiles()

        self.draw_pointer = 0

    def live_tiles(self):
        """Returns the number of drawable tiles in the wall

        Returns:
            int: tiles left
        """
        return self.total_tiles - self.draw_pointer - self.kan_counter - self.dead_wall_size

    def draw_tile(self):
        """Draws a tile from the live wall and increments the draw counter
        Returns:
            int: tile id"""

        if self.live_tiles() <= 0:
            raise IndexError("No tiles left in the wall")

        tile = self.tiles[self.draw_pointer] # add some error checking here
        self.draw_pointer += 1
        return tile

    def _get_rinshan_tiles(self):
        """Sets up the 4 rinshan tiles in correct order for convenience

        Returns:
            list: rinshan tiles
        """
        return [
            self.tiles[-2],
            self.tiles[-1],
            self.tiles[-4],
            self.tiles[-3]
        ]


    def draw_rinshan_tile(self):
        """Draws a tile from the dead wall and increments the kan counter
        Returns:
            int: tile id
        """
        if self.live_tiles() <= 0:
            raise IndexError("No tiles left in the wall")

        tile = self.rinshan_tiles[self.kan_counter]
        self.kan_counter += 1
        return tile
