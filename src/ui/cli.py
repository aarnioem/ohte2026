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
            self._render_draw(event, player)
            return

        if event_type == "discard":
            self._render_discard(event)
            return

        if event_type == "tsumo":
            self._render_tsumo(event)
            return

        if event_type == "calls":
            self._render_calls()
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
        print()

    def _render_tsumo(self, event):
        self._separator("TSUMO")
        tile = self._tile_to_text(event["tile"])
        han = event.get("han")
        fu = event.get("fu")

        print(f"Player {event['player']} declares tsumo with {tile} ({han} han, {fu} fu)")
        print()

    def _render_calls(self):
        self._separator("CALLS")
        print("No calls. Next player.")
        print()

    def _render_end(self):
        self._separator("END")
        print("Round ended.")
        print()

    def get_discard_choice(self, player: Player):
        if player.is_human():
            self._separator("CHOOSE DISCARD")
            self._print_hand(player)
            while True:
                try:
                    choice = int(input("Choose discard index: "))
                    if 0 <= choice < len(player.hand.tiles):
                        print()
                        return player.hand.tiles[choice]
                    print("Index out of range.")

                except ValueError:
                    print("Please input a valid number")
        else:
            return random.choice(player.hand.tiles)

    def get_tsumo_choice(self, player: Player, drawn_tile: int):
        if not player.is_human():
            return random.choice([True, False])

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


# AI GENERATED CODE STARTS

    def _print_hand(self, player: Player):
        col_width = 4  # enough for 'Wh' etc.

        indexes = [str(i).ljust(col_width) for i in range(len(player.hand.tiles))]
        tiles = [self._tile_to_text(t).ljust(col_width) for t in player.hand.tiles]

        print("Index:", "".join(indexes))
        print("Tile: ", "".join(tiles))

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

# AI GENERATED CODE ENDS
