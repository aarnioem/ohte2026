from core.player import Player
from ui.prompts import CLIPrompts
from ui.renderer import CLIRenderer


class CLI:
    def __init__(self):
        self._renderer = CLIRenderer()
        self._prompts = CLIPrompts(self._renderer)


    def render(self, event: dict, player: Player):
        """Render a single round event"""
        return self._renderer.render(event, player)


    def get_discard_choice(self, player: Player, dora_indicators=None):
        return self._prompts.get_discard_choice(player, dora_indicators)


    def get_riichi_choice(self, player: Player):
        return self._prompts.get_riichi_choice(player)


    def get_riichi_discard_choice(self, player: Player, valid_discards, dora_indicators=None):
        return self._prompts.get_riichi_discard_choice(player, valid_discards, dora_indicators)


    def get_tsumo_choice(self, player: Player, drawn_tile: int):
        return self._prompts.get_tsumo_choice(player, drawn_tile)


    def get_ron_choice(self, player: Player, discarded_tile: int):
        return self._prompts.get_ron_choice(player, discarded_tile)


    def get_pon_choice(self, player: Player, discarded_tile: int):
        return self._prompts.get_pon_choice(player, discarded_tile)


    def get_kan_choice(self, player: Player, discarded_tile: int):
        return self._prompts.get_kan_choice(player, discarded_tile)


    def get_chii_choice(self, player: Player, discarded_tile: int, options):
        return self._prompts.get_chii_choice(player, discarded_tile, options)
