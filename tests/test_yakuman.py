import pytest

from mahjong import *

tf = TileFactory()
mf = MeldFactory(tf)
hf = HandFactory(tf, mf)
mg = MeldGenerator()
scorer = RiichiMahjongScorer(mg)

# MARK: 13o
# 13 Orphans (+ 13-wait)
@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('199m 19p 19s 123467z', '5z', WinType.RON, {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }),
    ('19m 19p 1s 12344567z', '9s', WinType.TSUMO, {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }),
    ('19m 19p 99s 1234567z', '1s', WinType.TSUMO, {
        SingleYakuman.THIRTEEN_ORPHANS: 1
    }),
])
def test_13o(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]) -> None:
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('19m 19p 19s 1234567z', '1m', WinType.RON, {
        DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS: 2
    }),
    ('19m 19p 19s 1234567z', '1z', WinType.RON, {
        DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS: 2
    }),
    ('19m 19p 19s 1234567z', '9p', WinType.TSUMO, {
        DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS: 2
    }),
    ('19m 19p 19s 1234567z', '6z', WinType.TSUMO, {
        DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS: 2
    }),
])
def test_13o_13wait(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('19m 19p 99s 1234567z', '1m', WinType.RON, {}),
    ('19m 19p 19s 2345667z', '2z', WinType.TSUMO, {}),
])
def test_13o_wrong(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

# ---

# MARK: 4CT
# Four Concealed Triplets (+ Tanki Wait)
@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('222444m 444s 2233z', '2z', WinType.TSUMO, {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }),
    ('222444m 444s 2233z', '3z', WinType.TSUMO, {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }),
    ('11122m 444666p 99s', '2m', WinType.TSUMO, {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }),
    ('11122m 444666p 99s', '9s', WinType.TSUMO, {
        SingleYakuman.FOUR_CONCEALED_TRIPLETS: 1
    }),
    # TODO: add tests with closed kan
])
def test_4ct(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('111222m 444666p 9s', '9s', WinType.TSUMO, {
        DoubleYakuman.FOUR_CONCEALED_TRIPLETS_TANKI: 2
    }),
    ('333444666p 444s 1z', '1z', WinType.RON, {
        DoubleYakuman.FOUR_CONCEALED_TRIPLETS_TANKI: 2
    }),
    # TODO: add tests with closed kan
])
def test_4ct_tanki(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

@pytest.mark.parametrize('h, t, win_type, yakuman', [
    ('11122m 444666p 99s', '2m', WinType.RON, {}),          # cannot Ron last triplet; only 3CT
    ('11122m 444666p 99s', '9s', WinType.RON, {}),          # cannot Ron last triplet; only 3CT
    ('333555m 222444p 1z', '2z', WinType.TSUMO, {}),        # not winning tile
])
def test_4ct_wrong(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    assert scorer.get_yakuman(hf.create_hand(h), tf.create_tile(t), win_type=win_type) == yakuman

# ---

# TODO combine yakuman
"""
@pytest.mark.parametrize('h, t, win_type, yakuman', [
])
def test_combo_yakuman(h: str, t: str, win_type: WinType, yakuman: dict[Yakuman, int]):
    pass
"""