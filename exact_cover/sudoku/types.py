import enum

class ConstraintType(enum.Enum):
    ROW = enum.auto()
    COLUMN = enum.auto()
    BLOCK = enum.auto()
    PLACEMENT = enum.auto()

ChoiceK = tuple[int, int, int]
ConstraintK = tuple[ConstraintType, int, int]
