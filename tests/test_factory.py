from mahjong import *

tf = TileFactory()
mf = MeldFactory(tf)
hf = HandFactory(tf, mf)

def test_tile_factory():
    # Man
    assert tf.create_tile('1m') == SuitedTile(1, TileSuit.MAN)
    assert tf.create_tile('5m') == SuitedTile(5, TileSuit.MAN)
    assert tf.create_tile('0m') == SuitedTile(5, TileSuit.MAN, True)
    assert tf.create_tile('9m') == SuitedTile(9, TileSuit.MAN)
    # Pin
    assert tf.create_tile('1p') == SuitedTile(1, TileSuit.PIN)
    assert tf.create_tile('5p') == SuitedTile(5, TileSuit.PIN)
    assert tf.create_tile('0p') == SuitedTile(5, TileSuit.PIN, True)
    assert tf.create_tile('9p') == SuitedTile(9, TileSuit.PIN)
    # Sou
    assert tf.create_tile('1s') == SuitedTile(1, TileSuit.SOU)
    assert tf.create_tile('5s') == SuitedTile(5, TileSuit.SOU)
    assert tf.create_tile('0s') == SuitedTile(5, TileSuit.SOU, True)
    assert tf.create_tile('9s') == SuitedTile(9, TileSuit.SOU)
    # Honor Winds
    assert tf.create_tile('1z') == HonorTile(Wind.EAST)
    assert tf.create_tile('2z') == HonorTile(Wind.SOUTH)
    assert tf.create_tile('3z') == HonorTile(Wind.WEST)
    assert tf.create_tile('4z') == HonorTile(Wind.NORTH)
    # Honor Dragons
    assert tf.create_tile('5z') == HonorTile(Dragon.WHITE)
    assert tf.create_tile('6z') == HonorTile(Dragon.GREEN)
    assert tf.create_tile('7z') == HonorTile(Dragon.RED)

def test_meld_factory():
    # Man
    assert mf.create_meld('123m') == Meld([SuitedTile(i, TileSuit.MAN) for i in (1, 2, 3)])
    assert mf.create_meld('456m') == Meld([SuitedTile(i, TileSuit.MAN) for i in (4, 5, 6)])
    assert mf.create_meld('789m') == Meld([SuitedTile(i, TileSuit.MAN) for i in (7, 8, 9)])
    assert mf.create_meld('333m') == Meld([SuitedTile(i, TileSuit.MAN) for i in (3, 3, 3)])
    assert mf.create_meld('888m') == Meld([SuitedTile(i, TileSuit.MAN) for i in (8, 8, 8)])
    # Pin
    assert mf.create_meld('123p') == Meld([SuitedTile(i, TileSuit.PIN) for i in (1, 2, 3)])
    assert mf.create_meld('456p') == Meld([SuitedTile(i, TileSuit.PIN) for i in (4, 5, 6)])
    assert mf.create_meld('789p') == Meld([SuitedTile(i, TileSuit.PIN) for i in (7, 8, 9)])
    assert mf.create_meld('111p') == Meld([SuitedTile(i, TileSuit.PIN) for i in (1, 1, 1)])
    assert mf.create_meld('555p') == Meld([SuitedTile(i, TileSuit.PIN) for i in (5, 5, 5)])
    # Sou
    assert mf.create_meld('123s') == Meld([SuitedTile(i, TileSuit.SOU) for i in (1, 2, 3)])
    assert mf.create_meld('456s') == Meld([SuitedTile(i, TileSuit.SOU) for i in (4, 5, 6)])
    assert mf.create_meld('789s') == Meld([SuitedTile(i, TileSuit.SOU) for i in (7, 8, 9)])
    assert mf.create_meld('444s') == Meld([SuitedTile(i, TileSuit.SOU) for i in (4, 4, 4)])
    assert mf.create_meld('777s') == Meld([SuitedTile(i, TileSuit.SOU) for i in (7, 7, 7)])
    # Honor Tiles
    assert mf.create_meld('111z') == Meld([HonorTile(Wind.EAST), HonorTile(Wind.EAST), HonorTile(Wind.EAST)])
    assert mf.create_meld('222z') == Meld([HonorTile(Wind.SOUTH), HonorTile(Wind.SOUTH), HonorTile(Wind.SOUTH)])
    assert mf.create_meld('333z') == Meld([HonorTile(Wind.WEST), HonorTile(Wind.WEST), HonorTile(Wind.WEST)])
    assert mf.create_meld('444z') == Meld([HonorTile(Wind.NORTH), HonorTile(Wind.NORTH), HonorTile(Wind.NORTH)])
    assert mf.create_meld('555z') == Meld([HonorTile(Dragon.WHITE), HonorTile(Dragon.WHITE), HonorTile(Dragon.WHITE)])
    assert mf.create_meld('666z') == Meld([HonorTile(Dragon.GREEN), HonorTile(Dragon.GREEN), HonorTile(Dragon.GREEN)])
    assert mf.create_meld('777z') == Meld([HonorTile(Dragon.RED), HonorTile(Dragon.RED), HonorTile(Dragon.RED)])