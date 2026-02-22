from collections import Counter
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from functools import total_ordering
from typing import Generator
from sortedcontainers import SortedDict

class TileSuit(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[auto]) -> int:
        return count * 9
    MAN = auto()
    PIN = auto()
    SOU = auto()

    def __repr__(self) -> str:
        match self:
            case TileSuit.MAN:
                return 'MAN'
            case TileSuit.PIN:
                return 'PIN'
            case TileSuit.SOU:
                return 'SOU'

    def __str__(self) -> str:
        match self:
            case TileSuit.MAN:
                return 'MAN'
            case TileSuit.PIN:
                return 'PIN'
            case TileSuit.SOU:
                return 'SOU'

    def __lt__(self, other: object) -> bool:
        match other:
            case TileSuit():
                return self.value < other.value
            case _:
                raise ValueError

@total_ordering
class Wind(Enum):
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()

    def __repr__(self) -> str:
        match self:
            case Wind.EAST:
                return 'EAST'
            case Wind.SOUTH:
                return 'SOUTH'
            case Wind.WEST:
                return 'WEST'
            case Wind.NORTH:
                return 'NORTH'
            case _:
                raise ValueError

    def __str__(self) -> str:
        match self:
            case Wind.EAST:
                return 'EAST'
            case Wind.SOUTH:
                return 'SOUTH'
            case Wind.WEST:
                return 'WEST'
            case Wind.NORTH:
                return 'NORTH'
            case _:
                raise ValueError

    def __lt__(self, other: object) -> bool:
        match other:
            case Wind():
                return self.value < other.value
            case Dragon():
                return True
            case _:
                raise ValueError

@total_ordering
class Dragon(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[auto]) -> int:
        return count + [w.value for w in Wind][-1]+1
    WHITE = auto()
    GREEN = auto()
    RED = auto()

    def __repr__(self) -> str:
        match self:
            case Dragon.WHITE:
                return 'WHITE'
            case Dragon.GREEN:
                return 'GREEN'
            case Dragon.RED:
                return 'RED'
            case _:
                raise ValueError

    def __str__(self) -> str:
        match self:
            case Dragon.WHITE:
                return 'WHITE'
            case Dragon.GREEN:
                return 'GREEN'
            case Dragon.RED:
                return 'RED'
            case _:
                raise ValueError

    def __lt__(self, other: object) -> bool:
        match other:
            case Wind():
                return False
            case Dragon():
                return self.value < other.value
            case _:
                raise ValueError

@dataclass
@total_ordering
class SuitedTile:
    rank: int
    suit: TileSuit
    red_dora: bool = False

    def __hash__(self) -> int:
        return hash((__class__.__name__, self.rank, self.suit, self.red_dora))

    def __str__(self) -> str:
        return f'({self.rank}{'R' if self.red_dora else ''},{self.suit})'

    def __eq__(self, other: object) -> bool:
        match other:
            case SuitedTile(rank=rank, suit=suit):
                return (self.suit, self.rank) == (suit, rank)
            case HonorTile():
                return False
            case _:
                raise ValueError

    def __lt__(self, other: object) -> bool:
        match other:
            case SuitedTile(rank=rank, suit=suit):
                return (self.suit, self.rank) < (suit, rank)
            case HonorTile():
                return True
            case _:
                raise ValueError

    @property
    def is_terminal(self) -> bool:
        return self.rank == 1 or self.rank == 9

@dataclass
@total_ordering
class HonorTile:
    symbol: Wind | Dragon

    def __hash__(self) -> int:
        return hash((__class__.__name__, self.symbol))

    def __str__(self) -> str:
        return f'({self.symbol})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tile):
            match other:
                case SuitedTile():
                    return False
                case HonorTile(symbol=symbol):
                    return self.symbol == symbol
        else:
            raise ValueError

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Tile):
            match other:
                case SuitedTile():
                    return False
                case HonorTile(symbol=symbol):
                    return self.symbol < symbol
        else:
            raise ValueError

