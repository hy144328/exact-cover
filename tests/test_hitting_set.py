#!/usr/bin/env python3

import pytest

from cover import test_wiki as cover_test_wiki

from .incidence import IncidenceMatrix
from .links import DancingLinks


class WikiIncidenceMatrix(cover_test_wiki.Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)


class WikiDancingLinks(cover_test_wiki.Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> DancingLinks:
        return DancingLinks.read_json(data)


class WikiAlgorithmX(cover_test_wiki.WikiAlgorithmX):
    @pytest.fixture
    def solution(self) -> tuple:
        return (1, 2, 5)


class WikiConstraintProgramming(cover_test_wiki.WikiConstraintProgramming):
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
