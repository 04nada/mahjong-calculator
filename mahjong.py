from dataclasses import dataclass
from enum import Enum, StrEnum, auto

MIN_TILE_RANK = 1
MAX_TILE_RANK = 9

class TileSuit(Enum):
    MAN = auto()
    PIN = auto()
    SOU = auto()

class Wind(Enum):
    _start = -1
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    NORTH = auto()

class Dragon(Enum):
    _start = [w.value for w in Wind][-1]
    WHITE = auto()
    GREEN = auto()
    RED = auto()

@dataclass
class SuitedTile:
    rank: int
    suit: TileSuit
    red_dora: bool = False

    @property
    def is_terminal(self) -> bool:
        return self.rank == MIN_TILE_RANK or self.rank == MAX_TILE_RANK

@dataclass
class HonorTile:
    symbol: Wind | Dragon

Tile = SuitedTile | HonorTile

# ---

def tile_order(t: Tile) -> int:
    match t:
        case SuitedTile(rank=rank, suit=suit):
            return (MAX_TILE_RANK - MIN_TILE_RANK + 1)*(suit.value-1) + rank
        case HonorTile(symbol=symbol):
            return (MAX_TILE_RANK - MIN_TILE_RANK + 1)*len(TileSuit) + symbol.value

def sorted_tiles(tiles: list[Tile]):
    return sorted(tiles, key=tile_order)

# ---

class MeldKind(StrEnum):
    SEQUENCE = auto()
    TRIPLE = auto()

class Meld:
    tiles: list[Tile]

    def __init__(self, tiles: list[Tile]):
        self.tiles = tiles

    def __len__(self):
        return len(self.tiles)

# ---

TILES_PER_HAND = 13

class Hand:
    tiles: list[Tile]
    open_melds: list[Meld]
    num_kita: int

    def __init__(self, tiles: list[Tile], open_melds: list[Meld], num_kita: int = 0):
        self.tiles = tiles
        self.open_melds = open_melds
        self.num_kita = num_kita

    def __len__(self) -> int:
        return len(self.tiles)
    
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
    
class HandCreator:
    def create_hand(self, raw: str) -> Hand:
        tiles: list[Tile] = []
        open_melds: list[Meld] = []

        return Hand(tiles, open_melds, 0)

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

tile1: Tile = SuitedTile(3, TileSuit.PIN)
tile2: Tile = SuitedTile(3, TileSuit.PIN)

scorer = RiichiMahjongScorer()
print(scorer.compute_base_points(0, 2, 60))