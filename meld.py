from dataclasses import dataclass
from functools import total_ordering

from meld_enums import ClosedMeldKind, MeldKind, OpenMeldKind
from tile import SuitedTile, Tile, TileFactory

# ---

@dataclass
@total_ordering
class Meld:
    tiles: list[Tile]
    is_open: bool = False

    def __len__(self) -> int:
        return len(self.tiles)

    def __repr__(self) -> str:
        return f'{'Open' if self.is_open else 'Closed'}Meld[{' '.join([*map(repr, self.tiles)])}]'

    def __str__(self) -> str:
        return f'{'Open' if self.is_open else 'Closed'}Meld[{' '.join([*map(str, self.tiles)])}]'

    def __lt__(self, other: object) -> bool:
        match other:
            case Meld(tiles=tiles, is_open=is_open):
                return (self.tiles, self.is_open) < (tiles, is_open)
            case _:
                raise ValueError

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
            
# ---

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