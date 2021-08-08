#!/usr/bin/env python3

import json
import os
import pytest

from algo import IncidenceMatrix
from . import read_json


class TestWiki:
    @pytest.fixture
    def file_path(self):
        return os.path.join(
            os.path.dirname(__file__),
            "wiki.json",
        )

    @pytest.fixture
    def data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return read_json(data)

    @pytest.fixture
    def cover(self, data):
        return IncidenceMatrix(data)

    def test(self, cover):
        cover.solve()

        assert len(cover.solutions) == 1
        assert tuple(sorted(cover.solutions[0])) == ("B", "D", "F")

