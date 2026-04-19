from core.melds import Meld

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


    def _tile34(self, tile):
        """Gives a 34-tile index for a given tile. Same types of tiles have the same 34 index.

        Args:
            tile (int): 136-index

        Returns:
            int: 34-index
        """
        return tile // 4


    def _tile34_counts(self):
        """Checks how many tiles of a given type there are in the hand

        Returns:
            dict: 34-index: count
        """
        counts = {}
        for tile in self.tiles:
            tile34 = self._tile34(tile)
            counts[tile34] = counts.get(tile34, 0) + 1
        return counts


    def can_pon(self, discard_tile):
        """Checks if pon can be called on the discarded tile.

        Args:
            discard_tile (int): discarded tile

        Returns:
            Bool: Returns True if pon can be called, otherwise False
        """
        discard34 = self._tile34(discard_tile)
        return self._tile34_counts().get(discard34, 0) >= 2


    def can_chii(self, discard_tile):
        """Checks if chii can be called on a discarded tile.

        Args:
            discard_tile (int): discarded tile

        Returns:
            bool: True if chii can be called, otherwise False
        """
        # AI GENERATED CODE STARTS

        discard34 = self._tile34(discard_tile)

        # Honors cannot be used in chii
        if discard34 >= 27:
            return False

        suit_start = (discard34 // 9) * 9
        suit_pos = discard34 % 9
        counts = self._tile34_counts()

        patterns = []

        # x-2, x-1, x
        if suit_pos >= 2:
            patterns.append((discard34 - 2, discard34 - 1))

        # x-1, x, x+1
        if 1 <= suit_pos <= 7:
            patterns.append((discard34 - 1, discard34 + 1))

        # x, x+1, x+2
        if suit_pos <= 6:
            patterns.append((discard34 + 1, discard34 + 2))

        for a, b in patterns:
            # defensive check against crossing suit boundaries
            if not (suit_start <= a < suit_start + 9 and suit_start <= b < suit_start + 9):
                continue

            if counts.get(a, 0) >= 1 and counts.get(b, 0) >= 1:
                return True

        return False
        # AI GENERATED CODE ENDS

    def can_open_kan(self, discard_tile):
        """Checks if an open kan can be called.

        Args:
            discard_tile (int): discarded tile

        Returns:
            Bool: True if call can be made, othewise False
        """
        discard34 = self._tile34(discard_tile)
        return self._tile34_counts().get(discard34, 0) >= 3


    def apply_pon(self):
        pass


    def apply_kan(self):
        pass


    def apply_chii(self):
        pass
