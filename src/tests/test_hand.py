import unittest
import pytest
from core.hand import Hand
from core.melds import Meld


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
        self.assertEqual(self.hand.tiles, [
                         1, 2, 4, 5, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112])

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

    def test_can_pon(self):
        # hand has two 1m tiles, pon for 1m
        self.hand.tiles = [0, 1, 5, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 2
        self.assertTrue(self.hand.can_pon(discard_tile))

    def test_can_not_pon(self):
        self.hand.tiles = [0, 5, 12, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 2
        self.assertFalse(self.hand.can_pon(discard_tile))

    def test_can_chii(self):
        # hand has 1m and 2m, chii for 3m
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 8
        self.assertTrue(self.hand.can_chii(discard_tile))

    def test_can_not_chii(self):
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 112
        self.assertFalse(self.hand.can_chii(discard_tile))

    def test_can_open_kan(self):
        # three 1m, open kan for 1m
        self.hand.tiles = [0, 1, 2, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 3
        self.assertTrue(self.hand.can_open_kan(discard_tile))

    def test_apply_pon(self):
        # hand has two 1m tiles, pon for 1m
        self.hand.tiles = [0, 1, 5, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 2
        expected_meld = Meld(called_tile=2, tiles=[0, 1, 2],
                             from_player=0, meld_type="pon", open_call=True)
        meld = self.hand.apply_pon(discard_tile, from_player=0)
        self.assertEqual(meld, expected_meld)
        self.assertTrue(meld in self.hand.melds)

    def test_apply_chii(self):
        # hand has 1m and 2m, chii for 3m
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 8
        expected_meld = Meld(called_tile=8, tiles=[0, 4, 8],
                             from_player=0, meld_type="chii", open_call=True)
        meld = self.hand.apply_chii(discard_tile, from_player=0, use_tiles=[0, 4])
        self.assertEqual(meld, expected_meld)
        self.assertTrue(meld in self.hand.melds)

    def test_apply_invalid_chii_pattern(self):
        # hand has 1m and 2m, chii for 3m
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 113
        with pytest.raises(ValueError):
            self.hand.apply_chii(discard_tile, from_player=0, use_tiles=[0, 4])

    def test_apply_chii_no_tiles_raises(self):
        # hand has 1m and 2m, chii for 3m
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 8
        with pytest.raises(ValueError):
            self.hand.apply_chii(discard_tile, from_player=0, use_tiles=[])

    def test_apply_chii_wrong_tiles_raises(self):
        # hand has 1m and 2m, chii for 3m
        self.hand.tiles = [0, 1, 4, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 8
        with pytest.raises(ValueError):
            self.hand.apply_chii(discard_tile, from_player=0, use_tiles=[90, 95])

    def test_apply_kan(self):
        # three 1m, open kan for 1m
        self.hand.tiles = [0, 1, 2, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        discard_tile = 3
        expected_meld = Meld(called_tile=3, tiles=[0, 1, 2, 3],
                             from_player=0, meld_type="kan", open_call=True)
        meld = self.hand.apply_kan(discard_tile, from_player=0)
        self.assertEqual(meld, expected_meld)
        self.assertTrue(meld in self.hand.melds)

    def test_get_chii_options_with_none_available(self):
        self.hand.tiles = [0, 1, 2, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        options = self.hand.get_chii_options(135)

        self.assertEqual(options, [])

    def test_get_chii_options_available(self):
        self.hand.tiles = [0, 4, 20, 22, 30, 31, 50, 66, 70, 79, 90, 95, 112]
        options = self.hand.get_chii_options(8)

        self.assertEqual(options, [[0, 4]])
