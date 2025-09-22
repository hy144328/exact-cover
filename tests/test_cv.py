import cv2 as cv
import numpy as np
import numpy.typing as npt
import pytest

import exact_cover.sudoku.cv
import exact_cover.sudoku.ocr

@pytest.fixture
def detector() -> exact_cover.sudoku.cv.SudokuDetector:
    return exact_cover.sudoku.cv.SudokuDetector()

def test_normalize_contour(detector: exact_cover.sudoku.cv.SudokuDetector):
    cnt = np.array(
        [
            [[5, 6]],
            [[5, 379]],
            [[378, 379]],
            [[378, 6]],
        ]
    )

    res = detector.normalize_contour(cnt)
    sol = np.array(
        [
            [[5, 6]],
            [[378, 6]],
            [[378, 379]],
            [[5, 379]],
        ]
    )

    assert np.array_equal(res, sol)

@pytest.fixture
def img() -> npt.NDArray[np.uint8]:
    res = cv.imread(
        "assets/Screenshot from 2022-01-02 21-00-15.png",
        cv.IMREAD_GRAYSCALE,
    )
    return res

@pytest.fixture
def sol() -> list[list[int | None]]:
    res: list[list[int | None]] = [
        [
            None
            for _ in range(9)
        ]
        for _ in range(9)
    ]

    with open("assets/Screenshot from 2022-01-02 21-00-15.csv") as f:
        data = [
            line_it.split(",")
            for line_it in f
        ]

    for row_it in range(9):
        for col_it in range(9):
            try:
                res[row_it][col_it] = int(data[row_it][col_it])
            except ValueError:
                pass

    return res

def test(
    img: npt.NDArray[np.uint8],
    sol: list[list[int | None]],
    detector: exact_cover.sudoku.cv.SudokuDetector,
):
    img = detector.apply_blur(img)
    img = detector.apply_threshold(img)
    img = next(detector.extract_board(img))

    squares = detector.extract_squares(img)

    for i in range(9):
        for j in range(9):
            img_it = squares[i][j]
            res_it, conf_it = exact_cover.sudoku.ocr.parse_digit(img_it)

            assert (res_it is not None) == (sol[i][j] is not None)
            if conf_it is not None:
                assert conf_it > 0.9
