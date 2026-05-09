from core.player import Player
from core.wall import Wall
from core.scoring import can_tsumo, can_ron, get_tenpai_discards, is_tenpai_after_discard
from core.scoring import is_furiten


class RoundManager:
    """Handles the game logic for a single round of mahjong.

    The manager advances through phases (deal, draw, rinshan, discard, calls, end).
    Creates event dictionaries for events that happen in the game, and passes those to the UI.
    """

    PHASE_START = "START"
    PHASE_DEALING = "DEALING"
    PHASE_DRAW = "DRAW"
    PHASE_RINSHAN = "RINSHAN"
    PHASE_DISCARD = "DISCARD"
    PHASE_CALLS = "CALLS"
    PHASE_END = "END"

    def __init__(self, players: list[Player], wall: Wall, dealer_index=0, renderer=None):
        """Initializes the round manager.

        Args:
            players (list[Player]): List of players in seating order.
            wall (Wall): The tile wall for the round.
            renderer: Optional renderer object to display game events.
        """
        self.players = players
        self.dealer_index = dealer_index
        self.turn_pointer = 0
        self.renderer = renderer

        self.last_discard = None
        self.last_player_index = None
        self.pending_dora_reveal = False

        self.riichi_sticks = 0
        self.riichi_declared_by = set()

        self.wall = wall
        self.round_phase = self.PHASE_START

    def play_round(self):
        """Initializes the round and runs the round loop until the round ends.
        """
        self._start_round()

        while True:
            event = self.next_phase()
            if self.renderer:
                self.renderer.render(event, self.get_game_state(), self._current_player())

            if self.round_phase == self.PHASE_END:
                return

# AI generated
    def get_game_state(self) -> dict:
        return {
            "turn": self.turn_pointer,
            "dora_indicators": self.wall.get_dora_indicators(),
            "wall_remaining": self.wall.live_tiles(),
            "discards": {i: p.discards for i, p in enumerate(self.players)},
            "melds": {i: p.hand.melds for i, p in enumerate(self.players)},
            "riichi_declared": self.riichi_declared_by,
            "player_hands": {i: p.hand.tiles for i, p in enumerate(self.players)}
        }
