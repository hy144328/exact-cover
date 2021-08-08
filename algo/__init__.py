#!/usr/bin/env python3

import pandas as pd


class Table(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)

    def choose_rows(self, col) -> list:
        return [row_it for row_it in self.index if self.at[row_it, col] == 1]

    def choose_cols(self, row) -> list:
        return [col_it for col_it in self.columns if self.at[row, col_it] == 1]

    def delete_rows(self, rows: list) -> "Table":
        new_index = [e for e in self.index if e not in set(rows)]
        return Table(self.loc[new_index, :])

    def delete_cols(self, cols: list) -> "Table":
        new_columns = [e for e in self.columns if e not in set(cols)]
        return Table(self.loc[:, new_columns])


class AlgorithmX:
    @classmethod
    def solve(cls, A: Table, sols: list, res: list = None) -> list:
        if len(A.columns) == 0:
            sols.append(res)
            return

        if not res:
            res = []

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
            cls.solve(new_A, sols, res_it)

