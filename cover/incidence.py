#!/usr/bin/env python3

from collections.abc import Iterable, Sequence
import pandas as pd

from . import Cover


class IncidenceMatrix(Cover, pd.DataFrame):
    def __init__(self, df: pd.DataFrame) -> "IncidenceMatrix":
        super().__init__(df)

        self.current_index: list = self.index
        self.current_columns: list = self.columns
        self.current: pd.DataFrame = self.loc[self.current_index, self.current_columns]

    @staticmethod
    def read_json(data: dict[object, Sequence]) -> "IncidenceMatrix":
        rows = list(data.keys())
        cols = set()
        cols = list(cols.union(*data.values()))

        df = pd.DataFrame(
            0,
            index=rows,
            columns=cols,
            dtype=int,
        )
        for row_it in data:
            df.loc[row_it, data[row_it]] = 1

        return IncidenceMatrix(df)

    def next_col(self):
        try:
            return min(
                self.current_columns,
                key=lambda x: sum(self.current.loc[:, x] == 1),
            )
        except ValueError:
            raise StopIteration

    def choose_rows(self, col) -> Iterable:
        return (row_it for row_it in self.current_index if self.at[row_it, col] == 1)

    def choose_cols(self, row) -> Iterable:
        return (col_it for col_it in self.current_columns if self.at[row, col_it] == 1)

    def delete_rows(self, rows: Iterable):
        rows = set(rows)
        self.current_index = [
            row_it
            for row_it in self.current_index
            if row_it not in rows
        ]
        self.current = self.loc[self.current_index, self.current_columns]

    def delete_cols(self, cols: Iterable):
        cols = set(cols)
        self.current_columns = [
            col_it
            for col_it in self.current_columns
            if col_it not in cols
        ]
        self.current = self.loc[self.current_index, self.current_columns]

    def restore_rows(self, rows: Iterable):
        rows = set(rows)
        self.current_index = [
            row_it
            for row_it in self.index
            if row_it in self.current_index
            or row_it in rows
        ]
        self.current = self.loc[self.current_index, self.current_columns]

    def restore_cols(self, cols: Iterable):
        cols = set(cols)
        self.current_columns = [
            col_it
            for col_it in self.columns
            if col_it in self.current_columns
            or col_it in cols
        ]
        self.current = self.loc[self.current_index, self.current_columns]
