#!/usr/bin/env python3

import abc
from collections.abc import Sequence
import json
import os
import pytest

from . import AlgorithmX, Cover
from .incidence import IncidenceMatrix
from .links import DancingLinks


class Wiki:
    @pytest.fixture
    def file_path(self) -> str:
        return os.path.join(
            os.path.dirname(__file__),
            "wiki.json",
        )

    @pytest.fixture
    def data(self, file_path: str) -> dict[object, Sequence]:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    @abc.abstractmethod
    def cover(self, data: dict[object, Sequence]) -> Cover:
        ...

    def test(self, cover: Cover):
        solutions = AlgorithmX.solve(cover)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == ("B", "D", "F")


class TestWikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, Sequence]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)


class TestWikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, Sequence]) -> DancingLinks:
        return DancingLinks.read_json(data)
