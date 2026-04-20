from core.melds import Meld

class Hand:
    def __init__(self):
        self.tiles = []
        self.melds = []

    def tile_amount(self):
        return len(self.tiles)

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
        discard34 = self._tile34(discard_tile)
        return len(self._available_chii_patterns(discard34)) > 0

    def can_open_kan(self, discard_tile):
        """Checks if an open kan can be called.

        Args:
            discard_tile (int): discarded tile

        Returns:
            Bool: True if call can be made, othewise False
        """
        discard34 = self._tile34(discard_tile)
        return self._tile34_counts().get(discard34, 0) >= 3


# AI GENERATED CODE STARTS

    def get_chii_options(self, discard_tile):
        """Returns options for different chii shapes"""

        discard34 = self._tile34(discard_tile)
        options = []

        for a, b in self._available_chii_patterns(discard34):
            option = [
                self._first_tile_by_tile34(a),
                self._first_tile_by_tile34(b),
            ]
            options.append(option)

        return options

    def _remove_n_by_tile34(self, tile34, amount):
        removed = []

        for tile in list(self.tiles):
            if self._tile34(tile) == tile34:
                self.tiles.remove(tile)
                removed.append(tile)
                if len(removed) == amount:
                    break

        if len(removed) != amount:
            raise ValueError(f"Could not remove {amount} tiles of type {tile34}")

        return removed


    def _first_tile_by_tile34(self, tile34):
        for tile in self.tiles:
            if self._tile34(tile) == tile34:
                return tile

        raise ValueError(f"Tile type {tile34} not found in hand")


    def _chii_patterns(self, discard34):
        if discard34 >= 27:
            return []

        suit_start = (discard34 // 9) * 9
        suit_pos = discard34 % 9
        patterns = []

        if suit_pos >= 2:
            patterns.append((discard34 - 2, discard34 - 1))

        if 1 <= suit_pos <= 7:
            patterns.append((discard34 - 1, discard34 + 1))

        if suit_pos <= 6:
            patterns.append((discard34 + 1, discard34 + 2))

        valid = []
        for a, b in patterns:
            if suit_start <= a < suit_start + 9 and suit_start <= b < suit_start + 9:
                valid.append((a, b))

        return valid


    def _available_chii_patterns(self, discard34):
        counts = self._tile34_counts()
        return [
            (a, b)
            for a, b in self._chii_patterns(discard34)
            if counts.get(a, 0) >= 1 and counts.get(b, 0) >= 1
        ]


    def _tiles_match_chii_pattern(self, use_tiles, valid_patterns):
        use_34 = tuple(sorted(self._tile34(tile) for tile in use_tiles))
        valid_normalized = {tuple(sorted(pattern)) for pattern in valid_patterns}
        return use_34 in valid_normalized


    def _remove_tiles_for_chii_pattern(self, pattern):
        a, b = pattern
        removed = []
        removed.extend(self._remove_n_by_tile34(a, 1))
        removed.extend(self._remove_n_by_tile34(b, 1))
        return removed


    def apply_pon(self, discard_tile, from_player):
        if not self.can_pon(discard_tile):
            raise ValueError("Pon is not available for this discard")

        discard34 = self._tile34(discard_tile)
        own_tiles = self._remove_n_by_tile34(discard34, 2)
        meld_tiles = sorted(own_tiles + [discard_tile])

        meld = Meld(
            called_tile=discard_tile,
            tiles=meld_tiles,
            from_player=from_player,
            meld_type="pon",
            open_call=True,
        )
        self.melds.append(meld)
        return meld


    def apply_kan(self, discard_tile, from_player):
        if not self.can_open_kan(discard_tile):
            raise ValueError("Open kan is not available for this discard")

        discard34 = self._tile34(discard_tile)
        own_tiles = self._remove_n_by_tile34(discard34, 3)
        meld_tiles = sorted(own_tiles + [discard_tile])

        meld = Meld(
            called_tile=discard_tile,
            tiles=meld_tiles,
            from_player=from_player,
            meld_type="kan",
            open_call=True,
        )
        self.melds.append(meld)
        return meld


    def apply_chii(self, discard_tile, from_player, use_tiles=None):
        discard34 = self._tile34(discard_tile)
        available_patterns = self._available_chii_patterns(discard34)

        if not available_patterns:
            raise ValueError("Chii is not available for this discard")

        if use_tiles is not None:
            if len(use_tiles) != 2:
                raise ValueError("use_tiles must contain exactly two tile IDs")

            use_tiles = list(use_tiles)
            if not self._tiles_match_chii_pattern(use_tiles, available_patterns):
                raise ValueError("Chosen tiles do not form a valid chii pattern")

            for tile in use_tiles:
                self.remove_tile(tile)

            selected_tiles = use_tiles
        else:
            selected_tiles = self._remove_tiles_for_chii_pattern(available_patterns[0])

        meld_tiles = sorted(selected_tiles + [discard_tile])

        meld = Meld(
            called_tile=discard_tile,
            tiles=meld_tiles,
            from_player=from_player,
            meld_type="chii",
            open_call=True,
        )
        self.melds.append(meld)
        return meld
# AI GENERATED CODE ENDS
