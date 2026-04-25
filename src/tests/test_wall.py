import unittest
from core.wall import Wall


class TestWall(unittest.TestCase):

    def test_live_tiles_decreases_after_draw(self):
        wall = Wall(tiles=None, shuffle=False, dead_wall_size=14)
        self.assertEqual(wall.live_tiles(), 122)
        wall.draw_tile()
        self.assertEqual(wall.live_tiles(), 121)

    def test_draw_tile_returns_next_tile(self):
        wall = Wall(tiles=[0, 1, 2, 3], shuffle=False, dead_wall_size=0)
        tile = wall.draw_tile()
        self.assertEqual(tile, 0)

    def test_draw_tile_error_when_no_tiles_left(self):
        wall = Wall(tiles=[5], shuffle=False, dead_wall_size=0)
        tile = wall.draw_tile()
        self.assertEqual(tile, 5)
        with self.assertRaises(IndexError):
            wall.draw_tile()

    def test_initial_dora_indicator_exists(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        dora = wall.get_dora_indicators()
        self.assertEqual([wall.tiles[-6]], dora)


    def test_initial_uradora_indicator_exists(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        dora = wall.get_uradora_indicators()
        self.assertEqual([wall.tiles[-5]], dora)


    def test_revealing_dora_adds_next_dora_indicator(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        wall.reveal_next_dora()
        dora = wall.get_dora_indicators()
        self.assertEqual([wall.tiles[-6], wall.tiles[-8]], dora)


    def test_revealing_dora_adds_next_uradora_indicator(self):
        wall = Wall(tiles=range(136), shuffle=False, dead_wall_size=14)
        wall.reveal_next_dora()
        dora = wall.get_uradora_indicators()
        self.assertEqual([wall.tiles[-5], wall.tiles[-7]], dora)
