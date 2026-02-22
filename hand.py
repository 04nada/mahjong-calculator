from collections import Counter
from dataclasses import dataclass

from meld import Meld, MeldFactory
from tile import HonorTile, SuitedTile, Tile, TileFactory
from tile_enums import Wind

# ---

@dataclass
class Hand:
    _tiles: list[Tile]
    _open_melds: list[Meld]
    _num_kita: int = 0

    def __len__(self) -> int:
        return len(self._tiles)
    
    def __repr__(self) -> str:
        return f'Hand({' '.join([*map(repr, self._tiles), *map(repr, self._open_melds)])}{f' + {self._num_kita} kita' if self._num_kita > 0 else ''})'

    def __str__(self) -> str:
        return f'Hand({' '.join([*map(str, self._tiles), *map(str, self._open_melds)])}{f' + {self._num_kita} kita' if self._num_kita > 0 else ''})'

    @property
    def tiles(self) -> list[SuitedTile | HonorTile]:
        return self._tiles
    @property
    def open_melds(self) -> list[Meld]:
        return self._open_melds
    @property
    def num_kita(self) -> int:
        return self._num_kita

    @property
    def all_tiles(self) -> list[Tile]:
        ret: list[Tile] = []
        ret.extend(self._tiles)

        for m in self._open_melds:
            ret.extend(m.tiles)
        
        return ret

    @property
    def all_tiles_dict(self) -> dict[Tile, int]:
        return dict(Counter(self.all_tiles))

    @property
    def all_tiles_with_kita(self) -> list[Tile]:
        ret: list[Tile] = []
        ret.extend(self._tiles)

        for m in self._open_melds:
            ret.extend(m.tiles)

        for _ in range(self._num_kita):
            ret.append(HonorTile(Wind.NORTH))
        
        return ret

    @property
    def all_tiles_with_kita_dict(self) -> dict[Tile, int]:
        return dict(Counter(self.all_tiles_with_kita))

    @property
    def is_open(self) -> bool:
        return len(self._open_melds) > 0
    
# ---

class HandFactory:
    _tile_factory: TileFactory
    _meld_factory: MeldFactory

    def __init__(self, tile_factory: TileFactory, meld_factory: MeldFactory):
        self._tile_factory = tile_factory
        self._meld_factory = meld_factory

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
                    tiles.append(self._tile_factory.create_tile(f'{rank_str}{suit}'))
            except:
                raise ValueError

        # create Meld instances from open tiles
        for s in raw_open:
            try:
                open_melds.append(self._meld_factory.create_meld(s, True))
            except:
                raise ValueError

        return Hand(tiles, open_melds, num_kita)