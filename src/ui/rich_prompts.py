from core.player import Player
from ui.rich_renderer import RichRenderer
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.panel import Panel
from rich import box

class RichPrompts:
    def __init__(self, renderer: RichRenderer):
        self._renderer = renderer

    def is_human(self) -> bool:
        return False

    def get_discard_choice(self, player: Player, game_state):
        drawn_tile = player.last_drawn_tile

        valid_choices = [str(i) for i in range(1, player.hand.tile_amount())]
        valid_choices.append("0")

        choice = IntPrompt.ask(
            "\n[bold green]Your Turn[/bold green] - Choose discard index", 
            choices=valid_choices,
            console=self._renderer.console
        )

        if drawn_tile is not None and choice == 0:
            return drawn_tile

        if 1 <= choice <= player.hand.tile_amount():
            return player.hand.tiles[choice - 1]


# AI GENERATED STARTS
    def get_tsumo_choice(self, player_data, game_state):
        drawn_tile = int(game_state.get("last_drawn_tile", -1))
        tile_text = self._renderer.tile_to_text(drawn_tile)

        return Confirm.ask(
            f"\n[bold yellow]TSUMO[/bold yellow] - You drew {tile_text}. Declare Tsumo?",
            console=self._renderer.console
        )

    def get_ron_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_pon_choice(self, player_data, game_state):
        discarded_tile = int(game_state.get("last_discarded_tile", -1))
        tile_text = self._renderer.tile_to_text(discarded_tile)

        return Confirm.ask(
            f"\n[bold cyan]PON[/bold cyan] - Call Pon on {tile_text}?",
            console=self._renderer.console
        )

    def get_kan_choice(self, player_data, game_state):
        raise NotImplementedError

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

# AI GENERATED ENDS

    def get_riichi_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_riichi_discard_choice(self, player_data, game_state):
        raise NotImplementedError
