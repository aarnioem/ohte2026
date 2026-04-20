from core.player import Player
import random


class CLI:
    def __init__(self):
        pass


# This rendering method turned out to be really difficult to read in the terminal.
# Clean this up later.

    def render(self, event: dict, player: Player):
        """Render a single round event"""
        event_type = event.get("type")

        if event_type == "draw":
            if "tile" in event and not player.is_human():
                return
            self._render_draw(event, player)
            return

        if event_type == "discard":
            self._render_discard(event)
            return

        if event_type == "tsumo":
            self._render_tsumo(event)
            return

        if event_type == "ron":
            self._render_ron(event)
            return

        if event_type == "calls":
            # this creates unnecessary spam so it's disabled for now
            # self._render_calls()
            return

        if event_type == "pon":
            self._render_pon(event)
            return

        if event_type == "kan":
            self._render_kan(event)
            return

        if event_type == "chii":
            self._render_chii(event)
            return

        if event_type == "end":
            self._render_end()
            return

        print(f"Unknown event: {event}")

    def _render_draw(self, event, player):
        self._separator("DRAW")
        if "tile" in event and player.is_human():
            tile = self._tile_to_text(event["tile"])
            print(f"Player {event['player']} draws {tile}")

        elif "tile" in event:
            print(f"Player {event['player']} draws a tile")
        else:
            print("No live tiles left. Exhaustive draw!")
        print()

    def _render_discard(self, event):
        self._separator("DISCARD")
        tile = self._tile_to_text(event["tile"])
        print(f"Player {event['player']} discards {tile}")
        self._render_player_discards(
            event.get("player"),
            event.get("player_discards", [])
        )
        print()

    def _render_tsumo(self, event):
        self._separator("TSUMO")
        tile = self._tile_to_text(event["tile"])
        han = event.get("han")
        fu = event.get("fu")

        print(f"Player {event['player']} declares tsumo with {tile} ({han} han, {fu} fu)")
        print()

    def _render_ron(self, event):
        self._separator("RON")
        tile = self._tile_to_text(event["tile"])
        han = event.get("han")
        fu = event.get("fu")

        print(f"Player {event['player']} declares ron with {tile} ({han} han, {fu} fu)")
        print()


    def _render_calls(self):
        self._separator("CALLS")
        print("No calls. Next player.")
        print()

    def _render_pon(self, event):
        self._separator("PON")
        tile = self._tile_to_text(event["tile"])
        print(f"Player {event['player']} calls pon on {tile}")
        print()

    def _render_kan(self, event):
        self._separator("KAN")
        tile = self._tile_to_text(event["tile"])
        print(f"Player {event['player']} calls kan on {tile}")
        print()

    def _render_chii(self, event):
        self._separator("CHII")
        tile = self._tile_to_text(event["tile"])
        print(f"Player {event['player']} calls chii on {tile}")
        print()

    def _render_end(self):
        self._separator("END")
        print("Round ended.")
        print()

    def get_discard_choice(self, player: Player):
        if player.is_human():
            self._separator("CHOOSE DISCARD")
            regular_tiles, drawn_tile = self._print_discard_hand(player)

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
            self._separator("TSUMO")
            print(f"You drew {self._tile_to_text(drawn_tile)}")
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
            self._separator("RON")
            print(f"You can ron on {self._tile_to_text(discarded_tile)}")
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
            self._separator("PON")
            print(f"You can pon on {self._tile_to_text(discarded_tile)}")
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
            self._separator("KAN")
            print(f"You can kan on {self._tile_to_text(discarded_tile)}")
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
            self._separator("CHII")
            print(f"You can chii on {self._tile_to_text(discarded_tile)}")
            self._print_hand(player)

            for i, option in enumerate(options):
                meld_tiles = sorted(list(option) + [discarded_tile])
                meld_text = " ".join(self._tile_to_text(tile) for tile in meld_tiles)
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
        tiles = [self._tile_to_text(t).ljust(col_width) for t in player.hand.tiles]

        print("Index:", "".join(indexes))
        print("Tile: ", "".join(tiles))

    def _print_discard_hand(self, player: Player):
        col_width = 4

        hand_tiles = list(player.hand.tiles)
        drawn_tile = getattr(player, "last_drawn_tile", None)

        if drawn_tile is not None and drawn_tile in hand_tiles:
            regular_tiles = [tile for tile in hand_tiles if tile != drawn_tile]
        else:
            regular_tiles = hand_tiles
            drawn_tile = None

        indexes = [str(i).ljust(col_width) for i in range(1, len(regular_tiles) + 1)]
        tiles = [self._tile_to_text(t).ljust(col_width) for t in regular_tiles]

        index_row = "".join(indexes)
        tile_row = "".join(tiles)

        if drawn_tile is not None:
            index_row += "   0"
            tile_row += f"   {self._tile_to_text(drawn_tile)} (last draw)"

        print("Index:", index_row)
        print("Tile: ", tile_row)

        return regular_tiles, drawn_tile

    def _tile_to_text(self, tile_id: int):
        # 136-id -> 34-index (ignore copy)
        tile34 = tile_id // 4

        if tile34 < 9:
            value = tile34 + 1
            return f"{value}m"
        if tile34 < 18:
            value = tile34 - 9 + 1
            return f"{value}p"
        if tile34 < 27:
            value = tile34 - 18 + 1
            return f"{value}s"

        honors = ["E", "S", "W", "N", "Wh", "G", "R"]
        return f"{honors[tile34 - 27]}"

    def _separator(self, label: str = "", width: int = 36):
        if label:
            text = f" {label} "
            line = text.center(width, "-")
        else:
            line = "-" * width
        print(line)

    def _render_player_discards(self, player_index, discards):
        if player_index is None:
            return

        tiles = " ".join(self._tile_to_text(tile) for tile in discards)
        if not tiles:
            tiles = "-"
        print(f"P{player_index} discard pile: {tiles}")

# AI GENERATED CODE ENDS
