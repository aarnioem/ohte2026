import unittest
import pytest
from core.hand import Hand

class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand()
        self.hand.tiles = [2, 4, 5, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]

    def test_adding_tiles_appends(self):
        self.assertEqual(len(self.hand.tiles), 13)
        self.hand.add_tile(1)
        self.assertEqual(len(self.hand.tiles), 14)

    def test_tiles_stay_sorted(self):
        self.assertEqual(self.hand.tiles[0], 2)
        self.hand.add_tile(1)
        self.assertEqual(self.hand.tiles, [1, 2, 4, 5, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112])

    def test_add_tile_already_in_hand(self):
        with pytest.raises(ValueError):
            self.hand.add_tile(90)

    def test_remove_tile_not_in_hand(self):
        with pytest.raises(ValueError):
            self.hand.remove_tile(1)

    def test_remove_tile_in_hand(self):
        tile = self.hand.remove_tile(95)

        self.assertEqual(tile, 95)
        self.assertTrue(tile not in self.hand.tiles)