# AI generated ends

    def next_phase(self) -> dict:
        """Advances the round state machine by one phase and returns an event.

        Returns:
            dict: An event dict describing the result of the phase.
        """
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
        """Returns the player whose turn it is currently

        Returns:
            Player: current player
        """
        return self.players[self.turn_pointer]

    def _player_wind(self, player_index):
        """Returns the player's seat wind. East = 27, South = 28, West = 29, North = 30

        Args:
            player_index (int):
        """
        offset = (player_index - self.dealer_index) % 4
        return 27 + offset

    def advance_turn(self):
        """Advances turn_pointer to the next player.
        """
        self.turn_pointer = (self.turn_pointer + 1) % len(self.players)

    def _start_round(self):
        self.round_phase = self.PHASE_DEALING
        self._initial_dealing()
        self.round_phase = self.PHASE_DRAW

    def _initial_dealing(self):
        """Deals initial hands to all players.

        Tiles are dealt 4 at a time for three rounds, then one tile.
        This is the same as real mahjong dealing order.
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
        """Handles a player's draw.

        Draws a tile for the current player or ends the round if the wall is empty.
        If a tsumo is called by the player a tsumo event dict is returned and the round phase is
        set to end. Otherwise returns a draw event dict describing the
        drawn tile and sets the next phase to discard.

        Returns:
            dict: An event dict
                - {"type": "tsumo", ...} when a tsumo is called
                - {"type": "draw", "player": int, "tile": int}
        """
        player = self._current_player()
        tile, end_event = self._draw_tile_or_end(player)
        if end_event is not None:
            return end_event

        if tile is None:
            raise RuntimeError("Tile shouldn't ever be none after a draw")

        tsumo_event = self._try_tsumo(player, tile)
        if tsumo_event is not None:
            return tsumo_event

        if player.ippatsu:
            player.ippatsu = False

        self.round_phase = self.PHASE_DISCARD
        return {
            "type": "draw",
            "player": self.turn_pointer,
            "tile": tile
        }

    def _rinshan_phase(self):
        """Handles a kan replacement draw.

        Draws a rinshan tile (from the dead wall) for the current player, checks for tsumo,
        Returns an event dict. If four kans are called retursn an abortive draw event.
        """
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
        """Draws a tile or ends the game if the wall has run out of tiles.

        Args:
            player (Player): player whose turn it is

        Returns:
            tuple(int | None, dict | None): First case when a tile is drawn successfully,
                second case when the wall is empty.
        """
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
        """Checks if a tsumo is possible for the player and asks if they want to call tsumo.

        Args:
            player (Player): Player who has drawn a tile
            tile (int): Last drawn tile

        Returns:
            dict | None: Returns None if tsumo is not possible or declined.
                Otherwise a tsumo event dict.
        """
        dora_indicators = self.wall.get_dora_indicators()
        tsumo_available, result = can_tsumo(
            player.hand.tiles,
            tile,
            riichi=player.riichi,
            player_wind=self._player_wind(self.turn_pointer),
            melds=player.hand.melds,
            dora_indicators=dora_indicators
        )

        game_state = self.get_game_state()
        game_state["last_drawn_tile"] = tile

        if tsumo_available and player.controller.get_tsumo_choice(player, game_state):
            self.round_phase = self.PHASE_END

            han = None
            fu = None
            cost = None
            if result is not None:
                han = result.han
                fu = result.fu
                cost = result.cost

            self._calculate_tsumo_scores(cost, player)
            self._award_riichi_sticks(player)

            return {
                "type": "tsumo",
                "player": self.turn_pointer,
                "tile": tile,
                "han": han,
                "fu": fu,
                "cost": cost,
            }
        return None

# AI GENERATED
    def _calculate_tsumo_scores(self, cost, player: Player):
        """Calculates and takes the points from other players for a winning tsumo hand.

        Args:
            cost (ScoresResult): Cost from the HandResponse object
            player (Player): Winning player
        """
        if 'additional' in cost:
            # non-dealer win
            for i, p in enumerate(self.players):
                if i == self.turn_pointer:
                    continue
                if i == self.dealer_index:
                    p.score -= cost['main']
                    player.score += cost['main']
                else:
                    p.score -= cost['additional']
                    player.score += cost['additional']
        else:
            # dealer win
            for i, p in enumerate(self.players):
                if i == self.turn_pointer:
                    continue
                p.score -= cost['main']
                player.score += cost['main']
# AI GENERATED ENDS

    def _award_riichi_sticks(self, player: Player):
        """Gives the available riichi sticks to a player and resets riichi stick counter

        Args:
            player (Player): Winning player
        """
        pot = self.riichi_sticks * 1000
        player.score += pot
        self.riichi_sticks = 0

    def _discard_phase(self) -> dict:
        player = self._current_player()

        if player.riichi:
            tile = player.last_drawn_tile
        else:
            dora_indicators = self.wall.get_dora_indicators()
            riichi_tile = self._try_declare_riichi(player, dora_indicators)
            if riichi_tile is None:
                tile = player.controller.get_discard_choice(
                    player, self.get_game_state())
            else:
                tile = riichi_tile

        player.discard(tile)
        self.last_discard = tile
        self.last_player_index = self.turn_pointer

        self.round_phase = self.PHASE_CALLS

        return {
            "type": "discard",
            "player": self.turn_pointer,
            "tile": tile,
            "player_discards": player.discards,
            "player_melds": player.hand.melds
        }

# AI GENERATED STARTS

    def _try_declare_riichi(self, player: Player, dora_indicators=None):
        if player.riichi:
            return None

        if not player.hand.is_closed:
            return None

        if player.score < 1000:
            return None

        if not is_tenpai_after_discard(player.hand.tiles, melds=player.hand.melds):
            return None

        valid_discards = get_tenpai_discards(
            player.hand.tiles, melds=player.hand.melds)

        game_state = self.get_game_state()
        game_state["valid_discards"] = valid_discards
        game_state["dora_indicators"] = dora_indicators

        riichi_tile = player.controller.get_riichi_discard_choice(
            player, game_state)

        if riichi_tile is None:
            return None

        player.riichi = True
        player.ippatsu = True
        player.riichi_declared_tile = riichi_tile
        player.score -= 1000
        self.riichi_sticks += 1
        self.riichi_declared_by.add(self.turn_pointer)
        return riichi_tile

# AI GENERATED ENDS

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

            if is_furiten(ron_player.hand.tiles, ron_player.discards, melds=ron_player.hand.melds):
                continue

            dora_indicators = self.wall.get_dora_indicators()
            ron_available, result = can_ron(
                ron_player.hand.tiles,
                self.last_discard,
                riichi=ron_player.riichi,
                player_wind=self._player_wind(player_index),
                melds=ron_player.hand.melds,
                dora_indicators=dora_indicators
            )

            han = None
            fu = None

            if result is not None:
                han = result.han
                fu = result.fu

            game_state = self.get_game_state()
            game_state["last_discarded_tile"] = self.last_discard

            if ron_available and ron_player.controller.get_ron_choice(ron_player, game_state):
                winning_tile = self.last_discard
                self.round_phase = self.PHASE_END

                # AI generated code
                cost = 0
                if result is not None and result.cost and self.last_player_index is not None:
                    cost = result.cost['main']
                    self.players[self.last_player_index].score -= cost
                    ron_player.score += cost
                # AI generated code ends

                self._award_riichi_sticks(ron_player)

                deal_in_player = self.last_player_index

                self._clear_last_discard_state()
                return {
                    "type": "ron",
                    "player": player_index,
                    "deal_in_player": deal_in_player,
                    "tile": winning_tile,
                    "han": han,
                    "fu": fu,
                    "cost": cost,
                }

        return None

    def _resolve_pon_kan_calls(self):
        for offset in range(1, 4):
            player_index = (offset + self.turn_pointer) % 4
            player = self.players[player_index]
            if player.riichi:
                continue

            kan_event = self._try_open_kan_call(player_index, player)
            if kan_event is not None:
                return kan_event

            pon_event = self._try_pon_call(player_index, player)
            if pon_event is not None:
                return pon_event

        return None

    def _try_open_kan_call(self, player_index: int, player: Player):
        if not player.hand.can_open_kan(self.last_discard):
            return None

        game_state = self.get_game_state()
        game_state["last_discarded_tile"] = self.last_discard

        if not player.controller.get_kan_choice(player, game_state):
            return None

        called_tile = self.last_discard
        player.hand.apply_kan(self.last_discard, self.last_player_index)
        self._set_call_state(
            player_index, self.PHASE_RINSHAN, reveal_dora=True)
        return {
            "type": "kan",
            "player": player_index,
            "tile": called_tile,
        }

    def _try_pon_call(self, player_index: int, player: Player):
        if not player.hand.can_pon(self.last_discard):
            return None

        game_state = self.get_game_state()
        game_state["last_discarded_tile"] = self.last_discard

        if not player.controller.get_pon_choice(player, game_state):
            return None

        called_tile = self.last_discard
        player.hand.apply_pon(self.last_discard, self.last_player_index)
        self._set_call_state(player_index, self.PHASE_DISCARD)
        return {
            "type": "pon",
            "player": player_index,
            "tile": called_tile,
        }

    def _set_call_state(self, player_index: int, next_phase: str, reveal_dora: bool = False):
        self.turn_pointer = player_index
        self.round_phase = next_phase
        self.pending_dora_reveal = reveal_dora
        self._clear_last_discard_state()

    def _resolve_chii_calls(self):
        if self.last_discard is None or self.last_player_index is None:
            return None

        # only next player may call chii
        player_index = (self.last_player_index + 1) % len(self.players)
        chii_player = self.players[player_index]
        if chii_player.riichi:
            return None

        chii_options = chii_player.hand.get_chii_options(self.last_discard)
        if not chii_options:
            return None

        game_state = self.get_game_state()
        game_state["chii_options"] = chii_options
        game_state["last_discarded_tile"] = self.last_discard

        selected_tiles = chii_player.controller.get_chii_choice(
            chii_player, game_state)
        if selected_tiles is None:
            return None

        called_tile = self.last_discard
        from_player = self.last_player_index

        chii_player.hand.apply_chii(
            called_tile, from_player, use_tiles=selected_tiles)
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
        """Clears the information about last discard and the player who last discarded.
        """
        self.last_discard = None
        self.last_player_index = None
# AI GENERATED ENDS

    def _end_phase(self) -> dict:
        """Handles the end phase

        Returns:
            dict: Returns an ending event.
        """
        return {"type": "end"}
