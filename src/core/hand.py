class Hand:    
    def __init__(self):
        self.tiles = []
        self.melds = []

    def add_tile(self, tile):
        if tile in self.tiles:
            raise ValueError(f"Tile {tile} is already in hand")

        self.tiles.append(tile)
        self.tiles.sort()

    def remove_tile(self, tile):
        if tile not in self.tiles:
            raise ValueError(f"Tile {tile} is not in hand")

        self.tiles.remove(tile)
        return tile
