from dataclasses import dataclass
from enum import Enum, StrEnum, auto

MIN_TILE_RANK = 1
MAX_TILE_RANK = 9

class TileSuit(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[auto]):
        return count * (MAX_TILE_RANK-MIN_TILE_RANK+1)

    MAN = auto()
    PIN = auto()
    SOU = auto()

    def __repr__(self):
        match self:
            case TileSuit.MAN:
                return 'MAN'
            case TileSuit.PIN:
                return 'PIN'
            case TileSuit.SOU:
                return 'SOU'

    def __str__(self):
        match self:
            case TileSuit.MAN:
                return 'MAN'
            case TileSuit.PIN:
                return 'PIN'
            case TileSuit.SOU:
                return 'SOU'

class Wind(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[auto]):
        return count+1

    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()

    def __repr__(self):
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

    def __str__(self):
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

class Dragon(Enum):
    _start = [w.value for w in Wind][-1]
    WHITE = auto()
    GREEN = auto()
    RED = auto()

    def __repr__(self):
        match self:
            case Dragon.WHITE:
                return 'WHITE'
            case Dragon.GREEN:
                return 'GREEN'
            case Dragon.RED:
                return 'RED'
            case _:
                raise ValueError

    def __str__(self):
        match self:
            case Dragon.WHITE:
                return 'WHITE'
            case Dragon.GREEN:
                return 'GREEN'
            case Dragon.RED:
                return 'RED'
            case _:
                raise ValueError

@dataclass
class SuitedTile:
    rank: int
    suit: TileSuit
    red_dora: bool = False

    def __repr__(self) -> str:
        return f'SuitedTile({self.rank},{self.suit})'

    @property
    def is_terminal(self) -> bool:
        return self.rank == MIN_TILE_RANK or self.rank == MAX_TILE_RANK

@dataclass
class HonorTile:
    symbol: Wind | Dragon

    def __repr__(self) -> str:
        return f'HonorTile({self.symbol})'

Tile = SuitedTile | HonorTile

# ---

def tile_order(t: Tile) -> int:
    match t:
        case SuitedTile(rank=rank, suit=suit):
            return suit.value + rank
        case HonorTile(symbol=symbol):
            return (MAX_TILE_RANK - MIN_TILE_RANK + 1)*len(TileSuit) + symbol.value

def sorted_tiles(tiles: list[Tile]) -> list[Tile]:
    return sorted(tiles, key=tile_order)

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
                    print(f'? {n}z')
                    for w in Wind:
                        print(w.value, int(n))
                        if w.value == int(n):
                            return HonorTile(Wind(int(n)))
                    for d in Dragon:
                        if d.value == int(n):
                            return HonorTile(Dragon(int(n)))
                    raise ValueError('Invalid honor tile passed to TileFactory')
                case _:
                    raise ValueError('Invalid tile kind passed to TileFactory')

# ---

class MeldKind(StrEnum):
    SEQUENCE = auto()
    TRIPLE = auto()

@dataclass
class Meld:
    tiles: list[Tile]
    is_open: bool = False

    def __len__(self) -> int:
        return len(self.tiles)

    def __repr__(self):
        return f'[{' '.join([*map(str, self.tiles)])}]'

    def __str__(self):
        return ' '.join([*map(str, self.tiles)])

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
    
    def __repr__(self):
        return f'Hand({' '.join([*map(repr, self.tiles), *map(repr, self.open_melds)])})'

    def __str__(self):
        return f'Hand({' '.join([*map(str, self.tiles), *map(str, self.open_melds)])})'

    @property
    def all_tiles(self) -> list[Tile]:
        ret: list[Tile] = []
        ret.extend(self.tiles)

        for m in self.open_melds:
            ret.extend(m.tiles)
        
        return ret
    
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
    def is_open(self):
        return len(self.open_melds) == 0
    
class HandFactory:
    tile_factory: TileFactory
    meld_factory: MeldFactory

    def __init__(self, tile_factory: TileFactory, meld_factory: MeldFactory):
        self.tile_factory = tile_factory
        self.meld_factory = meld_factory

    def create_hand(self, raw: str, num_kita: int = 0) -> Hand:
        tiles: list[Tile] = []
        open_melds: list[Meld] = []

        raw_split = raw.split(' ')
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

class RiichiState(StrEnum):
    NONE = ''
    RIICHI = 'Riichi'
    IPPATSU = 'Ippatsu'

class UnderState(StrEnum):
    NONE = ''
    UNDER_THE_SEA = 'Under the Sea'
    UNDER_THE_RIVER = 'Under the River'

class RiichiMahjongScorer:
    def _count_yakuman(self, hand: Hand, winning_tile: Tile) -> int:
        # todo: implement yakuman check
        #yaku: list[str] = []
        yakuman = 0
        #TILES: list[Tile] = sorted_tiles([*hand.all_tiles, winning_tile])

        return yakuman

    def _count_han_fu(
            self, hand: Hand, winning_tile: Tile, *,
            round_wind: Wind, seat_wind: Wind,
            riichi: RiichiState, under: UnderState,
            dora: list[Tile], ura_dora: list[Tile]) -> tuple[int, int]:
        yaku: list[str] = []
        han, fu = 0, 0
        TILES: list[Tile] = sorted_tiles([*hand.all_tiles, winning_tile])

        # add han from Riichi/Ippatsu
        match riichi:
            case RiichiState.NONE:
                pass
            case _:
                # add han from Ura Dora
                ura_dora_count = 0
                for ud in ura_dora:
                    for tile in TILES:
                        if ud == tile:
                            ura_dora_count += 1
                han += ura_dora_count
                if ura_dora_count:
                    yaku.append(f'{han} Ura Dora')

                # add han from Riichi/Ippatsu
                match riichi:
                    case RiichiState.RIICHI:
                        han += 1
                    case RiichiState.IPPATSU:
                        han += 2
                yaku.append(riichi)

        # add han from Kita
        han += hand.num_kita
        if hand.num_kita:
            yaku.append(f'{hand.num_kita} Kita')

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
            yaku.append(f'{red_dora_count} Red Dora')

        # add han from Dora
        dora_count = 0
        for d in dora:
            for tile in TILES:
                if d == tile:
                    dora_count += 1
        han += dora_count
        if dora_count:
            yaku.append(f'{dora_count} Dora')

        # ---

        # todo: implement actual yaku check

        # ---

        if len(yaku) == 0:
           han, fu = 0, 0

        return han, fu

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
            riichi: RiichiState, under: UnderState,
            dora: list[Tile], ura_dora: list[Tile]) -> int:
        yakuman, han, fu = 0, 0, 0

        if len(hand.tiles) + 3*len(hand.open_melds) == TILES_PER_HAND:
            yakuman = self._count_yakuman(hand, winning_tile)
            if yakuman == 0:
                han, fu = self._count_han_fu(
                    hand, winning_tile,
                    round_wind=round_wind, seat_wind=seat_wind,
                    riichi=riichi, under=under,
                    dora=dora, ura_dora=ura_dora
                )

        return self.compute_base_points(yakuman, han, fu)

# ---

tile_factory = TileFactory()
meld_factory = MeldFactory(tile_factory)
hand_factory = HandFactory(tile_factory, meld_factory)

raw1 = '45m 4555899p 88s 12z'
hand1 = hand_factory.create_hand(raw1)
print(raw1)
print(hand1)

scorer = RiichiMahjongScorer()
print(scorer.compute_base_points(0, 2, 60))