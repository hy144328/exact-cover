import pytest

import exact_cover.solve
import exact_cover.sudoku

class TestWiki:
    @pytest.fixture
    def sudoku(self) -> exact_cover.sudoku.Sudoku:
        res = exact_cover.sudoku.Sudoku()

        with open("tests/wiki.csv") as f:
            data = [
                line_it.split(",")
                for line_it in f
            ]

        for row_it in range(9):
            for col_it in range(9):
                try:
                    res[row_it, col_it] = int(data[row_it][col_it])
                except ValueError:
                    pass

        return res

    @pytest.fixture
    def solver(self) -> exact_cover.solve.Solver:
        return exact_cover.solve.AlgorithmX()

    def test(
        self,
        sudoku: exact_cover.sudoku.Sudoku,
        solver: exact_cover.solve.Solver,
    ):
        for sol_it in sudoku.solve(solver):
            for row_it in range(9):
                res_it = (
                    sol_it[row_it, col_it]
                    for col_it in range(9)
                )
                assert set(res_it) == set(range(1, 10))

            for col_it in range(9):
                res_it = (
                    sol_it[row_it, col_it]
                    for row_it in range(9)
                )
                assert set(res_it) == set(range(1, 10))

            for block_row_it in range(3):
                for block_col_it in range(3):
                    res_it = (
                        sol_it[row_it, col_it]
                        for row_it in range(3 * block_row_it, 3 * block_row_it + 3)
                        for col_it in range(3 * block_col_it, 3 * block_col_it + 3)
                    )
                    assert set(res_it) == set(range(1, 10))
