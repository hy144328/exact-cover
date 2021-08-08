#!/usr/bin/env python3

import json
import os
import pytest

from algo import Table, AlgorithmX
from cover import io

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
        return io.read_json(data)

    @pytest.fixture
    def table(self, data):
        return Table(data)

    def test(self, table):
        sols = []
        AlgorithmX.solve(table, sols)

        assert len(sols) == 1
        assert tuple(sorted(sols[0])) == ("B", "D", "F")

