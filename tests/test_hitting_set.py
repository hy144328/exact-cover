import pytest

import exact_cover.hitting_set.incidence
import exact_cover.hitting_set.links

import tests.test_cover

class WikiIncidenceMatrix(tests.test_cover.Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> exact_cover.hitting_set.incidence.IncidenceMatrix:
        return exact_cover.hitting_set.incidence.IncidenceMatrix.read_json(data)

class WikiDancingLinks(tests.test_cover.Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> exact_cover.hitting_set.links.DancingLinks:
        return exact_cover.hitting_set.links.DancingLinks.read_json(data)

class WikiAlgorithmX(tests.test_cover.WikiAlgorithmX):
    @pytest.fixture
    def solution(self) -> tuple:
        return (1, 2, 5)

class WikiConstraintProgramming(tests.test_cover.WikiConstraintProgramming):
    @pytest.fixture
    def solution(self) -> tuple:
        return ("1", "2", "5")

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
