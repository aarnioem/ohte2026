from hand import Hand

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

    def receive_tile(self):
        pass

    def discard(self):
        pass
