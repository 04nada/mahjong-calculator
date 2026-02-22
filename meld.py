from dataclasses import dataclass
from functools import total_ordering

from meld_enums import ClosedMeldKind, MeldKind, OpenMeldKind
from tile import SuitedTile, Tile, TileFactory

# ---

@dataclass
@total_ordering
class Meld:
    _tiles: list[Tile]
    _is_open: bool = False

    def __len__(self) -> int:
        return len(self._tiles)

    def __repr__(self) -> str:
        return f'{'Open' if self._is_open else 'Closed'}Meld[{' '.join([*map(repr, self._tiles)])}]'

    def __str__(self) -> str:
        return f'{'Open' if self._is_open else 'Closed'}Meld[{' '.join([*map(str, self._tiles)])}]'

    def __lt__(self, other: object) -> bool:
        match other:
            case Meld(_tiles=tiles, _is_open=is_open):
                return (self._tiles, self._is_open) < (tiles, is_open)
            case _:
                raise ValueError
            
    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    @property
    def meld_kind(self) -> MeldKind | None:
        match len(self._tiles):
            case 3:
                if self._tiles[0] == self._tiles[1] == self._tiles[2]:
                    return OpenMeldKind.PON if self._is_open else ClosedMeldKind.TRIPLET
                else:
                    match self._tiles[0]:
                        case SuitedTile(_rank=rank, _suit=suit):
                            if rank <= 7 and self._tiles[1] == SuitedTile(rank+1, suit) and self._tiles[2] == SuitedTile(rank+2, suit):
                                return OpenMeldKind.CHII if self._is_open else ClosedMeldKind.SEQUENCE
                            else:
                                return None
                        case _:
                            return None
            case 4:
                if self._is_open and self._tiles[0] == self._tiles[1] == self._tiles[2] == self._tiles[3]:
                    return OpenMeldKind.KAN
                else:
                    return None
            case _:
                return None
            
# ---

class MeldFactory:
    _tile_factory: TileFactory

    def __init__(self, tile_factory: TileFactory):
        self._tile_factory = tile_factory

    def create_meld(self, raw: str, is_open: bool = False) -> Meld:
        tiles: list[Tile] = []

        try:
            ranks = raw[:-1]
            suit = raw[-1]

            for rank_str in ranks:
                tiles.append(self._tile_factory.create_tile(f'{rank_str}{suit}'))
        except:
            raise ValueError

        return Meld(tiles, is_open)