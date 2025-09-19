import collections.abc

import pulp

import exact_cover.cover

from .base import Solver

class ConstraintProgramming(Solver):
    def solve[ChoiceT, ConstraintT](
        self,
        cov: exact_cover.cover.Cover[ChoiceT, ConstraintT],
    ) -> collections.abc.Generator[set[ChoiceT]]:
        prob = pulp.LpProblem()
        choices = {
            choice_it: pulp.LpVariable(str(choice_it), 0, 1, pulp.LpInteger)
            for choice_it in cov.choices
        }

        for constraint_it in cov.constraints:
            prob += pulp.lpSum(
                vector = [
                    choices[choice_it]
                    for choice_it in cov.get_choices(constraint_it)
                ],
            ) == 1

        prob.solve()
        yield {
            next(k for k, v in choices.items() if var_it is v)
            for var_it in prob.variables()
            if var_it.varValue == 1
        }
