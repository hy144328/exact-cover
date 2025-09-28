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

import numpy as np
import numpy.typing as npt

from . import cv, ocr
from .base import Sudoku

def read_sudoku(
    img: npt.NDArray[np.uint8],
) -> Sudoku:
    detector = cv.SudokuDetector()
    res = Sudoku()

    board = next(detector.extract_board(img))
    squares = detector.extract_squares(board)

    for i in range(9):
        for j in range(9):
            img_it = detector.extract_symbol(squares[i][j])

            if img_it is None:
                res_it = None
            else:
                res_it, _ = ocr.parse_digit(img_it)

                if res_it is None:
                    img_it = detector.cut_region_of_interest(img_it)
                    res_it, _ = ocr.parse_digit(img_it)

            res[i, j] = res_it

    return res
