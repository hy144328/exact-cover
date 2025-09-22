import numpy as np
import pytest

import exact_cover.sudoku.cv

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
