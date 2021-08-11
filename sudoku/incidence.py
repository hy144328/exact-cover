#!/usr/bin/env python3

import pandas as pd

from cover import incidence as cover_incidence


class IncidenceMatrix(cover_incidence.IncidenceMatrix):
    @staticmethod
    def read_csv(file_path):
        with open(file_path, 'r') as f:
            df = pd.read_csv(f, header=None)

        rows = IncidenceMatrix.build_index(df)
        cols = IncidenceMatrix.build_columns(df)
        new_df = pd.DataFrame(
            0,
            index=rows,
            columns=cols,
            dtype=int,
        )

        for row_it in range(9):
            for col_it in range(9):
                val_it = df.at[row_it, col_it]
                if val_it != " ":
                    continue

                for val_it in range(1, 10):
                    index_it = str(row_it) + str(col_it) + str(val_it)
                    if index_it not in new_df.index:
                        continue

                    # Row.
                    column_it = "r" + str(row_it) + str(val_it)
                    if column_it in new_df.columns:
                        new_df.loc[index_it, column_it] = 1

                    # Column.
                    column_it = "c" + str(col_it) + str(val_it)
                    if column_it in new_df.columns:
                        new_df.loc[index_it, column_it] = 1

                    # Block.
                    column_it = "b" + str(3 * (row_it // 3) + (col_it // 3)) + str(val_it)
                    if column_it in new_df.columns:
                        new_df.loc[index_it, column_it] = 1

                    # Position.
                    column_it = "p" + str(row_it) + str(col_it)
                    if column_it in new_df.columns:
                        new_df.loc[index_it, column_it] = 1

        return IncidenceMatrix(new_df)

    @staticmethod
    def build_index(df):
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

    @staticmethod
    def build_columns(df):
        res = []

        # Rows.
        res += [
            "r" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if str(constraint_val) not in set(df.loc[constraint_idx, :])
        ]

        # Columns.
        res += [
            "c" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if str(constraint_val) not in set(df.loc[:, constraint_idx])
        ]

        # Blocks.
        res += [
            "b" + str(constraint_idx) + str(constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if str(constraint_val) not in df.loc[
                (3 * (constraint_idx // 3)):(3 * (constraint_idx // 3) + 2),
                (3 * (constraint_idx % 3)):(3 * (constraint_idx % 3) + 2)
            ].values
        ]

        # Positions.
        res += [
            "p" + str(row_it) + str(col_it)
            for row_it in range(9)
            for col_it in range(9)
            if df.at[row_it, col_it] == " "
        ]

        return res

