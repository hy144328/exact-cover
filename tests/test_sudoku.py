import abc

import cv2 as cv
import numpy as np
import numpy.typing as npt
import pytest

import exact_cover
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

    def test_representation(
        self,
        sudoku: exact_cover.sudoku.Sudoku,
    ):
        sol = """
+---+---+---+
|53 | 7 |   |
|6  |195|   |
| 98|   | 6 |
+---+---+---+
|8  | 6 |  3|
|4  |8 3|  1|
|7  | 2 |  6|
+---+---+---+
| 6 |   |28 |
|   |419|  5|
|   | 8 | 79|
+---+---+---+
        """
        assert str(sudoku).strip() == sol.strip()

class TestCV(abc.ABC):
    @pytest.fixture
    @abc.abstractmethod
    def img(self) -> npt.NDArray[np.uint8]:
        raise NotImplementedError()

    def test(
        self,
        img: npt.NDArray[np.uint8],
    ):
        puzzle, solutions = exact_cover.parse_and_solve_sudoku(img)

        print("Puzzle:")
        print(puzzle)
        print("\n")

        print("Solutions:")
        for sol_it in solutions:
            print(sol_it)
            print("\n")

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

class TestScreenshot1(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/Screenshot from 2022-01-02 21-00-15.png",
            cv.IMREAD_GRAYSCALE,
        )
        return res

class TestScreenshot2(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/Screenshot from 2022-01-06 13-35-44.png",
            cv.IMREAD_GRAYSCALE,
        )
        return res

class TestAakash(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/opencv_sudoku_puzzle_sudoku_puzzle-768x817.webp",
            cv.IMREAD_GRAYSCALE,
        )
        return res
