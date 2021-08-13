#!/usr/bin/env python3

import pytest

from cover import test_wiki as cover_test_wiki
from .incidence import IncidenceMatrix
from .links import DancingLinks


class Wiki(cover_test_wiki.Wiki):
    @pytest.fixture
    def solution(self) -> tuple:
        return (1, 2, 5)


class TestWikiIncidenceMatrix(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> IncidenceMatrix:
        return IncidenceMatrix.read_json(data)


class TestWikiDancingLinks(Wiki):
    @pytest.fixture
    def cover(self, data: dict[object, list]) -> DancingLinks:
        return DancingLinks.read_json(data)
