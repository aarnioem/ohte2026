import unittest
from unittest.mock import patch
from game.round_manager import RoundManager
from core.player import Player
from core.melds import Meld
from core.wall import Wall
from ui.controller import AIController

class StubController(AIController):
    def __init__(self, *, kan_choice=False, shouminkan_choice=None,
                 pon_choice=False, discard_choice=0) -> None:
        super().__init__()
        self.kan_choice = kan_choice
        self.shouminkan_choice = shouminkan_choice
        self.pon_choice = pon_choice
        self.discard_choice = discard_choice

    def get_kan_choice(self, player_data, game_state):
        if game_state.get("call_type") == "shouminkan" and self.shouminkan_choice is not None:
            return self.shouminkan_choice
        return self.kan_choice

    def get_pon_choice(self, player_data, game_state):
        return self.pon_choice
    
    def get_discard_choice(self, player_data, game_state):
        return self.discard_choice

class TestRoundManager(unittest.TestCase):
    def setUp(self):
        self.players = [Player(AIController()), Player(AIController()), Player(AIController()), Player(AIController())]
        self.game = RoundManager(self.players, Wall())


    def test_advance_turn(self):
        self.game.turn_pointer = 2
        self.game.advance_turn()
        self.assertEqual(self.game.turn_pointer, 3)
        self.game.advance_turn()
        self.assertEqual(self.game.turn_pointer, 0)


    def test_draw_phase_empty_wall_goes_to_end(self):
        self.game = RoundManager(self.players, Wall(tiles=[], shuffle=False, dead_wall_size=0))
        self.game._draw_phase()
        self.assertEqual(self.game.round_phase, self.game.PHASE_END)


    def test_start_round_deals_correct_amount_of_tiles_to_players(self):
        self.game._start_round()
        player0 = self.game.players[0]
        player1 = self.game.players[1]
        player2 = self.game.players[2]
        player3 = self.game.players[3]
        self.assertEqual(player0.hand.tile_amount(), 13)
        self.assertEqual(player1.hand.tile_amount(), 13)
        self.assertEqual(player2.hand.tile_amount(), 13)
        self.assertEqual(player3.hand.tile_amount(), 13)


    def test_start_round_ends_in_draw_phase(self):
        self.game._start_round()
        self.assertEqual(self.game.round_phase, self.game.PHASE_DRAW)


    def test_draw_phase_returns_correct_draw_event(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall)

        event = game._draw_phase()
        self.assertEqual(event["type"], "draw")
        self.assertEqual(event["tile"], 0)


    def test_kan_call_returns_correct_event_and_goes_to_correct_phase(self):
        controller = StubController(kan_choice=True)
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        self.players[1].hand.tiles = [0, 1, 2, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        self.players[1].controller = controller
        game = RoundManager(self.players, wall=wall)
        game.turn_pointer = 0
        game.last_discard = 3
        event = game._resolve_pon_kan_calls()

        self.assertIsNotNone(event)
        assert event is not None
        self.assertEqual(event["type"], "kan")
        self.assertEqual(event["player"], 1)
        self.assertEqual(game.turn_pointer, 1)
        self.assertEqual(game.round_phase, game.PHASE_RINSHAN)


    def test_try_pon_call_returns_correct_event(self):
        controller = StubController(pon_choice=True)
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall=wall)

        game.turn_pointer = 0
        game.last_discard = 0
        game.last_player_index = 0

        pon_player_index = 1
        pon_player = game.players[pon_player_index]
        pon_player.controller = controller

        # pon on 1m (IDs 0, 1 and 2)
        pon_player.hand.tiles = [1, 2, 8, 12, 16, 20, 24, 28, 40, 44, 48, 52, 56]

        event = game._try_pon_call(pon_player_index, pon_player)

        expected_event = {
                "type": "pon",
                "player": 1,
                "tile": 0,
                }

        self.assertEqual(event, expected_event)


    def test_four_kans_abort(self):
        self.game.wall.kan_counter = 3
        self.game.round_phase = self.game.PHASE_RINSHAN

        event = self.game._rinshan_phase()
        self.assertEqual(event["type"], "draw")
        self.assertEqual(event["draw_type"], "abortive")
        self.assertEqual(event["reason"], "four_kan")


    def test_rinshan_phase_goes_to_draw_phase(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall)

        event = game._rinshan_phase()

        self.assertEqual(event["type"], "draw")
        self.assertEqual(event["tile"], 134)
        self.assertEqual(game.round_phase, game.PHASE_DISCARD)
        self.assertEqual(game.wall.kan_counter, 1)


    def test_try_tsumo_returns_correct_end_event(self):
        # test hand is same as the one in scoring tests, 7 han
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall)
        player = game.players[0]
        player.hand.tiles = [1, 2, 3, 36, 37, 38, 72, 73, 74, 99, 102, 107, 112, 113]
        event = game._try_tsumo(player, 113)

        expected_result = {
                "type": "tsumo",
                "player": 0,
                "tile": 113,
                "han": 7,
                "fu": 50,
                "cost": {'main': 6000, 'additional': 6000, 'main_bonus': 0, 'additional_bonus': 0, 'kyoutaku_bonus': 0, 'total': 18000, 'yaku_level': 'haneman'}
            }

        self.assertEqual(game.round_phase, game.PHASE_END)
        self.assertEqual(event, expected_result)


    def test_resolve_ron_calls_returns_correct_end_event(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall)

        game.turn_pointer = 0
        game.last_discard = 113
        game.last_player_index = 0

        ron_player = game.players[1]
        ron_player.hand.tiles = [1, 2, 3, 36, 37, 38, 72, 73, 74, 99, 102, 107, 112]

        event = game._resolve_ron_calls()

        expected_result = {
                "type": "ron",
                "player": 1,
                "deal_in_player": 0,
                "tile": 113,
                "han": 6,
                "fu": 60,
                "cost": 12000,
            }

        self.assertEqual(game.round_phase, game.PHASE_END)
        self.assertEqual(event, expected_result)


    def test_next_phase_calls_draw_phase_handler(self):
        self.game.round_phase = self.game.PHASE_DRAW
        expected = "draw"

        with patch.object(self.game, "_draw_phase", return_value=expected) as draw_phase:
            event = self.game.next_phase()

        draw_phase.assert_called_once_with()
        self.assertEqual(event, expected)


    def test_next_phase_calls_rinshan_phase_handler(self):
        self.game.round_phase = self.game.PHASE_RINSHAN
        expected = "rinshan"

        with patch.object(self.game, "_rinshan_phase", return_value=expected) as rinshan_phase:
            event = self.game.next_phase()

        rinshan_phase.assert_called_once_with()
        self.assertEqual(event, expected)


    def test_next_phase_calls_discard_phase_handler(self):
        self.game.round_phase = self.game.PHASE_DISCARD
        expected = "discard"

        with patch.object(self.game, "_discard_phase", return_value=expected) as discard_phase:
            event = self.game.next_phase()

        discard_phase.assert_called_once_with()
        self.assertEqual(event, expected)


    def test_next_phase_calls_calls_phase_handler(self):
        self.game.round_phase = self.game.PHASE_CALLS
        expected = "calls"

        with patch.object(self.game, "_calls_phase", return_value=expected) as calls_phase:
            event = self.game.next_phase()

        calls_phase.assert_called_once_with()
        self.assertEqual(event, expected)


    def test_next_phase_calls_end_phase_handler(self):
        self.game.round_phase = self.game.PHASE_END
        expected = "end"

        with patch.object(self.game, "_end_phase", return_value=expected) as end_phase:
            event = self.game.next_phase()

        end_phase.assert_called_once_with()
        self.assertEqual(event, expected)


    def test_next_phase_returns_unknown_error_for_unknown_phase(self):
        self.game.round_phase = "UNKNOWN_PHASE"
        self.assertEqual(self.game.next_phase(), {"type": "unknown/error"})


    def test_discard_phase_returns_correct_event(self):
        self.game.players[0].controller = StubController(discard_choice=1)
        self.game.players[0].hand.tiles = [1, 2, 3, 36, 37, 38, 72, 73, 74, 99, 102, 107, 112, 134]

        expected = { 
            "type": "discard", 
            "player": 0, 
            "tile": 1, 
            "player_discards": [1], 
            "player_melds": []
        }

        result = self.game._discard_phase()

        self.assertEqual(result, expected)


    def test_draw_phase_performs_shouminkan_when_accepted(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        game = RoundManager(self.players, wall)
        player = game.players[0]
        player.controller = StubController(shouminkan_choice=True)


        player.hand.tiles = [36, 37, 38, 72, 73, 74, 99, 102, 107, 112]
        # pon on 1m, tile_id 3 fills out the kan
        player.hand.melds = [
            Meld(
                called_tile=0,
                tiles=[0, 1, 2],
                from_player=1,
                meld_type="pon",
                open_call=True,
            )
        ]
        player.hand.is_closed = False

        game.turn_pointer = 0
        game.round_phase = game.PHASE_DRAW
        game.wall.draw_pointer = 3

        event = game._draw_phase()

        expected = {
            "type": "kan",
            "player": 0,
            "tile": 3,
            "call_type": "shouminkan",
        }

        self.assertEqual(event, expected)
        self.assertEqual(player.hand.melds[0].meld_type, "kan")
        self.assertEqual(player.hand.melds[0].tiles, [0, 1, 2, 3])
