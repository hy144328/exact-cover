#!/usr/bin/env python3

import pandas as pd

from exact_cover.cover import links as cover_links
from . import Sudoku


class DancingLinks(Sudoku, cover_links.DancingLinks):
    @classmethod
    def read_csv(cls, df: pd.DataFrame) -> "DancingLinks":
        choices = Sudoku.build_choices(df)
        constraints = Sudoku.build_constraints(df)
        new_df = pd.DataFrame(
            0,
            index=choices,
            columns=constraints,
            dtype=int,
        )

        res = DancingLinks(choices, constraints)
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
                        res.insert(cover_links.Node(), choice_it, constraint_it)

                    # Column.
                    constraint_it = cls.index_constraint_column(col_it, val_it)
                    if constraint_it in new_df.columns:
                        res.insert(cover_links.Node(), choice_it, constraint_it)

                    # Block.
                    block_it = cls.index_block(row_it, col_it)
                    constraint_it = cls.index_constraint_block(block_it, val_it)
                    if constraint_it in new_df.columns:
                        res.insert(cover_links.Node(), choice_it, constraint_it)

                    # Position.
                    constraint_it = cls.index_constraint_position(row_it, col_it)
                    if constraint_it in new_df.columns:
                        res.insert(cover_links.Node(), choice_it, constraint_it)

        return res
