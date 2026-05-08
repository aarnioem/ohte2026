from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

class RichRenderer:
    def __init__(self) -> None:
        self.console = Console()


    def create_layout(self) -> Layout:
        """Divides the terminal into a 4-player mahjong table structure."""
        layout = Layout()

        layout.split_column(
            Layout(name="top", size=7),
            Layout(name="middle"),
            Layout(name="bottom", size=7)
        )

        layout["middle"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="center", ratio=1),
            Layout(name="right", ratio=1)
        )

        return layout

    def render(self, event: dict, game_state: dict, current_player):
        """Fills the layout with data and prints it."""
        layout = self.create_layout()

        event_type = event.get("type", "Unknown").upper()
        event_msg = f"Last Action: {event_type} by P{event.get('player', '?')}"
        if "tile" in event:
            event_msg += f"\nTile ID: {event['tile']}"

# AI GENERATED CODE STARTS
        compass_info = f"[bold yellow]Round Information[/bold yellow]\nWall: {game_state.get('wall_remaining', 70)} tiles left\nDora: 🀫\n\n[cyan]{event_msg}[/cyan]"
# AI GENERATED CODE ends
        layout["center"].update(Panel(compass_info, title="Center", border_style="cyan"))

        discards = game_state.get("discards", {})
        hands = game_state.get("player_hands", {0: [], 1: [], 2: [], 3: []})


        layout["bottom"].update(Panel(f"Discards:\n{self._format_discards(discards.get(0, []))}\n\nHand:\n{self._format_hand(hands.get(0, []))}", title="You (Bottom) - P0", border_style="bold green"))
        layout["right"].update(Panel(f"Discards:\n{self._format_discards(discards.get(1, []))}\n\nUnknown Tiles: {len(hands.get(1, []))}", title="Player 1 (Right)"))
        layout["top"].update(Panel(f"Discards:\n{self._format_discards(discards.get(2, []))}\n\nUnknown Tiles: {len(hands.get(2, []))}", title="Player 2 (Top)"))
        layout["left"].update(Panel(f"Discards:\n{self._format_discards(discards.get(3, []))}\n\nUnknown Tiles: {len(hands.get(3, []))}", title="Player 3 (Left)"))

        self.console.clear()
        self.console.print(layout)

# AI GENERATED CODE STARTS
    def _format_discards(self, discards: list):
        formatted = ""
        for i, tile_id in enumerate(discards):
            formatted += self.tile_to_text(tile_id) + " "
            if (i + 1) % 6 == 0:
                formatted += "\n"

        return formatted.strip()

    def _format_hand(self, hand_tiles: list):
        if not hand_tiles:
            return ""
        sorted_tiles = sorted(hand_tiles)
        formatted = " ".join([self.tile_to_text(t) for t in sorted_tiles])
        return formatted


    def tile_to_text(self, tile_id: int):
        tile34 = tile_id // 4

        # Red 5s are brightly colored
        if tile_id == 16:
            return "[bold red]r5m[/bold red]"
        if tile_id == 52:
            return "[bold red]r5p[/bold red]"
        if tile_id == 88:
            return "[bold red]r5s[/bold red]"

        # Manzu (Characters) -> Red
        if tile34 < 9:
            value = tile34 + 1
            return f"[red]{value}m[/red]"
        # Pinzu (Circles) -> Cyan/Blue
        if tile34 < 18:
            value = tile34 - 9 + 1
            return f"[cyan]{value}p[/cyan]"
        # Souzu (Bamboo) -> Green
        if tile34 < 27:
            value = tile34 - 18 + 1
            return f"[green]{value}s[/green]"

        # Honors -> White/Yellow
        honors = ["E", "S", "W", "N", "Wh", "G", "R"]
        return f"[yellow]{honors[tile34 - 27]}[/yellow]"

# AI GENERATED CODE ENDS

if __name__ == "__main__":
    renderer = RichRenderer()
    dummy_state = {
        "wall_remaining": 69, 
        "discards": {0: [1,2,3], 1: [4,5], 2: [], 3: [7]},
        "player_hands": {0: [16, 20, 24, 0, 1, 2, 9, 10, 11, 50, 66, 116, 89]}
    }
    dummy_event = {"type": "discard", "player": 1, "tile": 34}
    renderer.render(dummy_event, dummy_state, current_player=None)
