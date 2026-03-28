from core.wall import Wall
from ui.cli import CLI


class RoundManager:
    """
    Handles the game logic for a single round of mahjong.
    """

    # phases of round flow
    PHASE_START = "START"
    PHASE_DEALING = "DEALING"
    PHASE_DRAW = "DRAW"
    PHASE_DISCARD = "DISCARD"
    PHASE_CALLS = "CALLS"
    PHASE_END = "END"

    def __init__(self, players, ui: CLI):
        self.players = players
        self.ui = ui
        self.turn_pointer = 0

        self.wall = Wall()
        self.round_phase = self.PHASE_START

    def play_round(self):
        self._start_round()

        while True:
            event = self.next_phase()
            self.ui.render(event)

            if self.round_phase == self.PHASE_END:
                return

    def next_phase(self) -> dict:
        if self.round_phase == self.PHASE_DRAW:
            return self._draw_phase()

        if self.round_phase == self.PHASE_DISCARD:
            return self._discard_phase()

        if self.round_phase == self.PHASE_CALLS:
            return self._calls_phase()

        if self.round_phase == self.PHASE_END:
            return self._end_phase()

        return {"type": "unknown/error"}


    def _current_player(self):
        return self.players[self.turn_pointer]

    def _start_round(self):
        self.round_phase = self.PHASE_DEALING
        self._initial_dealing()
        self.round_phase = self.PHASE_DRAW

    def _initial_dealing(self):
        """
        Tiles are dealt 4 at a time at first, and then 1 extra for each player
        """
        for _ in range(3):
            for player in self.players:
                for _ in range(4):
                    tile = self.wall.draw_tile()
                    player.hand.add_tile(tile)
        for player in self.players:
            tile = self.wall.draw_tile()
            player.hand.add_tile(tile)

    # THIS NEEDS A TSUMO CHECK
    def _draw_phase(self) -> dict:
        if self.wall.live_tiles() <= 0:
            self.round_phase = self.PHASE_END
            return {
                "type": "draw",
                "player": self.turn_pointer,
                }


        tile = self.wall.draw_tile()
        self.players[self.turn_pointer].receive_tile(tile)

        self.round_phase = self.PHASE_DISCARD
        return {
            "type": "draw",
            "player": self.turn_pointer,
            "tile": tile
            }

    def _discard_phase(self) -> dict:
        player = self._current_player()

        tile = self.ui.get_discard_choice(player)

        player.discard(tile)

        self.round_phase = self.PHASE_CALLS

        return {
            "type": "discard",
            "player": self.turn_pointer,
            "tile": tile
        }

    def _calls_phase(self) -> dict:
        """Calls are unimplemented for now but this is necessary for game flow"""
        self.round_phase = self.PHASE_DRAW
        self.turn_pointer += 1
        self.turn_pointer %= 4

        return {"type": "calls"}

    def _end_phase(self) -> dict:
        return {"type": "end"}
