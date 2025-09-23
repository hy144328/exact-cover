import collections.abc

import numpy as np
import numpy.typing as npt

import exact_cover.sudoku.cv
import exact_cover.sudoku.ocr

from exact_cover.cover import Cover, DancingLinks, IncidenceMatrix, MutableCover
from exact_cover.solve import AlgorithmX, ConstraintProgramming, Solver
from exact_cover.sudoku import Sudoku

def parse_and_solve_sudoku(
    img: npt.NDArray[np.uint8],
) -> tuple[Sudoku, collections.abc.Generator[Sudoku]]:
    detector = exact_cover.sudoku.cv.SudokuDetector()
    solver = AlgorithmX()
    puzzle = Sudoku()

    board = next(detector.extract_board(img))
    squares = detector.extract_squares(board)

    for i in range(9):
        for j in range(9):
            img_it = detector.extract_symbol(squares[i][j])

            if img_it is None:
                res_it = None
            else:
                res_it, _ = exact_cover.sudoku.ocr.parse_digit(img_it)

                if res_it is None:
                    img_it = detector.cut_region_of_interest(img_it)
                    res_it, _ = exact_cover.sudoku.ocr.parse_digit(img_it)

            puzzle[i, j] = res_it

    return puzzle, puzzle.solve(solver)
