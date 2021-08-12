#!/usr/bin/env python3

import json
import os
import pytest

from . import AlgorithmX
from .incidence import IncidenceMatrix


class TestWiki:
    @pytest.fixture
    def file_path(self) -> str:
        return os.path.join(
            os.path.dirname(__file__),
            "wiki.json",
        )

    @pytest.fixture
    def data(self, file_path: str) -> dict[object, list]:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)

    def test(self, cover):
        solutions = AlgorithmX.solve(cover)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == ("B", "D", "F")

