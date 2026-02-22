from enum import StrEnum

class ClosedMeldKind(StrEnum):
    SEQUENCE = 'Sequence'
    TRIPLET = 'Triplet'

class OpenMeldKind(StrEnum):
    CHII = 'Chii'
    PON = 'Pon'
    KAN = 'Kan'

MeldKind = ClosedMeldKind | OpenMeldKind