Tile = SuitedTile | HonorTile

# ---

class TileFactory:
    def create_tile(self, raw: str) -> Tile:
        if len(raw) != 2:
            raise ValueError(f'Raw string "{raw}" passed to TileFactory is not of length 2.')
        else:
            match raw[0], raw[1]:
                case n, 'm':
                    rank = int(n)
                    red_dora = False
                    if rank == 0:
                        rank = 5
                        red_dora = True
                    return SuitedTile(rank, TileSuit.MAN, red_dora)
                case n, 'p':
                    rank = int(n)
                    red_dora = False
                    if rank == 0:
                        rank = 5
                        red_dora = True
                    return SuitedTile(rank, TileSuit.PIN, red_dora)
                case n, 's':
                    rank = int(n)
                    red_dora = False
                    if rank == 0:
                        rank = 5
                        red_dora = True
                    return SuitedTile(rank, TileSuit.SOU, red_dora)
                case n, 'z':
                    for w in Wind:
                        if w.value == int(n):
                            return HonorTile(Wind(int(n)))
                    for d in Dragon:
                        if d.value == int(n):
                            return HonorTile(Dragon(int(n)))
                    raise ValueError('Invalid honor tile passed to TileFactory')
                case _:
                    raise ValueError('Invalid tile kind passed to TileFactory')

# ---

class ClosedMeldKind(StrEnum):
    SEQUENCE = auto()
    TRIPLET = auto()

class OpenMeldKind(StrEnum):
    CHII = 'Chii'
    PON = 'Pon'
    KAN = 'Kan'

MeldKind = ClosedMeldKind | OpenMeldKind

@dataclass
class Meld:
    tiles: list[Tile]
    is_open: bool = False

    def __len__(self) -> int:
        return len(self.tiles)

    def __repr__(self) -> str:
        return f'{'Open' if self.is_open else 'Closed'}Meld[{' '.join([*map(repr, self.tiles)])}]'

    def __str__(self) -> str:
        return f'{'Open' if self.is_open else 'Closed'}Meld[{' '.join([*map(str, self.tiles)])}]'

    @property
    def meld_kind(self) -> MeldKind | None:
        match len(self.tiles):
            case 3:
                if self.tiles[0] == self.tiles[1] == self.tiles[2]:
                    return OpenMeldKind.PON if self.is_open else ClosedMeldKind.TRIPLET
                else:
                    match self.tiles[0]:
                        case SuitedTile(rank=rank, suit=suit):
                            if rank <= 7 and self.tiles[1] == SuitedTile(rank+1, suit) and self.tiles[2] == SuitedTile(rank+2, suit):
                                return OpenMeldKind.CHII if self.is_open else ClosedMeldKind.SEQUENCE
                            else:
                                return None
                        case _:
                            return None
            case 4:
                if self.is_open and self.tiles[0] == self.tiles[1] == self.tiles[2] == self.tiles[3]:
                    return OpenMeldKind.KAN
                else:
                    return None
            case _:
                return None

class MeldFactory:
    tile_factory: TileFactory

    def __init__(self, tile_factory: TileFactory):
        self.tile_factory = tile_factory

    def create_meld(self, raw: str, is_open: bool = False) -> Meld:
        tiles: list[Tile] = []

        try:
            ranks = raw[:-1]
            suit = raw[-1]

            for rank_str in ranks:
                tiles.append(self.tile_factory.create_tile(f'{rank_str}{suit}'))
        except:
            raise ValueError

        return Meld(tiles, is_open)

# ---

TILES_PER_HAND = 13

