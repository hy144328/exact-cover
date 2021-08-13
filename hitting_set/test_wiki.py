#!/usr/bin/env python3

import pytest

from cover.test_wiki import Wiki
from .incidence import IncidenceMatrix
from .links import DancingLinks


class TestWikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)

    @pytest.fixture
    def solution(self) -> tuple:
        return (1, 2, 5)


class TestWikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> DancingLinks:
        return DancingLinks.read_json(data)
