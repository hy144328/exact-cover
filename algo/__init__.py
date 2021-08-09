#!/usr/bin/env python3

import abc
import pandas as pd


class Cover:
    @abc.abstractmethod
    def next_col(self):
        ...

    @abc.abstractmethod
    def choose_rows(self, col) -> tuple:
        ...

    @abc.abstractmethod
    def choose_cols(self, row) -> tuple:
        ...

    @abc.abstractmethod
    def delete_rows(self, rows: tuple):
        ...

    @abc.abstractmethod
    def delete_cols(self, cols: tuple):
        ...

    @abc.abstractmethod
    def restore_rows(self, rows: tuple):
        ...

    @abc.abstractmethod
    def restore_cols(self, cols: tuple):
        ...


class IncidenceMatrix(Cover, pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)

        self.current_index = self.index
        self.current_columns = self.columns
        self.current = self.loc[self.current_index, self.current_columns]

    def next_col(self):
        return self.current_columns[0]

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
    @staticmethod
    def solve(A: Cover, solutions: list[tuple] = None, res: tuple = None):
        if solutions is None:
            solutions = []

        if res is None:
            res = tuple()

        try:
            col = A.next_col()
        except IndexError:
            solutions.append(res)
            return solutions

        for row_it in A.choose_rows(col):
            res_it = res + (row_it, )
            cols_removed = A.choose_cols(row_it)

            rows_removed = set()
            for col_it in cols_removed:
                rows_removed |= set(A.choose_rows(col_it))

            A.delete_rows(rows_removed)
            A.delete_cols(cols_removed)

            AlgorithmX.solve(A, solutions, res_it)

            A.restore_cols(cols_removed)
            A.restore_rows(rows_removed)

        return solutions

