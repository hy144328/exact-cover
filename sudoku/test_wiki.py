#!/usr/bin/env python3

import os
import pandas as pd
import pytest

from cover import AlgorithmX
from .incidence import IncidenceMatrix


class TestWiki:
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

    @pytest.fixture
    def cover(self, df: pd.DataFrame) -> IncidenceMatrix:
        return IncidenceMatrix.read_csv(df)

    def test(self, cover: IncidenceMatrix):
        print(cover)
        solutions = AlgorithmX.solve(cover)
        print(solutions)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == (1, 2, 5)
