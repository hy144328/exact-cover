from . import types

def identify_choice(
    row: int,
    col: int,
    val: int,
) -> types.ChoiceK:
    return (row, col, val)

def identify_row_constraint(
    row: int,
    val: int,
) -> types.ConstraintK:
    return (
        types.ConstraintType.ROW,
        row,
        val,
    )

def identify_column_constraint(
    col: int,
    val: int,
) -> types.ConstraintK:
    return (
        types.ConstraintType.COLUMN,
        col,
        val,
    )

def identify_block_constraint(
    block_row: int,
    block_col: int,
    val: int,
) -> types.ConstraintK:
    return (
        types.ConstraintType.BLOCK,
        3 * block_row + block_col,
        val,
    )

def identify_placement_constraint(
    row: int,
    col: int,
) -> types.ConstraintK:
    return (
        types.ConstraintType.PLACEMENT,
        row,
        col,
    )
