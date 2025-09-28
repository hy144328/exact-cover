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

import collections.abc
import copy
import itertools

import exact_cover.cover
import exact_cover.solve

from . import types, util

class Sudoku:
    ROW_SEP = "\n" + "---".join("++++") + "\n"
    COL_SEP = "|"

    def __init__(self):
        self.data: list[list[int | None]] = [
            [None for _ in range(9)]
            for _ in range(9)
        ]

    def __getitem__(self, ij: tuple[int, int]) -> int | None:
        i, j = ij
        return self.data[i][j]

    def __setitem__(self, ij: tuple[int, int], val: int | None):
        i, j = ij
        self.data[i][j] = val

    def __str__(self) -> str:
        return Sudoku.ROW_SEP + Sudoku.ROW_SEP.join(
            [
                "\n".join(
                    [
                        Sudoku.COL_SEP + Sudoku.COL_SEP.join(
                            [
                                "".join(
                                    [
                                        str(col_it)
                                        if col_it is not None
                                        else " "
                                        for col_it in col_group_it
                                    ]
                                )
                                for col_group_it in itertools.batched(row_it, 3)
                            ]
                        ) + Sudoku.COL_SEP
                        for row_it in row_group_it
                    ]
                )
                for row_group_it in itertools.batched(self.data, 3)
            ]
        ) + Sudoku.ROW_SEP

    def __copy__(self) -> "Sudoku":
        res = Sudoku()

        for row_it in range(9):
            for col_it in range(9):
                val_it = self[row_it, col_it]
                if val_it is None:
                    continue

                res[row_it, col_it] = val_it

        return res

    def build_cover(self) -> exact_cover.cover.DancingLinks[types.ChoiceK, types.ConstraintK]:
        choices = list(itertools.product(range(9), range(9), range(1, 10)))
        constraints = [
            util.identify_row_constraint(row_it, val_it)
            for row_it in range(9)
            for val_it in range(1, 10)
        ] + [
            util.identify_column_constraint(col_it, val_it)
            for col_it in range(9)
            for val_it in range(1, 10)
        ] + [
            util.identify_block_constraint(block_it // 3, block_it % 3, val_it)
            for block_it in range(9)
            for val_it in range(1, 10)
        ] + [
            util.identify_placement_constraint(row_it, col_it)
            for row_it in range(9)
            for col_it in range(9)
        ]
        res = exact_cover.cover.DancingLinks(choices, constraints)

        for row_it in range(9):
            for col_it in range(9):
                for val_it in range(1, 10):
                    choice_it = util.identify_choice(row_it, col_it, val_it)

                    res.create_node(choice_it, util.identify_row_constraint(row_it, val_it))
                    res.create_node(choice_it, util.identify_column_constraint(col_it, val_it))
                    res.create_node(choice_it, util.identify_block_constraint(row_it // 3, col_it // 3, val_it))
                    res.create_node(choice_it, util.identify_placement_constraint(row_it, col_it))

        for row_it in range(9):
            for col_it in range(9):
                val_it = self[row_it, col_it]
                if val_it is None:
                    continue

                choice_it = util.identify_choice(row_it, col_it, val_it)
                res.choose(choice_it)

        return res

    def solve(self, solver: exact_cover.solve.Solver) -> collections.abc.Generator["Sudoku"]:
        cov = self.build_cover()

        for sol_it in solver.solve(cov):
            res_it = copy.copy(self)

            for row_it, col_it, val_it in sol_it:
                res_it[row_it, col_it] = val_it

            yield res_it
