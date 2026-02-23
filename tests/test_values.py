from mahjong import *

# ---

def test_enum_values():
    assert TileSuit.MAN.value == 0
    assert TileSuit.PIN.value == 9
    assert TileSuit.SOU.value == 18
    assert Wind.EAST.value == 1
    assert Wind.SOUTH.value == 2
    assert Wind.WEST.value == 3
    assert Wind.NORTH.value == 4
    assert Dragon.WHITE.value == 5
    assert Dragon.GREEN.value == 6
    assert Dragon.RED.value == 7