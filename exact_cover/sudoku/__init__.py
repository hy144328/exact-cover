import collections.abc
import copy
import itertools

import exact_cover.cover
import exact_cover.solve

class Sudoku:
    ROW_SEP = "\n" + 20 * "-" + "\n"
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
        rows = [
            "|" + Sudoku.COL_SEP.join(
                [
                    str(col_it)
                    if col_it is not None
                    else " "
                    for col_it in row_it
                ],
            ) + "|"
            for row_it in self.data
        ]

        return 20 * "-" + "\n" + Sudoku.ROW_SEP.join(rows) + "\n" + 20 * "-"

    def __copy__(self) -> "Sudoku":
        res = Sudoku()

        for row_it in range(9):
            for col_it in range(9):
                val_it = self[row_it, col_it]
                if val_it is None:
                    continue

                res[row_it, col_it] = val_it

        return res

    def build_cover(self) -> exact_cover.cover.DancingLinks[tuple[int, int, int], tuple[str, int, int]]:
        choices = list(itertools.product(range(9), range(9), range(1, 10)))
        constraints = [
            ("R", row_it, val_it)
            for row_it in range(9)
            for val_it in range(1, 10)
        ] + [
            ("C", col_it, val_it)
            for col_it in range(9)
            for val_it in range(1, 10)
        ] + [
            ("B", block_it, val_it)
            for block_it in range(9)
            for val_it in range(1, 10)
        ] + [
            ("P", row_it, col_it)
            for row_it in range(9)
            for col_it in range(9)
        ]
        res = exact_cover.cover.DancingLinks(choices, constraints)

        for row_it in range(9):
            for col_it in range(9):
                for val_it in range(1, 10):
                    choice_it = (row_it, col_it, val_it)

                    res.create_node(choice_it, ("R", row_it, val_it))
                    res.create_node(choice_it, ("C", col_it, val_it))
                    res.create_node(choice_it, ("B", 3 * (row_it // 3) + (col_it // 3), val_it))
                    res.create_node(choice_it, ("P", row_it, col_it))

        for row_it in range(9):
            for col_it in range(9):
                val_it = self[row_it, col_it]
                if val_it is None:
                    continue

                choice_it = (row_it, col_it, val_it)
                res.choose(choice_it)

        return res

    def solve(self, solver: exact_cover.solve.Solver) -> collections.abc.Generator["Sudoku"]:
        cov = self.build_cover()

        for sol_it in solver.solve(cov):
            res_it = copy.copy(self)

            for row_it, col_it, val_it in sol_it:
                res_it[row_it, col_it] = val_it

            yield res_it