@dataclass
class Hand:
    tiles: list[Tile]
    open_melds: list[Meld]
    num_kita: int = 0

    def __len__(self) -> int:
        return len(self.tiles)
    
    def __repr__(self) -> str:
        return f'Hand({' '.join([*map(repr, self.tiles), *map(repr, self.open_melds)])}{f' + {self.num_kita} kita' if self.num_kita > 0 else ''})'

    def __str__(self) -> str:
        return f'Hand({' '.join([*map(str, self.tiles), *map(str, self.open_melds)])}{f' + {self.num_kita} kita' if self.num_kita > 0 else ''})'

    @property
    def all_tiles(self) -> list[Tile]:
        ret: list[Tile] = []
        ret.extend(self.tiles)

        for m in self.open_melds:
            ret.extend(m.tiles)
        
        return ret

    @property
    def all_tiles_dict(self) -> dict[Tile, int]:
        return dict(Counter(self.all_tiles))

    @property
    def all_tiles_with_kita(self) -> list[Tile]:
        ret: list[Tile] = []
        ret.extend(self.tiles)

        for m in self.open_melds:
            ret.extend(m.tiles)

        for _ in range(self.num_kita):
            ret.append(HonorTile(Wind.NORTH))
        
        return ret

    @property
    def all_tiles_with_kita_dict(self) -> dict[Tile, int]:
        return dict(Counter(self.all_tiles_with_kita))

    @property
    def is_open(self) -> bool:
        return len(self.open_melds) > 0

class HandFactory:
    tile_factory: TileFactory
    meld_factory: MeldFactory

    def __init__(self, tile_factory: TileFactory, meld_factory: MeldFactory):
        self.tile_factory = tile_factory
        self.meld_factory = meld_factory

    def create_hand(self, raw: str, num_kita: int = 0) -> Hand:
        tiles: list[Tile] = []
        open_melds: list[Meld] = []

        raw_split: list[str] = raw.split(' ')
        if '-' in raw:
            raw_closed: list[str] = raw_split[:-1]
            raw_open: list[str] = raw_split[-1].split('-')
        else:
            raw_closed = raw_split
            raw_open = []

        # create Tile instances from closed tiles
        for s in raw_closed:
            try:
                ranks = s[:-1]
                suit = s[-1]

                for rank_str in ranks:
                    tiles.append(self.tile_factory.create_tile(f'{rank_str}{suit}'))
            except:
                raise ValueError

        # create Meld instances from open tiles
        for s in raw_open:
            try:
                open_melds.append(self.meld_factory.create_meld(s, True))
            except:
                raise ValueError

        return Hand(tiles, open_melds, num_kita)

# ---

class DoubleYakuman(StrEnum):
    THIRTEEN_WAIT_THIRTEEN_ORPHANS = '13-wait 13 Orphans'
    FOUR_CONCEALED_TRIPLETS_TANKI = 'Four Concealed Triplets - Tanki Wait'
    TRUE_NINE_GATES = 'True Nine Gates'
    FOUR_BIG_WINDS = 'Four Big Winds'

class SingleYakuman(StrEnum):
    THIRTEEN_ORPHANS = '13 Orphans'
    FOUR_CONCEALED_TRIPLETS = 'Four Concealed Triplets'
    BIG_THREE_DRAGONS = 'Big Three Dragons'
    NINE_GATES = 'Nine Gates'
    FOUR_LITTLE_WINDS = 'Four Little Winds'
    ALL_HONORS = 'All Honors'
    ALL_TRIPLETS = 'All Triplets'
    ALL_GREEN = 'All Green'
    FOUR_KANS = 'Four Kans'

Yakuman = SingleYakuman | DoubleYakuman

class WinType(StrEnum):
    RON = 'Ron'
    TSUMO = 'Tsumo'

class RiichiState(StrEnum):
    NONE = ''
    RIICHI = 'Riichi'
    IPPATSU = 'Ippatsu'
    DOUBLE_RIICHI = 'Double Riichi'
    DOUBLE_RIICHI_IPPATSU = 'Double Riichi + Ippatsu'

class UnderState(StrEnum):
    NONE = ''
    UNDER_THE_SEA = 'Under the Sea'
    UNDER_THE_RIVER = 'Under the River'

