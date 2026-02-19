from mahjong import *

# ---

def test_enum_values():
    assert TileSuit.MAN.value == 0
    assert TileSuit.PIN.value == MAX_TILE_RANK-MIN_TILE_RANK+1
    assert TileSuit.SOU.value == 2*(MAX_TILE_RANK-MIN_TILE_RANK+1)
    assert Wind.EAST.value == 1
    assert Wind.SOUTH.value == 2
    assert Wind.WEST.value == 3
    assert Wind.NORTH.value == 4
    assert Dragon.WHITE.value == 5
    assert Dragon.GREEN.value == 6
    assert Dragon.RED.value == 7

def test_tile_orders():
    assert tile_order(SuitedTile(1, TileSuit.MAN)) == 1
    assert tile_order(SuitedTile(5, TileSuit.MAN)) == 5
    assert tile_order(SuitedTile(5, TileSuit.MAN, True)) == 5
    assert tile_order(SuitedTile(9, TileSuit.MAN)) == 9
    assert tile_order(SuitedTile(1, TileSuit.PIN)) == 10
    assert tile_order(SuitedTile(5, TileSuit.PIN)) == 14
    assert tile_order(SuitedTile(5, TileSuit.PIN, True)) == 14
    assert tile_order(SuitedTile(9, TileSuit.PIN)) == 18
    assert tile_order(SuitedTile(1, TileSuit.SOU)) == 19
    assert tile_order(SuitedTile(5, TileSuit.SOU)) == 23
    assert tile_order(SuitedTile(5, TileSuit.SOU, True)) == 23
    assert tile_order(SuitedTile(9, TileSuit.SOU)) == 27
    assert tile_order(HonorTile(Wind.EAST)) == 28
    assert tile_order(HonorTile(Wind.SOUTH)) == 29
    assert tile_order(HonorTile(Wind.WEST)) == 30
    assert tile_order(HonorTile(Wind.NORTH)) == 31
    assert tile_order(HonorTile(Dragon.WHITE)) == 32
    assert tile_order(HonorTile(Dragon.GREEN)) == 33
    assert tile_order(HonorTile(Dragon.RED)) == 34