from core.player import Player
from core.wall import Wall
from core.scoring import can_tsumo, can_ron


class RoundManager:
    """
    Handles the game logic for a single round of mahjong.
    """

    # phases of round flow
    PHASE_START = "START"
    PHASE_DEALING = "DEALING"
    PHASE_DRAW = "DRAW"
    PHASE_RINSHAN = "RINSHAN"
    PHASE_DISCARD = "DISCARD"
    PHASE_CALLS = "CALLS"
    PHASE_END = "END"

    def __init__(self, players: list[Player], ui, wall: Wall):
        self.players = players
        self.ui = ui
        self.turn_pointer = 0

        self.last_discard = None
        self.last_player_index = None
        self.pending_dora_reveal = False

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

        if self.round_phase == self.PHASE_RINSHAN:
            return self._rinshan_phase()

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

    def _rinshan_phase(self):
        player = self._current_player()
        rinshan_draw = self.wall.draw_rinshan_tile()
        player.receive_tile(rinshan_draw)
        tsumo_event = self._try_tsumo(player, rinshan_draw)
        if tsumo_event is not None:
            return tsumo_event

        if self.wall.kan_counter >= 4:
            self.round_phase = self.PHASE_END
            return {
                "type": "draw",
                "draw_type": "abortive",
                "reason": "four_kan"
            }

        self.round_phase = self.PHASE_DISCARD
        return {
            "type": "draw",
            "player": self.turn_pointer,
            "tile": rinshan_draw
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
        dora_indicators = self.wall.get_dora_indicators()
        tsumo_available, result = can_tsumo(
            player.hand.tiles,
            tile,
            riichi=player.riichi,
            melds=player.hand.melds,
            dora_indicators=dora_indicators
        )
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

        dora_indicators = self.wall.get_dora_indicators()
        tile = self.ui.get_discard_choice(player, dora_indicators)

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


    def _calls_phase(self) -> dict:
        """Resolve calls in priority order: ron -> kan/pon -> chii."""
        if self.last_discard is None:
            return {"type": "calls"}

        ron_event = self._resolve_ron_calls()
        if ron_event is not None:
            return ron_event

        if self.pending_dora_reveal:
            self.wall.reveal_next_dora()
            self.pending_dora_reveal = False

        pon_kan_event = self._resolve_pon_kan_calls()
        if pon_kan_event is not None:
            return pon_kan_event

        chii_event = self._resolve_chii_calls()
        if chii_event is not None:
            return chii_event

        self.round_phase = self.PHASE_DRAW
        self.advance_turn()
        self._clear_last_discard_state()

        return {"type": "calls"}

    def _resolve_ron_calls(self):
        for offset in range(1, 4):
            player_index = (offset + self.turn_pointer) % 4
            ron_player = self.players[player_index]

            dora_indicators=self.wall.get_dora_indicators()
            ron_available, result = can_ron(
                ron_player.hand.tiles,
                self.last_discard,
                riichi=ron_player.riichi,
                melds=ron_player.hand.melds,
                dora_indicators=dora_indicators
            )

            han = None
            fu = None

            if result is not None:
                han = result.han
                fu = result.fu

            if ron_available and self.ui.get_ron_choice(ron_player, self.last_discard):
                winning_tile = self.last_discard
                self.round_phase = self.PHASE_END
                self._clear_last_discard_state()
                return {
                    "type": "ron",
                    "player": player_index,
                    "tile": winning_tile,
                    "han": han,
                    "fu": fu,
                }

        return None

    def _resolve_pon_kan_calls(self):
        for offset in range(1, 4):
            player_index = (offset + self.turn_pointer) % 4
            pon_kan_player = self.players[player_index]

            if pon_kan_player.hand.can_open_kan(self.last_discard):
                if self.ui.get_kan_choice(pon_kan_player, self.last_discard):
                    called_tile = self.last_discard
                    pon_kan_player.hand.apply_kan(self.last_discard, self.last_player_index)
                    self.turn_pointer = player_index
                    self.round_phase = self.PHASE_RINSHAN
                    self.pending_dora_reveal = True
                    self._clear_last_discard_state()
                    return {
                        "type": "kan",
                        "player": player_index,
                        "tile": called_tile,
                    }

            if pon_kan_player.hand.can_pon(self.last_discard):
                if self.ui.get_pon_choice(pon_kan_player, self.last_discard):
                    called_tile = self.last_discard
                    pon_kan_player.hand.apply_pon(self.last_discard, self.last_player_index)
                    self.turn_pointer = player_index
                    self.round_phase = self.PHASE_DISCARD
                    self._clear_last_discard_state()
                    return {
                        "type": "pon",
                        "player": player_index,
                        "tile": called_tile,
                    }

        return None


    def _resolve_chii_calls(self):
        if self.last_discard is None or self.last_player_index is None:
            return None

        # only next player may call chii
        player_index = (self.last_player_index + 1) % len(self.players)
        chii_player = self.players[player_index]

        chii_options = chii_player.hand.get_chii_options(self.last_discard)
        if not chii_options:
            return None

        selected_tiles = self.ui.get_chii_choice(
            chii_player,
            self.last_discard,
            chii_options,
        )
        if selected_tiles is None:
            return None

        called_tile = self.last_discard
        from_player = self.last_player_index

        chii_player.hand.apply_chii(called_tile, from_player, use_tiles=selected_tiles)
        self.turn_pointer = player_index
        self.round_phase = self.PHASE_DISCARD
        self._clear_last_discard_state()

        return {
            "type": "chii",
            "player": player_index,
            "tile": called_tile,
        }


# AI GENERATED (instances of this elsewhere in the code were recommended by AI as well)
    def _clear_last_discard_state(self):
        self.last_discard = None
        self.last_player_index = None
# AI GENERATED ENDS

    def _end_phase(self) -> dict:
        return {"type": "end"}