class MeldGenerator:
    def _yield_melds(self, tiles_sorteddict: SortedDict[Tile, int], melds: list[Meld]) -> Generator[list[Meld], None, None]:
        if sum(tiles_sorteddict.values()) % 3 != 0:
            # check if tile count can be grouped into 3s
            raise ValueError('Total number of tiles not divisible by 3; cannot group into melds')
        elif sum(tiles_sorteddict.values()) == 0:
            # Base Case: yield melds if there are no more tiles to be processed
            yield melds
        else:
            # get leftmost "unmelded" tile in dictionary (hence the SortedDict use)
            first_tile, first_tile_freq = tiles_sorteddict.peekitem(index=0)

            # check if first_tile can be part of a triplet
            if first_tile_freq >= 3:
                # remove triplet of first_tile
                tiles_sorteddict[first_tile] -= 3
                if tiles_sorteddict[first_tile] == 0:
                    del tiles_sorteddict[first_tile]

                new_meld = Meld([first_tile for _ in range(3)])
                melds.append(new_meld)
                yield from self._yield_melds(tiles_sorteddict, melds)

                # undo updates
                tiles_sorteddict[first_tile] = tiles_sorteddict.get(first_tile, 0) + 3
                melds.pop()

            # check if first_tile can be part of a sequence
            match first_tile:
                case SuitedTile(rank=rank, suit=suit):
                    next1_tile = SuitedTile(rank+1, suit)
                    next2_tile = SuitedTile(rank+2, suit)
                    new_meld_list: list[Tile] = [first_tile, next1_tile, next2_tile]

                    if rank <= 7 and tiles_sorteddict.get(next1_tile, 0) >= 1 and tiles_sorteddict.get(next2_tile, 0) >= 1:
                        # remove sequence starting with first_tile
                        for t in new_meld_list:
                            tiles_sorteddict[t] -= 1
                            if tiles_sorteddict[t] == 0:
                                del tiles_sorteddict[t]

                        new_meld = Meld(new_meld_list)
                        melds.append(new_meld)
                        yield from self._yield_melds(tiles_sorteddict, melds)

                        # undo updates
                        for t in new_meld_list:
                            tiles_sorteddict[t] = tiles_sorteddict.get(t, 0) + 1
                        melds.pop()
                case _:
                    pass
        
    def yield_melds(self, tiles_dict: dict[Tile, int], melds: list[Meld]) -> Generator[list[Meld], None, None]:
        tiles_sorteddict: SortedDict[Tile, int] = SortedDict()
        for k, v in tiles_dict.items():
            tiles_sorteddict[k] = v
        yield from self._yield_melds(tiles_sorteddict, melds)

    def yield_melds_with_pair(self, tiles_dict: dict[Tile, int], melds: list[Meld]) -> Generator[tuple[list[Meld], tuple[Tile, Tile]], None, None]:
        tiles_sorteddict: SortedDict[Tile, int] = SortedDict()
        for k, v in tiles_dict.items():
            tiles_sorteddict[k] = v

        TILES: list[Tile] = [*tiles_sorteddict.keys()]
        for t in TILES:
            # check if pair can be retrieved from current tile
            if tiles_sorteddict[t] >= 2:
                # remove pair of current tile
                pair: tuple[Tile, Tile] = (t, t)
                tiles_sorteddict[t] -= 2
                if tiles_sorteddict[t] == 0:
                    del tiles_sorteddict[t]

                for melds in self._yield_melds(tiles_sorteddict, []):
                    yield melds, pair

                # undo updates
                tiles_sorteddict[t] = tiles_sorteddict.get(t, 0) + 2

