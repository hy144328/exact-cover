#!/usr/bin/env python3

import abc
from collections.abc import Sequence


class Cover:
    @abc.abstractmethod
    def next_constraint(self):
        ...

    @abc.abstractmethod
    def choose_choices(self, constraint) -> Sequence:
        ...

    @abc.abstractmethod
    def choose_constraints(self, choice) -> Sequence:
        ...

    @abc.abstractmethod
    def delete_choices(self, choices: Sequence):
        ...

    @abc.abstractmethod
    def delete_constraints(self, constraints: Sequence):
        ...

    @abc.abstractmethod
    def restore_choices(self, choices: Sequence):
        ...

    @abc.abstractmethod
    def restore_constraints(self, constraints: Sequence):
        ...


class AlgorithmX:
    @staticmethod
    def solve(A: Cover, solutions: list[tuple] = None, res: tuple = None) -> list[tuple]:
        if solutions is None:
            solutions = []

        if res is None:
            res = tuple()

        try:
            constraint = A.next_constraint()
        except StopIteration:
            solutions.append(res)
            return solutions

        for choice_it in A.choose_choices(constraint):
            res_it = res + (choice_it, )
            constraints_removed = list(A.choose_constraints(choice_it))

            choices_removed = set()
            for constraint_it in constraints_removed:
                choices_removed |= set(A.choose_choices(constraint_it))
            choices_removed = list(choices_removed)

            A.delete_choices(choices_removed)
            A.delete_constraints(constraints_removed)

            AlgorithmX.solve(A, solutions, res_it)

            A.restore_constraints(list(reversed(constraints_removed)))
            A.restore_choices(list(reversed(choices_removed)))

        return solutions
