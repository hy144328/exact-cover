#!/usr/bin/env python3

import abc
from collections.abc import Iterable


class Cover:
    @abc.abstractmethod
    def next_col(self):
        ...

    @abc.abstractmethod
    def choose_rows(self, col) -> Iterable:
        ...

    @abc.abstractmethod
    def choose_cols(self, row) -> Iterable:
        ...

    @abc.abstractmethod
    def delete_rows(self, rows: Iterable):
        ...

    @abc.abstractmethod
    def delete_cols(self, cols: Iterable):
        ...

    @abc.abstractmethod
    def restore_rows(self, rows: Iterable):
        ...

    @abc.abstractmethod
    def restore_cols(self, cols: Iterable):
        ...


class AlgorithmX:
    @staticmethod
    def solve(A: Cover, solutions: list[tuple] = None, res: tuple = None) -> list[tuple]:
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
            cols_removed = set(A.choose_cols(row_it))

            rows_removed = set()
            for col_it in cols_removed:
                rows_removed |= set(A.choose_rows(col_it))

            A.delete_rows(rows_removed)
            A.delete_cols(cols_removed)

            AlgorithmX.solve(A, solutions, res_it)

            A.restore_cols(cols_removed)
            A.restore_rows(rows_removed)

        return solutions

