import time
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich import box

class RichRenderer:
    def __init__(self) -> None:
        self.console = Console()
        self.live = None

# AI GENERATED CODE STARTS

    def start_live(self):
        """Starts the live display context."""
        self.live = Live(console=self.console, auto_refresh=False, transient=True, screen=True)
        self.live.start()

    def stop_live(self):
        """Stops the live display context."""
        if self.live:
            self.live.stop()
            self.live = None
            if hasattr(self, '_last_layout'):
                self.console.print(self._last_layout)

# AI GENERATED CODE ENDS


    def create_layout(self) -> Layout:
        """Divides the terminal into a 4-player mahjong table structure."""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=2),
            Layout(name="top", size=12),
            Layout(name="middle"),
            Layout(name="bottom", size=15)
        )

        layout["middle"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="center", ratio=1),
            Layout(name="right", ratio=1)
        )

        return layout

# AI GENERATED CODE STARTS
    def render(self, event: dict, game_state: dict, current_player=None):
        """Fills the layout with data and prints it."""
        layout = self.create_layout()

        dora_indicators = game_state.get('dora_indicators', [])
        dora_text = " ".join([self.tile_to_text(d) for d in dora_indicators]) if dora_indicators else "None"

        event_type = event.get("type", "Unknown").upper()
        
        event_msg = ""
        tile_text = self.tile_to_text(event['tile']) if 'tile' in event else ""
        player_info = f"P{event.get('player', '?')}"

        if event_type == "DRAW":
            if "tile" not in event and event.get("draw_type") != "abortive":
                event_msg = "[bold red]EXHAUSTIVE DRAW[/bold red] - No live tiles left!"
            elif event.get("draw_type") == "abortive":
                event_msg = f"[bold red]ABORTIVE DRAW[/bold red] - {event.get('reason', 'Unknown reason')}"
            else:
                event_msg = f"{player_info} draws."
        
        elif event_type == "DISCARD":
            event_msg = f"{player_info} discards {tile_text}."
        
        elif event_type in ("PON", "KAN", "CHII"):
            event_msg = f"[bold yellow]{player_info} calls {event_type} on {tile_text}![/bold yellow]"

        elif event_type in ("TSUMO", "RON"):
            action_colored = f"[bold magenta]{event_type}[/bold magenta]"
            deal_in = f"P{event.get('deal_in_player', '?')}"
            if event_type == "RON":
                event_msg = f"{player_info} calls {action_colored} on {tile_text} from {deal_in}!"
            else:
                event_msg = f"{player_info} calls {action_colored} on {tile_text}!"
            
            han, fu, cost = event.get("han"), event.get("fu"), event.get("cost")
            if han is not None and fu is not None:
                event_msg += f"\n[bold magenta]{han} Han, {fu} Fu[/bold magenta]"
            if cost is not None:
                if event_type == "RON":
                    event_msg += f"\n{deal_in} pays {cost}"
                else:
                    event_msg += f"\nCost: {cost}"
        
        elif event_type == "CALLS":
            event_msg = "Checking for calls..."

        elif event_type == "END":
            event_msg = "[bold blue]Round Ended[/bold blue]"

        else:
            event_msg = f"Last Action: {event_type}"

        compass_info = f"""[bold yellow]Round Information[/bold yellow]
Wall: {game_state.get('wall_remaining', 70)} tiles left

Dora: {dora_text}

[cyan]{event_msg}[/cyan]"""


        layout["center"].update(Panel(compass_info, title="Center", border_style="cyan", box=box.ASCII))

        discards = game_state.get("discards", {})
        hands = game_state.get("player_hands", {0: [], 1: [], 2: [], 3: []})
        melds = game_state.get("melds", {0: [], 1: [], 2: [], 3: []})

        layout["header"].update(Panel("", title="NotenMahjong", border_style="red", box=box.ASCII))

        layout["top"].update(Panel(f"Discards:\n{self._format_discards(discards.get(2, []))}\n\nMelds:\n{self._format_melds(melds.get(2, []))}\n\nUnknown Tiles: {len(hands.get(2, []))}",
                                   title="Player 2 (Top)",
                                   box=box.ASCII))

        layout["left"].update(Panel(f"Discards:\n{self._format_discards(discards.get(3, []))}\n\nMelds:\n{self._format_melds(melds.get(3, []))}\n\nUnknown Tiles: {len(hands.get(3, []))}",
                                    title="Player 3 (Left)",
                                    box=box.ASCII))

        layout["right"].update(Panel(f"Discards:\n{self._format_discards(discards.get(1, []))}\n\nMelds:\n{self._format_melds(melds.get(1, []))}\n\nUnknown Tiles: {len(hands.get(1, []))}",
                                     title="Player 1 (Right)",
                                     box=box.ASCII))

        discard_text = f"Discards:\n{self._format_discards(discards.get(0, []))}\n\nMelds:\n{self._format_melds(melds.get(0, []))}\n\nHand:"
        
        is_human_turn = game_state.get("turn") == 0
        drawn_tile = current_player.last_drawn_tile if current_player and is_human_turn else None
        
        hand_table = self._format_hand(hands.get(0, []), drawn_tile)

        layout["bottom"].update(Panel(Group(discard_text, hand_table),
                                      title="You (Bottom) - P0",
                                      border_style="bold green",
                                      box=box.ASCII))

        if self.live:
            self._last_layout = layout
            self.live.update(layout, refresh=True)
            time.sleep(0.5)
        else:
            self.console.clear()
            self.console.print(layout)
            time.sleep(0.2)

    def _format_discards(self, discards: list):
        formatted = ""
        for i, tile_id in enumerate(discards):
            formatted += self.tile_to_text(tile_id) + " "
            if (i + 1) % 6 == 0:
                formatted += "\n"

        return formatted.strip()

    def _format_melds(self, melds: list) -> str:
        if not melds:
            return "None"
        formatted = []
        for meld in melds:
            tiles = list(meld.tiles)
            called_tile = getattr(meld, "called_tile", None)
            from_player = getattr(meld, "from_player", None)
            called_used = False
            rendered = []

            for tile in tiles:
                text = self.tile_to_text(tile)
                if called_tile is not None and not called_used and tile == called_tile:
                    text = f"[{text}]"
                    called_used = True
                rendered.append(text)

            prefix = ""
            if from_player is not None:
                prefix = f"[magenta]P{from_player}[/magenta] "

            formatted.append(prefix + "{" + " ".join(rendered) + "}")
        
        return "  ".join(formatted)

    def _format_hand(self, hand_tiles: list, drawn_tile=None):
        if not hand_tiles:
            return ""

        if drawn_tile is not None and drawn_tile in hand_tiles:
            regular_tiles = sorted([tile for tile in hand_tiles if tile != drawn_tile])
        else:
            regular_tiles = sorted(hand_tiles)

        table = Table(show_header=False, show_edge=False, padding=(0, 1), box=box.ASCII)

        for _ in regular_tiles:
            table.add_column(justify="center")

        if drawn_tile is not None:
            table.add_column(justify="center")
            table.add_column(justify="center")

        indices = [f"[dim]{i}[/dim]" for i in range(1, len(regular_tiles)+1)]
        if drawn_tile is not None:
            indices.extend(["", "[yellow]0[/yellow]"])

        # must convert numbers to strings, Table columns will fail if lengths don't match exactly
        table.add_row(*[str(i) for i in indices])

        tiles = [self.tile_to_text(t) for t in regular_tiles]
        if drawn_tile is not None:
            tiles.extend(["", self.tile_to_text(drawn_tile)])

        table.add_row(*[str(t) for t in tiles])

        return table


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
