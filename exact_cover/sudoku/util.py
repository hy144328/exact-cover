# Copyright (C) 2025  Hans Yu <hans.yu@outlook.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
