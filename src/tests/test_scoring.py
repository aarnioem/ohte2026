import unittest
import pytest
from core.scoring import can_tsumo, can_ron, calculate_win, get_winning_tiles, is_furiten
from core.melds import Meld


# TSUMO

def test_can_tsumo_is_false_with_too_few_tiles():
    tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # 13 tiles

    can_win, result = can_tsumo(tiles, 13)

    assert can_win is False
    assert result is None


def test_can_closed_tsumo_with_no_other_yaku():
    # 123m 234p 456p 789s WW
    tiles = [0, 4, 8, 40, 44, 48, 49, 53, 56, 96, 100, 104, 116, 117]

    can_win, result = can_tsumo(tiles, 117)

    assert can_win is True
    assert result is not None and result.han == 1


def test_can_open_tsumo_with_tanyao():
    # 234m 234p 456p 888s 66s
    tiles = [4, 8, 12, 40, 44, 48, 49, 53, 56, 92, 93]
    melds = [Meld(called_tile=100, tiles=[100, 101, 102],
                  from_player=1, meld_type="pon", open_call=True)]

    can_win, result = can_tsumo(tiles, 93, riichi=False, melds=melds)

    assert can_win is True
    assert result is not None and result.han == 1


# RON

def test_can_ron_is_false_with_too_few_tiles():
    tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 12 tiles
    can_win, result = can_ron(tiles, 12)

    assert can_win is False
    assert result is None

def test_can_open_ron_with_tanyao():
    # 234m 234p 456p 888s 66s
    tiles = [4, 8, 12, 40, 44, 48, 49, 53, 56, 92]
    melds = [Meld(called_tile=100, tiles=[100, 101, 102],
                  from_player=1, meld_type="pon", open_call=True)]

    can_win, result = can_ron(tiles, 93, riichi=False, melds=melds)

    assert can_win is True
    assert result is not None and result.han == 1

def test_can_ron_with_no_yaku_returns_false():
    # 123m 234p 456p 789s WW
    tiles = [0, 4, 8, 40, 44, 48, 49, 52, 56, 96, 100, 104, 116]

    can_win, result = can_ron(tiles, 117)

    assert can_win is False
    assert result is not None and result.han is None


def test_calculate_win_tsumo_with_valid_hand():
    # 111m 111p 111s 789s SS
    # tsumo 1 han, chanta 2 han, sanankou 2 han, sanshoku doukou 2 han = 7 han
    tiles = [1, 2, 3, 36, 37, 38, 72, 73, 74, 99, 102, 107, 112, 113]

    result = calculate_win(tiles, 113, True)

    assert result.error is None
    assert result.han == 7


def test_calculate_win_tsumo_with_valid_hand_and_3_dora():
    # 111m 111p 111s 789s SS
    # tsumo 1 han, chanta 2 han, sanankou 2 han, sanshoku doukou 2 han, 3 dora = 10 han
    # dora indicator is 9m which makes 1m dora 
    tiles = [1, 2, 3, 36, 37, 38, 72, 73, 74, 99, 102, 107, 112, 113]

    result = calculate_win(tiles, 113, True, dora_indicators=[32])

    assert result.error is None
    assert result.han == 10


def test_calculate_ron_with_red_5_and_red5s_dora():
    # P2 [r5m {5m} 5m] P2 [7p {7p} 7p], 6p6p6p, 8p8p, 6s7s, winning tile 5s
    melds = [
        Meld(called_tile=17, tiles=[16, 17, 18], from_player=2, meld_type="pon", open_call=True),
        Meld(called_tile=60, tiles=[60, 61, 62], from_player=2, meld_type="pon", open_call=True),
    ]

    tiles = [56, 57, 58, 64, 65, 92, 96, 89]

    result = calculate_win(
        tiles,
        89,
        False,
        melds=melds,
        dora_indicators=[88],
    )

    assert result.error is None
    assert result.han == 3
    assert result.fu == 30


def test_get_winning_tiles():
    # 123m 234p 456p 78s WW
    # Wait tiles are 6s and 9s
    tiles = [0, 4, 8, 40, 44, 48, 49, 52, 56, 96, 100, 116, 117]

    expected = [23, 26]

    result = get_winning_tiles(tiles)

    assert expected == result

def test_is_furiten_when_in_furiten():
    tiles = [0, 4, 8, 40, 44, 48, 49, 52, 56, 96, 100, 116, 117]
    discards = [104]

    assert is_furiten(tiles, discards, melds=None)

def test_is_furiten_when_not_in_furiten():
    tiles = [0, 4, 8, 40, 44, 48, 49, 52, 56, 96, 100, 116, 117]
    discards = [15]

    assert not is_furiten(tiles, discards, melds=None)
