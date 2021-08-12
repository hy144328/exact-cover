#!/usr/bin/env python3

import os
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
    def cover(self, file_path):
        return IncidenceMatrix.read_csv(file_path)

    def test(self, cover):
        solutions = AlgorithmX.solve(cover)
        print(solutions)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == (1, 2, 5)
