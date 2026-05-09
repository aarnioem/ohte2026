from ui.rich_renderer import RichRenderer
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.panel import Panel
from rich import box

class RichPrompts:
    def __init__(self, renderer: RichRenderer):
        self._renderer = renderer

    def is_human(self) -> bool:
        return False

    def get_discard_choice(self, player, game_state):
        drawn_tile = player.last_drawn_tile

        hand_tiles = list(player.hand.tiles)
        if drawn_tile is not None and drawn_tile in hand_tiles:
            regular_tiles = sorted([tile for tile in hand_tiles if tile != drawn_tile])
        else:
            regular_tiles = sorted(hand_tiles)

        valid_choices = [str(i) for i in range(1, len(regular_tiles) + 1)]
        if drawn_tile is not None:
            valid_choices.append("0")

        choice = IntPrompt.ask(
            "[bold green]Your Turn[/bold green] - Choose discard index", 
            choices=valid_choices,
            console=self._renderer.console
        )

        if drawn_tile is not None and choice == 0:
            return drawn_tile

        if 1 <= choice <= len(regular_tiles):
            return regular_tiles[choice - 1]


# AI GENERATED STARTS
    def get_tsumo_choice(self, player_data, game_state):
        drawn_tile = int(game_state.get("last_drawn_tile", -1))
        tile_text = self._renderer.tile_to_text(drawn_tile)

        return Confirm.ask(
            f"[bold yellow]TSUMO[/bold yellow] - You drew {tile_text}. Declare Tsumo?",
            console=self._renderer.console
        )

    def get_ron_choice(self, player_data, game_state):
        discarded_tile = int(game_state.get("last_discarded_tile", -1))
        tile_text = self._renderer.tile_to_text(discarded_tile)

        return Confirm.ask(
            f"[bold yellow]RON[/bold yellow] - Call Ron on {tile_text}?",
            console=self._renderer.console
        )

    def get_pon_choice(self, player_data, game_state):
        discarded_tile = int(game_state.get("last_discarded_tile", -1))
        tile_text = self._renderer.tile_to_text(discarded_tile)

        return Confirm.ask(
            f"[bold cyan]PON[/bold cyan] - Call Pon on {tile_text}?",
            console=self._renderer.console
        )

    def get_kan_choice(self, player_data, game_state):
        # For shouminkan (draw-based kan), use last_drawn_tile; for daiminkan, use last_discarded_tile
        call_type = game_state.get("call_type", "daiminkan")
        if call_type == "shouminkan":
            tile_id = int(game_state.get("last_drawn_tile", -1))
            prompt_text = "Call Kan (shouminkan) on"
        else:
            tile_id = int(game_state.get("last_discarded_tile", -1))
            prompt_text = "Call Kan on"

        tile_text = self._renderer.tile_to_text(tile_id)
        return Confirm.ask(
            f"[bold cyan]KAN[/bold cyan] - {prompt_text} {tile_text}?",
            console=self._renderer.console
        )

    def get_chii_choice(self, player_data, game_state):
        discarded_tile = int(game_state.get("last_discarded_tile", -1))
        options = game_state.get("chii_options", [])

        if not options:
            return None

        action_text = f"You can Chii on {self._renderer.tile_to_text(discarded_tile)}:\n"
        for i, option in enumerate(options):
            meld_tiles = sorted(list(option) + [discarded_tile])
            meld_text = " ".join(self._renderer.tile_to_text(t) for t in meld_tiles)
            action_text += f" [[bold cyan]{i}[/bold cyan]] {meld_text}  "

        self._renderer.console.print(Panel(action_text, border_style="cyan", box=box.ASCII))

        valid_choices = [str(i) for i in range(len(options))] + ["n"]

        choice = Prompt.ask(
            "Choose option index (or 'n' to skip)", 
            choices=valid_choices,
            console=self._renderer.console
        ).lower()

        if choice == "n":
            return None
        return list(options[int(choice)])


    def get_riichi_choice(self, player_data, game_state):
        return Confirm.ask(
            "[bold magenta]RIICHI[/bold magenta] - Declare Riichi?",
            console=self._renderer.console
        )

    def get_riichi_discard_choice(self, player_data, game_state):
        valid_discards = game_state.get("valid_discards", [])
        if not valid_discards:
            return None

        drawn_tile = player_data.last_drawn_tile
        valid_set = set(valid_discards)

        valid_choices = ["n"]
        display_indices = []

        # Here we match the sorted behavior of the renderer's hand
        hand_tiles = list(player_data.hand.tiles)
        if drawn_tile is not None and drawn_tile in hand_tiles:
            regular_tiles = sorted([tile for tile in hand_tiles if tile != drawn_tile])
        else:
            regular_tiles = sorted(hand_tiles)

        for i, tile in enumerate(regular_tiles, start=1):
            if tile in valid_set:
                valid_choices.append(str(i))
                display_indices.append(str(i))

        if drawn_tile is not None and drawn_tile in valid_set:
            valid_choices.append("0")
            display_indices.append("0")

        display_str = ", ".join(display_indices) if display_indices else "-"

        choice = Prompt.ask(
            f"[bold magenta]RIICHI[/bold magenta] - Choose discard index ({display_str}) or 'n' to skip",
            choices=valid_choices,
            console=self._renderer.console
        ).lower()

        if choice == "n":
            return None

        choice_int = int(choice)
        if drawn_tile is not None and choice_int == 0:
            return drawn_tile

        if 1 <= choice_int <= len(regular_tiles):
            return regular_tiles[choice_int - 1]

        return None
# AI GENERATED ENDS
