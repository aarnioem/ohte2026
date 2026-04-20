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
