from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld as MahjongMeld
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

# AI has been used lot of the scoring functions,
# but it would be difficult to mark each part separately here.
# essentially this module can be considered AI generated. Any docstrings are my own.


def _to_mahjong_melds(melds):
    """Converts custom meld objects into mahjong library meld objects

    Args:
        melds (list[Meld]): List of custom meld objects
    
    Raises:
        ValueError: In the case where meld types are not recognised

    Returns:
        list[MahjongMeld]: List of melds as mahjong library meld objects
    """
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


def _tiles_34_counts(tiles_136, melds=None):
    all_tiles = list(tiles_136) + _meld_tiles_136(melds)
    return TilesConverter.to_34_array(all_tiles)


def get_tenpai_discards(tiles_136, *, melds=None):
    """Returns discards that leave the hand in tenpai.

    Args:
        tiles_136 (list[int]): list of tile ids in hand (usually 14 tiles after draw)
        melds (list[Meld], optional): List of melds in the hand. Defaults to None.

    Returns:
        list[int]: Tile ids from the hand that leave the hand in tenpai after discarding.
    """
    if not tiles_136:
        return []

    counts = _tiles_34_counts(tiles_136, melds)
    shanten = Shanten()
    valid = []

    # Try removing one tile from hand
    for tile in tiles_136:
        tile34 = tile // 4
        if counts[tile34] <= 0:
            continue
        counts[tile34] -= 1
        if shanten.calculate_shanten(counts) == 0:
            valid.append(tile)
        counts[tile34] += 1

    return valid


def is_tenpai_after_discard(tiles_136, *, melds=None):
    """Checks whether any discard from the current hand leads to tenpai.

    Args:
        tiles_136 (list[int]): list of tile ids in hand (usually 14 tiles after draw)
        melds (list[Meld], optional): List of melds in the hand. Defaults to None.

    Returns:
        bool: True if discarding one tile can leave the hand in tenpai.
    """
    return len(get_tenpai_discards(tiles_136, melds=melds)) > 0


def calculate_win(tiles_136: list[int], win_tile: int, is_tsumo: bool, *, riichi=False,
                  melds=None, dora_indicators=None, uradora_indicators=None):
    """Calculates the hand value using the mahjong library calculator

    Args:
        tiles_136 (list[int]): list of tile ids in hand
        win_tile (int): tile the win was called on
        is_tsumo (bool): is the winning tile drawn (True) or discarded (False)
        riichi (bool, optional): Is the player in riichi. Defaults to False.
        melds (list[Meld], optional): List of meld objects in the hand. Defaults to None.
        dora_indicators (list[int], optional): Visible dora indicators. Defaults to None.
        uradora_indicators (list[int], optional): Uradora indicators if the player is in riichi.
        Defaults to None.

    Returns:
        HandResponse: Mahjong library result object containing score details.
    """
    all_tiles = list(tiles_136) + _meld_tiles_136(melds)
    tiles = sorted(all_tiles)
    scoring_melds = _to_mahjong_melds(melds)

    calculator = HandCalculator()
    config = HandConfig(
        is_tsumo=is_tsumo,
        is_riichi=riichi,
        options=OptionalRules(has_open_tanyao=True, has_aka_dora=True),
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
    """Checks if the calculated result is a valid win

    Args:
        result (HandResponse): result calculation object

    Returns:
        bool: True if the hand has a valid yaku, otherwise False
    """
    return result.error is None and result.han is not None and result.han > 0


def can_tsumo(tiles_136, drawn_tile, *, riichi=False, melds=None,
              dora_indicators=None, uradora_indicators=None):
    """Checks whether a hand can win by tsumo on a drawn tile.

    Args:
        tiles_136 (list[int]): list of tile ids in hand
        drawn_tile (int): tile id of drawn tile
        riichi (bool, optional): Is the player in riichi. Defaults to False.
        melds (list[Meld], optional): List of melds the player has called. Defaults to None.
        dora_indicators (list[int], optional): List of open dora indicators. Defaults to None.
        uradora_indicators (list[int], optional): List of uradora indicators if the player
            is in riichi. Defaults to None.

    Returns:
        tuple[bool, HandResponse | None]: Tuple where the first part indicates whether tsumo
            is possible and the second part has the mahjong library result object.
            Returns ``(False, None)`` when hand size is invalid.
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
    """Checks whether a hand can win by ron on a discarded tile.

    Args:
        tiles_136 (list[int]): list of tile ids in hand
        discarded_tile (int): tile id of discarded tile
        riichi (bool, optional): Is the player in riichi. Defaults to False.
        melds (list[Meld], optional): List of melds the player has called. Defaults to None.
        dora_indicators (list[int], optional): List of open dora indicators. Defaults to None.
        uradora_indicators (list[int], optional): List of uradora indicators if the player
            is in riichi. Defaults to None.

    Returns:
        tuple[bool, HandResponse | None]: Tuple where the first part indicates whether ron
            is possible and the second part has the mahjong library result object.
            Returns ``(False, None)`` when hand size is invalid.
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
