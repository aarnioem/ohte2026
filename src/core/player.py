from core.hand import Hand

class Player:
    """
    Representation for a player of the game, should have information of tiles in hand,
    called tiles, discards, score etc.
    """
    def __init__(self, human=False):
        self.human = human
        self.hand = Hand()
        self.discards = [] # change this to a class later maybe
        self.score = 25000
        self.riichi = False

    def is_human(self):
        return self.human

    def receive_tile(self, tile_id):
        self.hand.add_tile(tile_id)

    def discard(self, tile):
        tile = self.hand.remove_tile(tile)
        self.discards.append(tile)
        return tile
