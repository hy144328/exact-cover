#!/usr/bin/env python3

from collections.abc import Sequence
import pandas as pd

from . import Cover


class IncidenceMatrix(Cover, pd.DataFrame):
    def __init__(self, df: pd.DataFrame) -> "IncidenceMatrix":
        super().__init__(df)

        self.choices: list = list(self.index)
        self.constraints: list = list(self.columns)
        self.current: pd.DataFrame = self.loc[self.choices, self.constraints]

    @staticmethod
    def read_json(data: dict[object, list]) -> "IncidenceMatrix":
        choices = list(data.keys())
        constraints = set()
        constraints = list(constraints.union(*data.values()))

        df = pd.DataFrame(
            False,
            index=choices,
            columns=constraints,
            dtype=bool,
        )
        for choice_it in data:
            df.loc[choice_it, data[choice_it]] = True

        return IncidenceMatrix(df)

    def next_col(self):
        try:
            return min(
                self.constraints,
                key=lambda x: sum(self.current.loc[:, x] == 1),
            )
        except ValueError:
            raise StopIteration

    def choose_choices(self, col) -> Sequence:
        return (row_it for row_it in self.choices if self.at[row_it, col] == 1)

    def choose_constraints(self, row) -> Sequence:
        return (col_it for col_it in self.constraints if self.at[row, col_it] == 1)

    def delete_choices(self, rows: Sequence):
        rows = set(rows)
        self.choices = [
            row_it
            for row_it in self.choices
            if row_it not in rows
        ]
        self.current = self.loc[self.choices, self.constraints]

    def delete_constraints(self, cols: Sequence):
        cols = set(cols)
        self.constraints = [
            col_it
            for col_it in self.constraints
            if col_it not in cols
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_choices(self, rows: Sequence):
        rows = set(rows)
        self.choices = [
            row_it
            for row_it in self.index
            if row_it in self.choices
            or row_it in rows
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_constraints(self, cols: Sequence):
        cols = set(cols)
        self.constraints = [
            col_it
            for col_it in self.columns
            if col_it in self.constraints
            or col_it in cols
        ]
        self.current = self.loc[self.choices, self.constraints]
