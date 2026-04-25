from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld as MahjongMeld

# AI has been used lot of the scoring functions,
# but it would be difficult to mark each part separately here.
# essentially this module can be considered AI generated. Any docstrings are my own.


def _to_mahjong_melds(melds):
    """Converts a meld object into a mahjong library meld object"""
    if not melds:
        return None

    meld_type_map = {
        "chii": MahjongMeld.CHI,
        "pon": MahjongMeld.PON,
        "kan": MahjongMeld.KAN,
    }

    converted = []
    for meld in melds:
        if isinstance(meld, MahjongMeld):
            converted.append(meld)
            continue

        mapped_type = meld_type_map.get(meld.meld_type)
        if mapped_type is None:
            raise ValueError(f"Unsupported meld type for scoring: {meld.meld_type}")

        converted.append(
            MahjongMeld(
                meld_type=mapped_type,
                tiles=sorted(meld.tiles),
                opened=meld.open_call,
                called_tile=meld.called_tile,
                from_who=meld.from_player,
            )
        )

    return converted


def _meld_tiles_136(melds):
    if not melds:
        return []

    tiles = []
    for meld in melds:
        tiles.extend(meld.tiles)
    return tiles


def calculate_win(tiles_136, win_tile, is_tsumo, *, riichi=False,
                  melds=None, dora_indicators=None, uradora_indicators=None):
    all_tiles = list(tiles_136) + _meld_tiles_136(melds)
    tiles = sorted(all_tiles)
    scoring_melds = _to_mahjong_melds(melds)

    calculator = HandCalculator()
    config = HandConfig(
        is_tsumo=is_tsumo,
        is_riichi=riichi,
        options=OptionalRules(has_open_tanyao=True),
    )

    return calculator.estimate_hand_value(
        tiles=tiles,
        win_tile=win_tile,
        melds=scoring_melds,
        dora_indicators=dora_indicators,
        ura_dora_indicators=uradora_indicators,
        config=config,
    )


def _is_valid_win(result):
    return result.error is None and result.han is not None and result.han > 0


def can_tsumo(tiles_136, drawn_tile, *, riichi=False, melds=None,
              dora_indicators=None, uradora_indicators=None):
    """
    Check whether a 14-tile concealed hand can win by tsumo.
    """

    if not melds and len(tiles_136) != 14:
        return (False, None)

    result = calculate_win(
        tiles_136,
        drawn_tile,
        is_tsumo=True,
        riichi=riichi,
        melds=melds,
        dora_indicators=dora_indicators,
        uradora_indicators=uradora_indicators
    )

    can_win = _is_valid_win(result)
    return (can_win, result)


def can_ron(tiles_136, discarded_tile, *, riichi=False, melds=None,
            dora_indicators=None, uradora_indicators=None):
    """
    Check whether a 13-tile concealed hand can win by Ron.
    """
    if not melds and len(tiles_136) != 13:
        return (False, None)

    result = calculate_win(
        tiles_136 + [discarded_tile],
        discarded_tile,
        is_tsumo=False,
        riichi=riichi,
        melds=melds,
        dora_indicators=dora_indicators,
        uradora_indicators=uradora_indicators
    )

    can_win = _is_valid_win(result)

    return (can_win, result)
