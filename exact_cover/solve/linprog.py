# Copyright (C) 2025  Hans Yu <hans.yu@outlook.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import collections.abc

import pulp

import exact_cover.cover

from . import base

class ConstraintProgramming(base.Solver):
    def solve[ChoiceT, ConstraintT](
        self,
        cov: exact_cover.cover.Cover[ChoiceT, ConstraintT],
    ) -> collections.abc.Generator[set[ChoiceT]]:
        prob = pulp.LpProblem()
        choices = {
            choice_it: pulp.LpVariable(str(choice_it), 0, 1, pulp.LpInteger)
            for choice_it in cov.choices
        }
        constraints = {
            constraint_it: []
            for constraint_it in cov.constraints
        }

        for choice_it in cov.choices:
            for constraint_it in cov.get_constraints(choice_it):
                constraints[constraint_it].append(choices[choice_it])

        for constraint_it in constraints.values():
            prob += (pulp.lpSum(constraint_it) == 1)

        prob.solve()
        yield {
            next(k for k, v in choices.items() if var_it is v)
            for var_it in prob.variables()
            if var_it.varValue == 1
        }
