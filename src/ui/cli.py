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
            if "tile" in event and player.is_human():
                tile = self._tile_to_text(event["tile"])
                print(f"Player {event['player']} draws {tile}")
            elif "tile" in event:
                print(f"Player {event['player']} draws a tile")
            else:
                print("No live tiles left. Exhaustive draw!")
            return

        if event_type == "discard":
            tile = self._tile_to_text(event["tile"])
            print(f"Player {event['player']} discards {tile}")
            return

        if event_type == "calls":
            print("No calls. Next player.")
            return

        if event_type == "end":
            print("Round ended.")
            return

        print(f"Unknown event: {event}")


    # I need to sort this out so I can just choose an index or a tile instead of the tile_id.
    def get_discard_choice(self, player: Player):

        if player.is_human():
            self._print_hand(player)
            while True:
                try:
                    choice = int(input("Choose discard tile id: "))
                    if choice in player.hand.tiles:
                        return choice
                    print("That tile is not in your hand.")

                except ValueError:
                    print("Please input a valid number")
        else:
            return random.choice(player.hand.tiles)


# AI GENERATED CODE STARTS

    def _print_hand(self, player: Player):
        tiles = " ".join(self._tile_to_text(t) for t in player.hand.tiles)
        print(f"Player hand: {tiles}")

    def _tile_to_text(self, tile_id: int):
        # 136-id -> 34-index (ignore copy)
        tile34 = tile_id // 4

        if tile34 < 9:
            value = tile34 + 1
            return f"{value}m[{tile_id}]"
        if tile34 < 18:
            value = tile34 - 9 + 1
            return f"{value}p[{tile_id}]"
        if tile34 < 27:
            value = tile34 - 18 + 1
            return f"{value}s[{tile_id}]"

        honors = ["E", "S", "W", "N", "Wh", "G", "R"]
        return f"{honors[tile34 - 27]}[{tile_id}]"

# AI GENERATED CODE ENDS