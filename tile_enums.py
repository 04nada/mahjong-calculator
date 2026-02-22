from enum import Enum, auto
from functools import total_ordering

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