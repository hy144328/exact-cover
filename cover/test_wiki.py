#!/usr/bin/env python3

import abc
import json
import os
import pytest

from . import AlgorithmX, Cover
from . import ConstrainedProgramming
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
    def data(self, file_path: str) -> dict[object, list]:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    @pytest.fixture
    def solution(self) -> tuple:
        return ("B", "D", "F")

    @abc.abstractmethod
    def cover(self, data: dict[object, list]) -> Cover:
        ...

    def test(self, cover: Cover, solution: tuple):
        solutions = AlgorithmX.solve(cover)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == solution


class TestWikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)


class TestWikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> DancingLinks:
        return DancingLinks.read_json(data)


class WikiLP(Wiki):
    def test(self, cover: Cover, solution: tuple):
        solutions = ConstrainedProgramming.solve(cover)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == solution


class TestWikiLPIncidenceMatrix(WikiLP):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)
