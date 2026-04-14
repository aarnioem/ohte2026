from core.player import Player
from core.wall import Wall
from core.scoring import can_tsumo, can_ron
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

    def __init__(self, players, ui, wall: Wall):
        self.players = players
        self.ui = ui
        self.turn_pointer = 0

        self.last_discard = None
        self.last_player_index = None

        self.wall = wall
        self.round_phase = self.PHASE_START

    def play_round(self):
        self._start_round()

        while True:
            event = self.next_phase()
            self.ui.render(event, self._current_player())

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

    def _current_player(self) -> Player:
        return self.players[self.turn_pointer]

    def advance_turn(self):
        self.turn_pointer = (self.turn_pointer + 1) % len(self.players)

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

    def _draw_phase(self) -> dict:
        player = self._current_player()
        tile, end_event = self._draw_tile_or_end(player)
        if end_event is not None:
            return end_event

        if tile is None:
            raise RuntimeError("Tile shouldn't ever be none after a draw")

        tsumo_event = self._try_tsumo(player, tile)
        if tsumo_event is not None:
            return tsumo_event

        self.round_phase = self.PHASE_DISCARD
        return {
            "type": "draw",
            "player": self.turn_pointer,
            "tile": tile
        }


    def _draw_tile_or_end(self, player: Player):
        if self.wall.live_tiles() <= 0:
            self.round_phase = self.PHASE_END
            return None, {
                "type": "draw",
                "player": self.turn_pointer,
            }

        tile = self.wall.draw_tile()
        player.receive_tile(tile)
        return tile, None


    def _try_tsumo(self, player: Player, tile: int):
        tsumo_available, result = can_tsumo(player.hand.tiles, tile, player.riichi)
        if tsumo_available and self.ui.get_tsumo_choice(player, tile):
            self.round_phase = self.PHASE_END

            han = None
            fu = None
            if result is not None:
                han = result.han
                fu = result.fu

            return {
                "type": "tsumo",
                "player": self.turn_pointer,
                "tile": tile,
                "han": han,
                "fu": fu,
            }
        return None


    def _discard_phase(self) -> dict:
        player = self._current_player()

        tile = self.ui.get_discard_choice(player)

        player.discard(tile)
        self.last_discard = tile
        self.last_player_index = self.turn_pointer

        self.round_phase = self.PHASE_CALLS

        return {
            "type": "discard",
            "player": self.turn_pointer,
            "tile": tile,
            "player_discards": player.discards
        }


    # This needs a similar refactor as drawa phase
    def _calls_phase(self) -> dict:
        """Only ron currently"""
        if self.last_discard is None:
            return {"type": "calls"}

        for offset in range(1, 4):
            player_index = (offset + self.turn_pointer) % 4
            ron_player = self.players[player_index]

            ron_available, result = can_ron(
                ron_player.hand.tiles,
                self.last_discard,
                ron_player.riichi
            )

            han = None
            fu = None

            if result is not None:
                han = result.han
                fu = result.fu

            if ron_available and self.ui.get_ron_choice(ron_player, self.last_discard):
                self.round_phase = self.PHASE_END
                return {
                    "type": "ron",
                    "player": player_index,
                    "tile": self.last_discard,
                    "han": han,
                    "fu": fu,
                }

        self.round_phase = self.PHASE_DRAW
        self.advance_turn()

        return {"type": "calls"}

    def _end_phase(self) -> dict:
        return {"type": "end"}
