from mahjong import *

tf = TileFactory()
mf = MeldFactory(tf)
hf = HandFactory(tf, mf)
mg = MeldGenerator()
scorer = RiichiMahjongScorer(mg)

# MARK: 13o
# 13 Orphans (+ 13-wait)
def test_13o():
    assert scorer.get_yakuman(
        hf.create_hand('199m 19p 19s 123467z'), tf.create_tile('5z'),
        win_type=WinType.RON
    ) == {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }

    assert scorer.get_yakuman(
        hf.create_hand('19m 19p 1s 12344567z'), tf.create_tile('9s'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }

    assert scorer.get_yakuman(
        hf.create_hand('19m 19p 99s 1234567z'), tf.create_tile('1s'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }

def test_13o_13wait():
    for tile in ('1m', '9m', '1p', '9p', '1s', '9s', '1z', '2z', '3z', '4z', '5z', '6z', '7z'):
        assert scorer.get_yakuman(
            hf.create_hand('19m 19p 19s 1234567z'), tf.create_tile(tile),
            win_type=WinType.TSUMO
        ) == {
            DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS: 2
        }

def test_13o_wrong():
    assert scorer.get_yakuman(
        hf.create_hand('19m 19p 99s 1234567z'), tf.create_tile('1m'),
        win_type=WinType.RON
    ) == {}

    assert scorer.get_yakuman(
        hf.create_hand('19m 19p 19s 2345667z'), tf.create_tile('2z'),
        win_type=WinType.RON
    ) == {}

# ---

# MARK: 4CT
# Four Concealed Triplets (+ Tanki Wait)

def test_4ct():
    assert scorer.get_yakuman(
        hf.create_hand('222444m 444s 2233z'), tf.create_tile('2z'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }

    assert scorer.get_yakuman(
        hf.create_hand('222444m 444s 2233z'), tf.create_tile('3z'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }

    assert scorer.get_yakuman(
        hf.create_hand('11122m 444666p 99s'), tf.create_tile('2m'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }

    assert scorer.get_yakuman(
        hf.create_hand('11122m 444666p 99s'), tf.create_tile('9s'),
        win_type=WinType.TSUMO
    ) == {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }

    # TODO: add tests with closed kan

def test_4ct_tanki():
    assert scorer.get_yakuman(
        hf.create_hand('111222m 444666p 9s'), tf.create_tile('9s'),
        win_type=WinType.TSUMO
    ) == {
        DoubleYakuman.FOUR_CONCEALED_TRIPLETS_TANKI: 2
    }

    assert scorer.get_yakuman(
        hf.create_hand('333444666p 444s 1z'), tf.create_tile('1z'),
        win_type=WinType.RON
    ) == {
        DoubleYakuman.FOUR_CONCEALED_TRIPLETS_TANKI: 2
    }

    # TODO: add tests with closed kan
    pass

def test_4ct_wrong():
    # cannot Ron last triplet; only 3CT
    assert scorer.get_yakuman(
        hf.create_hand('11122m 444666p 99s'), tf.create_tile('2m'),
        win_type=WinType.RON
    ) == {}

    # cannot Ron last triplet; only 3CT
    assert scorer.get_yakuman(
        hf.create_hand('11122m 444666p 99s'), tf.create_tile('9s'),
        win_type=WinType.RON
    ) == {}

    # not winning tile
    assert scorer.get_yakuman(
        hf.create_hand('333555m 222444p 1z'), tf.create_tile('2z'),
        win_type=WinType.RON
    ) == {}

# ---

# TODO combine yakuman
def test_combo_yakuman():
    pass