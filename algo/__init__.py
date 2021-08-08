#!/usr/bin/env python3

import pandas as pd


class Table(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)
        self.current_index = self.index
        self.current_columns = self.columns
        self.current = self.loc[self.current_index, self.current_columns]

    def choose_rows(self, col) -> tuple:
        return tuple(row_it for row_it in self.current_index if self.at[row_it, col] == 1)

    def choose_cols(self, row) -> tuple:
        return tuple(col_it for col_it in self.current_columns if self.at[row, col_it] == 1)

    def delete_rows(self, rows: tuple):
        self.current_index = [row_it for row_it in self.current_index if row_it not in set(rows)]
        self.current = self.loc[self.current_index, self.current_columns]

    def delete_cols(self, cols: tuple):
        self.current_columns = [col_it for col_it in self.current_columns if col_it not in set(cols)]
        self.current = self.loc[self.current_index, self.current_columns]

    def restore_rows(self, rows: tuple):
        self.current_index = [row_it for row_it in self.index if row_it in self.current_index or row_it in rows]
        self.current = self.loc[self.current_index, self.current_columns]

    def restore_cols(self, cols: tuple):
        self.current_columns = [col_it for col_it in self.columns if col_it in self.current_columns or col_it in cols]
        self.current = self.loc[self.current_index, self.current_columns]


class AlgorithmX:
    @classmethod
    def solve(cls, A: Table, sols: list[tuple], res: tuple = None):
        if len(A.current_columns) == 0:
            sols.append(res)
            return

        if not res:
            res = tuple()

        col = next(iter(A.current_columns))
        for row_it in A.choose_rows(col):
            res_it = res + (row_it, )
            cols_removed = A.choose_cols(row_it)

            rows_removed = set()
            for col_it in cols_removed:
                rows_removed |= set(A.choose_rows(col_it))

            A.delete_rows(rows_removed)
            A.delete_cols(cols_removed)

            cls.solve(A, sols, res_it)

            A.restore_cols(reversed(cols_removed))
            A.restore_rows(reversed(rows_removed))

