#!/usr/bin/env python3

from collections.abc import Iterable, Sequence
import pandas as pd

from . import Cover


class IncidenceMatrix(Cover, pd.DataFrame):
    def __init__(self, df: pd.DataFrame) -> "IncidenceMatrix":
        super().__init__(df)

        self.choices: list = self.index
        self.constraints: list = self.columns
        self.current: pd.DataFrame = self.loc[self.choices, self.constraints]

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
                self.constraints,
                key=lambda x: sum(self.current.loc[:, x] == 1),
            )
        except ValueError:
            raise StopIteration

    def choose_choices(self, col) -> Iterable:
        return (row_it for row_it in self.choices if self.at[row_it, col] == 1)

    def choose_constraints(self, row) -> Iterable:
        return (col_it for col_it in self.constraints if self.at[row, col_it] == 1)

    def delete_choices(self, rows: Iterable):
        rows = set(rows)
        self.choices = [
            row_it
            for row_it in self.choices
            if row_it not in rows
        ]
        self.current = self.loc[self.choices, self.constraints]

    def delete_constraints(self, cols: Iterable):
        cols = set(cols)
        self.constraints = [
            col_it
            for col_it in self.constraints
            if col_it not in cols
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_choices(self, rows: Iterable):
        rows = set(rows)
        self.choices = [
            row_it
            for row_it in self.index
            if row_it in self.choices
            or row_it in rows
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_constraints(self, cols: Iterable):
        cols = set(cols)
        self.constraints = [
            col_it
            for col_it in self.columns
            if col_it in self.constraints
            or col_it in cols
        ]
        self.current = self.loc[self.choices, self.constraints]
