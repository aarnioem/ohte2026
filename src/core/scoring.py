from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig

def can_tsumo(tiles_136, drawn_tile, riichi=False):
    """
    Check whether a 14-tile concealed hand can win by tsumo.

    Returns a tuple: (can_win: bool, result)
    where result is mahjong library calculation response or None.
    """

    if len(tiles_136) != 14:
        return (False, None)

    tiles = sorted(tiles_136)
    win_tile = drawn_tile

    calculator = HandCalculator()
    config = HandConfig(is_tsumo=True, is_riichi=riichi)

    result = calculator.estimate_hand_value(
        tiles=tiles,
        win_tile=win_tile,
        melds=None,
        dora_indicators=None,
        config=config,
    )

    can_win = result.error is None and result.han is not None and result.han > 0
    return (can_win, result)