class RiichiMahjongScorer:
    def count_yakuman(self, yakuman: dict[Yakuman, int]) -> int:
        return sum(yakuman.values())
    
    def count_han_fu(self, yaku: dict[str, tuple[int, int]]) -> tuple[int, int]:
        han, fu = 0, 0
        for y in yaku.values():
            han += y[0]
            fu += y[1]
        return han, fu

    def get_yakuman(self, hand: Hand, winning_tile: Tile, *, win_type: WinType) -> dict[Yakuman, int]:
        yakuman: dict[Yakuman, int] = {}
        TILES: list[Tile] = sorted([*hand.all_tiles, winning_tile])
        TILES_DICT: dict[Tile, int] = dict(Counter(TILES))
        assert len(TILES) == TILES_PER_HAND+1

        # 13o
        set_13o: set[Tile] = {*(SuitedTile(i, s) for i in (1, 9) for s in TileSuit), *(HonorTile(w) for w in Wind), *(HonorTile(d) for d in Dragon)}
        if set(TILES) == set_13o:
            if set(hand.all_tiles) == set_13o:
                # 13-wait (Double Yakuman)
                yakuman[DoubleYakuman.THIRTEEN_WAIT_THIRTEEN_ORPHANS] = 2
            else:
                # regular (Single Yakuman)
                yakuman[SingleYakuman.THIRTEEN_ORPHANS] = 1

        # 4CT
        # TODO: consider closed kans for 4CT
        if set(TILES_DICT.values()) == {2,3,3,3,3}:
            match set(hand.all_tiles_dict.values()) == {1,3,3,3,3}, win_type:
                case True, _:
                    # Suuankou Tanki / Four Concealed Triplets - Tanki Wait
                    # Tanki wait (Double Yakuman)
                    yakuman[DoubleYakuman.FOUR_CONCEALED_TRIPLETS_TANKI] = 2
                case False, WinType.TSUMO:
                    # Suuankou / Four Concealed Triplets
                    # regular (Single Yakuman)
                    yakuman[SingleYakuman.FOUR_CONCEALED_TRIPLETS] = 1
                case False, WinType.RON:
                    # cannot Ron the last triplet
                    # only counts as 3CT (no Yakuman)
                    pass

        # TODO: Daisangen / Big Three Dragons
        # TODO: Suushiihou / Four Winds
            # TODO: Daisuushii / Four Big Winds
            # TODO: Shousuushii / Four Little Winds
        # TODO: / All Terminals 
        # TODO: / All Honors
        # TODO: / Nine Gates
            # TODO: / True Nine Gates
            # TODO: / Nine Gates
        # TODO: / All Green
        # TODO: / Four Kans

        return yakuman

    def get_yaku(
            self, hand: Hand, winning_tile: Tile, *,
            round_wind: Wind, seat_wind: Wind,
            win_type: WinType, riichi: RiichiState, under: UnderState,
            dora: list[Tile], ura_dora: list[Tile]) -> dict[str, tuple[int, int]]:
        yaku: dict[str, tuple[int, int]] = {}
        han, _ = 0, 0

        #HAND_DICT: dict[Tile, int] = dict(Counter(hand.tiles))
        TILES: list[Tile] = sorted([*hand.all_tiles, winning_tile])
        #TILES_DICT: dict[Tile, int] = dict(Counter(TILES))

        # add han from Riichi/Ippatsu
        match riichi:
            case RiichiState.NONE:
                pass
            case _:
                # add han from Tsumo if Riichi
                tsumo_han: int = 1 if win_type == WinType.TSUMO else 0
                han += tsumo_han
                if tsumo_han:
                    yaku[WinType.TSUMO] = (tsumo_han, 0)

                # add han from Ura Dora
                ura_dora_count = sum((1 for ud in ura_dora for t in TILES if ud == t))
                han += ura_dora_count
                if ura_dora_count:
                    yaku[f'{ura_dora_count} Ura Dora'] = (ura_dora_count, 0)

                # add han from Riichi/Double Riichi
                riichi_han: int = 0
                match riichi:
                    case RiichiState.RIICHI | RiichiState.IPPATSU:
                        riichi_han = 1
                        yaku[RiichiState.RIICHI] = (riichi_han, 0)
                    case RiichiState.DOUBLE_RIICHI | RiichiState.DOUBLE_RIICHI_IPPATSU:
                        riichi_han = 2
                        yaku[RiichiState.DOUBLE_RIICHI] = (riichi_han, 0)
                han += riichi_han

                # add han from Ippatsu
                ippatsu_han: int = 0
                match riichi:
                    case RiichiState.IPPATSU | RiichiState.DOUBLE_RIICHI_IPPATSU:
                        ippatsu_han = 1
                        yaku[RiichiState.IPPATSU] = (ippatsu_han, 0)
                    case _:
                        ippatsu_han = 0
                han += ippatsu_han

        # add han from Kita
        han += hand.num_kita
        if hand.num_kita:
            yaku[f'{hand.num_kita} Kita'] = (hand.num_kita, 0)

        # add han from Red Dora
        red_dora_count = 0
        for tile in TILES:
            match tile:
                case SuitedTile(red_dora=red_dora):
                    if red_dora:
                        red_dora_count += 1
                case _:
                    pass
        han += red_dora_count
        if red_dora_count:
            yaku[f'{red_dora_count} Red Dora'] = (red_dora_count, 0)

        # add han from Dora
        dora_count = sum((1 for d in dora for t in TILES if d == t))
        han += dora_count
        if dora_count:
            yaku[f'{dora_count} Dora'] = (dora_count, 0)

        # ---

        # TODO: implement actual yaku check using meld generator

        # ---

        # clear yaku if 0 han
        if han == 0:
            yaku.clear()
            han, _ = 0, 0

        return yaku

    def compute_base_points(self, yakuman: int, han: int, fu: int) -> int:
        if yakuman > 0:
            # [multiple] yakuman
            return 8000 * yakuman
        elif han >= 13:
            # kazoe yakuman
            return 8000
        elif han >= 11:
            # sanbaiman
            return 6000
        elif han >= 8:
            # baiman
            return 4000
        elif han >= 6:
            # haneman
            return 3000
        elif han == 5 or (han == 4 and fu >= 40) or (han == 3 and fu >= 70):
            # mangan
            return 2000
        else:
            return min(2000, fu * 2**(2+han))

    def get_points(
            self, hand: Hand, winning_tile: Tile, *,
            round_wind: Wind, seat_wind: Wind,
            win_type: WinType, riichi: RiichiState, under: UnderState,
            dora: list[Tile], ura_dora: list[Tile]) -> int:
        num_yakuman, han, fu = 0, 0, 0

        if len(hand.tiles) + 3*len(hand.open_melds) == TILES_PER_HAND:
            yakuman = self.get_yakuman(hand, winning_tile, win_type=win_type)
            num_yakuman = sum(yakuman.values())

            if num_yakuman == 0:
                yaku = self.get_yaku(
                    hand, winning_tile,
                    round_wind=round_wind, seat_wind=seat_wind,
                    win_type=win_type, riichi=riichi, under=under,
                    dora=dora, ura_dora=ura_dora
                )

                for y in yaku.values():
                    han += y[0]
                    fu += y[1]

        return self.compute_base_points(num_yakuman, han, fu)

# ---

tf = TileFactory()
mf = MeldFactory(tf)
hf = HandFactory(tf, mf)
scorer = RiichiMahjongScorer()
mg = MeldGenerator()

str1 = '22223333444455m'
hand1 = hf.create_hand(str1, 1)
print(str1)
for melds, pair in mg.yield_melds_with_pair(hand1.all_tiles_dict, []):
    print(*[str(meld) for meld in melds], *pair)

str2 = '222233334444m'
hand2 = hf.create_hand(str2, 1)
print(str2)
for melds in mg.yield_melds(hand2.all_tiles_dict, []):
    print(*[str(meld) for meld in melds])