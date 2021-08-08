#!/usr/bin/env python3

from collections.abc import Iterable

import pandas as pd


class Table(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)

    def choose_rows(self, col) -> Iterable:
        return [row_it for row_it in self.index if self.at[row_it, col] == 1]

    def choose_cols(self, row) -> Iterable:
        return [col_it for col_it in self.columns if self.at[row, col_it] == 1]

    def delete_rows(self, rows: Iterable) -> "Table":
        new_index = set(self.index) - set(rows)
        return Table(self.loc[new_index, :])

    def delete_cols(self, cols: Iterable) -> "Table":
        new_columns = set(self.columns) - set(cols)
        return Table(self.loc[:, new_columns])


class AlgorithmX:
    @classmethod
    def solve(cls, A: Table, res=None) -> list:
        if not res:
            res = []

        if len(A.columns) == 0:
            return res, True

        col = next(iter(A.columns))
        for row_it in A.choose_rows(col):
            res_it = res + [row_it]
            cols_removed = A.choose_cols(row_it)

            rows_removed = set()
            for col_it in cols_removed:
                rows_removed |= set(A.choose_rows(col_it))

            new_A = A
            new_A = new_A.delete_rows(rows_removed)
            new_A = new_A.delete_cols(cols_removed)
            new_res, new_stat = cls.solve(new_A, res_it)
            if new_stat:
                return new_res, True

        return res, False

