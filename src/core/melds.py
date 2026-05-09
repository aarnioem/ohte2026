class Meld:

    def __init__(self, called_tile, tiles, from_player, meld_type, *, open_call=True) -> None:
        self.called_tile = called_tile
        self.tiles = tiles
        self.from_player = from_player
        self.meld_type = meld_type
        self.open_call = open_call

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Meld):
            return NotImplemented

        return (
            self.called_tile == value.called_tile
            and self.tiles == value.tiles
            and self.from_player == value.from_player
            and self.meld_type == value.meld_type
            and self.open_call == value.open_call
        )
