class Meld:

    def __init__(self, called_tile, tiles, from_player, meld_type, open_call=True) -> None:
        self.called_tile = called_tile
        self.tiles = tiles
        self.from_player = from_player
        self.meld_type = meld_type
        self.open_call = open_call
