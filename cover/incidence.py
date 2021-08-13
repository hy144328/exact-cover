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

    def next_constraint(self):
        try:
            return min(
                self.constraints,
                key=lambda x: sum(self.current.loc[:, x]),
            )
        except ValueError:
            raise StopIteration

    def choose_choices(self, constraint) -> Sequence:
        return [
            choice_it
            for choice_it in self.choices
            if self.at[choice_it, constraint]
        ]

    def choose_constraints(self, choice) -> Sequence:
        return [
            constraint_it
            for constraint_it in self.constraints
            if self.at[choice, constraint_it]
        ]

    def delete_choices(self, choices: Sequence):
        self.choices = [
            choice_it
            for choice_it in self.choices
            if choice_it not in choices
        ]
        self.current = self.loc[self.choices, self.constraints]

    def delete_constraints(self, constraints: Sequence):
        self.constraints = [
            constraint_it
            for constraint_it in self.constraints
            if constraint_it not in constraints
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_choices(self, choices: Sequence):
        self.choices = [
            choice_it
            for choice_it in self.index
            if choice_it in self.choices
            or choice_it in choices
        ]
        self.current = self.loc[self.choices, self.constraints]

    def restore_constraints(self, constraints: Sequence):
        self.constraints = [
            constraint_it
            for constraint_it in self.columns
            if constraint_it in self.constraints
            or constraint_it in constraints
        ]
        self.current = self.loc[self.choices, self.constraints]
