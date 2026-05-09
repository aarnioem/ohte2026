import random
from ui.rich_renderer import RichRenderer
from ui.rich_prompts import RichPrompts

# AI generated boilerplate
class PlayerController:
    """Base controller interface for a player.
    """
    def is_human(self) -> bool:
        return False

    def get_discard_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_tsumo_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_ron_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_pon_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_kan_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_riichi_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_riichi_discard_choice(self, player_data, game_state):
        raise NotImplementedError

    def get_chii_choice(self, player_data, game_state):
        raise NotImplementedError
# AI generated ends


class AIController(PlayerController):
    """Simple AI controller that acts automatically without UI prompts."""

    def __init__(self) -> None:
        pass

    def is_human(self) -> bool:
        return False

    def get_discard_choice(self, player_data, game_state):
        return random.choice(player_data.hand.tiles)

    def get_tsumo_choice(self, player_data, game_state):
        return True

    def get_ron_choice(self, player_data, game_state):
        return True

    def get_pon_choice(self, player_data, game_state):
        return False

    def get_kan_choice(self, player_data, game_state):
        return False

    def get_riichi_choice(self, player_data, game_state):
        return False

    def get_riichi_discard_choice(self, player_data, game_state):
        return None

    def get_chii_choice(self, player_data, game_state):
        return None

class RichController(PlayerController):
    """Controller that asks a human using a CLI that uses Rich"""

# AI GENERATED CODE STARTS

    def __init__(self, renderer: RichRenderer) -> None:
        self.renderer = renderer
        self.prompts = RichPrompts(self.renderer)

    def is_human(self) -> bool:
        return True

    def get_discard_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_discard_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_tsumo_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_tsumo_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_ron_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_ron_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_pon_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_pon_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_kan_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_kan_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_riichi_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_riichi_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_riichi_discard_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_riichi_discard_choice(player_data, game_state)
        self.renderer.start_live()
        return choice

    def get_chii_choice(self, player_data, game_state):
        self.renderer.stop_live()
        choice = self.prompts.get_chii_choice(player_data, game_state)
        self.renderer.start_live()
        return choice
# AI GENERATED CODE ENDS
