#!/usr/bin/env python3

import pandas as pd

from cover import incidence as cover_incidence
from . import Sudoku


class IncidenceMatrix(Sudoku, cover_incidence.IncidenceMatrix):
    @classmethod
    def read_csv(cls, df: pd.DataFrame) -> "IncidenceMatrix":
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
                    choice_it = cls.index_choice(row_it, col_it, val_it)
                    if choice_it not in new_df.index:
                        continue

                    # Row.
                    constraint_it = cls.index_constraint_row(row_it, val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Column.
                    constraint_it = cls.index_constraint_column(col_it, val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Block.
                    block_it = cls.index_block(row_it, col_it)
                    constraint_it = cls.index_constraint_block(block_it, val_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

                    # Position.
                    constraint_it = cls.index_constraint_position(row_it, col_it)
                    if constraint_it in new_df.columns:
                        new_df.loc[choice_it, constraint_it] = 1

        return IncidenceMatrix(new_df)
