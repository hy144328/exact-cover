#!/usr/bin/env python3

from collections.abc import Sequence

import numpy as np
import pandas as pd

from cover import incidence as cover_incidence


class IncidenceMatrix(cover_incidence.IncidenceMatrix):
    @staticmethod
    def read_csv(file_path: str) -> "IncidenceMatrix":
        with open(file_path, 'r') as f:
            df = pd.read_csv(f, header=None)

        choices = IncidenceMatrix.build_index(df)
        constraints = IncidenceMatrix.build_columns(df)
        new_df = pd.DataFrame(
            0,
            index=choices,
            columns=constraints,
            dtype=int,
        )

        for row_it in range(9):
            for col_it in range(9):
                val_it = df.at[row_it, col_it]
                if val_it != " ":
                    continue

                for val_it in range(1, 10):
                    choice_it = str(row_it) + str(col_it) + str(val_it)
                    if choice_it not in new_df.index:
                        continue

                    # Row.
                    constraint_it = "r" + str(row_it) + str(val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Column.
                    constraint_it = "c" + str(col_it) + str(val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Block.
                    constraint_it = "b" + str(3 * (row_it // 3) + (col_it // 3)) + str(val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Position.
                    constraint_it = "p" + str(row_it) + str(col_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

        return IncidenceMatrix(new_df)

    @classmethod
    def build_index(cls, df: pd.DataFrame) -> Sequence:
        return [
            str(row_it) + str(col_it) + str(val_it)
            for row_it in range(9)
            for col_it in range(9)
            for val_it in range(1, 10)
            if df.at[row_it, col_it] == " "
            and str(val_it) not in set(df.loc[row_it, :])
            and str(val_it) not in set(df.loc[:, col_it])
            and str(val_it) not in df.loc[
                (3 * (row_it // 3)):(3 * (row_it // 3) + 2),
                (3 * (col_it // 3)):(3 * (col_it // 3) + 2)
            ].values
        ]

    @classmethod
    def build_columns(cls, df: pd.DataFrame) -> Sequence:
        res = []

        # Rows.
        res += [
            "r" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_row(df, constraint_idx, constraint_val)
        ]

        # Columns.
        res += [
            "c" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_column(df, constraint_idx, constraint_val)
        ]

        # Blocks.
        res += [
            "b" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_block(df, constraint_idx, constraint_val)
        ]

        # Positions.
        res += [
            "p" + str(row_it) + str(col_it)
            for row_it in range(9)
            for col_it in range(9)
            if cls.check_position(df, row_it, col_it)
        ]

        return res

    @staticmethod
    def check_row(df: pd.DataFrame, row: int, val, no_occurrences=0) -> bool:
        return np.count_nonzero(df.iloc[row, :] == str(val)) == no_occurrences

    @staticmethod
    def check_column(df: pd.DataFrame, col: int, val, no_occurrences=0) -> bool:
        return np.count_nonzero(df.iloc[:, col] == str(val)) == no_occurrences

    @staticmethod
    def check_block(df: pd.DataFrame, block: int, val, no_occurrences=0) -> bool:
        row = 3 * (block // 3)
        col = 3 * (block % 3)
        return np.count_nonzero(df.iloc[row:row + 3, col:col + 3] == str(val)) == no_occurrences

    @staticmethod
    def check_position(df: pd.DataFrame, row: int, col: int) -> bool:
        return df.at[row, col] == " "

