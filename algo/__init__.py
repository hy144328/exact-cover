#!/usr/bin/env python3

from collections.abc import Iterable

import pandas as pd


class Table(pd.DataFrame):
    def __init__(self, data):
        rows = list(data.keys())
        no_rows = len(rows)

        cols = set()
        cols = list(cols.union(*data.values()))
        no_cols = len(cols)

        super().__init__(
            0,
            index=rows,
            columns=cols,
            dtype=int,
        )

        for row_it in wiki_data:
            self.loc[row_it, wiki_data[row_it]] = 1

    def choose_rows(self, col) -> Iterable:
        return (row_it for row_it in self.index if self.loc[row_it, col] == 1)

    def choose_cols(self, row) -> Iterable:
        return (col_it for col_it in self.columns if self.loc[row, col_it] == 1)

    def delete_rows(self, rows: Iterable) -> "Table":
        new_index = self.index - rows
        return self.loc[new_index, :]

    def delete_cols(self, cols: Iterable) -> "Table":
        new_columns = self.columns - cols
        return self.loc[:, new_columns]


class AlgorithmX:
    @staticmethod
    def solve(A: Table) -> list:
        pass


if __name__ == "__main__":
    import json
    import os

    file_path = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        "cover",
        "wiki.json",
    )

    with open(file_path, 'r') as f:
        wiki_data = json.load(f)
    t = Table(wiki_data)

    print(t)

