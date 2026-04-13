from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig

# AI has been used lot of the scoring functions, but it would be difficult to mark each part separately here.


def calculate_win(tiles_136, win_tile, is_tsumo, riichi=False):
    tiles = sorted(tiles_136)

    calculator = HandCalculator()
    config = HandConfig(is_tsumo=is_tsumo, is_riichi=riichi)

    return calculator.estimate_hand_value(
        tiles=tiles,
        win_tile=win_tile,
        melds=None,
        dora_indicators=None,
        config=config,
    )


def _is_valid_win(result):
    return result.error is None and result.han is not None and result.han > 0


def can_tsumo(tiles_136, drawn_tile, riichi=False):
    """
    Check whether a 14-tile concealed hand can win by tsumo.
    """

    if len(tiles_136) != 14:
        return (False, None)

    result = calculate_win(tiles_136, drawn_tile, is_tsumo=True, riichi=riichi)

    can_win = _is_valid_win(result)
    return (can_win, result)


def can_ron(tiles_136, discarded_tile, riichi=False):
    """
    Check whether a 13-tile concealed hand can win by Ron.
    """
    if len(tiles_136) != 13:
        return (False, None)

    result = calculate_win(
        tiles_136 + [discarded_tile],
        discarded_tile,
        is_tsumo=False,
        riichi=riichi,
    )

    can_win = _is_valid_win(result)

    return (can_win, result)
