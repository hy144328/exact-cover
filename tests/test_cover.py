import abc
import functools
import json

import pytest

import exact_cover.cover
import exact_cover.solve

class Wiki:
    @pytest.fixture
    @abc.abstractmethod
    def cover(self) -> exact_cover.cover.Cover:
        raise NotImplementedError()

    @pytest.fixture
    @abc.abstractmethod
    def solver(self) -> exact_cover.solve.Solver:
        raise NotImplementedError()

    def test(
        self,
        cover: exact_cover.cover.Cover,
        solver: exact_cover.solve.Solver,
    ):
        solutions = list(solver.solve(cover))

        assert len(solutions) == 1
        assert solutions[0] == {"B", "D", "F"}

class WikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self) -> exact_cover.cover.IncidenceMatrix:
        with open("tests/wiki.json") as f:
            data: dict[str, list[int]] = json.load(f)
            choices = sorted(data.keys())
            constraints = sorted(functools.reduce(lambda l, r: l | set(r), data.values(), set()))

        return exact_cover.cover.IncidenceMatrix(sorted(choices), sorted(constraints), data)

#class WikiDancingLinks(Wiki):
#    @pytest.fixture
#    def cover(self) -> exact_cover.cover.links.DancingLinks:
#        return exact_cover.cover.links.DancingLinks.read_json(data)
#
#class WikiAlgorithmX:
#    def solve(self, cover: exact_cover.cover.Cover) -> list[tuple]:
#        return exact_cover.cover.AlgorithmX.solve(cover)

class WikiConstraintProgramming(Wiki):
    @pytest.fixture
    def solver(self) -> exact_cover.solve.ConstraintProgramming:
        return exact_cover.solve.ConstraintProgramming()

#class TestWikiAlgorithmXIncidenceMatrix(
#    WikiAlgorithmX,
#    WikiIncidenceMatrix,
#):
#    ...
#
#class TestWikiAlgorithmXDancingLinks(
#    WikiAlgorithmX,
#    WikiDancingLinks,
#):
#    ...

class TestWikiConstraintProgrammingIncidenceMatrix(
    WikiConstraintProgramming,
    WikiIncidenceMatrix,
):
    ...

#class TestWikiConstraintProgrammingDancingLinks(
#    WikiConstraintProgramming,
#    WikiDancingLinks,
#):
#    ...
