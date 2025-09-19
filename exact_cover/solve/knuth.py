import collections.abc

import exact_cover.cover

from .base import Solver

class AlgorithmX(Solver):
    def solve[ChoiceT, ConstraintT](
        self,
        cov: exact_cover.cover.Cover[ChoiceT, ConstraintT],
    ) -> collections.abc.Generator[set[ChoiceT]]:
        if not isinstance(cov, exact_cover.cover.MutableCover): # pragma: no cover
            raise ValueError("Non-mutable cover too slow.")

        yield from self.solve_rec(cov, set())

    def solve_rec[ChoiceT, ConstraintT](
        self,
        cov: exact_cover.cover.MutableCover[ChoiceT, ConstraintT],
        acc: collections.abc.Set[ChoiceT],
    ) -> collections.abc.Generator[set[ChoiceT]]:
        try:
            constraint = cov.next_constraint()
        except StopIteration:
            yield set(acc)
            return

        for choice_it in cov.get_choices(constraint):
            acc_it = acc | {choice_it}
            constraints_satisfied = cov.get_constraints(choice_it)

            choices_invalidated = [
                choice_it
                for constraint_it in constraints_satisfied
                for choice_it in cov.get_choices(constraint_it)
            ]
            choices_invalidated = list(set(choices_invalidated))

            for choice_it in choices_invalidated:
                cov.drop_choice(choice_it)

            for constraint_it in constraints_satisfied:
                cov.drop_constraint(constraint_it)

            yield from self.solve_rec(cov, acc_it)

            for constraint_it in reversed(constraints_satisfied):
                cov.restore_constraint(constraint_it)

            for choice_it in reversed(choices_invalidated):
                cov.restore_choice(choice_it)
