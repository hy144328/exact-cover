import abc
import os
import pandas as pd

import pytest

from exact_cover.cover import Cover
from tests import test_cover as cover_test_wiki

from exact_cover.sudoku import Sudoku
from exact_cover.sudoku.incidence import IncidenceMatrix
from exact_cover.sudoku.links import DancingLinks

class Wiki:
    @pytest.fixture
    def file_path(self):
        return os.path.join(
            os.path.dirname(__file__),
            "wiki.csv",
        )

    @pytest.fixture
    def df(self, file_path: str) -> pd.DataFrame:
        with open(file_path, 'r') as f:
            df = pd.read_csv(f, header=None)
        return df

    @abc.abstractmethod
    def cover(self, df: pd.DataFrame) -> Cover:
        ...

    @abc.abstractmethod
    def solve(self, cover: Cover) -> list[tuple]:
        ...

    def test(self, df: pd.DataFrame, cover: Cover):
        solutions = self.solve(cover)
        for sol_it in solutions:
            new_df = pd.DataFrame(df)
            for choice_it in sol_it:
                new_df.iloc[int(choice_it[0]), int(choice_it[1])] = choice_it[2]
            print(new_df)

        # Rows.
        for row_it in range(9):
            for val_it in range(1, 10):
                assert Sudoku.check_row(df, row_it, val_it, 1)

        # Columns.
        for col_it in range(9):
            for val_it in range(1, 10):
                assert Sudoku.check_column(df, col_it, val_it, 1)

        # Blocks.
        for block_it in range(9):
            for val_it in range(1, 10):
                assert Sudoku.check_block(df, block_it, val_it, 1)

        # Positions.
        for row_it in range(9):
            for col_it in range(9):
                assert Sudoku.check_position(df, row_it, col_it, 1)

class WikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, df: pd.DataFrame) -> IncidenceMatrix:
        return IncidenceMatrix.read_csv(df)

class WikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, df: pd.DataFrame) -> DancingLinks:
        return DancingLinks.read_csv(df)

class TestWikiAlgorithmXIncidenceMatrix(
    cover_test_wiki.WikiAlgorithmX,
    WikiIncidenceMatrix,
):
    ...

class TestWikiAlgorithmXDancingLinks(
    cover_test_wiki.WikiAlgorithmX,
    WikiDancingLinks,
):
    ...

class TestWikiConstraintProgrammingIncidenceMatrix(
    cover_test_wiki.WikiConstraintProgramming,
    WikiIncidenceMatrix,
):
    ...

class TestWikiConstraintProgrammingDancingLinks(
    cover_test_wiki.WikiConstraintProgramming,
    WikiDancingLinks,
):
    ...
