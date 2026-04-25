import unittest
import pytest
from game.round_manager import RoundManager
from core.player import Player
from core.wall import Wall

class StubUI:
    def __init__(self, tsumo_choice=False, ron_choice=False, discard_index=0):
        self.tsumo_choice = tsumo_choice
        self.ron_choice = ron_choice
        self.discard_index = discard_index
        self.rendered_events = []

    def render(self, event, player):
        self.rendered_events.append((event, player))

    def get_tsumo_choice(self, player, tile):
        return self.tsumo_choice

    def get_ron_choice(self, player, tile):
        return self.ron_choice

    def get_discard_choice(self, player):
        return player.hand.tiles[self.discard_index]


class TestRoundManager(unittest.TestCase):
    def setUp(self):
        self.players = [Player(), Player(), Player(), Player()]
        self.game = RoundManager(self.players, StubUI(), Wall())


    def test_advance_turn(self):
        self.game.turn_pointer = 2
        self.game.advance_turn()
        self.assertEqual(self.game.turn_pointer, 3)
        self.game.advance_turn()
        self.assertEqual(self.game.turn_pointer, 0)


    def test_draw_phase_empty_wall_goes_to_end(self):
        self.game = RoundManager(self.players, StubUI(), Wall(tiles=[], shuffle=False, dead_wall_size=0))
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
        game = RoundManager(self.players, StubUI, wall)

        event = game._draw_phase()
        self.assertEqual(event["type"], "draw")
        self.assertEqual(event["tile"], 0)
