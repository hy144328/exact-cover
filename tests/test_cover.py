import abc
import functools
import json

import pytest

import exact_cover.cover
import exact_cover.solve

class Wiki:
    @pytest.fixture
    @abc.abstractmethod
    def cover(self) -> exact_cover.cover.Cover[str, int]:
        raise NotImplementedError()

    @pytest.fixture
    @abc.abstractmethod
    def solver(self) -> exact_cover.solve.Solver:
        raise NotImplementedError()

    def test(
        self,
        cover: exact_cover.cover.Cover[str, int],
        solver: exact_cover.solve.Solver,
    ):
        solutions = list(solver.solve(cover))

        assert len(solutions) == 1
        assert solutions[0] == {"B", "D", "F"}

class WikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self) -> exact_cover.cover.IncidenceMatrix[str, int]:
        with open("tests/wiki.json") as f:
            data: dict[str, list[int]] = json.load(f)
            choices = sorted(data.keys())
            constraints = sorted(functools.reduce(lambda l, r: l | set(r), data.values(), set()))

        return exact_cover.cover.IncidenceMatrix(choices, constraints, data)

class WikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self) -> exact_cover.cover.DancingLinks[str, int]:
        with open("tests/wiki.json") as f:
            data: dict[str, list[int]] = json.load(f)
            choices = sorted(data.keys())
            constraints = sorted(functools.reduce(lambda l, r: l | set(r), data.values(), set()))

        cov = exact_cover.cover.DancingLinks(choices, constraints)
        for choice_it in data:
            for constraint_it in data[choice_it]:
                cov.create_node(choice_it, constraint_it)

        return cov

class WikiConstraintProgramming(Wiki):
    @pytest.fixture
    def solver(self) -> exact_cover.solve.ConstraintProgramming:
        return exact_cover.solve.ConstraintProgramming()

class WikiAlgorithmX(Wiki):
    @pytest.fixture
    def solver(self) -> exact_cover.solve.AlgorithmX:
        return exact_cover.solve.AlgorithmX()

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

class TestWikiAlgorithmXDancingLinks(
    WikiAlgorithmX,
    WikiDancingLinks,
):
    ...
