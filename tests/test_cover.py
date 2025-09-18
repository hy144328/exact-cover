import abc
import json
import os

import pytest

import exact_cover.cover
import exact_cover.cover.incidence
import exact_cover.cover.links

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
    def cover(self, data: dict[object, list]) -> exact_cover.cover.Cover:
        ...

    @abc.abstractmethod
    def solve(self, cover: exact_cover.cover.Cover) -> list[tuple]:
        ...

    def test(self, cover: exact_cover.cover.Cover, solution: tuple):
        solutions = self.solve(cover)

        assert len(solutions) == 1
        assert tuple(sorted(solutions[0])) == solution

class WikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> exact_cover.cover.incidence.IncidenceMatrix:
        return exact_cover.cover.incidence.IncidenceMatrix.read_json(data)

class WikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> exact_cover.cover.links.DancingLinks:
        return exact_cover.cover.links.DancingLinks.read_json(data)

class WikiAlgorithmX:
    def solve(self, cover: exact_cover.cover.Cover) -> list[tuple]:
        return exact_cover.cover.AlgorithmX.solve(cover)

class WikiConstraintProgramming:
    def solve(self, cover: exact_cover.cover.Cover) -> list[tuple]:
        return exact_cover.cover.ConstraintProgramming.solve(cover)

class TestWikiAlgorithmXIncidenceMatrix(
    WikiAlgorithmX,
    WikiIncidenceMatrix,
):
    ...

class TestWikiAlgorithmXDancingLinks(
    WikiAlgorithmX,
    WikiDancingLinks,
):
    ...

class TestWikiConstraintProgrammingIncidenceMatrix(
    WikiConstraintProgramming,
    WikiIncidenceMatrix,
):
    ...

class TestWikiConstraintProgrammingDancingLinks(
    WikiConstraintProgramming,
    WikiDancingLinks,
):
    ...
