#!/usr/bin/env python3

from collections.abc import Sequence

import numpy as np
import pandas as pd


class Sudoku:
    @classmethod
    def build_index(cls, df: pd.DataFrame) -> Sequence:
        return [
            cls.index_choice(row_it, col_it, val_it)
            for row_it in range(9)
            for col_it in range(9)
            for val_it in range(1, 10)
            if cls.check_position(df, row_it, col_it)
            and cls.check_row(df, row_it, val_it)
            and cls.check_column(df, col_it, val_it)
            and cls.check_block(df, cls.index_block(row_it, col_it), val_it)
        ]

    @classmethod
    def build_columns(cls, df: pd.DataFrame) -> Sequence:
        res = []

        # Rows.
        res += [
            cls.index_constraint_row(constraint_idx, constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_row(df, constraint_idx, constraint_val)
        ]

        # Columns.
        res += [
            cls.index_constraint_column(constraint_idx, constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_column(df, constraint_idx, constraint_val)
        ]

        # Blocks.
        res += [
            cls.index_constraint_block(constraint_idx, constraint_val)
            for constraint_idx in range(9)
            for constraint_val in range(1, 10)
            if cls.check_block(df, constraint_idx, constraint_val)
        ]

        # Positions.
        res += [
            cls.index_constraint_position(row_it, col_it)
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
    def check_position(df: pd.DataFrame, row: int, col: int, no_occurrences=0) -> bool:
        return len(df.at[row, col].strip()) == no_occurrences

    @staticmethod
    def index_block(row: int, col: int) -> int:
        return 3 * (row // 3) + (col // 3)

    @staticmethod
    def index_choice(row: int, col: int, val: int) -> str:
        return str(row) + str(col) + str(val)

    @staticmethod
    def _index_constraint(type_id: str, idx: int, val: int) -> str:
        return type_id + str(idx) + str(val)

    @classmethod
    def index_constraint_row(cls, idx: int, val: int) -> str:
        return cls._index_constraint("r", idx, val)

    @classmethod
    def index_constraint_column(cls, idx: int, val: int) -> str:
        return cls._index_constraint("c", idx, val)

    @classmethod
    def index_constraint_block(cls, idx: int, val: int) -> str:
        return cls._index_constraint("b", idx, val)

    @classmethod
    def index_constraint_position(cls, row: int, col: int) -> str:
        return "p" + str(row) + str(col)
