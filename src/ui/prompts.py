import random

from core.player import Player
from ui.renderer import CLIRenderer


class CLIPrompts:
    def __init__(self, renderer: CLIRenderer):
        self._renderer = renderer

    def get_discard_choice(self, player: Player, dora_indicators=None):
        if player.is_human():
            self._renderer.separator("CHOOSE DISCARD")
            regular_tiles, drawn_tile = self._print_discard_hand(player, dora_indicators)

            while True:
                try:
                    choice = int(input("Choose discard index: "))
                    if drawn_tile is not None and choice == 0:
                        print()
                        return drawn_tile

                    if 1 <= choice <= len(regular_tiles):
                        print()
                        return regular_tiles[choice - 1]

                    print("Index out of range.")

                except ValueError:
                    print("Please input a valid number")
        else:
            return random.choice(player.hand.tiles)

    def get_tsumo_choice(self, player: Player, drawn_tile: int):
        if not player.is_human():
            return True

        while True:
            self._renderer.separator("TSUMO")
            print(f"You drew {self._renderer.tile_to_text(drawn_tile)}")
            self._print_hand(player)
            choice = input("Tsumo? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                print()
                return True
            if choice in ("n", "no"):
                print()
                return False
            print("Please choose y or n.")

    def get_ron_choice(self, player: Player, discarded_tile: int):
        if not player.is_human():
            return True

        while True:
            self._renderer.separator("RON")
            print(f"You can ron on {self._renderer.tile_to_text(discarded_tile)}")
            self._print_hand(player)
            choice = input("Ron? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                print()
                return True
            if choice in ("n", "no"):
                print()
                return False
            print("Please choose y or n.")

    def get_pon_choice(self, player: Player, discarded_tile: int):
        if not player.is_human():
            return False

        while True:
            self._renderer.separator("PON")
            print(f"You can pon on {self._renderer.tile_to_text(discarded_tile)}")
            self._print_hand(player)
            choice = input("Call pon? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                print()
                return True
            if choice in ("n", "no"):
                print()
                return False
            print("Please choose y or n.")

    def get_kan_choice(self, player: Player, discarded_tile: int):
        if not player.is_human():
            return False

        while True:
            self._renderer.separator("KAN")
            print(f"You can kan on {self._renderer.tile_to_text(discarded_tile)}")
            self._print_hand(player)
            choice = input("Call kan? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                print()
                return True
            if choice in ("n", "no"):
                print()
                return False
            print("Please choose y or n.")

# AI GENERATED CODE STARTS

    def get_chii_choice(self, player: Player, discarded_tile: int, options):
        if not player.is_human():
            return None

        if not options:
            return None

        while True:
            self._renderer.separator("CHII")
            print(f"You can chii on {self._renderer.tile_to_text(discarded_tile)}")
            self._print_hand(player)

            for i, option in enumerate(options):
                meld_tiles = sorted(list(option) + [discarded_tile])
                meld_text = " ".join(self._renderer.tile_to_text(tile) for tile in meld_tiles)
                print(f"{i}: {meld_text}")

            choice = input("Choose chii option index (or n to skip): ").strip().lower()
            if choice in ("n", "no"):
                print()
                return None

            if choice.isdigit():
                index = int(choice)
                if 0 <= index < len(options):
                    print()
                    return list(options[index])

            print("Please choose a valid index or n.")

    def _print_hand(self, player: Player):
        col_width = 4  # enough for 'Wh' etc.

        indexes = [str(i).ljust(col_width) for i in range(1, len(player.hand.tiles) + 1)]
        tiles = [self._renderer.tile_to_text(t).ljust(col_width) for t in player.hand.tiles]

        self._renderer.render_melds(player)
        print("Index:", "".join(indexes))
        print("Tile: ", "".join(tiles))

    def _print_discard_hand(self, player: Player, dora_indicators=None):
        col_width = 4

        hand_tiles = list(player.hand.tiles)
        drawn_tile = getattr(player, "last_drawn_tile", None)

        if drawn_tile is not None and drawn_tile in hand_tiles:
            regular_tiles = [tile for tile in hand_tiles if tile != drawn_tile]
        else:
            regular_tiles = hand_tiles
            drawn_tile = None

        indexes = [str(i).ljust(col_width) for i in range(1, len(regular_tiles) + 1)]
        tiles = [self._renderer.tile_to_text(t).ljust(col_width) for t in regular_tiles]

        index_row = "".join(indexes)
        tile_row = "".join(tiles)

        if drawn_tile is not None:
            index_row += "   0"
            tile_row += f"   {self._renderer.tile_to_text(drawn_tile)} (last draw)"

        self._renderer.render_dora_indicators(dora_indicators)
        self._renderer.render_melds(player)
        print("Index:", index_row)
        print("Tile: ", tile_row)

        return regular_tiles, drawn_tile

# AI GENERATED CODE ENDS
