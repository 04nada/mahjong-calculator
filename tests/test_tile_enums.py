import pytest

from mahjong import *

# ---
@pytest.mark.parametrize('e, val', [
    (TileSuit.MAN, 0),
    (TileSuit.PIN, 9),
    (TileSuit.SOU, 18),
    (Wind.EAST, 1),
    (Wind.SOUTH, 2),
    (Wind.WEST, 3),
    (Wind.NORTH, 4),
    (Dragon.WHITE, 5),
    (Dragon.GREEN, 6),
    (Dragon.RED, 7),
])
def test_tile_enum_values(e: TileSuit | Wind | Dragon, val: int):
    assert e.value == val

@pytest.mark.parametrize('e, val', [
    (TileSuit.MAN, 'MAN'),
    (TileSuit.PIN, 'PIN'),
    (TileSuit.SOU, 'SOU'),
    (Wind.EAST, 'EAST'),
    (Wind.SOUTH, 'SOUTH'),
    (Wind.WEST, 'WEST'),
    (Wind.NORTH, 'NORTH'),
    (Dragon.WHITE, 'WHITE'),
    (Dragon.GREEN, 'GREEN'),
    (Dragon.RED, 'RED'),
])
def test_tile_enum_repr(e: TileSuit | Wind | Dragon, val: str):
    assert repr(e) == val

@pytest.mark.parametrize('e, val', [
    (TileSuit.MAN, 'MAN'),
    (TileSuit.PIN, 'PIN'),
    (TileSuit.SOU, 'SOU'),
    (Wind.EAST, 'EAST'),
    (Wind.SOUTH, 'SOUTH'),
    (Wind.WEST, 'WEST'),
    (Wind.NORTH, 'NORTH'),
    (Dragon.WHITE, 'WHITE'),
    (Dragon.GREEN, 'GREEN'),
    (Dragon.RED, 'RED'),
])
def test_tile_enum_str(e: TileSuit | Wind | Dragon, val: str):
    assert str(e) == val

def test_tile_enum_error_comp():
    with pytest.raises(ValueError):
        _ = TileSuit.SOU < {2, 3, 4, 6, 8}
    with pytest.raises(ValueError):
        _ = Wind.EAST < [15]
    with pytest.raises(ValueError):
        _ = Dragon.GREEN < ()