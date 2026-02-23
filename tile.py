from dataclasses import dataclass
from functools import total_ordering

from tile_enums import TileSuit, Wind, Dragon

# ---

@dataclass
@total_ordering
class SuitedTile:
    _rank: int
    _suit: TileSuit
    _red_dora: bool = False

    def __hash__(self) -> int:
        return hash((__class__.__name__, self._rank, self._suit, self._red_dora))

    def __str__(self) -> str:
        return f'({self._rank}{'R' if self._red_dora else ''},{self._suit})'

    def __lt__(self, other: object) -> bool:
        match other:
            case SuitedTile(_rank=rank, _suit=suit):
                return (self._suit, self._rank) < (suit, rank)
            case HonorTile():
                return True
            case _:
                raise TypeError

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def suit(self) -> TileSuit:
        return self._suit

    @property
    def red_dora(self) -> bool:
        return self._red_dora

    @property
    def is_terminal(self) -> bool:
        return self._rank == 1 or self._rank == 9

@dataclass
@total_ordering
class HonorTile:
    _symbol: Wind | Dragon

    def __hash__(self) -> int:
        return hash((__class__.__name__, self._symbol))

    def __str__(self) -> str:
        return f'({self._symbol})'

    def __lt__(self, other: object) -> bool:
        match other:
            case SuitedTile():
                return False
            case HonorTile(_symbol=symbol):
                return self._symbol < symbol
            case _:
                raise TypeError

Tile = SuitedTile | HonorTile

# ---

class TileFactory:
    def create_tile(self, raw: str) -> Tile:
        if len(raw) != 2:
            raise ValueError(f'Raw string "{raw}" passed to TileFactory is not of length 2.')
        else:
            if not raw[0].isdigit():
                raise ValueError(f'Raw string "{raw}" passed to TileFactory does not have a numerical rank.')
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
                            return HonorTile(w)
                    for d in Dragon:
                        if d.value == int(n):
                            return HonorTile(d)
                    raise ValueError('Invalid honor tile passed to TileFactory')
                case _:
                    raise ValueError('Invalid tile kind passed to TileFactory')