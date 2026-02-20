from mahjong import *

tf = TileFactory()
mf = MeldFactory(tf)
hf = HandFactory(tf, mf)
scorer = RiichiMahjongScorer()

# MARK: 13o
# 13 Orphans (+ 13-wait)
def test_13o():
    assert scorer.count_yakuman(
        hf.create_hand('199m 19p 19s 123467z'), tf.create_tile('5z'),
        win_type=WinType.RON
    ) == 1

    assert scorer.count_yakuman(
        hf.create_hand('19m 19p 1s 12344567z'), tf.create_tile('9s'),
        win_type=WinType.TSUMO
    ) == 1

    assert scorer.count_yakuman(
        hf.create_hand('19m 19p 99s 1234567z'), tf.create_tile('1s'),
        win_type=WinType.TSUMO
    ) == 1

def test_13o_13wait():
    for tile in ('1m', '9m', '1p', '9p', '1s', '9s', '1z', '2z', '3z', '4z', '5z', '6z', '7z'):
        assert scorer.count_yakuman(
            hf.create_hand('19m 19p 19s 1234567z'), tf.create_tile(tile),
            win_type=WinType.TSUMO
        ) == 2

def test_13o_wrong():
    assert scorer.count_yakuman(
        hf.create_hand('19m 19p 99s 1234567z'), tf.create_tile('1m'),
        win_type=WinType.RON
    ) == 0

    assert scorer.count_yakuman(
        hf.create_hand('19m 19p 19s 2345667z'), tf.create_tile('2z'),
        win_type=WinType.RON
    ) == 0

# ---

# TODO onwards
# MARK: 4CT
# Four Concealed Triplets (+ Tanki Wait)

def test_4ct():
    pass

def test_4ct_tanki():
    pass

def test_4ct_wrong():
    pass

# ---

# TODO combine yakuman
def test_combo_yakuman():
    pass