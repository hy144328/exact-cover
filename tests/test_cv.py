import abc
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

class TestCV(abc.ABC):
    @pytest.fixture
    @abc.abstractmethod
    def img(self) -> npt.NDArray[np.uint8]:
        raise NotImplementedError()

    @pytest.fixture
    @abc.abstractmethod
    def sol(self) -> list[list[int | None]]:
        raise NotImplementedError()

    def test(
        self,
        img: npt.NDArray[np.uint8],
        sol: list[list[int | None]],
        detector: exact_cover.sudoku.cv.SudokuDetector,
    ):
        board = next(detector.extract_board(img))
        cv.imwrite("output.d/board.png", board)
        squares = detector.extract_squares(board)

        success = []
        failure = []

        for i in range(9):
            for j in range(9):
                img_it = detector.extract_symbol(squares[i][j])
                res_it, conf_it = exact_cover.sudoku.ocr.parse_digit(img_it)

                if res_it == sol[i][j]:
                    success.append((i, j))
                else:
                    cv.imwrite(f"output.d/square_{i}_{j}.png", img_it)
                    print(f"{i}, {j}: {res_it}/{sol[i][j]} ({conf_it}).")
                    failure.append((i, j))

        assert sum(1 for i, j in success if sol[i][j] is None) == sum(1 for i in range(9) for j in range(9) if sol[i][j] is None)
        assert sum(1 for i, j in success if sol[i][j] is not None) == sum(1 for i in range(9) for j in range(9) if sol[i][j] is not None)

class TestScreenshot1(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/Screenshot from 2022-01-02 21-00-15.png",
            cv.IMREAD_GRAYSCALE,
        )
        return res

    @pytest.fixture
    def sol(self) -> list[list[int | None]]:
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

class TestScreenshot2(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/Screenshot from 2022-01-06 13-35-44.png",
            cv.IMREAD_GRAYSCALE,
        )
        return res

    @pytest.fixture
    def sol(self) -> list[list[int | None]]:
        res: list[list[int | None]] = [
            [
                None
                for _ in range(9)
            ]
            for _ in range(9)
        ]

        with open("assets/Screenshot from 2022-01-06 13-35-44.csv") as f:
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

class TestAakash(TestCV):
    @pytest.fixture
    def img(self) -> npt.NDArray[np.uint8]:
        res = cv.imread(
            "assets/opencv_sudoku_puzzle_sudoku_puzzle-768x817.webp",
            cv.IMREAD_GRAYSCALE,
        )
        return res

    @pytest.fixture
    def sol(self) -> list[list[int | None]]:
        res: list[list[int | None]] = [
            [
                None
                for _ in range(9)
            ]
            for _ in range(9)
        ]

        with open("assets/opencv_sudoku_puzzle_sudoku_puzzle-768x817.csv") as f:
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
